"""
collectors/email.py — Email Collector (IMAP)

Collects emails from IMAP mailboxes. Supports incremental collection
and basic content filtering.
"""

from __future__ import annotations

import email
import logging
import time
from email.header import decode_header
from typing import Any

from .base import MemoryCollector, RawMemory, CollectionResult, CollectorStatus

logger = logging.getLogger(__name__)


class EmailConfig:
    """IMAP email configuration."""
    def __init__(self, host: str = "", port: int = 993,
                 username: str = "", password: str = "",
                 folder: str = "INBOX", tenant_id: str = "work",
                 reliability_score: float = 0.85,
                 max_emails_per_sync: int = 50):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.folder = folder
        self.tenant_id = tenant_id
        self.reliability_score = reliability_score
        self.max_emails_per_sync = max_emails_per_sync


class EmailCollector(MemoryCollector):
    """Collect emails from an IMAP mailbox."""

    def __init__(self, config: EmailConfig | dict | None = None):
        if isinstance(config, EmailConfig):
            cfg = config
        else:
            d = config or {}
            cfg = EmailConfig(**{k: v for k, v in d.items()
                                 if k in EmailConfig.__dataclass_fields__})
        super().__init__(config={
            "host": cfg.host, "port": cfg.port,
            "username": cfg.username, "folder": cfg.folder,
            "tenant_id": cfg.tenant_id,
            "reliability_score": cfg.reliability_score,
            "max_emails_per_sync": cfg.max_emails_per_sync,
        })
        self._email_config = cfg

    def get_source_id(self) -> str:
        return "email"

    def test_connection(self) -> bool:
        if not self._email_config.host:
            return False
        try:
            import imaplib
            conn = imaplib.IMAP4_SSL(self._email_config.host, self._email_config.port)
            conn.login(self._email_config.username, self._email_config.password)
            conn.logout()
            return True
        except Exception as e:
            logger.error("Email connection test failed: %s", e)
            return False

    async def collect(self, since: float | None = None) -> CollectionResult:
        result = CollectionResult(
            source=self.get_source_id(),
            started_at=time.time(),
            status=CollectorStatus.SYNCING,
        )

        if not self._email_config.host:
            result.status = CollectorStatus.ERROR
            result.errors.append("No IMAP host configured")
            result.finished_at = time.time()
            return result

        try:
            import imaplib
            from email.utils import parsedate_to_datetime

            conn = imaplib.IMAP4_SSL(self._email_config.host, self._email_config.port)
            conn.login(self._email_config.username, self._email_config.password)
            conn.select(self._email_config.folder)

            # Search for emails since the given date
            if since:
                since_dt = time.strftime("%d-%b-%Y", time.gmtime(since))
                search_criteria = f'(SINCE "{since_dt}")'
            else:
                search_criteria = "ALL"

            _, msg_ids = conn.search(None, search_criteria)
            msg_id_list = msg_ids[0].split()[-self._email_config.max_emails_per_sync:]
            result.total_available = len(msg_ids[0].split())

            for mid in msg_id_list:
                try:
                    _, msg_data = conn.fetch(mid, "(RFC822)")
                    raw = self._process_email(msg_data[0][1])
                    if raw:
                        result.items.append(raw)
                        result.collected_count += 1
                    else:
                        result.skipped_count += 1
                except Exception as e:
                    result.error_count += 1
                    result.errors.append(str(e))

            conn.logout()
            self.last_sync = time.time()
            self._collect_count += result.collected_count
            result.status = CollectorStatus.IDLE

        except Exception as e:
            result.status = CollectorStatus.ERROR
            result.errors.append(str(e))
            self._error_count += 1

        result.finished_at = time.time()
        return result

    def _process_email(self, raw_email: bytes) -> RawMemory | None:
        """Parse a raw email into a RawMemory."""
        try:
            msg = email.message_from_bytes(raw_email)
            subject = self._decode_header(msg.get("Subject", ""))
            from_addr = self._decode_header(msg.get("From", ""))
            date_str = msg.get("Date", "")

            # Extract text body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        payload = part.get_payload(decode=True)
                        charset = part.get_content_charset() or "utf-8"
                        body = payload.decode(charset, errors="replace")
                        break
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    charset = msg.get_content_charset() or "utf-8"
                    body = payload.decode(charset, errors="replace")

            if not body or len(body) < 10:
                return None

            content = f"Subject: {subject}\nFrom: {from_addr}\n\n{body}"

            return RawMemory(
                content=content,
                source="email",
                source_id=f"email_{hash(subject + from_addr) % 100000}",
                timestamp=self._parse_date(date_str),
                metadata={
                    "subject": subject,
                    "from": from_addr,
                    "to": msg.get("To", ""),
                    "date": date_str,
                    "tenant_id": self._email_config.tenant_id,
                },
            )
        except Exception as e:
            logger.warning("Failed to parse email: %s", e)
            return None

    @staticmethod
    def _decode_header(value: str) -> str:
        """Decode email header value."""
        if not value:
            return ""
        parts = decode_header(value)
        decoded = []
        for part, encoding in parts:
            if isinstance(part, bytes):
                decoded.append(part.decode(encoding or "utf-8", errors="replace"))
            else:
                decoded.append(part)
        return " ".join(decoded)

    @staticmethod
    def _parse_date(date_str: str) -> float:
        """Parse email date to timestamp."""
        try:
            from email.utils import parsedate_to_datetime
            dt = parsedate_to_datetime(date_str)
            return dt.timestamp()
        except Exception:
            return time.time()
