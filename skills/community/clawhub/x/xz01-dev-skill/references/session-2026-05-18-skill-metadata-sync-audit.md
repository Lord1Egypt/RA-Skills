# Session note: skill metadata sync must be audited before publish

## Trigger

During xz01 pagination remediation, the skill's `SKILL.md` frontmatter had advanced beyond the metadata files: `SKILL.md` showed a newer version while `skill.json` / `_meta.json` still reflected the previous release.

## Durable lesson

For xz01 skill updates, editing and publishing are not enough if metadata files drift. Treat version/description sync as a blocking pre-publish audit.

## Required audit

Before publishing any xz01 skill update:

1. Check `SKILL.md` frontmatter `version`.
2. Check `skill.json` `version` and description.
3. Check `_meta.json` `version`, description, and changelog.
4. Confirm the version is identical in all three files.
5. Confirm the descriptions/changelog describe the actual change just made.
6. Only then run `clawhub publish`.

After publish, record the published version and publish ID in the user-facing report.

## Why this matters

A mismatch makes later sessions load or report stale skill metadata and can hide the fact that the latest durable rule was not fully packaged.
