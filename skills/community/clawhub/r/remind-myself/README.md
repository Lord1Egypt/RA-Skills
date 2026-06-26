# reminder

OpenClaw skill to set one-shot reminders delivered via Telegram at a specific time or after a duration.

## What it does

Tell your agent to remind you of something — at an absolute time or after a relative delay — and it schedules a cron job that fires a Telegram message at the right moment and self-destructs after delivery.

## Requirements

- OpenClaw gateway running locally
- Telegram channel configured in OpenClaw
- Your Telegram chat ID set in `~/.openclaw/workspace/TOOLS.md`

## Setup

1. Add your Telegram chat ID to `TOOLS.md`:
   ```markdown
   ### Telegram
   - **My chat ID**: `<your_chat_id>` — use as `--to <id>` for cron delivery
   ```

2. Install the skill via clawhub:
   ```bash
   clawhub install remind-myself
   ```

## Usage

Natural language, relative or absolute:

> "Rappelle-moi dans 20 minutes de sortir le linge."

> "Remind me tomorrow at 9am to call the dentist."

> "Dans 2h : check the oven."

The agent schedules the cron job and confirms with the exact time. The reminder is delivered directly to your Telegram chat.
