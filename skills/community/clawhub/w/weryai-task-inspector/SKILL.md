---
name: weryai-task-inspector
description: Inspect, query, summarize, and debug WeryAI task IDs and batch IDs through the official task query endpoints. Use when you need to query WeryAI task status, inspect batch task progress, debug a stuck generation task, verify podcast content_status, or extract final image, video, audio, lyrics, cover, or script artifacts from an existing WeryAI task.
metadata: { "openclaw": { "emoji": "🔍", "primaryEnv": "WERYAI_API_KEY", "paid": false, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
---

# WeryAI Task Inspector

Inspect existing WeryAI tasks and batches through the official task query endpoints. This skill is read-only: it never submits new jobs and never mutates remote state.

## Example Prompts

- `Inspect this WeryAI task ID and tell me whether it is finished.`
- `Query this WeryAI batch ID and summarize the state of each task.`
- `Check whether this podcast task reached audio-success yet.`
- `Show me the output artifacts for this WeryAI task, including audio or video URLs if present.`

## Quick Summary

- Main jobs: `task status lookup`, `batch status lookup`, `artifact inspection`, `podcast content_status inspection`
- Inputs: `taskId` or `batchId`
- Main outputs: normalized status, best-effort artifacts, raw task payload
- Main trust signals: official read-only task query endpoints, explicit no-submit boundary, podcast-aware `content_status` handling

## Prerequisites

- `WERYAI_API_KEY` must be set before running task queries.
- Node.js `>=18` is required.
- This skill is read-only and safe to re-run.

## Preferred command

```sh
node {baseDir}/scripts/task-inspector.js --task-id <task-id>
node {baseDir}/scripts/task-inspector.js --batch-id <batch-id>
```

## Workflow

1. Determine whether the user has a single `taskId` or a `batchId`.
2. Query the corresponding official endpoint.
3. Return normalized state plus best-effort extracted artifacts.
4. For podcast tasks, interpret `content_status` as the primary lifecycle signal.

## Output contract

Successful output includes:

- `ok`
- `phase`
- `queryType`
- `taskId` or `batchId`
- `taskStatus`
- `contentStatus` when present
- `artifacts`
- `raw`

Failure output includes:

- `errorCode`
- `errorMessage`

## Definition of Done

- A valid `taskId` returns normalized task state plus best-effort artifacts and the raw payload.
- A valid `batchId` returns a batch-level phase and per-task normalized state.
- Podcast tasks surface `contentStatus` when present.
- Invalid or inaccessible task identifiers fail with a clear `errorCode` and `errorMessage`.

## Re-run Behavior

- Re-running this skill is read-only and safe.
- It never creates new WeryAI tasks and never spends credits by itself.

## Boundaries

- Do not use this skill to create new image, video, music, chat, or podcast jobs.
- Do not invent undocumented output fields when the raw payload does not contain them.
- Do not treat podcast `task_status=completed` as final if `content_status` has not reached `audio-success`.

## References

- Official task query summary: [references/tasks-api.md](references/tasks-api.md)
- Task details API: [Query Task Details](https://docs.weryai.com/api-reference/tasks/query-task-details)
- Batch task API: [Query Batch Task Status](https://docs.weryai.com/api-reference/tasks/query-batch-task-status)
