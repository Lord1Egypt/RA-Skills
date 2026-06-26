"""WhatsApp chat export ingestion for YouOS."""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from app.core.config import get_user_names, get_user_timezone
from app.ingestion.models import IngestionResult
from app.ingestion.run_log import IngestRunContext, IngestRunCounts, finish_ingest_run, start_ingest_run

EXPECTED_EXPORT_FORMAT = """
Expected WhatsApp export input:

- UTF-8 text export from WhatsApp chat export
- one message per line in the typical exported transcript format
- optional media omitted for the first implementation

Example:
12/31/25, 9:41 PM - Alice: Message text
12/31/25, 9:45 PM - User: Reply text
""".strip()

# Regex: MM/DD/YY, H:MM AM/PM - Sender: Message
LINE_RE = re.compile(r"^(\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}\s*[APap][Mm])\s*-\s*(.+?):\s(.+)$")


@dataclass(slots=True)
class ParsedMessage:
    timestamp: str
    sender: str
    text: str


@dataclass(slots=True)
class WhatsAppIngestCounts:
    total_lines: int = 0
    parsed_messages: int = 0
    inbound_documents: int = 0
    reply_pairs: int = 0


def parse_whatsapp_export(text: str) -> list[ParsedMessage]:
    """Parse a WhatsApp text export into structured messages."""
    messages: list[ParsedMessage] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        m = LINE_RE.match(line)
        if m:
            messages.append(
                ParsedMessage(
                    timestamp=m.group(1).strip(),
                    sender=m.group(2).strip(),
                    text=m.group(3).strip(),
                )
            )
        elif messages:
            # Continuation line — append to previous message
            messages[-1].text += "\n" + line
    return messages


def _is_user_message(sender: str, user_names: tuple[str, ...]) -> bool:
    """Check if sender matches any configured user name (case-insensitive)."""
    sender_lower = sender.lower()
    for name in user_names:
        if name.lower() == sender_lower:
            return True
    return False


def build_reply_pairs(
    messages: list[ParsedMessage],
    user_names: tuple[str, ...],
) -> list[tuple[ParsedMessage, ParsedMessage]]:
    """Pair a run of consecutive inbound messages with the next user reply.

    Accumulates consecutive inbound messages (the other party often sends several
    in a row) and pairs the whole block with the next user reply — the previous
    i/i+1 pairing silently dropped all but the last inbound message of a run.
    """
    pairs: list[tuple[ParsedMessage, ParsedMessage]] = []
    pending: list[ParsedMessage] = []
    for msg in messages:
        if _is_user_message(msg.sender, user_names):
            if pending:
                block = ParsedMessage(
                    timestamp=pending[-1].timestamp,
                    sender=pending[-1].sender,
                    text="\n".join(m.text for m in pending),
                )
                pairs.append((block, msg))
                pending = []
            # A user message with no preceding inbound is user-initiated; skip.
        else:
            pending.append(msg)
    return pairs


def _parse_timestamp(ts: str, *, tz_name: str | None = None) -> str | None:
    """Convert WhatsApp timestamp to tz-aware ISO format.

    WhatsApp export timestamps are tz-naive (`3/14/24, 3:30 PM`). Storing
    them without a timezone meant recency-boost and any time-window query
    sorted WhatsApp pairs incorrectly relative to Gmail pairs (which are
    tz-aware via RFC 2822). Now: attach the configured `user.timezone`
    (or UTC if unset / unknown / pytz unavailable) so the persisted ISO
    string carries an offset.

    Defaulting to UTC rather than the system's local time because the
    *server* clock may be in a different zone than the device that
    produced the export — UTC keeps timestamps monotonic across sources,
    even if the wall-clock interpretation is wrong by a few hours.
    """
    if tz_name is None:
        tz_name = get_user_timezone()

    # Resolve the timezone. `zoneinfo` is stdlib in Py>=3.9. If the user
    # configured a string that doesn't resolve (typo, unknown zone), fall
    # back to UTC rather than dropping the timestamp entirely.
    try:
        from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

        try:
            tzinfo = ZoneInfo(tz_name)
        except ZoneInfoNotFoundError:
            tzinfo = timezone.utc
    except ImportError:
        tzinfo = timezone.utc

    for fmt in ("%m/%d/%y, %I:%M %p", "%m/%d/%Y, %I:%M %p"):
        try:
            dt = datetime.strptime(ts, fmt)
            return dt.replace(tzinfo=tzinfo).isoformat()
        except ValueError:
            continue
    return None


def _content_fingerprint(*parts: str) -> str:
    """Stable short hash of message content for source_id disambiguation.

    Two messages in the same minute from the same sender used to collide
    on `source_id = wa-{chat}-{ts}-{sender}` (WhatsApp timestamps have
    minute resolution and INSERT OR IGNORE silently dropped the
    duplicate). Appending an 8-char content hash gives a deterministic,
    collision-resistant per-content suffix: re-ingesting the same export
    produces the same IDs (idempotent), but distinct same-minute messages
    now get distinct IDs.

    Note: this changes the on-disk `source_id` shape relative to pre-PR
    rows. A re-ingest after upgrade will produce *additional* rows for
    the same messages because old IDs (no suffix) don't match new IDs
    (with suffix). Documented in the PR; users who care can wipe
    WhatsApp rows and re-import.
    """
    h = hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()
    return h[:8]


def ingest_whatsapp_export(
    export_path: Path,
    *,
    db_path: Path | None = None,
    user_names: tuple[str, ...] = (),
) -> IngestionResult:
    """Parse a WhatsApp export file and ingest into the corpus."""
    if not export_path.exists():
        return IngestionResult(
            source_type="whatsapp_export",
            status="failed",
            detail=f"File not found: {export_path}",
        )

    text = export_path.read_text(encoding="utf-8")
    messages = parse_whatsapp_export(text)

    if not user_names:
        user_names = get_user_names()

    if not user_names:
        # Without configured names we can't tell the user's messages from the
        # other party's. Bail rather than store every message as inbound (which
        # would pollute the corpus and produce zero reply pairs).
        return IngestionResult(
            source_type="whatsapp_export",
            status="failed",
            detail="No user names configured — set `user.names` in your config so WhatsApp ingestion can identify your own messages. Nothing was ingested.",
        )

    counts = WhatsAppIngestCounts(total_lines=len(text.splitlines()), parsed_messages=len(messages))

    if not messages:
        return IngestionResult(
            source_type="whatsapp_export",
            status="completed",
            detail="No messages parsed from export file.",
        )

    pairs = build_reply_pairs(messages, user_names)

    if db_path is None:
        from app.core.settings import get_settings
        from app.db.bootstrap import resolve_sqlite_path

        settings = get_settings()
        db_path = resolve_sqlite_path(settings.database_url)

    run_id = f"whatsapp-{uuid.uuid4()}"
    conn = sqlite3.connect(db_path)
    try:
        context = IngestRunContext(run_id=run_id, source="whatsapp")
        start_ingest_run(conn, context)
        conn.commit()

        chat_name = export_path.stem
        run_counts = IngestRunCounts(discovered=len(messages), fetched=len(messages))

        # Insert inbound messages as documents. The content fingerprint
        # disambiguates messages that share a minute + sender; without it,
        # bursts of messages in the same minute silently lost all but the
        # first to INSERT OR IGNORE.
        for msg in messages:
            if _is_user_message(msg.sender, user_names):
                continue
            content_fp = _content_fingerprint(msg.text, msg.sender)
            source_id = f"wa-{chat_name}-{msg.timestamp}-{msg.sender}-{content_fp}"
            iso_ts = _parse_timestamp(msg.timestamp)
            try:
                conn.execute(
                    """INSERT OR IGNORE INTO documents
                       (source_type, source_id, title, author, content, metadata_json,
                        ingestion_run_id, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        "whatsapp_export",
                        source_id,
                        f"WhatsApp: {chat_name}",
                        msg.sender,
                        msg.text,
                        json.dumps({"chat": chat_name, "timestamp": msg.timestamp}),
                        run_id,
                        iso_ts,
                    ),
                )
                if conn.execute("SELECT changes()").fetchone()[0] > 0:
                    counts.inbound_documents += 1
                    run_counts.stored_documents += 1
            except sqlite3.IntegrityError:
                pass

        # Insert reply pairs. Same content-fingerprint disambiguation:
        # pair_source_id used to collide on (chat, inbound_ts, reply_ts)
        # alone, which loses a pair whenever two distinct inbounds in the
        # same minute were each replied to in the same minute. Inbound
        # fingerprint disambiguates the inbound side; reply fingerprint
        # the reply side.
        for inbound, reply in pairs:
            inbound_fp = _content_fingerprint(inbound.text, inbound.sender)
            reply_fp = _content_fingerprint(reply.text, reply.sender)
            pair_source_id = f"wa-{chat_name}-{inbound.timestamp}-{inbound_fp}-{reply.timestamp}-{reply_fp}"
            iso_ts = _parse_timestamp(reply.timestamp)

            # Find the document_id for this inbound message — by the same
            # source_id we used in the document insert above so the link
            # points at the right row even when collisions are present.
            doc_source_id = f"wa-{chat_name}-{inbound.timestamp}-{inbound.sender}-{inbound_fp}"
            doc_row = conn.execute("SELECT id FROM documents WHERE source_id = ?", (doc_source_id,)).fetchone()
            doc_id = doc_row[0] if doc_row else None

            try:
                conn.execute(
                    """INSERT OR IGNORE INTO reply_pairs
                       (source_type, source_id, document_id, inbound_text, reply_text,
                        inbound_author, reply_author, paired_at, metadata_json)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        "whatsapp_export",
                        pair_source_id,
                        doc_id,
                        inbound.text,
                        reply.text,
                        inbound.sender,
                        "user",
                        iso_ts,
                        json.dumps({"chat": chat_name}),
                    ),
                )
                if conn.execute("SELECT changes()").fetchone()[0] > 0:
                    counts.reply_pairs += 1
                    run_counts.stored_reply_pairs += 1
            except sqlite3.IntegrityError:
                pass

        finish_ingest_run(
            conn,
            run_id=run_id,
            status="completed",
            counts=run_counts,
        )
        conn.commit()
    finally:
        conn.close()

    return IngestionResult(
        source_type="whatsapp_export",
        status="completed",
        detail=(
            f"Parsed {counts.parsed_messages} messages, "
            f"stored {counts.inbound_documents} inbound docs, "
            f"{counts.reply_pairs} reply pairs from {export_path.name}"
        ),
        run_id=run_id,
    )
