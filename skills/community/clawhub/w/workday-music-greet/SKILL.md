---
name: workday-music-greet
description: Auto-switch music scenes by workday schedule and send matching GIF greeting emails. Combines home-music scene control with IMAP/SMTP email for a full morning-to-evening ambient workflow.
version: 1.0.0
author: OpenClaw Workspace
tags: ["music", "automation", "email", "workday", "cron"]
triggers:
  - workday music
  - music schedule
  - greeting email
  - daily music scene
metadata:
  openclaw:
    requires:
      bins: ["node", "npm"]
    emoji: "🗓️🎵"
---

# Workday Music & Greet

Automate your workday with timed music scene switches and GIF-enhanced greeting emails.

## What It Does

| Time | Scene | Email Greeting |
|------|-------|---------------|
| 07:30 | 🌅 Morning | "Good morning! Start fresh ☀️" + sunrise GIF |
| 09:00 | 💼 Focus | "Deep work time 🎯" + focus GIF |
| 12:00 | 🍱 Break | "Lunch break! Recharge 🔋" + food GIF |
| 14:00 | 💼 Focus | "Back at it! 💪" + coffee GIF |
| 17:30 | 😌 Chill | "Wind down time 🧘" + sunset GIF |
| 22:00 | 🔇 Off | "Good night! 🌙" + moon GIF |

## Setup

### 1. Install Dependencies

```bash
cd skills/workday-music-greet
npm install
```

### 2. Configure Email (.env)

Create a `.env` file in the skill directory:

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=you@gmail.com
SMTP_PASS=your-app-password
SMTP_FROM=you@gmail.com
GREET_TO=you@gmail.com
```

### 3. Configure Music Scenes

Edit `scripts/config.json` to set your preferred scenes and `home-music` command path.

### 4. Register Cron Jobs

Run the setup script to register all timed triggers:

```bash
node scripts/setup-cron.js
```

Or set up manually — each scene triggers `node scripts/scene-trigger.js <scene>`.

## One-Shot Usage

Trigger a scene + email manually:

```bash
node scripts/scene-trigger.js morning
node scripts/scene-trigger.js focus
node scripts/scene-trigger.js break
node scripts/scene-trigger.js chill
node scripts/scene-trigger.js off
```

## GIF Sources

Default GIFs are pulled from Giphy. To use custom GIFs, replace URLs in `scripts/config.json`.

## Architecture

```
workday-music-greet/
├── SKILL.md                 # This file
├── package.json             # Dependencies (nodemailer)
├── scripts/
│   ├── config.json          # Scene & email configuration
│   ├── scene-trigger.js     # Main: switch scene + send email
│   ├── send-greet.js        # Email sending logic
│   └── setup-cron.js        # Register OpenClaw cron jobs
└── assets/
    └── email-template.html  # HTML email template
```

## Dependencies

- **home-music** skill (for music scene control)
- **imap-smtp-email** skill (for email sending; reuses SMTP config)
- **OpenClaw cron** (for scheduled triggers)

## License

MIT