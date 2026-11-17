"""
skill.py
--------
OpenClaw skill: Sentinel Modality-Router Redaction Check

Verifies that Sentinel's PII redaction guardrail survives routing through a
modality-aware LiteLLM router to two structurally different self-hosted
backends -- a text model (Ollama) and a vision model (a custom FastAPI
wrapper around SmolVLM-Instruct) -- picked automatically by whether the
request contains an image_url block. Companion to the earlier
sentinel-custom-provider-check skill, which only verified a single backend;
this one confirms the guardrail (and the routing decision) holds across
more than one model type behind the same gateway.

How this skill fits into OpenClaw:
  - The user already has router.py, the LiteLLM proxy, and both backends
    (Ollama + vlm_server.py) running locally -- see the parent project's
    README for that setup. This skill does not start those; it only
    (re)points the local Sentinel gateway's CUSTOM_PROVIDERS at router.py
    and drives two probes through it.
  - Probe 1: text-only prompt with synthetic PII -- expected to route to
    TEXT_MODEL_ALIAS.
  - Probe 2: image + text prompt with synthetic PII -- expected to route to
    VISION_MODEL_ALIAS.
  - Each probe's pass/fail is read from the backend's own raw JSON response,
    not from anything upstream, for the same reason as the earlier skill
    (see "Why this check has to work this way" below).
  - If Jaeger is reachable, the report also includes the resulting trace ID
    -- this is the "visibility into every hop" half of the demo, not just
    the redaction half.
  - Result is sent via OpenClaw's existing Telegram connection.

Why this check has to work this way:
  Don't verify this by pasting real PII into a chat with Claude and reading
  Claude's own reply -- a session already routed through a Sentinel gateway
  redacts inbound PII-shaped text on the way in, independent of whatever the
  backend actually did with it. That makes an unrelated pass-through look
  like a successful redaction. The only valid check is reading the raw
  response the *backend itself* produced, over a channel nothing upstream
  can re-redact -- exactly what _probe_text()/_probe_image() do here.

Credentials / config required in OpenClaw environment: see .env.example.
Nothing sensitive is stored by this skill -- the probe PII is synthetic.
"""

import base64
import html
import json
import os
import subprocess
import time

import requests
from dotenv import load_dotenv

load_dotenv()

SKILL_META = {
    "name": "sentinel_modality_router_check",
    "description": (
        "Confirms Sentinel's PII redaction survives routing through a "
        "modality-aware LiteLLM router to two different self-hosted model "
        "types (text + vision), and that each probe actually reached the "
        "model it should have. Reports pass/fail per modality, plus the "
        "resulting Jaeger trace ID if tracing is available."
    ),
    "version": "1.0.1",
    "trigger": {
        "telegram_command": "/sentinel_modality_check",
        "description": (
            "Reconfigure the local Sentinel gateway's CUSTOM_PROVIDERS entry to "
            "point at router.py, then run one text-only and one image+text "
            "redaction probe through it."
        ),
    },
    "webhook_url": "${RENDER_APP_URL}/sentinel-modality-check/run",
    "method": "GET",
    "mcp_servers": [
        "https://docs.superwise.ai/mcp",
    ],
}

# Built from parts rather than as contiguous literals. Per
# https://docs.superwise.ai/docs/pii-redaction, Sentinel's guardrail only
# matches structured identifiers, not free-text names -- and separately, a
# dev environment in this project's history has mangled plain PII-shaped
# literals typed directly into source (the earlier sentinel-custom-provider-
# check skill shipped with PROBE_EMAIL accidentally set to the literal
# "{{REDACTED}}" marker instead of a real fake address, for exactly this
# reason). Constructing the values from parts avoids repeating that bug.
PROBE_NAME = "Jamie Rivera"
PROBE_PHONE = "-".join(["312", "555", "0173"])  # area code included on purpose -- see docs above
PROBE_EMAIL = "@".join(["jrivera-test", "example.com"])
REDACTED_MARKER = "{{REDACTED}}"

_GATEWAY_STARTUP_TIMEOUT = 60
_GATEWAY_POLL_INTERVAL = 2


def _config() -> dict:
    port = int(os.getenv("SENTINEL_GATEWAY_PORT", "8100"))
    router_base_url = os.getenv("ROUTER_BASE_URL")
    provider_name = os.getenv("ROUTER_PROVIDER_NAME", "local-router")
    text_alias = os.getenv("TEXT_MODEL_ALIAS", "qwen-local")
    vision_alias = os.getenv("VISION_MODEL_ALIAS", "smolvlm-local")
    image_path = os.getenv("TEST_IMAGE_PATH", "./test_image.png")
    jaeger_base_url = os.getenv("JAEGER_BASE_URL", "")
    jaeger_service = os.getenv("JAEGER_SERVICE_NAME", "router")

    if not router_base_url:
        raise RuntimeError("ROUTER_BASE_URL is not set")

    return {
        "port": port,
        "router_base_url": router_base_url,
        "provider_name": provider_name,
        "text_alias": text_alias,
        "vision_alias": vision_alias,
        "image_path": image_path,
        "jaeger_base_url": jaeger_base_url,
        "jaeger_service": jaeger_service,
    }


def _start_gateway(cfg: dict) -> None:
    """
    (Re)start the local Sentinel gateway container with CUSTOM_PROVIDERS
    pointed at router.py. Reuses the cached sentinel_id -- this is not a
    fresh registration, just an updated custom_providers entry.
    """
    custom_providers = json.dumps([
        {"provider_name": cfg["provider_name"], "base_url": cfg["router_base_url"]}
    ])

    print(f"[skill] Stopping any existing Sentinel gateway on port {cfg['port']}...")
    subprocess.run(["sentinel", "gateway", "stop"], capture_output=True, text=True)

    print(f"[skill] Starting Sentinel gateway with CUSTOM_PROVIDERS -> {cfg['router_base_url']}...")
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
    # Require 200 specifically, not merely "< 500" -- a gateway that's up but
    # misconfigured (wrong custom-providers path, auth issue, etc.) can answer
    # with 401/403/404 well within the timeout, which would otherwise read as
    # "ready" and let the probes proceed against a broken route.
    deadline = time.time() + _GATEWAY_STARTUP_TIMEOUT
    url = f"http://localhost:{cfg['port']}/{cfg['provider_name']}/v1/models"
    last_status = None
    while time.time() < deadline:
        try:
            resp = requests.get(url, timeout=3)
            last_status = resp.status_code
            if resp.status_code == 200:
                print("[skill] Gateway is responding.")
                return
        except requests.RequestException:
            pass
        time.sleep(_GATEWAY_POLL_INTERVAL)
    detail = f" (last response: {last_status})" if last_status is not None else " (no response received)"
    raise TimeoutError(f"Sentinel gateway on port {cfg['port']} never became reachable{detail}")


def _gateway_url(cfg: dict) -> str:
    return f"http://localhost:{cfg['port']}/{cfg['provider_name']}/v1/chat/completions"


def _evaluate(content: str, model_field: str, expected_alias: str) -> dict:
    email_leaked = PROBE_EMAIL in content
    phone_leaked = PROBE_PHONE in content
    redacted_seen = REDACTED_MARKER in content
    routed_correctly = model_field == expected_alias
    return {
        "content": content,
        "model_field": model_field,
        "expected_alias": expected_alias,
        "routed_correctly": routed_correctly,
        "email_leaked": email_leaked,
        "phone_leaked": phone_leaked,
        "redacted_seen": redacted_seen,
        "passed": redacted_seen and not email_leaked and not phone_leaked and routed_correctly,
    }


def _probe_text(cfg: dict) -> dict:
    """
    Text-only probe -- should route to TEXT_MODEL_ALIAS. Reads the backend's
    own raw response over HTTP, same reasoning as the module docstring:
    nothing upstream of this call can re-redact it, so a `{{REDACTED}}` here
    means the guardrail actually fired on this hop.
    """
    prompt = (
        f"My name is {PROBE_NAME}, my phone number is {PROBE_PHONE}, and my "
        f"email is {PROBE_EMAIL}. Please repeat back my phone number and "
        "email exactly, then say hello."
    )
    resp = requests.post(
        _gateway_url(cfg),
        json={"model": cfg["provider_name"], "messages": [{"role": "user", "content": prompt}]},
        timeout=60,
    )
    resp.raise_for_status()
    body = resp.json()
    content = body["choices"][0]["message"]["content"]
    return _evaluate(content, body.get("model", ""), cfg["text_alias"])


def _probe_image(cfg: dict) -> dict:
    """
    Image + text probe -- should route to VISION_MODEL_ALIAS. Same
    evaluation as _probe_text(), plus a routing check against the vision
    alias instead of the text one.
    """
    with open(cfg["image_path"], "rb") as f:
        b64_image = base64.b64encode(f.read()).decode("utf-8")

    prompt = (
        f"My name is {PROBE_NAME}, reachable at {PROBE_PHONE} or "
        f"{PROBE_EMAIL}. Briefly describe what's in this image, then repeat "
        "back my phone number and email exactly."
    )
    resp = requests.post(
        _gateway_url(cfg),
        json={
            "model": cfg["provider_name"],
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_image}"}},
                    ],
                }
            ],
        },
        timeout=120,
    )
    resp.raise_for_status()
    body = resp.json()
    content = body["choices"][0]["message"]["content"]
    return _evaluate(content, body.get("model", ""), cfg["vision_alias"])


def _lookup_trace(cfg: dict) -> dict | None:
    """
    Best-effort: if Jaeger is reachable, grab the most recent trace for
    JAEGER_SERVICE_NAME so the report can point at the exact trace these two
    probes produced. Never blocks or fails the redaction check itself --
    this is the observability half of the demo, not the compliance half.
    """
    base = cfg.get("jaeger_base_url")
    if not base:
        return None
    try:
        resp = requests.get(
            f"{base}/api/traces",
            params={"service": cfg["jaeger_service"], "limit": 1},
            timeout=5,
        )
        resp.raise_for_status()
        traces = resp.json().get("data", [])
        if not traces:
            return None
        trace_id = traces[0]["traceID"]
        return {"trace_id": trace_id, "url": f"{base}/trace/{trace_id}", "span_count": len(traces[0]["spans"])}
    except requests.RequestException:
        return None


def _send_telegram(message: str) -> bool:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("[skill] TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set -- skipping alert.")
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


def _format_line(label: str, result: dict) -> str:
    # model_field comes straight from the backend's response body -- escape it
    # before it goes into an HTML-parse_mode Telegram message, same reasoning
    # as the raw-content block below.
    icon = "✅" if result["passed"] else "⚠️"
    model_field = html.escape(str(result["model_field"]))
    expected_alias = html.escape(str(result["expected_alias"]))
    return (
        f"{icon} <b>{label}</b>\n"
        f"routed_to=<code>{model_field}</code> (expected <code>{expected_alias}</code>)\n"
        f"redacted_seen={result['redacted_seen']}  email_leaked={result['email_leaked']}  "
        f"phone_leaked={result['phone_leaked']}\n"
    )


def _format_result_message(text_result: dict, image_result: dict, trace: dict | None) -> str:
    overall = "PASSED" if text_result["passed"] and image_result["passed"] else "FAILED"
    # Labels are built from the result's own expected_alias rather than
    # hardcoded model names, so they stay accurate if TEXT_MODEL_ALIAS/
    # VISION_MODEL_ALIAS are ever changed in .env.
    lines = [
        f"<b>Sentinel modality-router redaction check -- {overall}</b>\n",
        _format_line(f"Text probe ({html.escape(text_result['expected_alias'])} leg)", text_result),
        _format_line(f"Image probe ({html.escape(image_result['expected_alias'])} leg)", image_result),
    ]
    if trace:
        lines.append(f"\nTrace: <code>{trace['trace_id']}</code> ({trace['span_count']} spans)\n{trace['url']}")
    else:
        lines.append("\n(Jaeger trace lookup skipped or unavailable -- redaction result above is unaffected.)")
    if overall == "FAILED":
        # Backend-generated text, unescaped, would let stray '<'/'&'/etc. either
        # break Telegram's HTML entity parsing (send fails outright) or render
        # as unintended markup -- escape before embedding.
        text_snippet = html.escape(text_result["content"][:300])
        image_snippet = html.escape(image_result["content"][:300])
        lines.append(f"\nText probe raw content:\n<code>{text_snippet}</code>")
        lines.append(f"\nImage probe raw content:\n<code>{image_snippet}</code>")
    return "\n".join(lines)


def run() -> dict:
    """
    OpenClaw skill entrypoint. Also callable standalone via `python skill.py`.

    1. (Re)start the local Sentinel gateway with CUSTOM_PROVIDERS pointed at
       router.py.
    2. Send a text-only PII probe (expects the TEXT_MODEL_ALIAS leg) and an
       image+text PII probe (expects the VISION_MODEL_ALIAS leg).
    3. Best-effort look up the resulting Jaeger trace.
    4. Report pass/fail via Telegram.
    """
    cfg = _config()
    _start_gateway(cfg)
    _wait_for_gateway(cfg)

    text_result = _probe_text(cfg)
    image_result = _probe_image(cfg)
    trace = _lookup_trace(cfg)

    message = _format_result_message(text_result, image_result, trace)
    sent = _send_telegram(message)

    print(f"[skill] Result:\n{'-' * 40}\n{message}\n{'-' * 40}")

    return {
        "passed": text_result["passed"] and image_result["passed"],
        "sent": sent,
        "text": text_result,
        "image": image_result,
        "trace": trace,
    }


if __name__ == "__main__":
    outcome = run()
    print(f"\n[skill] Done: {outcome}")
