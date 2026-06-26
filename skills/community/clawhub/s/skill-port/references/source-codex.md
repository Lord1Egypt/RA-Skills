# Codex Source Adapter

Use this reference when the source is a Codex skill, Codex plugin, project instruction bundle, custom-agent bundle, hook config, MCP config, or Codex plugin marketplace.

## Artifact Mapping

| Codex artifact | Target handling |
| --- | --- |
| `SKILL.md` | Usually portable after frontmatter, wording, and path cleanup. |
| `.agents/skills/<name>/SKILL.md` or `~/.agents/skills/<name>/SKILL.md` | Treat as Agent Skills-compatible source. Stage under the target agent's skill location. |
| `agents/openai.yaml` | Codex-specific metadata. Preserve as notes unless the target has equivalent UI/dependency metadata. |
| `AGENTS.md`, `AGENTS.override.md`, nested instruction files | Treat as project instructions. Translate or bridge to target guidance such as `CLAUDE.md` or `GEMINI.md`; do not package as a skill. |
| `.codex-plugin/plugin.json` | Convert into a target plugin/extension manifest only when target package fields are known; otherwise document as plugin implementation notes. |
| `.agents/plugins/marketplace.json` | Treat as distribution metadata. Do not assume another agent can consume it directly. |
| `.codex/agents/*.toml` or `~/.codex/agents/*.toml` | Convert required fields and instructions into target subagent format when supported; otherwise mark partial. |
| `.codex/config.toml`, `~/.codex/config.toml`, `[mcp_servers.*]` | Treat MCP/tool setup as dependency-bound. Convert simple configs only with target-specific review. |
| `.codex/hooks.json`, `hooks/hooks.json`, inline hooks in `config.toml` | Treat as risky lifecycle behavior. Convert only with known event/matcher/input/output mapping. |

## Codex-Specific Signals

Flag these because they require target adaptation:

- `AGENTS.md` and `AGENTS.override.md` instruction layering.
- `.codex-plugin/plugin.json` plugin metadata.
- `.agents/plugins/marketplace.json` marketplace metadata.
- `.codex/agents/*.toml` custom agents.
- `agents/openai.yaml` skill UI/dependency metadata.
- Codex MCP config in TOML.
- Codex hook events and plugin hook feature flags.

## Rewrite Rules

- Convert `AGENTS.md` into the target's project-instruction file, not into a skill.
- Convert Codex custom-agent TOML into the target's agent format only for known fields: name, description, instructions, model/effort when meaningful, sandbox/tool notes as compatibility warnings.
- Preserve skill instructions, scripts, references, and assets when target-neutral.
- Preserve Codex-only metadata as notes unless the target supports an equivalent field.
- Keep MCP auth, scopes, trust, tool allow/deny lists, and project-trust behavior as dependency notes.
- Keep hooks inactive until target lifecycle semantics are reviewed.

## Classification Defaults

- Plain skills are usually portable.
- `AGENTS.md` is translated/bridged.
- Plugin manifests are partial.
- Custom agents are partial.
- MCP config is dependency-bound.
- Hooks are unsupported by default unless explicitly mapped.
