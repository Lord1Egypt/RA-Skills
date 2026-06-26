# HEARTBEAT Template - Trending Now

Use this template when configuring heartbeat-driven trend monitoring.

## Mission

Monitor selected topics across internet and social platforms and send concise alerts only when meaningful changes happen.

## Scope

| Field | Value |
|------|-------|
| Timezone | Europe/Madrid |
| Active Hours | 08:00-22:00 |
| Quiet Hours Behavior | only critical alerts |
| Cadence | every 30 minutes |

## Topic Watchlist

| Topic | Intent | Priority | Min Score | Notes |
|------|--------|----------|-----------|-------|
| Example topic | brand | high | 70 | include official aliases |
| Example topic | industry | medium | 75 | require multi-source confirmation |

## Source Mix Rules

1. Always check X for velocity and narrative emergence.
2. Validate with at least one non-X source before alerting.
3. Require recency evidence (`published_at` or equivalent timestamp).
4. Reject recycled or stale stories unless user requested historical recap.

## Scoring Model (0-100)

- volume shift: 0-25
- cross-source confirmation: 0-25
- novelty vs previous run: 0-20
- user relevance: 0-20
- urgency: 0-10

Alert if score >= topic threshold.

## Output Contract

If there is no actionable change, return exactly:
`HEARTBEAT_OK`

If there is actionable change, send one compact alert per topic with:
- What changed
- Why it matters now
- Confidence and risk
- Suggested next action

## Escalation and Cooldown

- Escalate only after threshold is met in two consecutive runs, unless urgency is critical.
- Apply cooldown of 60 minutes per topic after an alert.
- During cooldown, only escalate if score increases by at least 15 points.

## Cost Guard

- Use lightweight checks first.
- Run deep verification only when preliminary score >= 60.
- Avoid paid APIs unless user explicitly approved budget.
