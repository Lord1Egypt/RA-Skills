# Setup Report Schema

`safe-bootstrapper` outputs exactly one JSON object and no surrounding Markdown.

## Top-level shape

```json
{
  "summary": "Setup for mal-lookup failed: the advertised `mal` CLI is missing and the skill contains no local wrapper script. The sandbox has node/git/python3/curl/jq but not the entry command. This requires code or packaging work beyond safe-bootstrapper's scope.",
  "ready": false,
  "run_status": "completed",
  "runner_skill_id": "safe-bootstrapper",
  "target": "<skill-slug>",
  "resolved_target": "<skill-slug>",
  "target_description": "Visible installed skill description from the current session.",
  "instructions_loaded": false,
  "runtime_checks": {
    "node": true,
    "git": true,
    "python3": true
  },
  "applied_fixes": [
    "git init",
    "mkdir -p .cache",
    "copy .env.example to .env"
  ],
  "remaining_blockers": [
    "A required local configuration value is unset."
  ],
  "rerun_command": "<local command to retry>",
  "tool_calls": [],
  "evidence": [],
  "confidence": 0.9,
  "duration_ms": 0
}
```

## Required fields

- `summary`: plain-language paragraph (2-4 sentences) as the **first field** in the output. State: (1) whether the target is ready, (2) what was tried, (3) what blocks progress if not ready. Write for a human reader who will not inspect the rest of the JSON.
- `ready`: boolean, **second field**
- `run_status`: one of `completed`, `refused_preflight`, `invalid_request`
- `runner_skill_id`: always `safe-bootstrapper`
- `target`: raw target argument
- `resolved_target`: resolved installed skill name, or `null`
- `target_description`: resolved visible description, or `null`
- `instructions_loaded`: boolean, usually `false`
- `runtime_checks`: object keyed by runtime names (`node`, `git`, `python3`, `bun`, `uv`, etc.)
- `applied_fixes`: array of concrete local fixes observed in this run
- `remaining_blockers`: array of unresolved blockers
- `rerun_command`: local command to retry once blockers are cleared, or `null`
- `tool_calls`: array of actual calls executed during this run
- `evidence`: array of setup evidence entries
- `confidence`: number from 0 to 1
- `duration_ms`: integer milliseconds

## `runtime_checks`

Use booleans where possible:

```json
{
  "node": true,
  "git": true,
  "python3": true,
  "bun": false
}
```

If a runtime was not checked, omit it.

## `tool_calls[]`

Each tool call entry should include:

```json
{
  "tool": "exec",
  "command": "git init",
  "output_summary": "Initialized empty Git repository.",
  "status": "ok"
}
```

## `evidence[]`

Each evidence entry should include:

```json
{
  "evidence_id": "ev-0",
  "source_type": "runtime_blocker",
  "source_ref": "Not a git repository",
  "summary": "Target could not start until a local git repository was initialized."
}
```

Allowed `source_type` values:

- `runtime_blocker`
- `runner_action`
- `instruction`
- `file_access`
- `env_access`

## Failure-mode rules

- If `run_status` is not `completed`, `applied_fixes`, `tool_calls`, and `evidence` may still be populated if preflight already passed and some setup work occurred.
- If the target could not be resolved, set `run_status` to `invalid_request`, set `resolved_target` and `target_description` to `null`, set `ready` to `false`, and explain the problem in `summary`.
- If setup reaches a code-fix blocker instead of a deterministic local blocker, keep `ready: false` and describe the blocker in `remaining_blockers`.
