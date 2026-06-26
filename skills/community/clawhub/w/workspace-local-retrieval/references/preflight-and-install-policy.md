# Preflight and Install Policy

Read this file when the user wants the skill to be directly usable after installation, or when you need to decide whether to execute, stop, or prepare an installation plan.

## Rule

Run prerequisite checks before any retrieval workflow.

Do not bootstrap, index, embed, refresh, or search until the environment has been evaluated.

## Decision policy

### Case 1 — required prerequisites pass

Proceed with the normal retrieval workflow.

### Case 2 — only recommended or optional prerequisites are missing

Proceed only if the reduced capability is acceptable.
State clearly what is degraded.

Examples:
- no local embedding backend yet -> lexical retrieval only
- no sqlite3 CLI -> retrieval may still work, but inspection/debugging is weaker

### Case 3 — one or more required prerequisites are missing

Treat this as a hard stop for the main workflow.

If the user has not authorized installation or environment changes:
- report that the skill is currently unavailable
- list the missing requirements
- state what the user needs to install or configure
- do not continue execution

If the user wants the environment prepared:
- create a task plan first
- tailor the plan to the current operating system
- install or configure dependencies
- update config and docs to reflect the chosen backend
- rerun prerequisite checks
- continue only after required checks pass

## Task plan expectations

A good install plan should include:
- operating system assumption
- required packages or tools
- backend choice
- config files to create or update
- validation commands
- expected degraded modes if the full stack is not installed

## Cross-platform rule

Do not assume one installation recipe works everywhere.

At minimum, distinguish:
- macOS
- Linux
- Windows

Prefer Python-based checks and config-driven backends to reduce shell-specific failure modes.

## User-facing response pattern

When prerequisites are missing, say this plainly:
- what is missing
- whether execution is blocked or degraded
- whether you can prepare an install plan
- what happens next after installation

Avoid vague phrases like "may not work" when the main workflow is actually blocked.
