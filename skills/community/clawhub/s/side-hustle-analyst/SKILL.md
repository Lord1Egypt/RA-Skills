---
name: side-hustle-analyst
description: Runs structured day-by-day execution for AI agent side hustles. Use when: executing the Agent Side Hustle School workflow, tracking experiment progress, or maintaining persistent state across a 28-day hustle cycle. NOT for: generic productivity advice, long-term business strategy, or non-AI/agent business ideas.
---

# Side Hustle Analyst

**Operational mode:** Execution tracker. Maintains state across the hustle lifecycle and drives sequential, blocking progress.

## What it does
1. Loads current day/phase state from course-state.json
2. Executes today's step in the 6-phase workflow:
   - Phase 1 (Days 1-5): Idea intake and ranking
   - Phase 2 (Days 6-12): Minimum viable test execution
   - Phase 3 (Days 13-17): Offer construction
   - Phase 4 (Days 18-21): Traffic drives
   - Phase 5 (Days 22-25): Conversion optimization
   - Phase 6 (Days 26-28): Documentation and next cycle
3. Logs OUTCOME / SCORE / WHY after every meaningful action
4. Advances phase only when "done when" criteria are met
5. Flags blockers that persist >48 hours

## When to use
- Daily execution of the hustle engine workflow
- After selecting an experiment, for Day 2+ execution
- When restarting after a gap and needing to know current state

## State management
- Reads: state/course-state.json (canonical position)
- Writes: output/experiment-log/ and output/daily-summaries/
- Maintains: outcome_log array with scores per action

## Approval gates
Requires operator approval before:
- Experiment selection (presents exactly 3 options)
- Experiment lock-in (Day 5 confirmation)
- Offer definition and pricing (Day 13)
- Any spend above $0

## Output naming
- Daily summaries: output/daily-summaries/YYYY-MM-DD-day-N.md
- Experiment logs: output/experiment-log/day-NN-name.md

## Aesthetic
Dark mode. Charcoal (#1a1a1a) primary. Electric purple accent (#9b59b6). Monospace details.
