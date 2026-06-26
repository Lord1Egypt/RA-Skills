#!/usr/bin/env python3
"""
One safer Yahoo email purge cycle.

What it does:
1. Move up to N messages from INBOX into the first export folder with room.
2. Download messages currently in that export folder to local .eml files.
3. Delete only the messages that were successfully downloaded in this run.

Safety upgrades over the original:
- Uses UID-based fetch/delete in the export folder instead of unstable sequence deletes.
- Never clears an entire export folder blindly.
- Saves raw .eml before metadata; metadata failures do not lose the email.
- Has a lock file so overlapping cron/manual runs do not stomp each other.
- Supports --dry-run and --no-delete.
- Credentials can come from env vars; existing literal fallback retained for compatibility.
"""

from __future__ import annotations

import argparse
import email
import email.header
import imaplib
import json
import os
import re
import sys
import time
from contextlib import suppress
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Iterable

HOST = os.environ.get("YAHOO_IMAP_HOST", "imap.mail.yahoo.com")
PORT = int(os.environ.get("YAHOO_IMAP_PORT", "993"))
ACCOUNT = os.environ.get("YAHOO_EMAIL", "your-email@yahoo.com")
PASSWORD = os.environ.get("YAHOO_PASSWORD")

EXPORT_FOLDERS = ["export1", "export2", "export3"]
DEFAULT_MOVE_BATCH = 8999  # Yahoo gets cranky at 10000.
MOVE_CHUNK = 1000
DELETE_CHUNK = 1000

BASE_DIR = Path(os.environ.get("EMAIL_PURGE_DIR", "~/email-purge")).expanduser()
LOG_FILE = BASE_DIR / "logs" / "purge_cycle.log"
LOCK_FILE = BASE_DIR / "metadata" / "purge_cycle.lock"
STATE_FILE = BASE_DIR / "metadata" / "purge_cycle_state.json"


class PurgeError(RuntimeError):
    pass


def log(msg: str) -> None:
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def decode_header(value: str | None) -> str:
    if not value:
        return ""
    pieces: list[str] = []
    for part, charset in email.header.decode_header(value):
        if isinstance(part, bytes):
            # Yahoo mail contains garbage charset labels. Treat them as advisory.
            try:
                pieces.append(part.decode(charset or "utf-8", errors="replace"))
            except (LookupError, TypeError):
                pieces.append(part.decode("utf-8", errors="replace"))
        else:
            pieces.append(str(part))
    return " ".join(pieces).strip()


def extract_metadata(raw: bytes, folder: str, uid: int) -> dict:
    msg = email.message_from_bytes(raw)
    date_raw = msg.get("Date", "")
    try:
        date_iso = parsedate_to_datetime(date_raw).isoformat() if date_raw else ""
    except Exception:
        date_iso = date_raw[:100]

    attachments: list[str] = []
    if msg.is_multipart():
        for part in msg.walk():
            disposition = str(part.get("Content-Disposition", "")).lower()
            if "attachment" in disposition:
                filename = part.get_filename()
                attachments.append(decode_header(filename) if filename else "")

    return {
        "folder": folder,
        "uid": uid,
        "message_id": str(msg.get("Message-ID", ""))[:300],
        "subject": decode_header(msg.get("Subject"))[:500],
        "from": decode_header(msg.get("From"))[:500],
        "to": decode_header(msg.get("To"))[:500],
        "date": date_iso,
        "has_attachments": bool(attachments),
        "attachments": attachments[:50],
        "downloaded_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }


def chunks(items: list[bytes], size: int) -> Iterable[list[bytes]]:
    for i in range(0, len(items), size):
        yield items[i : i + size]


class Yahoo:
    def __init__(self) -> None:
        self.mail: imaplib.IMAP4_SSL | None = None
        self.selected: str | None = None

    def connect(self) -> None:
        self.close()
        self.mail = imaplib.IMAP4_SSL(HOST, PORT)
        self.mail.login(ACCOUNT, PASSWORD)
        self.selected = None

    def close(self) -> None:
        if self.mail is not None:
            with suppress(Exception):
                self.mail.logout()
        self.mail = None
        self.selected = None

    def ensure(self) -> imaplib.IMAP4_SSL:
        if self.mail is None:
            self.connect()
        assert self.mail is not None
        return self.mail

    def reconnect(self) -> None:
        previous = self.selected
        log("  Reconnecting to Yahoo IMAP")
        self.connect()
        if previous:
            self.select(previous, readonly=False)

    def select(self, folder: str, readonly: bool = False) -> int:
        m = self.ensure()
        typ, data = m.select(f'"{folder}"', readonly=readonly)
        if typ != "OK":
            raise PurgeError(f"Cannot select {folder}: {data}")
        self.selected = folder
        return int(data[0] or 0)

    def count(self, folder: str) -> int:
        m = self.ensure()
        typ, data = m.status(f'"{folder}"', "(MESSAGES)")
        if typ == "OK" and data:
            match = re.search(r"MESSAGES (\d+)", str(data))
            if match:
                return int(match.group(1))
        return 0

    def uid_search_all(self, folder: str) -> list[bytes]:
        self.select(folder, readonly=False)
        typ, data = self.ensure().uid("search", None, "ALL")
        if typ != "OK":
            raise PurgeError(f"UID search failed in {folder}: {data}")
        return data[0].split() if data and data[0] else []


def acquire_lock(force: bool = False) -> None:
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    if LOCK_FILE.exists() and not force:
        try:
            lock = json.loads(LOCK_FILE.read_text())
        except Exception:
            lock = {"raw": LOCK_FILE.read_text(errors="replace")}
        raise PurgeError(f"Lock exists at {LOCK_FILE}: {lock}. Use --force-lock if stale.")
    LOCK_FILE.write_text(json.dumps({"pid": os.getpid(), "started_at": time.time()}, indent=2))


def release_lock() -> None:
    with suppress(FileNotFoundError):
        LOCK_FILE.unlink()


def move_from_inbox(y: Yahoo, target: str, amount: int, dry_run: bool) -> int:
    inbox = y.select("INBOX", readonly=False)
    amount = min(amount, inbox)
    if amount <= 0:
        return 0
    if dry_run:
        log(f"DRY RUN: would move {amount} messages from INBOX to {target}")
        return 0

    moved = 0
    while moved < amount:
        chunk = min(MOVE_CHUNK, amount - moved)
        try:
            # Repeatedly moving 1:N is intentional: after MOVE, the next messages shift down.
            typ, data = y.ensure()._simple_command("MOVE", f"1:{chunk}", target)
            if typ != "OK":
                raise PurgeError(f"MOVE failed: {typ} {data}")
            moved += chunk
            log(f"  Moved {chunk} -> {target} ({moved} total)")
            time.sleep(2)
        except Exception as e:
            log(f"  MOVE error after {moved}: {e}")
            y.reconnect()
            break
    return moved


def download_export_folder(y: Yahoo, folder: str, delete_after: bool, dry_run: bool) -> tuple[int, int, int]:
    uids = y.uid_search_all(folder)
    total = len(uids)
    if total == 0:
        log(f"  {folder}: empty")
        return (0, 0, 0)

    folder_dir = BASE_DIR / "eml" / folder
    meta_file = BASE_DIR / "metadata" / f"emails_{folder}.jsonl"
    folder_dir.mkdir(parents=True, exist_ok=True)
    meta_file.parent.mkdir(parents=True, exist_ok=True)

    log(f"  {folder}: {total} messages available to download")
    if dry_run:
        log(f"DRY RUN: would fetch {total} messages from {folder}")
        return (0, 0, 0)

    downloaded_uids: list[bytes] = []
    skipped_existing = 0
    errors = 0

    with meta_file.open("a", encoding="utf-8") as meta_f:
        for index, uid in enumerate(uids, start=1):
            uid_int = int(uid)
            eml_path = folder_dir / f"{uid_int}.eml"
            if eml_path.exists() and eml_path.stat().st_size > 0:
                skipped_existing += 1
                downloaded_uids.append(uid)
                continue

            try:
                typ, data = y.ensure().uid("fetch", uid, "(RFC822)")
                if typ != "OK" or not data or not data[0] or not isinstance(data[0], tuple):
                    raise PurgeError(f"bad fetch response: {typ} {data[:1] if data else data}")
                raw = data[0][1]
                if not raw:
                    raise PurgeError("empty RFC822 payload")

                eml_path.write_bytes(raw)
                meta_f.write(json.dumps(extract_metadata(raw, folder, uid_int), ensure_ascii=False) + "\n")
                downloaded_uids.append(uid)

                if len(downloaded_uids) % 100 == 0:
                    log(f"  Downloaded/verified {len(downloaded_uids)}/{total} ({errors} errors)")
                if index % 1000 == 0:
                    y.reconnect()
                    y.select(folder, readonly=False)
            except Exception as e:
                errors += 1
                log(f"  Error fetching UID {uid.decode(errors='replace')}: {e}")
                if errors % 10 == 0:
                    y.reconnect()
                    y.select(folder, readonly=False)

    deleted = 0
    if delete_after and downloaded_uids:
        log(f"  Deleting {len(downloaded_uids)} successfully downloaded messages from {folder}")
        y.select(folder, readonly=False)
        for batch in chunks(downloaded_uids, DELETE_CHUNK):
            uid_set = b",".join(batch).decode("ascii")
            try:
                typ, _ = y.ensure().uid("store", uid_set, "+FLAGS", "\\Deleted")
                if typ != "OK":
                    raise PurgeError(f"UID STORE returned {typ}")
                y.ensure().expunge()
                deleted += len(batch)
                log(f"    Deleted {deleted}/{len(downloaded_uids)}")
                time.sleep(1)
            except Exception as e:
                log(f"    Delete error after {deleted}: {e}")
                y.reconnect()
                y.select(folder, readonly=False)
                break
    elif not delete_after:
        log("  --no-delete set; leaving downloaded messages in export folder")

    return (len(downloaded_uids), errors, deleted)


def write_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one safe Yahoo purge cycle")
    parser.add_argument("--move-batch", type=int, default=DEFAULT_MOVE_BATCH)
    parser.add_argument("--no-delete", action="store_true", help="download but do not delete from export folder")
    parser.add_argument("--dry-run", action="store_true", help="show intended actions without changing Yahoo")
    parser.add_argument("--force-lock", action="store_true", help="ignore a stale lock file")
    args = parser.parse_args()

    state: dict = {"started_at": time.time(), "status": "running", "dry_run": args.dry_run}
    log("=== Purge Cycle ===")

    try:
        acquire_lock(force=args.force_lock)
        y = Yahoo()
        if not PASSWORD:
            raise PurgeError("YAHOO_PASSWORD environment variable is required")
        y.connect()
        log(f"Connected to {HOST} as {ACCOUNT}")

        inbox = y.count("INBOX")
        log(f"INBOX: {inbox}")
        state["inbox_start"] = inbox
        if inbox <= 0:
            log("INBOX empty - nothing to do")
            state["status"] = "empty"
            write_state(state)
            return 0

        target = None
        folder_counts: dict[str, int] = {}
        for folder in EXPORT_FOLDERS:
            folder_counts[folder] = y.count(folder)
            if target is None and folder_counts[folder] < 10000:
                target = folder
        state["export_counts_start"] = folder_counts

        if target is None:
            raise PurgeError("All export folders are full; download/clear them before moving more mail.")

        room = max(0, 10000 - folder_counts[target])
        move_amount = min(args.move_batch, room, inbox)
        log(f"Step 1: Moving {move_amount} to {target} (room={room})")
        moved = move_from_inbox(y, target, move_amount, args.dry_run)
        log(f"Moved {moved} messages")
        state.update({"target": target, "requested_move": move_amount, "moved": moved})

        log(f"Step 2: Downloading {target}")
        downloaded, errors, deleted = download_export_folder(
            y,
            target,
            delete_after=not args.no_delete,
            dry_run=args.dry_run,
        )
        log(f"Downloaded/verified {downloaded} messages; errors={errors}; deleted={deleted}")
        state.update({"downloaded_or_verified": downloaded, "download_errors": errors, "deleted": deleted})

        inbox_final = y.count("INBOX")
        log(f"Final: INBOX={inbox_final}")
        state["inbox_final"] = inbox_final
        state["export_counts_final"] = {folder: y.count(folder) for folder in EXPORT_FOLDERS}
        for folder, c in state["export_counts_final"].items():
            if c > 0:
                log(f"  {folder}: {c}")

        y.close()
        state["status"] = "ok" if errors == 0 else "partial"
        log("=== Cycle Complete ===")
        return 0 if errors == 0 else 2
    except Exception as e:
        state["status"] = "error"
        state["error"] = str(e)
        log(f"ERROR: {e}")
        return 1
    finally:
        state["finished_at"] = time.time()
        write_state(state)
        release_lock()


if __name__ == "__main__":
    sys.exit(main())
