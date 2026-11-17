---
name: spex
disable-model-invocation: true
description: "Spec-Driven Development (Spex) skill that manages the full SDLC — from requirement analysis and design to incremental implementation and submission. Invoked manually via /spex <command>. Supports commands: create (new), modify, apply (run, do, go), apply-one-step (step), merge (submit), archive, init."
version: 0.7.0
arguments:
  - name: command
    required: false
    description: "Sub-command to execute. Must be one of: create (alias: new), modify, apply (aliases: run, do, go), apply-one-step (alias: step), merge (alias: submit), archive, init. If omitted, infer intent from the remaining text; route directly when confidence ≥ 90%, otherwise ask user to confirm."
  - name: prompt
    required: false
    description: "Optional context passed to the command. For 'create', this is the requirement describing the spec to generate."
---

# Spex — Spec-Driven Development

## Usage

```text
/spex [command] [prompt]
```

- IF no args (`/spex`) -> show Supported Commands table -> STOP
- IF recognized command (`/spex create ...`) -> load matching
  `commands/<file>.md` (Command Routing) -> follow that SOP exactly;
  forward user text as `$prompt`
- IF free-form (`/spex <arbitrary text>`) -> Free-form Intent Inference

## Supported Commands

| Command         | Aliases            | Description                          |
|-----------------|--------------------|--------------------------------------|
| `create`        | `new`              | Create a spec document (no code changes) |
| `modify`        |                    | Modify a spec's requirements         |
| `apply`         | `run`, `do`, `go`  | Apply a spec to generate code        |
| `apply-one-step`| `step`             | Apply one step from a spec's todo list |
| `merge`         | `submit`           | Submit completed work (merge or PR)  |
| `archive`       |                    | Archive a completed spec             |
| `init`          |                    | Initialize spex environment          |

## Command Routing

Command file paths are relative to this `SKILL.md` directory.

| Match                              | Command file                  |
|------------------------------------|-------------------------------|
| `create` / `new`                   | `commands/create.md`          |
| `modify`                           | `commands/modify.md`          |
| `apply` / `run` / `do` / `go`     | `commands/apply.md`           |
| `apply-one-step` / `step`          | `commands/apply-one-step.md`  |
| `merge` / `submit`                 | `commands/merge.md`           |
| `archive`                          | `commands/archive.md`         |
| `init`                             | `commands/init.md`            |

### Routing Discipline

- Role: router, not assistant
- Resolve command -> load command file -> follow every Phase
- User prompt => `$prompt` for the command SOP only
- NEVER act on user prompt directly (no read/write/plan outside SOP)
- NEVER skip or shortcut the command SOP
- ALWAYS load the full command markdown; follow every Phase as written

### Free-form Intent Inference

When first arg matches no route, infer intent:

| If the user's text suggests...                      | Suggest command   |
|-----------------------------------------------------|-------------------|
| A new feature, requirement, or idea to implement    | `create`          |
| Changing requirements for an existing spec           | `modify`          |
| Starting implementation of a spec                    | `apply`           |
| Working through a spec one step at a time            | `apply-one-step`  |
| Finishing, merging, or submitting completed work     | `merge`           |
| Cleaning up completed specs                          | `archive`         |
| Setting up spex for the first time                   | `init`            |

- IF confidence >= 90% -> route directly; free-form text => `$prompt`
- IF confidence < 90% OR multiple commands plausible -> ask user to
  confirm before routing
- IF too vague (e.g. "help" / empty) -> show Supported Commands
  table -> STOP
