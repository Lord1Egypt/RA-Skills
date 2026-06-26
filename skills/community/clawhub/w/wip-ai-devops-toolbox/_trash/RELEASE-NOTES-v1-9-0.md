# v1.9.0: README Formatter, Repo Init, Dev Guide overhaul

Two new tools, eight SKILL.md fixes, and a major Dev Guide update.

## New: wip-readme-format

Auto-generates READMEs following the WIP Computer standard. Detects all six interfaces, reads SKILL.md for tool names, generates badges, "Teach Your AI" block, features, interface coverage table, license block. Works on single repos and toolbox repos.

The key design: generates separate section files instead of one monolithic README.

```
wip-readme-format /path/to/repo          # generates README-init-*.md section files
wip-readme-format /path/to/repo --deploy  # assembles sections into README.md
```

Section files: `README-init-badges.md`, `README-init-title.md`, `README-init-teach.md`, `README-init-features.md`, `README-init-coverage.md`, `README-init-more-info.md`, `README-init-license.md`, `README-init-technical.md`. Edit any section independently, then deploy assembles them in order. Same pattern as release notes: staging, review, deploy.

Also supports `--dry-run` (preview) and `--check` (validate existing README against the standard).

## New: wip-repo-init

Scaffolds the standard `ai/` directory in any repo. Plans, notes, ideas, dev updates, todos. Every folder has self-documenting READMEs.

New repo: creates the full structure. Existing repo: moves old `ai/` contents to `ai/_sort/ai_old/` so you can sort at your own pace. Nothing is deleted.

## Dev Guide: release notes workflow

Both Dev Guides (public and private) now explicitly document the `RELEASE-NOTES-v{version}.md` workflow. Write the release notes file on the branch, commit it with the code, review it in the PR, `wip-release` auto-detects it after merge. Both guides cross-reference each other at the top so agents know to read both.

## Fixes

- Fixed SKILL.md `name:` frontmatter in all 8 existing tools. Interface coverage table now shows human-readable names ("Release Pipeline", "Identity File Protection") instead of directory names ("wip-release", "wip-file-guard").
- Fixed interface coverage table: renamed "OpenClaw" column to "OC Plugin", corrected License Guard row (was falsely claiming Module + CC Hook).
- Skill deployment: `wip-install` now deploys SKILL.md files to `~/.openclaw/skills/<tool>/` so OpenClaw agents can use them.
- Amalgamated interface system notes, README standard, and Universal Installer vision into one reference document.
- Dogfooded wip-repo-init on the toolbox itself. Filled in product bible, roadmap, and readme-first with real content.
- Created plan stubs for all roadmap items (README Formatter, Daily Dev Summary, GitHub Actions Pack, Security Suite).
