# Multi-Device Orchestration Risk Check (EN)

Use this file before proposing or executing `rauto orchestrate`.

Default goal:
- reduce blast radius
- make rollback boundaries explicit
- confirm path and connection assumptions before live execution

## Table of Contents

1. Scope review
2. Concurrency and stop behavior
3. Rollback boundary
4. Path and dependency checks
5. Connection and defaults review
6. Safe execution sequence
7. Output template

## 1) Scope review

Check:
- total number of stages
- total number of targets
- which stages are serial vs parallel
- whether a stage mixes `target_groups` and inline `targets`

Call out explicitly:
- canary/small-scope vs broad rollout
- any inline target with raw `host` instead of saved `connection`

## 2) Concurrency and stop behavior

Check:
- plan-level `fail_fast`
- stage-level `fail_fast` overrides
- each parallel stage `max_parallel`

Important:
- if `max_parallel` is omitted, the runtime defaults to bounded parallelism instead of unlimited fan-out
- higher concurrency increases blast radius and makes partial completion more likely before an error stops the stage

## 3) Rollback boundary

State this clearly in every orchestration review:
- orchestration does **not** provide cross-device global rollback
- rollback remains device-local through reused `tx_block` / `tx_workflow` semantics
- if one device succeeds and another fails, the successful device is not automatically reverted by orchestration itself

## 4) Path and dependency checks

Verify before execution:
- `inventory_file` exists when referenced
- `workflow_file` exists for every `tx_workflow` stage
- `template` exists for every templated `tx_block` stage
- relative paths are evaluated from the plan location or provided `base_dir`

Prefer:
- repo sample files when the user is working inside this repo
- `--dry-run` or Web preview before live execution

## 5) Connection and defaults review

Check:
- string targets require saved connections to exist
- inline targets need usable `host` or `connection`
- `inventory.defaults` affects all relevant targets
- group `defaults` override inventory defaults
- target-level fields override inherited defaults

Call out:
- username/profile/template-dir assumptions
- per-target `vars` overrides that materially change rendered commands

## 6) Safe execution sequence

Recommended order:

1. validate JSON structure
2. run `rauto orchestrate <plan> --dry-run`
3. if needed, run `--view` for terminal structure
4. start with a canary target/group or a low `max_parallel`
5. execute with recording when auditability matters

Typical live command:

```bash
rauto orchestrate ./orchestration.json --record-level full
```

## 7) Output template

Use this when proposing orchestration execution:

```text
Operation: Orchestration risk review
Plan: <orchestration.json>
Scope: <stages/targets/blast radius>
Concurrency: <serial/parallel + max_parallel + fail_fast>
Rollback Boundary: <device-local only / no cross-device global rollback>
Path Check: <inventory/workflow/template assumptions>
Connection Assumptions: <saved connections / inline hosts / inherited defaults>
Recommended Next Step: <dry-run / canary / execute>
Confirmation Needed: <yes>
```
