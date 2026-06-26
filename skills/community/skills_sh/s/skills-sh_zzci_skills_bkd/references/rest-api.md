# BKD REST API Reference

Use this file when the `bkd` skill needs exact BKD routes, payload shapes, or
operational examples.

## Table of Contents

- [Setup](#setup)
- [Sending Request Bodies Safely](#sending-request-bodies-safely)
- [Health and Status](#health-and-status)
- [Engines](#engines)
- [Processes and Capacity](#processes-and-capacity)
- [Projects](#projects)
- [Issues](#issues)
- [Issue Execution](#issue-execution)
- [Issue Changes](#issue-changes)
- [Issue Logs](#issue-logs)
- [Worktrees](#worktrees)
- [Cron Jobs](#cron-jobs)
- [Other Endpoint Groups](#other-endpoint-groups)


## Setup

```bash
BKD_URL="http://your-host:port/api"
```

BKD responses use one of these envelopes:

- Success: `{ "success": true, "data": ... }`
- Failure: `{ "success": false, "error": "..." }`

## Sending Request Bodies Safely

Issue prompts and other free-form text contain quotes, `$`, backticks, and
newlines that get mangled when inlined into `-d '{...}'` (shell quoting and JSON
escaping fight each other). **Never inline free-form text.** Write the text to a
temp file verbatim, build the JSON body with `jq` (it escapes correctly), and
POST the file with `--data-binary @file`:

```bash
# 1. Write the prompt as plain text — no escaping needed
cat > /tmp/bkd-prompt.txt <<'PROMPT'
Implement the change described above.
"Quotes", $vars, `backticks`, and multiple lines are all safe here.
PROMPT

# 2. Assemble a valid JSON body from the text file
jq -n --rawfile prompt /tmp/bkd-prompt.txt '{prompt: $prompt}' > /tmp/bkd-body.json

# 3. POST the file — never an inline -d string
curl -s -X POST "$BKD_URL/projects/{projectId}/issues/{issueId}/follow-up" \
  -H 'Content-Type: application/json' \
  --data-binary @/tmp/bkd-body.json | jq
```

Add more fields with extra `jq` args (`--rawfile` for file-sourced text, `--arg`
for short strings, `--argjson` for booleans/objects):

```bash
jq -n --rawfile prompt /tmp/bkd-prompt.txt \
      --arg engine "claude-code" --arg model "claude-sonnet-4-6" \
  '{engineType: $engine, prompt: $prompt, model: $model}' > /tmp/bkd-body.json
```

Fixed-value bodies with no free-form text (e.g. `{"statusId":"working"}`,
`{"id":"abc","sortOrder":"a5"}`) are safe to inline with `-d`. The examples below
use inline `-d` only for such fixed payloads; apply the file pattern above
whenever a body carries a prompt, title, description, or any user-supplied text.

## Health and Status

```bash
curl -s "$BKD_URL/health" | jq    # { status, version, commit, db, timestamp }
curl -s "$BKD_URL/status" | jq    # detailed server status
```

## Engines

An engine (`claude-code`, `codex`, `gemini`, ...) is the CLI that executes an
issue. `POST .../execute` requires an `engineType`, so use these to discover what
is installed and which models are available before dispatching.

```bash
# Detected engines + their models (installed, version, authStatus)
curl -s "$BKD_URL/engines/available" | jq

# Per-engine model list, profiles, and current engine settings
curl -s "$BKD_URL/engines/{engineType}/models" | jq
curl -s "$BKD_URL/engines/profiles" | jq
curl -s "$BKD_URL/engines/settings" | jq
```

## Processes and Capacity

Check capacity before starting more issue executions.

```bash
curl -s "$BKD_URL/processes/capacity" | jq   # capacity summary (below)
curl -s "$BKD_URL/processes" | jq            # list active engine processes
```

Response fields:

- `summary.totalActive`
- `summary.byState`
- `summary.byEngine`
- `summary.byProject`
- `maxConcurrent`
- `availableSlots`
- `canStartNewExecution`

Force-terminate the engine process for one issue:

```bash
curl -s -X POST "$BKD_URL/processes/{issueId}/terminate" | jq
```

This is the process-monitor (project-agnostic) route. It is **equivalent** to the
project-scoped [`POST .../issues/{issueId}/terminate`](#restart-cancel-terminate-or-clear-session)
— both force-kill the same process and return `{ issueId, status: "terminated" }`.
In orchestration, prefer the project-scoped command since you already hold the
`projectId`; reach for this one from a global "what's running" view.

## Projects

### List projects

```bash
curl -s "$BKD_URL/projects" | jq
```

### Get project

```bash
curl -s "$BKD_URL/projects/{projectId}" | jq
```

### Create project

```bash
jq -n --arg name "my-project" --arg desc "Optional description" \
      --arg dir "/path/to/workspace" --arg repo "https://github.com/example/repo" \
  '{name: $name, description: $desc, directory: $dir, repositoryUrl: $repo}' > /tmp/bkd-body.json
curl -s -X POST "$BKD_URL/projects" \
  -H 'Content-Type: application/json' \
  --data-binary @/tmp/bkd-body.json | jq
```

Useful fields (only `name` is required):

- `name`
- `alias`
- `description`
- `directory`
- `repositoryUrl`
- `systemPrompt`
- `envVars`
- `defaultEngine`
- `defaultModel`

### Lifecycle

```bash
curl -s -X POST "$BKD_URL/projects/{projectId}/archive" | jq
curl -s -X POST "$BKD_URL/projects/{projectId}/unarchive" | jq
curl -s -X DELETE "$BKD_URL/projects/{projectId}" | jq   # soft-delete

# Reorder a project in the board
curl -s -X PATCH "$BKD_URL/projects/sort" \
  -H 'Content-Type: application/json' \
  -d '{"id":"{projectId}","sortOrder":"a5"}' | jq
```

## Issues

All issue routes are project-scoped:

`/api/projects/{projectId}/issues/...`

### Create issue

Prefer the safe flow: create in `todo`, then follow up, then move to `working`.

```bash
jq -n --arg title "fix auth bug" --argjson useWorktree true \
  '{title: $title, statusId: "todo", useWorktree: $useWorktree}' > /tmp/bkd-body.json
curl -s -X POST "$BKD_URL/projects/{projectId}/issues" \
  -H 'Content-Type: application/json' \
  --data-binary @/tmp/bkd-body.json | jq
```

Useful fields:

- `title`
- `statusId`: `todo|working|review|done`
- `engineType`
- `model`
- `useWorktree`
- `keepAlive`
- `tags`
- `permissionMode`

### List or get issues

```bash
curl -s "$BKD_URL/projects/{projectId}/issues" | jq
curl -s "$BKD_URL/projects/{projectId}/issues/{issueId}" | jq
```

### Update issue

```bash
curl -s -X PATCH "$BKD_URL/projects/{projectId}/issues/{issueId}" \
  -H 'Content-Type: application/json' \
  -d '{"statusId":"working"}' | jq
```

Common fields:

- `title`
- `statusId`
- `tags` with `null` to clear tags
- `keepAlive`
- `isPinned`
- `sortOrder`

### Bulk update

Update many issues in one call — handy for moving a batch of subtasks at once.
Each entry needs `id`; `statusId` and `sortOrder` are optional (max 1000).

```bash
curl -s -X PATCH "$BKD_URL/projects/{projectId}/issues/bulk" \
  -H 'Content-Type: application/json' \
  -d '{"updates":[{"id":"abc12345","statusId":"working"},
                  {"id":"def67890","statusId":"review"}]}' | jq
```

### Duplicate issue

```bash
curl -s -X POST "$BKD_URL/projects/{projectId}/issues/{issueId}/duplicate" | jq
```

### Delete issue

```bash
curl -s -X DELETE "$BKD_URL/projects/{projectId}/issues/{issueId}" | jq
```

## Issue Execution

The normal BKD execution trigger is moving the issue to `working`.

```bash
curl -s -X PATCH "$BKD_URL/projects/{projectId}/issues/{issueId}" \
  -H 'Content-Type: application/json' \
  -d '{"statusId":"working"}' | jq
```

Recommended sequence:

1. Create the issue in `todo`
2. Send details with `follow-up`
3. Move the issue to `working`

**Do not use `/execute` as the normal execution trigger — move the issue to
`working` instead.** The status change is the trigger used throughout this
skill. `execute` is a lower-level primitive that starts a turn in one call,
pinning the engine/model/prompt at start time; reach for it only when you
specifically need that. Unlike the status trigger, `execute` **requires**
`engineType` and `prompt`:

```bash
cat > /tmp/bkd-prompt.txt <<'PROMPT'
Implement the change described above.
PROMPT
jq -n --rawfile prompt /tmp/bkd-prompt.txt \
      --arg engine "claude-code" --arg model "claude-sonnet-4-6" \
  '{engineType: $engine, prompt: $prompt, model: $model}' > /tmp/bkd-body.json
curl -s -X POST "$BKD_URL/projects/{projectId}/issues/{issueId}/execute" \
  -H 'Content-Type: application/json' \
  --data-binary @/tmp/bkd-body.json | jq
# -> { executionId, issueId, messageId, queued }
```

Discover valid `engineType`/`model` values via [`/engines/available`](#engines).

### Follow-up issue

```bash
cat > /tmp/bkd-prompt.txt <<'PROMPT'
Also fix the logout flow and add tests.
PROMPT
jq -n --rawfile prompt /tmp/bkd-prompt.txt '{prompt: $prompt}' > /tmp/bkd-body.json
curl -s -X POST "$BKD_URL/projects/{projectId}/issues/{issueId}/follow-up" \
  -H 'Content-Type: application/json' \
  --data-binary @/tmp/bkd-body.json | jq
```

Fields:

- `prompt` (required)
- `model`
- `permissionMode`: `auto | supervised | plan`
- `busyAction`: `queue | cancel`
- `displayPrompt`

Behavior (by current `statusId`):

- `todo` or `done`: queued, waits for the issue to move to `working`
- `working` during an active turn (or with messages already queued): queued,
  processed after the current turn ends
- `working` when idle: immediate, triggers the next turn
- `review`: immediate — the issue is auto-moved to `working` and a turn starts.
  A bare follow-up to a `review` issue is therefore enough to begin rework; no
  separate `PATCH {statusId:"working"}` is needed.

### Restart, cancel, terminate, or clear session

```bash
curl -s -X POST "$BKD_URL/projects/{projectId}/issues/{issueId}/restart" | jq
curl -s -X POST "$BKD_URL/projects/{projectId}/issues/{issueId}/cancel" | jq
curl -s -X POST "$BKD_URL/projects/{projectId}/issues/{issueId}/terminate" | jq
curl -s -X POST "$BKD_URL/projects/{projectId}/issues/{issueId}/clear-session" | jq
```

- `restart`: re-run a failed session.
- `cancel`: graceful stop of the current execution. The default way to halt a
  running turn.
- `terminate`: force-kill the running process. Use only when `cancel` does not
  stop a hung / unresponsive turn. After a terminate the issue is no longer
  executing — re-trigger it by moving it back to `working`.
- `clear-session`: drop the engine's external session id so the next run starts
  a fresh conversation instead of resuming. Use when the prior context is stale
  or corrupted.

To redirect a busy issue to a changed requirement, the reliable sequence is
**stop → follow-up → start** (cancel first; terminate only if it hangs):

```bash
# 1. Stop the in-flight turn (graceful)
curl -s -X POST "$BKD_URL/projects/{projectId}/issues/{issueId}/cancel" | jq
#    If it does not stop, force-kill:
#    curl -s -X POST "$BKD_URL/projects/{projectId}/issues/{issueId}/terminate" | jq
# 2. Send the new requirement (queued while stopped)
curl -s -X POST "$BKD_URL/projects/{projectId}/issues/{issueId}/follow-up" \
  -H 'Content-Type: application/json' -d '{"prompt":"<new requirement>"}' | jq
# 3. Start a fresh turn
curl -s -X PATCH "$BKD_URL/projects/{projectId}/issues/{issueId}" \
  -H 'Content-Type: application/json' -d '{"statusId":"working"}' | jq
```

## Issue Changes

Get files changed by an issue (useful before merging worktree branches):

```bash
curl -s "$BKD_URL/projects/{projectId}/issues/{issueId}/changes" | jq
```

## Issue Logs

### Get logs

```bash
curl -s "$BKD_URL/projects/{projectId}/issues/{issueId}/logs?limit=50" | jq
```

Useful query params:

- `cursor`
- `before`
- `limit`

### Filtered logs

Use the filter API to pull specific log slices without fetching full logs.

```
GET /projects/{projectId}/issues/{issueId}/logs/filter/{filter_path}
```

#### Filter path syntax

| Dimension | Format | Example |
|-----------|--------|---------|
| Entry types | `types/{type1,type2}` | `types/tool-use` |
| Single turn | `turn/{n}` | `turn/3` |
| Turn range | `turn/{start-end}` | `turn/2-5` |
| Last turn | `turn/last` | `turn/last` |
| Last N turns | `turn/last{N}` | `turn/last3` |
| Combined | concatenate | `types/tool-use/turn/last3` |

Available entry types: `user-message` `assistant-message` `tool-use` `system-message` `thinking` `error-message` `token-usage`

## Worktrees

### List worktrees

```bash
curl -s "$BKD_URL/projects/{projectId}/worktrees" | jq
```

### Delete worktree

Force-deletes the worktree for an issue (does not wait for the auto-clean cycle):

```bash
curl -s -X DELETE "$BKD_URL/projects/{projectId}/worktrees/{issueId}" | jq
```

BKD auto-cleans worktrees 1 day after an issue enters `done`. The cleanup cycle runs every 30 minutes and is controlled by the `worktree:autoCleanup` application setting.

## Cron Jobs

Use `GET /cron/actions` when you need the current server help text.

### List cron jobs

```bash
curl -s "$BKD_URL/cron" | jq
```

Useful query params:

- `limit`
- `cursor`
- `deleted=false|true|only`

### List cron actions

```bash
curl -s "$BKD_URL/cron/actions" | jq
```

Builtin maintenance actions (no per-issue config):

- `upload-cleanup` — remove uploaded files older than 7 days
- `worktree-cleanup` — remove git worktrees for `done` issues older than 1 day
- `log-cleanup` — trim cron job logs to the last 1000 per job
- `issue-log-retention` — delete issue logs for `done` issues past the retention
  period (default 30 days, configurable in app settings)

Issue actions (`issue-execute`, `issue-follow-up`, `issue-close`,
`issue-check-status`) are documented below.

### Create cron job

```bash
curl -s -X POST "$BKD_URL/cron" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "daily-cleanup",
    "cron": "@daily",
    "action": "upload-cleanup",
    "config": {}
  }' | jq
```

Generic fields:

- `name`
- `cron`
- `action`
- `config`

### Issue cron actions

#### `issue-execute`

Required config: `projectId`, `issueId`, `prompt`
Optional config: `engineType`, `model`

```bash
cat > /tmp/bkd-prompt.txt <<'PROMPT'
Run the nightly maintenance task and report the result.
PROMPT
jq -n --rawfile prompt /tmp/bkd-prompt.txt \
  '{name: "nightly-issue-execute", cron: "@daily", action: "issue-execute",
    config: {projectId: "my-project", issueId: "abc12345", prompt: $prompt, engineType: "claude-code"}}' \
  > /tmp/bkd-body.json
curl -s -X POST "$BKD_URL/cron" \
  -H 'Content-Type: application/json' \
  --data-binary @/tmp/bkd-body.json | jq
```

#### `issue-follow-up`

Required config: `projectId`, `issueId`, `prompt`
Optional config: `model`

```bash
cat > /tmp/bkd-prompt.txt <<'PROMPT'
Post a status check-in and ask for the next step.
PROMPT
jq -n --rawfile prompt /tmp/bkd-prompt.txt \
  '{name: "morning-follow-up", cron: "@hourly", action: "issue-follow-up",
    config: {projectId: "my-project", issueId: "abc12345", prompt: $prompt}}' \
  > /tmp/bkd-body.json
curl -s -X POST "$BKD_URL/cron" \
  -H 'Content-Type: application/json' \
  --data-binary @/tmp/bkd-body.json | jq
```

#### `issue-close`

Required config: `projectId`, `issueId`
Optional config: `targetStatus` (default `done`)

```bash
curl -s -X POST "$BKD_URL/cron" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "close-stale-review-item",
    "cron": "@weekly",
    "action": "issue-close",
    "config": {
      "projectId": "my-project",
      "issueId": "abc12345",
      "targetStatus": "done"
    }
  }' | jq
```

#### `issue-check-status`

Required config: `projectId`, `issueId`

```bash
curl -s -X POST "$BKD_URL/cron" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "check-issue-status",
    "cron": "@every_minute",
    "action": "issue-check-status",
    "config": {
      "projectId": "my-project",
      "issueId": "abc12345"
    }
  }' | jq
```

### Trigger, pause, resume, delete

For these operations, `{job}` may be the job ID or job name.

```bash
curl -s -X POST "$BKD_URL/cron/{job}/trigger" | jq
curl -s -X POST "$BKD_URL/cron/{job}/pause" | jq
curl -s -X POST "$BKD_URL/cron/{job}/resume" | jq
curl -s -X DELETE "$BKD_URL/cron/{job}" | jq
```

### Get cron job logs

```bash
curl -s "$BKD_URL/cron/{jobId}/logs?limit=20" | jq
```

Supported query params:

- `status=success|failed|running`
- `cursor`
- `limit`

## Other Endpoint Groups

Additional built-in endpoint groups outside the orchestration core:

- **Notes** — scratch notes: `GET/POST /notes`, `PATCH/DELETE /notes/{noteId}`
- **Settings** — `server-info`, `max-concurrent-executions`, `log-page-size`,
  `workspace-path`, `write-filter-rules` under `/settings/...`
- **Webhooks** — `/settings/webhooks` CRUD, `/test`, and `/deliveries`
- **Slash commands** — `GET /projects/{projectId}/issues/{issueId}/slash-commands`,
  `GET /settings/slash-commands`
- **Events (SSE)** — server-sent event stream for real-time board updates
