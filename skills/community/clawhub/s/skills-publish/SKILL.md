---
name: clawhub-publish
description: Publish an OpenClaw skill to ClawHub with release checks, version metadata, and command generation. Use when you need to prepare a skill for first publication, publish a new version, validate slug, name, and semver inputs, or generate the exact clawhub publish command before release.
metadata: { "openclaw": { "emoji": "🚀", "requires": { "bins": ["python3", "clawhub"] } } }
---

# Clawhub Publish

Prepare a skill for ClawHub release, generate the publish command, and verify the release inputs before anything is uploaded.

## Quick Start

1. Point this skill at the target skill folder.
2. Run the release checker to catch obvious metadata and packaging issues.
3. Fill in slug, display name, version, changelog, and tags.
4. Review the generated `clawhub publish` command before running it.
5. Fix any public-facing language, personal path, or placeholder issues before release.

## Prerequisites

- `python3` available for the local checker script.
- `clawhub` CLI installed.
- Authentication established with `clawhub login` or `clawhub login --token <token>` before actual publish.
- A target skill folder with a valid `SKILL.md`.

## Example Prompts

- `Prepare this skill for first publish to ClawHub and generate the exact publish command.`
- `Check whether this skill is safe to publish, then draft the clawhub publish command for version 1.2.0.`
- `I need to release a new ClawHub version of this skill. Validate the metadata and show me what to run.`
- `Audit this skill's release inputs before I publish it to ClawHub.`

## When to Use This Skill

Use this skill when the goal is to publish or update a skill on ClawHub with fewer release mistakes.

Typical use cases:

- First-time publication of a new skill
- Publishing a new semver version of an existing skill
- Validating slug, name, version, changelog, and tags before release
- Checking whether a local skill package looks publishable

## When Not to Use

Do not use this skill for tasks that are primarily about skill quality or listing optimization.

Use a different workflow when you need to:

- Improve search visibility or listing copy: use `skill-seo`
- Evaluate quality, regressions, or trigger accuracy: use `skill-test`
- Create a new skill from scratch: use `skill-creator`
- Debug runtime issues inside the target skill itself

## If Publishing Is Inconclusive

If the local checks are clean but release confidence is still low, say what remains unverified.

Common next steps:

- Confirm `clawhub whoami` before publishing
- Run `skill-test` for quality concerns
- Run `skill-seo` for discoverability concerns
- Compare the target skill against the currently published version if this is an update

## Pre-Publish Checklist

Before publishing, confirm all of the following:

- `SKILL.md` has valid frontmatter and no obvious placeholders
- Public-facing copy matches the intended audience language
- No personal file paths, usernames, or internal-only identifiers leak into the package
- Slug, display name, version, changelog, and tags are ready
- Any remaining release risk has been explained to the user

## Versioning Guide

Use semantic versioning deliberately:

| Change type | Suggested version |
| --- | --- |
| First publish | `1.0.0` |
| Small wording or typo fix | `1.0.1` |
| Content improvement or meaningful documentation update | `1.1.0` |
| Major workflow or structure rewrite | `2.0.0` |

If the user already has a versioning policy, follow it instead of this default table.

## Workflow

1. Read the target skill's `SKILL.md` and inspect the directory contents.
2. Run the local checker:

   ```sh
   python3 {baseDir}/scripts/check_publish_ready.py /path/to/skill
   ```

3. Collect release inputs:
   - `slug`
   - display `name`
   - `version`
   - `changelog`
   - `tags`
4. Re-run the checker with release inputs to generate the exact publish command.
5. Present the command and any warnings to the user for confirmation.
6. If the user wants execution, run the generated `clawhub publish ...` command.
7. After publishing, verify the result with `clawhub search "<slug>"` or by opening the ClawHub page.

## Batch Publish

When publishing multiple skills:

1. Run the local checker for each skill independently.
2. Review slug, version, and changelog for each release.
3. Publish one skill at a time so failures stay attributable.
4. Verify each published slug before moving to the next one.

## Commands

```sh
# Baseline release audit
python3 {baseDir}/scripts/check_publish_ready.py /path/to/skill

# Release audit plus publish command preview
python3 {baseDir}/scripts/check_publish_ready.py /path/to/skill \
  --slug my-skill \
  --display-name "My Skill" \
  --version 1.0.0 \
  --changelog "Initial release" \
  --tags latest

# Actual publish command after review
clawhub publish /path/to/skill --slug my-skill --name "My Skill" --version 1.0.0 --changelog "Initial release" --tags latest
```

## Definition of Done

- The local checker has run against the target skill.
- Required release inputs have been validated or explicitly flagged as missing.
- A concrete `clawhub publish ...` command has been prepared.
- Any publish blockers or warnings have been explained to the user.
- If a publish was requested, the post-publish verification step has been completed.

## Assistant Responsibilities

- Distinguish publish blockers from optional improvements.
- Do not run `clawhub publish` until the user confirms the release inputs.
- Be explicit about what was verified locally versus what still depends on ClawHub or authentication.
- Preserve the target skill's actual metadata unless the user asks for edits.

## Notes and Constraints

- Local checks cannot guarantee that ClawHub authentication is valid unless the publish command is actually run.
- This skill helps generate and review the release command; it should not silently publish.
- `slug` should usually match the local directory name unless the user has a clear migration reason.
- Treat version bumps as intentional release actions, not automatic fixes.
- Publishing a technically valid skill is not the same as publishing a good skill; use `skill-test` and `skill-seo` if quality or discoverability is still in doubt.

## Common Errors

- `clawhub` CLI missing: install it before attempting publish
- not logged in: run `clawhub login`, or use `clawhub login --token <token>`, then confirm with `clawhub whoami`
- slug rejected or already taken: choose a more specific slug
- invalid semver: correct the version before generating the final command

## Resources

- ClawHub publish flow and flags: [references/publish-flow.md](references/publish-flow.md)
- Release checklist and common blockers: [references/release-checklist.md](references/release-checklist.md)
- Local release checklist: [references/checklist.md](references/checklist.md)
- Common publish errors and fixes: [references/common-errors.md](references/common-errors.md)
