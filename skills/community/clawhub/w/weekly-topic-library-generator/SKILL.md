---
name: weekly-topic-library-generator
description: Weekly viral-topic library for AI video creators. Collects public trend signals from TikTok / Reels / Shorts, extracts non-copyright structure (hook, pacing, visual keywords, camera), maps a generator-ready prompt pack, and grades topics. Use when the user says generate this week's topic library, run the topic library, weekly content production, or viral teardown plus prompts.
---

# Weekly Topic Library Generator

Core workflow only: collect → compliant teardown → prompt pack → grade → ship Markdown + JSON. Marketing copy is out of scope for this public skill.

## When to use

The user wants a week of AI-video topic ideas with reusable prompts, not a 1:1 clone of someone else's clip.

## Rights and AIGC

1. Work from **public** trend write-ups, public posts, and search results. Do not download videos, scrape behind a login, or copy captions/audio.
2. Extract **non-copyright** pieces only: topic angle, emotional hook, structure, visual style keywords, camera move, color, pacing. Never extract frame-accurate shots, dialogue, trademarks, a real person's face, protected characters, or a full shot list meant for cloning.
3. Prompt packs produce **synthetic** video. Every topic that shows a face, a speaking object, or a made-up person must carry: `AI-generated / synthetic; add the platform AI label`.
4. Do not claim a topic "will go viral" or attach a star rating as a promise. Grades are an internal filter, not a performance guarantee.

If a source is copyrighted IP (studio characters, collectible toys, brand mascots), drop it.

## Workflow

### 1. Collect (last 7 days)

Search the open web for AI-generated short-video trends this week. Queries:

- `AI generated viral video [current month year]`
- `Runway Pika Kling viral trends [current year]`
- `AI content trends TikTok Reels Shorts`

For each hit record: platform, style name, why it spreads, view-order-of-magnitude if stated by a public source, date. Prefer new styles over repeats. Keep the source URL.

Target: 12–20 raw rows. Fewer is fine for a smoke run; say so.

### 2. Compliant teardown

For each row, write a short brief:

- Style name
- Hook (emotion, not a copied line)
- Structure (e.g. result → process → result)
- Visual keywords
- Camera
- Color / pace

Banned in the brief: verbatim captions, logos, celebrity likeness, protected characters, music titles used as prompts.

### 3. Prompt pack

Four blocks, copy-paste ready for a text-to-video model (Runway-style; Kling / Pika as alternates if the user asks):

1. **Scene** — `[style] of [subject], [detail], [light], [quality]`
2. **Camera** — move, speed, duration (5s or 10s)
3. **Params** — generator, T2V or I2V, 9:16, 1080p
4. **Negative** — `text, watermark, blurry, distorted anatomy, extra limbs`

No brand names. No real-person names. If a face appears, add the AI-label line from above.

### 4. Grade (filter, not a promise)

Score 1–5 on three axes: replicability, spread-odds, compliance. Product = replicability × spread-odds × compliance.

- S: ≥45 — lead the week
- A: 30–44 — backup
- B: 15–29 — possible, has a catch
- <15 — drop

Write the three numbers and the product. Do not write "guaranteed views."

### 5. Ship

Write two files in the working directory, then pause for the user:

- `weekly-topic-library-[Year]W[WeekNumber].md`
- `weekly-topic-library-[Year]W[WeekNumber].json`

Each topic: title, teardown, prompt pack, grade, risk flags, suggested generator.

Markdown opens with this disclaimer:

```
Synthetic / AIGC library. Prompts are starting points, not clones.
Do not omit platform AI labels. Grades are editorial, not performance forecasts.
```

Quality bar for a full week: at least 10 kept topics, with ≥3 S and ≥5 A. A smoke run may ship 3 topics and mark `smoke: true` in the JSON.

## Stop conditions

- User has not confirmed the library → do not write outreach or social posts.
- A topic needs a real person's face or a protected IP → delete it.
- Search failed → say so; do not invent view counts.

## License

CC BY-SA 4.0. Commercial use allowed. Credit the author and share derivatives under the same license.
