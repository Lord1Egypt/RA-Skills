---
name: weekly-update
version: 1.1.0
description: >
  Transform raw weekly activity notes into a clean, organized personal weekly update
  covering all active projects. Automatically reads OpenClaw session logs for the
  current week to extract activity, then combines with any manual notes provided.
  Use when the user says "generate my weekly update", "summarize my week", or provides
  a dump of what they worked on this week across any number of projects or areas.
  Output is a structured, honest summary of the week — what was done, what's in
  progress, what's next.
author: gorilli
license: Apache-2.0
tags: [productivity, weekly-update, notes, planning, journaling, builder, session-logs]
compatibility:
  tools: []
  mcp: [sessions_list, sessions_history]
changelog:
  - version: 1.1.0
    date: 2026-03-31
    notes: Auto-read OpenClaw session logs for the week to extract activity automatically
  - version: 1.0.0
    date: 2026-03-31
    notes: Initial release
---

# Weekly Update Generator

Transforms activity from OpenClaw session logs (plus any manual notes) into a clean weekly update covering all active projects.

## Step 0: Gather Activity from Session Logs

Before processing any manual input, automatically pull this week's activity from OpenClaw sessions.

1. Call `sessions_list` to get all sessions from the past 7 days. Filter by `activeMinutes` or check timestamps to scope to the current week (Monday–today).
2. For each session returned, call `sessions_history` with `includeTools: false` to get the conversation transcript.
3. Scan each transcript for:
   - Projects or codebases mentioned by name
   - Work described as completed ("shipped", "fixed", "merged", "deployed", "published", "resolved", "done")
   - Work described as in progress ("working on", "started", "investigating", "blocked on", "continuing")
   - Decisions made or conclusions reached
4. Build a raw activity list grouped by project. Ignore small talk, clarification exchanges, and meta-conversation about Claude itself.
5. If `sessions_list` or `sessions_history` are unavailable, skip this step silently and proceed with manual input only.

## Step 1: Merge with Manual Input

If the user also provided manual notes alongside the session data:
- Merge both sources, deduplicating where the same item appears in both
- Manual notes take precedence for accuracy (the user knows best what's "done" vs "in progress")
- If no manual input was provided, proceed with session-derived activity only

If neither session logs nor manual input produced any activity, ask the user to share what they worked on this week.

## Core Principles

1. **Honest over polished**: Reflect what actually happened, including pivots, blockers, and decisions. Don't inflate progress.
2. **Project-grouped**: Organize by project so it's easy to scan. Skip projects with no activity.
3. **Done vs. In Progress**: Be precise — "done" means shipped/merged/decided, "in progress" means actively being worked on.
4. **Concise**: Each item should be one tight sentence. No filler.
5. **No corporate language**: Write like a builder talking to other builders.

## Output Structure

```
📅 Week [NUMBER] — [DATE RANGE]

## What got done

**[Project Name]**
- [Completed item — be specific about what was shipped/decided/resolved]
- [...]

**[Project Name]**
- [...]

---

## In Progress

**[Project Name]**
- [What's actively being worked on and where it stands]

---

## What's Next

- [Project]: [Specific next action]
- [Project]: [Specific next action]

---

## One thought from the week
[Single honest sentence — a realization, a lesson, or something that shifted this week]
```

## Section Guidelines

### What got done
- Only include things that are actually complete (shipped, merged, decided, resolved, published)
- Lead with the outcome, not the activity: "Fixed invoice validation bug" not "Worked on invoicing"
- Group by project; skip projects with no completed items
- 2–6 items per project is typical; more means the list needs trimming

### In Progress
- Only include work that is actively running this week — not backlog
- Include enough context to know what "done" looks like for each item
- If something has been "in progress" for multiple weeks, flag it honestly

### What's Next
- One concrete action per project, not a wishlist
- Should feel like commitments, not aspirations
- Keep to the most important 3–5 items total across all projects

### One thought from the week
- Single sentence
- Something genuine — a decision made, a lesson learned, something that clarified
- Not a tagline. Not motivational. Just honest.
- Examples:
  - "Shipping something imperfect beats another week of spec refinement."
  - "The budget tracking problem is a state management problem, not a policy problem."
  - "Two open blockers on the invoicing module were the same root cause."

## Processing Activity

1. **Identify projects mentioned** — map activity to known projects
2. **Separate done from in-progress** — if unclear, default to in-progress
3. **Compress and sharpen** — rewrite each item to lead with outcome
4. **Find the week's thread** — what was the dominant theme? Use it for the closing thought
5. **Drop the noise** — admin, minor fixes, and routine work don't need to appear unless significant

## Quality Checklist

- [ ] Every "done" item is actually done, not in progress
- [ ] Each item leads with outcome, not activity
- [ ] No project appears in both "done" and "in progress" with the same item
- [ ] "What's Next" items are specific and actionable
- [ ] Closing thought is genuine, not generic
- [ ] Tone is direct — reads like a builder, not a press release
