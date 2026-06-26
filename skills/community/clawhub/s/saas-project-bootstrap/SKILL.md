---
name: saas-project-bootstrap
description: Bootstrap any SaaS, dashboard, mobile, or API project with a reusable 3-agent AI operating system. Creates AGENTS.md, architect/builder/tester instructions, docs templates, and prompt templates for Codex-style execution.
---

# SaaS Project Bootstrap

Use this skill when the user wants to initialize a new project with a reusable AI workflow layer for planning, building, and testing.

## What this skill does

This skill sets up a project operating system with 3 specialized agents:

- Architect
- Builder
- Tester

It installs or generates:

- `AGENTS.md`
- `.agents/architect.md`
- `.agents/builder.md`
- `.agents/tester.md`
- `docs/PRD.md`
- `docs/architecture.md`
- `docs/user-stories.md`
- `docs/api-spec.md`
- `docs/test-plan.md`
- `docs/decision-log.md`
- `templates/feature-request.md`
- `templates/bug-report.md`
- `templates/task-prompt.md`

## Use this skill for

- starting a new SaaS project
- adding AI operating structure to an existing repo
- preparing a repo for 3-agent workflows
- standardizing docs and prompts
- making a reusable project template

## Project types supported

- Next.js SaaS
- React Native mobile app
- backend or API service
- dashboard or admin panel
- full-stack product repo

## Operating model

### Architect
Use for:
- scoping
- PRD
- user stories
- architecture
- task breakdown
- acceptance criteria

### Builder
Use for:
- implementation
- refactoring
- API and UI wiring
- scoped code changes
- migrations

### Tester
Use for:
- validation
- edge cases
- regression checks
- bug reporting
- done criteria verification

## Required behavior

When using this skill:

1. Detect the current project type from the repository structure.
2. Do not overwrite important project files without clear need.
3. Keep changes scoped to the AI operating layer.
4. Preserve the existing application structure.
5. Prefer reusable conventions over project-specific assumptions.
6. Generate docs and templates that match the detected stack when possible.

## Standard output format

Always produce:

### Detected Project Type
State the likely project type.

### Files to Create
List the files that should be added.

### Files to Update
List files that may need edits.

### Starter Workflow
Explain how to start with:
- Architect
- Builder
- Tester

### Missing Setup
List anything still missing.

## Prompt discipline

All work should follow:

- Context
- Goal
- Constraints
- Files involved
- Expected output
- Done criteria

## Safety rules

- Do not execute arbitrary shell commands unless the user explicitly asks.
- Do not add dependencies unless necessary.
- Do not rewrite unrelated files.
- Prefer text templates and instructions over automation scripts unless the user requests install automation.

## Success criteria

This skill is successful when:

- the project contains the full AI operating structure
- agent roles are clearly separated
- reusable docs and templates are present
- the repo is ready for Architect, Builder, and Tester workflows
