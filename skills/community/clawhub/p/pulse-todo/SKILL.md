---
name: pulse-todo
description: "Unified task management and scheduling for AI agents. Use when: (1) a commitment is made (I'll do X, 帮你跟进, remember to), (2) checking what's pending (待办, what's left, 还有什么没做), (3) completing or dropping a task, (4) heartbeat/wake-up triggers a scheduling check, (5) a recurring or timed task needs to be created, (6) prioritizing what to do next. Triggers on: TODO, 待办, 记一下, 帮我跟进, remember, don't forget, 承诺, follow up, track this, what should I do, schedule, remind, 提醒, heartbeat check, next task. NOT for: one-off questions, things being done right now in this turn."
---

# Pulse TODO

One list. All tasks. Every wake-up, check the pulse.

## Core Principle

**Everything is a TODO.** Commitments, reminders, recurring checks, idle-time work — they're all tasks in one list. The difference is dependency and timing, not priority buckets.

## TODO.md Location

`TODO.md` in workspace root. This is the single source of truth for all pending work.

## TODO.md Format

```markdown
# TODO

## 📋 Tasks

### Do it myself
- [ ] Implement semantic search for memex #29
- [ ] Publish FlowForge v1.1.0 to npm

### Depends on human
- [ ] Cloud deployment — waiting for Luna to prepare server
- [ ] Podcast — waiting for Luna to register accounts

### Waiting on external
- [ ] Tool bug #57973 — waiting for upstream fix

## 🔄 Scheduled
- [ ] Daily review | repeat: daily 3:00 | cron: daily-review
- [ ] Morning briefing | repeat: daily 7:00 | cron: morning-briefing
- [ ] Check GitHub + inbox | repeat: every 2h | cron: check-notifications
- [ ] Remind Luna about X | once: 2026-03-31 09:45 | cron: remind-luna-x
```

### Sections

**📋 Tasks** — everything you need to do, grouped by dependency:
- **Do it myself** — you can start right now, no blockers
- **Depends on human** — need input/action from your human; nudge them or set a reminder cron
- **Waiting on external** — upstream fixes, third-party review, etc.; cron checks will catch status changes

**🔄 Scheduled** — tasks driven by cron jobs. Every `repeat:` or timed task MUST have a cron job.

### Attributes

Append after `|`:
- `repeat: <schedule>` — recurring task; reset after completion, never delete
- `once: <YYYY-MM-DD HH:MM>` — one-time scheduled task; delete or disable cron after firing
- `cron: <job-name>` — linked to an OpenClaw cron job (MUST stay in sync)

### Key Rule: repeat/timed = cron

**Never rely on the model to remember timing.** If a task has `repeat:` or a specific time, it MUST have a corresponding cron job. The cron is the enforcement mechanism. The TODO entry is the documentation.

- Adding a `repeat:` task → create cron job immediately
- Adding a timed reminder → create one-time cron job immediately
- Removing a `repeat:` task → disable/delete the cron job

### Rules

1. **Add immediately.** When a commitment is detected — from the user, from a notification, from your own work — add it before doing anything else.
2. **One source of truth.** If it's not in TODO.md, it doesn't exist. No mental notes.
3. **Done = verified done.** PR submitted ≠ done. PR merged = done.
4. **Repeat tasks reset.** After completing a `repeat:` task, uncheck it — don't delete.
5. **Stale = 3 days.** Item untouched for 3+ days? Either do it or delete it.
6. **Move between sections.** Situation changed? Move the item to the right section.
7. **Cron sync.** Adding/removing a scheduled task means updating OpenClaw cron too. Always.
8. **Only track what needs action.** "Waiting for review" on 20 PRs is not 20 TODOs — that's what notification cron is for. Track tasks where YOU need to do something.
9. **Nudge, don't wait.** "Depends on human" items should trigger you to message them, not sit there forever.

## Choosing What to Work On

When picking a task from "Do it myself", **don't just grab the easiest one.** Use this decision order:

### 1. Read your strategic goals

Check SOUL.md, MEMORY.md, or wherever your north star / strategic direction is defined. If you don't have one, ask your human: "What's the most important thing we're working toward?"

### 2. Pick by alignment, not ease

- **Directly advances the north star** → do this first, even if it's hard
- **Supports the north star indirectly** (tooling, learning, infrastructure) → second choice
- **Useful but not aligned** (quick wins, maintenance, cleanup) → only if nothing aligned is available
- **Not aligned and not urgent** → consider deleting it

### 3. Anti-pattern: path of least resistance

If you notice yourself always picking small/easy tasks and avoiding the big aligned ones, stop. That's avoidance, not productivity. The hard aligned task is almost always more valuable than three easy unaligned ones.

### 4. When everything is equally aligned

Break ties with: **momentum** (continue something in progress) > **time-sensitive** (deadline approaching) > **learning value** (builds knowledge you'll reuse).

## Scheduling (Heartbeat Wake-Up)

When triggered by heartbeat or any "what should I do next" moment:

1. Read TODO.md
2. **Do it myself** section — pick one task using the "Choosing What to Work On" logic above
3. **Depends on human** — anything stale? Nudge them
4. Nothing actionable or aligned → HEARTBEAT_OK

Heartbeat is for picking up unscheduled work. Scheduled work (notifications, reminders, recurring checks) is handled by cron — don't duplicate it in heartbeat.

## During Conversations

When talking with the user or working on tasks:

- User says "do X later" or "remember to" → add to TODO.md immediately
- User says "remind me at 3pm" → add to TODO.md AND create cron job
- Discover a new task while working → add to TODO.md
- Finish something → mark [x] or delete
- New recurring task → add to TODO.md with `repeat:` AND create cron job

## Setup

If this is your first time using pulse-todo, follow the setup guide in [setup.md](setup.md).

## What This Replaces

- Priority bucket systems (🔴🟡🔵⚪) that create scanning bottlenecks
- `repeat: every wake` items that rely on model memory for timing
- Tracking "waiting for review" as individual TODOs (use notification cron instead)
- Scattered checklists in HEARTBEAT.md
