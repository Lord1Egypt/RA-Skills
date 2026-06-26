# tiktok-to-mealie

OpenClaw skill for turning TikTok cooking links into structured recipes and importing them into Mealie.

## What it does

- resolves TikTok recipe links
- extracts available recipe clues
- reconstructs a usable recipe
- localizes the recipe to the user's language when needed
- imports the result into Mealie
- uploads a cover image when available

## Best for

- TikTok cooking links
- short-form recipe content
- turning messy social content into usable recipes
- execution-focused recipe workflows

## Included files

- `SKILL.md`
- `references/workflow.md`
- `references/mealie-api-notes.md`
- `references/localization.md`
- `references/failure-modes.md`
- `references/output-templates.md`
- `references/configuration.md`

## Configuration

This skill needs:
- a Mealie base URL
- a Mealie API token

Recommended options:
- environment variables: `MEALIE_BASE_URL`, `MEALIE_API_TOKEN`
- or local secret files under `~/.openclaw/secrets/`

See `references/configuration.md` for details.

## Philosophy

This skill prefers:
- a usable recipe over a noisy scrape
- clean failure over importing junk
- concise output over commentary

## Success behavior

On success, return the final recipe link.
