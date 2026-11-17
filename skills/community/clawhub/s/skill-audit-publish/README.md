# Skill Publish

Audit, clean, and publish agent skills to ClawHub and GitHub. Works with any SKILL.md-based skill in the OpenClaw ecosystem.

Complements `skill-design-guide` (design-time) with publish-time workflow.

**Version**: v1.5.7 (2026-09-16)

> ⚠️ **Publish has external side effects.** `audit` mode is read-only. `publish` mode
> transmits the cleaned skill contents to ClawHub and GitHub (public services). The bundled
> sync helper only creates or updates files — it never deletes anything from your repos or
> your machine, and it never modifies your local files. Publishing runs only after an audit
> and your explicit confirmation of the file list, target repos, and version. Treat
> everything you publish as publicly visible.

## Modes

| Mode | Command | Description |
|------|---------|-------------|
| **Audit** | "audit skill" | Read-only scan — reports issues, changes nothing, transmits nothing |
| **Publish** | "publish skill" | After audit + confirmation: clean (in a temp copy) → push to ClawHub/GitHub → verify |

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

## Bundled Scripts

`scripts/sync_skill_to_github.js` — optional helper that mirrors a publish folder to a GitHub repo via the Contents API.

- Token: read from `GITHUB_TOKEN` / `GITHUB_PAT` env vars only; exits with an error if unset. Never embedded, read from files, or logged. (The SkillHub upload stage reads a separate credential from a local file — declared in the skill's frontmatter permissions; it does not involve this helper.)
- Network: talks to `api.github.com` only. Creates/updates files (PUT); **never deletes** anything.
- Fully parameterized: `--owner`, `--repo`, `--dir`, `--message`, `--branch`, `--files`. No hardcoded paths or usernames.

```bash
node scripts/sync_skill_to_github.js --owner <you> --repo <skill-repo> --dir ./publish-my-skill
```

## License

MIT
