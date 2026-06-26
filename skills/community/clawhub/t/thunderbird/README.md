# Thunderbird Skill for OpenClaw

Search and inspect local Mozilla Thunderbird mail storage directly from disk (mbox and Maildir), with filters for account, folder, sender, recipient, subject, body, unread state, time ranges, and attachments.

## ClawHub

- https://clawhub.ai/KomelT/clawhub-thunderbird-skill

## Features

- Detect Thunderbird profiles on Windows and Linux profile roots
- List accounts from `prefs.js`
- Search local mail in `Mail/` and `ImapMail/`
- Filter by sender, recipient, subject, folder, free-text query, unread status
- Filter by day or time range (`--today`, `--yesterday`, `--since`, `--until`)
- Filter and export attachments (`--has-attachment`, `--attachment-name`, `--save-attachments`)
- Output as table-like text or JSON

## Quick start

Run from the skill directory:

```powershell
python scripts/search_thunderbird.py --list-profiles
python scripts/search_thunderbird.py --profile default-release --list-accounts
python scripts/search_thunderbird.py --profile default-release --account user@example.com --folder inbox --query invoice --limit 20
```

Search by attachment name and save files:

```powershell
python scripts/search_thunderbird.py --profile default-release --attachment-name invoice --save-attachments .\out --limit 10
```

## Date filter behavior

- `--since YYYY-MM-DD` starts at `00:00:00` UTC of that date
- `--until YYYY-MM-DD` ends at `23:59:59.999999` UTC of that date
- ISO-8601 timestamps are used exactly as provided

## Project files

- `SKILL.md`: skill usage instructions
- `scripts/search_thunderbird.py`: local Thunderbird search CLI
- `references/storage-layout.md`: Thunderbird storage reference
- `LICENSE`: MIT license
