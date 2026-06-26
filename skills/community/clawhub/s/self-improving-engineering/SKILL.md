---
name: self-improving-engineering
description: "Captures architecture decisions, code quality issues, build/deploy failures, dependency problems, performance regressions, tech debt accumulation, and test gaps for continuous engineering improvement. Use when: (1) A build or deployment fails, (2) An architecture violation is discovered, (3) A test gap or flaky test is found, (4) A dependency CVE or breaking change surfaces, (5) A performance regression is detected, (6) Code review reveals design flaws, (7) Tech debt accumulates past a threshold."
metadata:
---

# Self-Improving Engineering Skill

Log engineering learnings, issues, and feature requests to markdown files for continuous improvement. Captures architecture decisions, build failures, test gaps, performance regressions, dependency problems, and code quality issues. Important learnings get promoted to architecture decision records, coding standards, and CI/CD runbooks.

## First-Use Initialisation

Before logging anything, ensure the `.learnings/` directory and files exist in the project or workspace root. If any are missing, create them:

```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# Engineering Learnings\n\nArchitecture decisions, code quality insights, and engineering knowledge captured during development.\n\n**Categories**: architecture_debt | code_smell | performance_regression | dependency_issue | testing_gap | design_flaw\n**Areas**: design | implementation | code_review | ci_cd | deployment | monitoring\n\n---\n" > .learnings/LEARNINGS.md
[ -f .learnings/ENGINEERING_ISSUES.md ] || printf "# Engineering Issues Log\n\nBuild failures, deployment errors, performance regressions, and infrastructure problems.\n\n---\n" > .learnings/ENGINEERING_ISSUES.md
[ -f .learnings/FEATURE_REQUESTS.md ] || printf "# Feature Requests\n\nEngineering capabilities, tooling improvements, and infrastructure enhancements requested during development.\n\n---\n" > .learnings/FEATURE_REQUESTS.md
```

Never overwrite existing files. This is a no-op if `.learnings/` is already initialised.

Do not log secrets, tokens, private keys, environment variables, or full config files unless the user explicitly asks for that level of detail. Prefer short summaries or redacted excerpts over raw command output or full stack traces.

Use a manual-first workflow by default. If you want reminders, use the opt-in hook workflow described in [Hook Integration](#hook-integration).

## Quick Reference

| Situation | Action |
|-----------|--------|
| Build fails (CI or local) | Log to `.learnings/ENGINEERING_ISSUES.md` with build context |
| Architecture violation discovered | Log to `.learnings/LEARNINGS.md` with category `architecture_debt` |
| Test flake or gap identified | Log to `.learnings/LEARNINGS.md` with category `testing_gap` |
| Dependency CVE or breaking change | Log to `.learnings/ENGINEERING_ISSUES.md` with dependency details |
| Performance regression detected | Log to `.learnings/ENGINEERING_ISSUES.md` with metrics/benchmarks |
| Code smell found during review | Log to `.learnings/LEARNINGS.md` with category `code_smell` |
| Design flaw surfaces | Log to `.learnings/LEARNINGS.md` with category `design_flaw` |
| User requests engineering capability | Log to `.learnings/FEATURE_REQUESTS.md` |
| Deployment rollback triggered | Log to `.learnings/ENGINEERING_ISSUES.md` with rollback reason |
| N+1 query or slow path found | Log to `.learnings/LEARNINGS.md` with category `performance_regression` |
| Similar to existing entry | Link with `**See Also**`, consider priority bump |
| Broadly applicable pattern | Promote to ADR, coding standards, or CI/CD runbook |
| Design pattern proven in practice | Promote to `SOUL.md` (OpenClaw workspace) |
| CI/CD workflow improvement | Promote to `AGENTS.md` (OpenClaw workspace) |
| Build tool or infra gotcha | Promote to `TOOLS.md` (OpenClaw workspace) |

## OpenClaw Setup (Recommended)

OpenClaw is the primary platform for this skill. It uses workspace-based prompt injection with automatic skill loading.

### Installation

**Via ClawdHub (recommended):**
```bash
clawdhub install self-improving-engineering
```

**Manual:**
```bash
git clone https://github.com/jose-compu/self-improving-engineering.git ~/.openclaw/skills/self-improving-engineering
```

### Workspace Structure

OpenClaw injects these files into every session:

```
~/.openclaw/workspace/
├── AGENTS.md          # CI/CD workflows, deployment patterns, multi-agent coordination
├── SOUL.md            # Design principles, architecture guidelines, coding standards
├── TOOLS.md           # Build tools, test frameworks, dependency managers, infra gotchas
├── MEMORY.md          # Long-term memory (main session only)
├── memory/            # Daily memory files
│   └── YYYY-MM-DD.md
└── .learnings/        # This skill's log files
    ├── LEARNINGS.md
    ├── ENGINEERING_ISSUES.md
    └── FEATURE_REQUESTS.md
```

### Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Then create the log files (or copy from `assets/`):
- `LEARNINGS.md` — architecture decisions, code quality insights, design patterns
- `ENGINEERING_ISSUES.md` — build failures, deploy errors, performance regressions
- `FEATURE_REQUESTS.md` — tooling improvements, infrastructure enhancements

### Promotion Targets

When learnings prove broadly applicable, promote them to workspace files:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Design patterns & principles | `SOUL.md` | "Prefer composition over inheritance for service layer" |
| CI/CD workflows & deploy patterns | `AGENTS.md` | "Run migration check before deploy" |
| Build tool & infra gotchas | `TOOLS.md` | "Node 20 breaks native modules; pin to 18 LTS" |

### Optional: Enable Hook

For lightweight reminders at session start (recommended: activator only):

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-engineering
openclaw hooks enable self-improving-engineering
```

See `references/openclaw-integration.md` for complete details.

---

## Generic Setup (Other Agents)

For Claude Code, Codex, Copilot, or other agents, create `.learnings/` in the project or workspace root:

```bash
mkdir -p .learnings
```

Create the files inline using the headers shown above. Avoid reading templates from the current repo or workspace unless you explicitly trust that path.

### Add reference to agent files AGENTS.md, CLAUDE.md, or .github/copilot-instructions.md to remind yourself to log engineering learnings. (this is an alternative to hook-based reminders)

#### Self-Improving Engineering Workflow

When engineering issues or architectural discoveries occur:
1. Log to `.learnings/ENGINEERING_ISSUES.md`, `LEARNINGS.md`, or `FEATURE_REQUESTS.md`
2. Review and promote broadly applicable learnings to:
   - Architecture Decision Records (ADRs) in `docs/decisions/`
   - Coding standards in `CLAUDE.md` or `.github/copilot-instructions.md`
   - CI/CD runbooks in `AGENTS.md`

## Logging Format

### Learning Entry

Append to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: design | implementation | code_review | ci_cd | deployment | monitoring

### Summary
One-line description of the engineering learning

### Details
Full context: what was discovered, why it matters, what the correct approach is

### Suggested Action
Specific fix, refactoring step, or architectural change to make

### Metadata
- Source: build_failure | test_failure | code_review | deployment | monitoring | investigation
- Category: architecture_debt | code_smell | performance_regression | dependency_issue | testing_gap | design_flaw
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (if related to existing entry)
- Pattern-Key: arch.circular_dependency | perf.n_plus_one | test.missing_integration (optional)
- Recurrence-Count: 1 (optional)
- First-Seen: 2025-01-15 (optional)
- Last-Seen: 2025-01-15 (optional)

---
```

**Categories**:
- `architecture_debt` — coupling, circular dependencies, layer violations, missing abstractions
- `code_smell` — long methods, god classes, feature envy, primitive obsession
- `performance_regression` — N+1 queries, memory leaks, slow endpoints, missing indexes
- `dependency_issue` — CVEs, version conflicts, breaking upgrades, deprecated packages
- `testing_gap` — missing integration tests, untested edge cases, flaky tests
- `design_flaw` — wrong pattern choice, API contract issues, data model problems

### Engineering Issue Entry

Append to `.learnings/ENGINEERING_ISSUES.md`:

```markdown
## [ENG-YYYYMMDD-XXX] issue_type

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: design | implementation | code_review | ci_cd | deployment | monitoring

### Summary
Brief description of the engineering issue

### Error
```
Actual error message, build output, or test failure
```

### Context
- Build/deploy step that failed
- Environment details (CI runner, Node version, OS)
- Input or configuration that triggered the issue
- Summary or redacted excerpt of relevant output

### Impact
What is blocked or degraded by this issue

### Suggested Fix
If identifiable, what might resolve this

### Metadata
- Reproducible: yes | no | unknown
- Environment: local | ci | staging | production
- Related Files: path/to/file.ext
- See Also: ENG-20250110-001 (if recurring)

---
```

### Feature Request Entry

Append to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: design | implementation | code_review | ci_cd | deployment | monitoring

### Requested Capability
What engineering capability or tooling improvement is needed

### Engineering Context
Why this is needed, what pain point it addresses, what breaks without it

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
Architecture approach, libraries to evaluate, integration points

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature_name

---
```

## ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` (learning), `ENG` (engineering issue), `FEAT` (feature request)
- YYYYMMDD: Current date
- XXX: Sequential number or random 3 chars (e.g., `001`, `A7B`)

Examples: `LRN-20250115-001`, `ENG-20250115-A3F`, `FEAT-20250115-002`

## Resolving Entries

When an issue is fixed, update the entry:

1. Change `**Status**: pending` → `**Status**: resolved`
2. Add resolution block after Metadata:

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Commit/PR**: abc123 or #42
- **Root Cause**: Brief description of actual root cause
- **Notes**: What was done and any follow-up needed
```

Other status values:
- `in_progress` — Actively being worked on
- `wont_fix` — Decided not to address (add reason in Resolution notes)
- `promoted` — Elevated to ADR, coding standard, or CI/CD runbook
- `promoted_to_skill` — Extracted as a reusable skill

## Promoting to Project Memory

When a learning is broadly applicable (not a one-off fix), promote it to permanent project memory.

### When to Promote

- Learning applies across multiple services or modules
- Knowledge any engineer (human or AI) should know about the codebase
- Prevents recurring build failures or deployment issues
- Documents architecture decisions and their rationale
- Establishes a coding standard or testing requirement

### Promotion Targets

| Target | What Belongs There |
|--------|-------------------|
| `docs/decisions/ADR-NNN.md` | Architecture decisions with context and consequences |
| `CLAUDE.md` | Project facts, build conventions, gotchas for all Claude interactions |
| `AGENTS.md` | CI/CD workflows, deployment patterns, automation rules |
| `.github/copilot-instructions.md` | Project context and conventions for GitHub Copilot |
| `SOUL.md` | Design principles, coding philosophy, architecture guidelines (OpenClaw) |
| `TOOLS.md` | Build tools, test frameworks, dependency manager gotchas (OpenClaw) |
| `.github/CODING_STANDARDS.md` | Team coding standards and conventions |

### How to Promote

1. **Distill** the learning into a concise rule, ADR, or standard
2. **Add** to appropriate section in target file (create file if needed)
3. **Update** original entry:
   - Change `**Status**: pending` → `**Status**: promoted`
   - Add `**Promoted**: docs/decisions/ADR-007.md` or target file

### Promotion Examples

**Learning** (verbose):
> Discovered circular dependency between UserService and AuthService. UserService imports AuthService for token validation, AuthService imports UserService for user lookup. Causes test isolation failures and makes both services untestable independently.

**As ADR** (concise):
```markdown
# ADR-007: Break circular service dependencies with event bus

## Status: Accepted

## Context
UserService and AuthService have circular imports causing test isolation failures.

## Decision
Use an event bus for cross-service communication. Services publish events instead of direct imports.

## Consequences
- Services become independently testable
- Adds event bus infrastructure dependency
- Requires eventual consistency for cross-service queries
```

## Recurring Pattern Detection

If logging something similar to an existing entry:

1. **Search first**: `grep -r "keyword" .learnings/`
2. **Link entries**: Add `**See Also**: ENG-20250110-001` in Metadata
3. **Bump priority** if issue keeps recurring
4. **Consider systemic fix**: Recurring issues often indicate:
   - Flaky tests → missing test isolation or shared state (→ coding standard)
   - Repeated build failures → missing CI validation step (→ CI/CD runbook)
   - Recurring dependency conflicts → missing lockfile discipline (→ `TOOLS.md`)
   - Architecture violations keep appearing → missing fitness functions (→ ADR)
   - Same code smell in multiple PRs → missing linter rule (→ `.eslintrc` or coding standard)

## Simplify & Harden Feed

Use this workflow to ingest recurring engineering patterns from the `simplify-and-harden` skill and turn them into durable engineering guidance.

### Ingestion Workflow

1. Read `simplify_and_harden.learning_loop.candidates` from the task summary.
2. For each candidate, use `pattern_key` as the stable dedupe key.
3. Search `.learnings/LEARNINGS.md` for an existing entry with that key:
   - `grep -n "Pattern-Key: <pattern_key>" .learnings/LEARNINGS.md`
4. If found:
   - Increment `Recurrence-Count`
   - Update `Last-Seen`
   - Add `See Also` links to related entries/tasks
5. If not found:
   - Create a new `LRN-...` entry
   - Set `Source: simplify-and-harden`
   - Set `Pattern-Key`, `Recurrence-Count: 1`, and `First-Seen`/`Last-Seen`

### Promotion Rule (System Prompt Feedback)

Promote recurring patterns into agent context/system prompt files when all are true:

- `Recurrence-Count >= 3`
- Seen across at least 2 distinct tasks or services
- Occurred within a 30-day window

Promotion targets:
- `CLAUDE.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`
- `SOUL.md` / `TOOLS.md` for OpenClaw workspace-level guidance when applicable

Write promoted rules as short prevention rules (what to check before/while coding), not long incident write-ups.

## Periodic Review

Review `.learnings/` at natural engineering breakpoints:

### When to Review
- Before cutting a release or deploying to production
- After a production incident or rollback
- During sprint retrospectives
- When onboarding to a new service or module
- After dependency upgrades or migration work

### Quick Status Check
```bash
# Count pending engineering items
grep -h "Status\*\*: pending" .learnings/*.md | wc -l

# List pending high-priority items
grep -B5 "Priority\*\*: high" .learnings/*.md | grep "^## \["

# Find learnings for a specific area
grep -l "Area\*\*: ci_cd" .learnings/*.md

# Find all architecture debt entries
grep -B2 "Category.*architecture_debt" .learnings/LEARNINGS.md | grep "^## \["
```

### Review Actions
- Resolve fixed items
- Promote applicable learnings to ADRs or coding standards
- Link related entries
- Escalate recurring issues to tech debt backlog
- Create follow-up tickets for unresolved critical items

## Detection Triggers

Automatically log when you notice:

**Build Failures** (→ engineering issue):
- CI pipeline fails with compilation errors
- Docker build breaks on dependency resolution
- Webpack/Vite/esbuild bundler errors
- Type checking failures in CI

**Test Failures** (→ engineering issue or learning with `testing_gap`):
- Test suite goes red after changes
- Flaky test detected (passes locally, fails in CI)
- Coverage drops below threshold
- Integration test timeout

**Code Review Feedback** (→ learning with appropriate category):
- Reviewer flags architecture violation
- PR rejected for missing tests
- Design pattern concerns raised
- Performance concerns noted in review

**Deployment Issues** (→ engineering issue):
- Deployment rollback triggered
- Health check failures after deploy
- Migration script errors
- Configuration drift between environments

**Performance Alerts** (→ learning with `performance_regression`):
- Response time increases past threshold
- Memory usage spikes
- Database query time degrades
- Benchmark regression detected

**Dependency Audit Warnings** (→ engineering issue):
- `npm audit` / `pnpm audit` finds vulnerabilities
- Dependabot/Renovate flags CVE
- Breaking change in minor/patch version
- Deprecated package still in use

## Priority Guidelines

| Priority | When to Use |
|----------|-------------|
| `critical` | Production outage, data loss risk, security vulnerability (CVE with exploit), service completely down |
| `high` | Build broken on main, test suite red, blocking deployment, dependency CVE without known exploit |
| `medium` | Tech debt accumulating, code smell in frequently-changed module, missing tests for happy path |
| `low` | Style inconsistency, documentation gap, minor code smell in stable code, nice-to-have refactor |

## Area Tags

Use to filter learnings by engineering concern:

| Area | Scope |
|------|-------|
| `design` | Architecture decisions, system design, API contracts, data modeling |
| `implementation` | Code quality, algorithms, data structures, business logic |
| `code_review` | Review feedback, PR patterns, merge conflicts, coding standards |
| `ci_cd` | Build pipelines, test automation, artifact management, CI configuration |
| `deployment` | Release process, infrastructure, containers, orchestration, rollbacks |
| `monitoring` | Observability, alerting, logging, tracing, SLO/SLA tracking |

## Best Practices

1. **Log immediately** — context is freshest right after the build breaks or the review lands
2. **Include the error output** — future agents need the exact error message to pattern-match
3. **Record the environment** — Node version, OS, CI runner matter for reproducibility
4. **Link the PR or commit** — makes root cause traceable
5. **Suggest concrete fixes** — not just "investigate" but "add index on users.email"
6. **Categorize precisely** — enables filtering by architecture_debt vs code_smell vs testing_gap
7. **Promote aggressively** — if it broke the build twice, it belongs in coding standards
8. **Track recurrence** — third time is a systemic issue, not a one-off

## Gitignore Options

**Keep learnings local** (per-developer):
```gitignore
.learnings/
```

This is the default to avoid committing sensitive or noisy local logs by accident.

**Track learnings in repo** (team-wide):
Don't add to .gitignore — learnings become shared engineering knowledge.

**Hybrid** (track templates, ignore entries):
```gitignore
.learnings/*.md
!.learnings/.gitkeep
```

## Hook Integration

Enable reminders through agent hooks only when needed. This is **opt-in** — you must explicitly configure hooks.

### Conservative Mode (Recommended)

- Default to **no hooks** and log manually; if reminders are useful, enable `UserPromptSubmit` with `scripts/activator.sh` only.
- Enable `PostToolUse` (`scripts/error-detector.sh`) only in trusted environments when you explicitly want command-output pattern checks.

### Quick Setup (Claude Code / Codex)

Create `.claude/settings.json` in your project:

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-engineering/scripts/activator.sh"
      }]
    }]
  }
}
```

This injects a lightweight engineering learning reminder after each prompt (~50-100 tokens overhead).

For advanced setup with `PostToolUse` error detection, see `references/hooks-setup.md`. Keep it disabled unless you explicitly want tool-output pattern checks.

| Script | Hook Type | Purpose |
|--------|-----------|---------|
| `scripts/activator.sh` | UserPromptSubmit | Reminds to evaluate engineering learnings after tasks |
| `scripts/error-detector.sh` | PostToolUse (Bash) | Triggers on build errors, test failures, dep vulnerabilities |

## Automatic Skill Extraction

When a learning is valuable enough to become a reusable skill, extract it using the provided helper.

### Skill Extraction Criteria

A learning qualifies for skill extraction when ANY of these apply:

| Criterion | Description |
|-----------|-------------|
| **Recurring** | Has `See Also` links to 2+ similar issues |
| **Verified** | Status is `resolved` with working fix |
| **Non-obvious** | Required actual debugging/investigation to discover |
| **Broadly applicable** | Not project-specific; useful across codebases |
| **User-flagged** | User says "save this as a skill" or similar |

### Extraction Workflow

1. **Identify candidate**: Learning meets extraction criteria
2. **Run helper** (or create manually):
   ```bash
   ./skills/self-improving-engineering/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improving-engineering/scripts/extract-skill.sh skill-name
   ```
3. **Customize SKILL.md**: Fill in template with learning content
4. **Update learning**: Set status to `promoted_to_skill`, add `Skill-Path`
5. **Verify**: Read skill in fresh session to ensure it's self-contained

### Manual Extraction

1. Create `skills/<skill-name>/SKILL.md` using template from `assets/SKILL-TEMPLATE.md`
2. Follow [Agent Skills spec](https://agentskills.io/specification): YAML frontmatter with `name` and `description`, name matches folder name
3. Before extracting, verify: solution is tested, description is context-free, no hardcoded values, follows naming conventions

## Multi-Agent Support

| Agent | Activation | Setup |
|-------|-----------|-------|
| Claude Code | Hooks (UserPromptSubmit, PostToolUse) | `.claude/settings.json` |
| Codex CLI | Hooks (same as Claude Code) | `.codex/settings.json` |
| GitHub Copilot | Manual (no hooks) | `.github/copilot-instructions.md` |
| OpenClaw | Workspace injection + inter-agent messaging | See "OpenClaw Setup" above |

### Agent-Agnostic Guidance

Regardless of agent, apply self-improving engineering when you:

1. **Hit a build failure** — especially if the fix wasn't obvious
2. **Discover an architecture violation** — coupling, circular deps, layer breaches
3. **Find missing tests** — gaps in coverage for critical paths
4. **Encounter a dependency problem** — CVE, version conflict, breaking change
5. **Detect a performance regression** — N+1 query, memory leak, slow endpoint
6. **Receive review feedback** — design concerns, code smells, pattern violations

## Stackability Contract (Standalone + Multi-Skill)

This skill is standalone-compatible and stackable with other self-improving skills.

### Namespaced Logging (recommended for 2+ skills)
- Namespace for this skill: `.learnings/engineering/`
- Keep current standalone behavior if you prefer flat files.
- Optional shared index for all skills: `.learnings/INDEX.md`

### Required Metadata
Every new entry must include:

```markdown
**Skill**: engineering
```

### Hook Arbitration (when 2+ skills are enabled)
- Use one dispatcher hook as the single entrypoint.
- Dispatcher responsibilities: route by matcher, dedupe repeated events, and rate-limit reminders.
- Suggested defaults: dedupe key = `event + matcher + file + 5m_window`; max 1 reminder per skill every 5 minutes.

### Narrow Matcher Scope (engineering)
Only trigger this skill automatically for engineering signals such as:
- `build failed|ci failed|deploy failed|rollback|pipeline`
- `dependency|version conflict|coverage drop|performance regression`
- explicit engineering intent in user prompt

### Cross-Skill Precedence
When guidance conflicts, apply:
1. `security`
2. `engineering`
3. `coding`
4. `ai`
5. user-explicit domain skill
6. `meta` as tie-breaker

### Ownership Rules
- This skill writes only to `.learnings/engineering/` in stackable mode.
- It may read other skill folders for cross-linking, but should not rewrite their entries.
