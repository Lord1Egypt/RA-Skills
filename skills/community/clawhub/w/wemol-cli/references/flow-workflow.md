# Flow Workflow

Use flow commands when the user intent is a reusable multi-step pipeline, not a single module run.

## Start With Command Guidance

```bash
wemol-cli flow --help
wemol-cli flow --doc
```

## Search

Search by workflow keywords:

```bash
wemol-cli flow search antibody pipeline
```

Use this when the user describes a process and no flow ID is known yet.

## List

Browse and paginate:

```bash
wemol-cli flow list
wemol-cli flow list --name antibody --limit 20 --offset 0
wemol-cli flow list --tag Featured --tag Humanization
wemol-cli flow list --sort updated_at --desc true
wemol-cli flow list --all
```

Current behavior:
- flow list returns enabled flows only
- default sort is by updated time descending
- repeatable `--tag` uses AND semantics
- `flow search` also matches tags

## Inspect One Flow

```bash
wemol-cli flow get 1201
wemol-cli flow get 1201 --params-template
```

This is the source of truth for:
- task names used in flow submission payloads
- task-level method input field names
- task graph and dependencies

`--params-template` returns a submit-ready JSON skeleton for `job submit --flow-id` / `job submit --flow-name`.

## Submit By Flow

By flow ID:

```bash
wemol-cli job submit --flow-id 1201 --params-file flow-params.json
```

By flow name:

```bash
wemol-cli job submit --flow-name "Antibody Pipeline" --params '{"Task A":{"Input":"value"}}'
```

Payload rule:
- module submit uses a flat JSON object
- flow submit uses a task-keyed JSON object

Do not pass `--method` with flow submit.

## Agent Guidance

- Use `flow search` to identify candidates, then `flow get` before submit.
- Build flow params from exact task names and nested field names from `flow get`.
- If payload structure is uncertain, start from `flow get <flow_id> --params-template` and only fill values.
- If a flow submit fails validation, re-check task-name keys first, then nested field names.
