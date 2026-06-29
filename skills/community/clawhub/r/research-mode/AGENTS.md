# Agent Notes

This file is for coding agents and maintainers working on this repository.
Human-facing project documentation lives in `README.md`, `TROUBLESHOOTING.md`,
`ARCHITECTURE.md`, `RELEASE_NOTES.md`, `RELEASING.md`, and `SECURITY.md`.

## Keep The Boundary Clear

- Keep human documentation useful without requiring private workspace context.
- Put operational instructions for OpenClaw runtime agents in `SKILL.md`.
- Put repository-maintenance guidance for coding agents in this file.
- Do not add private paths, chat ids, cron ids, tokens, webhook URLs, personal
  notes, or generated research artifacts to public examples.
- Do not mix hidden prompts or agent-only instructions into human-facing docs.

## Before Changing Behavior

- Read `SKILL.md` and the relevant helper modules under `scripts/`.
- Preserve the cron-based execution model: Research Mode is an OpenClaw skill,
  not a standalone daemon or generic Python package.
- Keep task state and artifacts task-local and path-contained.
- Keep `awaiting_review` separate from delivered/completed state.
- Keep finalization evidence explicit before a worker marks a result reviewable.

## Verification

Run the release gate from the repository root after meaningful changes:

```bash
scripts/check_research_mode.sh
```

For documentation-only changes, at minimum run:

```bash
python3 scripts/check_research_mode_docs.py
```
