---
name: skill-quick-publish
description: One-click skill publishing automation covering duplicate check, Bear notes sync, and GitHub push. Use when publishing a new or updated skill to ClawHub and GitHub, or when the user says "publish skill", "push skill", "release skill", or "一键发布".
---

# Skill Quick Publish

Automate the full skill publishing pipeline: duplicate check → Bear dev-log sync → GitHub push → ClawHub publish.

## Prerequisites

- `clawhub` CLI installed and authenticated (`clawhub whoami`)
- `git` CLI available with push access to target repo
- (Optional) `grizzly` CLI for Bear notes sync on macOS

## Workflow

Run the main orchestrator script:

```bash
bash SKILL_DIR/scripts/publish.sh <skill-path> [options]
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--repo <owner/repo>` | GitHub repo to push to | (required or set `SKILL_GH_REPO`) |
| `--branch <name>` | Target branch | `main` |
| `--skip-bear` | Skip Bear notes sync | `false` |
| `--skip-github` | Skip GitHub push | `false` |
| `--dry-run` | Preview all steps without executing | `false` |
| `--changelog <msg>` | Changelog message for ClawHub publish | `"Automated publish"` |
| `--version <semver>` | Version for ClawHub publish | Auto from SKILL.md or `0.1.0` |

### Environment Variables

- `SKILL_GH_REPO` — Default GitHub repo (e.g., `user/skills`)
- `SKILL_BEAR_TAG` — Bear note tag for dev logs (default: `skill-dev`)
- `GRIZZLY_TOKEN_FILE` — Path to Bear API token (default: `~/.config/grizzly/token`)

## Steps in Detail

### 1. Duplicate Check

Validates skill name uniqueness against:
- Locally installed skills (`~/.openclaw/skills/`)
- ClawHub registry (`clawhub search`)

Exits with error if a conflicting skill exists, unless `--force` is passed.

### 2. Bear Notes Sync

Creates or appends a dev-log note in Bear:
- Title: `[Skill Dev] <skill-name>`
- Tag: value of `SKILL_BEAR_TAG`
- Content: timestamp, version, changelog summary

On non-macOS or when `grizzly` is unavailable, prints a structured log line to stdout instead (so the pipeline continues).

### 3. GitHub Push

Commits and pushes the skill directory to the configured GitHub repo:
1. Clones/pulls the target repo to a temp directory
2. Copies skill files into the repo under `skills/<skill-name>/`
3. Commits with message: `feat(skill): publish <skill-name> v<version>`
4. Pushes to the target branch

### 4. ClawHub Publish

Runs `clawhub publish` with the skill path, slug, name, version, and changelog.

## Error Handling

- Each step logs `✅` on success, `❌` on failure
- The pipeline stops on the first failure unless `--continue-on-error` is set
- Bear sync failure is non-fatal by default (warns and continues)

## Examples

```bash
# Full publish
bash scripts/publish.sh ./my-skill --repo user/skills --version 1.0.0

# Dry run
bash scripts/publish.sh ./my-skill --repo user/skills --dry-run

# Skip Bear and GitHub, only ClawHub
bash scripts/publish.sh ./my-skill --repo user/skills --skip-bear --skip-github

# Using env var for repo
SKILL_GH_REPO=user/skills bash scripts/publish.sh ./my-skill
```