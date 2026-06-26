"""Sender classification for sender-aware retrieval."""

from __future__ import annotations

import re
from typing import Literal

from app.core.config import get_internal_domains

SenderType = Literal["internal", "external_client", "personal", "automated", "unknown"]

_EMAIL_RE = re.compile(r"[\w.+-]+@[\w.-]+\.\w+")

_TITLE_PREFIXES = re.compile(r"^(dr\.?|prof\.?|mr\.?|mrs\.?|ms\.?|sir)\s+", re.IGNORECASE)


def first_name_from_display_name(display_name: str | None) -> str | None:
    """Extract first name from a display name string.

    Handles: "Sarah Mitchell", "Dr. Baher", "sarah.mitchell@company.com", etc.
    Returns None if unparseable.
    """
    if not display_name or not display_name.strip():
        return None

    name = display_name.strip()

    # If it looks like an email, extract from local part
    if "@" in name:
        local = name.split("@")[0]
        # Split on dots, hyphens, underscores
        parts = re.split(r"[._\-]", local)
        if parts and parts[0]:
            return parts[0].capitalize()
        return None

    # Strip titles
    name = _TITLE_PREFIXES.sub("", name).strip()

    if not name:
        return None

    # Take first word as first name
    first = name.split()[0]
    # Remove any trailing punctuation
    first = first.rstrip(",.")
    if not first:
        return None
    return first[0].upper() + first[1:] if len(first) > 1 else first.upper()


_AUTOMATED_PREFIXES = frozenset(
    {
        "no-reply",
        "noreply",
        "donotreply",
        "do-not-reply",
        "invoice",
        "billing",
        "mailer",
        "notifications",
        "support",
        "bounce",
        "postmaster",
        "daemon",
    }
)

_PERSONAL_DOMAINS = frozenset(
    {
        "gmail.com",
        "yahoo.com",
        "hotmail.com",
        "icloud.com",
        "me.com",
        "outlook.com",
        "live.com",
        "aol.com",
        "protonmail.com",
        "proton.me",
        "fastmail.com",
    }
)


def extract_domain(author: str | None) -> str | None:
    """Extract domain from an email address in the author string."""
    if not author:
        return None
    match = _EMAIL_RE.search(author)
    if not match:
        return None
    return match.group().split("@", 1)[1].lower()


def classify_sender(author: str | None) -> SenderType:
    """Classify a sender into a category based on their email address."""
    if not author:
        return "unknown"

    match = _EMAIL_RE.search(author)
    if not match:
        return "unknown"

    email = match.group().lower()
    local, domain = email.split("@", 1)

    # Check automated first (overrides domain checks)
    local_base = local.replace(".", "").replace("-", "").replace("_", "")
    for prefix in _AUTOMATED_PREFIXES:
        normalized = prefix.replace("-", "")
        if local_base == normalized or local_base.startswith(normalized):
            return "automated"

    # Check internal domains from user config
    internal_domains = get_internal_domains()
    if domain in internal_domains:
        return "internal"

    if domain in _PERSONAL_DOMAINS:
        return "personal"

    return "external_client"
