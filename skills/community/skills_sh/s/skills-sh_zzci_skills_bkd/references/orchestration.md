# BKD Orchestration Workflow

Multi-subtask dispatch through a coordinator issue that manages subtask lifecycle,
follow-up communication, and completion tracking.

## Table of Contents

- [Flow Overview](#flow-overview)
- [1. Pre-Flight](#1-pre-flight)
- [2. Create Coordinator Issue](#2-create-coordinator-issue)
- [3. Mode Selection](#3-mode-selection)
- [4. Subtask Creation and Execution](#4-subtask-creation-and-execution)
- [5. Subtask Self-Review, Fix, and Reporting](#5-subtask-self-review-fix-and-reporting)
- [6. Final Confirmation](#6-final-confirmation)
- [Status Flow](#status-flow)
- [Key Constraints](#key-constraints)


## Flow Overview

```
Check capacity -> Create coordinator issue -> Split subtasks -> Subtask execution
                                                                     |
                                                              Subtask self-review + first fix
                                                                     |
                                                              Subtask auto-enters review
                                                              + follow-up report to coordinator
                                                              (includes review results)
                                                                     |
                                                        Coordinator quality assessment (logs filter)
                                                                     |
                                                        [Worktree mode] Branch merge
                                                                     |
                                                              Build/test verification
                                                                     |
                                                        Coordinator -> review -> done (human)
```

## 1. Pre-Flight

```bash
curl -s "$BKD_URL/health" | jq
curl -s "$BKD_URL/processes/capacity" | jq
```

- `$BKD_URL` missing: ask the user for it
- `availableSlots` is 0: wait, do not force-create tasks
- Re-check capacity before each new subtask

> **Rule 10 — never inline prompts.** The `"prompt": "..."` blocks below are
> shown inline for readability only. When actually sending them, write the prompt
> to a temp file and POST via `jq`: `jq -n --rawfile prompt /tmp/bkd-prompt.txt
> '{prompt:$prompt}' > /tmp/bkd-body.json` then `curl --data-binary
> @/tmp/bkd-body.json`. Inlining free-form text into `-d '{...}'` corrupts quotes,
> `$`, backticks, and newlines. Full pattern + templated-var handling:
> `rest-api.md` → [Sending Request Bodies Safely](rest-api.md#sending-request-bodies-safely).

## 2. Create Coordinator Issue

```bash
ORCH=$(curl -s -X POST "$BKD_URL/projects/{projectId}/issues" \
  -H 'Content-Type: application/json' \
  -d '{"title":"[dispatch] task title","statusId":"todo"}')

ORCH_ID=$(echo "$ORCH" | jq -r '.data.id')
```

Send task details and subtask breakdown:

```bash
curl -s -X POST "$BKD_URL/projects/{projectId}/issues/$ORCH_ID/follow-up" \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "## Goal\n{full description}\n\n## Subtasks\n1. {subtask A title} - {acceptance criteria}\n2. {subtask B title} - {acceptance criteria}\n\n## Mode\n{Worktree mode | Simple mode}\n\n## Rules\n- Each subtask must follow-up report to this issue after completion\n- Report includes: status, changed files, key decisions, issues encountered"
  }' | jq
```

Start the coordinator:

```bash
curl -s -X PATCH "$BKD_URL/projects/{projectId}/issues/$ORCH_ID" \
  -H 'Content-Type: application/json' \
  -d '{"statusId":"working"}' | jq
```

## 3. Mode Selection

Choose before creating subtasks based on task characteristics:

| Condition | Mode | `useWorktree` |
|-----------|------|---------------|
| Many files changed, or subtasks may overlap | Worktree | `true` |
| Few files changed (<=3), no file overlap | Simple | `false` |
| Parallel development on same module | Worktree | `true` |
| Independent small fixes, config, or docs | Simple | `false` |

**Simple mode constraints:**

- Subtasks must not modify the same files
- Run subtasks serially, or ensure no file overlap when parallel
- If file conflict is discovered during execution, abort and switch to worktree mode

## 4. Subtask Creation and Execution

### 4.1 Create

**Worktree mode:**

```bash
SUB=$(curl -s -X POST "$BKD_URL/projects/{projectId}/issues" \
  -H 'Content-Type: application/json' \
  -d '{"title":"{subtask title}","statusId":"todo","useWorktree":true}')

SUB_ID=$(echo "$SUB" | jq -r '.data.id')
```

**Simple mode:**

```bash
SUB=$(curl -s -X POST "$BKD_URL/projects/{projectId}/issues" \
  -H 'Content-Type: application/json' \
  -d '{"title":"{subtask title}","statusId":"todo"}')

SUB_ID=$(echo "$SUB" | jq -r '.data.id')
```

### 4.2 Send Implementation Details

The follow-up **must** include:
- Implementation requirements and acceptance criteria
- Self-review instruction: subtask must review its own code and fix issues before reporting
- Completion report instruction with the full API path

```bash
curl -s -X POST "$BKD_URL/projects/{projectId}/issues/$SUB_ID/follow-up" \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "## Requirements\n{detailed implementation spec}\n\n## Acceptance Criteria\n- {criterion 1}\n- {criterion 2}\n\n## Before Reporting: Self-Review (mandatory)\n\nAfter implementation is complete, you MUST:\n1. Review your own code changes against the acceptance criteria\n2. Run /pma-cr on your changes\n3. Fix all P0 and P1 issues found in the first round\n4. Only report to the coordinator after self-review and first-round fixes are done\n\nInclude the review summary in your completion report.\n\n## After Self-Review: Report to Coordinator\n\nUse BKD skill (/bkd) to send a follow-up report:\n\n```bash\ncurl -s -X POST \"$BKD_URL/projects/{projectId}/issues/'"$ORCH_ID"'/follow-up\" \\\n  -H '\''Content-Type: application/json'\'' \\\n  -d '\''{\n    \"prompt\": \"Subtask {id} ({title}) complete\\nStatus: success|failure|partial\\nChanged files: file1, file2, ...\\nKey decisions: {description}\\nSelf-review: passed|{issues found and fixed}\\nRemaining issues: {if any}\\nIssues: {if any}\"\n  }'\'' | jq\n```\n\nStrict requirements:\n- Must complete self-review and first-round fixes before reporting\n- Must use the /follow-up endpoint for all inter-issue communication\n- If unsure about usage, consult BKD skill references/rest-api.md"
  }' | jq
```

### 4.3 Start Execution

```bash
# Re-check capacity
curl -s "$BKD_URL/processes/capacity" | jq '.data.availableSlots'

curl -s -X PATCH "$BKD_URL/projects/{projectId}/issues/$SUB_ID" \
  -H 'Content-Type: application/json' \
  -d '{"statusId":"working"}' | jq
```

### 4.4 Monitor

```bash
# Last 3 turns, assistant messages only
curl -s "$BKD_URL/projects/{projectId}/issues/$SUB_ID/logs/filter/types/assistant-message/turn/last3" | jq

# Or check for errors
curl -s "$BKD_URL/projects/{projectId}/issues/$SUB_ID/logs/filter/types/error-message" | jq
```

## 5. Subtask Self-Review, Fix, and Reporting

After a subtask finishes implementation:

### 5.1 Self-Review and First-Round Fix (done by the subtask)

The subtask must:

1. Run `/pma-cr` on its own changes
2. Fix all P0 and P1 issues found
3. Only then report to the coordinator

This is mandatory. The coordinator should not need to send back obvious issues.

### 5.2 Report to Coordinator

- **Status change**: BKD automatically moves completed subtasks from `working` to `review` (built-in `autoMoveToReview`). Do not manually change status.
- **Report to coordinator**: the subtask sends a follow-up including self-review results.

```bash
curl -s -X POST "$BKD_URL/projects/{projectId}/issues/$ORCH_ID/follow-up" \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "Subtask '$SUB_ID' ({title}) complete.\nStatus: success\nChanged files: src/foo.ts, src/bar.ts\nKey decisions: used XX approach\nSelf-review: passed (fixed 1 P1: missing error handling in api.ts)\nRemaining issues: none"
  }' | jq
```

### Follow-up Queue Behavior

| Coordinator status | Follow-up behavior |
|--------------------|--------------------|
| `working` and idle (between turns) | **Immediate**: triggers coordinator's next turn |
| `working` and busy (turn in progress) | **Queued**: processed after current turn ends |
| `review` | **Queued**: waits for status change |
| `todo` or `done` | **Queued**: waits for status change |

Key behaviors:

- Follow-up **actively triggers** the coordinator to continue, not a passive log
- Multiple queued follow-ups are **merged** and delivered together
- If the coordinator process has exited, follow-up **auto-starts a new process**

## 6. Final Confirmation

After all subtasks pass self-review + coordinator quality assessment (+ merge in worktree mode):

```bash
# Move coordinator to review
curl -s -X PATCH "$BKD_URL/projects/{projectId}/issues/$ORCH_ID" \
  -H 'Content-Type: application/json' \
  -d '{"statusId":"review"}' | jq
```

After human confirmation, close everything:

```bash
# Move coordinator and all subtasks to done
curl -s -X PATCH "$BKD_URL/projects/{projectId}/issues/$ORCH_ID" \
  -H 'Content-Type: application/json' \
  -d '{"statusId":"done"}' | jq

curl -s -X PATCH "$BKD_URL/projects/{projectId}/issues/$SUB_ID" \
  -H 'Content-Type: application/json' \
  -d '{"statusId":"done"}' | jq
```

## Status Flow

### Worktree Mode

```
Coordinator:  todo -> working -> (await subtasks) -> merge branches -> review -> done (human)

Subtask:      todo -> working -> self-review + fix -> review (auto) + report to coordinator
                                                        |
                                              Coordinator: logs filter assessment
                                               /       |        \
                                          red:reject  yellow:   green:pass
                                          -> working  human       |
                                                      decision  merge bkd/{issueId}
                                                                /        \
                                                            conflict    success
                                                              |           |
                                                        merge --abort   build/test verify
                                                        + escalate       /        \
                                                                      fail      pass
                                                                       |          |
                                                                revert + reject  -> done (with coordinator)
                                                                   -> working
```

### Simple Mode

```
Coordinator:  todo -> working -> (await subtasks) -> review -> done (human)

Subtask:      todo -> working -> self-review + fix -> review (auto) + report to coordinator
                                                        |
                                              Coordinator: logs filter assessment
                                               /       |        \
                                          red:reject  yellow:   green:pass
                                          -> working  human       |
                                                      decision  -> done (with coordinator)
```

## Key Constraints

1. **Follow-up only** - use `POST /projects/{pid}/issues/{iid}/follow-up` for all inter-issue communication
3. **Follow-up queue** - messages to `todo`/`done` issues are queued; `working` + idle = immediate; multiple queued messages are merged
4. **Report instructions are mandatory** - subtask follow-up details must include the full report API path to prevent agents from using wrong endpoints
5. **Capacity first** - check `/processes/capacity` before every new subtask
6. **autoMoveToReview** - BKD auto-moves completed subtasks to `review`; do not manually change status
7. **Subtask self-review is mandatory** - each subtask must run pma-cr on its own changes and fix P0/P1 issues before reporting to coordinator
8. **Pipeline assessment** - coordinator assesses each subtask immediately on completion; do not wait for all subtasks
9. **review != done** - `review` awaits human confirmation; only move to `done` after human approval
10. **Soft delete** - project and issue deletions are soft-delete by default
11. **No sleep** - never use `sleep` to wait for subtasks or long-running operations; create a cron job (`issue-follow-up`) to callback the coordinator issue on a schedule, then let the current turn end. The cron follow-up will wake the coordinator when it fires.
