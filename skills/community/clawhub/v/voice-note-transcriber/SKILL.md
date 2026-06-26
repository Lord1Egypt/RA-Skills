---
name: voice-note-transcriber
version: 1.0.0
description: >
  Fetch voice note emails via IMAP, transcribe attachments with OpenAI Whisper,
  and save transcripts to an Obsidian vault's fleeting notes folder.
author: workspace-hub
category: productivity
type: skill
license: MIT
tags:
  - voice-note
  - transcription
  - whisper
  - obsidian
  - email
  - imap
  - fleeting-notes
capabilities:
  - email_voice_note_retrieval
  - audio_transcription
  - obsidian_fleeting_note_creation
tools:
  - imap
  - openai-whisper-api
  - obsidian
metadata:
  openclaw:
    requires:
      env:
        - EMAIL_ADDRESS
        - EMAIL_PASSWORD
        - OPENAI_API_KEY
      bins:
        - python3
    config:
      obsidianVaultPath:
        description: Absolute path to the Obsidian vault root
        type: string
        default: ""
      fleetingFolder:
        description: Folder inside the vault for fleeting notes (relative to vault root)
        type: string
        default: "0-Inbox"
      emailProvider:
        description: Email provider key (gmail, outlook, 163.com, 126.com, etc.)
        type: string
        default: "gmail"
      subjectKeyword:
        description: Keyword to filter voice-note emails by subject
        type: string
        default: "Voice Note"
      audioExtensions:
        description: Recognised audio attachment extensions
        type: array
        default: [".mp3", ".wav", ".m4a", ".webm", ".ogg", ".flac"]
      markEmailRead:
        description: Mark processed emails as read
        type: boolean
        default: true
---

# Voice Note Transcriber → Obsidian

Fetch voice-note emails from IMAP, transcribe audio attachments with OpenAI
Whisper, and save the result as a fleeting note in your Obsidian vault.

## Quick start

```bash
python3 {skillDir}/scripts/transcribe_voice_notes.py
```

## Configuration

Set environment variables (or let the skill read from OpenClaw config):

| Variable | Required | Description |
|---|---|---|
| `EMAIL_ADDRESS` | ✅ | IMAP login address |
| `EMAIL_PASSWORD` | ✅ | App-specific password |
| `OPENAI_API_KEY` | ✅ | OpenAI API key |
| `OBSIDIAN_VAULT_PATH` | ✅ | Absolute path to Obsidian vault root |
| `EMAIL_PROVIDER` | | Provider key: `gmail` (default), `outlook`, `163.com`, `126.com` |
| `FLEETING_FOLDER` | | Vault subfolder for fleeting notes (default: `0-Inbox`) |
| `VOICE_NOTE_KEYWORD` | | Subject filter keyword (default: `Voice Note`) |
| `MARK_EMAIL_READ` | | `true` / `false` (default: `true`) |

### OpenClaw config example

```json5
{
  skills: {
    "voice-note-transcriber": {
      obsidianVaultPath: "/home/user/Documents/MyVault",
      fleetingFolder: "0-Inbox",
      emailProvider: "gmail",
      subjectKeyword: "Voice Note",
      markEmailRead: true,
    },
  },
}
```

## What it does

1. Connects to IMAP and fetches unread emails whose subject contains the
   configured keyword.
2. Downloads audio attachments (`.mp3`, `.wav`, `.m4a`, `.webm`, `.ogg`,
   `.flac`) to a temp directory.
3. Transcribes each attachment via the OpenAI Whisper API (`whisper-1`).
4. Writes a Markdown note with YAML frontmatter to the vault's fleeting
   folder.
5. Optionally marks the source email as read.

## Output note format

```markdown
---
tags:
  - type/transcript
  - source/voice-note
date: 2025-05-12
email_subject: "Voice Note — weekly recap"
email_from: sender@example.com
---

# Voice Note Transcript — 2025-05-12

## Transcript

(transcribed text here)

## Source

- **Subject:** Voice Note — weekly recap
- **From:** sender@example.com
- **Date:** Mon, 12 May 2025 08:00:00 +0800
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| "Missing OPENAI_API_KEY" | Export `OPENAI_API_KEY` or set it in OpenClaw config |
| Notes not appearing in Obsidian | Check `OBSIDIAN_VAULT_PATH` is the **vault root** (not a subfolder) and `FLEETING_FOLDER` exists inside it |
| No emails found | Verify `EMAIL_PROVIDER`, credentials, and `VOICE_NOTE_KEYWORD` match your mailbox |
| Attachment not transcribed | Ensure the attachment has a recognised audio extension |

## Publishing to ClawHub

```bash
clawhub publish ~/.openclaw/skills/voice-note-transcriber \
  --slug voice-note-transcriber \
  --name "Voice Note Transcriber" \
  --version 1.0.0 \
  --changelog "Initial release"
```
