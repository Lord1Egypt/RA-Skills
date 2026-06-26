---
name: telegram-readonly
description: Read the user's personal Telegram account in a controlled, read-only way via Telethon/MTProto. Use when you need to inspect Telegram chats, list dialogs, read recent messages from a specific chat, or search Telegram messages without relying on the Telegram Bot API. Do not use for sending, replying, editing, deleting, or any write action.
---

# Telegram Readonly

Use the installed `telegram-readonly` CLI for Telegram reads from the user's personal account.

This skill exists because Telegram Bot API is the wrong tool for reading a real personal account. Use MTProto via Telethon instead.

## Quick rules

- Use this skill only for reads.
- Do not improvise write actions.
- Do not add send/edit/delete logic to the wrapper unless the user explicitly asks.
- Treat the Telethon session like a high-privilege secret.
- Assume unread preservation is best-effort until tested on a real chat.

## Installation preference

Prefer an installed CLI over hardcoded script paths.

Preferred install:

```bash
pipx install git+https://github.com/ropl-btc/telegram-readonly-cli.git
```

Fallback inside a repo checkout:

```bash
pip install .
```

After install, use:

`telegram-readonly`

## Commands

### Show built-in help

```bash
telegram-readonly help
```

### Authenticate once

```bash
export TELEGRAM_API_ID='12345678'
export TELEGRAM_API_HASH='your_api_hash'
telegram-readonly auth
```

### List chats

`dialogs --query` does token-based matching across `name`, `username`, and `title`, so queries like `petros skynet` work even when the exact full string is not present as one substring.

```bash
telegram-readonly dialogs --limit 50
```

### Read recent messages

```bash
telegram-readonly messages --chat '@username' --limit 50 --reverse
```

### Search messages

```bash
telegram-readonly search 'invoice' --limit 50
```

Restrict search to one chat:

```bash
telegram-readonly search 'deadline' --chat '@username' --limit 50
```

### List recent unread chats

Default behavior is opinionated: exclude **muted** and **archived** chats.

```bash
telegram-readonly unread-dialogs --limit 10
```

Include muted and/or archived when needed:

```bash
telegram-readonly unread-dialogs --limit 10 --include-muted --include-archived
```

### List recent unread DMs only

```bash
telegram-readonly unread-dms --limit 10
```

## Workflow

1. Read `references/setup-and-safety.md` if setup, auth, or unread-state behavior matters.
2. Ensure the `telegram-readonly` CLI is installed.
3. Ensure Telegram API credentials exist.
4. Run `auth` once to create the session.
5. Use `dialogs`, `messages`, `search`, `unread-dialogs`, or `unread-dms` as needed.
6. Keep usage narrow and intentional.

## Expected outputs

The wrapper returns JSON. Parse it instead of relying on fragile text scraping.

Dialog objects include:
- `is_user`
- `is_group`
- `is_channel`
- `is_bot`
- `archived`
- `muted`
- unread counters

## Files

- Package repo: `https://github.com/ropl-btc/telegram-readonly-cli`
- Compatibility wrapper: `scripts/telegram_readonly.py`
- Setup notes: `references/setup-and-safety.md`
- Config storage: `~/.config/telegram-readonly/config.json`

## When to stop and ask

Stop and ask before:
- adding write capabilities
- enabling any background watcher/daemon
- broad exporting of large chat histories
- changing how secrets/session storage works
