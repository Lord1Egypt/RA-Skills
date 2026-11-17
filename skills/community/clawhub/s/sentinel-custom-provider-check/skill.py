"""
skill.py
--------
OpenClaw skill: Sentinel CUSTOM_PROVIDERS Redaction Check

Verifies that Sentinel's PII/secret guardrails survive a hop through
CUSTOM_PROVIDERS to a self-hosted OpenAI-compatible backend (vLLM, TGI,
Ollama, or anything else that speaks the /v1/chat/completions shape) —
not just Sentinel's first-party Anthropic/OpenAI/Google routes.

How this skill fits into OpenClaw:
  - The user already runs a self-hosted OpenAI-compatible server, reachable
    at a public URL (ngrok/Cloudflare tunnel, or a real deployment).
  - This skill (re)configures a local Sentinel gateway container with
    CUSTOM_PROVIDERS pointed at that backend, fires a probe prompt containing
    fake-but-realistic PII, and checks the backend's own response to confirm
    the PII arrived redacted rather than in the clear.
  - Result is sent via OpenClaw's existing Telegram connection.

Why the check has to work this way:
  Don't verify this by pasting real PII into a chat with Claude and reading
  Claude's own reply — a session already routed through a Sentinel gateway
  redacts inbound PII-shaped text on the way in, independent of whatever the
  custom backend did with it. That makes an unrelated pass-through look like
  a successful redaction. The only valid check is reading the raw response
  the *backend itself* produced, which is exactly what `_probe_backend()`
  does here: it talks to the gateway's OpenAI-compatible endpoint directly
  over HTTP and inspects the JSON body, with nothing upstream re-redacting it.

Credentials / config required in OpenClaw environment:
    CUSTOM_PROVIDER_BASE_URL   public base URL of the self-hosted backend,
                               e.g. https://<id>.ngrok-free.app
    CUSTOM_PROVIDER_NAME       short slug used as the CUSTOM_PROVIDERS name
                               and in the gateway's routed path, e.g. "vllm-colab"
    CUSTOM_PROVIDER_MODEL      model name the backend serves, e.g.
                               Qwen/Qwen2.5-3B-Instruct
    SENTINEL_GATEWAY_PORT      local port for the Sentinel gateway (default 8100)
    TELEGRAM_BOT_TOKEN         already configured in OpenClaw
    TELEGRAM_CHAT_ID           already configured in OpenClaw

Nothing sensitive is stored by this skill — the probe values are synthetic,
and the gateway container itself holds Sentinel's own cached config.
"""

import json
import os
import subprocess
import time

import requests
from dotenv import load_dotenv

load_dotenv()

SKILL_META = {
    "name": "sentinel_custom_provider_check",
    "description": (
        "Confirms Sentinel's PII/secret redaction survives routing through "
        "CUSTOM_PROVIDERS to a self-hosted OpenAI-compatible model backend "
        "(vLLM, TGI, Ollama, etc.), not just first-party providers. Starts/updates "
        "the local Sentinel gateway container, sends a synthetic-PII probe straight "
        "through it to the backend, and reports whether the backend only ever saw "
        "the redacted placeholder."
    ),
    "version": "1.0.1",
    "trigger": {
        "telegram_command": "/sentinel_custom_check",
        "description": (
            "Reconfigure the local Sentinel gateway's CUSTOM_PROVIDERS entry from "
            "the current env vars, then run the redaction probe against it."
        ),
    },
    "webhook_url": "${RENDER_APP_URL}/sentinel-custom-check/run",
    "method": "GET",
    "mcp_servers": [
        "https://docs.superwise.ai/mcp",
    ],
}

PROBE_EMAIL = "probe.test.user@example.com"
PROBE_PHONE = "555-0142"
REDACTED_MARKER = "{{REDACTED}}"

_GATEWAY_STARTUP_TIMEOUT = 60
_GATEWAY_POLL_INTERVAL = 2


def _provider_config() -> dict:
    base_url = os.getenv("CUSTOM_PROVIDER_BASE_URL")
    name = os.getenv("CUSTOM_PROVIDER_NAME", "custom-backend")
    model = os.getenv("CUSTOM_PROVIDER_MODEL")
    port = int(os.getenv("SENTINEL_GATEWAY_PORT", "8100"))

    if not base_url:
        raise RuntimeError("CUSTOM_PROVIDER_BASE_URL is not set")
    if not model:
        raise RuntimeError("CUSTOM_PROVIDER_MODEL is not set")

    return {"base_url": base_url, "name": name, "model": model, "port": port}


def _start_gateway(cfg: dict) -> None:
    """
    (Re)start the local Sentinel gateway container with CUSTOM_PROVIDERS
    pointed at the configured backend. Reuses the cached sentinel_id — this
    is not a fresh registration, just an updated custom_providers entry.
    """
    custom_providers = json.dumps([
        {"provider_name": cfg["name"], "base_url": cfg["base_url"]}
    ])

    print(f"[skill] Stopping any existing Sentinel gateway on port {cfg['port']}...")
    subprocess.run(
        ["sentinel", "gateway", "stop"],
        capture_output=True, text=True,
    )

    print(f"[skill] Starting Sentinel gateway with CUSTOM_PROVIDERS -> {cfg['base_url']}...")
    result = subprocess.run(
        [
            "sentinel", "gateway", "start",
            "--port", str(cfg["port"]),
            "--custom-providers", custom_providers,
        ],
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(f"sentinel gateway start failed: {result.stderr.strip()}")
    print(f"[skill] Gateway start output: {result.stdout.strip()}")


def _wait_for_gateway(cfg: dict) -> None:
    deadline = time.time() + _GATEWAY_STARTUP_TIMEOUT
    url = f"http://localhost:{cfg['port']}/{cfg['name']}/v1/models"
    while time.time() < deadline:
        try:
            resp = requests.get(url, timeout=3)
            if resp.status_code < 500:
                print("[skill] Gateway is responding.")
                return
        except requests.RequestException:
            pass
        time.sleep(_GATEWAY_POLL_INTERVAL)
    raise TimeoutError(f"Sentinel gateway on port {cfg['port']} never became reachable")


def _probe_backend(cfg: dict) -> dict:
    """
    Send a synthetic-PII prompt through the gateway to the custom backend and
    ask it to echo the values back verbatim. Reads the backend's raw JSON
    response directly over HTTP — nothing upstream of this call can redact it
    a second time, so a `{{REDACTED}}` here means the guardrail actually fired
    on this hop, not on some unrelated relay.
    """
    url = f"http://localhost:{cfg['port']}/{cfg['name']}/v1/chat/completions"
    prompt = (
        f"Please repeat back, exactly and only, this email and phone number: "
        f"{PROBE_EMAIL} and {PROBE_PHONE}"
    )
    resp = requests.post(
        url,
        json={
            "model": cfg["model"],
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 60,
        },
        timeout=30,
    )
    resp.raise_for_status()
    body = resp.json()
    content = body["choices"][0]["message"]["content"]

    email_leaked = PROBE_EMAIL in content
    phone_leaked = PROBE_PHONE in content
    redacted_seen = REDACTED_MARKER in content

    return {
        "content": content,
        "email_leaked": email_leaked,
        "phone_leaked": phone_leaked,
        "redacted_seen": redacted_seen,
        "passed": redacted_seen and not email_leaked and not phone_leaked,
    }


def _send_telegram(message: str) -> bool:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("[skill] TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set — skipping alert.")
        return False
    try:
        resp = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": message, "parse_mode": "HTML"},
            timeout=10,
        )
        resp.raise_for_status()
        return True
    except requests.RequestException as exc:
        print(f"[skill] Telegram send failed: {exc}")
        return False


def _format_result_message(result: dict, cfg: dict) -> str:
    if result["passed"]:
        return (
            "✅ <b>Sentinel CUSTOM_PROVIDERS redaction check — passed</b>\n\n"
            f"Backend: <code>{cfg['name']}</code> ({cfg['base_url']})\n"
            f"Model: <code>{cfg['model']}</code>\n\n"
            f"Backend response only showed <code>{REDACTED_MARKER}</code> in place of "
            "the probe email + phone number. The guardrail held on this hop."
        )
    return (
        "⚠️ <b>Sentinel CUSTOM_PROVIDERS redaction check — FAILED</b>\n\n"
        f"Backend: <code>{cfg['name']}</code> ({cfg['base_url']})\n"
        f"Model: <code>{cfg['model']}</code>\n\n"
        f"email_leaked={result['email_leaked']}  phone_leaked={result['phone_leaked']}  "
        f"redacted_seen={result['redacted_seen']}\n\n"
        f"Raw backend content:\n<code>{result['content'][:400]}</code>"
    )


def run() -> dict:
    """
    OpenClaw skill entrypoint. Also callable standalone via `python skill.py`.

    1. (Re)start the local Sentinel gateway with CUSTOM_PROVIDERS pointed at
       the configured backend.
    2. Send a synthetic-PII probe through it.
    3. Report pass/fail via Telegram.
    """
    cfg = _provider_config()
    _start_gateway(cfg)
    _wait_for_gateway(cfg)
    result = _probe_backend(cfg)
    message = _format_result_message(result, cfg)
    sent = _send_telegram(message)

    print(f"[skill] Result:\n{'─' * 40}\n{message}\n{'─' * 40}")

    return {"passed": result["passed"], "sent": sent, "detail": result}


if __name__ == "__main__":
    outcome = run()
    print(f"\n[skill] Done: {outcome}")
