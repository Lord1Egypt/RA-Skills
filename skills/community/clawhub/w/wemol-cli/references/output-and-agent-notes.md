# Output And Agent Notes

Use these rules when interpreting `wemol-cli` output.

## Help vs Doc

- `--help` is concise and command-structured.
- `--doc` is available on root and supported commands/groups (`module`, `flow`, `job`, `host`, `lang`, `account`).
- Leaf `--doc` support is limited and version-dependent. In current CLI, `module get --doc` and `job download --doc` are supported.

## Module Output

- `module get <id>` prints one language only, following `wemol-cli lang`.
- It appends a method summary section at the end.
- `module get <id> --params-json` returns structured JSON for all methods unless `--method` is provided.
- In `--params-json`, `description` fields also follow the current CLI language.
- `module list` and `module search` return enabled modules only.

## Flow Output

- `flow get <id>` is the source of truth for task names and task-level input fields.
- `flow get <id> --params-template` returns a submit-ready skeleton that reduces payload-shape mistakes.
- Use flow details to build task-keyed payloads for flow-based `job submit`.

## Job Output

- `job tasks <job_id>` is the bridge from execution back to module context.
- `job status <job_id>` is better than `job get <job_id>` for quick polling.
- `job progress <job_id>` adds aggregate task-status counts and active tasks for faster triage.
- `job diagnose <job_id>` returns focused suggestions and executable `next_commands`.
- Authentication failures are normalized by the CLI and should be treated as a login requirement, not as raw backend diagnostics.
- `job download` defaults to resume mode and writes `.wemol-download-manifest.json` in the output directory.
- `job download` summary now exposes skipped artifacts and transient/permanent failure counts.

## Exploration Discipline

- Prefer low-cost discovery first: `--help`, `--doc`, `module search`, `job status`, `job progress`.
- Only fetch large outputs when needed.
- When a user asks what a module needs, use `--params-json` before answering.
- When a user asks why a job failed, inspect `job status`, then `job tasks`, then `job logs`.
