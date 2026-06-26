# Research Protocol - Trending Now

## Objective

Produce trend alerts that are fresh, verifiable, and relevant to user priorities.

## Cycle Workflow

1. Pull the current topic list and thresholds.
2. Run quick discovery checks for each topic.
3. Collect candidate signals with links and timestamps.
4. Cross-validate on at least two source families.
5. Score candidates using the shared model.
6. Decide: alert, watchlist, or no-op (`HEARTBEAT_OK`).

## Source Family Requirements

- Fast signal: X or equivalent high-velocity channel.
- Community signal: Reddit, forums, or specialized communities.
- Validation signal: publisher coverage or query trend tools.

At least two families must agree before alerting.

## Freshness Rules

- Mark each item with UTC timestamp.
- Prefer items <= 24 hours old.
- If all items are stale, do not alert unless the user asked for retrospective analysis.

## Evidence Quality Rules

- Keep direct source links.
- Separate observed fact from interpretation.
- Include one disconfirming check before final alert.
- Avoid claims based only on repost loops.

## Output Decision Tree

- score below threshold -> move to watchlist
- score meets threshold once -> monitor next cycle
- score meets threshold with confirmation -> send alert
- no meaningful change -> return `HEARTBEAT_OK`

## Reliability Checklist

- topic scope respected
- source diversity satisfied
- freshness window satisfied
- confidence stated with uncertainty
- one clear next action included
