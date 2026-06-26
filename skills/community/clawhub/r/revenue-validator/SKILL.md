---
name: revenue-validator
description: Validates side hustle ideas against real market demand. Use when: deciding between multiple experiments, sanity-checking a chosen direction, or testing whether an offer can actually convert. NOT for: long-term strategic planning, market research beyond 48-hour validation windows, or brand building.
---

# Revenue Validator

**Operational mode:** Validation engine. Takes an idea and runs it through a structured demand test — fast.

## What it does
1. Takes a named experiment or offer as input
2. Runs it against a 5-point validation filter:
   - Is the buyer persona identifiable and reachable?
   - Is the problem painful enough to pay to solve?
   - Is the solution deliverable in <48h for first signal?
   - Is there existing infrastructure to execute without cold start?
   - Does it fit the operator's ecosystem (AI tools, agents, automation)?
3. Outputs: pass/fail on each point + overall score + recommended MVT
4. If failing: identifies the single biggest blocker and suggests a pivot direction

## When to use
- After selecting an experiment, before committing full time
- When stuck on whether an idea is worth pursuing
- Mid-experiment when signal is ambiguous

## Constraints
- Validation window: 48 hours maximum
- Metrics that count as signal: profile views, bookmarks, DMs, email subs, clicks, sales
- Metrics that do NOT count: likes, followers, compliments, "this is interesting"
- Rejects ideas that require spend before first signal

## Output format
- Validation scorecard (5 points)
- Overall score (1-10)
- Single biggest blocker (if failing)
- Recommended MVT adjustment
- 24-hour check-in metric

## Aesthetic
Dark mode. Charcoal (#1a1a1a) primary. Emerald green accent (#2ecc71). Monospace details.
