# Claude Code WIP — TaskCreate/TodoWrite API guide

Tool usage for registering / updating / deleting tasks in the Claude Code environment.

For the workflow procedure (cleanup → per-item direction ask → execute), see [resume.md](./resume.md).

## Recording methods (at least one required)

| Method | When | Characteristics |
|--------|------|-----------------|
| **TaskCreate** | Independent tasks, dependency tracking needed | ID-based, supports `addBlockedBy` |
| **TodoWrite** | Sequential steps (3–7) | Order preserved, array-overwrite |
| **fix_plan.md / checklist.md** | Need cross-session persistence | Survives compact / session end |
| **WIP commit** | Preserve incomplete code | `WIP: <description>` tag, amend/squash later |

**On `/wip`, execute at least one of the above.** Emitting only a text summary is forbidden.

## Tool Selection

### Decision Tree

```
New work arrives
  ├─ Multiple independent tasks → TaskCreate
  │   (e.g., "modify 3 files in parallel")
  └─ Sequential steps → TodoWrite
      (e.g., "5-step deploy procedure")
```

## TaskCreate Pattern

### Register

```javascript
TaskCreate({ subject: "Modify file A" })
TaskCreate({ subject: "Modify file B" })
TaskCreate({ subject: "Run tests", addBlockedBy: ["1", "2"] })
```

### Progress

```javascript
TaskUpdate({ taskId: "1", status: "in_progress" })
// ... do work ...
TaskUpdate({ taskId: "1", status: "completed" })
```

### Delete (stale)

```javascript
TaskUpdate({ taskId: "1", status: "deleted" })
```

`status: "deleted"` permanently removes the task. Do not leave stale entries as `completed` — delete them immediately.

## TodoWrite Pattern

### ⚠️ CRITICAL: TodoWrite overwrites the entire list (HARD STOP)

**TodoWrite receives an array and overwrites the entire todo list on every call.** It is not an "update / append" tool. On each call, pass an array containing **all existing todos + any new todos**. Any todo not in the array **disappears immediately**.

**Forbidden pattern** (data loss):
```javascript
// 1st call: 8 tasks registered
TodoWrite([t1, t2, t3, t4, t5, t6, t7, t8])

// 2nd call (WRONG): only the new 2 → t1..t8 are all lost
TodoWrite([new1, new2])  // ❌ 8 tasks lost
```

**Correct pattern**:
```javascript
// Remember the array after the 1st call
existing = [t1, t2, t3, t4, t5, t6, t7, t8]

// 2nd call: pass existing + new together
TodoWrite([...existing, new1, new2])  // ✅ 10 preserved

// Even when only changing one task's status, pass the entire array again
TodoWrite([
  {...t1, status: "completed"},
  t2, t3, t4, t5, t6, t7, t8,
  new1, new2
])
```

**Self-check (every time before calling)**:
1. How many tasks (N) were registered by the previous TodoWrite call?
2. Does this call's array contain all N existing tasks + the new ones?
3. If you intend to delete any task, state it explicitly (e.g., "fix-* 4 deleted")
4. If anything is missing, **reconstruct the array now** — recovery after the call is impossible

### Register

```javascript
TodoWrite([
  { content: "Step 1 description", status: "in_progress" },
  { content: "Step 2 description", status: "pending" },
  { content: "Step 3 description", status: "pending" }
])
```

### Progress

```javascript
// Re-pass the entire array including all existing tasks
TodoWrite([
  { content: "Step 1 description", status: "completed" },
  { content: "Step 2 description", status: "in_progress" },
  { content: "Step 3 description", status: "pending" }
])
```

## Mid-session task completion (MANDATORY)

When the user signals completion mid-session (e.g., "X is done", "X was completed in another session", "I handled X"):

1. **Verify the task is done** — use `TaskGet` to inspect contents and validate related artifacts (PR merged, plan file, issue closed, etc.)
2. **If verified, immediately call `TaskUpdate(status: "deleted")`**
3. **Handle any other instructions in the same message** — do not handle "done" but ignore the rest of the message

**Forbidden patterns**:
- User says "done" but you neither verify nor delete, and only answer some other part of the message
- Treating "done" as mere information without changing task state

## AskUserQuestion — per-item direction ask

The Claude environment implementation of resume.md Step 2. **One question per task, split across the `questions` array** (max 4 entries).

### Do & Don't — AskUserQuestion format

| # | Don't | Do |
|---|-------|-----|
| 1 | List 4 tasks as options of a single question ("Delete all / Keep all / ...") | Split into `questions` array with one question per task (max 4) |
| 2 | Use `multiSelect: true` to bundle the task list under one question | Each question independently decides one task's direction (proceed / hold / delete) |
| 3 | Compress 5+ remaining tasks into a single question | Ask the top 4 by priority in the `questions` array, report the rest as "deferred" |

### Correct pattern (4 tasks — full use of the `questions` array)

```javascript
// questions array up to 4 — one question per task, independent decision
AskUserQuestion({
  questions: [
    {
      question: "#12 Add API endpoint — direction?",
      header: "#12",
      options: [
        { label: "Proceed", description: "Implement as currently defined" },
        { label: "Split", description: "Separate lookup vs update into distinct tasks" },
        { label: "Delete", description: "No longer needed" },
      ], multiSelect: false
    },
    {
      question: "#13 Strengthen test coverage — direction?",
      header: "#13",
      options: [
        { label: "Proceed", description: "Write missing cases" },
        { label: "Hold", description: "After #12 implementation" },
      ], multiSelect: false
    },
    // ... one question per task, max 4
  ]
})
```

### 5 or more tasks

The `questions` array is capped at 4 → ask the top 4 by priority. Report the rest as "deferred / external wait" (re-ask on the next `/wip`).

### Auto-proceed — verification/lookup tasks need no ask

If a task subject contains any of the following keywords, run the action immediately without asking and reflect the result:

| Keyword | Auto-run command |
|---------|-----------------|
| `CI result`, `CI check`, `check` | `gh pr checks` / `gh run view` |
| `PR state`, `merge check` | `gh pr view --json state` |
| `deploy check`, `deploy result` | `curl` / `ssh` checks |
| `test result` | `gh run view` / log inspection |

Where to reflect the result:
1. **TaskUpdate** — add a result summary to the task subject, or mark `completed`
2. **Checklist file** — tick the matching `[x]` in `checklist.md` / `fix_plan.md` with the result noted

**Ask when the criterion is ambiguous** — any task that includes actions beyond "check" (edit, delete, merge, etc.) is not eligible for auto-run.

## PR merge option verification (HARD STOP — multiple recurrences)

In resume Step 2, before annotating an option description with a PR number plus "merge", "Review ✅", or "CI ✅", verify the four merge conditions against primary data (the `gh` API). Do not quote a context summary / memory / prior-session record verbatim.

### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Copy a "Review ✅" claim from the context summary into the option description | Verify the AI Review Summary comment directly: `gh api repos/{owner}/{repo}/issues/<N>/comments --jq '.[] \| select(.body \| startswith("## AI Review Summary"))'` |
| 2 | Quote "Test Plan 8/8 ✅" from fix_plan / memory | Measure directly with `gh pr view <N> --json body` (count `[ ]` / `[x]` in the body) |
| 3 | Interpret a bot's auto-generated comment (CodeRabbit summary) as "AI Review Summary posted" | Separately confirm the user-authored `## AI Review Summary` header comment. Bot auto-comments do not satisfy this condition |
| 4 | Keep "merge" in the AskUserQuestion option while papering over an unmet condition in the description | Remove "merge" from the option itself → only present options that resolve the unmet condition (e.g., "Post consolidate first then revisit", "Verify Test Plan") |

### 4-condition measurement procedure (every time an option for a PR is on the table)

```bash
# 1. CI
gh pr checks <N> --json state,conclusion

# 2. Test Plan
gh pr view <N> --json body | jq -r .body | grep -cE '^\s*-\s*\[[ x]\]'

# 3. AI Review Summary comment posted
gh api repos/{owner}/{repo}/issues/<N>/comments --jq '.[] | select(.body | startswith("## AI Review Summary"))'

# 4. Mergeable
gh pr view <N> --json mergeable,mergeStateStatus
```

All four OK → the "Proceed to merge" option may be included, with the four-condition evidence cited in the description (follow `merge.md` formatting).
Any one unmet → drop the "merge" option and present unmet-condition-resolution options instead.

## Bot comment timing parsing (HARD STOP)

In resume Step 2, before annotating a PR option description with "walkthrough pending", "rate-limited", or "waiting", **Read the bot comment body directly and extract the timing information (wait time, retry-after, unlock time)**. Do not infer from comment metadata alone (user, length, first 80 chars).

### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | `user=coderabbitai[bot]` + first 80 chars contain "Rate limit" → conclude "walkthrough pending, auto-defer" | Read the entire body → grep "wait **N minutes M seconds**" → compute `created_at + wait` → report the unlock time |
| 2 | Defer indefinitely under a generic "rate-limited" label | State the explicit unlock time in the option description: "rate limit clears: HH:MM (UTC)" or "already cleared (N min ago)" |
| 3 | Mark "waiting" even though the unlock time has already passed | If unlock < now, the option must include an action (e.g., "trigger `@coderabbitai review`", "re-request via a new commit push") |
| 4 | Dismiss CodeRabbit / Dependabot / Actions retry-after bot comments as "irrelevant" | Bot comments with timing/numeric data are primary sources. Apply common.md's "don't infer the body — read it" rule |

### Timing extraction procedure

```bash
# 1. Get the comment body + creation time
gh api repos/{owner}/{repo}/issues/<N>/comments > /tmp/comments.json
jq '.[N].body' /tmp/comments.json     # body (N = the bot comment index)
jq '.[N].created_at' /tmp/comments.json  # creation time, ISO8601

# 2. Grep for wait-time patterns in the body
#    - "wait **N minutes M seconds**"
#    - "Please wait N seconds"
#    - "Retry-After: N"
#    - "Try again at HH:MM"

# 3. unlock = created_at + wait time (UTC)

# 4. Compare with the current UTC
date -u +"%Y-%m-%dT%H:%M:%SZ"
```

### Option description format

| State | description format |
|-------|--------------------|
| Cleared | `"rate limit already cleared (N min ago). Can trigger @coderabbitai review"` |
| Waiting (short — within 30 min) | `"rate limit clears at: HH:MM UTC (in N min)"` |
| Waiting (long — 30+ min) | `"rate limit clears at: HH:MM UTC (in N hours). Prefer other work first"` |
| No timing in the body | `"walkthrough pending (unlock time unknown — body parsing failed)"` (explicit) |

## Copilot Rate Limit Sharing (HARD STOP)

When a Copilot rate limit is detected (e.g. from GitHub Actions run failures containing "limit to reset in N hours M minutes"), the reset timestamp must be written to the shared cache to prevent other sessions from running blocked Copilot requests:

1. **Calculate the reset timestamp** in ISO 8601 UTC format.
2. **Write the reset timestamp** to `~/.claude/copilot-rate-limit.json`:
   ```bash
   echo '{"reset_at": "YYYY-MM-DDTHH:MM:SSZ"}' > ~/.claude/copilot-rate-limit.json
   ```
3. The `PreToolUse: Bash` hook (`~/.claude/hooks/block-copilot-rate-limit.sh`) intercepts `copilot-pull-request-reviewer` commands when the cache is present. **The hook MUST verify `reset_at >= now` before blocking** — a stale cache (timestamp already in the past) must not keep blocking. Hook contract (mandatory in the implementation):

   ```bash
   # ~/.claude/hooks/block-copilot-rate-limit.sh (pseudo)
   CACHE=~/.claude/copilot-rate-limit.json
   [[ -f "$CACHE" ]] || exit 0  # no cache → allow
   RESET=$(jq -r .reset_at "$CACHE")
   NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
   if [[ "$RESET" < "$NOW" ]]; then
     rm -f "$CACHE"     # auto-cleanup stale cache
     exit 0             # allow — limit has cleared
   fi
   # reset_at > now → still rate-limited
   echo "Copilot rate limit active until $RESET" >&2
   exit 2
   ```

4. **Cleanup responsibility**: the hook (step 3) is the primary cleanup path. As a backup, any session that detects `reset_at < now` while reading the file (e.g., during a `/wip` lookup or consolidate Step 2.4) should also `rm -f ~/.claude/copilot-rate-limit.json` so the next Copilot invocation is not gated by stale data.

## Compact recovery

After a compact, restore the prior work state (a precursor to resume.md Step 1).

### Procedure

1. **Detect the work source**:
   - Find referenced files in the compact summary (`fix_plan.md`, `plan.md`, `research.md`, etc.)
   - Check whether `.ralph/fix_plan.md` exists (`ls .ralph/fix_plan.md`)
   - If the summary contains keywords like "fix_plan", "plan", or "in order", that file is the work source
   - **If a work source exists**: Read the file and identify `[x]` (done) vs `[ ]` (not done) → extract the next not-done items
   - **If no work source**: extract from the compact summary

2. **Emit a summary of prior work**: combine the file's done/not-done state with the compact-summary progress and present it to the user

3. **AskUserQuestion(multiSelect) for restore selection**: present the not-done list as choices

4. **Register via TodoWrite/TaskCreate**: register the user's selection → after registration **enter resume Step 2** (per-item direction ask)

### Example

```text
# 1. Summary output
"Work in progress before compact:"
- [x] Implement API endpoint
- [/] Write tests
- [ ] Create PR

# 2. AskUserQuestion (multiSelect: true)
"Select items to resume"
→ User selects: Write tests, Create PR

# 3. Re-register only the selected items via TodoWrite
TodoWrite([
  { content: "Write tests", status: "in_progress" },
  { content: "Create PR", status: "pending" }
])
```

### Skip conditions

- Skip if the compact summary contains no in-progress work
- Skip if the user chooses "Start fresh"
