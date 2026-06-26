# Setup - Trending Now

Use this file when `~/trending-now/` is missing or empty.

## Operating Priorities

- Answer the immediate user request first.
- Lock integration behavior in early exchanges.
- Confirm what topics should be monitored and what should be ignored.
- Keep setup short and practical.

## First Activation Flow

1. Confirm integration behavior early:
- Should this activate whenever the user asks what is trending?
- Should it run proactively on heartbeat or only when directly requested?
- Are there topics or sources this skill should never monitor?

2. Confirm monitoring scope:
- topics to watch (brands, markets, creators, products, events)
- geography and language boundaries
- source priorities, with X as optional fast-signal source

3. Confirm alert behavior:
- active hours and timezone
- strictness level (conservative, balanced, aggressive)
- message style (brief alerts or richer mini-briefs)

4. If setup context is approved, initialize local workspace:
```bash
mkdir -p ~/trending-now
touch ~/trending-now/{memory.md,topics.md,runs.md,alerts.md}
chmod 700 ~/trending-now
chmod 600 ~/trending-now/{memory.md,topics.md,runs.md,alerts.md}
```

5. If `memory.md` is empty, initialize it from `memory-template.md`.

## Integration Defaults

- Start in conservative mode unless the user requests aggressive monitoring.
- Prefer no-op output (`HEARTBEAT_OK`) over low-quality alerts.
- Require at least two independent sources before sending alerts.
- Keep focus tight: fewer topics with higher signal quality.

## What to Save

- activation and suppression preferences
- topic definitions and boundaries
- run cadence, active hours, and strictness mode
- alert outcomes and false-positive patterns

## Guardrails

- Never claim certainty without source evidence and timestamps.
- Never store secrets or private credentials in local notes.
- Never auto-post to social networks.
