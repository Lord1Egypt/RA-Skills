# Job Workflow

Use jobs to run a selected module method and then inspect progress and outputs.

## Submit

By module ID:

```bash
wemol-cli job submit --module-id 451 --params-file params.json
cat params.json | wemol-cli job submit --module-id 451 --params @-
```

By module name:

```bash
wemol-cli job submit --module-name "AlphaMHC" --method run --params '{"sequence":"AAA"}'
```

By flow ID:

```bash
wemol-cli job submit --flow-id 1201 --params-file flow-params.json
```

By flow name:

```bash
wemol-cli job submit --flow-name "Antibody Pipeline" --params '{"Task A":{"Input":"value"}}'
```

Method selection:

- `--method` is optional.
- If `--method` is omitted, `wemol-cli` uses the first method exposed by the module.
- For multi-method modules, prefer setting `--method <name>` explicitly instead of relying on the default.
- `--method` is for module submit only, not flow submit.
- `--params` supports `@-` to read JSON from stdin.

File parameters:

```bash
wemol-cli job submit --module-id 226 --params '{"Sequence File":"./seq.fasta"}'
```

When a parameter expects a file, pass a local file path in the JSON payload. The CLI uploads the file automatically and binds it to the matching file argument.

Parameter names in the JSON payload must match the module parameter `field` names exactly as returned by:

```bash
wemol-cli module get <module_id> --params-json
```

Do not invent normalized names such as `sequence_file` or `fasta_file` unless the module actually exposes those exact `field` values.

For flow submit payloads:
- top-level keys are flow task names
- nested keys are task method input fields from `flow get <flow_id>`

## Track Status

Quick summary:

```bash
wemol-cli job status 127822
```

The summary includes an `Elapsed` field so polling users can see how long the job has been running even when progress is still `0%`.

Full record:

```bash
wemol-cli job get 127822
```

Wait for completion:

```bash
wemol-cli job wait 127822
wemol-cli job wait 127822 --until terminal
wemol-cli job wait 127822 --interval 5
```

Wait behavior:
- `job wait <job_id>` defaults to `--until done` (must reach `Done`)
- use `--until terminal` to stop on `Done/Abort/Cancel`

Aggregate progress:

```bash
wemol-cli job progress 127822
```

Use this for compact task-status counts plus active tasks when `job status` is too coarse.

Diagnose and next actions:

```bash
wemol-cli job diagnose 127822
```

Use this when a job is stuck, failed, or output routing is unclear. The command returns focused suggestions and executable `next_commands`.

## Inspect Tasks

```bash
wemol-cli job tasks 127822
```

Task output includes:
- `module_id`
- `module_name`
- `method`

Use these fields to reconnect a job task back to its source module.

## Logs And Outputs

Logs:

```bash
wemol-cli job logs 127822
wemol-cli job logs 127822 --task-id 1 --stderr
```

If logs are not ready yet, the CLI returns a retry-oriented message instead of raw backend `DBDataNotFound` text.

Output values:

```bash
wemol-cli job output 127822 --task-id 1 --name output
```

If the named output is missing, treat that as a hint to try `job download <job_id>` because many modules publish result files instead of output keys.

Downloads:

```bash
wemol-cli job download 127822
wemol-cli job download 127822 --retry 3 --concurrency 8
wemol-cli job download 127822 --no-resume
wemol-cli job download --all --output ./downloads --retry 3 --concurrency 6
```

Download behavior:
- Resume is enabled by default and tracked in `.wemol-download-manifest.json`
- `--no-resume` disables state reuse
- `--retry` controls per-artifact retries with exponential backoff
- `--concurrency` controls parallel artifact downloads per job
- summary includes downloaded/skipped and transient/permanent failure counts

## Agent Guidance

- Always fetch `module get <module_id> --params-json` before submission when parameter names are not already known.
- JSON keys for `job submit` must exactly match the module parameter `field` values.
- Prefer `job status` for polling loops.
- Use `job progress` for aggregate task-level progress and active-task inspection.
- Use `job diagnose` when you need focused troubleshooting and direct `next_commands`.
- Use `job tasks` before `job logs` or `job output` when task IDs are not known.
- Use `job output` for structured result retrieval and `job download` for artifact files.
