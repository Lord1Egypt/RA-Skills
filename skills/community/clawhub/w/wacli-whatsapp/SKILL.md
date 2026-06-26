---
name: wacli-whatsapp
description: Send WhatsApp messages or files from the command line using wacli (WhatsApp Web via whatsmeow). Use when the user asks to message someone on WhatsApp (send text, reply/quote, send a file/media with caption, react), or to auth/sync/search WhatsApp history via wacli.
---

# wacli (WhatsApp CLI)

Use `wacli` via `exec`.

## Safety / permission

- Treat sending as an **external, privacy-sensitive action**.
- Only send when the user explicitly provided (a) recipient and (b) message/file content **and** asked to send.
- If any detail is missing/ambiguous (wrong number, unclear chat, not sure which attachment), ask one clarifying question before sending.

## Quick checks

- Verify install:
  - `wacli version`
- If missing, suggest:
  - `brew install steipete/tap/wacli`

## Auth + sync (required before sending)

- Login (shows QR) and bootstrap initial sync:
  - `wacli auth`
- Keep syncing in the background (recommended so messages/IDs resolve):
  - `wacli sync --follow`
- Diagnostics:
  - `wacli doctor`

## Send a WhatsApp message

Text:

- `wacli send text --to <PHONE_OR_JID> --message "<TEXT>"`

Quoted reply (needs message id, usually from `messages list/search/show/context`):

- `wacli send text --to <PHONE_OR_JID> --message "<TEXT>" --reply-to <MSG_ID>`

React:

- `wacli send react --to <PHONE_OR_JID> --id <MSG_ID> [--reaction "<EMOJI>"]`

## Send a file

- `wacli send file --to <PHONE_OR_JID> --file <PATH> [--caption "<TEXT>"] [--filename <DISPLAY_NAME>] [--mime <MIME>]`

## Finding chats / message ids

- Search messages:
  - `wacli messages search "<QUERY>"`
- List recent messages (for a known chat JID):
  - `wacli messages list --chat <JID> --asc --limit 50`
- Show context around a message:
  - `wacli messages context --chat <JID> --id <MSG_ID>`
- Find chats/groups:
  - `wacli chats list --query "<NAME>" --limit 50`
  - `wacli groups list --query "<NAME>" --limit 50`

## Store location (FYI)

- Default store is `~/.wacli` on macOS; override with `--store DIR` or `WACLI_STORE_DIR`.
