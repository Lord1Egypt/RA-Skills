---
name: speckit
description: "GitHub Spec-Kit integration for Spec-Driven Development (SDD). Use when: (1) initializing a new Spec-Kit project, (2) creating/updating project constitution, (3) writing feature specifications, (4) planning technical implementation, (5) generating task breakdowns, (6) implementing features from specs, (7) clarifying requirements, (8) cross-artifact analysis, (9) managing extensions and presets, (10) reassigning Paperclip issues. Triggers on: speckit, spec-kit, spec driven, constitution, specification, /speckit.*, feature spec, implementation plan."
---

# Spec-Kit — Spec-Driven Development (SDD)

> GitHub 官方開源工具包 (v0.4.3)，將規格驅動開發引入 AI Agent 工作流程。
> Repo: https://github.com/github/spec-kit | License: MIT

## What is Spec-Driven Development?

Spec-Kit reverses traditional AI coding: **specifications are first-class citizens, code is a derived output.** Instead of "vibe coding" where you prompt AI directly, SDD follows a structured pipeline:

```
Constitution → Specify → Clarify → Plan → Tasks → Implement
```

Each phase has explicit inputs, outputs, and quality gates.

## Prerequisites

### CLI Installation

```bash
# Install Specify CLI (requires uv)
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v0.4.3

# Verify
specify check
```

**System requirements**: Python 3.11+, `uv`, Git, a supported AI agent.

### Agent Support

Spec-Kit supports 30+ AI agents. Key ones for our stack:

| Agent | Integration | Notes |
|-------|-------------|-------|
| Claude Code | `/speckit.*` slash commands | `.claude/commands/speckit.*.md` |
| Gemini CLI | `.gemini/commands/speckit.*.toml` | Standard |
| opencode | `/speckit.*` slash commands | Standard |
| Codex CLI | `--ai-skills` flag | Skills in `.agents/skills/` |
| GitHub Copilot | `/speckit.*` slash commands | VS Code native |

## Workflow Commands

### Core Pipeline

| Step | Command | Output | When |
|------|---------|--------|------|
| 0. Init | `specify init <project> --ai <agent>` | `.specify/` + commands | New project |
| 1. Constitution | `/speckit.constitution <description>` | `memory/constitution.md` | New project / principles |
| 2. Specify | `/speckit.specify <feature description>` | `specs/<NNN-feature>/spec.md` | Starting a new feature |
| 3. Clarify | `/speckit.clarify` | Updates `spec.md` clarifications | Before planning |
| 4. Plan | `/speckit.plan <tech stack description>` | `specs/<NNN-feature>/plan.md` + research | After spec approved |
| 5. Tasks | `/speckit.tasks` | `specs/<NNN-feature>/tasks.md` | After plan validated |
| 6. Implement | `/speckit.implement` | Code changes | Tasks defined |

### Optional Commands

| Command | Purpose | When |
|---------|---------|------|
| `/speckit.analyze` | Cross-artifact consistency & coverage analysis | Before final review |
| `/speckit.checklist` | Quality checklists (unit tests for specs) | Validate completeness |
| `/speckit.taskstoissues` | Convert tasks to GitHub Issues | Need project board sync |

## CLI Reference

### `specify init`

```bash
# New project
specify init my-project --ai claude

# Existing directory
specify init . --ai claude --force

# With Codex skills
specify init my-project --ai codex --ai-skills

# Skip git init
specify init my-project --ai claude --no-git

# Timestamp-based branch numbering
specify init my-project --ai claude --branch-numbering timestamp
```

### `specify check`

Verifies: `git` + all CLI agents configured in `AGENT_CONFIG`.

### Extension & Preset Management

```bash
# Extensions
specify extension search                    # Browse available
specify extension add <name>                # Install

# Presets
specify preset search                       # Browse available
specify preset add <name>                   # Install
```

## Project Structure

After `specify init`:

```
project-root/
├── .specify/
│   ├── memory/
│   │   └── constitution.md          # Project principles (Step 1)
│   ├── scripts/
│   │   ├── check-prerequisites.sh
│   │   ├── common.sh
│   │   ├── create-new-feature.sh    # Creates feature branch + spec dir
│   │   ├── setup-plan.sh
│   │   └── update-claude-md.sh
│   ├── templates/
│   │   ├── constitution-template.md
│   │   ├── spec-template.md
│   │   ├── plan-template.md
│   │   └── tasks-template.md
│   ├── extensions/
│   │   ├── catalog.json
│   │   └── <ext-id>/templates/
│   └── presets/
│       └── <preset-id>/templates/
├── specs/
│   └── 001-feature-name/
│       ├── spec.md                   # Feature specification (Step 2)
│       ├── plan.md                   # Technical plan (Step 4)
│       ├── research.md               # Phase 0 research output
│       ├── data-model.md             # Data model design
│       ├── quickstart.md             # Getting started guide
│       ├── contracts/                # API contracts
│       │   ├── api-spec.json
│       │   └── signalr-spec.md
│       └── tasks.md                  # Task breakdown (Step 5)
├── .claude/commands/
│   ├── speckit.constitution.md
│   ├── speckit.specify.md
│   ├── speckit.plan.md
│   ├── speckit.tasks.md
│   └── speckit.implement.md
└── [source code]
```

## Template Details

### Constitution (`memory/constitution.md`)

Defines **non-negotiable** project principles. All specs must comply.

Structure:
- **Core Principles** (I, II, III, ...) — Each with clear description
- **Additional Constraints** — Tech stack, compliance, security
- **Development Workflow** — Code review, testing gates
- **Governance** — Amendment rules, compliance verification

Only CEO/CTO may amend. Version: `X.Y.Z | Ratified: YYYY-MM-DD`

### Spec (`spec.md`)

Key sections:
- **Feature Branch**: `NNN-feature-name`
- **User Scenarios & Testing** — Prioritized user stories (P1, P2, P3), each independently testable
- **Edge Cases** — Boundary conditions, error scenarios
- **Requirements** — Functional + non-functional
- **Review & Acceptance Checklist** — Validation gates

### Plan (`plan.md`)

- **Summary** — Primary requirement + technical approach
- **Technical Context** — Language, dependencies, storage, testing, platform
- **Constitution Check** — Must pass before Phase 0
- **Project Structure** — File tree
- **Implementation Details** — Phase-by-phase breakdown

### Tasks (`tasks.md`)

Format: `[ID] [P?] [Story] Description`
- `[P]` = can run in parallel
- `[Story]` = which user story (US1, US2, ...)
- Organized by user story for independent implementation

## Extensions & Presets

### Template Resolution Priority (highest → lowest)

```
Project-local overrides (.specify/templates/overrides/)
    ↓
Presets (.specify/presets/<preset-id>/templates/)
    ↓
Extensions (.specify/extensions/<ext-id>/templates/)
    ↓
Core (.specify/templates/)
```

### Notable Community Extensions

| Extension | Purpose | Type |
|-----------|---------|------|
| spec-kit-jira | Sync specs to Jira Epics/Stories | integration |
| spec-kit-verify | Validate code vs spec artifacts | code (read-only) |
| spec-kit-cleanup | Post-implementation quality gate | code (read+write) |
| spec-kit-review | Comprehensive code review | code (read-only) |
| spec-kit-archive | Archive merged features | docs (read+write) |
| spec-kit-sync | Detect/resolve spec vs code drift | docs (read+write) |
| spec-kit-doctor | Project health diagnostics | visibility (read-only) |
| spec-kit-maqa-ext | Multi-agent QA coordinator | process |

### Notable Presets

| Preset | Purpose |
|--------|---------|
| pirate-speak | Fun localization demo |
| aide-in-place | In-place technology migrations |

## Paperclip Integration

### Reassign via API (use this, NOT shell scripts)

```bash
PAPERCLIP_API="http://localhost:3100/api"

# Reassign by agent ID
curl -s -X PATCH "$PAPERCLIP_API/issues/$ISSUE_ID" \
  -H "Content-Type: application/json" \
  -d "{\"assigneeAgentId\": \"$TARGET_AGENT_ID\"}"

# Comment on issue
curl -s -X POST "$PAPERCLIP_API/issues/$ISSUE_ID/comments" \
  -H "Content-Type: application/json" \
  -d "{\"body\": \"Description of work done\"}"
```

### Issue Lifecycle

```
Dev → implement → reassign code-reviewer → CTO review → reassign qa → PM confirms → done
Bug: Dev → fix → reassign cto → reassign qa → done
```

## Best Practices

1. **Spec before code** — Resist "write code first, document later"
2. **Constitution is law** — All PRs must verify compliance
3. **Prioritize user stories** — P1 is the MVP, each story independently testable
4. **Keep specs alive** — Update specs when implementation drifts, don't pretend
5. **Task granularity** — Each task 2-4 hours max, split large ones
6. **Use extensions** — Install verify + cleanup for automated quality gates
7. **Validate before implement** — Run `/speckit.analyze` + `/speckit.checklist`
8. **Clarify before planning** — `/speckit.clarify` reduces rework

## Common Pitfalls

- **Skipping constitution** → Agent makes inconsistent decisions
- **Overly vague specs** → AI hallucinates features or misses edge cases
- **No clarify step** → Plan includes wrong assumptions
- **Tasks too large** → AI loses context, produces buggy code
- **Not updating specs after changes** → Drift between spec and code
- **Ignoring constitution during plan** → Architecture violations

## Upgrade

```bash
uv tool install specify-cli --force --from git+https://github.com/github/spec-kit.git@v0.4.3
```

## References

- Official repo: https://github.com/github/spec-kit
- Methodology deep-dive: `spec-driven.md` in repo
- GitHub blog: https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
- Extension catalog: `extensions/catalog.community.json`
- Preset catalog: `presets/catalog.community.json`
- Addy Osmani's spec writing guide: https://addyosmani.com/blog/good-spec/
