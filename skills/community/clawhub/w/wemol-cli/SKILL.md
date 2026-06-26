---
name: wemol-cli-official
description: Use when a task may involve Wemol, a drug-discovery computing platform that integrates many biology, AI, and chemistry modules for workflows such as biologics design, small-molecule discovery, molecular simulation, ADMET prediction, virtual screening, structure prediction, antibody engineering, and immunogenicity analysis. This skill is the operating manual for the Wemol CLI client.
---

# Using wemol-cli

## Overview

`wemol-cli` is the operational client for Wemol modules and flows. Use it to discover modules/flows, inspect real input schemas, submit jobs, track execution, and recover outputs.

Primary rule:
- Prefer executing CLI commands and reading real output over assumptions.

This `SKILL.md` is now self-sufficient for normal operation. `references/` and `examples/` are secondary for edge cases and domain-specific patterns.

## When To Use

Use when:
- user asks for a biology/chemistry/AI workflow that may map to Wemol modules or flows
- task requires live module params, job status, logs, outputs, downloads
- session/host/lang/install behavior affects task execution

Do not use when:
- task is SDK/CLI source implementation work
- user only asks for static code edits unrelated to running CLI

## Quick Start

When context is unknown:

```bash
wemol-cli --help
wemol-cli --version
wemol-cli host
wemol-cli lang
wemol-cli module search antibody
```

If authentication error appears, stop and run:

```bash
wemol-cli login
```

If interactive login is not possible (non-TTY), use:

```bash
wemol-cli login --username <name> --password <password>
```

## Quick Reference

| Situation | Required Action | Avoid |
|---|---|---|
| User asks capability but no ID | `module search` / `flow search` first | guessing module/flow by name only |
| Any submit intent | fetch schema (`--params-json` or `flow get`) first | building payload from natural language |
| Flow submit | enforce task-keyed JSON | flat JSON submit |
| `job output` missing/empty | `job tasks` then `job download` | concluding job failed immediately |
| Auth/session issue | `login` / `account` / `host` / `lang` checks | continuing API probes while unauthenticated |
| User asks “need update?” | run update workflow and conclude directly | asking user to compare versions manually |

## Command Routing (Default)

- Capability request, no module ID:
  - `wemol-cli module search <keywords...>`
- Catalog browsing/filtering:
  - `wemol-cli module list ...`
- Pipeline/workflow request:
  - `wemol-cli flow search <keywords...>` then `wemol-cli flow get <flow_id>`
- Need exact module payload:
  - `wemol-cli module get <module_id> --params-json`
- Need flow payload shape:
  - `wemol-cli flow get <flow_id> --params-template`
- Submitted job, need progress:
  - `wemol-cli job status <job_id>` and `wemol-cli job progress <job_id>`
- Need `task_id`:
  - `wemol-cli job tasks <job_id>`
- Output unclear:
  - `wemol-cli job diagnose <job_id>` then `wemol-cli job download <job_id>`
- Historical run, unknown `job_id`:
  - `wemol-cli job list ...` or `wemol-cli job search ...`

## Core Commands And Rules

### Global Options

```bash
wemol-cli --host <url> ...
wemol-cli --session-id <session_id> ...
wemol-cli --user-agent <ua> ...
wemol-cli --timeout <sec> ...
wemol-cli --secure ...
wemol-cli --verbose ...
wemol-cli --doc
```

Environment equivalents:
- `WEMOL_HOST`
- `WEMOL_SESSION_ID`
- `WEMOL_USER_AGENT`

Rules:
- Prefer persisted `host --set` and cached login for routine work.
- Use `--host` / `--session-id` for one-off overrides.
- Use `--user-agent` only when explicit routing/debugging requires it.
- `--doc` exists on root and command groups (`module`, `flow`, `job`, `host`, `lang`, `account`); some leaf commands also support it depending on version.

### Host / Language / Session / Account

```bash
wemol-cli host
wemol-cli host --set https://wemol.wecomput.com
wemol-cli lang
wemol-cli lang --set en
wemol-cli lang --set cn
wemol-cli account
wemol-cli logout
```

Rules:
- `module get` and `module get --params-json` follow current language.
- use `account` to confirm active identity and resource summary.
- use `logout` to clear current host session before relogin/switch account.

### Module Discovery And Inspection

```bash
wemol-cli module search antibody numbering
wemol-cli module list --name antibody --tag Biologics --tag Antibody --limit 20 --offset 0
wemol-cli module list --sort updated_at --desc true
wemol-cli module get <module_id>
wemol-cli module get <module_id> --params-json
wemol-cli module get <module_id> --params-json --method "<method_name>"
```

Rules:
- `module list` and `module search` currently return enabled modules.
- `module list --tag` is repeatable and uses AND semantics.
- `module search` includes tag matching.
- Before submit, always read `--params-json`; do not guess keys/types/options.

### Flow Discovery And Inspection

```bash
wemol-cli flow search antibody pipeline
wemol-cli flow list --name antibody --tag Featured --tag Humanization --limit 20 --offset 0
wemol-cli flow list --sort updated_at --desc true
wemol-cli flow get <flow_id>
wemol-cli flow get <flow_id> --params-template
```

Rules:
- `flow list --tag` is repeatable and uses AND semantics.
- `flow search` includes tag matching.
- `flow get` is source of truth for task names and nested input keys.
- use `--params-template` whenever payload structure is uncertain.

### Job Submit

Module submit:

```bash
wemol-cli job submit --module-id <module_id> --method "<method_name>" --params '{"Input":"value"}'
wemol-cli job submit --module-name "<module_name>" --params-file params.json
cat params.json | wemol-cli job submit --module-id <module_id> --params @-
```

Flow submit:

```bash
wemol-cli job submit --flow-id <flow_id> --params-file flow-params.json
wemol-cli job submit --flow-name "<flow_name>" --params '{"Task A":{"Input":"value"}}'
cat flow-params.json | wemol-cli job submit --flow-id <flow_id> --params @-
```

Rules:
- Select exactly one target: `--module-id` / `--module-name` / `--flow-id` / `--flow-name`.
- `--method` is module-only; do not use with flow submit.
- `--params` and `--params-file` are mutually exclusive.
- `job submit` supports repeatable `--tag`; CLI auto-adds `Wemol CLI` source tag.
- Module payload keys must match `--params-json` `field` values exactly.
- Flow payload must be task-keyed JSON (`{"Task Name": {"Input": value}}`).
- File args accept local file path; CLI uploads automatically.
- For file args, check `format` / `value_formats` from `--params-json` before submit.
- For `MultipleChoice`, send array even for one option (for example `{"Numbering Scheme":["imgt"]}`).

### Job Read / Track / Diagnose

```bash
wemol-cli job list --status Done --tag "Wemol CLI" --limit 20 --offset 0
wemol-cli job search antibody numbering
wemol-cli job status <job_id>
wemol-cli job progress <job_id>
wemol-cli job get <job_id>
wemol-cli job wait <job_id>
wemol-cli job wait <job_id> --until terminal --interval 5
wemol-cli job tasks <job_id>
wemol-cli job diagnose <job_id>
wemol-cli job cancel <job_id>
```

Rules:
- use `job list` for status/history filters; `job search` for topic/module keyword recovery.
- `job wait <job_id>` defaults to `--until done`; use `--until terminal` to stop on `Done/Abort/Cancel`.
- `job progress` is preferred when `status` is too coarse.
- `job diagnose` gives focused suggestions and executable `next_commands`.

### Logs / Output / Download

```bash
wemol-cli job logs <job_id>
wemol-cli job logs <job_id> --task-id <task_id> --stderr
wemol-cli job logs <job_id> --task-id <task_id1>,<task_id2> --stdout

wemol-cli job output <job_id> --task-id <task_id> --name output
wemol-cli job output <job_id> --task-id <task_id1>,<task_id2> --dynamic

wemol-cli job download <job_id>
wemol-cli job download <job_id> --output ./result_dir
wemol-cli job download <job_id> --retry 3 --concurrency 8
wemol-cli job download <job_id> --no-resume
wemol-cli job download --all --output ./downloads
```

Rules:
- `job output` normally requires `--task-id`; if missing, run `job tasks` first.
- If output key missing or empty-data style errors (`DBDataNull`/similar) appear, try `job download` before declaring failure.
- download resume is enabled by default with `.wemol-download-manifest.json`.
- `--no-resume` disables state reuse.
- summary includes skipped artifacts and transient/permanent failures.

## Hard Rules (Must Follow)

1. No guessed payload keys
- Never infer submit keys from natural language.
- Always derive from `module get --params-json` or `flow get`.

2. No flow flat JSON submit
- Flow submit must be task-keyed.
- If user gives flat JSON, fix structure first, then ask missing values.

3. No blind retry
- On validation error, re-read schema and payload shape first.
- On `JobModuleTaskMaxNumLimit`, treat as capacity/quota issue, not payload formatting.

4. No premature failure conclusion
- `job output` failure is not equal to job failure.
- Try `job tasks` + `job download`.

5. No auth-ignore probing
- After auth-required error, login/session handling comes first.

6. No update-question deflection
- For “需要更新吗 / latest?” do comparison work yourself, do not tell user to compare.

## Detection Triggers (Auto-Branch)

When these signals appear, branch automatically:
- `Authentication required` / `DBUserNoLogin` / `session null`:
  - branch to session handling (`login`, `account`, `host`, `lang`) before further task commands.
- user message contains `flow_id` / `--flow-id` / `flow submit` / `pipeline submit`:
  - branch to flow-shape validation (`flow get`, optional `--params-template`) before accepting payload.
- output errors contain `Output '<name>' was not found` or empty-data style (`DBDataNull`, `DBDataNotFound`):
  - branch to artifact recovery (`job download`) before failure conclusion.
- submit error contains `JobModuleTaskMaxNumLimit`:
  - branch to capacity/quota diagnosis, not payload rewrite.
- user asks `需要更新吗` / `latest` / `should I update`:
  - branch to version/update decision workflow.

## Version / Update Decision Workflow

When user asks whether update is needed:

1. Check installed version:

```bash
wemol-cli --version
```

2. Compare against known baseline:
- this skill baseline is `v1.0.0` (minimum)
- if operating in this repo, also read repo CLI version from `crates/cli/Cargo.toml`

3. Decision:
- installed `< v1.0.0` -> update required
- installed `< repo version` -> update required
- installed `== repo version` (or `>= v1.0.0` and no higher trusted source available) -> no mandatory update from local evidence

4. Upstream check:
- if channel access is available, check official release channel directly
- if blocked, report explicit blocker and what was checked

Allowed final statements:
- `update required`
- `no update required from current evidence`
- `cannot verify upstream latest due to <specific blocker>`

## Response Contract

When answering operational questions, include:
- what was checked (exact command(s))
- observed key evidence (version/status/error marker)
- decision/result category (for example update required / no update required / blocked)
- next concrete command when action is needed

Do not return generic uncertainty without evidence.

## When To Read References (Secondary)

Use references for extra depth, not for basic operation:
- `references/install.md`: installer, PATH/security, cross-platform details
- `references/session-and-host.md`: auth/session/host/lang/account nuances
- `references/module-workflow.md`: deeper module filtering/schema patterns
- `references/flow-workflow.md`: flow payload troubleshooting patterns
- `references/job-workflow.md`: advanced diagnose/download behavior
- `references/output-and-agent-notes.md`: output ambiguity interpretation

## Example Triggers

Use examples when task matches known pattern:
- antibody numbering: `examples/antibody-numbering-variable-region.md`
- protein descriptors: `examples/protein-physicochemical-properties.md`
- ADMET CSV: `examples/admet-ai.md`
- MHC-I minimal output: `examples/mhc-i-binding-prediction.md`
- history recovery: `examples/job-history-recovery.md`
- flow submit + download: `examples/flow-submit-and-download-recovery.md`
- run-limit error: `examples/module-run-limit-error.md`

## Completion Checklist

Before concluding:
- Are command and payload shapes confirmed from live CLI output?
- If submit happened, were keys copied from schema (not guessed)?
- If output unclear, did you try `job tasks`/`job download` before declaring failure?
- If asked about update, did you run the full update decision workflow and return a direct conclusion?

## Self-Check Scorecard (Pass/Fail)

Run this quick scorecard before sending the final answer:

1. Evidence check (Pass/Fail)
- Did I run or quote concrete command evidence (`--version`, `status`, error marker, etc.)?

2. Decision check (Pass/Fail)
- Did I provide an explicit result category (for example update required / no update required / blocked with reason)?

3. Actionability check (Pass/Fail)
- If action is needed, did I provide the exact next command?

4. Deflection check (Pass/Fail)
- Did I avoid pushing core comparison/diagnosis work back to the user?

If any item is Fail, revise the response before sending.
