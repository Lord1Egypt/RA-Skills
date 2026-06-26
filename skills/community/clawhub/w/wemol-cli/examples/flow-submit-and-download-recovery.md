# Flow Submit And Download Recovery Example

Use this example when the user wants to run a predefined multi-step pipeline (flow), then retrieve results reliably.

## Why This Example Matters

This is the typical flow-first path:
- discover/select flow
- inspect task names and inputs from `flow get`
- submit with task-keyed JSON params
- recover results with resumable, retryable downloads

## Verified Command Pattern

Discover and inspect:

```bash
wemol-cli flow search antibody pipeline
wemol-cli flow get <flow_id>
```

Submit by flow:

```bash
wemol-cli job submit --flow-id <flow_id> --params-file flow-params.json
cat flow-params.json | wemol-cli job submit --flow-id <flow_id> --params @-
```

Example payload shape (`flow-params.json`):

```json
{
  "Task A": {
    "Input": "value"
  },
  "Task B": {
    "Threshold": 0.5
  }
}
```

Track and fetch:

```bash
wemol-cli job status <job_id>
wemol-cli job tasks <job_id>
wemol-cli job output <job_id> --task-id <task_id> --name output
wemol-cli job download <job_id> --retry 3 --concurrency 6
```

If output keys are missing, switch to download:

```bash
wemol-cli job download <job_id> --output ./result_dir --retry 3 --concurrency 6
```

Resume-related retry pattern:

```bash
wemol-cli job download <job_id> --output ./result_dir
wemol-cli job download <job_id> --output ./result_dir --no-resume
```

Observed behavior in current CLI:
- rerunning the same download path reuses manifest state and skips completed artifacts
- summary includes skipped count and transient/permanent failure classification

## Agent Rules From This Example

- For flow submit, never use module-style flat params.
- Build flow params from exact task names and nested field names shown by `flow get`.
- `--params` supports `@-`, so stdin piping is valid for flow payloads.
- Use `job output` first for structured keys; switch to `job download` when output key is missing.
- Prefer `--retry` and `--concurrency` for large artifact sets or unstable networks.
