---
name: vibe-prompt-compiler-portable
description: Compile rough natural-language coding requests into structured, high-signal prompts for cross-platform AI coding tools such as Cursor, Claude Code, Codex CLI, Gemini CLI, and generic IDE chat assistants. Use when a user describes a vague implementation request like "build a dashboard", "fix this bug", "add CRUD", or "refactor this page" and you should first transform it into a scoped implementation brief before generating code.
---

# Vibe Prompt Compiler Portable

Turn rough implementation requests into portable coding briefs that can be pasted into almost any AI coding tool.

## Default Behavior

Use this skill automatically when a user gives a vague coding request. Do not require the user to run scripts first.

Instead:

1. Classify the request.
2. Extract the facts already present.
3. Turn missing details into explicit assumptions.
4. Compile a clean internal implementation brief.
5. Use that brief as the source of truth for the coding response.

Only mention scripts when the user wants portability, reusable CLI commands, or a saved handoff for another tool.

## Task Types

Classify into one of these:

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

Use the narrowest obvious type. Only ask a follow-up question when one missing detail blocks useful progress.

## Portable Defaults

Unless the user says otherwise:

- prefer MVP over over-engineering
- prefer minimal diffs over broad rewrites
- do not modify unrelated files
- avoid adding dependencies unless justified
- make assumptions explicit
- keep outputs easy to test and verify
- state non-goals when they reduce drift
- prefer evolutionary changes over rewrites for existing systems
- separate current-task execution from future-state ideas

## Main Commands

Default: compile mentally and use the structure directly in the answer or coding workflow.

Compile a prompt via CLI when needed:

`python3 scripts/compile_prompt.py --request "<user request>"`

Create a handoff brief:

`python3 scripts/create_handoff.py --request "<user request>" --output handoff`

Extract repository-aware rules:

`python3 scripts/extract_repo_rules.py --repo-root .`

Useful flags:

- `--task auto`
- `--stack "Next.js, Supabase, Tailwind"`
- `--audience "运营人员"`
- `--mode plan-only`
- `--mode build-first-slice`
- `--mode bugfix`
- `--target-tool codex-cli`
- `--language-preset chinese-first`
- `--ruleset minimal-diff`
- `--repo-root .`
- `--auto-repo-rules`
- `--output json`

## Target Tool Usage

When the request is broad, architectural, or likely to drift, prefer creating a handoff-style brief over answering from the raw request.

### Cursor / VS Code chat

- run `compile_prompt.py` or `create_handoff.py`
- paste the output into the chat
- let the tool implement only the current slice

### Claude Code / Codex CLI / Gemini CLI

- use the compiled prompt or handoff as the source of truth
- ask the coding tool to plan first for broad tasks
- ask for minimal fixes for bug work
- prefer `--target-tool`, `--ruleset`, and repo-aware flags for stronger execution constraints

## Publish Notes

This skill is now suitable for sharing as a portable coding-brief compiler with:

- structured prompt compilation
- stronger execution handoffs
- Chinese-first output
- tool-specific presets
- development rulesets
- repository-aware rule extraction and merging
- regression coverage across routing, golden outputs, presets, linting, and repo-aware flows

## References

- Read `references/auto-mode.md` first for the default automatic behavior.
- Read `references/templates.md` for prompt skeletons.
- Read `references/routing.md` when classification is unclear.
- Read `references/usage.md` for suggested workflows in common IDEs and coding tools.
- Read `references/tool-examples.md` for concrete examples in Cursor, Claude Code, Codex CLI, and Gemini CLI.
- Read `references/real-examples.md` for realistic request-to-brief transformations, especially for architecture, integration, workflow, and vague coding requests.
