"""Warm local-model server — load Qwen + the LoRA adapter once, serve over HTTP.

Local generation otherwise spawns a fresh ``mlx_lm generate`` per draft, paying
the ~3s model load every time — fine for one draft, painful for a batch and for
streaming's first token. This wraps ``mlx_lm.server`` (an OpenAI-compatible HTTP
server) so the model is loaded once and reused: every local draft becomes a fast
HTTP call, which is what makes batch-on-local viable.

Scope notes:
  * The server loads a single ``--adapter-path`` at startup — the **global**
    adapter. Per-persona routing still uses the per-request subprocess path.
  * Pure plumbing here: nothing auto-starts unless a caller opts in. Wiring the
    generation paths to prefer it (with graceful fallback) is layered on top.
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import threading
import time
from collections.abc import Iterator

import httpx

from app.core.config import get_base_model
from app.core.settings import get_adapter_path

# Module-global handle to the managed server process + a lock so concurrent
# requests don't race to start (or kill) it. _started_adapter_sig records the
# adapter the running server loaded, so we can detect a retrain and reload.
_proc: subprocess.Popen | None = None
_lock = threading.Lock()
_started_adapter_sig: float | None = None


def _adapter_sig() -> float | None:
    """A signature (mtime) of the global adapter, or None if untrained."""
    a = get_adapter_path() / "adapters.safetensors"
    try:
        return a.stat().st_mtime if a.exists() else None
    except OSError:
        return None


def get_server_config() -> dict:
    """``model.server`` config: enabled (default off) + port."""
    from app.core.config import load_config

    cfg = load_config() or {}
    model = cfg.get("model", {}) if isinstance(cfg, dict) else {}
    srv = model.get("server", {}) if isinstance(model, dict) else {}
    srv = srv if isinstance(srv, dict) else {}
    return {"enabled": bool(srv.get("enabled", True)), "port": int(srv.get("port", 8088))}


def is_enabled() -> bool:
    return get_server_config()["enabled"]


def _port() -> int:
    return get_server_config()["port"]


def _base_url() -> str:
    return f"http://127.0.0.1:{_port()}"


def _adapter_arg() -> str | None:
    """The global adapter path if one is trained, else None (base model)."""
    adapter = get_adapter_path()
    return str(adapter) if (adapter / "adapters.safetensors").exists() else None


def model_label() -> str:
    """The model_used label a server-produced draft should report."""
    return "qwen2.5-1.5b-lora" if _adapter_arg() else "qwen2.5-1.5b-base"


def is_healthy(*, timeout: float = 0.5) -> bool:
    """True if the server answers /health. Cheap enough to gate every request."""
    try:
        r = httpx.get(f"{_base_url()}/health", timeout=timeout)
        return r.status_code == 200
    except Exception:
        return False


def ensure_running(*, startup_timeout: float = 40.0) -> bool:
    """Start the server if it isn't already healthy; wait until it is.

    Returns True if the server is healthy (already, or after starting). Safe to
    call before every local request — it's a no-op fast path once warm. Any
    failure returns False so the caller can fall back to the subprocess/cloud
    path rather than erroring.
    """
    global _proc, _started_adapter_sig
    # Never auto-spawn the heavy (~3GB) model server inside the test suite — many
    # tests exercise the generation path via TestClient and must not start a real
    # server. The server's own spawn tests clear this env var to test the logic.
    if os.environ.get("PYTEST_CURRENT_TEST"):
        return is_healthy()
    if is_healthy():
        # Running, but if the adapter was retrained since it loaded, reload it so
        # drafts use the new voice model rather than the stale one.
        if _adapter_sig() != _started_adapter_sig:
            return restart()
        return True
    with _lock:
        # Re-check under the lock — another thread may have started it.
        if is_healthy():
            return True
        if _proc is not None and _proc.poll() is None:
            # Process is up but not yet answering /health — wait it out below.
            pass
        else:
            cmd = [sys.executable, "-m", "mlx_lm.server", "--model", get_base_model(), "--port", str(_port())]
            adapter = _adapter_arg()
            if adapter:
                cmd.extend(["--adapter-path", adapter])
            try:
                _proc = subprocess.Popen(  # noqa: S603
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True,
                )
            except Exception:
                _proc = None
                return False
        # Poll /health until the model finishes loading.
        deadline = time.monotonic() + startup_timeout
        while time.monotonic() < deadline:
            if _proc is not None and _proc.poll() is not None:
                _proc = None  # died during startup
                return False
            if is_healthy(timeout=1.0):
                _started_adapter_sig = _adapter_sig()  # remember what it loaded
                return True
            time.sleep(0.5)
    return False


def stop() -> None:
    """Terminate the managed server (whole process group)."""
    global _proc
    with _lock:
        if _proc is not None and _proc.poll() is None:
            try:
                os.killpg(os.getpgid(_proc.pid), signal.SIGTERM)
            except (ProcessLookupError, PermissionError):
                _proc.terminate()
        _proc = None


def restart() -> bool:
    """Stop and start fresh — used after fine-tuning so the new adapter loads."""
    stop()
    return ensure_running()


def _payload(prompt: str, *, max_tokens: int, temperature: float | None, top_p: float | None, stream: bool) -> dict:
    body: dict = {"prompt": prompt, "max_tokens": max_tokens, "stream": stream}
    if temperature is not None:
        body["temperature"] = temperature
    if top_p is not None:
        body["top_p"] = top_p
    return body


def complete(
    prompt: str,
    *,
    max_tokens: int = 300,
    temperature: float | None = None,
    top_p: float | None = None,
    timeout: float = 120.0,
) -> str:
    """One-shot completion via the warm server. Raises on transport/HTTP error."""
    r = httpx.post(
        f"{_base_url()}/v1/completions",
        json=_payload(prompt, max_tokens=max_tokens, temperature=temperature, top_p=top_p, stream=False),
        timeout=timeout,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["text"]


def stream(
    prompt: str,
    *,
    max_tokens: int = 400,
    temperature: float | None = None,
    top_p: float | None = None,
    timeout: float = 120.0,
) -> Iterator[str]:
    """Yield text deltas from the warm server's streaming completion endpoint.

    mlx_lm.server emits OpenAI-style ``data: {json}`` SSE lines whose
    ``choices[0].text`` is the incremental delta; a ``data: [DONE]`` sentinel (if
    sent) and any non-JSON line are ignored.
    """
    with httpx.stream(
        "POST",
        f"{_base_url()}/v1/completions",
        json=_payload(prompt, max_tokens=max_tokens, temperature=temperature, top_p=top_p, stream=True),
        timeout=timeout,
    ) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if not line or not line.startswith("data:"):
                continue
            data = line[len("data:"):].strip()
            if data == "[DONE]":
                break
            try:
                delta = json.loads(data)["choices"][0].get("text", "")
            except (json.JSONDecodeError, KeyError, IndexError):
                continue
            if delta:
                yield delta
