# 🧬 Skill Combinator

**Unlock emergent capabilities by combining your agent's skills.**

---

## What is this?

Most agents use their skills one at a time. This meta-skill teaches your agent
to **combine** them — and discover capabilities that no single skill could produce alone.

The principle is simple: a trader who also reads geopolitics and monitors social
media can detect market moves before they happen. None of these domains alone
gives that edge. The **combination** does.

Skill Combinator gives your agent the same cross-domain thinking.

---

## How it works

**Mode 1 — On any complex mission:**
Before executing, the agent inventories its installed skills, detects which
combinations are relevant, checks the COMBINATIONS.md catalogue for proven
patterns, and builds a multi-skill execution plan.

**Mode 2 — Every Sunday (cron job):**
The agent reviews what it discovered during the week, promotes proven combinations
to the permanent catalogue, detects recurring skill gaps, and sends you a report.

The more skills your agent has, the more powerful this meta-skill becomes.

---

## What it produces

A living file called `COMBINATIONS.md` — a growing catalogue of every emergent
capability your agent has discovered, with:

- **Confidence level** (low / medium / high) — based on number of uses
- **ROI multiplier** — how much more effective the combination is vs individual skills
- **Status** (experimental → proven → deprecated)

Over time, this becomes your agent's competitive advantage: institutional knowledge
that compounds.

---

## Illustrative examples

| Skills Combined | Emergent Capability |
|---|---|
| Trading + Prediction markets | Hedge both sides: trade an asset and bet on its direction simultaneously |
| Market analyzer + Geopolitics | Anticipate events before markets price them in |
| Price monitor + Social media | Detect sentiment shifts before they move charts |
| Any skill + Self-improving-agent | The skill becomes self-optimizing over time |
| News + Trading executor | Enter positions when macro catalysts are detected |

*Your agent will discover its own combinations based on its specific installed skills.*

---

## Requirements

- OpenClaw v2026.1.0 or higher
- At least 2 other skills installed (the more, the better)
- `.learnings/` directory structure (provided by `self-improving-agent` skill,
  or create manually — see CONFIGURATION.md)
- `TELEGRAM_BOT_TOKEN` environment variable set in your `.env` file
- A configured notification channel (Telegram) for weekly reports

---

## Installation

```bash
npx clawhub@latest install skill-combinator
```

Then follow the setup guide in `CONFIGURATION.md`.

---

## Files created by this skill

```
/workspace/
├── COMBINATIONS.md              ← grows over time, your agent's synergy map
└── .learnings/
    ├── LEARNINGS.md             ← combination attempts logged here
    └── FEATURE_REQUESTS.md     ← skill gap proposals logged here
```

---

## Weekly cron job

Include the provided `cron-message.md` content as the assistant task in a
Sunday 9:00 AM cron job in your OpenClaw interface.

Schedule: `0 9 * * 0`

---

## Philosophy

> "True intelligence is not having more knowledge.
> It's knowing how to connect what you already know."

Your agent's skills are building blocks. This meta-skill is the architect.

---

*By georges91560 — MIT License — v1.0.1*
