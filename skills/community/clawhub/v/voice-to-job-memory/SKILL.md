---
name: voice-to-job-memory
description: A field worker records a quick voice note after a site visit; the skill updates the job record with measurements, materials, customer changes, and unresolved questions, then drafts an estimate handoff. Use for fence, HVAC, landscaping, and other field-service businesses. Requires a BlueColumn API key (bc_live_*).
---

# Voice-to-Job Memory — BlueColumn Skill

The details that die between the truck and the office are exactly what make or break a job. This skill turns a 60-second voice note from the field into an updated job record and a draft estimate handoff — no typing, no lost measurements.

## Setup

Get a free key at https://bluecolumn.ai/login (no card). Keys look like `bc_live_*`. Base URL: `https://api.bluecolumn.ai`.

## Capture the site visit

The worker talks; BlueColumn transcribes and stores the job update.

```bash
curl -X POST https://api.bluecolumn.ai/remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://example.com/jobs/441-voice-note-09-29.mp3",
    "text": "JOB 441 UPDATE — site visit 09-29. Measurements: back fence 62ft, needs 4 posts replaced + 2 gates (5ft and 8ft). Materials: cedar 1x6 dog-ear, 18 boards. Customer change: wants gate on left side not right; gate hardware in black. Unresolved: HOA — customer unsure if fence height 6ft allowed, will send HOA doc. Next: draft estimate with cedar + black hardware, hold until HOA doc arrives.",
    "title": "job-441 - fence - 09-29 site visit"
  }'
```

## Pull the job before writing the estimate

The office recalls the latest site note when drafting the quote.

```bash
curl -X POST https://api.bluecolumn.ai/recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "What did the field note say for job 441 — measurements, materials, customer changes, and open questions?"}'
```

## Log a quick change from the road

```bash
curl -X POST https://api.bluecolumn.ai/note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Job 441: customer just approved 6ft height (HOA doc received). Release estimate today.", "tags": ["job-441", "approved"]}'
```

## Workflow

1. **On site** — worker records a voice note: measurements, materials, changes, open questions.
2. **Back office** — recall the job note and draft the estimate from it.
3. **Changes** — new voice notes append to the same job record, so the quote always reflects the latest site truth.
4. **Handoff** — estimate drafts reference the exact visit note, so nothing is invented from memory.

## Billing

If the API returns `402` or `429`, read `topup_url` / `upgrade_url` from the error body and surface that link to the user — do not retry.

## Docs

API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
