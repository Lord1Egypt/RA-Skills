# Telegram Readonly — Setup and safety

## What this skill is for

Use this skill to read Telegram chats from the user's personal account via Telethon/MTProto in a controlled, read-only way.

This is not a Telegram bot skill.
It is for local access to a real user account.

## Safety model

The wrapper intentionally exposes only:
- `auth`
- `dialogs`
- `messages`
- `search`
- `unread-dialogs`
- `unread-dms`
- `help`

It does not expose:
- send
- edit
- delete
- mark-read calls
- background auto-reply logic

Important: the underlying Telethon session still has high privilege because it is a real Telegram login. The safety comes from the wrapper surface area, not from Telegram granting reduced permissions.

## Files and locations

- Package repo: `https://github.com/ropl-btc/telegram-readonly-cli`
- Package entrypoint: `telegram-readonly`
- Local config: `~/.config/telegram-readonly/config.json`

## Prerequisites

1. Telegram API credentials from `https://my.telegram.org`
2. Telethon installed through the package
3. One interactive login to create a session string

## Install

Preferred:

```bash
pipx install git+https://github.com/ropl-btc/telegram-readonly-cli.git
```

Fallback:

```bash
git clone https://github.com/ropl-btc/telegram-readonly-cli.git
cd telegram-readonly-cli
python3 -m venv .venv
. .venv/bin/activate
pip install .
```

## Telegram API credentials

At `https://my.telegram.org`:
1. Log in with the Telegram account phone number.
2. Open API development tools.
3. Create an application.
4. Save `api_id` and `api_hash`.

## First auth flow

Use env vars.

```bash
export TELEGRAM_API_ID='12345678'
export TELEGRAM_API_HASH='your_api_hash'
telegram-readonly auth
```

The CLI will prompt for:
- phone number
- login code
- 2FA password if enabled

It saves the resulting session string to `~/.config/telegram-readonly/config.json`.
Protect that file like a password.

## Read-only usage

Show built-in help:

```bash
telegram-readonly help
```

List chats:

`dialogs --query` uses token-based matching across `name`, `username`, and `title`.

```bash
telegram-readonly dialogs --limit 50
```

Read one chat:

```bash
telegram-readonly messages --chat '@username' --limit 50 --reverse
```

Search globally:

```bash
telegram-readonly search 'invoice' --limit 50
```

Search in one chat:

```bash
telegram-readonly search 'deadline' --chat '@username' --limit 50
```

List recent unread chats, excluding muted + archived by default:

```bash
telegram-readonly unread-dialogs --limit 10
```

List recent unread DMs only, excluding muted + archived by default:

```bash
telegram-readonly unread-dms --limit 10
```

Include muted and archived when needed:

```bash
telegram-readonly unread-dialogs --limit 10 --include-muted --include-archived
```

## Unread behavior

Goal: avoid changing unread state.

This wrapper never calls explicit read acknowledgements.
That should usually avoid marking messages as read, but this must be verified with a live test because Telegram state can be subtle.

Before broad use:
1. pick a sacrificial chat
2. confirm unread badge/state before read
3. fetch messages with the wrapper
4. verify whether unread state changed in official Telegram clients

If unread state changes unexpectedly, stop and adjust workflow before wider rollout.

## Operational guidance

- Prefer narrow reads over broad scraping.
- Start with specific chats or direct need.
- Do not add write actions to this wrapper unless the user explicitly asks.
- If later automation is needed, create a separate write-capable tool instead of weakening this one.
