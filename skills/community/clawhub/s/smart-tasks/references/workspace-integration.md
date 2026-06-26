# Workspace Integration Guide

This skill does NOT modify workspace files outside its own directory.
Apply these changes manually with user approval during setup.

## AGENTS.md Changes

### Add INDEX.md to Session Startup

```diff
 ## Session Startup
 
 Before doing anything else:
 
 1. Read `SOUL.md` — this is who you are
 2. Read `USER.md` — this is who you're helping
 3. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent context
-4. **If in MAIN SESSION** (direct chat with your human): Also read `MEMORY.md`
+4. Read `tasks/INDEX.md` — current task status at a glance
+5. **If in MAIN SESSION** (direct chat with your human): Also read `MEMORY.md`
 
 Don't ask permission. Just do it.
```

### Add Tasks Section (after Memory section)

```diff
 Use `~/proactivity/` for proactive operating state.
 
+## Tasks
+
+`tasks/` is the task management system.
+
+- **INDEX.md**: Active task summary. Read every session startup.
+- **active/**: Individual task files. Read only when detail is needed.
+- **done/**: Completed tasks (30-day retention). Check during weekly review.
+- **archive/**: Long-term storage. Access only via explicit search.
+
+### Task Operating Rules
+
+- When the user mentions todos/deadlines, propose creating a task.
+- Always update both the task file AND INDEX.md together.
+- If INDEX.md can answer the question, don't read individual files.
+- Fill Agent Notes with workspace cross-references at task creation.
+- Categories are user-defined — never assume a fixed set.
+
 Before non-trivial work: read `~/self-improving/memory.md`...
```

## SOUL.md Changes

### Extend Proactivity Section

```diff
 ## Proactivity
 
 **Proactivity**
 Being proactive is part of the job, not an extra.
 Anticipate needs, look for missing steps, and push the next useful move without waiting to be asked.
+When the user mentions deadlines, tasks, or things to do, naturally offer to track them.
+When reminding about tasks, include relevant context — not just the deadline.
+Prioritize suggestions based on deadline urgency, estimated effort, and importance.
 Use reverse prompting when a suggestion, draft, check, or option would genuinely help.
```

## HEARTBEAT.md Changes

### Add Task Check Section

```diff
 ## Proactivity Check
 
 ...existing content...
+
+## Task Check
+
+- Read `tasks/INDEX.md` for current overview
+- Check for overdue tasks (due < today)
+- Check for tasks due within 24 hours
+- If urgent task found AND not already alerted today:
+  - Send brief, actionable reminder
+  - Read task detail file if helpful context exists
+- If nothing urgent → skip silently (no noise)
+- Log alert to `memory/YYYY-MM-DD.md` to avoid duplicate alerts
```

## Application Instructions

1. Show these diffs to the user and get approval.
2. Apply changes one file at a time.
3. Verify each file still parses correctly after editing.
4. The skill itself never auto-applies these changes.
