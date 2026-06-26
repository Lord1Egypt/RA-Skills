# Host adapter: Claude Code

## Typical skill locations

Paths vary by install; verify on the user's machine.

| Scope | Common locations |
|-------|------------------|
| User (Anthropic Claude Code) | `~/.claude/skills/<skill-name>/SKILL.md` |
| Project | `<repo>/.claude/skills/<skill-name>/SKILL.md` or plugin bundles per CC docs |

Consult current [Claude Code documentation](https://docs.anthropic.com/claude-code) for the authoritative layout if these paths drift.

## Installing `skill-hr`

1. Copy this repository folder `packages/skill-hr/` to a directory named `skill-hr` under the Claude Code skills root (so `SKILL.md` resolves as `skill-hr/SKILL.md`).
2. Restart or reload skills if your CC version requires it.

## Discovering installed skills for P02

- Enumerate sibling directories under the skills root; read each `SKILL.md` frontmatter (`name`, `description`).
- Merge with `.skill-hr/registry.json` if present in the **workspace** (project-specific HR state).

## Tools assumption

Claude Code agents typically have shell, file read/write, and optional MCP. Recruitment flows should **prefer** `git clone` into the skills directory over opaque installers when source is public.

## Incident and registry paths

Use **workspace root** paths documented in `references/06-state-and-artifacts.md` so HR state travels with the repo when desired.
