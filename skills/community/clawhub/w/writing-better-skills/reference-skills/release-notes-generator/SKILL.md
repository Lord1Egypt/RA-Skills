---
name: release-notes-generator-skill
description: Use when an agent needs to generate or update release notes from structured project changes, especially when the repository defines local output paths, release-note conventions, or validation requirements.
---

# Release Notes Generator Skill

Generate release notes in a reusable way without hardcoding repository-specific commands or paths into the global skill.

## The Iron Laws

```text
NO PROJECT-SPECIFIC CONTEXT IN THE GLOBAL SKILL
```

```text
NO RELEASE-NOTES WORKFLOW IS COMPLETE UNTIL ANOTHER AGENT COULD RUN IT WITHOUT GUESSING LOCAL PATHS OR VALIDATION STEPS
```

## Project-Local Context Comes First

Before doing substantial work in a repository:

1. Look for `project.skill.md` in the project root.
2. If it exists, read it before taking action.
3. If it does not exist and local context is needed, create it from `project.skill.template.md`.
4. Put repository-specific commands, paths, output locations, and constraints in `project.skill.md`, not in this global skill.
5. Treat `project.skill.md` as overriding generic guidance here when local details differ.

## What This Skill Covers

Use this skill to:
- generate markdown release notes from structured input
- apply a default release-notes format unless the project overrides it
- validate that the generated file exists and contains required sections
- heal a missing output directory only when that failure is explicit and unambiguous

## Reference Map

- Need the default markdown shape? Read `references/output-format.md`.
- Need example local setup? Read `project.skill.template.md` and the paired example project file at `../../examples/release-notes-project/project.skill.md`.

## Scripts

- `scripts/generate_release_notes.py` reads a JSON input file and writes markdown release notes.

## Tests

- `tests/test_generate_release_notes.py` proves the generator creates a release-notes file with expected sections.

## Self-Healing

- `self-healing/heal_output_dir.py` creates a missing output directory.
- Use it only when the generator fails specifically because the output directory does not exist.
- If the failure is anything else, stop and investigate instead of healing.

## Workflow

1. Read `project.skill.md` in the project root if present.
2. Determine the input file path, output path, and required sections from project-local context.
3. If local context is missing, create `project.skill.md` from `project.skill.template.md` before guessing.
4. Run `scripts/generate_release_notes.py <input.json> <output.md>`.
5. Validate with `tests/test_generate_release_notes.py` or equivalent project-specific verification.
6. If the generator fails because the output directory does not exist, run `self-healing/heal_output_dir.py <output-dir>` and retry once.
7. Do not claim completion until the file exists and required sections are present.

## Red Flags — STOP

- Putting repo paths in this global skill
- Guessing where release notes should be written
- Skipping the paired test because the script is small
- Running healing for an unclear failure
- Claiming success because the script "should work"
