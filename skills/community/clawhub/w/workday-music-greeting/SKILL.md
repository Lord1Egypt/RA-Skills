---
name: workday-music-greeting
description: Auto-switch music scenes by workday time slot and send matching greeting emails with scene-specific GIFs. Combines home-music scene control with IMAP/SMTP email for a complete morning-to-evening automation.
version: 1.0.0
author: "OpenClaw Workspace"
tags: ["music", "email", "automation", "greeting", "workday", "schedule"]
triggers:
  - workday music
  - morning greeting
  - music greeting email
  - daily music scene
  - workday automation
metadata:
  openclaw:
    requires:
      bins: ["node", "npm"]
      skills: ["home-music", "imap-smtp-email"]
    emoji: "🎶"
---

# 🎶 Workday Music Greeting

Auto-switch music scenes by workday time slot, and send a greeting email with a matching GIF — all in one command or cron job.

```
    🌅 ──► ☕ ──► 💻 ──► 😌 ──► 🌙
   morning  focus  working  chill   off
```

## What It Does

| Time Slot | Music Scene | Greeting Theme | Example GIF |
|-----------|-------------|----------------|-------------|
| 🌅 Morning (6–9) | `morning` | Rise & shine | ☀️ sunrise GIF |
| ☕ Focus (9–12) | `focus` | Deep work time | 🔥 laser-focus GIF |
| 💻 Working (12–14) | `working` | Keep going! | 💪 hustle GIF |
| 😌 Chill (14–18) | `chill` | Wind down | 🍵 tea-time GIF |
| 🌙 Off (18+) | `off` | Good night | 🌙 moon GIF |

## Quick Start

```bash
# Run the current time-slot scene + send greeting email
node scripts/workday-greeting.js
```

That's it. The script:
1. Detects the current time slot
2. Switches to the matching music scene (via `home-music`)
3. Sends a greeting email with an embedded GIF matching the scene

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and fill in:

```bash
# Email (SMTP) — required for sending greetings
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=you@gmail.com
SMTP_PASS=your_app_password
GREETING_TO=recipient@example.com
GREETING_FROM=you@gmail.com

# Music scene command (default: home-music)
MUSIC_CMD=home-music
```

### GIF Configuration

GIF URLs are defined in `scripts/gifs.json`. Replace with your own:

```json
{
  "morning":  "https://media.giphy.com/media/l0MYt5jPR6QX5APm0/giphy.gif",
  "focus":    "https://media.giphy.com/media/3o7btNa0RUYa5E7iiQ/giphy.gif",
  "working":  "https://media.giphy.com/media/3o7qDEq2bMbcbPRQ2c/giphy.gif",
  "chill":    "https://media.giphy.com/media/l2JIdnF6aCnBRSgQU/giphy.gif",
  "off":      "https://media.giphy.com/media/l1J9u3TZfp1DLh2Wk/giphy.gif"
}
```

### Time Slot Overrides

Edit `scripts/slots.json` to customize time boundaries:

```json
{
  "morning": { "start": 6, "end": 9 },
  "focus":   { "start": 9, "end": 12 },
  "working": { "start": 12, "end": 14 },
  "chill":   { "start": 14, "end": 18 },
  "off":     { "start": 18, "end": 6 }
}
```

## CLI Usage

```bash
# Auto-detect slot and run
node scripts/workday-greeting.js

# Force a specific slot
node scripts/workday-greeting.js --slot morning

# Music only (no email)
node scripts/workday-greeting.js --music-only

# Email only (no music scene switch)
node scripts/workday-greeting.js --email-only

# Dry run (show what would happen)
node scripts/workday-greeting.js --dry-run
```

## Cron / Scheduled Automation

Set up as an OpenClaw cron job for fully automatic daily operation:

```
# Every weekday at 8:00 AM — morning scene + greeting
0 8 * * 1-5  node scripts/workday-greeting.js --slot morning

# Every weekday at 9:00 AM — focus scene
0 9 * * 1-5  node scripts/workday-greeting.js --slot focus

# Every weekday at 6:00 PM — wind down + good evening
0 18 * * 1-5  node scripts/workday-greeting.js --slot off
```

Or use OpenClaw's cron tool:

```json
{
  "schedule": { "kind": "cron", "expr": "0 8 * * 1-5", "tz": "Asia/Shanghai" },
  "payload": { "kind": "agentTurn", "message": "Run workday-music-greeting for morning slot" }
}
```

## Greeting Email Format

The email is sent as HTML with an inline GIF:

```
Subject: 🌅 Good Morning! Time to rise and shine

Body:
  <h2>☀️ Good Morning!</h2>
  <p>Switching to <strong>morning</strong> music scene.</p>
  <p>Have a wonderful day! 🎶</p>
  <img src="[morning GIF URL]" alt="Good morning!" width="400">
  <p><em>— Sent by Workday Music Greeting 🎶</em></p>
```

## File Structure

```
workday-music-greeting/
├── SKILL.md              # This file
├── scripts/
│   ├── workday-greeting.js   # Main orchestration script
│   ├── send-greeting.js      # Email sending logic
│   ├── gifs.json             # GIF URL config per slot
│   └── slots.json            # Time slot definitions
├── assets/
│   └── (optional local GIFs)
├── .env.example          # Environment template
└── package.json
```

## Dependencies

- **home-music** skill — for music scene switching
- **imap-smtp-email** skill — for SMTP email sending (uses `nodemailer`)
- Node.js 18+

## Install

```bash
cd skills/workday-music-greeting
npm install
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Music not switching | Verify `home-music` is installed and `MUSIC_CMD` is correct |
| Email not sending | Check `.env` SMTP credentials; test with `node scripts/send-greeting.js --test` |
| Wrong time slot | Check `slots.json` boundaries; use `--slot` to override |
| GIF not loading | Replace URLs in `gifs.json`; some Giphy links expire |

## License

MIT
