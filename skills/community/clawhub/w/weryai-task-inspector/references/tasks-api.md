# WeryAI Task Query APIs

Use this file when you need the exact public contract for the read-only WeryAI task query endpoints.

## Endpoints

- `GET /v1/generation/{taskId}/status`
  - query a single task
- `GET /v1/generation/batch/{batchId}/status`
  - query a batch

## Important podcast rule

For podcast tasks, the lifecycle should be interpreted through `content_status`:

- `text-success`
- `text-fail`
- `audio-success`
- `audio-fail`

Do not rely only on `task_status` when inspecting podcast generation.

## Inspector behavior

This skill is intentionally read-only:

- no submit
- no wait that creates new tasks
- no balance mutation

It should normalize status and surface artifacts, then return the raw payload for debugging.
