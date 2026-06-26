# Skill Publish

Audit, clean, and publish agent skills to ClawHub and GitHub. Works with any SKILL.md-based skill in the OpenClaw ecosystem.

Complements `skill-design-guide` (design-time) with publish-time workflow.

**Version**: v1.0.1 (2026-06-06)

## Modes

| Mode | Command | Description |
|------|---------|-------------|
| **Audit** | "audit skill" | Scan only — report issues, no changes |
| **Publish** | "publish skill" | Full pipeline: audit → clean → push → verify |

## What It Checks

1. **Personal data** — share counts, cost basis, account values, personal names
2. **Frontmatter** — description length, language, version numbers in name
3. **Content** — internal dev notes, references sections, version history
4. **Language** — English SKILL.md body, bilingual READMEs
5. **Files** — ticker-specific scripts, meta-documents, outdated files

## Quick Start

```bash
# Audit a skill directory
"audit skill ~/.workbuddy/skills/my-skill"

# Publish to ClawHub + GitHub
"publish skill ~/.workbuddy/skills/my-skill@1.2.0"
```

## License

MIT
