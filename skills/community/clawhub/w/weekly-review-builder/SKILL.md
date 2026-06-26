---
name: weekly-review-builder
description: "Build a weekly review that refreshes project phase, bottleneck, and next steps. Use on: weekly schedule, after several daily loops, before resetting project priorities, after cleanup mode before full resume. Triggered when weekly review is due or when project state needs refresh."
---

# Weekly Review Builder

Compress one week's activity into an updated, honest project state. Prevent long-term drift.

## Input

Required:
- `project_card` — full project card with current state, goals, phase
- `weekly_daily_logs` — array of 5-7 daily loop logs from this week
- `weekly_decisions` — decisions made during the week
- `weekly_outputs` — tangible outputs produced this week
- `stale_tasks` — tasks that were planned but not completed

Optional:
- `blocked_tasks` — tasks that failed due to blockers

## Output Schema

```
updated_current_phase: string       # refreshed project phase
updated_current_bottleneck: string  # the one most critical blocker now
next_week_goal: string              # single clear goal for next week
next_3_actions: string[]            # top 3 actions for next week
risk_check: string                  # honest assessment of current risks
one_page_project_summary: string    # compressed project status (≤300 words)
review_confidence: "high" | "medium" | "low"
review_writeback: object           # structured record for project memory
stale_tasks_resolved: string[]      # tasks cleared this week
stale_tasks_remaining: string[]     # tasks still pending
```

## Rules

1. **Must remove outdated actions.** If a planned task wasn't touched, mark it stale and either drop or reschedule it.
2. **Must identify the single current bottleneck.** Not 3, not 5 — one.
3. **Must distinguish progress from activity.** Meetings attended ≠ progress. Code shipped ≠ impact. Be precise.
4. **Must be honest if no real progress was made.** Say so. A stagnant review is better than a flattering one.
5. **Evidence-based only.** Do not update phase or bottleneck without supporting evidence from logs.

## Review Phases

### Phase 1: Log Compression
- Read all weekly_daily_logs
- Extract: findings, decisions, completions, blockers
- Separate actual progress from busy-work

### Phase 2: Gap Analysis
- Compare weekly_outputs against weekly_daily_logs stated objectives
- Identify: what was claimed vs what was delivered
- Mark stale_tasks as resolved or remaining

### Phase 3: State Refresh
- Update current_phase based on evidence (not ambition)
- Identify current bottleneck (the one thing blocking most progress)
- Assess risk: what's the biggest threat to the project right now?

### Phase 4: Forward Planning
- Set next_week_goal (one clear goal)
- List next_3_actions (ranked by impact)
- Write one_page_project_summary for human readability

### Phase 5: Writeback
- Populate review_writeback with structured record
- Set review_confidence based on evidence quality

## Failure Handling

If evidence is insufficient (e.g., logs are missing, can't determine progress):
- Mark `review_confidence = "low"`
- Do not fabricate phase changes or bottleneck updates
- Request missing log recovery before completing review
- Write partial review with explicit gaps noted
