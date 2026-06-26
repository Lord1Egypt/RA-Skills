---
name: thunderbird
description: Read and search local Mozilla Thunderbird mail storage on disk. Use when working with Thunderbird profiles, extracting emails from local folders or IMAP cache, locating messages by sender/recipient/subject/body, checking which account a mailbox belongs to, or answering inbox questions for a specific Thunderbird account such as "do I have unread mail today?" or "search mail for user@example.com".
---

# Thunderbird

Use Thunderbird's local profile data as the source of truth for offline mail inspection. Prefer read-only access and search the raw local storage directly rather than relying on UI automation.

Run the bundled script from the skill directory, or use an absolute path resolved from the skill root:

- `python scripts/search_thunderbird.py ...`

If the current working directory is not the skill directory, resolve `scripts/search_thunderbird.py` relative to this `SKILL.md` location before running it.

## Quick start

1. Detect available profiles:
   - `python scripts/search_thunderbird.py --list-profiles`
2. List accounts in one profile:
   - `python scripts/search_thunderbird.py --profile default-release --list-accounts`
3. Search one mailbox account directly:
   - `python scripts/search_thunderbird.py --profile default-release --account user@example.com --folder inbox --query invoice --limit 10`
4. Narrow content search when needed:
   - `--subject-only` to search only the subject line
   - `--body-only` to search only the body/preview text
   - `--exclude <text>` to remove noisy matches
5. Return only unread inbox messages when needed:
   - `python scripts/search_thunderbird.py --profile default-release --account user@example.com --folder inbox --unread-only --limit 20`
6. Extract, filter, or sort more when needed:
   - `--show-body`
   - `--unread-only`
   - `--subject-only`
   - `--body-only`
   - `--exclude wordpress`
   - `--has-attachment`
   - `--attachment-name invoice`
   - `--list-attachments`
   - `--save-attachments ./out`
   - `--today`
   - `--yesterday`
   - `--since 2026-03-11`
   - `--until 2026-03-12T08:00:00+01:00`
   - `--sort-by date|from|subject|to`
   - `--sort-order asc|desc`
   - `--json`

## Workflow

### 1. Pick the profile

Use `--list-profiles` first if the profile is unknown. The script now checks common Thunderbird profile roots on Windows and Linux automatically. Accept either:

- absolute profile path
- exact profile directory name
- unique profile-name fragment

If multiple profiles match, stop and choose explicitly.

### 2. Pick the account when possible

For account-specific requests, do not scan every mailbox first.

Use:

- `--list-accounts` to inspect the profile
- `--account <email-or-fragment>` to restrict work to one Thunderbird account
- `--folder inbox|sent|archive|drafts|junk|trash|spam` to narrow further

This is usually both faster and easier than scanning the whole profile.

### 3. Search local storage

Use `scripts/search_thunderbird.py` for most tasks. It scans common Thunderbird storage roots:

- `Mail/`
- `ImapMail/`

It supports:

- mbox folders such as `Inbox`, `Sent`, `Archives`
- Maildir folders containing `cur/` and `new/`
- common profile discovery on Windows and Linux (`%APPDATA%/Thunderbird/Profiles`, `~/.thunderbird`, `~/.mozilla/thunderbird`)

### 4. Return useful results

By default, summarize:

- source mailbox path
- date
- from
- to
- subject
- body preview

Prefer focused summaries for the user. Use `--show-body` only when the full message text is necessary.

## Common tasks

### List profiles

```powershell
python scripts/search_thunderbird.py --list-profiles
```

### List accounts inside a profile

```powershell
python scripts/search_thunderbird.py --profile default-release --list-accounts
```

### Search one account inbox by keyword

```powershell
python scripts/search_thunderbird.py --profile default-release --account user@example.com --folder inbox --query contract --limit 20
```

### Find messages from a sender inside one account

```powershell
python scripts/search_thunderbird.py --profile default-release --account user@example.com --from billing@example.com --limit 20
```

### Find messages by subject fragment and return JSON

```powershell
python scripts/search_thunderbird.py --profile default-release --account user@example.com --subject invoice --json --limit 20
```

### Return only unread inbox messages

```powershell
python scripts/search_thunderbird.py --profile default-release --account user@example.com --folder inbox --unread-only --limit 20
```

### Search only in subject or only in body

```powershell
python scripts/search_thunderbird.py --profile default-release --account user@example.com --folder inbox --query invoice --subject-only --limit 20
python scripts/search_thunderbird.py --profile default-release --account user@example.com --folder inbox --query password --body-only --limit 20
```

### Exclude noisy matches

```powershell
python scripts/search_thunderbird.py --profile default-release --account user@example.com --folder inbox --query update --exclude wordpress --limit 20
```

### Find messages with attachments or save them

```powershell
python scripts/search_thunderbird.py --profile default-release --account user@example.com --folder inbox --has-attachment --list-attachments --limit 20
python scripts/search_thunderbird.py --profile default-release --account user@example.com --attachment-name invoice --save-attachments .\out --limit 20
```

### Sort messages by sender or subject

```powershell
python scripts/search_thunderbird.py --profile default-release --account user@example.com --folder inbox --sort-by from --sort-order asc --limit 20
```

### Filter messages by time range

```powershell
python scripts/search_thunderbird.py --profile default-release --account user@example.com --folder inbox --since 2026-01-01 --until 2026-01-02T08:00:00+01:00 --sort-by date --sort-order desc --limit 20
```

### Use day shortcuts

```powershell
python scripts/search_thunderbird.py --profile default-release --account user@example.com --folder inbox --yesterday --sort-by date --sort-order desc --limit 20
```

### Extract full body text for a narrow match

```powershell
python scripts/search_thunderbird.py --profile default-release --account user@example.com --query "reset password" --show-body --limit 5
```

## Interpretation rules

- Treat `.msf` files as indexes, not message sources.
- Prefer the raw mbox file when a mailbox file and `.msf` both exist.
- Remember that IMAP results reflect cached local messages, not necessarily the full server mailbox.
- If a message is not found, mention that local Thunderbird storage may not contain it or may not have synced it.
- When the user names an email address, prefer `--account` before broader searches.
- `--unread-only` depends on Thunderbird folder indexes (`.msf`) for mbox folders; if unread state is unavailable, say so instead of guessing.
- `--since` and `--until` accept `YYYY-MM-DD` or ISO-8601 timestamps. Bare `--since` dates are interpreted as UTC midnight, while bare `--until` dates are interpreted as UTC end-of-day.
- `--today` and `--yesterday` are UTC-based shortcuts and cannot be combined with `--since` or `--until`.
- `--subject-only` and `--body-only` only change how `--query` is matched; do not combine them with each other.
- `--has-attachment` filters to messages with attachments; `--attachment-name` filters by attachment filename.
- `--save-attachments <dir>` writes matching attachments to disk and implicitly enables attachment-aware filtering when needed.

## Attachment interaction policy

When the user asks for an attachment, do not save or open it immediately unless they already said what they want done.

Default follow-up:

- `Should I save it or open it?`

If the user says **save**:

- ask where to save it if they did not already specify a location
- then use `--save-attachments <dir>`
- return the final saved path(s)

If the user says **open**:

- first extract the attachment to a temporary or user-requested location
- then open it with the system default app from the CLI
- prefer the platform default opener instead of inventing app-specific commands
- mention the file path you opened

If the attachment is text-like and the user likely wants contents rather than launching an external app, it is also acceptable to read or summarize it directly after asking.

## Reference

Read `references/storage-layout.md` when you need a quick map of Thunderbird's on-disk structure.
