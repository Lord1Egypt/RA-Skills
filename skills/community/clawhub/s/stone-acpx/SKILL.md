---
name: acpx
description: Use the acpx CLI to run coding agents over the Agent Client Protocol (ACP) instead of PTY scraping. Use when routing work to Codex, Claude Code, Gemini CLI, Pi, OpenCode, or other ACP-compatible coding clients; when inspecting acpx commands, flags, sessions, or workflows; or when maintaining a fixed acpx runtime version for OpenClaw ACP agents.
---

# acpx

Use `acpx` as the CLI transport for ACP coding clients.

## Local policy for this machine

- OpenClaw ACP runtime uses a fixed plugin-local `acpx` version, not `npx acpx@latest`.
- Current pinned target: `0.3.0`.
- Prefer these configured ACP harness agents for coding work:
  - `openai_codex_agent` -> Codex
  - `claude_code_agent` -> Claude Code
  - `google_gemini_agent` -> Gemini CLI
- Gemini CLI must use its own default model on this machine; do not force deprecated model ids in ACP overrides.
- Use `npx acpx@latest` only for explicit manual experiments or upgrade checks, not as the default OpenClaw runtime backend.

## Binary selection

For OpenClaw/runtime-integrated ACP work, prefer the plugin-local binary:

```bash
/opt/homebrew/lib/node_modules/openclaw/extensions/acpx/node_modules/.bin/acpx
```

Check the pinned version from the extension package:

```bash
node -e "console.log(require('/opt/homebrew/lib/node_modules/openclaw/extensions/acpx/package.json').dependencies.acpx)"
```

## Common commands

```bash
acpx codex "fix the tests"
acpx claude "refactor auth"
acpx gemini exec "summarize this repo"
acpx codex sessions new --name backend
acpx codex sessions close backend
```

## References

For the full upstream reference, read:

- https://raw.githubusercontent.com/openclaw/acpx/main/skills/acpx/SKILL.md
- https://raw.githubusercontent.com/openclaw/acpx/main/docs/CLI.md
