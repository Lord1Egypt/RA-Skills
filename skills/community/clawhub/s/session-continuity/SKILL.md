---
name: session-continuity
description: >
  Use when a session is about to end with unfinished work, after context loss
  or compaction, after a crash, or when the user wants to resume a multi-step task.
  Saves a named checkpoint of current task state, progress, blockers, and next action
  so the next session starts from the exact resume point — not from scratch.
  Checkpoints survive session death and can stack (deep resume) for multi-day workflows.
  Builds on the WAL Protocol from proactive-agent: WAL captures per-message decisions;
  checkpoints capture task-level resume state. Activate automatically on close signals,
  high context, or user explicitly requests save/resume.
license: MIT
metadata:
  version: "1.0"
  category: productivity
  author: wangjipeng
  sources:
    - proactive-agent (WAL Protocol / Compaction Recovery patterns)
---

# Session Continuity

Save your place. Resume exactly where you left off — even days later.

---

## Core Position

Most agents lose all state when sessions die. This skill treats checkpoints as
first-class artifacts: written proactively before context is at risk, read
automatically on session start, consumed to restore full working context.

This is not "note-taking." A checkpoint is a machine-readable resume signal.
If it can't restore the exact next action with enough context to execute it,
the checkpoint is incomplete.

---

## Modes

### `/checkpoint save <name>`

Save current task state to a named checkpoint file. Use before closing any
session with unfinished work, before manual reset, approaching context limits,
or when the task spans multiple sessions.

**Trigger when:**
- About to close a session with active work
- Context >70% and work is incomplete
- Multi-day task where tomorrow you need to continue
- After a milestone, to mark the resume point

**Do not use for:** trivial one-shot tasks that complete in a single reply.

```bash
/checkpoint save meeting-prep
/checkpoint save build-login-page --task "Build login page with OAuth fallback"
/checkpoint save analyze-q1-data
```

**What gets saved:**
- Task name and one-line summary
- Current progress (what was done)
- Blockers and uncertainties
- Exact next action (the very next command or step)
- Relevant file paths and recent decisions
- Context snippets critical to continue

**Output:** Confirmation with checkpoint name and file path.

---

### `/checkpoint list`

List all available checkpoints in the workspace.

**Use when:**
- Starting a new session and want to see what was left open
- User asks "what was I working on?"
- About to start work and want to check for existing resume points

**Output:** Table of checkpoints with name, created time, task summary,
and age (how long since last saved).

---

### `/checkpoint resume <name>`

Read a checkpoint and restore the session to that resume point.

**Trigger when:**
- Session starts and a recent checkpoint exists
- User says "continue where we left off", "resume task X"
- You detect `<summary>` tag or compaction recovery signals
- User asks "where did we stop?"

**Behavior:**
1. Read the checkpoint file
2. Present the task summary and last progress
3. State the exact next action
4. Confirm before proceeding — user must approve resumption

**Output:** "Resuming: [task name]. Last progress: [summary]. Next action: [action]. Ready to continue? (yes/no)"

---

### `/checkpoint delete <name>`

Delete a named checkpoint. Use when a task is fully complete and the
checkpoint is no longer needed.

**Do not use for:** archiving — delete only when the task is truly done.

---

## Execution Steps

### For `/checkpoint save <name>`

Before writing, gather context:

1. **Read `SESSION-STATE.md`** — this is the WAL source; it contains active task state, decisions, current goal
2. **Scan conversation history** — what has been done since session start?
3. **Verify directory exists** — run `ls memory/checkpoints/`; if missing, create it
4. **Draft checkpoint content** — fill every section of the Checkpoint File Format:
   - **Task**: one-line summary (infer from SESSION-STATE.md and conversation)
   - **Progress**: specific completed items — file paths, line ranges, command outputs
   - **Next Action**: exact next step — which file to edit, which command to run
   - **Blockers**: concrete obstacles with names and error messages
   - **Key Decisions**: reasoning that led to current state, not just facts
   - **Relevant Context**: file paths, user preferences, anything not inferable from files alone
5. **Write** the completed checkpoint to `memory/checkpoints/<name>.md`
6. **Confirm** to user: checkpoint name, task, next action

**Naming rules (strict):**
- Use `kebab-case`: `build-login-page`, `q1-data-analysis`
- Must be specific enough to identify the task at a glance
- Forbidden names: `task`, `work`, `save`, `untitled`, `backup`

**If SESSION-STATE.md is empty:** derive checkpoint content entirely from the
conversation. Do not skip the checkpoint just because SESSION-STATE.md is empty.

### For `/checkpoint resume <name>`

1. **Read** `memory/checkpoints/<name>.md`
2. **Verify referenced files still exist** — check each file path in the checkpoint;
   flag any that are missing or changed as potentially stale
3. **Present** the checkpoint as a structured recovery briefing:
   ```
   📌 Resume: <task name>
   Saved: <date> (<age>)

   ✅ Progress:
   - <item 1>
   - <item 2>

   🔜 Next action: <exact command or step>

   ⚠️ Stale warnings (if any): <files that no longer exist>
   ```
4. **Wait** for user confirmation ("yes" / "no")
5. **If confirmed:** execute the next action; if stale, re-verify paths first
6. **If rejected:** delete the checkpoint and start fresh

### `/checkpoint auto` Protocol (internal)

Not a user-invokable mode. The agent scans every message for these trigger signals
and acts autonomously:

**Trigger signals (scan in priority order):**
1. **Context >70%** — call `session_status`; if usedTokens/contextWindow > 0.70, trigger
2. **Close signals** — user says "goodnight", "晚安", "logout", "exit", "明天见"
3. **Idle with work** — session idle >10 min and SESSION-STATE.md is non-empty
4. **Long operation** — about to run a command expected to take >30s

**When triggered:**
1. **Read** current SESSION-STATE.md content
2. **Write** to `memory/checkpoints/autosave.md` (overwrite previous autosave)
3. **Append** entry to `memory/checkpoints/autosave-log.md`
4. **No user-visible output** — only write to the log file

Autosave never overwrites named checkpoints. Named checkpoints are preserved
indefinitely until explicitly deleted.

---

## Do Not

- **Do not** dump raw chat transcript into a checkpoint
- **Do not** write vague progress like "worked on the task" — write exact file/state
- **Do not** mark a task complete if next action is undefined
- **Do not** save checkpoints for trivial one-shot replies
- **Do not** overwrite a named checkpoint with autosave (keep named checkpoints intact)
- **Do not** resume from checkpoint without presenting summary and confirming
- **Do not** delete a checkpoint while the task is still active
- **Do not** present a stale checkpoint as current — flag outdated file paths before resuming
- **Do not** save a checkpoint without reading SESSION-STATE.md first (or conversation if empty)
- **Do not** use forbidden names (`task`, `work`, `save`, `untitled`, `backup`)

---

## Quality Bar

A checkpoint is complete when:

- [ ] Task name and summary are clear
- [ ] Progress is specific enough to verify what was done
- [ ] Next action is executable without any additional context from the previous session
- [ ] Blockers are listed with concrete details (file paths, error messages, decisions pending)
- [ ] Relevant decisions are captured (not just facts — the reasoning that led to them)
- [ ] File paths referenced are actual paths, not generic descriptions
- [ ] Age of checkpoint is surfaced at resume (via file mtime, shown to user before confirming)

A checkpoint is incomplete if you have to ask "what were we doing?" after reading it.

---

## Good vs. Bad Examples

| Aspect | Good | Bad |
|---|---|---|
| Progress | "Wrote `src/auth.py` lines 45-120, login flow complete" | "Worked on auth" |
| Next action | "Run `pytest tests/auth_test.py` to verify login" | "Continue testing" |
| Blockers | "Git conflict in `src/main.py` lines 80-95" | "Need to fix some conflicts" |
| Context | "User prefers verbose error messages" | nothing |
| Naming | `build-login-page`, `q1-financial-analysis` | `task`, `work`, `save`, `backup` |
| State source | Read SESSION-STATE.md first, then conversation | Guessed from memory alone |
| Staleness | Verified file paths exist before presenting | Presented as if still current |

---

## Checkpoint File Format

```markdown
# Checkpoint: <name>

**Created:** YYYY-MM-DD HH:MM GMT+8
**Task:** <one-line task summary>

## Progress
<!-- What was completed — be specific -->

## Next Action
<!-- Exact next step: file, command, decision -->

## Blockers
<!-- Concrete obstacles: errors, conflicts, pending decisions -->

## Key Decisions
<!-- Reasoning that led to current state, not just facts -->

## Relevant Context
<!-- Files, paths, preferences, anything needed to continue -->

**Age:** Derived from file mtime at resume time (shown automatically by `/checkpoint list` script)
```

---

## Architecture

```
memory/
└── checkpoints/
    ├── <name>.md        # Named checkpoints (user-created)
    └── autosave.md       # Auto-created before risky close events

SESSION-STATE.md           # Active working memory (existing WAL target)
memory/working-buffer.md  # Danger zone log (existing compaction recovery)
```

**Relationship to existing files:**
- `SESSION-STATE.md` — active task state, written per WAL Protocol. **Primary source** when saving a checkpoint — read it first.
- `memory/working-buffer.md` — danger zone exchanges, consumed on recovery. Check this when checkpoint content is thin.
- `memory/checkpoints/` — durable resume artifacts, survive session death. Named checkpoints never expire unless explicitly deleted.

**How WAL and checkpoints differ:**
- WAL (SESSION-STATE.md): per-message decisions, corrections, preferences — updated on every significant human input
- Checkpoint: task-level resume state — updated at natural break points or when session ends
- WAL feeds into checkpoint: when saving, read SESSION-STATE.md to populate the checkpoint

The checkpoint system does not replace WAL; it amplifies it for multi-session durability.

---

## References

- `references/checkpoint-format.md` — full checkpoint template with examples
- `references/resume-flow.md` — step-by-step resume decision tree
- `references/auto-checkpoint-signals.md` — trigger signals for auto-checkpoint protocol (internal)