#!/usr/bin/env python3
"""
Voice Note Transcriber → Obsidian
Fetches voice-note emails via IMAP, transcribes with Whisper, saves to Obsidian fleeting folder.
"""
import os
import sys
import json
import tempfile
import subprocess
from datetime import datetime, timezone

# ── Configuration ────────────────────────────────────────────────────────────

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_PROVIDER = os.getenv("EMAIL_PROVIDER", "gmail")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Obsidian vault — the VAULT PATH must be the root, fleeting folder is relative
OBSIDIAN_VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH", "")
FLEETING_FOLDER = os.getenv("FLEETING_FOLDER", "0-Inbox")

VOICE_NOTE_KEYWORD = os.getenv("VOICE_NOTE_KEYWORD", "Voice Note")
MARK_EMAIL_READ = os.getenv("MARK_EMAIL_READ", "true").lower() == "true"

AUDIO_EXTENSIONS = tuple(os.getenv(
    "AUDIO_EXTENSIONS", ".mp3,.wav,.m4a,.webm,.ogg,.flac"
).split(","))

# ── Email provider configs ───────────────────────────────────────────────────

EMAIL_PROVIDERS = {
    "gmail": {"imap_host": "imap.gmail.com", "imap_port": 993},
    "outlook": {"imap_host": "imap-mail.outlook.com", "imap_port": 993},
    "163.com": {"imap_host": "imap.163.com", "imap_port": 993},
    "126.com": {"imap_host": "imap.126.com", "imap_port": 993},
    "vip.163.com": {"imap_host": "imap.vip.163.com", "imap_port": 993},
    "188.com": {"imap_host": "imap.188.com", "imap_port": 993},
}

# ── Helpers ──────────────────────────────────────────────────────────────────

def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def check_deps():
    if not EMAIL_ADDRESS:
        die("EMAIL_ADDRESS is not set")
    if not EMAIL_PASSWORD:
        die("EMAIL_PASSWORD is not set")
    if not OPENAI_API_KEY:
        die("OPENAI_API_KEY is not set")
    if not OBSIDIAN_VAULT_PATH:
        die("OBSIDIAN_VAULT_PATH is not set")


def fleeting_path() -> str:
    """Return the absolute path to the fleeting notes folder inside the vault."""
    path = os.path.join(OBSIDIAN_VAULT_PATH, FLEETING_FOLDER)
    os.makedirs(path, exist_ok=True)
    return path


def transcribe(audio_path: str) -> str:
    """Transcribe audio via OpenAI Whisper API (curl)."""
    cmd = [
        "curl", "-sS", "https://api.openai.com/v1/audio/transcriptions",
        "-H", f"Authorization: Bearer {OPENAI_API_KEY}",
        "-F", f"file=@{audio_path}",
        "-F", "model=whisper-1",
        "-F", "response_format=json",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  Whisper API error: {result.stderr.strip()}")
        return ""
    try:
        data = json.loads(result.stdout)
        return data.get("text", "")
    except json.JSONDecodeError:
        # response_format=text fallback
        return result.stdout.strip()


def save_note(transcript: str, subject: str, sender: str, date_str: str) -> str:
    """Write a fleeting note to the Obsidian vault and return its path."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    filename = f"{timestamp} Voice Note.md"
    filepath = os.path.join(fleeting_path(), filename)

    content = f"""---
tags:
  - type/transcript
  - source/voice-note
date: {today}
email_subject: "{subject}"
email_from: "{sender}"
---

# Voice Note Transcript — {today}

## Transcript

{transcript}

## Source

- **Subject:** {subject}
- **From:** {sender}
- **Date:** {date_str}
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


# ── IMAP processing ─────────────────────────────────────────────────────────

def fetch_and_process():
    """Main flow: connect IMAP → filter → download → transcribe → save."""
    from imbox import Imbox  # lazy import

    provider = EMAIL_PROVIDERS.get(EMAIL_PROVIDER, EMAIL_PROVIDERS["gmail"])
    imap_host = provider["imap_host"]
    imap_port = provider["imap_port"]

    print(f"Connecting to {imap_host}:{imap_port} …")

    with Imbox(imap_host, username=EMAIL_ADDRESS, password=EMAIL_PASSWORD,
               ssl=True, port=imap_port) as imbox:

        messages = imbox.messages(unread=True)
        count = 0

        for uid, msg in messages:
            subject = msg.subject or ""
            if VOICE_NOTE_KEYWORD.lower() not in subject.lower():
                continue

            sender = ""
            if msg.sent_from:
                first = msg.sent_from[0]
                sender = first.get("email", first.get("name", "Unknown"))

            date_str = str(msg.date) if msg.date else ""

            # Find audio attachments
            audio_attachments = [
                a for a in msg.attachments
                if isinstance(a.get("filename", ""), str)
                and a["filename"].lower().endswith(AUDIO_EXTENSIONS)
            ]

            if not audio_attachments:
                print(f"  No audio attachments in: {subject}")
                continue

            print(f"  Processing: {subject} ({len(audio_attachments)} attachment(s))")

            for att in audio_attachments:
                filename = att["filename"]
                content = att.get("content", att.get("data"))

                if content is None:
                    print(f"    Skipping {filename}: no content")
                    continue

                with tempfile.NamedTemporaryFile(
                    suffix=f"_{filename}", delete=False
                ) as tmp:
                    if isinstance(content, bytes):
                        tmp.write(content)
                    else:
                        tmp.write(content.encode("utf-8", errors="replace"))
                    tmp_path = tmp.name

                try:
                    transcript = transcribe(tmp_path)
                finally:
                    os.unlink(tmp_path)

                if not transcript:
                    print(f"    Empty transcript for {filename}")
                    continue

                note_path = save_note(transcript, subject, sender, date_str)
                print(f"    ✓ Saved: {note_path}")
                count += 1

            if MARK_EMAIL_READ:
                try:
                    imbox.mark_seen(uid)
                    print(f"  Marked as read: {subject}")
                except Exception as e:
                    print(f"  Could not mark as read: {e}")

    print(f"\nDone — {count} transcript(s) saved to {fleeting_path()}")


# ── Entry ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    check_deps()
    fetch_and_process()
