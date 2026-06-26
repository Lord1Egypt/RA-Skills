# Long-Running Check-In Pattern

For audits and other autonomous work expected to run >30 minutes, set up a companion `/loop` that fires every 15 minutes alongside the main session. The loop is **not** firing the audit itself — the main session is doing that continuously. The loop is a **supervisor prompt** that records findings, confirms activity, and gives the long-running work a durable home.

## Why it helps

1. **Grounding.** The session can't drift silently for an hour. Every 15 minutes it has to articulate what it's found, which forces coherence.
2. **Progress preservation.** Findings land in a file every 15 minutes, not just at the end. If the session dies or compacts, the record is current.
3. **Self-termination signal.** When a check-in returns "no new findings, nothing actionable left", that's the natural stopping condition.
4. **Readable trail.** You (or a later reviewer) can read the progression of findings in chronological chunks, not as one monolithic end-of-run dump.

## When it's worth it

| Task duration | Check-in loop? |
|---------------|----------------|
| < 15 min | No — finishes before the first check-in fires |
| 15–30 min | Optional — probably not worth the setup overhead |
| 30–60 min | Recommended — catches drift, preserves partial progress |
| 1+ hours | Strongly recommended — without it, context fragility is real |

Not a replacement for the skill's own internal loop-to-exhaustion. A *complement* that adds journalling and supervision on top.

## Setup

Use `/loop` infrastructure with a 15-minute interval and a supervisor prompt. Example:

```
/loop 15m Progress check on the UX audit in progress.
1. What page or area are you currently on?
2. What findings have you recorded since the last check-in? (new bugs, friction, edge cases)
3. Any state worth noting — blocked, waiting on input, exploring a side thread?
4. Append progress to the report file. Then continue where you were.
```

Key shape: the supervisor prompt is **short, structured, asks for recording**, and explicitly says "continue where you were" so the main session doesn't restart or switch contexts.

## When to tear down

Stop the check-in loop when:

- The audit produces a "no new findings" check-in twice in a row (exhaustion)
- The audit hits the natural end of the scenario battery and fix-and-verify
- The user signals the audit is complete

`CronDelete <id>` — session-scoped, no persistence needed.

## Connection to heartbeats

Structurally identical to specialist heartbeat patterns, just at a finer scale:

- **Nightly learnings** (22:03 cron) — end-of-day consolidation, writes to journal/persona/discoveries
- **Hourly heartbeat** (every :17) — operational presence, scans channels, records signals
- **15-min check-in** (this pattern) — task-scoped supervision during long autonomous work

Same mechanism (scheduled prompt), same benefit (keep long-running work grounded and recorded), applied at three different periodicities for three different scopes.

## Gotcha

Don't mistake this for a work-doing loop. If the `/loop` fires and the main session isn't already running the audit, the check-in prompt will land in an idle session and probably start a new audit — wrong shape. This pattern only works when the main session is actively working when the check-in fires. Set the loop up *after* starting the audit, not before.
