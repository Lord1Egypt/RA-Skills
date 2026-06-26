# ClawHub Publish Checklist

Use this checklist when preparing marketplace submission for this skill.

## Pre-publish

1. Validate structure locally:

```bash
python3 /Users/petercsipkay/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/useclick-link-shortening-analytics
```

2. Confirm metadata quality:
- Clear display name
- Short description for discovery
- Default prompt includes `$useclick-link-shortening-analytics`

3. Confirm technical accuracy:
- Endpoints and payload fields match backend behavior.
- Plan limits match pricing source.

## Publish (OpenClaw)

From the repository root, publish using OpenClaw CLI for your skill directory.

```bash
openclaw publish skills/useclick-link-shortening-analytics
```

If your CLI version uses a different subcommand format, run:

```bash
openclaw --help
openclaw publish --help
```

and use the equivalent publish command for the same folder.

## Listing Positioning

Emphasize:

- API-first short-linking workflows
- Plan-aware guidance (reduces failed integrations)
- Analytics and geo-targeting recipes
- Upgrade-aware fallbacks for Free users
