# Gemini Target Adapter

Use this reference when the target agent is Gemini CLI.

## Skill Shape

Gemini CLI skills should be staged as:

```text
<skill-name>/
  SKILL.md
  references/        # optional docs loaded on demand
  scripts/           # optional helpers, only after security review
  assets/            # optional templates or static assets
```

Gemini discovers skills from `.gemini/skills/`, `~/.gemini/skills/`, and the `.agents/skills/` alias. Keep `SKILL.md` frontmatter valid with `name` and `description`.

## Project Instructions

Gemini CLI uses `GEMINI.md` for persistent project context. Project guidance belongs in `GEMINI.md`, not in a skill unless it is a reusable workflow.

When the source has `AGENTS.md` or `CLAUDE.md`, translate reusable project instructions into `GEMINI.md` and preserve source-specific behavior as notes.

## Staging Paths

- Single skill: `skills/gemini/<skill-name>/`
- Multi-skill/plugin source: `ports/<source-name>/gemini/`
- Do not write directly to `~/.gemini/skills/`, `.gemini/skills/`, or `.agents/skills/` unless the user explicitly asks for installation.

## Target-Specific Package Surfaces

| Target artifact | Use |
| --- | --- |
| `skills/<name>/SKILL.md` | Extension skill or staged skill. |
| `gemini-extension.json` | Gemini extension manifest. |
| `GEMINI.md` | Extension or project context file. |
| `commands/*.toml` | Gemini custom command files. |
| `agents/*.md` | Gemini subagent definitions. |
| `hooks/hooks.json` | Gemini hook config; keep inactive until reviewed. |
| `policies/*.toml` | Gemini policy rules/safety checkers; target-specific safety layer. |

## Porting Rules

- Convert Agent Skills-compatible `SKILL.md` files directly after frontmatter and wording cleanup.
- Convert Codex `AGENTS.md` or Claude `CLAUDE.md` into `GEMINI.md`.
- Convert Claude slash commands and Codex command-like workflows into Gemini command notes or `commands/*.toml` only when the command schema is known.
- Convert Claude/Codex agents into Gemini subagent Markdown only for known fields.
- Keep MCP/provider setup as dependency notes unless the user explicitly asks to stage settings.
- Keep hooks and policies inactive unless the event/schema mapping is explicit.

## Validation

When Gemini CLI is available, validate discovery with:

```bash
gemini skills list
```

For local development, prefer linking or staging over global installation until the user approves:

```bash
gemini skills link <skill-path>
```
