#!/usr/bin/env python3
import json
import os
import signal
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional


CURRENT_FILE = Path(__file__).resolve()
SCRIPT_DIR = CURRENT_FILE.parent
SKILL_ROOT = SCRIPT_DIR.parent


def get_workspace_root() -> Path:
    env_workspace = os.getenv("AUDIOCLAW_WORKSPACE", "").strip()
    if env_workspace:
        path = Path(env_workspace).expanduser().resolve()
        if path.exists():
            return path
    for parent in CURRENT_FILE.parents:
        if parent.name == "workspace":
            return parent
    return (Path.home() / ".audioclaw" / "workspace").resolve()


WORKSPACE_ROOT = get_workspace_root()
DEFAULT_STATE_DIR = WORKSPACE_ROOT / "state" / "wespeaker"
DEFAULT_VENV_PYTHON = WORKSPACE_ROOT / "tools" / "wespeaker" / ".venv" / "bin" / "python"
DEFAULT_SERVICE_SCRIPT = SCRIPT_DIR / "local_wespeaker_service.py"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 18567


def get_state_dir(args) -> Path:
    raw = getattr(args, "wespeaker_state_dir", "") or str(DEFAULT_STATE_DIR)
    return Path(str(raw)).expanduser().resolve()


def get_pid_path(args) -> Path:
    return get_state_dir(args) / "service.pid"


def get_log_path(args) -> Path:
    return get_state_dir(args) / "service.log"


def get_python_path(args) -> Path:
    raw = getattr(args, "wespeaker_python", "") or str(DEFAULT_VENV_PYTHON)
    return Path(str(raw)).expanduser()


def get_service_script(args) -> Path:
    raw = getattr(args, "wespeaker_service_script", "") or str(DEFAULT_SERVICE_SCRIPT)
    return Path(str(raw)).expanduser().resolve()


def get_base_url(args) -> str:
    host = getattr(args, "wespeaker_host", DEFAULT_HOST) or DEFAULT_HOST
    port = int(getattr(args, "wespeaker_port", DEFAULT_PORT) or DEFAULT_PORT)
    return f"http://{host}:{port}"


def _request_json(url: str, *, payload: Optional[dict] = None, timeout: float = 5.0) -> dict:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read().decode("utf-8")
    return json.loads(body or "{}")


def health(args, *, timeout: float = 1.5) -> Optional[dict]:
    try:
        return _request_json(f"{get_base_url(args)}/health", timeout=timeout)
    except Exception:
        return None


def service_is_ready(args) -> bool:
    payload = health(args)
    return bool(payload and payload.get("ok"))


def profile_status(args, profile_name: str = "default", *, timeout: float = 3.0) -> dict:
    query = urllib.parse.urlencode({"name": profile_name})
    return _request_json(f"{get_base_url(args)}/profile?{query}", timeout=timeout)


def verify_audio(args, audio_path: Path, *, profile_name: str = "default", threshold: Optional[float] = None, timeout: float = 15.0) -> dict:
    payload = {
        "audio_path": str(audio_path),
        "profile_name": profile_name,
    }
    if threshold is not None:
        payload["threshold"] = float(threshold)
    return _request_json(f"{get_base_url(args)}/verify", payload=payload, timeout=timeout)


def enroll_audio(
    args,
    audio_path: Path,
    *,
    profile_name: str = "default",
    reset: bool = False,
    max_samples: int = 3,
    timeout: float = 20.0,
) -> dict:
    payload = {
        "audio_path": str(audio_path),
        "profile_name": profile_name,
        "reset": bool(reset),
        "max_samples": int(max_samples),
    }
    return _request_json(f"{get_base_url(args)}/enroll", payload=payload, timeout=timeout)


def clear_profile(args, profile_name: str = "default", *, timeout: float = 5.0) -> dict:
    payload = {"profile_name": profile_name}
    return _request_json(f"{get_base_url(args)}/clear_profile", payload=payload, timeout=timeout)


def stop_service(args, *, timeout: float = 3.0) -> bool:
    try:
        _request_json(f"{get_base_url(args)}/shutdown", payload={}, timeout=timeout)
        return True
    except Exception:
        pid_path = get_pid_path(args)
        if not pid_path.exists():
            return False
        try:
            pid = int(pid_path.read_text(encoding="utf-8").strip())
            os.kill(pid, signal.SIGTERM)
            return True
        except Exception:
            return False


def wait_until_ready(args, *, timeout: float = 60.0) -> Optional[dict]:
    deadline = time.time() + max(1.0, timeout)
    last = None
    while time.time() < deadline:
        last = health(args, timeout=2.0)
        if last and last.get("ok"):
            return last
        time.sleep(0.5)
    return last


def launch_service(args, *, timeout: float = 60.0) -> dict:
    state_dir = get_state_dir(args)
    state_dir.mkdir(parents=True, exist_ok=True)
    python_path = get_python_path(args)
    service_script = get_service_script(args)
    if not python_path.exists():
        raise RuntimeError(f"WeSpeaker Python 不存在：{python_path}")
    if not service_script.exists():
        raise RuntimeError(f"WeSpeaker service 脚本不存在：{service_script}")

    log_path = get_log_path(args)
    env = os.environ.copy()
    env["WESPEAKER_HOME"] = str((state_dir / "models").resolve())
    env["VIRTUAL_ENV"] = str(python_path.parent.parent)
    env["PATH"] = f"{python_path.parent}:{env.get('PATH', '')}"
    env.pop("PYTHONHOME", None)
    env.pop("PYTHONPATH", None)
    command = [
        str(python_path),
        str(service_script),
        "serve",
        "--host",
        str(getattr(args, "wespeaker_host", DEFAULT_HOST) or DEFAULT_HOST),
        "--port",
        str(int(getattr(args, "wespeaker_port", DEFAULT_PORT) or DEFAULT_PORT)),
        "--state-dir",
        str(state_dir),
        "--model",
        str(getattr(args, "wespeaker_model", "chinese") or "chinese"),
        "--threshold",
        str(float(getattr(args, "wespeaker_threshold", 0.8) or 0.8)),
    ]
    with log_path.open("ab") as handle:
        subprocess.Popen(
            command,
            stdout=handle,
            stderr=handle,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
            env=env,
        )
    result = wait_until_ready(args, timeout=timeout)
    if not result or not result.get("ok"):
        raise RuntimeError(f"WeSpeaker 后台服务启动失败，请查看日志：{log_path}")
    return result


def ensure_service(args, *, autostart: bool = True, timeout: float = 60.0) -> dict:
    ready = health(args, timeout=2.0)
    if ready and ready.get("ok"):
        return ready
    if not autostart:
        raise RuntimeError("WeSpeaker 后台服务未运行。")
    return launch_service(args, timeout=timeout)
