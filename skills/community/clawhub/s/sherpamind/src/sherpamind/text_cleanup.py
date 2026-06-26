from __future__ import annotations

import html
import re


HTML_TAG_RE = re.compile(r"<[^>]+>")
BR_RE = re.compile(r"<\s*br\s*/?>", re.IGNORECASE)
P_CLOSE_RE = re.compile(r"</p\s*>", re.IGNORECASE)
TABLE_RE = re.compile(r"<table[\s\S]*?</table>", re.IGNORECASE)
MULTISPACE_RE = re.compile(r"[ \t]+")
MULTIBLANK_RE = re.compile(r"\n{3,}")
UPLOADED_FILE_RE = re.compile(r"Following file(?:s)? (?:was|were) uploaded:.*", re.IGNORECASE)
EMAIL_PARSER_RE = re.compile(r"This (?:ticket was created|response was entered) via the email parser\.?", re.IGNORECASE)
NOTICE_RE = re.compile(r"NOTICE:.*", re.IGNORECASE)
BITDEFENDER_RE = re.compile(r"https?://lsems\.gravityzone\.bitdefender\.com/scan/\S+", re.IGNORECASE)
MAILTO_RE = re.compile(r"mailto:[^\s>]+", re.IGNORECASE)
URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)
REPLY_HEADER_RE = re.compile(r"^(on .+ wrote:|from:|sent:|to:|subject:)\s*$", re.IGNORECASE)
SIGNATURE_MARKERS = [
    "NOTICE:",
    "This message is intended exclusively",
    "Connect with me on",
    "LT.agency",
    "Patrol Division",
    "Police Department",
    "Sent from my",
    "Get Outlook for",
]


def _strip_reply_tail(lines: list[str]) -> list[str]:
    kept: list[str] = []
    for line in lines:
        lower = line.lower().strip()
        if line.startswith('>'):
            break
        if REPLY_HEADER_RE.match(lower):
            break
        if lower.startswith('on ') and ' wrote:' in lower:
            break
        if lower.startswith('________________________________'):
            break
        if lower.startswith('-----original message-----'):
            break
        if lower.startswith('begin forwarded message'):
            break
        kept.append(line)
    return kept


def normalize_ticket_text(value: str | None) -> str:
    if not value:
        return ""
    text = value
    text = BR_RE.sub("\n", text)
    text = P_CLOSE_RE.sub("\n", text)
    text = TABLE_RE.sub("\n", text)
    text = HTML_TAG_RE.sub(" ", text)
    text = html.unescape(text)
    text = BITDEFENDER_RE.sub(" ", text)
    text = MAILTO_RE.sub(" ", text)
    text = URL_RE.sub(" ", text)
    text = UPLOADED_FILE_RE.sub(" ", text)
    text = EMAIL_PARSER_RE.sub(" ", text)
    text = NOTICE_RE.sub(" ", text)
    lines = []
    for raw_line in text.splitlines():
        line = MULTISPACE_RE.sub(" ", raw_line).strip(" \t\r\u200b")
        if not line:
            lines.append("")
            continue
        if any(marker.lower() in line.lower() for marker in SIGNATURE_MARKERS):
            break
        lines.append(line)
    lines = _strip_reply_tail(lines)
    text = "\n".join(lines)
    text = MULTIBLANK_RE.sub("\n\n", text).strip()
    return text


def summarize_resolution_from_logs(log_text: str | None) -> str | None:
    cleaned = normalize_ticket_text(log_text)
    if not cleaned:
        return None
    parts = [part.strip() for part in cleaned.split("---") if part.strip()]
    if not parts:
        return None
    return parts[0][:600]
