---
name: self-improving-coding
description: "Captures lint errors, type mismatches, runtime bugs, anti-patterns, refactoring opportunities, language idiom gaps, debugging insights, and tooling issues to enable continuous coding improvement. Use when: (1) A lint or type error occurs, (2) A runtime exception is thrown, (3) An anti-pattern is identified in code, (4) A refactoring opportunity is discovered, (5) A better language idiom is found, (6) A debugging breakthrough reveals root cause, (7) A tooling issue blocks development."
---

# Self-Improving Coding Skill

Log coding-specific learnings, bug patterns, and feature requests to markdown files for continuous improvement. Captures lint errors, type mismatches, runtime bugs, anti-patterns, refactoring opportunities, language idiom gaps, debugging insights, and tooling issues. Important learnings get promoted to style guides, lint rules, code snippet libraries, or debug playbooks.

## First-Use Initialisation

Before logging anything, ensure the `.learnings/` directory and files exist in the project or workspace root. If any are missing, create them:

```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# Coding Learnings\n\nBug patterns, anti-patterns, idiom gaps, debugging insights, and tooling issues captured during development.\n\n**Categories**: bug_pattern | anti_pattern | refactor_opportunity | idiom_gap | tooling_issue | debugging_insight\n**Areas**: syntax | logic | data_structures | algorithms | error_handling | testing | tooling\n\n---\n" > .learnings/LEARNINGS.md
[ -f .learnings/BUG_PATTERNS.md ] || printf "# Bug Patterns Log\n\nRecurring bugs, common mistakes, and error patterns.\n\n---\n" > .learnings/BUG_PATTERNS.md
[ -f .learnings/FEATURE_REQUESTS.md ] || printf "# Feature Requests\n\nCoding tools, capabilities, and automation requests.\n\n---\n" > .learnings/FEATURE_REQUESTS.md
```

Never overwrite existing files. This is a no-op if `.learnings/` is already initialised.

Do not log secrets, tokens, private keys, or environment variables. Prefer short summaries or redacted excerpts over raw stack traces or full source files.

If you want automatic reminders, use the opt-in hook workflow described in [Hook Integration](#hook-integration).

## Quick Reference

| Situation | Action |
|-----------|--------|
| Lint error encountered | Log to `.learnings/BUG_PATTERNS.md` with error rule and fix |
| Type error from checker | Log to `.learnings/BUG_PATTERNS.md` with type mismatch details |
| Runtime exception thrown | Log to `.learnings/BUG_PATTERNS.md` with stack trace summary |
| Anti-pattern found in code | Log to `.learnings/LEARNINGS.md` with category `anti_pattern` |
| Refactoring opportunity | Log to `.learnings/LEARNINGS.md` with category `refactor_opportunity` |
| Better idiom discovered | Log to `.learnings/LEARNINGS.md` with category `idiom_gap` |
| Debugging breakthrough | Log to `.learnings/LEARNINGS.md` with category `debugging_insight` |
| Tooling issue encountered | Log to `.learnings/LEARNINGS.md` with category `tooling_issue` |
| Recurring bug pattern | Link with `**See Also**`, consider priority bump |
| Broadly applicable pattern | Promote to style guide, lint rule, or debug playbook |
| Reusable code solution | Promote to code snippets library |

## OpenClaw Setup (Recommended)

OpenClaw is the primary platform for this skill. It uses workspace-based prompt injection with automatic skill loading.

### Installation

**Via ClawdHub (recommended):**
```bash
clawdhub install self-improving-coding
```

**Manual:**
```bash
git clone https://github.com/jose-compu/self-improving-coding.git ~/.openclaw/skills/self-improving-coding
```

### Workspace Structure

OpenClaw injects these files into every session:

```
~/.openclaw/workspace/
├── AGENTS.md          # Multi-agent workflows, delegation patterns
├── SOUL.md            # Behavioral guidelines, personality, principles
├── TOOLS.md           # Tool capabilities, integration gotchas
├── MEMORY.md          # Long-term memory (main session only)
├── memory/            # Daily memory files
│   └── YYYY-MM-DD.md
└── .learnings/        # This skill's log files
    ├── LEARNINGS.md
    ├── BUG_PATTERNS.md
    └── FEATURE_REQUESTS.md
```

### Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Then create the log files (or copy from `assets/`):
- `LEARNINGS.md` — anti-patterns, idiom gaps, debugging insights, tooling issues
- `BUG_PATTERNS.md` — lint errors, type mismatches, runtime exceptions, recurring bugs
- `FEATURE_REQUESTS.md` — coding tools, automation, IDE capabilities

### Promotion Targets

When coding learnings prove broadly applicable, promote them:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Code style patterns | Style guide | "Always use early returns over nested if/else" |
| Recurring lint fixes | Lint rules (`.eslintrc`, `ruff.toml`) | "Disallow mutable default arguments" |
| Reusable solutions | Code snippets library | "Retry with exponential backoff" |
| Debugging workflows | Debug playbooks | "Race condition diagnosis steps" |
| Tool configuration | `TOOLS.md` | "TypeScript strict mode catches 80% of null bugs" |
| Workflow patterns | `AGENTS.md` | "Run type checker before committing" |

### Optional: Enable Hook

For automatic reminders at session start:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-coding
openclaw hooks enable self-improving-coding
```

See `references/openclaw-integration.md` for complete details.

---

## Generic Setup (Other Agents)

For Claude Code, Codex, Copilot, or other agents, create `.learnings/` in the project or workspace root:

```bash
mkdir -p .learnings
```

Create the files inline using the headers shown above.

### Add reference to agent files

Add to `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md`:

#### Self-Improving Coding Workflow

When coding errors or patterns are discovered:
1. Log to `.learnings/BUG_PATTERNS.md`, `LEARNINGS.md`, or `FEATURE_REQUESTS.md`
2. Review and promote broadly applicable learnings to:
   - Style guides — code style and convention rules
   - Lint configuration — `.eslintrc`, `ruff.toml`, `pylintrc`
   - Code snippets — reusable solution templates
   - Debug playbooks — step-by-step diagnosis guides

## Logging Format

### Learning Entry [LRN-YYYYMMDD-XXX]

Append to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: syntax | logic | data_structures | algorithms | error_handling | testing | tooling

### Summary
One-line description of the coding insight

### Details
Full context: what code pattern was found, why it is problematic or beneficial,
what the correct idiom or approach is. Include minimal code snippets.

### Code Example

**Before (problematic):**
\`\`\`language
// problematic code
\`\`\`

**After (correct):**
\`\`\`language
// improved code
\`\`\`

### Suggested Action
Specific refactor, lint rule, or coding guideline to adopt

### Metadata
- Source: lint_error | type_checker | runtime_exception | code_review | profiler | static_analysis
- Language: python | typescript | javascript | rust | go | java | other
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (if related to existing entry)
- Pattern-Key: anti_pattern.mutable_default | idiom.list_comprehension (optional)
- Recurrence-Count: 1 (optional)
- First-Seen: 2025-01-15 (optional)
- Last-Seen: 2025-01-15 (optional)

---
```

**Categories for learnings:**

| Category | Use When |
|----------|----------|
| `bug_pattern` | Recurring bug class (off-by-one, null deref, race condition) |
| `anti_pattern` | Code pattern that leads to bugs or maintenance burden |
| `refactor_opportunity` | Code that works but should be restructured |
| `idiom_gap` | Using non-idiomatic approach when a better idiom exists |
| `tooling_issue` | Build tool, linter, formatter, or IDE problem |
| `debugging_insight` | Technique or approach that revealed root cause |

### Bug Pattern Entry [BUG-YYYYMMDD-XXX]

Append to `.learnings/BUG_PATTERNS.md`:

```markdown
## [BUG-YYYYMMDD-XXX] error_type_or_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: syntax | logic | data_structures | algorithms | error_handling | testing | tooling

### Summary
Brief description of the bug pattern

### Error Output
\`\`\`
Actual error message, lint output, or stack trace (redacted/summarized)
\`\`\`

### Root Cause
What in the code caused this error. Include the problematic code snippet.

### Fix
\`\`\`language
// corrected code
\`\`\`

### Prevention
How to avoid this bug in the future (lint rule, type annotation, assertion, test)

### Context
- Trigger: lint | type_checker | runtime | test_failure | code_review
- Language: python | typescript | javascript | rust | go | java
- Framework: react | express | django | flask | fastapi (if applicable)
- Input or parameters that triggered the bug

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: BUG-20250110-001 (if recurring)

---
```

### Feature Request Entry [FEAT-YYYYMMDD-XXX]

Append to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: syntax | logic | data_structures | algorithms | error_handling | testing | tooling

### Requested Capability
What coding tool, automation, or capability is needed

### User Context
Why it's needed, what workflow it improves, what problem it solves

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built: lint plugin, IDE extension, script, code generator

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_tool_or_feature

---
```

## ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` (learning), `BUG` (bug pattern), `FEAT` (feature request)
- YYYYMMDD: Current date
- XXX: Sequential number or random 3 chars (e.g., `001`, `A7B`)

Examples: `LRN-20250415-001`, `BUG-20250415-A3F`, `FEAT-20250415-002`

## Resolving Entries

When an issue is fixed, update the entry:

1. Change `**Status**: pending` → `**Status**: resolved`
2. Add resolution block after Metadata:

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Commit/PR**: abc123 or #42
- **Notes**: Added lint rule / updated style guide / created snippet
```

Other status values:
- `in_progress` — Actively being refactored or fixed
- `wont_fix` — Decided not to address (add reason in Resolution notes)
- `promoted` — Elevated to style guide, lint config, or debug playbook
- `promoted_to_skill` — Extracted as a reusable skill

## Detection Triggers

Automatically log when you encounter:

**Lint Failures** (→ bug pattern with lint trigger):
- ESLint errors or warnings
- Pylint/Ruff/Flake8 violations
- Clippy warnings (Rust)
- `go vet` issues

**Type Errors** (→ bug pattern with type_checker trigger):
- TypeScript `tsc` errors (`TS2322`, `TS2345`, etc.)
- Python `mypy`/`pyright` type mismatches
- Java/Kotlin compiler type errors
- Rust borrow checker violations

**Runtime Exceptions** (→ bug pattern with runtime trigger):
- `SyntaxError`, `TypeError`, `ReferenceError` (JavaScript/Python)
- `NullPointerException`, `ClassCastException` (Java)
- `panic!`, segfault (Rust/C)
- Stack overflow, out of memory

**Test Assertion Failures** (→ bug pattern with test_failure trigger):
- `AssertionError` / `expect(...).toBe(...)` failures
- Snapshot mismatches
- Timeout in async tests
- Flaky test detection (passes sometimes, fails others)

**Code Smells from Static Analysis** (→ learning with anti_pattern or refactor_opportunity):
- Code duplication warnings
- Cyclomatic complexity exceeding threshold
- Dead code / unused imports
- Long parameter lists / god objects

**Performance Hotspots** (→ learning with debugging_insight):
- Profiler output showing slow functions
- N+1 query detection
- Memory leak indicators
- Excessive re-renders (React)

## Priority Guidelines

| Priority | When to Use | Coding Examples |
|----------|-------------|-----------------|
| `critical` | Data corruption, security vulnerability, production crash | SQL injection, buffer overflow, data race writing to shared state |
| `high` | Recurring bug pattern, type safety hole, test reliability | Off-by-one in pagination, null deref in optional chaining, flaky test |
| `medium` | Anti-pattern, code smell, minor type issue | Mutable default argument, deep nesting, missing error boundary |
| `low` | Style issue, minor refactor, naming convention | Inconsistent naming, unused variable, import ordering |

## Area Tags

Use to filter learnings by coding domain:

| Area | Scope |
|------|-------|
| `syntax` | Language syntax errors, parsing issues, grammar |
| `logic` | Logical errors, off-by-one, boundary conditions, control flow |
| `data_structures` | Array/list/map misuse, wrong collection type, mutation bugs |
| `algorithms` | Algorithmic correctness, complexity issues, sorting/search bugs |
| `error_handling` | Missing try/catch, unhandled promises, error propagation |
| `testing` | Test assertions, mocking, fixtures, coverage gaps |
| `tooling` | Linter config, build tools, formatters, IDE setup, CI/CD |

## Promoting to Permanent Coding Standards

When a learning is broadly applicable (not a one-off fix), promote it to permanent project standards.

### When to Promote

- Bug pattern recurs across multiple files or PRs
- Anti-pattern is found in 3+ locations in the codebase
- Idiom gap applies to the entire language/framework usage
- Debugging insight would save significant time if documented

### Promotion Targets

| Target | What Belongs There |
|--------|-------------------|
| Style guide | Code conventions, naming patterns, structural preferences |
| Lint configuration | Automated rule enforcement (`.eslintrc`, `ruff.toml`, `clippy.toml`) |
| Code snippets library | Reusable solutions, utility functions, common patterns |
| Debug playbooks | Step-by-step diagnosis for specific error classes |
| `CLAUDE.md` | Project-specific coding conventions for AI agents |
| `AGENTS.md` | Automated coding workflows, pre-commit checks |

### How to Promote

1. **Distill** the learning into a concise rule or code snippet
2. **Add** to appropriate target (lint rule, style guide entry, snippet)
3. **Update** original entry:
   - Change `**Status**: pending` → `**Status**: promoted`
   - Add `**Promoted**: style guide` (or `lint rule`, `snippet library`, `debug playbook`)

### Promotion Examples

**Learning** (verbose):
> Found mutable default argument `def add_item(items=[])` causing shared state bug.
> List persists across function calls. Three instances found in codebase.

**As lint rule** (concise):
```toml
# ruff.toml
[lint]
select = ["B006"]  # mutable-argument-default
```

**Learning** (verbose):
> Spent 2 hours debugging race condition in async code. Root cause: shared
> mutable state between concurrent coroutines without lock.

**As debug playbook** (actionable):
```markdown
## Race Condition Diagnosis
1. Identify shared mutable state
2. Check for missing locks/mutexes around shared access
3. Add logging with thread/coroutine ID at access points
4. Use `asyncio.Lock()` (Python) or `Mutex` (Rust) to serialize access
5. Write concurrent test to reproduce
```

## Recurring Pattern Detection

If logging something similar to an existing entry:

1. **Search first**: `grep -r "keyword" .learnings/`
2. **Link entries**: Add `**See Also**: BUG-20250110-001` in Metadata
3. **Bump priority** if issue keeps recurring
4. **Consider systemic fix**: Recurring coding issues often indicate:
   - Missing lint rule (→ add to lint config)
   - Missing type annotation (→ stricter type checking)
   - Architectural problem (→ refactor)
   - Documentation gap (→ add to style guide)

## Periodic Review

Review `.learnings/` at natural breakpoints:

### When to Review
- Before starting a new coding task in the same area
- After completing a feature or PR
- When the same error class appears again
- Weekly during active development

### Quick Status Check
```bash
# Count pending coding issues
grep -h "Status\*\*: pending" .learnings/*.md | wc -l

# List pending high-priority bug patterns
grep -B5 "Priority\*\*: high" .learnings/BUG_PATTERNS.md | grep "^## \["

# Find learnings for a specific area
grep -l "Area\*\*: error_handling" .learnings/*.md

# Find all anti-patterns
grep -B2 "anti_pattern" .learnings/LEARNINGS.md | grep "^## \["
```

### Review Actions
- Resolve fixed bug patterns
- Promote recurring patterns to lint rules
- Link related entries across files
- Extract reusable solutions as code snippets

## Simplify & Harden Feed

Ingest recurring coding patterns from `simplify-and-harden` into lint rules or style guides.

1. For each candidate, use `pattern_key` as the dedupe key.
2. Search `.learnings/LEARNINGS.md` for existing entry: `grep -n "Pattern-Key: <key>" .learnings/LEARNINGS.md`
3. If found: increment `Recurrence-Count`, update `Last-Seen`, add `See Also` links.
4. If not found: create new `LRN-...` entry with `Source: simplify-and-harden`.

**Promotion threshold**: `Recurrence-Count >= 3`, seen in 2+ files/modules, within 30-day window.
Targets: lint config, style guide entries, code snippets library, `CLAUDE.md` / `AGENTS.md`.

## Hook Integration

Enable automatic reminders through agent hooks. This is **opt-in**.

### Quick Setup (Claude Code / Codex)

Create `.claude/settings.json` in your project:

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-coding/scripts/activator.sh"
      }]
    }]
  }
}
```

This injects a coding-focused learning evaluation reminder after each prompt (~50-100 tokens overhead).

### Advanced Setup (With Error Detection)

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-coding/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-coding/scripts/error-detector.sh"
      }]
    }]
  }
}
```

### Available Hook Scripts

| Script | Hook Type | Purpose |
|--------|-----------|---------|
| `scripts/activator.sh` | UserPromptSubmit | Reminds to evaluate coding learnings after tasks |
| `scripts/error-detector.sh` | PostToolUse (Bash) | Triggers on lint errors, type errors, runtime exceptions |

See `references/hooks-setup.md` for detailed configuration and troubleshooting.

## Automatic Skill Extraction

When a coding learning is valuable enough to become a reusable skill, extract it.

### Skill Extraction Criteria

| Criterion | Description |
|-----------|-------------|
| **Recurring** | Same bug pattern in 2+ codebases or modules |
| **Verified** | Status is `resolved` with working fix and test |
| **Non-obvious** | Required actual debugging or investigation |
| **Broadly applicable** | Not project-specific; useful across languages/frameworks |
| **User-flagged** | User says "save this as a skill" or similar |

### Extraction Workflow

1. **Identify candidate**: Learning meets extraction criteria
2. **Run helper** (or create manually):
   ```bash
   ./skills/self-improving-coding/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improving-coding/scripts/extract-skill.sh skill-name
   ```
3. **Customize SKILL.md**: Fill in template with coding-specific content
4. **Update learning**: Set status to `promoted_to_skill`, add `Skill-Path`
5. **Verify**: Read skill in fresh session to ensure it's self-contained

### Extraction Detection Triggers

Use conversation signals ("This bug keeps happening", "Save this pattern as a skill") and entry signals (multiple `See Also`, high-priority resolved items, recurring `Pattern-Key`) to identify extraction candidates.

## Multi-Agent Support

| Agent | Activation | Detection |
|-------|-----------|-----------|
| Claude Code | Hooks (UserPromptSubmit, PostToolUse) | Automatic via error-detector.sh |
| Codex CLI | Hooks (same pattern) | Automatic via hook scripts |
| GitHub Copilot | Manual (`.github/copilot-instructions.md`) | Manual review |
| OpenClaw | Workspace injection + inter-agent messaging | Via session tools |

## Best Practices

1. **Log immediately** — context fades fast after debugging sessions
2. **Include minimal code snippets** — before/after examples are most useful
3. **Specify the language** — patterns differ between Python, TypeScript, Rust, etc.
4. **Suggest concrete prevention** — a lint rule is better than "be careful"
5. **Distinguish root cause from symptom** — the error message is the symptom, not the cause
6. **Test your fix** — mark resolved only after verification

## Gitignore Options

**Keep learnings local** (per-developer):
```gitignore
.learnings/
```

**Track learnings in repo** (team-wide):
Don't add to .gitignore — learnings become shared knowledge.

**Hybrid** (track templates, ignore entries):
```gitignore
.learnings/*.md
!.learnings/.gitkeep
```

## Stackability Contract (Standalone + Multi-Skill)

This skill is standalone-compatible and stackable with other self-improving skills.

### Namespaced Logging (recommended for 2+ skills)
- Namespace for this skill: `.learnings/coding/`
- Keep current standalone behavior if you prefer flat files.
- Optional shared index for all skills: `.learnings/INDEX.md`

### Required Metadata
Every new entry must include:

```markdown
**Skill**: coding
```

### Hook Arbitration (when 2+ skills are enabled)
- Use one dispatcher hook as the single entrypoint.
- Dispatcher responsibilities: route by matcher, dedupe repeated events, and rate-limit reminders.
- Suggested defaults: dedupe key = `event + matcher + file + 5m_window`; max 1 reminder per skill every 5 minutes.

### Narrow Matcher Scope (coding)
Only trigger this skill automatically for coding signals such as:
- `eslint|ruff|flake8|mypy|pyright|tsc`
- `exception|traceback|assertionerror|test failed`
- explicit coding intent in user prompt

### Cross-Skill Precedence
When guidance conflicts, apply:
1. `security`
2. `engineering`
3. `coding`
4. `ai`
5. user-explicit domain skill
6. `meta` as tie-breaker

### Ownership Rules
- This skill writes only to `.learnings/coding/` in stackable mode.
- It may read other skill folders for cross-linking, but should not rewrite their entries.
