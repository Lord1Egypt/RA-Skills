---
name: workday-music-greeter
description: On weekdays, automatically switch the home-music scene for the current time slot, fetch a matching GIF, and send a greeting email that embeds and attaches that GIF. Includes a cron installer for Mon–Fri scheduling. Use when the user wants automated workday music scene switching paired with themed greeting emails.
version: 1.0.0
author: "OpenClaw workspace"
tags: ["automation", "music", "email", "gif", "cron", "workday"]
triggers:
  - workday music
  - auto music scene
  - greeting email gif
  - weekday automation
metadata:
  openclaw:
    requires:
      bins: ["bash", "node"]
    emoji: "🎶"
---

# workday-music-greeter

Orchestrates three existing skills into one weekday routine:

1. **home-music** — switches the whole-house music scene for the current slot.
2. **gifgrep** — pulls a GIF that matches the scene mood.
3. **imap-smtp-email** — sends a greeting email with the GIF embedded *and* attached.

A cron installer schedules it Monday–Friday at each scene's start hour.

## Files

```
workday-music-greeter/
├── SKILL.md          # this file
├── run.sh            # main orchestrator (supports --dry-run and `auto`)
├── scenes.conf       # scene | hour-start | gif-query | email-subject
├── install-cron.sh   # registers Mon–Fri crontab entries
└── .env.example      # required/optional env vars
```

## Quick start

```bash
cp .env.example .env && $EDITOR .env      # set WMG_MAIL_TO + SMTP_* creds
WMG_MAIL_TO=you@example.com ./run.sh morning --dry-run   # preview, touches nothing
WMG_MAIL_TO=you@example.com ./run.sh auto                # pick scene by current time
./install-cron.sh                          # schedule Mon–Fri
```

## How it works

- `run.sh <scene>` runs one scene. `run.sh auto` selects the scene whose
  `hour-start` is the latest one at/"before now (see `scenes.conf`).
- Weekend guard: if `date +%u >= 6` (Sat/Sun) it exits without acting.
- The GIF is injected into the email HTML via `<img src>` (the gifgrep URL) and,
  when a local download exists, attached via `--attach`.
- `--dry-run` prints every external call instead of executing it — use it to
  verify wiring before going live.

## Customizing scenes

Edit `scenes.conf` (pipe-delimited):

```
morning|8|good morning coffee sunrise|🌅 Good morning — easing into the day
chill|12|relax lofi midday break|🍵 Midday reset — chill vibes on
focus|14|focus work productivity calm|🎯 Afternoon focus block
off|18|goodbye work done relax weekend|🔇 Wrapping up — music off
```

Scene names must match `home-music` scenes (`morning`, `chill`, `party`, `off`, …).
Re-run `install-cron.sh` after changing hours; it replaces its own tagged block idempotently.

## Dependencies & honest limitations

| Dependency | Needed for | Notes |
|------------|-----------|-------|
| `home-music` | live scene switch | **macOS-only** (AppleScript + Spotify + Airfoil). On non-macOS the scene switch is skipped with a warning; the rest still runs. |
| `gifgrep` | matching GIF | If absent, the email is sent without a GIF. |
| `imap-smtp-email` | sending mail | Requires SMTP creds in env/`.env`. Without them, sending fails (reported, not silently swallowed). |
| `crontab` | scheduling | `install-cron.sh` uses the system user crontab. |

If a dependency or credential is missing, `run.sh` warns and degrades rather
than faking success. Always validate with `--dry-run` first.

## Environment

See `.env.example`. Required: `WMG_MAIL_TO`. SMTP_* are consumed by the
`imap-smtp-email` sender. Optional overrides: `WMG_GIF_DIR`, `WMG_SMTP_SCRIPT`.
