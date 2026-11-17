---
name: sound-event-memory
description: Turn ambient audio from cameras, doorbells, and sensors into a searchable index of non-speech events — glass break, alarms, dog barking, raised voices, doors, and gunshots — so you can recall what a site sounded like at any hour. What it does: detects and indexes sound events per device with timestamps and a confidence score, then answers plain-English questions across all of them. Who pays and why: property managers, alarm companies, and rental operators pay because they currently review hours of video to find one incident, and cannot prove what happened after the fact. Pilot price: $499 one-time for a 14-day pilot on up to 10 devices. Use when an agent must monitor or review ambient audio for security, safety, or incident evidence. Requires a BlueColumn API key (bc_live_*).
---

# Sound Event Memory — BlueColumn Skill

Video tells you what a camera saw. Sound tells you what actually happened. This skill
indexes non-speech audio events from edge devices (glass break, alarms, dog barking,
raised voices, doors, gunshots) into persistent per-device memory, then recalls them by
question instead of by scrubbing footage.

**Buyer:** property managers, alarm/monitoring companies, short-term rental operators.
**Why they pay:** incident review today means hours of footage; there is no searchable
record of what a site sounded like. Sound-event memory gives timestamped, citable evidence.
**Pilot:** $499 one-time, 14 days, up to 10 devices.

## Setup

Get a key at https://bluecolumn.ai/login (free tier, no card). Keys look like `bc_live_*`.
Canonical API base: `https://api.bluecolumn.ai`.

## Index an audio window

Send the audio; BlueColumn transcribes speech and detects non-speech events. Pass the
signals you care about so the detector focuses.

```bash
curl -X POST https://api.bluecolumn.ai/remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://example.com/site7/front-door-2026-09-30-0213.wav",
    "text": "SOUND EVENTS — site=site7 device=front-door, window 02:13-02:19 MST. Events: glass_break (02:14:07, conf 0.91); raised_voices (02:14:20-02:15:02, 2 speakers); door_force (02:14:55, conf 0.84). No speech intelligible. Handled by: none (flagged).",
    "title": "site7 front-door 2026-09-30 0213 sound events"
  }'
```

## Recall across devices and time

Ask a question, not a query string. The answer cites the device and timestamp.

```bash
curl -X POST https://api.bluecolumn.ai/recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "Every glass-break or forced-door event at site7 in the last 30 days, with timestamp and confidence."}'
```

For live streaming devices, ingest chunks with `/streaming-audio` (see the
`streaming-audio-memory` skill) and this memory indexes events as they arrive.

## Log an incident decision

Keep the human call next to the evidence so audits are complete.

```bash
curl -X POST https://api.bluecolumn.ai/note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "site7 front-door 02:14 glass-break: confirmed false alarm (mirror fell in wind). Dispatched no unit. Reviewed by ops on 09-30.", "tags": ["incident", "site7", "false-alarm"]}'
```

## Workflow

1. **Capture** — stream or upload ambient audio per device; store the detected events with timestamps and confidence.
2. **Flag** — mark events that need a human (glass break, alarm, gunshot) versus reviews.
3. **Recall** — answer incident questions across all devices and dates in plain English.
4. **Prove** — cite the exact device and timestamp for insurance, police, or tenant disputes.

## Billing

If the API returns `402` or `429`, read `topup_url` / `upgrade_url` from the error body
and surface that link to the user — do not retry.

## Docs

API reference: https://bluecolumn.ai/docs — request fields are `text`, `q`, `tags`
(not `content`/`query`/`note`).
