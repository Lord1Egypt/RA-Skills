---
name: wacrawl
description: Read-only local archive and full-text search of macOS WhatsApp Desktop chats. Snapshots WhatsApp's SQLite databases into ~/.wacrawl/wacrawl.db without modifying the app container.
homepage: https://github.com/steipete/wacrawl
metadata: {"clawdbot":{"emoji":"📱","os":["darwin"],"requires":{"bins":["wacrawl"]},"install":[{"id":"brew","kind":"brew","tap":"steipete/tap","formula":"wacrawl","bins":["wacrawl"],"label":"Install wacrawl (brew)"}]}}
---

# Wacrawl

Local read-only mirror of WhatsApp Desktop on macOS. Copies WhatsApp's SQLite databases into a temp snapshot, imports useful chat data into its own archive, and exposes scriptable search.

**Does not** send messages, decrypt cloud backups, talk to WhatsApp Web, or write back into WhatsApp's app container.

## Requirements
- macOS with **WhatsApp Desktop** (Mac App Store version) installed and signed in.
- Full-disk access for the terminal that runs `wacrawl` (System Settings → Privacy & Security → Full Disk Access). WhatsApp's group container is sandboxed and otherwise unreadable.
- `wacrawl` binary on PATH.

## Setup
```bash
wacrawl doctor    # verify WhatsApp data path + read access
wacrawl import    # copy + import chats into ~/.wacrawl/wacrawl.db
wacrawl status    # show row counts + last import time
```

## State
- Source (read-only): `~/Library/Group Containers/group.net.whatsapp.WhatsApp.shared`
- Database: `~/.wacrawl/wacrawl.db`

## Common Commands
```bash
wacrawl chats list --json
wacrawl messages list --chat <id> --limit 100 --json
wacrawl search "keyword" --json
wacrawl sql 'SELECT count(*) FROM messages'
```

## Integration Notes
- Snapshot model: each `wacrawl import` re-snapshots WhatsApp's SQLite into a temp dir before reading, so live use of the WhatsApp app never blocks the import.
- No auth flow — relies entirely on the local logged-in WhatsApp Desktop session.
- Run `wacrawl import` on a PaperFang schedule (e.g. hourly) to keep the archive fresh.
