# Ralph Loop Skill

## Concept & Vision
Ralph Loop is a task execution discipline that turns the AI agent into a self-running sprint machine. For every user task, the AI creates a structured persistent memory file at `/workspace/memory/ralph-loop.md` and follows it until the job is done — checking off each step, updating progress, and sending brief human-readable updates after each completed phase. The name comes from Ralph Wiggum (The Simpsons): the AI keeps going, never gives up, and iterates until it succeeds.

## Activation
Triggered when the user says:
- "Ralph loop" (any capitalization)
- "Start Ralph Loop on [task]"
- "Run it in Ralph loop"
- "Ralph loop" before any multi-step task
- Any task the user expects the AI to execute autonomously without questions

## Ralph Loop File — Structure
Location: `/workspace/memory/ralph-loop.md`

```markdown
# Ralph Loop — [Task Name]
Started: [YYYY-MM-DD HH:MM UTC] | Status: 🟡 In Progress

## Goal
[User's original request — verbatim]

## Plan
- [ ] Step 1 — [brief description of what needs doing]
- [ ] Step 2 — [brief description]
- [ ] Step 3 — [brief description]
...

## Current Work
[What I'm working on RIGHT NOW — one line]

## Progress Log
### Phase 1 — [Phase name] ✓
[Time] — [what is done]
### Phase 2 — [Phase name] ✓
[Time] — [what is done]

## Stalled / Blockers
[Empty — fill ONLY if stuck after 2 failed attempts]
```

## Ralph Loop Protocol

### PHASE 1: Init
1. Create `/workspace/memory/ralph-loop.md` with the full plan
2. Set status to `🟡 In Progress`
3. Send ONE short Telegram message — informational only, NOT asking for anything:
   > "🚀 *Task name* — Ralph Loop started. *What will be done*."

### PHASE 2: Execute — NEVER STOP

**The only acceptable reasons to pause and wait for the user:**
- Error cannot be resolved after exactly 2 attempts
- Critical information only the user has (e.g. their name, CV content, password)

**For every other situation: keep working. Do not stop. Do not ask. Do not wait.**

For each step in the plan:
1. Read `ralph-loop.md` to know current state
2. Work the step completely (write code, run commands, create files, fetch data, write content)
3. Update the file — mark the step as `[x]`
4. Add sub-steps if the work reveals micro-tasks
5. When a logical group of 2-4 steps is complete → add Progress Log entry + send ONE Telegram update:
   > "✅ *[Phase name]* — *[what is done]*. *Starting: [next phase]*."
6. If the entire task is done → go to Phase 3

### PHASE 2B: Only stop when truly stuck
Only stop here — never before:
1. Write to "Stalled / Blockers" in `ralph-loop.md`
2. Set status to `⏸️ Paused — Awaiting Input`
3. Send Telegram message:
   > "⏸️ *Ralph Loop paused* — *Step N: [exact error]. Please advise how to proceed.*"
4. **Wait for user's response. Resume only after they provide the solution.**
5. After resuming: continue from where you stopped, do not restart.

### PHASE 3: Completion
1. Set status to `✅ Done`
2. Add final Progress Log entry
3. **Delete `/workspace/memory/ralph-loop.md`**
4. Send final Telegram message:
   > "🎉 *Task name* — done. *[What was produced]*. Files: *[/workspace/path]*."
5. Ralph Loop ends.

## Ralph Loop Rules

| Rule | Strictness |
|------|-----------|
| **Never stop mid-task to ask the user something unless truly stuck** | 🚨 CRITICAL |
| Do not restart a loop once started — continue until done | 🚨 CRITICAL |
| Send Telegram updates only after completing a phase (2-4 steps) | ✅ Normal |
| If stuck after 2 failed attempts → stop, inform, wait for user | ✅ Normal |
| Update the file after every single step | ✅ Normal |
| Delete ralph-loop.md on completion | ✅ Normal |
| Break large steps into micro-steps freely | ✅ Normal |
| Telegram messages are 2-3 sentences max | ✅ Normal |

## Telegram Message Style

**After a phase (good):**
> "✅ Job boards — пронашао 12 компанија. Следећи: компаније мета."

**Bad (too long):**
> "Завршио сам истраживање job boards-ова и пронашао сам неколико занимљивих..."

**Bad (asking a question):**
> "Да ли желиш да наставим са следећим кораком?"

## Deactivating the Loop
The loop ends when all steps are checked `[x]` and the file is deleted. No lingering files.

## Ralph Loop Rules (plain English)

1. **START → FINISH. No stopping in the middle.**
2. If stuck after 2 attempts → only then stop and tell the user
3. Keep working until every step is `[x]` before sending any Telegram message
4. Telegram message = progress notification, NOT a request for permission
5. Delete the file when done
6. Never restart a loop — continue from where you left off