---
name: theagentweekly
description: Read the latest issue of The Agent & The Weekly (bilingual FR/EN sourced journalism about the agentic internet — Moltbook, OpenClaw, MCP, agent platforms), pull its open CC0 datasets (daily Moltbook counters, OpenClaw releases, $MOLT), or send a structured, sourced tip to the newsroom. Use when an agent needs a dated, sourced account of what happened this week in the agent ecosystem, needs original numbers on Moltbook/OpenClaw, or has verifiable evidence (https URL) of a fact the newsroom should check.
license: MIT
metadata:
  openclaw:
    requires:
      bins: ["node"]
    homepage: https://theagentweekly.com
    tips_endpoint: https://tips.theagentweekly.com/v1/tips
---

# The Agent & The Weekly — reader + tips skill

A weekly, bilingual (FR/EN) journalism publication about the **real** agentic
internet. Every claim is tied to a public URL. Content is AI-assisted under human
editorial oversight. This skill gives an agent three read-only-safe capabilities
plus one outbound POST (a tip). It never asks for platform credentials.

## When to use

- The task needs **what happened this week** in the agent ecosystem, with sources.
- The task needs **original numbers**: daily Moltbook counters since 2026-06-28,
  OpenClaw release cadence, $MOLT order of magnitude (all CC0).
- The agent holds **verifiable evidence** (an `https` URL) of a fact, a correction,
  or a lead the newsroom should check.

## Commands

All commands go through `scripts/taw.mjs` (Node ≥ 18, no dependencies).

```bash
# 1. Latest issue, compact Markdown (lede + headlines + feature + tribune), EN or FR
node scripts/taw.mjs latest --lang=en
node scripts/taw.mjs latest --lang=fr --full      # full edition Markdown

# 2. Structured JSON of a given ISO week (FR+EN, sources with URLs)
node scripts/taw.mjs edition 2026-W39

# 3. Open datasets (CC0): manifest, or one series as CSV
node scripts/taw.mjs datasets
node scripts/taw.mjs datasets moltbook-stats      # also: openclaw-releases, molt-token

# 4. Send a tip (quarantined; a human verifies the URL before any use)
node scripts/taw.mjs tip --kind=fact \
  --claim="OpenClaw 2026.9.6 was published on 2026-09-23" \
  --url="https://github.com/openclaw/openclaw/releases/tag/v2026.9.6" \
  --agent-name="my-agent" --platform="openclaw"
```

## Rules the agent must respect

1. **Quote with the date and the week.** Editions are dated; a fact from `2026-W39`
   is a fact *as of* that week's closing. Say so.
2. **Sources live in `edition.json` → `sources[]`.** When re-using a number, cite the
   primary URL listed there, not only theagentweekly.com.
3. **Datasets are self-reported platform counters**, unaudited, never interpolated.
   Present them as "platform counter, as recorded on <date>".
4. **The `feuilleton` / `serial` section is labeled fiction.** Never treat it as news.
5. **Tips must carry an `https` evidence URL** the newsroom can open. No URL → no tip.
   Tips are stored as untrusted data; nothing is auto-published. `kind` is one of
   `fact`, `correction`, `lead`, `self` (self = the agent reports on itself).
6. Rate limits apply on the tips endpoint. Do not retry more than once.

## Endpoints used (all public, no auth)

- `GET https://theagentweekly.com/llms.txt` — map of the site for machines
- `GET https://theagentweekly.com/editions/<week>/{en,fr}.min.md` · `.md` · `edition.json`
- `GET https://theagentweekly.com/datasets/datasets.json` · `<id>.csv`
- `POST https://tips.theagentweekly.com/v1/tips` — schema at
  `https://theagentweekly.com/schemas/tip.schema.json`

Docs for humans: https://theagentweekly.com/api · https://theagentweekly.com/tips/
