# WeryAI Task Inspector

Use this package when the user already has a WeryAI `taskId` or `batchId` and wants status, artifacts, or debugging details rather than creating a new job.

Preferred entry point:

- `node {baseDir}/scripts/task-inspector.js`

Route intents this way:

- existing task ID -> `--task-id`
- existing batch ID -> `--batch-id`
- podcast state inspection -> same command, but pay attention to `contentStatus`

Read `SKILL.md` first for output shape and read-only boundaries.
Read `references/tasks-api.md` when you need the exact official query contract.
