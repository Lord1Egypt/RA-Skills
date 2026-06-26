"""Parse raw RFC-822 email bytes into a normalized struct for the detection pipeline.

Consumed by:
- `tests/` on committed `.eml` fixtures
- `gog_client.py` which calls `gog gmail get --format full --json` and decodes the raw MIME
"""

from __future__ import annotations

import email
import re
from dataclasses import dataclass, field
from email.header import decode_header, make_header
from email.message import Message
from email.utils import parseaddr
from typing import Union

from bs4 import BeautifulSoup

_URL_RE = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)


@dataclass
class ParsedEmail:
    from_address: str                          # e.g. "bob@scam.xyz"
    from_display: str                          # e.g. "PayPal Support"
    from_domain: str                           # e.g. "scam.xyz"
    subject: str
    message_id: str                            # including angle brackets
    body_plain: str                            # html stripped, best-effort plain
    urls: list[str] = field(default_factory=list)
    authentication_results: str | None = None  # raw `Authentication-Results` header if present


def parse_eml(raw: Union[bytes, str]) -> ParsedEmail:
    msg = _load(raw)

    from_hdr = _decode_header(msg.get("From", ""))
    display, addr = parseaddr(from_hdr)
    if not addr:
        raise ValueError("missing From header")
    from_domain = addr.split("@", 1)[1].lower() if "@" in addr else ""

    subject = _decode_header(msg.get("Subject", ""))
    message_id = _decode_header(msg.get("Message-ID", ""))
    auth = msg.get("Authentication-Results")
    auth = _decode_header(auth) if auth else None

    body_plain = _extract_body(msg)
    urls = _URL_RE.findall(body_plain)

    return ParsedEmail(
        from_address=addr,
        from_display=display,
        from_domain=from_domain,
        subject=subject,
        message_id=message_id,
        body_plain=body_plain,
        urls=urls,
        authentication_results=auth,
    )


def _load(raw: Union[bytes, str]) -> Message:
    if isinstance(raw, str):
        return email.message_from_string(raw)
    return email.message_from_bytes(raw)


def _decode_header(value: str) -> str:
    if not value:
        return ""
    try:
        return str(make_header(decode_header(value))).strip()
    except Exception:
        return value.strip()


def _extract_body(msg: Message) -> str:
    plain = None
    html = None

    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if part.get("Content-Disposition", "").lower().startswith("attachment"):
                continue
            if ctype == "text/plain" and plain is None:
                plain = _decode_payload(part)
            elif ctype == "text/html" and html is None:
                html = _decode_payload(part)
    else:
        ctype = msg.get_content_type()
        if ctype == "text/html":
            html = _decode_payload(msg)
        else:
            plain = _decode_payload(msg)

    if plain is not None and plain.strip():
        return plain
    if html is not None:
        return _html_to_text(html)
    return ""


def _decode_payload(part: Message) -> str:
    payload = part.get_payload(decode=True)
    if payload is None:
        return ""
    charset = part.get_content_charset() or "utf-8"
    try:
        return payload.decode(charset, errors="replace")
    except LookupError:
        return payload.decode("utf-8", errors="replace")


def _html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href and href not in a.get_text(strip=True):
            a.append(f" {href}")
    return soup.get_text(separator=" ", strip=True)
