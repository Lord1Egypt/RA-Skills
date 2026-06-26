# Claude Target Adapter

Use this reference when the target agent is Claude Code.

## Skill Shape

Claude Code skills should be staged as:

```text
<skill-name>/
  SKILL.md
  references/        # optional docs loaded on demand
  scripts/           # optional helpers, only after security review
  assets/            # optional templates or static assets
```

`SKILL.md` should include frontmatter with at least a clear `description`. Keep `name` when it is already Agent Skills-compatible, because it improves index portability.

## Project Instructions

Claude Code reads `CLAUDE.md`, not `AGENTS.md` or `GEMINI.md`. Project guidance belongs in `CLAUDE.md` or `.claude/CLAUDE.md`, not in a skill unless it is a reusable workflow.

When the source has `AGENTS.md`, prefer a bridge:

```md
@AGENTS.md

## Claude Code

Claude-specific notes go here.
```

When the source has `GEMINI.md`, translate the reusable instructions into `CLAUDE.md` and preserve Gemini-specific behavior as notes.

## Staging Paths

- Single skill: `skills/claude/<skill-name>/`
- Multi-skill/plugin source: `ports/<source-name>/claude/`
- Do not write directly to `~/.claude/skills/` or `.claude/skills/` unless the user explicitly asks for installation.

## Target-Specific Package Surfaces

| Target artifact | Use |
| --- | --- |
| `skills/<name>/SKILL.md` | Plugin skill or staged skill. |
| `.claude-plugin/plugin.json` | Claude plugin manifest. |
| `.claude-plugin/marketplace.json` | Claude plugin marketplace catalog. |
| `agents/*.md` | Plugin subagents or staged custom subagents. |
| `.mcp.json` | Project/plugin MCP dependency config. |
| `hooks/hooks.json` | Plugin hook config; keep inactive until reviewed. |

## Porting Rules

- Convert slash-command intent into Claude skill descriptions and procedural instructions.
- Convert Codex `AGENTS.md` and Gemini `GEMINI.md` into `CLAUDE.md` guidance or a bridge note.
- Convert Codex custom-agent TOML into Claude subagent Markdown only for known fields.
- Convert Gemini extension agents into Claude agent Markdown only for known fields.
- Keep MCP/provider setup as dependency notes unless the user explicitly asks to stage `.mcp.json`.
- Do not emit Claude dynamic context injection (`!` shell syntax) unless the source already used it and the command has been security reviewed.
- Do not enable hooks automatically.

## Validation

When Claude Code is available, validate staged plugins with:

```bash
claude plugin validate <plugin-or-marketplace-path>
```

Ask before installing or adding a marketplace.
