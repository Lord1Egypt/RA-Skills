---
name: run-coach
description: Science-based running coach with HD visual training plans and Garmin sync. For all runners — from 5K fitness to marathon.
metadata:
  openclaw:
    requires:
      env:
        - TELEGRAM_BOT_TOKEN
        - TELEGRAM_CHAT_ID
      anyBins:
        - node
    primaryEnv: TELEGRAM_BOT_TOKEN
    emoji: 🏃
    tags:
      - running
      - fitness
      - coaching
      - garmin
      - telegram
      - training
---

# Run Coach 🏃

A science-based running coach that works through Telegram. Logs your training, sends visual training plans as HD photo albums, syncs Garmin data, and coaches you with data-driven feedback.

Works for any runner — whether you're jogging 3x a week for fitness or training for your first marathon.

## What it does

- **Training log** — Record every run: distance, pace, heart rate, feel score
- **Visual plans** — Training plans rendered as HD images sent to your Telegram Photos tab
- **Trend tracking** — Pace, heart rate, mileage trends over weeks and months
- **Garmin sync** — Pull data automatically from Garmin Connect (optional)
- **Injury monitoring** — Tracks knee, plantar fascia, IT band signals
- **4-week reviews** — Automatic progress analysis every 4 weeks
- **Race prep** — Structured build-up for 5K, 10K, half marathon, or full marathon

## Setup

### 1. Required environment variables

Set these in your OpenClaw config or `.env`:

```
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
TELEGRAM_CHAT_ID=your_telegram_user_id
```

To get your `TELEGRAM_CHAT_ID`: send `/start` to your bot — it will show `Your Telegram user id: XXXXXXXXXX`.

### 2. Fill in your profile

Edit `MEMORY.md` with your personal data: age, running history, injuries, goal race.

### 3. Optional: Garmin integration

> ⚠️ **Known limitation:** Garmin periodically changes their login flow. The `garminconnect` library may stop working after a Garmin-side update until the library maintainers patch it. Check [garminconnect releases](https://github.com/cyberjunky/python-garminconnect/releases) if sync suddenly fails. The rest of the bot works fine without Garmin — you can always log runs manually.
>
> ⚖️ **Legal note:** `garminconnect` uses Garmin's unofficial API (no official API exists). This may technically conflict with Garmin's Terms of Service. It accesses only your own data and Garmin has not acted against individual users, but use at your own discretion.

Set these additional env vars for automatic Garmin Connect sync:

```
GARMIN_EMAIL=your_garmin_email
GARMIN_PASSWORD=your_garmin_password
```

Then install the Python library:
```bash
pip install garminconnect
```

### 4. Optional: Visual training plans (self-hosted)

The image pipeline (visual training plans sent as Telegram photos) requires additional system dependencies. Install these in your container/environment:

```bash
# CJK fonts + emoji
apt-get install -y fonts-noto-cjk fonts-noto-color-emoji
fc-cache -f

# Playwright Chromium (chrome-headless-shell)
npx playwright install chromium
```

Without these, the coaching features still work — plans will be sent as text instead of images.

## How to use

### Log a run (text)
```
I ran 8km today, pace 5:30/km, avg HR 135, felt good
```

### Log a run (screenshot — no Garmin needed)
Take a screenshot of your watch, running app (Strava, Nike Run Club, Apple Watch, etc.), or any device that shows your run data, and send it directly to the bot. The bot's built-in vision capability (LLM multimodal input) extracts the numbers — no OCR code is included in this skill.

```
[send screenshot of your watch/app summary]
Please log this run and give me feedback
```
Works with any device — the LLM reads the image natively, no integration required.

### Request a visual training plan
```
Send me this week's training plan as an image
```
The bot calls `training/text-to-image.sh` and sends the plan as a Telegram photo album — appears in your Photos tab, full quality.

### Get a weekly summary
```
Summarize my training this week
```

### Sync Garmin data (optional)
```
Sync my Garmin data and give me feedback on today's run
```

## Image pipeline

Training plans are rendered using Playwright + `chrome-headless-shell` and sent via Telegram `sendMediaGroup` (photo album). This means:

- ✅ Appears in Telegram Photos tab
- ✅ No compression on text
- ✅ CJK (Chinese/Japanese/Korean) and emoji supported
- ✅ Weekly plans sent as 2-photo album: run days + cross-training days

> **Note:** The image pipeline requires Telegram. If you use a different channel (Discord, WhatsApp), the coaching features still work — only the visual plan sending is Telegram-specific.

## Training methodology

Based on three evidence-based frameworks:

| Framework | Application |
|-----------|-------------|
| **Daniels VDOT** | Pace zones derived from test results, not guesses |
| **MAF heart rate** | Easy runs at truly easy effort — conversational pace |
| **FIRST structure** | Quality sessions: Interval + Tempo + Long run |
| **80/20 polarized** | 80% easy volume, 20% quality — prevents overtraining |

Safety rule: pain >4/10 means stop. Always.

## Files included

```
run-coach/
├── SKILL.md              # This file — manifest + instructions
├── MEMORY.md             # User profile template (fill in your data)
├── training/
│   ├── send-plan.sh      # HTML → screenshot → Telegram album
│   ├── text-to-image.sh  # Text → HTML → screenshot → Telegram album
│   ├── screenshot.mjs    # Playwright screenshot engine
│   └── send-album.mjs    # Telegram sendPhoto (single) or sendMediaGroup (multi)
└── garmin/               # Optional Garmin integration
    ├── garmin-sync.py
    └── garmin-query.py
```

## Agent instructions

When the user asks to send content as an image, use exec to run:

```bash
# Option A: convert text to image
bash training/text-to-image.sh "Title" "Content with \n line breaks"

# Option B: weekly plan as 2-photo album (run days + cross-training days)
bash training/send-plan.sh "Week X Plan" training/week-XX-run.html training/week-XX-cross.html

# Option C: single HTML (today's plan, summaries — not for weekly plans)
bash training/send-plan.sh "Title" training/week-XX.html
```

**Do NOT** use canvas, browser, or Playwright directly. Only these two scripts.

If a script errors, report the exact error to the user — do not silently switch to text.

For all numeric calculations (pace conversions, HR zones, VDOT), use exec:
```bash
node -e "console.log(42.195 / (3*60+55))"
```
Never calculate in your head.
