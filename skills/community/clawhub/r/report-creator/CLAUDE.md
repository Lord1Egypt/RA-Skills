# CLAUDE.md

This file is for project-level rules and contributor/agent guidance.
It is not part of the user-facing skill contract.

## Documentation Placement Rules

- `SKILL.md` is user-facing. It defines the skill interface, command behavior, and runtime contract that the user can rely on. Do not put internal project governance or contributor workflow rules here unless they directly affect the user-visible skill contract.
- `CLAUDE.md` is for project rules. Put repository conventions, contributor/agent workflow rules, and documentation placement policy here.
- `docs/` is for project documentation meant for humans: design notes, architectural writeups, adversarial reviews, rollout plans, ROI/eval analysis, and change rationale. These documents explain the project; they are not runtime inputs to the skill.
- `references/` is for runtime references that the skill may load or depend on during execution: rendering contracts, shell templates, routing matrices, review checklists, CSS assembly rules, and similar machine-followed specifications.

## Contract Boundary Rule

- If the skill program needs to read it, route against it, or treat it as executable guidance, it belongs in `references/`.
- If it exists to explain decisions, record reasoning, or help contributors understand the project, it belongs in `docs/`.
- If it is a repository policy about how we organize or maintain the project itself, it belongs in `CLAUDE.md`.

## Current Application

- Footer/watermark format is a runtime rendering contract, so it belongs in `references/html-shell-template.md` and tests.
- The rule explaining where project docs vs runtime references should live is a repository rule, so it belongs here in `CLAUDE.md`.
