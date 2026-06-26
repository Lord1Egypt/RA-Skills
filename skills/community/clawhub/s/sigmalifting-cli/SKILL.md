---
name: sigmalifting-cli
description: Use when the user wants to create, translate, import, validate, inspect, or update powerlifting training programs or workout logs for SigmaLifting using sigmalifting-cli, especially from spreadsheets, manuals, public programs, app exports, program-import bundles, or process-import bundles.
---

# SigmaLifting CLI

Use this skill when working with SigmaLifting CLI bundles, especially when turning a spreadsheet, manual, or public program into a `program-import` bundle.

## Core Boundaries

- Treat the CLI as a standalone JSON tool.
- Use the installed `sigmalifting-cli` executable as the contract and validation engine.
- Do not rely on Realm, Expo file APIs, or app services for CLI behavior.
- Stored program changes may cascade into linked process bundles in the CLI JSON store; file-only bundle edits cannot update unrelated files unless the command output is saved to the store.
- Prefer contract-valid JSON bundles over app-coupled shortcuts.
- Treat this skill folder as the modeling guide, not as the executable schema.

## Agent Mutation Policy

SigmaLifting JSON is the CLI's internal storage and import/export contract. It is not an agent editing surface.

Agents must not directly create or mutate program/process bundle JSON with file edits, `apply_patch`, ad hoc scripts, `jq`, editor operations, or manual rewrites of files in the CLI store. Reading JSON for diagnosis is allowed; writing JSON directly is not.

All bundle creation and mutation must go through CLI commands:

- create initial bundles with `template`, `program create`, `process create-from-program`, or `xlsx import`
- change programs with `program add-block`, `program update-block`, `program add-day`, `program update-schedule`, `program add-exercise`, `program update-exercise`, custom-lift commands, and the exercise-progression intent commands such as `program set-anchor`, `program add-set-group`, `program set-week-value`, and `program toggle-backoff`
- change processes with `process update-*` commands and narrow intent commands such as `process set-one-rm`
- write command results with `--out` or let the local store persist command output
- import externally supplied JSON only through `validate`; use `normalize` only when the user explicitly wants CLI cleanup/repair

`validate` is a strict import/acceptance gate for existing JSON. If it fails with repair warnings, use `normalize` to produce the cleaned bundle before inspecting or importing it.

If the CLI does not expose a command for a needed mutation, stop and report the CLI command gap or add the command first. Do not bypass the CLI by patching raw JSON.

## CLI Discovery

When the installed CLI and this skill are available, inspect the tool before modeling:

1. run `sigmalifting-cli doctor --compact`
2. read this `SKILL.md` and any task-relevant files in `references/`
3. run `sigmalifting-cli help --compact`
4. run `sigmalifting-cli schema list --compact`
5. run `sigmalifting-cli template program-import --compact` or `template process-import --compact`

Program and process bundle results persist as local JSON by default. Use `sigmalifting-cli store path` to locate the store, and use `SIGMALIFTING_HOME` or `--store-root` when you need an explicit test or project-local store.

## Schema Contract

Do not treat this skill file as the schema.

This skill explains modeling judgment: block boundaries, weekly structure, set-group semantics, and common translation mistakes. The installed CLI is the schema source of truth.

Schema mentions in this skill are routing instructions, not schema documentation. They tell the agent which CLI commands to call before building CLI payloads or accepting imported JSON.

Before building CLI command payloads or importing existing JSON, get the executable contract from the CLI:

1. `sigmalifting-cli schema list --compact`
2. `sigmalifting-cli schema show <kind> --compact`
3. `sigmalifting-cli template <kind> --compact`
4. `sigmalifting-cli validate <kind> --file <path|"-"> --compact`

Use the template to learn field shape, defaults, sentinel values, and nesting. Use `schema show` to check constraints. Use this skill to decide what the program should mean structurally.

If the skill and CLI appear to disagree, trust the CLI schema and report the skill as stale.

Do not invent fields that are not present in the CLI schema or template.

## Authoritative Sample Workflow

If the user provides an exported SigmaLifting JSON file, treat that export as the first source of truth.

Before generating or translating anything similar:

1. identify the bundle kind the file actually matches
2. run the standalone CLI against the file exactly as provided
3. validate it first
4. if validation reports repair warnings, normalize it and validate the normalized output
5. only then extract modeling rules from it
6. make any changes through CLI mutation commands, never by patching the JSON file

If an app-exported file cannot be consumed by the standalone CLI, treat that as a CLI problem to investigate before declaring the modeling wrong.

Do not skip this step and jump straight to reconstructing the program from memory, public spreadsheets, or a simplified interpretation.

## Block Semantics

Do not define a block by contiguous time alone.

A block is a maximal consecutive run of weeks that share the same structural skeleton.

The structural skeleton means:

- same training day layout
- same exercise identities on each day
- same set-group count and ordering per exercise
- same variable-parameter style per set group
- same dependency shape such as backoff or fatigue-drop relationships

What may vary inside a block:

- weekly set counts
- weekly reps
- weekly RPE values
- weekly percentages
- weekly notes

What should usually force a new block:

- a day appears, disappears, or changes role materially
- an exercise is added, removed, or replaced
- a set group appears or disappears
- a set group changes semantic role rather than just numeric values
- dependency structure changes
- the week only fits by abusing placeholder zero-sets across many exercises
- the phase intent clearly changes even if the schema could be compressed

Do not collapse an entire multi-week program into one block just because weekly arrays can encode it.

That is a schema-valid compression, but it is a modeling error under SigmaLifting semantics.

## Variable Parameter Semantics

Every set group has exactly one workout-recorded variable parameter: `weight`, `reps`, or `rpe`.

The other two training numbers are prescribed by the program:

- `variable_parameter: "weight"` means reps and RPE are prescribed, and weight is recorded during the workout.
- `variable_parameter: "reps"` means weight and RPE are prescribed, and reps are recorded during the workout.
- `variable_parameter: "rpe"` means weight and reps are prescribed, and RPE is recorded during the workout.

Do not model a set group by prescribing all three numbers. Do not leave two numbers open unless the CLI has a command and schema support for that explicit behavior.

Backoff and fatigue-drop configs are RPE-variable tools in the app model. They are only valid on set groups with `variable_parameter: "rpe"`. If weight is the variable parameter, do not enable `backoff_config`, `fatigue_drop_config`, or mixed-weight prescription.

## Workflow

When modeling a program:

1. Inspect each week for structural sameness, not just duration.
2. Group only consecutive weeks that share the same skeleton.
3. Create one block per structural group.
4. Use weekly arrays only for parameter variation inside that block.
5. Preserve special-case instructions in notes if they are not truly machine-derived.
6. If unsure, prefer more blocks over fewer blocks.

## Warning Signs

Stop and re-evaluate the block split if you notice:

- many `0` set placeholders just to make weeks fit
- weeks that feel like distinct phases but are still in one block
- day layouts drifting across weeks
- exercise schemes changing identity from week to week

## References

- For detailed modeling guidance, read [references/program-modeling.md](references/program-modeling.md).
- For Candito-specific lessons extracted from an exported app bundle, read [references/candito-translation.md](references/candito-translation.md).
- For process execution and workout logging rules, read [references/process-logging.md](references/process-logging.md).
