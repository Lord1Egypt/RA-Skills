---
title: "Second Brain Visualizer — Setup Guide"
version: 1.0.0
---

# Setup Guide

## The idea

You need a place to put things that's low-friction enough that you'll actually use it. Not a note-taking app with folders. Not a task manager. Just a channel — somewhere you can send a thought in ten seconds and move on.

The Second Brain Visualizer reads what accumulates there over time and finds the signal.

---

## Step 1 — Pick your drop channel

The system works with any channel your OpenClaw agent can read. Pick one you already use, or create a dedicated one.

**Good options:**
- A private Slack channel (e.g. `#sb-inbox`)
- A Telegram bot or private group
- A WhatsApp note-to-self
- A Gmail label you forward things to
- A private Discord channel

The channel doesn't matter. What matters is that dropping something there costs you almost nothing. If there's friction, you won't use it.

**One rule:** don't curate. Drop the half-formed thing. The misspelled thing. The joke that might be a product idea. The line from a book you can't explain yet. Raw input is better input. The system reads for intent, not polish.

---

## Step 2 — Start your atom ledger

Create a markdown file in your vault at `memory/second-brain.md`. This is where your parsed atoms will live.

Start with this front matter:

```markdown
---
title: "Second Brain — Atom Ledger"
created: YYYY-MM-DD
tags: [second-brain, ideas, capture]
status: active
---

# Second Brain — What It Is

A raw idea capture tool. Not a journal. Not a task list. A place for things worth keeping that don't fit anywhere else yet.
```

That's it. The parser will append atoms below this header as you run it.

---

## Step 3 — Write your first atoms manually (optional but recommended)

Before you wire up ingestion, seed the ledger by hand with 10–20 ideas from memory. Things you've been meaning to capture. This gives the clustering engine enough material to work with on first run.

Each atom follows this format:

```markdown
### ts: 1712034567

- **date:** 2026-04-06T14:00:00 UTC
- **raw:** your idea exactly as you thought it — misspelled, incomplete, whatever
- **type:** thought
- **tags:** [creativity, product]
- **signal:** hot
- **actionable:** no
- **nextAction:**
```

**Type options:** `thought` | `task` | `strategy` | `creative` | `meta` | `idea-jar` | `visual` | `link`

**Signal:** `hot` (strong energy right now) | `warm` (interesting, not urgent) | `cool` (low signal, keeping for record)

You don't have to fill everything out. `raw` is the only required field. The rest helps the clustering engine but won't break anything if it's missing.

---

## Step 4 — Run the parser

Once you have atoms in your ledger (either manual or from ingestion), run the parser to extract them into structured JSON:

```bash
node references/parser.js
```

This reads `memory/second-brain.md` from your vault and writes `data/second-brain-atoms.json`.

Check the output:

```bash
cat data/second-brain-atoms.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{len(d[\"atoms\"])} atoms parsed')"
```

You need at least 9 atoms before clustering is meaningful. More is better. 30+ atoms gives the engine real material to work with.

---

## Step 5 — Run clustering

With atoms in place, run the clustering engine:

```bash
node references/cluster.js
```

This calls your configured LLM with the full atom corpus and the intent-based clustering prompt. It writes `data/second-brain-clusters.json`.

First run takes 30–60 seconds depending on your LLM. Output will include clusters, tensions, emerging signals, and notable absences.

---

## Step 6 — Open the visualizer

The React component (`references/component.tsx`) renders the cluster graph. Mount it in your dashboard, or open it standalone.

Click any node to expand its cluster: base insight, LLM-generated deeper read, full atom list. Tensions and absences scroll below the graph.

Re-cluster whenever you've added 10+ new atoms. The clusters will shift as your idea stream evolves.

---

## What good looks like

After 2–3 weeks of consistent drops, you should see:

- 3–8 distinct clusters with names that feel accurate but slightly surprising
- At least one tension that makes you go "oh, that's real"
- An absence or two that points at creative territory you haven't touched yet
- FORMING clusters that didn't exist last week

That's the system working. The surprise is the signal.

---

## Troubleshooting

**"Not enough atoms to cluster"** — You need at least 9. Add more manually or run ingestion.

**Clusters feel generic** — Your atoms may be too surface-level. The raw field should capture the actual thought, not a cleaned-up summary of it. Rougher input produces sharper clusters.

**Same clusters every run** — You're not adding new atoms. The system can only find what's there.

**LLM timeout** — Large corpus (200+ atoms) can slow the clustering call. This is normal. Let it run.
