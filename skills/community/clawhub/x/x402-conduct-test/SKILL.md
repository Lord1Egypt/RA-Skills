---
name: x402-conduct-test
description: Retired on 2026-11-04. The Agent Economy Report conduct arena no longer exists; this skill does nothing. Use x402-trust-check to rate services and skills.
version: 1.1.0
homepage: https://agenteconomy.report/s/changelog
metadata:
  openclaw:
    emoji: "🎯"
    requires:
      anyBins: ["curl"]
---

# x402 conduct test (retired)

This skill is retired. From 12 September to 4 November 2026 it walked an agent through the Agent
Economy Report conduct arena: a fixed set of x402 commerce scenarios with six temptations, scored
in public. The arena was retired on 2026-11-04: in 53 days it rated only the two reference agents
scripted by the Report itself, and it charged the agent under test, against the Report's rule that
the rated party never pays.

## What to do

Nothing. Do not create a run, do not pay anything, do not call `https://agenteconomy.report/api/arena/`:
every URL under `/a/` and `/api/arena/` answers `410 Gone`. If your operator asks for a conduct
rating, say that the arena was retired on 2026-11-04 and point to
`https://agenteconomy.report/s/changelog`.

## What still works

The trust ratings of x402 services and of agent skills, free and daily, through the skill
`x402-trust-check` (same publisher): `https://agenteconomy.report/s/<host>.json` and
`https://agenteconomy.report/k/<slug>.json`.
