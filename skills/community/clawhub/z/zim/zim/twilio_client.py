"""Twilio REST API client for sending WhatsApp messages.

Uses httpx with HTTP Basic Auth — no twilio pip package required.

Environment variables
---------------------
TWILIO_ACCOUNT_SID   Twilio account SID.
TWILIO_AUTH_TOKEN    Twilio auth token.
TWILIO_WHATSAPP_FROM Sender number in Twilio format, e.g. 'whatsapp:+14155238886'.
"""

from __future__ import annotations

import logging
import os
from typing import Any

import httpx

logger = logging.getLogger(__name__)

_MESSAGES_URL = "https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"


def send_whatsapp_message(to: str, body: str) -> dict[str, Any]:
    """Send a WhatsApp message via the Twilio Messages API.

    Args:
        to:   Recipient number in Twilio format, e.g. 'whatsapp:+971544042230'.
        body: Text body of the message.

    Returns:
        Parsed JSON response from Twilio.

    Raises:
        EnvironmentError: If required credentials are missing.
        httpx.HTTPStatusError: If Twilio returns a non-2xx response.
    """
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID", "").strip()
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN", "").strip()
    from_number = os.environ.get("TWILIO_WHATSAPP_FROM", "").strip()

    if not account_sid or not auth_token or not from_number:
        raise EnvironmentError(
            "TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_WHATSAPP_FROM must all be set"
        )

    url = _MESSAGES_URL.format(sid=account_sid)

    with httpx.Client(timeout=10.0) as client:
        response = client.post(
            url,
            auth=(account_sid, auth_token),
            data={"To": to, "From": from_number, "Body": body},
        )

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        logger.error(
            "Twilio Messages API error %d for %s: %s",
            exc.response.status_code,
            to,
            exc.response.text,
        )
        raise

    result: dict[str, Any] = response.json()
    logger.info("Sent WhatsApp message to %s — sid=%s", to, result.get("sid", "?"))
    return result
