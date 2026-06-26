---
name: bkd
description: Operate a BKD kanban board over its REST API. Use when the user wants to manage BKD projects, issue execution workflows, cron jobs, or execution capacity through a reachable BKD server.
---

# BKD

Operate BKD by sending HTTP requests to `$BKD_URL`, which must point at the BKD
API root such as `http://host:port/api`.

Keep this entry file small. Load only the references needed for the current turn.

## Always-On Rules

1. Confirm `$BKD_URL` before making any request. If it is missing, ask for it.
2. Prefer `curl -s` piped to `jq` so results are easy to inspect.
3. Use the safe issue execution flow: create in `todo` -> follow-up -> move to `working`.
4. Check `/processes/capacity` before starting any execution.
5. Move finished work to `review`, not `done`. Use `done` only after human confirmation.
6. Use follow-up for all inter-issue communication.
7. Treat project and issue deletions as soft-delete unless the API says otherwise.
8. Expect all responses to use `{ success, data }` or `{ success, error }`.
9. Never use `sleep` to wait for subtasks or long-running operations. Create a cron job (`issue-follow-up`) to callback the coordinator issue on a schedule, then let the current turn end.
10. Never inline free-form text (prompts, descriptions) into `-d '{...}'` — quotes, `$`, backticks, and newlines get mangled by shell + JSON escaping. Write the text to a temp file, build the body with `jq`, and POST it with `--data-binary @file`. See `references/rest-api.md` → [Sending Request Bodies Safely](references/rest-api.md#sending-request-bodies-safely). Fixed-value bodies (e.g. `{"statusId":"working"}`) are safe to inline.

## Core Workflow

### Three-Tier Coordination Shortcut

When the user says a short phrase such as "use bkd to start coordination" or
"start BKD L1", treat the current agent session as L1 and load
`references/three-tier-coordination.md`. The user does not need to repeat the
full L1/L2/L3 rules in the prompt.

### Single Issue Execution

```bash
# 1. Create issue
ISSUE=$(curl -s -X POST "$BKD_URL/projects/{projectId}/issues" \
  -H 'Content-Type: application/json' \
  -d '{"title":"short title","statusId":"todo"}')
ISSUE_ID=$(echo "$ISSUE" | jq -r '.data.id')

# 2. Send details — write the prompt to a file, never inline (Rule 10)
cat > /tmp/bkd-prompt.txt <<'PROMPT'
full implementation details
PROMPT
jq -n --rawfile prompt /tmp/bkd-prompt.txt '{prompt: $prompt}' > /tmp/bkd-body.json
curl -s -X POST "$BKD_URL/projects/{projectId}/issues/$ISSUE_ID/follow-up" \
  -H 'Content-Type: application/json' \
  --data-binary @/tmp/bkd-body.json | jq

# 3. Start execution
curl -s -X PATCH "$BKD_URL/projects/{projectId}/issues/$ISSUE_ID" \
  -H 'Content-Type: application/json' \
  -d '{"statusId":"working"}' | jq
```

### Quick Operations

```bash
# Health check
curl -s "$BKD_URL/health" | jq

# Execution capacity
curl -s "$BKD_URL/processes/capacity" | jq

# Monitor logs (last 3 turns, assistant messages only)
curl -s "$BKD_URL/projects/{projectId}/issues/{issueId}/logs/filter/types/assistant-message/turn/last3" | jq

# Cron jobs
curl -s "$BKD_URL/cron/actions" | jq
curl -s "$BKD_URL/cron" | jq
```

## Reference Packs

Load only what the current task needs:

- `references/rest-api.md`
  Use for exact BKD routes, payload shapes, query params, and field lists.
- `references/orchestration.md`
  Use for multi-subtask dispatch workflows, mode selection (worktree vs simple), subtask creation and monitoring, and follow-up communication patterns.
- `references/quality-review.md`
  Use for subtask self-review responsibilities, coordinator logs filter assessment, and signal classification.
- `references/merge-strategy.md`
  Use for worktree branch merging, conflict resolution, post-merge verification, and cleanup after subtasks complete in worktree mode.
- `references/three-tier-coordination.md`
  Use for the L1/L2/L3 cron-driven autonomous coordination pattern: user-facing agent session (L1) reports to user only, BKD scheduling issue (L2) owns DAG decomposition + dispatch via 30-min self cron, short-lived subtasks (L3). Engine-agnostic — L1/L2/L3 may each run on different engines (Claude Code, Codex, etc.). Pick over `orchestration.md` when the campaign spans sessions/hours, needs capacity-aware DAG scheduling, and must run sleep-free.

## Quick Routing

Choose references by intent:

- Single issue CRUD, cron jobs, or API details: load `references/rest-api.md`.
- Short activation phrases like "use bkd to start coordination" or "start BKD L1": load `references/three-tier-coordination.md`.
- Multi-subtask dispatch or orchestration: load `references/orchestration.md`.
- Subtask quality assessment or code review: load `references/quality-review.md`.
- Branch merging after worktree subtasks: load `references/merge-strategy.md`.
- Long-running, cron-driven L1/L2/L3 autonomous coordination across heterogeneous engines: load `references/three-tier-coordination.md` (use instead of `orchestration.md` when the user wants the user-facing agent to only talk to the user while BKD self-drives dispatch via cron, and when L2/L3 may run on different engines than L1).
- Full orchestration pipeline: load `references/orchestration.md`, then `references/quality-review.md`, then `references/merge-strategy.md` as each phase is reached.
