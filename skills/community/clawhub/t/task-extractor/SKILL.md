---
name: task-extractor
version: 1.0.0
description: Extract, track, and verify completion of multiple tasks from a single user message. Use when any message contains 3+ actionable items, a prompt dump with mixed instructions, or a compound request. Prevents task drop by saving to TASK_QUEUE.md before executing. Reports completion status per item.
---

# Task Extractor

Parse multi-task messages → numbered queue → execute sequentially → verify each → report.

## Activation

Trigger on ANY user message containing 3+ distinct actionable items. Signs:
- Multiple sentences starting with verbs ("build", "fix", "send", "check", "add", "research")
- Comma-separated or period-separated instructions
- Mixed topics in one paragraph
- "also", "and then", "plus", "oh and", "one more thing"

If uncertain whether to activate: activate. False positives (structuring a 2-item request) cost nothing. False negatives (dropping task #7 of 12) cost trust.

## Step 1: EXTRACT (before any execution)

Parse the message into individual tasks. Each task gets:
- **Number** (sequential)
- **Summary** (one line, imperative verb)
- **Type**: BUILD | FIX | RESEARCH | SEND | DEPLOY | CONFIG | OTHER
- **Estimated effort**: QUICK (< 5 min) | MEDIUM (5-30 min) | HEAVY (30+ min / sub-agent)

Write to `workspace/TASK_QUEUE.md`:

```markdown
# TASK_QUEUE — [date] [time]
# Source: [channel]
# Total: [N]
# Status: IN PROGRESS

| # | Task | Type | Effort | Status | Artifact |
|---|------|------|--------|--------|----------|
| 1 | [summary] | BUILD | HEAVY | ⏳ | |
| 2 | [summary] | FIX | QUICK | ⏳ | |
| 3 | [summary] | SEND | QUICK | ⏳ | |
...
```

## Step 2: RECEIPT

Reply to the user with the extracted checklist BEFORE starting work:

```
📋 Extracted [N] tasks from your message:

1. ⏳ [task summary]
2. ⏳ [task summary]
3. ⏳ [task summary]
...

Starting now. I'll check each off as I go.
```

Do NOT ask "is this right?" unless genuinely ambiguous. Convert ambiguity into a task and execute. Ryan's rule: don't interrogate, just do.

## Step 3: EXECUTE

Work through tasks in dependency order (not necessarily numerical order):
- Independent QUICK tasks first (batch them in parallel tool calls)
- MEDIUM tasks next
- HEAVY tasks: spawn sub-agents with clear scope

For each completed task, update TASK_QUEUE.md:
- `⏳` → `✅` (done) or `❌` (failed) or `⚠️` (partial) or `🔄` (spawned sub-agent)
- Fill in the Artifact column (file path, URL, commit hash, or "n/a")

## Step 4: RECONCILE

After all tasks are attempted (or sub-agents spawned), reply with the final checklist:

```
📋 Task Report ([completed]/[total]):

1. ✅ [task] → [artifact]
2. ✅ [task] → [artifact]
3. 🔄 [task] → sub-agent running, will announce when done
4. ❌ [task] → [reason for failure]
5. ⚠️ [task] → [what was done, what's left]
```

## Step 5: VERIFY (on sub-agent completion)

When a sub-agent announces completion:
- Update TASK_QUEUE.md
- If ALL tasks are now ✅/❌, send final summary
- If tasks remain ⏳, continue working

## Rules

1. **NEVER skip the extract step.** Even if the answer seems obvious. The extract step IS the safety net.
2. **NEVER mark a task ✅ without evidence.** Evidence = file exists, command succeeded, API returned 200, deploy URL works.
3. **If a task fails, say WHY.** Not just ❌ — include the error, the blocker, or what's needed.
4. **Sub-agent tasks get 🔄 until completion event arrives.** Don't mark them ✅ optimistically.
5. **TASK_QUEUE.md is the source of truth.** If context overflows, re-read it. If a session restarts, re-read it.
6. **One TASK_QUEUE at a time.** If a new multi-task message arrives while one is active, append to the existing queue (renumber).
7. **Checkpoint at 5 completed tasks.** Update the user with progress so far.

## Edge Cases

### "Do X and also Y but wait on Z"
- X and Y get ⏳, Z gets 🕐 (blocked — note the dependency)

### Sub-agent timeout
- Mark as ⚠️, note what was attempted, offer to retry or take over manually

### User changes mind mid-execution
- Update TASK_QUEUE.md, cross out cancelled tasks with ~~strikethrough~~, continue with remaining

### Overlapping tasks
- If task 3 and task 7 are really the same thing, merge them. Note in Artifact: "merged with #3"

## Anti-patterns

- ❌ Reading the message, immediately jumping into task #1 without extracting all tasks
- ❌ Marking a sub-agent task ✅ before the completion event
- ❌ Saying "I'll get to that" and then forgetting
- ❌ Only reporting on the tasks you completed, silently dropping the ones you didn't
- ❌ Asking "which one should I do first?" — just prioritize by dependency + effort and go
