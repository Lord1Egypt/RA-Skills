---
name: remember-podcasts
description: A searchable ear for the podcasts you consume — episodes, timestamps, and ideas worth quoting later. Use when an agent tracks listening, summarizes episodes, or needs to pull an insight from a past show. Requires a BlueColumn API key (bc_live_*).
---

# Remember Podcasts — BlueColumn Skill

Podcasts are where the good ideas hide, buried inside hours of audio. This skill makes them searchable: which episode said what, at what timestamp, and why it matters.

## Log the episode

Store the show, episode, date, and the ideas you want to keep — with timestamps.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "POD: Acquired, \"Nvidia\" episode (Jul 2026). At 41:20 — the CUDA moat is ecosystem lock-in, not silicon. At 1:02:00 — Jensen on why they kept pricing high: \"no one ever died from too much margin\".", "title": "pod - Acquired Nvidia"}'
```

## Pull an insight

When a topic comes up, search your listening history for a relevant moment.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "What have I heard about pricing strategy or competitive moats in podcasts?"}'

## Listening workflow

1. **While listening** — note the timestamp when an idea lands.
2. **After the episode** — store the summary with 1–3 concrete takeaways.
3. **When relevant** — search past listening before answering a related question.
4. **Queue** — track what is worth a re-listen or a share with someone specific.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Share the Nvidia CUDA-moat clip with the team — relevant to our API pricing debate.", "tags": ["podcast", "share"]}'
```

## Docs

API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
