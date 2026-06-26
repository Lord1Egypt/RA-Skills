# Codex Target Adapter

Use this reference when the target agent is Codex.

## Skill Shape

Codex skills should be staged as:

```text
<skill-name>/
  SKILL.md
  agents/openai.yaml        # optional UI metadata
  references/               # optional docs loaded on demand
  scripts/                  # optional deterministic helpers
  assets/                   # optional templates or static assets
```

`SKILL.md` frontmatter must include:

```yaml
---
name: lowercase-hyphen-name
description: Clear trigger-oriented description
---
```

Keep `SKILL.md` concise. Move long examples, source mappings, provider docs, and domain tables into `references/`.

## Project Instructions

Project guidance belongs in `AGENTS.md` or target project-instruction files, not in a skill unless it is a reusable workflow. When a Claude source has `CLAUDE.md`, recommend a target `AGENTS.md` bridge or translated project guidance with notes for Claude-only behavior. When a Gemini source has `GEMINI.md`, translate reusable guidance into `AGENTS.md` and preserve Gemini-specific extension, hook, or policy behavior as notes.

## Staging Paths

- Single skill: `skills/codex/<skill-name>/`
- Multi-skill/plugin source: `ports/<source-name>/codex/`
- Do not write directly to `~/.codex/skills/` unless the user explicitly asks for installation.

## Claude-to-Codex Rules

- Convert `CLAUDE.md` project guidance into `AGENTS.md` guidance or a bridge note; do not treat it as a skill.
- Convert Claude slash commands into trigger descriptions or workflow sections.
- Convert Claude subagent/agent prompts only when they are procedural instructions; otherwise report them as orchestration requirements.
- Convert plugin manifests into dependency notes or a plugin implementation plan.
- Treat MCP configs as required setup. Do not claim the MCP is available unless Codex has the matching tool configured.
- Keep references/assets when they are target-neutral and useful.

## Gemini-to-Codex Rules

- Convert `GEMINI.md` project guidance into `AGENTS.md`; do not treat it as a skill.
- Convert `gemini-extension.json` into a Codex plugin implementation plan or `.codex-plugin/plugin.json` only when fields are known.
- Convert Gemini `commands/*.toml` into workflow sections or Codex command notes.
- Convert Gemini subagent Markdown into `.codex/agents/*.toml` only for known fields.
- Treat Gemini policies and hooks as unsupported until Codex hook or policy equivalents are explicitly mapped.

## Audit Recommendations

In audit-only mode, recommend the concrete Codex staging layout and automatic port work without creating files:

- Skills: `ports/<source-name>/codex/skills/<skill-name>/SKILL.md` for plugin ecosystems.
- Commands: `ports/<source-name>/codex/references/commands.md`.
- Dependencies: `ports/<source-name>/codex/references/dependencies.md`.
- Unsupported behavior: `ports/<source-name>/codex/references/unsupported.md`.

Only list credentials, subscriptions, MCP enablement, app provisioning, final install, and regulated human review as remaining manual steps.

## Validation

Run the Codex skill validator when available:

```bash
python3 /Users/yanivd/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-dir>
```

For index readiness, also run discovery checks when available:

```bash
npx skills add . --list
```

Ask the user before running commands likely to produce large output.
