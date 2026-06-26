"""Flask webhook handler for the Zim WhatsApp agent.

Provides:
- POST /webhook/whatsapp  — inbound message handler (Twilio)
- GET  /webhook/whatsapp  — Twilio webhook verification (no-op 200)
- GET  /health            — liveness probe

Environment variables
---------------------
TWILIO_AUTH_TOKEN   Twilio auth token for request signature verification.
                    If unset, verification is skipped (development mode only).
ZIM_STATE_DB        Path to the SQLite state file (default: /tmp/zim_state.db).
ZIM_TRAVELER_ID     Default traveler ID passed to the agent (default: "default").

LLM agent (used when OPENROUTER_API_KEY is set):
OPENROUTER_API_KEY  OpenRouter API key — enables the LLM conversational layer.
ZIM_LLM_MODEL       OpenRouter model to use (default: anthropic/claude-3-haiku).
                    Set ZIM_USE_LEGACY_AGENT=1 to force the keyword-based agent
                    even when OPENROUTER_API_KEY is present.

Running
-------
Development:
    python -m zim.webhook

Production (gunicorn):
    gunicorn "zim.webhook:create_app()" --bind 0.0.0.0:8080 --workers 2

Docker one-liner:
    docker run -e TWILIO_AUTH_TOKEN=xxx -e ZIM_STATE_DB=/data/zim.db \\
        -e OPENROUTER_API_KEY=sk-or-xxx \\
        -v /data:/data -p 8080:8080 zim-whatsapp

Dependencies (optional extras):
    pip install "zim[webhook]"   # installs flask
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Twilio request validation
# ---------------------------------------------------------------------------


def _twilio_signature_valid(
    auth_token: str,
    url: str,
    post_data: dict[str, str],
    x_twilio_signature: str,
) -> bool:
    """Validate a Twilio webhook request signature.

    See https://www.twilio.com/docs/usage/webhooks/webhooks-security
    """
    # Build the string Twilio signs: URL + sorted POST params concatenated
    params_str = "".join(
        f"{k}{v}" for k, v in sorted(post_data.items())
    )
    s = (url + params_str).encode("utf-8")
    expected = hmac.new(
        auth_token.encode("utf-8"), s, hashlib.sha1
    ).digest()

    import base64
    expected_b64 = base64.b64encode(expected).decode("utf-8")
    return hmac.compare_digest(expected_b64, x_twilio_signature)


# ---------------------------------------------------------------------------
# Flask app factory
# ---------------------------------------------------------------------------


def create_app() -> Any:
    """Create and return the configured Flask application.

    Import is deferred so the rest of the zim package works even when
    Flask is not installed.
    """
    try:
        from flask import Flask, abort, request
    except ImportError as exc:
        raise ImportError(
            "Flask is required for the webhook server. "
            "Install it with: pip install 'zim[webhook]'"
        ) from exc

    from zim.state_store import SQLiteStateStore
    from zim.whatsapp_agent import ZimWhatsAppAgent
    from zim.llm_agent import LLMWhatsAppAgent

    app = Flask(__name__)

    auth_token = os.environ.get("TWILIO_AUTH_TOKEN", "")
    traveler_id = os.environ.get("ZIM_TRAVELER_ID", "default")
    dev_mode = not bool(auth_token)

    if dev_mode:
        logger.warning(
            "TWILIO_AUTH_TOKEN not set — running in development mode "
            "(webhook signature verification disabled)"
        )

    store = SQLiteStateStore()

    openrouter_key = os.environ.get("OPENROUTER_API_KEY", "")
    use_legacy = os.environ.get("ZIM_USE_LEGACY_AGENT", "").strip() == "1"

    if openrouter_key and not use_legacy:
        logger.info(
            "OPENROUTER_API_KEY present — using LLM conversational agent "
            "(model: %s)",
            os.environ.get("ZIM_LLM_MODEL", "anthropic/claude-3-haiku"),
        )
        agent: Any = LLMWhatsAppAgent(
            api_key=openrouter_key,
            default_traveler_id=traveler_id,
            state_store=store,
        )
    else:
        logger.info(
            "OPENROUTER_API_KEY not set (or ZIM_USE_LEGACY_AGENT=1) — "
            "using keyword-based agent"
        )
        agent = ZimWhatsAppAgent(
            default_traveler_id=traveler_id,
            state_store=store,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _verify_twilio(req: Any) -> None:
        """Abort 403 if Twilio signature is missing or invalid."""
        if dev_mode:
            return
        signature = req.headers.get("X-Twilio-Signature", "")
        # Use the full URL that Twilio signed (scheme + host + path + query)
        url = req.url
        post_data = dict(req.form)
        if not _twilio_signature_valid(auth_token, url, post_data, signature):
            logger.warning("Twilio signature verification failed for request from %s", req.remote_addr)
            abort(403)

    def _twiml_reply(body: str) -> tuple[str, int, dict[str, str]]:
        """Wrap a plain-text reply in minimal TwiML."""
        # Escape XML special characters
        escaped = (
            body.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )
        xml = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            "<Response>\n"
            f"  <Message>{escaped}</Message>\n"
            "</Response>\n"
        )
        return xml, 200, {"Content-Type": "text/xml; charset=utf-8"}

    # ------------------------------------------------------------------
    # Routes
    # ------------------------------------------------------------------

    @app.get("/health")
    def health() -> tuple[str, int]:
        return "ok", 200

    @app.get("/webhook/whatsapp")
    def whatsapp_get() -> tuple[str, int]:
        # Twilio sends a GET to verify the URL exists during setup
        return "", 200

    @app.post("/webhook/whatsapp")
    def whatsapp_post() -> Any:
        _verify_twilio(request)

        body = request.form.get("Body", "").strip()
        user_id = request.form.get("From", "")

        if not user_id:
            logger.warning("Received WhatsApp webhook with no From field")
            abort(400)

        # Redact user_id in logs to avoid PII leakage (keep prefix for debugging)
        safe_uid = user_id[:12] + "..." if len(user_id) > 12 else user_id
        logger.info("Inbound message from %s (%d chars)", safe_uid, len(body))

        reply = agent.handle_message(body, user_id)
        return _twiml_reply(reply)

    return app


# ---------------------------------------------------------------------------
# Dev server entry point
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    port = int(os.environ.get("PORT", 5000))
    app = create_app()
    app.run(host="0.0.0.0", port=port, debug=True)
