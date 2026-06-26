# Heartbeat Tasks — [Agent Name]

## Every Cycle
1. Read god-mode-state.json → check for error streaks
2. Read TASKS.md → pick highest-priority unblocked task
3. Execute task → log result
4. Update state → increment cycle count
5. Self-audit → one line assessment

## Every 12th Cycle (Hygiene)
- Archive stale files (> 7 days) to memory/archive/
- Clean TASKS.md completed section if > 100 lines
- Truncate log files > 1MB

## Guardrails
- Max 1 task per cycle
- 3+ consecutive errors = pause + alert
- Quiet hours: respect configured times
- Never execute red-line tasks (money, contracts) without approval
