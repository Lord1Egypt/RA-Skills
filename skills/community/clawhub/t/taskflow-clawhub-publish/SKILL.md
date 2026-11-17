---
name: taskflow-clawhub-publish
description: Orchestrate a TaskFlow-managed ingestion job that validates, packages, and publishes an OpenClaw skill folder to the ClawHub registry, then verifies the published artifact. Use when a piece of digital content (an agent skill) must move through a durable multi-step flow and land in the ClawHub resource center in a reproducible way.
metadata: { "openclaw": { "emoji": "🪝📦" } }
---

# TaskFlow + ClawHub publish

This skill documents a reproducible two-tool pattern:

- **TaskFlow** owns the *process*: flow identity, owner session, child-task
  linkage, waiting/resuming, and revision-checked state transitions.
- **ClawHub** owns the *ingestion*: it takes a validated skill folder and
  publishes it to the ClawHub resource center so it is installable by slug.

The TaskFlow layer keeps the human-facing orchestration (which step is
running, what state must survive a restart, what we are waiting on). The
ClawHub layer performs the single irreversible write to the resource center.

## When to use

- Publishing any agent skill folder whose ingestion must be auditable and
  resumable across steps.
- Multi-step ingestion jobs that may wait on human review or an external
  scanner result before the final publish.

## Inputs

- `skillFolder`: absolute or workspace-relative path to a skill folder that
  contains a valid `SKILL.md` frontmatter block.
- `slug`, `name`, `version`, `changelog`: ClawHub publish arguments.

## Outputs

- A TaskFlow `flowId` with persisted `stateJson` capturing the skill folder,
  chosen publish arguments, and the resulting published version / URL.
- A published ClawHub skill installable via `clawhub install <slug>`.

## Execution order

1. **validate** (TaskFlow child task)
   - Confirm `SKILL.md` exists and has `name` + `description`.
   - Run `clawhub publish <path> --dry-run --json` and parse the preview.
   - Persist `{ validated: true, dryRun: <parsed> }` into `stateJson`.
2. **publish** (TaskFlow child task, irreversible)
   - Run `clawhub publish <path> --slug <slug> --name <name> --version <version>
     --changelog <changelog> --json`.
   - Persist the returned version and slug into `stateJson`.
3. **verify** (TaskFlow child task)
   - Run `clawhub inspect <slug>` and confirm the published `version` matches the value passed to publish.
   - Optionally install into a throwaway dir:
     `clawhub install <slug> --workdir <tmp>` and read back `_meta.json` / `.clawhub/origin.json`.
   - If a subagent was spawned for the validate/publish steps, confirm the mirrored TaskFlow with:
     `openclaw tasks flow list --json`.
4. **finish**
   - `taskFlow.finish({ flowId, expectedRevision, stateJson })`.

## Notes

- Carry `flow.revision` forward after every mutating call; mutations are
  revision-checked.
- The publish step is the only externally irreversible step; keep it behind
  the dry-run validation step so failures fail-fast.
- See `references/publish.sh` for the concrete commands, `references/inspect.sh`
  for the verification commands, and `references/flow.ts` for the TaskFlow
  orchestration shape.
