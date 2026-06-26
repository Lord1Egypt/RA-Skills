# Gemini Source Adapter

Use this reference when the source is a Gemini CLI skill, Gemini extension, project context bundle, command bundle, subagent bundle, MCP config, hook config, or policy bundle.

## Artifact Mapping

| Gemini artifact | Target handling |
| --- | --- |
| `SKILL.md` | Usually portable after frontmatter, wording, and path cleanup. |
| `.gemini/skills/<name>/SKILL.md` or `.agents/skills/<name>/SKILL.md` | Treat as Agent Skills-compatible source. |
| `GEMINI.md` | Treat as project instructions. Translate or bridge to target guidance such as `AGENTS.md` or `CLAUDE.md`; do not package as a skill. |
| `gemini-extension.json` | Gemini extension manifest. Convert to target plugin manifest only when target package fields are known; otherwise document as partial. |
| `commands/*.toml` | Gemini custom slash commands. Convert intent into target trigger/workflow text or target command format if supported. |
| `agents/*.md` | Gemini subagents. Convert known fields to target subagent/custom-agent format; otherwise mark partial. |
| `hooks/hooks.json` | Gemini lifecycle hooks. Treat as risky lifecycle behavior requiring event/schema mapping. |
| `policies/*.toml` | Gemini policy rules/safety checkers. Treat as target-specific safety configuration, not as a skill. |
| `.gemini/settings.json`, `~/.gemini/settings.json`, `mcpServers` | MCP/tool setup. Treat credentials, trust, include/exclude tools, and scopes as dependency-bound. |

## Gemini-Specific Signals

Flag these because they require target adaptation:

- `GEMINI.md` context hierarchy.
- `gemini-extension.json` manifest metadata.
- `commands/*.toml` command definitions.
- Gemini hook events such as `BeforeAgent`, `AfterAgent`, `BeforeModel`, `AfterModel`, `BeforeToolSelection`, and `BeforeTool`.
- Policy engine files under `policies/`.
- `run_shell_command` restrictions.
- MCP config and trust semantics in `settings.json`.

## Rewrite Rules

- Convert `GEMINI.md` into the target's project-instruction file.
- Convert Gemini command TOML into target workflows or command notes.
- Convert extension `skills/` directly where they follow the Agent Skills shape.
- Convert extension `mcpServers` into dependency notes unless a safe target MCP config is explicitly requested.
- Preserve extension context files as references unless they are project-wide instructions.
- Keep policies and hooks inactive; document their safety intent and required target equivalent.

## Classification Defaults

- Plain skills are usually portable.
- Extensions are partial packages.
- Commands need adaptation.
- Subagents are partial.
- MCP config is dependency-bound.
- Hooks and policies are unsupported by default unless explicitly mapped.
