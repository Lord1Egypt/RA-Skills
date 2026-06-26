# Vibe Prompt Compiler Portable

A cross-platform prompt-compiler skill for AI coding tools.

It turns rough natural-language coding requests into structured implementation briefs that work well in tools like Cursor, VS Code AI chat, Claude Code, Codex CLI, and Gemini CLI.

## Why This Exists

Most coding requests start too vague.

Examples:

- "build a dashboard"
- "fix this bug"
- "add CRUD"
- "make this page better"
- "design the architecture"
- "set up an automation flow"

AI coding tools perform much better when the request is first converted into a high-signal brief with:

- a clear goal
- a narrow current task
- explicit assumptions
- scope and non-goals
- constraints
- acceptance criteria
- a delivery shape the coding tool can follow

This skill does that compilation step for you.

## What It Does

- classifies rough requests into practical engineering task types
- compiles them into high-signal implementation prompts
- generates stronger handoff text for larger or riskier tasks
- includes non-goals, expected deliverables, and execution rules for better multi-agent handoff quality
- keeps scope, constraints, and acceptance criteria explicit
- supports architecture, integration, and automation requests in addition to normal coding tasks
- gives examples for Cursor, Claude Code, Codex CLI, and Gemini CLI
- supports `Chinese-first` prompt and handoff output
- supports development rulesets such as `minimal-diff`, `test-first`, and `repo-safe`
- can merge repository-aware rules from JSON or auto-extract them from common repo files
- includes routing, golden, preset, lint, and repository-rule tests so future changes do not silently drift

## Best Fit

Use this skill when the user gives a coding or product-engineering request that is real but underspecified.

Especially useful for:

- MVP and prototype requests
- vague full-stack feature asks
- bugfixes that need tighter scoping
- architecture and system design requests
- integration work with third-party services
- automation and background workflow design
- cross-tool handoffs between planning and implementation tools

## Task Types

The current compiler supports:

- `new-project`
- `page-ui`
- `crud-feature`
- `api-backend`
- `bugfix`
- `refactor`
- `ai-feature`
- `architecture-review`
- `integration`
- `automation-workflow`
- `deployment`
- `general`

## Included Files

- `SKILL.md` — skill metadata and usage guidance
- `references/auto-mode.md` — default automatic behavior
- `references/templates.md` — canonical prompt templates
- `references/routing.md` — task routing rules
- `references/usage.md` — suggested workflows by tool type
- `references/tool-examples.md` — tool-specific usage examples
- `references/real-examples.md` — realistic request-to-brief examples
- `scripts/compile_prompt.py` — compile a raw request into a structured prompt
- `scripts/create_handoff.py` — create a stronger execution handoff
- `scripts/prompt_lint.py` — lint a compiled brief for vagueness, weak verification, and assumption overload
- `scripts/test_routing.py` — verify routing behavior across representative requests
- `scripts/test_handoff.py` — verify handoff structure and required sections
- `scripts/test_web_cases.py` — verify routing behavior against realistic public-style request samples
- `scripts/test_golden_outputs.py` — verify key prompt and handoff skeletons do not drift unexpectedly
- `scripts/test_tool_presets.py` — verify target-tool preset wrappers for Cursor, Codex CLI, Claude Code, and Gemini CLI
- `scripts/test_prompt_lint.py` — verify lint behavior for vague, well-scoped, and assumption-heavy requests
- `scripts/test_language_presets.py` — verify Chinese-first output for prompt and handoff generation
- `scripts/test_rulesets.py` — verify development rule presets in prompt JSON and handoff output
- `scripts/test_extract_repo_rules.py` — verify repository-rule extraction from common repo files
- `tests/web_cases.json` — realistic routing fixtures, including mixed Chinese-English phrasing
- `tests/golden_prompts.json` — lightweight golden fixtures for representative prompt and handoff shapes
- `tests/tool_presets.json` — target-tool wrapper fixtures for tool-specific handoff checks
- `tests/prompt_lint_cases.json` — prompt-lint fixtures for scope, verification, and assumption checks
- `tests/language_presets.json` — language preset fixtures for Chinese-first prompt and handoff output
- `tests/rulesets.json` — development-rule fixtures for `minimal-diff`, `test-first`, and `repo-safe`
- `tests/repo_extract_cases.json` — repository-rule extraction fixtures
- `tests/test_repo/rules/package.json` — sample repo metadata for extraction tests
- `CHANGELOG.md` — notable changes to the skill
- `ROADMAP.md` — next likely improvements and productization directions
- `LICENSE.md` — MIT license for publishing and reuse
- `install-windows.md` — Windows PowerShell install instructions and script snippet

## Core Design Principles

- prefer minimal, verifiable slices over broad implementation sprawl
- convert missing details into explicit assumptions rather than hidden guesses
- avoid unrelated edits
- prefer evolutionary change over rewrites for existing systems
- separate current-task execution from future-state ideas
- use stronger handoff text when ambiguity or drift risk is high

## Requirements

- `python3` or `python`
- `bash` or `sh` on macOS/Linux
- `PowerShell` on Windows

## Quick Start

### 1. Copy the skill folder

Copy `vibe-prompt-compiler-portable/` into any workspace, tools folder, or skills folder used by your system.

Or run the installer.

macOS / Linux:

```bash
bash install.sh
```

Optional custom install directory:

```bash
bash install.sh "$HOME/tools/vibe-prompt-compiler-portable"
```

Windows PowerShell:

Use the script snippet in `install-windows.md`, or run the equivalent commands manually.

Suggested command flow:

```powershell
$TargetDir = "$HOME\AppData\Local\vibe-prompt-compiler-portable"
New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
Copy-Item -Path .\* -Destination $TargetDir -Recurse -Force
```

Optional custom install directory:

```powershell
$TargetDir = "$HOME\tools\vibe-prompt-compiler-portable"
New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
Copy-Item -Path .\* -Destination $TargetDir -Recurse -Force
```

### 2. Test prompt compilation

```bash
python3 scripts/compile_prompt.py --request "Build an admin dashboard MVP" --stack "Next.js, Supabase, Tailwind"
```

### 3. Test handoff generation

```bash
python3 scripts/create_handoff.py --request "Fix the login API 500 error" --mode bugfix --output handoff
```

### 4. Run routing tests

```bash
python3 scripts/test_routing.py
```

### 5. Run handoff structure tests

```bash
python3 scripts/test_handoff.py
```

### 6. Run realistic request regression tests

```bash
python3 scripts/test_web_cases.py
```

### 7. Run golden output regression tests

```bash
python3 scripts/test_golden_outputs.py
```

### 8. Run tool-preset regression tests

```bash
python3 scripts/test_tool_presets.py
```

### 9. Run prompt-lint regression tests

```bash
python3 scripts/test_prompt_lint.py
```

### 10. Run language-preset regression tests

```bash
python3 scripts/test_language_presets.py
```

### 11. Run ruleset regression tests

```bash
python3 scripts/test_rulesets.py
```

### 12. Run repository-rule extraction tests

```bash
python3 scripts/test_extract_repo_rules.py
```

## Common Commands

### Compile a request into a portable prompt

```bash
python3 scripts/compile_prompt.py \
  --request "Build an event registration admin panel MVP" \
  --stack "Next.js, Supabase, Tailwind"
```

### Return JSON instead of plain text

```bash
python3 scripts/compile_prompt.py \
  --request "Refactor the profile settings page" \
  --output json
```

### Compile with a development ruleset

```bash
python3 scripts/compile_prompt.py \
  --request "Fix the login API 500 error" \
  --ruleset minimal-diff \
  --output json
```

### Extract repository-aware rules

```bash
python3 scripts/extract_repo_rules.py \
  --repo-root .
```

### Compile with repository-aware rules

```bash
python3 scripts/compile_prompt.py \
  --request "Fix the login API 500 error" \
  --ruleset repo-safe \
  --repo-rules-file tests/repo_rules_sample.json \
  --output json
```

### Compile with automatic repository-rule extraction

```bash
python3 scripts/compile_prompt.py \
  --request "Fix the login API 500 error" \
  --ruleset repo-safe \
  --repo-root . \
  --auto-repo-rules \
  --output json
```

### Generate Chinese-first output

```bash
python3 scripts/compile_prompt.py \
  --request "修复登录接口 500" \
  --language-preset chinese-first \
  --output json
```

`Chinese-first` now uses dedicated Chinese templates for common task types, instead of only title-level localization.

## Chinese-first Support

Current `Chinese-first` support covers both `compile_prompt.py` and `create_handoff.py`.

Built-in development rulesets:

- `minimal-diff` — minimize patch surface and unrelated edits
- `test-first` — force verification-first thinking and explicit checks
- `repo-safe` — emphasize repository conventions, local boundaries, and dependency restraint

Repository-aware rules:

- `--repo-rules-file <path>` lets you merge repository-specific rules from a JSON file
- `scripts/extract_repo_rules.py --repo-root <path>` generates a first-pass rules JSON from common repo files
- `--repo-root <path> --auto-repo-rules` lets `compile_prompt.py` and `create_handoff.py` inject extracted repo rules directly
- current extractor reads `AGENTS.md`, `README.md`, and `package.json`

What is already fully Chinese-first:

- prompt section headers
- prompt body wording for supported task types
- handoff wrapper text
- non-goals
- expected deliverables
- execution rules
- tool-specific wrapper instructions

The current Chinese-first templates cover:

- `new-project`
- `page-ui`
- `crud-feature`
- `api-backend`
- `bugfix`
- `refactor`
- `ai-feature`
- `architecture-review`
- `integration`
- `automation-workflow`
- `deployment`
- `general`

Recommended checks before shipping template changes:

```bash
python3 scripts/test_language_presets.py
python3 scripts/test_golden_outputs.py
python3 scripts/test_rulesets.py
```

### Create a bugfix handoff

```bash
python3 scripts/create_handoff.py \
  --request "Fix the submit button not saving to database" \
  --mode bugfix \
  --output handoff
```

### Create a plan-first handoff for a broad MVP request

```bash
python3 scripts/create_handoff.py \
  --request "Build a lightweight CRM MVP" \
  --mode plan-only \
  --output handoff
```

### Create a Chinese-first Codex CLI handoff

```bash
python3 scripts/create_handoff.py \
  --request "Build a lightweight CRM MVP" \
  --target-tool codex-cli \
  --language-preset chinese-first \
  --output handoff
```

### Create a handoff with development rules

```bash
python3 scripts/create_handoff.py \
  --request "修复登录接口 500" \
  --ruleset test-first \
  --language-preset chinese-first \
  --output handoff
```

### Create a handoff with repository-aware rules

```bash
python3 scripts/create_handoff.py \
  --request "Build an admin dashboard MVP" \
  --ruleset repo-safe \
  --repo-rules-file tests/repo_rules_sample.json \
  --output handoff
```

### Create a handoff with automatic repository-rule extraction

```bash
python3 scripts/create_handoff.py \
  --request "Build an admin dashboard MVP" \
  --ruleset repo-safe \
  --repo-root . \
  --auto-repo-rules \
  --output handoff
```

### Create an architecture handoff

```bash
python3 scripts/create_handoff.py \
  --request "We have one testing system and want to support two products with isolated data but identical features" \
  --task architecture-review \
  --output handoff
```

### Create an automation workflow handoff

```bash
python3 scripts/create_handoff.py \
  --request "Set up a workflow that scans files, parses them, stores records, and alerts on failure" \
  --task automation-workflow \
  --output handoff
```

### Lint a compiled prompt before handoff

```bash
python3 scripts/prompt_lint.py \
  --request "Help me improve this thing" \
  --output text
```

## Recommended Use by Tool

- `Cursor / VS Code AI chat`
  - use `compile_prompt.py` for short tasks
  - use `create_handoff.py` for broad or ambiguous tasks
- `Claude Code`
  - prefer `create_handoff.py` when drift risk is high
  - especially good for bugfixes, refactors, and architecture-aware implementation
- `Codex CLI`
  - use `create_handoff.py` for higher-signal execution briefs
  - use `compile_prompt.py` for focused one-slice tasks
- `Gemini CLI`
  - good fit for architecture comparison, planning, and broad requirement shaping
- `Generic IDE side-panel assistants`
  - paste output from either script into chat and ask for only the current slice

## When to Use Which Script

### Use `compile_prompt.py` when:

- the request is short and already somewhat clear
- you want a concise portable prompt
- the task is a single slice and not very risky

### Use `create_handoff.py` when:

- the request is broad, risky, or likely to drift
- you want stronger execution rules
- the task is architectural, integration-heavy, or workflow-driven
- you want to hand work from one AI tool to another cleanly
- you want the brief to carry non-goals and expected deliverables explicitly

## Real Example Requests

Representative examples live in:

- `references/real-examples.md`

That file covers:

- multi-product isolation architecture
- vague bugfixes
- CRUD requests from one-liners
- WeCom-style integration requests
- automation workflows with retries and alerts
- AI feature expansion
- Windows deployment
- UI vs CRUD routing edge cases

## Testing and Regression Safety

Routing logic is easy to accidentally break when new keywords or task types are added.

Use this before shipping changes:

```bash
python3 scripts/test_routing.py
python3 scripts/test_web_cases.py
python3 scripts/test_golden_outputs.py
python3 scripts/test_tool_presets.py
python3 scripts/test_prompt_lint.py
python3 scripts/test_language_presets.py
```

The current test suite checks:

- MVP / project requests
- bugfix detection
- refactor detection
- UI and CRUD separation
- API task routing
- architecture requests
- integration requests
- automation workflow requests
- AI feature requests
- deployment requests
- realistic public-style requests
- mixed Chinese-English phrasing
- reusable fixture-based regression coverage

## Portability Notes

This package intentionally avoids platform-specific dispatch logic.

It does **not** depend on:

- OpenClaw `sessions_spawn`
- ACP runtimes
- OpenClaw-specific message routing

That makes it easier to reuse in other systems.

## Suggested Distribution Options

- share the folder directly
- share the packaged file: `dist/vibe-prompt-compiler-portable.skill`
- copy only `scripts/` and `references/` if the target system does not support skills

## Good Evolution Paths

If you want to keep improving this skill, the next most valuable areas are:

- richer handoff metadata for downstream agents
- more real-world routing examples
- regression tests for edge-case ambiguity
- output modes tailored for specific agent runtimes
- packaging and publication improvements
