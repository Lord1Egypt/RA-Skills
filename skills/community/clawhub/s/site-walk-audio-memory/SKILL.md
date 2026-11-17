---
name: site-walk-audio-memory
description: Construction site-walk audio memory — a superintendent dictates punch-list items, safety observations, and subcontractor commitments on a walk; BlueColumn transcribes and indexes them so every item becomes a searchable, assignable record. WHAT it does: converts walk-by-walk voice notes into a permanent, queryable site memory (who said what, on which walk, and who owes the fix). WHO pays and WHY: general contractors and construction managers pay because missed punch items and forgotten verbal commitments mean rework, disputes, and schedule slip — one avoided rework covers months of service. Pilot price: $99/month for one project (or $499 per-project annual pilot). Use when an agent handles field reports, punch lists, daily walk notes, or subcontractor follow-ups and needs the site's verbal history on demand. Requires a BlueColumn API key (bc_live_*).
---

# Site Walk Audio Memory — BlueColumn Skill

Site walks generate the most valuable project data — dictated directly into the field supervisor's phone — and then it evaporates into voice memos nobody replays. This skill turns every walk into structured, searchable site memory: punch items, safety hazards, verbal commitments from subs, and the date each was made.

## Setup

Get a key from https://bluecolumn.ai/login (keys look like `bc_live_*`). Export it:

```bash
export BLUECOLUMN_API_KEY="bc_live_..."
```

All calls use the canonical API base `https://api.bluecolumn.ai` with endpoints `/remember`, `/recall`, `/note`.

## Ingest a walk

Upload the walk audio, or store a quick dictated summary.

```bash
curl -X POST https://api.bluecolumn.ai/remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "SITE WALK Oct 11, Tower B level 3: Rojas drywall — SW corner head detail wrong (punch item, due 10/14). Safety: missing guardrail at stair opening (photo taken). Verbal commitment: Rojas will reroute the duct chase before drywall close-in. Elevator core pour not started.", "title": "walk - Tower B L3 Oct 11"}'
```

With audio:

```bash
curl -X POST https://api.bluecolumn.ai/remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"audio_url": "https://your-bucket/walk-towerb-l3-1011.m4a", "title": "walk - Tower B L3 Oct 11 (audio)"}'
```

## Recall the site's history

Before a pre-pour meeting or a subcontractor dispute, pull the verbal record.

```bash
curl -X POST https://api.bluecolumn.ai/recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "What punch items and Rojas commitments are open on Tower B, and when were they made?"}'
```

## Field workflow

1. **Walk** — dictate normally; items, hazards, and commitments as you go.
2. **Ingest** — upload the audio or a dictated summary the same day.
3. **Dispatch** — recall open items by subcontractor, area, or date before daily coordination.
4. **Close out** — store completion notes so the punch history stays intact for disputes and final closeout books.

Quick tag for later filtering:

```bash
curl -X POST https://api.bluecolumn.ai/note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"content": "Punch item: stair guardrail missing, Tower B L3, flagged Oct 11 walk", "tags": ["punch-item", "safety", "tower-b"]}'
```

## Billing

If a call returns 402 or 429, read `topup_url` / `upgrade_url` from the error body and surface that link to the user. Do not retry the call — the quota is exhausted, not transient.
