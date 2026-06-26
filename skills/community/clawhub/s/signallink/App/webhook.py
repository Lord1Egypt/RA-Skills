import logging
import hmac
import hashlib
from typing import Any

from fastapi import APIRouter, Request, HTTPException, Header
from app.config import config
from app.formatter import format_signal, format_raw
from app.telegram import send_message

router = APIRouter()
logger = logging.getLogger(__name__)


def verify_secret(provided: str) -> bool:
    """Constant-time comparison to prevent timing attacks."""
    if not config.WEBHOOK_SECRET:
        return True  # Secret not configured → open mode (not recommended for prod)
    return hmac.compare_digest(provided or "", config.WEBHOOK_SECRET)


@router.post("/webhook")
async def receive_webhook(
    request: Request,
    x_webhook_secret: str = Header(default=None),
):
    """
    Main webhook endpoint.

    Accepts JSON payload from TradingView or any custom source.
    Validates optional secret, formats the signal, and sends to Telegram.
    """
    # --- Auth check ---
    if not verify_secret(x_webhook_secret):
        logger.warning("Unauthorized webhook attempt")
        raise HTTPException(status_code=401, detail="Invalid webhook secret")

    # --- Parse body ---
    try:
        payload: dict[str, Any] = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    logger.info(f"Received webhook payload: {payload}")

    # --- Format & send ---
    try:
        # Use signal formatter if payload looks like a trading alert
        if any(k in payload for k in ("action", "signal", "symbol", "ticker")):
            message = format_signal(payload)
        else:
            message = format_raw(payload)

        await send_message(message)
        return {"status": "ok", "message": "Signal forwarded to Telegram"}

    except Exception as e:
        logger.error(f"Failed to forward signal: {e}")
        raise HTTPException(status_code=500, detail="Failed to send Telegram message")


@router.post("/webhook/raw")
async def receive_raw_webhook(request: Request):
    """
    Raw webhook endpoint — always uses key-value formatter.
    Useful for non-trading alerts (uptime monitors, CI/CD, etc.)
    """
    try:
        payload: dict[str, Any] = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    message = format_raw(payload)
    await send_message(message)
    return {"status": "ok"}
