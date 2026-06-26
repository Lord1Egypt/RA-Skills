# unbridled

> Unified multi-platform messaging for AI agents — Messenger, WhatsApp, Instagram, LinkedIn, Twitter/X, Signal, Telegram, Discord — powered by Beeper's Matrix bridges, end-to-end encrypted, all from one Python client.

![status: v0.2](https://img.shields.io/badge/status-v0.2-blue)
![license: MIT](https://img.shields.io/badge/license-MIT-green)
![runtime: python 3.10+](https://img.shields.io/badge/python-3.10+-blue)

---

## What this is

`unbridled` turns a personal **Beeper account** into a programmable API for your agents. Bridge Messenger, WhatsApp, LinkedIn, and the rest inside Beeper, then talk to them all through Matrix — from Python, the CLI, or a skill manifest.

It handles the unglamorous parts:

- Olm / Megolm end-to-end encryption (via `matrix-nio`)
- Bootstrapping cross-signing from the user's Beeper recovery key, so bridges actually trust your device
- Importing the full Matrix **key backup** (`m.megolm_backup.v1.curve25519-aes-sha2`) so incoming history decrypts out of the box
- Beeper's lazy sync quirk (injecting rooms manually for `room_send`; iterating `joined_rooms()` instead of the half-empty `client.rooms`)
- A long-running systemd daemon that accumulates fresh inbound group sessions so future messages decrypt without effort

It's the thing I wanted to exist when I said to Clawd "send this on Messenger for me".

## Why "unbridled"

Beeper calls its per-network connectors **bridges**. This library lets your agent run **unbridled** across all of them from one place. Also: once cross-signing is in place, there's nothing blocking an agent from reaching any of your chat networks. Hence the name — liberating, and slightly ominous. Use responsibly.

## Supported networks

Everything Beeper bridges. Tested on:

- Facebook Messenger ✅
- WhatsApp ✅
- LinkedIn ✅
- Instagram DM (listed, untested for send)
- Twitter/X DM (listed, untested for send)
- Signal, Telegram, Discord, iMessage, Google Messages: should work the same way — list-chats + send — feedback welcome.

## Architecture

```
┌───────────────────────────────┐
│ External networks             │
│  FB / WA / IG / LI / X / …    │
└──────────────▲────────────────┘
               │  appservice
┌──────────────┴────────────────┐
│ Beeper cloud bridges          │
│  facebookgo, whatsapp,        │
│  instagramgo, linkedin, …     │
└──────────────▲────────────────┘
               │
┌──────────────┴────────────────┐
│ hungryserv.beeper.com         │
│  per-user Matrix homeserver   │
│  enforces E2EE on outgoing    │
└──────────────▲────────────────┘
               │  Matrix CS API (HTTPS)
      ┌────────┴────────────┐
      │ unbridled (you)     │
      │  ┌──────────────┐   │
      │  │ nio_client   │   │  async E2EE send/read
      │  │ client       │   │  sync HTTP list-chats + bridge state
      │  │ bootstrap_   │   │  one-shot cross-signing from recovery key
      │  │   crosssign  │   │
      │  │ import_key_ │   │  one-shot: recovery key → download + decrypt
      │  │   backup     │   │  the server-side Megolm backup into the store
      │  │ sync_daemon  │   │  long-running sync → accumulates new Megolm sessions
      │  │ collect_     │   │  daily digest of active chats per network
      │  │   daily      │   │
      │  └──────────────┘   │
      │                     │
      │  Olm store          │  ~/.local/share/clawd-matrix/  (chmod 700)
      │  Secrets            │  ~/.secrets/beeper-recovery-key.txt
      │  bbctl config       │  ~/.config/bbctl/config.json
      └─────────────────────┘
```

## Quick start

### Prerequisites

- A **Beeper account** (beeper.com) with your networks bridged from Beeper Desktop.
- Your **Beeper Recovery Key** (Beeper Desktop → Settings → your name → ⌄ → Show Recovery Code).
- Linux or macOS with `python3.10+`, `uv` (or pip), and `libolm-dev`.

### Install

```bash
git clone https://github.com/jkobject/unbridled.git
cd unbridled
bash install.sh
```

What `install.sh` does:
1. Downloads `bbctl` into `~/bin/`
2. Ensures `libolm-dev` and `ffmpeg` are installed (via apt on Ubuntu/Debian)
3. Creates a dedicated venv at `~/.venvs/beeper` and installs `matrix-nio[e2e]` + crypto deps
4. Prints the next manual steps

Then:

```bash
# 1. Log in to Beeper
bbctl login
bbctl whoami  # sanity check: all bridges RUNNING

# 2. Save your recovery key (never commit this!)
mkdir -p ~/.secrets && chmod 700 ~/.secrets
echo 'YOUR RECOVERY KEY HERE' > ~/.secrets/beeper-recovery-key.txt
chmod 600 ~/.secrets/beeper-recovery-key.txt

# 3. Initialize the Olm store and cross-sign this device
~/.venvs/beeper/bin/python scripts/nio_client.py whoami          # creates store
~/.venvs/beeper/bin/python scripts/bootstrap_crosssign.py        # cross-signs
#     Expected last line: 🎉 SUCCESS — device is now cross-signed.

# 4. Import the Matrix key backup (required for reading history)
#     Stop the daemon first if you already started it — it locks the sqlite store.
systemctl --user stop clawd-beeper-sync 2>/dev/null || true
~/.venvs/beeper/bin/python scripts/import_key_backup.py
#     Expected: "✓ Imported N sessions into ~/.local/share/clawd-matrix/"

# 5. (Recommended) Install the long-running sync daemon for incoming decryption
bash systemd/install.sh
systemctl --user status clawd-beeper-sync

# 6. Smoke test — pick a chat you don't mind messaging
~/.venvs/beeper/bin/python scripts/nio_client.py list-chats --network messenger --limit 10
~/.venvs/beeper/bin/python scripts/nio_client.py send --room '!xxx:beeper.local' --text "hi from unbridled"
```

## Day-to-day usage

```bash
NIO=~/.venvs/beeper/bin/python
SCRIPT=./scripts/nio_client.py

$NIO $SCRIPT whoami
$NIO $SCRIPT list-chats --network messenger --limit 25
$NIO $SCRIPT list-chats --network whatsapp --limit 50
$NIO $SCRIPT send --room '!xxx:beeper.local' --text "…"
$NIO $SCRIPT history --room '!xxx:beeper.local' --limit 20

# Per-network daily digest
python3 ./scripts/collect_beeper_daily.py \
    --hours 24 \
    --networks messenger,whatsapp,linkedin \
    --output ./digest.md
```

Friendly network aliases: `messenger / facebook / fb`, `whatsapp / wa`, `instagram / ig`, `linkedin`, `twitter / x`, `signal`, `telegram`, `discord`.

## Python usage

```python
import asyncio, sys
sys.path.insert(0, "./scripts")
from nio_client import make_client

async def ping():
    client = await make_client()
    try:
        joined = await client.joined_rooms()
        print(f"{len(joined.rooms)} rooms")
    finally:
        await client.close()

asyncio.run(ping())
```

## Inbound decryption: backup import + sync daemon

Beeper enforces E2EE. Two complementary mechanisms feed Megolm group sessions into your local store:

### 1. One-shot: import the Matrix key backup

Beeper keeps a server-side, encrypted-at-rest backup of every Megolm session the user has ever held (algorithm `m.megolm_backup.v1.curve25519-aes-sha2`). `scripts/import_key_backup.py` downloads those, decrypts them with the recovery key (the same one you used for cross-signing), and writes each `InboundGroupSession` into the nio sqlite store.

```bash
systemctl --user stop clawd-beeper-sync 2>/dev/null || true
~/.venvs/beeper/bin/python scripts/import_key_backup.py
systemctl --user start clawd-beeper-sync
```

Run it once per device (after each new `bbctl login`). Typical coverage on an active account: **95%+** of joined rooms reachable for historical reads. The remaining gap is inactive rooms that simply have no session in the backup.

### 2. Continuous: the sync daemon

Future messages frequently reuse an already-known group session, so they decrypt fine on demand. But Megolm sessions rotate (new members, new rooms, bridge restarts), and the *new* session key is delivered via a single `to_device` event. Beeper only retains undelivered `to_device` events for a few days — so if nothing syncs during that window, those keys are lost.

`scripts/sync_daemon.py` wraps `matrix-nio`'s `sync_forever` in a supervised loop with exponential backoff and consumes these `to_device` events as they arrive. Running it under systemd keeps the store always up-to-date.

```bash
systemctl --user enable --now clawd-beeper-sync.service
journalctl --user -u clawd-beeper-sync -f
```

Resource footprint: ~37 MB RAM idle, negligible CPU.

**Do I strictly need the daemon 24/7?** If you only ever sync interactively and never go more than a few days without running *some* client, you'll usually be fine — but for unattended agents, cron jobs, or daily digests, run the daemon.

## Security model

| Asset | Where it lives | Treat as |
|---|---|---|
| Beeper password | User's head / password manager | Master secret |
| Beeper Recovery Key | `~/.secrets/beeper-recovery-key.txt` (600) | Master secret (decrypts cross-signing keys) |
| `bbctl` access token | `~/.config/bbctl/config.json` (600) | Device-scoped credential |
| Olm/Megolm store | `~/.local/share/clawd-matrix/` (700) | Device-scoped credential |

If the recovery key ever leaks, **regenerate it from Beeper Desktop** (Settings → name → ⌄ → Reset Recovery Code) and re-run `bootstrap_crosssign.py` on each agent device.

Never commit any of the above to git. `.gitignore` takes care of the common cases.

## Agent safety rules (the human part)

When an LLM agent has this package wired up:

- **Never auto-reply** on a new thread without explicit user confirmation.
- **Never mass-send** by looping over a contact list.
- **In group chats**, stay out unless directly addressed.
- **Log every send** somewhere the user can audit.
- **Respect quiet hours** implicit in the user's daily rhythm.

You're driving someone else's Messenger. Act like a guest in their house, not a bot.

## Known quirks / honest limitations

- **Lazy sync**: `client.rooms` from nio only includes recently-active rooms even on `full_state=True`. The wrappers use `joined_rooms()` + manual `MatrixRoom` injection as a workaround. Documented in `references/architecture.md`.
- **Schema warnings flood** on sync (`'events' is a required property`): hungryserv returns fields nio's validator doesn't recognize. Silenced by default.
- **"Notes to self" chats** (e.g. "Facebook Messenger (Your Name)") don't have a real external recipient; bridges return `m.event_not_handled` on send. Not a bug.
- **First message to a fresh room** may take 1-2 extra seconds as Megolm group sessions negotiate.
- **Do not set the decrypt window from the raw recent-event count.** If a room has only 1 recent raw Matrix event, that event may be a reaction or bridge/meta event, not the text message you actually want. Digest/collector code should over-fetch a small history window (`history --limit >= 10`) to avoid false `decryption unavailable` reports.
- **History decryption for messages predating the key backup import or daemon startup**: the backup covers sessions Beeper Desktop archived; inactive rooms without any backed-up session remain unreadable until the next `to_device` event for that room lands while the daemon is active.
- **Relies on Beeper's cloud bridges.** If Beeper changes their policy or goes down, self-hosted bridges (`bbctl run sh-<bridge>`) are a fallback — your recovery/token survives the migration.

## Files

```
unbridled/
├── SKILL.md                         OpenClaw skill manifest
├── README.md                        this file
├── LICENSE                          MIT
├── install.sh                       one-shot prerequisites installer
├── scripts/
│   ├── nio_client.py                async E2EE client (send/list/history)
│   ├── client.py                    sync HTTP wrapper (no e2ee, list + bridge state)
│   ├── bootstrap_crosssign.py       recovery key → device signature
│   ├── import_key_backup.py         recovery key → download + decrypt Matrix key backup
│   ├── verify_interactive.py        SAS verification fallback
│   ├── sync_daemon.py               long-running sync (Megolm accumulation)
│   └── collect_beeper_daily.py      daily digest generator
├── systemd/
│   ├── clawd-beeper-sync.service    user-level systemd unit
│   └── install.sh                   installs the unit to ~/.config/systemd/user
└── references/
    ├── setup-checklist.md           step-by-step for humans
    └── architecture.md              diagrams and crypto flow
```

## Changelog

- **v0.2.0** — 2026-04-18 — Added `import_key_backup.py` so incoming history actually decrypts (357/357 sessions imported on a real Beeper account, 95% room coverage). Fixed `list-chats --network X` that was returning 0 because of Beeper's lazy sync — now iterates `joined_rooms()` directly. Documented the two known libolm gotchas: HKDF salt is a single `0x00` byte (not 32), and the MAC is computed on empty input (not on the ciphertext).
- **v0.1.0** — 2026-04-18 — Initial release. Send across Messenger / WhatsApp / IG / LinkedIn / Twitter worked on cross-signed device; history decryption was partial.

## Roadmap

- [ ] `unread` helper (summarize unread chats)
- [ ] `reply --to <event_id>` with proper threading
- [ ] `mark-read` on inbound messages
- [ ] Media attachments (image send)
- [ ] Telegram / Signal / Discord end-to-end testing
- [ ] ClawHub skill release (`openclaw-skills/unbridled`)
- [ ] Optional TypeScript port

## Contributing

PRs welcome. The code is intentionally small and unopinionated — a handful of single-purpose Python scripts, no framework. If you add a feature, try to keep it that way.

## License

MIT © 2026 Jérémie Kalfon, with heavy lifting by Clawd, a personal AI assistant that happens to write decent Python.

## Credits

- [matrix-nio](https://github.com/poljar/matrix-nio) — the only Python Matrix client that gets E2EE right
- [beeper/bridge-manager](https://github.com/beeper/bridge-manager) — the CLI that makes this possible
- [mautrix bridges](https://github.com/mautrix) — the actual network connectors
- The Matrix spec community
