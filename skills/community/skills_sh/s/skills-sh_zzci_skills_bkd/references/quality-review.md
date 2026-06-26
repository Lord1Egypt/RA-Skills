# BKD Quality Assessment and Code Review

Two-tier review: subtasks self-review before reporting, then the coordinator
runs logs filter assessment. Assess immediately on each subtask completion;
do not wait for all subtasks to finish.

## Table of Contents

- [Pipeline Order](#pipeline-order)
- [1. Logs Filter Assessment](#1-logs-filter-assessment)
- [2. Subtask Self-Review (done by the subtask, not the coordinator)](#2-subtask-self-review-done-by-the-subtask-not-the-coordinator)
- [Key Rules](#key-rules)


## Pipeline Order

```
Subtask: implementation -> self-review (pma-cr) -> first-round fix -> report to coordinator
Coordinator: receive report -> Logs Filter assessment -> next phase (merge or done)
```

Subtasks own their code review. The coordinator only validates execution quality
via logs filter.

## 1. Logs Filter Assessment

Use the filter API to pull specific log slices. Do not fetch full logs.

```
GET /projects/{projectId}/issues/{issueId}/logs/filter/{filter_path}
```

See `references/rest-api.md` for filter path syntax and available entry types.

### 1.1 Check Error Signals

```bash
curl -s "$BKD_URL/projects/{pid}/issues/{iid}/logs/filter/types/error-message" | jq
```

- Error messages present = yellow signal; check subsequent steps for recovery

### 1.2 Check Final Output

```bash
curl -s "$BKD_URL/projects/{pid}/issues/{iid}/logs/filter/types/assistant-message/turn/last" | jq
```

- Output does not match task goal = red
- Contains "failed", "unable to complete", "gave up" = red

### 1.3 Check Tool Call Patterns

```bash
curl -s "$BKD_URL/projects/{pid}/issues/{iid}/logs/filter/types/tool-use/turn/last3" | jq
```

- Same tool + similar args >= 3 consecutive times = red (blind retry)
- `rm -rf`, `--force`, `git reset --hard` without reasonable context = red
- `file-edit` kind touching out-of-scope files = yellow

### 1.4 Check Execution Scale

```bash
curl -s "$BKD_URL/projects/{pid}/issues/{iid}/logs/filter/types/user-message?limit=200" \
  | jq '.data | length'
```

- Total turns exceeding 2x estimated complexity = yellow

### 1.5 Signal Classification

| Signal | Condition | Action |
|--------|-----------|--------|
| Red | Final output misses goal / blind retry / dangerous operations | Follow-up subtask with issue details, move back to `working` for rework |
| Yellow | Errors recovered / excessive turns / out-of-scope file changes | Follow-up coordinator with report, wait for human decision |
| Green | No red or yellow signals | Proceed to next phase (merge or done) |

### 1.6 Result Handling

**Green (pass):** Proceed directly to next phase (merge or done). Do not follow-up the coordinator issue — the coordinator is already running this assessment inline, so sending a follow-up to itself would cause self-activation loops.

**Red (rework):** (Rule 10 — the prompt is shown inline for readability; send it
via a temp file: `jq -n --rawfile prompt /tmp/bkd-prompt.txt '{prompt:$prompt}' >
/tmp/bkd-body.json`, then `curl --data-binary @/tmp/bkd-body.json`. See
`rest-api.md` → [Sending Request Bodies Safely](rest-api.md#sending-request-bodies-safely).)

```bash
curl -s -X POST "$BKD_URL/projects/{pid}/issues/$SUB_ID/follow-up" \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "Quality assessment failed.\nRed signal: turn/last output is \"unable to install dependencies\", task incomplete.\nRequired: investigate root cause and re-execute. Do not blindly retry."
  }' | jq

curl -s -X PATCH "$BKD_URL/projects/{pid}/issues/$SUB_ID" \
  -H 'Content-Type: application/json' \
  -d '{"statusId":"working"}' | jq
```

## 2. Subtask Self-Review (done by the subtask, not the coordinator)

Each subtask is responsible for reviewing and fixing its own code before reporting.

### 2.1 Subtask Responsibilities

1. Run `/pma-cr` on its own changes after implementation
2. Fix all P0 and P1 issues found
3. Include self-review summary in the completion report to the coordinator

### 2.2 Review Dimensions (by priority)

1. Correctness and regressions
2. Security and trust boundaries
3. Data integrity and error handling
4. Concurrency, cancellation, and resource lifecycle
5. Performance and scalability
6. Maintainability and testing

### 2.3 Coordinator Escalation

If the coordinator's logs filter assessment finds issues that the subtask's self-review missed,
send the subtask back for rework:

```bash
curl -s -X POST "$BKD_URL/projects/{pid}/issues/$SUB_ID/follow-up" \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "Logs filter found issues missed by self-review.\n- Red signal: blind retry pattern in turn/last3\n- Out-of-scope file changes detected\nRequired: fix issues, re-run self-review, and report again."
  }' | jq

curl -s -X PATCH "$BKD_URL/projects/{pid}/issues/$SUB_ID" \
  -H 'Content-Type: application/json' \
  -d '{"statusId":"working"}' | jq
```

After rework, the subtask re-enters the pipeline: self-review -> report -> coordinator assessment.

## Key Rules

- **Subtasks own their code review** - each subtask runs pma-cr and fixes P0/P1 before reporting
- **Coordinator only runs logs filter** - the coordinator validates execution quality, not code quality
- **pma-cr reviews incremental changes only** - do not chase historical debt
- **Pipeline processing** - assess each subtask as soon as it completes; do not batch
- **Both tiers must pass before merge** - subtask self-review + coordinator logs filter assessment
