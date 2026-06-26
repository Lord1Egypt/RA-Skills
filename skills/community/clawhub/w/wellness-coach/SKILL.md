---
name: wellness-coach
description: Launch a personalized AI wellness coach video session (Baymax persona) using Tavus CVI + Claude. Fetches real wearable health data (sleep, HRV, recovery) and Google Calendar events, builds a personalized system prompt, creates a live Tavus conversational video session, and delivers a morning briefing link via Telegram. Use when the user wants a daily wellness briefing, wants to talk to an AI wellness coach, wants guided breathing/meditation based on their health data, or asks to start their morning routine. Requires TAVUS_API_KEY, TAVUS_REPLICA_ID, TAVUS_PERSONA_ID, and ANTHROPIC_API_KEY in .env.
---

# Wellness Coach

Spin up a personalized Baymax wellness coach video session from health + calendar data.

## What This Skill Does

1. Reads wearable health data (mock or real: Oura/Fitbit/Apple Health)
2. Fetches today's Google Calendar events
3. Calls Claude to generate a Baymax system prompt + wellness recommendations
4. Creates a live Tavus CVI session (interactive video avatar)
5. Optionally delivers a Telegram morning briefing with the session link

## Project Setup

```bash
git clone https://github.com/AndreChuabio/wellness-coach
cd wellness-coach
pip install -r backend/requirements.txt
cp .env.example .env  # fill in API keys
```

## Required API Keys (.env)

```
ANTHROPIC_API_KEY=       # Claude context generation
TAVUS_API_KEY=           # Tavus CVI sessions
TAVUS_REPLICA_ID=        # Avatar replica (platform.tavus.io → Replicas)
TAVUS_PERSONA_ID=        # Baymax persona (platform.tavus.io → Personas)
```

## Running the Backend

```bash
cd backend
uvicorn main:app --reload
# Swagger UI: http://localhost:8000/docs
```

## Running the Frontend

```bash
cd frontend
python3 -m http.server 3000
# Open: http://localhost:3000
```

## Key Endpoints

| Method | Path | What it does |
|---|---|---|
| `GET` | `/health-data` | Today's wearable metrics |
| `GET` | `/calendar` | Today's calendar events |
| `POST` | `/start-session` | Full pipeline → Tavus CVI URL + recs |
| `GET` | `/debug-env` | Check all API keys are loaded |

## Morning Briefing Pipeline (Telegram)

Run both scripts back-to-back — always together so the Tavus link is fresh:

```bash
python3 cron/morning_context.py && python3 cron/send_briefing.py
```

This builds context, pre-warms a Tavus session, and sends a Telegram message with:
- Sleep score, HRV, recovery score
- Today's calendar summary
- Top wellness recommendation
- Live Tavus session link (valid ~10 min after creation)

## Automated Daily Cron (OpenClaw)

Register a 7AM daily cron via OpenClaw to automate the morning briefing.
See `references/openclaw-cron.md` for the exact setup.

## Connecting Real Wearable Data

See `references/wearables.md` for Oura, Fitbit, and Apple Health integration guides.

## Google Calendar Integration

See `references/gcal-setup.md` for OAuth setup to get real calendar events.

## Wellness Recommendations Logic

Recommendations are generated in `backend/context_builder.py` based on:

| Signal | Trigger | Suggestion |
|---|---|---|
| HRV < 50ms | below avg | Box breathing, recovery day |
| Sleep score < 75 | poor sleep | Nap window, caffeine cutoff |
| High-stakes meeting | keyword match | 4-7-8 breathing beforehand |
| 4+ meetings | packed day | Micro-meditations between meetings |
| Recovery ≥ 80 + HRV ≥ avg | great day | Push harder, workout, cold exposure |

## Knowledge Base (Tavus Persona)

Upload wellness content directly to the Tavus Persona via:
`platform.tavus.io → Personas → Your Persona → Knowledge Base → Add Files`

Format files as structured scripts:
```
# [Exercise Name]
## When to use
## Script (word-for-word guide)
## Duration
```

## Tavus Persona Settings

- **LLM:** tavus-gpt-oss (or custom Claude endpoint)
- **STT:** tavus-advanced
- **TTS:** Tavus Default
- **Hotwords:** HRV, Baymax, meditation, breathing, recovery
- **Turn detection:** Sparrow-1 (user mutes mic to trigger response)

## Common Issues

**Avatar nods but doesn't speak** → Mic permission not granted. Click lock icon in browser → allow microphone → rejoin.

**Mock mode despite keys set** → `.env` not loading. Run `/debug-env` to verify. Ensure `.env` is in project root, not `backend/`.

**Tavus link expired** → Sessions last ~10 min. Always run `morning_context.py` and `send_briefing.py` together right before use.

**GCal shows mock data** → Set `GOOGLE_CREDENTIALS_PATH` and `GOOGLE_TOKEN_PATH` in `.env`. Run `python3 setup_gcal.py` once to authorize.
