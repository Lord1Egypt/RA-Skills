# Project Rules

## Publishing Workflow

When updating this skill:

1. Make changes in `~/.claude/skills/slowmist-security-cc/`
2. Sync changes to `/tmp/slowmist-security-cc/` (git working directory)
3. Commit and push from `/tmp/slowmist-security-cc/`
4. Re-publish to ClawHub if metadata changed

## File Sync

Reference files (`references/*.md`) are identical copies between:
- `~/.claude/skills/slowmist-security-cc/references/`
- `/tmp/slowmist-security-cc/references/`

SKILL.md is the source of truth for the skill entry point.
README.md is the source of truth for documentation.
