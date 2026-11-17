# Profile Bio Positioning Copy

![Profile bio positioning promo](assets/promo-1600x900.png)

Turn a creator's real experience into a profile visitors understand immediately: ready-to-use bios, sustainable content pillars, and three pinned-post recommendations. Designed for Chinese small-shop owners, fiction writers, and independent creators.

## Input and output

Provide real credentials, content direction, and target audience. Platform, tone, and exclusions are optional. The skill preserves supplied local facts verbatim and separates known facts from writing recommendations.

It returns Markdown with three bio options, three to five content pillars, and three pinned-content suggestions. When a required field is absent, it names what is missing instead of inventing credentials, results, or audience insights. It writes for the owner's profile only; it is not a public audit of someone else's Douyin account.

## Fixtures

[fixtures/success.json](fixtures/success.json) includes complete input and expected examples of all three deliverables. [fixtures/failure-missing-fields.json](fixtures/failure-missing-fields.json) specifies the missing fields, follow-up questions, and deliverables that must not be generated; “I want to start doing self-media” is not a real credential.

## Validate

Run `python3 scripts/self_test.py` from this directory. The check covers package structure, metadata, image dimensions, and the expected-result contracts in the complete and incomplete fixtures. It does not run a fictional copy-generation engine or claim to validate real Skill behavior, copy quality, or factual accuracy.

## Source and license

This skill references the intended use of [social-media-skills/skills](https://github.com/social-media-skills/skills) and its [profile-optimization skill](https://github.com/social-media-skills/skills/blob/main/skills/profile-optimization/SKILL.md). Its Chinese instructions, workflow, and samples are original. Licensed under the [MIT-0](LICENSE).

## Complete response examples

See the [success response](fixtures/forward-success.md) and [missing-information response](fixtures/forward-failure.md) alongside the original inputs.

## Install

```bash
npx skills add xxjrq/selfmedia-bio-positioning-cn
```
