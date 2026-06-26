"""Telegram alerter — stdlib-only (urllib.request).

Sends alerts for HIGH/CRITICAL severity behaviors.
Rate-limited to prevent alert flooding.
"""

import json
import logging
import os
import time
import urllib.request
import urllib.error
from typing import Optional

from sal.monitor.behaviors import Severity

logger = logging.getLogger("sal.monitor.alerter")

# Rate limiting
_RATE_LIMIT_PER_HOUR = 10
_recent_alerts: list[float] = []


def _get_config() -> tuple[Optional[str], Optional[str]]:
    """Get Telegram bot token and chat ID from env."""
    token = os.environ.get("MONITOR_TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("MONITOR_TELEGRAM_CHAT_ID")
    return token, chat_id


def _is_rate_limited() -> bool:
    """Check if we've exceeded the hourly rate limit."""
    now = time.time()
    cutoff = now - 3600  # 1 hour ago
    # Clean old entries
    _recent_alerts[:] = [t for t in _recent_alerts if t > cutoff]
    return len(_recent_alerts) >= _RATE_LIMIT_PER_HOUR


def _severity_emoji(severity: Severity) -> str:
    """Map severity to emoji for Telegram message."""
    return {
        Severity.LOW: "ℹ️",
        Severity.MEDIUM: "⚠️",
        Severity.HIGH: "🚨",
        Severity.CRITICAL: "🔴",
    }.get(severity, "❓")


def send_alert(
    severity: Severity,
    behavior_name: str,
    evidence: str,
    agent_id: str = "unknown",
    session_id: str = "",
) -> bool:
    """Send a Telegram alert for a detected behavior.

    Args:
        severity: Alert severity level.
        behavior_name: Name of the detected behavior.
        evidence: Brief description of what was found.
        agent_id: Agent that triggered the alert.
        session_id: Session identifier.

    Returns:
        True if alert was sent successfully, False otherwise.
    """
    token, chat_id = _get_config()
    if not token or not chat_id:
        logger.warning("Telegram not configured — alert suppressed")
        return False

    if _is_rate_limited():
        logger.warning(
            "Rate limit reached (%d/h) — alert suppressed: %s",
            _RATE_LIMIT_PER_HOUR, behavior_name,
        )
        return False

    emoji = _severity_emoji(severity)
    # Truncate evidence to avoid Telegram message limit
    evidence_short = evidence[:300] if evidence else "No details"

    message = (
        f"{emoji} **Agent Monitor Alert**\n\n"
        f"**Severity:** {severity.name}\n"
        f"**Behavior:** {behavior_name}\n"
        f"**Agent:** {agent_id}\n"
        f"**Session:** {session_id[:8] if session_id else 'N/A'}\n\n"
        f"**Evidence:**\n{evidence_short}"
    )

    return _send_telegram(token, chat_id, message)


def send_canary_alert(message: str) -> bool:
    """Send a canary failure alert."""
    token, chat_id = _get_config()
    if not token or not chat_id:
        return False
    return _send_telegram(token, chat_id, f"⚠️ Monitor Canary Alert\n\n{message}")


def _send_telegram(token: str, chat_id: str, text: str) -> bool:
    """Low-level Telegram API call via urllib."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            _recent_alerts.append(time.time())
            logger.info("Alert sent to Telegram (status: %d)", resp.status)
            return resp.status == 200
    except urllib.error.URLError as e:
        logger.error("Telegram alert failed: %s", e)
        return False
    except Exception as e:
        logger.error("Unexpected error sending alert: %s", e)
        return False
