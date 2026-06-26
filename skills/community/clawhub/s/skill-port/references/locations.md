# Location Policy

Use target-agent staging by default. Porting and installation are separate operations.

## Source Cases

| Source case | Handling |
| --- | --- |
| Direct skill folder | Inspect the folder containing `SKILL.md`. |
| Local repo checkout | Inspect the checkout without installing anything. |
| Local installed skill | Inspect the install path read-only. Do not modify it. |
| Local installed plugin | Inspect the plugin path read-only. Do not run plugin commands. |
| Remote GitHub URL | Clone/fetch into a temporary inspection directory only after explicit execution approval. |
| Large repo | Ask the user to run focused commands if output would be too costly. |

## Output Cases

| Output case | Default path |
| --- | --- |
| Single skill to Codex | `skills/codex/<skill-name>/` |
| Multi-skill/plugin to Codex | `ports/<source-name>/codex/` |
| Single skill to Claude | `skills/claude/<skill-name>/` |
| Multi-skill/plugin to Claude | `ports/<source-name>/claude/` |
| Single skill to Gemini | `skills/gemini/<skill-name>/` |
| Multi-skill/extension to Gemini | `ports/<source-name>/gemini/` |
| Other target agent | `skills/<target-agent>/<skill-name>/` or `ports/<source-name>/<target-agent>/` |
| Audit-only report | No ported files. JSON/Markdown report only. |

## Install Policy

- Do not install by default.
- Do not mutate `~/.codex/skills`, `~/.claude`, `~/.gemini`, `.codex/`, `.claude/`, `.gemini/`, or `.agents/skills/` during porting.
- If the user asks to install after reviewing the report, use the target agent's normal installer and ask whether the scope is project or global when that choice matters.
- Prefer symlink/canonical install behavior where supported by the installer; use copy mode only when requested or required.
