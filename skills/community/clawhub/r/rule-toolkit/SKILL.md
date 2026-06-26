---
name: rule-toolkit
version: 1.0.0
description: Scan constraint files (CLAUDE.md, agents.md, soul.md, tools.md, bootstrap.md, .cursorrules) across AI coding platforms, identify rules enforceable by tools, and auto-generate linters, hooks, validators, and wrapper functions. Use when setting up a new project, onboarding an existing codebase, or when the user says "convert rules to tools", "make rules enforceable", "automate my CLAUDE.md rules", or "toolify constraints".
license: MIT
compatibility: "Requires Node.js 18+ for ESLint/Prettier/Husky generation. Python projects use ruff. Works with Claude Code, OpenClaw, Cursor, Copilot, and any Agent Skills compatible tool."
allowed-tools: "Bash Glob Grep Read Write Edit"
---

# Rule Toolkit

Convert hand-written constraint files into automated tooling. Rules in prompt files are forgotten when context grows long. Rules compiled into linters, hooks, and validators are enforced 100% of the time, at zero token cost.

## Platform Detection

Detect which platform(s) are present, then scan the corresponding constraint files.

```bash
test -f CLAUDE.md && echo "CLAUDE_CODE"
test -f openclaw.json && echo "OPENCLAW"
test -f .cursorrules && echo "CURSOR"
test -f .github/copilot-instructions.md && echo "COPILOT"
```

**Claude Code**: `CLAUDE.md` (monolithic), `.claude/commands/*.md`
**OpenClaw**: `agents.md` (priority 10), `soul.md` (20), `identity.md` (30), `user.md` (40), `tools.md` (50), `bootstrap.md` (60), `memory.md` (70). Skip `SAFETY.md` (hardcoded, read-only).
**Cursor**: `.cursorrules`
**Copilot**: `.github/copilot-instructions.md`
**Generic**: `AGENT.md`, `SOUL.md`, `README.md` conventions sections

Read ALL found files. Extract every rule, convention, and constraint.

## Rule Classification

Classify each extracted rule into one of two buckets.

### Auto-Toolable

| Category | Example Rule | Target Tool |
|----------|-------------|-------------|
| code-style | "2 spaces, no semicolons, single quotes" | .prettierrc |
| naming | "Files kebab-case, components PascalCase" | ESLint custom rule |
| import | "No default exports" / "Use @/ alias" | ESLint no-restricted-paths |
| api-format | "Responses use { code, data, msg }" | Wrapper function + lint |
| type-safety | "No any, no as" | tsconfig strict |
| security | "No innerHTML" / "Validate user input" | ESLint + zod |
| testing | "Every module needs a test file" | Test existence checker |
| git | "Conventional commits" / "Lint before commit" | commitlint + husky |
| dependency | "No new deps without approval" | dependency-check script |
| performance | "No lodash, use lodash-es" | ESLint no-restricted-imports |

### Prompt-Only (cannot automate)

| Category | Example Rule | Why |
|----------|-------------|-----|
| architecture | "Use repository pattern" | Semantic understanding needed |
| business-logic | "Prices in cents, not dollars" | Domain-specific |
| design | "Composition over inheritance" | Judgment call |
| communication | "Explain in Chinese" | Behavioral |
| workflow | "Ask before deleting" | Human-in-the-loop |

## Tech Stack Detection

Before generating tools, detect the project stack:

```
package.json → Node.js    | tsconfig.json → TypeScript
.eslintrc* → ESLint exists | .prettierrc* → Prettier exists
.husky/ → Husky exists     | pyproject.toml → Python
Cargo.toml → Rust          | go.mod → Go
```

## Code Generation

For each auto-toolable rule, generate the appropriate tool. See [references/tool-patterns.md](references/tool-patterns.md) for detailed generation patterns covering:

- ESLint rules (no-restricted-syntax, custom naming rules, import restrictions)
- Prettier config (.prettierrc)
- TypeScript strict config (tsconfig.json)
- Git hooks (husky + lint-staged + commitlint)
- Wrapper functions (API response format)
- Validation scripts (custom checkers)
- Python tooling (ruff, mypy)
- Rust tooling (clippy)

For OpenClaw-specific hooks, see [references/openclaw-hooks.md](references/openclaw-hooks.md).

## Reporting

After generation, produce a report:

```markdown
## Rule Toolkit Report

### Platform: Claude Code / OpenClaw / Cursor / Copilot

### Scanned Files
- CLAUDE.md (45 rules)
- soul.md (8 rules)

### Converted to Tools (38 rules)

| Rule | Source | Tool | Status |
|------|--------|------|--------|
| "Use 2-space indent" | CLAUDE.md | .prettierrc | Created |
| "No semicolons" | soul.md | .prettierrc | Created |
| "Conventional commits" | bootstrap.md | commitlint | Created |

### Remaining in Prompt (15 rules)

| Rule | Source | Reason |
|------|--------|--------|
| "Use repository pattern" | CLAUDE.md | Architectural judgment |
| "Ask before deleting" | tools.md | Human-in-the-loop |

### Summary
- N% rules automatically enforced
- M% remain in prompt
- Token savings: ~X tokens/conversation
```

## Cleanup Constraint Files

Remove toolified rules from source files to save tokens.

**Claude Code** — replace removed rules in `CLAUDE.md`:

```markdown
## Rules
Automated rules enforced by tooling. Run `npm run lint` to check.
See `.eslintrc.cjs`, `.prettierrc`, `scripts/check-rules.js`.
```

**OpenClaw** — replace removed rules in each file (e.g. `tools.md`):

```markdown
## Tool Rules
Automated: linting (`npx eslint .`), type check (`npx tsc --noEmit`).
API format: use `ok()`/`fail()` from `src/utils/response.ts`.
Remaining rules below require human judgment.
```

## Safety Rules

- NEVER modify existing tool configs without showing a diff first
- ALWAYS preserve existing rules, only add new ones
- ALWAYS create wrapper functions in a new file
- ALWAYS run generated configs to verify they parse correctly
- If a rule is ambiguous, ASK the user before generating
- OpenClaw `SAFETY.md` is hardcoded — skip it
- Show the user what will change before writing files
