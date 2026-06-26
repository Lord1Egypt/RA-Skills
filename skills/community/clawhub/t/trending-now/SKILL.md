---
name: Trending Now
slug: trending-now
version: 1.0.0
homepage: https://clawic.com/skills/trending-now
description: Monitor internet and social media trends with heartbeat topic watchlists, freshness scoring, and concise alerts on what changed and why it matters.
changelog: Initial release with heartbeat templates, topic monitoring rules, cross-network validation flow, and alert message formats for actionable updates.
metadata: {"clawdbot":{"emoji":"T","requires":{"bins":[],"config":["~/trending-now/"]},"os":["darwin","linux","win32"]}}
---

## Setup

On first use, read `setup.md` and lock integration behavior before starting trend monitoring.

## When to Use

User needs ongoing updates about what is trending across the internet and social platforms, with special attention to X and rapid shifts in conversation.
Use this skill to define topic watchlists, run heartbeat-based research cycles, rank signal strength, and send concise messages only when there is meaningful change.

## Architecture

Memory lives in `~/trending-now/`. See `memory-template.md` for the baseline structure.

```text
~/trending-now/
|-- memory.md                 # Activation behavior, scope, and monitoring preferences
|-- topics.md                 # Active topics, query variants, and relevance boundaries
|-- runs.md                   # Heartbeat run history and change detection summary
`-- alerts.md                 # Alerts sent, impact notes, and false-positive log
```

## Quick Reference

Use the smallest relevant file for the current task.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory schema and state model | `memory-template.md` |
| Production heartbeat template | `HEARTBEAT.md` |
| Research and verification workflow | `research-protocol.md` |
| Source mix and quality requirements | `source-map.md` |
| Alert message contract and examples | `message-format.md` |

## Requirements

- Web access for live trend validation.
- User-approved scope for topics, geographies, and languages.
- Timezone and active hours for heartbeat delivery behavior.

Never claim a trend is current without timestamped evidence from at least two independent sources.

## Data Storage

Local notes in `~/trending-now/` include:
- monitored topics with query variants and stop words
- run-level evidence links and freshness timestamps
- alert history with confidence and post-send outcomes
- rejected spikes and false-positive rationale

## Core Rules

### 1. Define Topic Scope Before Monitoring
Each topic must include:
- explicit intent (`brand`, `product`, `industry`, `culture`, or `breaking-event`)
- inclusion and exclusion criteria
- audience and geography boundaries

Without scope, trend monitoring becomes noisy and low trust.

### 2. Use HEARTBEAT.md as the Operating Contract
Always maintain topic and output rules in `HEARTBEAT.md`.
Every cycle must follow one contract:
- actionable update -> send structured message
- no meaningful change -> return `HEARTBEAT_OK`

Do not send filler summaries when there is no decision-relevant movement.

### 3. Prioritize Source Diversity with X as Fast Signal
For each topic, gather evidence from:
- X for velocity and narrative emergence
- at least one community source (Reddit, forums, niche communities)
- at least one publisher or search trend source

Single-network spikes are hypotheses, not confirmed trends.

### 4. Enforce Freshness and Recency Windows
Classify findings by age:
- hot: <= 6 hours
- recent: <= 24 hours
- stale: > 24 hours

Escalate only hot or recent signals unless the user explicitly requests longer-horizon analysis.

### 5. Score Trend Strength Before Alerting
Apply a fixed score per candidate trend:
- volume shift
- cross-source confirmation
- novelty versus prior runs
- user relevance
- action urgency

If score is below threshold, store in watchlist and do not alert yet.

### 6. Send Messages in Decision-Ready Format
Every alert message must include:
- what changed
- why it matters now
- confidence and risks
- one concrete next action

No long narrative dumps. Message length should fit quick mobile reading.

### 7. Protect Cost and Credibility
Start with low-cost checks, then deepen only when a signal passes threshold.
Never use paid APIs every cycle unless the user explicitly approves budget.
Always mark uncertain claims and avoid overconfident language.

## Common Traps

- Treating repost volume on X as proof of broad trend adoption -> repeated false positives.
- Using only one source family -> hype detection without validation.
- Ignoring recency windows -> old stories presented as breaking updates.
- Sending alerts without an action recommendation -> interesting but not useful output.
- Expanding topic scope mid-cycle without user approval -> relevance drift.
- Logging conclusions without links and timestamps -> impossible to audit later.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://x.com | Topic keywords and public post metadata references | Detect fast-moving narratives and sentiment inflections |
| https://www.reddit.com | Topic keywords and thread metadata references | Validate community-level recurrence and depth |
| https://news.google.com | Topic keywords and article metadata references | Confirm publisher coverage and recency |
| https://trends.google.com | Query terms and trend interest snapshots | Estimate demand momentum over time |

No other data should be sent externally unless the user explicitly approves additional sources.

## Security & Privacy

Data that leaves your machine:
- topic keywords used for live trend research
- source lookups needed to verify recency and momentum

Data that stays local:
- monitoring preferences and topic definitions under `~/trending-now/`
- run history, confidence scores, and alert outcomes

This skill does NOT:
- access private social accounts by default
- post content on any social platform automatically
- run undeclared external requests outside approved sources

## Trust

This skill relies on public internet and social sources, including X and other platforms the user approves.
Only install and run it if you trust those sources and the external services used for research.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `monitoring` - Build monitoring loops with clear thresholds and escalation paths
- `news` - Structure news tracking and summarization for time-sensitive decisions
- `competitor-monitoring` - Track competitor moves with disciplined evidence and update cadence
- `in-depth-research` - Expand weak or mixed signals into deeper evidence-backed analysis
- `digest` - Turn many raw updates into compact, high-signal briefings

## Feedback

- If useful: `clawhub star trending-now`
- Stay updated: `clawhub sync`
