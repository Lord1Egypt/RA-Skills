# Operating Rhythm

## Default Daily Rhythm

1. Before market open, compact and refresh long-term memory
2. During the day, use session journaling for plans, trades, and reflections
3. After exits, run review creation when the review window is reached
4. Periodically sync memory / vault so trade memories remain searchable
5. On the first trade day of the month, generate the behavior health report

## Scheduler Guidance

The default scheduler now distinguishes three periodic jobs:
- `memory_compaction`
- `review_cycle`
- `health_report`

There is no separate news polling or morning-brief job anymore.

## Practical Rule

When memory grows, do not rely on scrolling daily notes.
Use:
- session follow-ups for short-term context
- memory query for long-term recall
- evolution remind for bandit-prioritized reuse / risk suppression
