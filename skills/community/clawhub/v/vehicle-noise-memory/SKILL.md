---
name: vehicle-noise-memory
description: Give a shop a memory for what broken cars sound like. What it does: records engine, brake, suspension, and drivetrain noises; transcribes and indexes each clip with the year/make/model, mileage, symptom, and suspected cause; then recalls every prior case with a similar sound and what actually fixed it. Who pays and why: independent auto shops and fleet garages pay because diagnostic time is the real bottleneck, and the senior tech's ear for "that noise" walks out the door at retirement — this turns it into a searchable, shop-owned asset. Pilot price: $499 one-time for a 30-day pilot on one bay and one tech. Use when a mechanic, service writer, or fleet tech needs to diagnose a noise by comparing it to past repairs. Requires a BlueColumn API key (bc_live_*).
---

# Vehicle Noise Memory — BlueColumn Skill

A veteran tech hears a rattle and knows the fix in ten seconds. That ear is not written down anywhere. This skill records the noise, captures the diagnosis, and recalls the match — so the quietest knowledge in the shop becomes the most reusable.

## Setup

Get a free key at https://bluecolumn.ai/login (no card). Keys look like `bc_live_*`. Base URL: `https://api.bluecolumn.ai`.

## Log a noise case

Record the noise with the vehicle context and what you found. BlueColumn transcribes the clip and indexes the structured record alongside it.

```bash
curl -X POST https://api.bluecolumn.ai/remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://shop.example.com/clips/ro-2026-10-01-engine.mp3",
    "text": "NOISE CASE RO 4821 — 2016 Ford Escape, 118k mi. Symptom: rhythmic chirp at idle, worsens cold, fades warm. Location: front accessory drive. Suspected cause: serpentine belt tensioner or idler pulley bearing. Fix applied: replaced tensioner + idler pulley. Result: noise gone. Verified by road test. Source: bay-2 voice note, 10-01.",
    "title": "noise - 2016 Ford Escape chirp - RO 4821"
  }'
```

## Recall a match before you guess

When a new car comes in with a noise, search the shop's own history first.

```bash
curl -X POST https://api.bluecolumn.ai/recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "chirp at idle that gets worse cold and fades warm — what fixed this before and on which vehicles?"}'
```

## Note the guess mid-diagnosis

When a tech forms a hypothesis, store it so the next person on the ticket can see the reasoning.

```bash
curl -X POST https://api.bluecolumn.ai/note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Guess: front idler pulley bearing. Order both tensioner and idler — cheap insurance, same labor time.", "tags": ["noise", "diagnosis", "RO-4821"]}'
```

## Workflow

1. **On intake** — record the noise on a phone and store it with year/make/model, mileage, and symptom words.
2. **Before teardown** — recall prior cases with a similar sound and suspected cause.
3. **On close** — store the confirmed fix and result so the match gets stronger each time.
4. **Monthly** — recall the top recurring noises and turn them into a shop cheat-sheet for new techs.

## Billing

If the API returns `402` or `429`, read `topup_url` / `upgrade_url` from the error body and surface that link to the user — do not retry.

## Docs

API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
