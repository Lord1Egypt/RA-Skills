---
name: pma
description: Project development lifecycle management with a strict three-phase workflow (investigate, proposal, implement), file-based plan tracking in docs/plan/, task tracking in docs/task/, and claim-before-work multi-agent coordination. Use when handling feature development, bug fixes, refactors, planning, progress tracking, or multi-agent execution in an existing codebase. English-first for repository docs and remote-visible metadata; use Chinese docs only when the user explicitly requests a specific document in Chinese.
---

# PMA - Project Management Assistant

Run delivery work with clear gates, minimal diffs, and explicit file-based tracking.

Keep this entry file small. Load only the references needed for the current turn.

## Always-On Rules

1. Follow the three-phase workflow strictly: investigate -> proposal -> implement.
2. Do not implement before explicit approval such as `proceed`.
3. Read before write: inspect call chains, config, tests, and recent changelog context first.
4. Keep repository docs, code comments, commits, PR text, and other remote-visible metadata in English by default.
5. Do not use plan mode. Track plans only in `docs/plan/`.
6. Update task and plan files immediately; do not defer state sync.
7. Apply the Coding Principles below to every code change.
8. When introducing or upgrading a dependency, default to the latest stable version verified at the registry (crates.io / npmjs.com / pkg.go.dev), not at a version that came from a tutorial, prior PR, or model recall. Pin to a non-latest version only with a recorded reason. See `references/workflow.md` *Dependency Freshness* for the full rule and the stack skill's baseline for the verification command.
9. Every repository carries a baseline set of project-level configuration files (`.gitignore`, `.gitattributes`, `.editorconfig`, `LICENSE`, `README.md`, `.env.example`, plus stack-pinned toolchain files). See `references/delivery.md` *Repository Hygiene*.
10. Never hand-author or hand-edit database migration files. Migrations are produced by the project's migration tool / ORM (e.g. `sqlx migrate`, `sea-orm-migration`, `diesel migration`, Drizzle Kit, Prisma, Alembic) — change the model/schema, then let the tool emit the migration. Hand-written or restructured migrations desync from the tool's tracked state and break later auto-generated migrations. See `references/delivery.md` *Database Migrations*.

## Coding Principles

Behavioral guardrails for every edit. Bias toward caution over speed; for trivial tasks, use judgment.

### 1. Think Before Coding

Don't assume. Don't hide confusion. Surface tradeoffs.

- State assumptions explicitly; if uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so and push back when warranted.
- If something is unclear, stop, name what's confusing, and ask.

### 2. Simplicity First

Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked.
- No abstractions for single-use code.
- No flexibility or configurability that wasn't requested.
- No error handling for impossible scenarios.
- If 200 lines could be 50, rewrite it.
- Self-check: would a senior engineer say this is overcomplicated?

### 3. Surgical Changes

Touch only what you must. Clean up only your own mess.

- Don't improve adjacent code, comments, or formatting.
- Don't refactor code that isn't broken.
- Match existing style even if you'd do it differently.
- Mention unrelated dead code; do not delete it unless asked.
- Remove imports/variables/functions that YOUR changes made unused.
- Test: every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

Define success criteria. Loop until verified.

- Convert vague tasks into verifiable goals:
  - "Add validation" -> write tests for invalid inputs, then make them pass.
  - "Fix the bug" -> write a test that reproduces it, then make it pass.
  - "Refactor X" -> ensure tests pass before and after.
- For multi-step work, state a brief plan with a verify step per item:
  1. [Step] -> verify: [check]
  2. [Step] -> verify: [check]
- Strong criteria enable independent iteration; weak criteria ("make it work") require constant clarification.

## Core Workflow

### Phase 1: Investigation

- trace upstream and downstream impact
- inspect related code, tests, config, docs, and recent changelog entries
- find or create the matching task in `docs/task/index.md`
- claim the task before implementation
- create a plan file for non-trivial work

### Phase 2: Proposal

Output these items, then stop for approval:

- current state
- proposal
- risks
- scope
- alternatives when they matter

### Phase 3: Implement -> Verify -> Record

After approval:

- set task and plan status to in progress
- implement the approved scope
- run focused verification
- mark task and plan completed
- update changelog when needed

## Reference Packs

Load only what the current task needs:

- `references/workflow.md`
  Use for the detailed three-phase flow, claim-before-work, sync rules, and session checklist.
- `references/docs-and-tracking.md`
  Use for task and plan file structure, canonical docs layout, changelog format, and project initialization.
- `references/delivery.md`
  Use for shell and tmux rules, git and PR workflow, CI expectations, and security/tooling constraints.
- `references/dev-environment.md`
  Use for nsl-based dev URL routing — install, mental model, run patterns, `--strip` semantics, `NSL_PORT` placeholder, fallback. Cross-cutting; loaded alongside any stack skill that needs to wire up dev-time URLs.

## Canonical Format References

Use these format files instead of redefining schemas inline:

- [docs/task-format.md](docs/task-format.md)
- [docs/plan-format.md](docs/plan-format.md)
- [docs/monorepo-example.md](docs/monorepo-example.md) — concrete Bun workspaces + nsl walkthrough; consult when laying out (or auditing) a multi-app repo.
- [docs/project-injection.md](docs/project-injection.md) — `AGENTS.md` template (with `CLAUDE.md` as a symlink) for activating PMA in a new (or audited) project. Load when bootstrapping a repo or when an existing project's `AGENTS.md` looks thin compared to the current rule set.

## Quick Routing

Choose references by intent:

- New feature, bug fix, or refactor: load `references/workflow.md` and `references/docs-and-tracking.md`.
- Task claiming, ownership, or status sync: load `references/workflow.md`.
- Task or plan file creation: load `references/docs-and-tracking.md`.
- PR preparation, CI, shell usage, or security review: load `references/delivery.md`.
- Repository initialization or hygiene audit (`.gitignore`, `.gitattributes`, `.editorconfig`, `LICENSE`, `README.md`, `.env.example`, toolchain pinning): load `references/delivery.md` *Repository Hygiene*.
- Any database schema change or migration: load `references/delivery.md` *Database Migrations*.
- Bootstrapping a new project, or auditing an existing project's `AGENTS.md` injection (and verifying `CLAUDE.md` is a symlink to it): load `docs/project-injection.md`.
- Introducing or upgrading a dependency: load `references/workflow.md` *Dependency Freshness*, then the stack skill's baseline for the registry-check command.
- Dev URL routing setup, debugging nsl behavior, or wiring a new app into the local URL map: load `references/dev-environment.md`.
- Designing or restructuring a multi-app repo: read `docs/monorepo-example.md` together with the relevant stack skill's *Monorepo* section.

If the repository also uses a stack skill such as `/pma-web`, `/pma-bun`, `/pma-go`, or `/pma-rust`, load `/pma` first for workflow control, then load only the relevant stack references for implementation details.
