# Portable Usage

This version is designed for tools that do not know anything about OpenClaw-specific dispatch or session spawning.

## Best Fit Targets

- Cursor
- VS Code with AI chat/extensions
- Claude Code
- Codex CLI
- Gemini CLI
- Generic IDE side-panel assistants

## Recommended Workflow

### Mode 1: Prompt-first

1. Run `scripts/compile_prompt.py`.
2. Paste the output into the coding tool.
3. Let the tool plan or implement one slice.

Use this when:
- the request is already fairly clear
- you want the shortest path to code generation

### Mode 2: Handoff-first

1. Run `scripts/create_handoff.py`.
2. Paste the handoff into the coding tool.
3. Ask the tool to use it as the source of truth.

Use this when:
- the task is broad
- you want stronger guardrails
- the coding tool tends to drift

## Example Commands

```bash
python3 scripts/compile_prompt.py --request "做一个活动报名后台 MVP" --stack "Next.js, Supabase, Tailwind"
python3 scripts/create_handoff.py --request "修复登录接口 500" --mode bugfix --output handoff
```

## Recommended IDE Patterns

### Cursor / VS Code

- Use `compile_prompt.py` for shorter requests.
- Use `create_handoff.py` for larger work.
- Ask the IDE agent to modify only the current slice.

### Claude Code / Codex CLI

- Use the handoff output.
- Ask for a short plan first on broad tasks.
- Ask for a minimal patch first on bugfixes.

## Portability Rule

Do not rely on any tool-specific dispatch primitives here. Treat this skill as a prompt compiler and handoff generator only.
