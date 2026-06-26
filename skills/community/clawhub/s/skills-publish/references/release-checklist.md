# Release Checklist

Use this checklist before publishing a skill to ClawHub.

## Packaging

- `SKILL.md` exists
- `name` matches the local directory
- `description` is present and includes `Use when ...`
- referenced files exist
- commands use `{baseDir}` when appropriate
- no obvious TODO placeholders remain
- no personal file paths or internal-only references leak into public docs

## Release Inputs

- `slug` chosen and reviewed
- display name chosen and reviewed
- semver version chosen
- changelog drafted
- tags chosen

## Confidence Checks

- no obvious publish blocker in local structure
- prerequisites and limits are documented
- any release risk has been explained
- authentication state is known if publish execution is requested

## Optional Checks

- run `skill-test` for quality before release
- run `skill-seo` for directory discoverability
- compare against the previous published version if updating
