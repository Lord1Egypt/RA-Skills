# Owned Content Reuse Map

![Promotion image](assets/promo-1600x900.png)

Turn your owned articles, posts, store notes, or story materials into a traceable list of content to update, split, or bundle—without chasing or copying competitors' viral work.

Give the Skill a content inventory with a summary for each item. It returns reuse candidates, new angles clearly marked as suggestions, and the fields that still need to be supplied. It is designed for Chinese small-business owners, fiction writers, and independent creators.

## Input

Each content item needs `id`, `title`, `published_at`, `platform`, and `summary`. Optional source observations such as comments can be supplied as `audience_signal`. The [successful fixture](fixtures/success.json) includes both a complete owned-content input and the expected Markdown delivery.

If a required field is absent, the Skill lists the gap instead of inventing it and stops recommendations for that item; see the [missing-summary fixture](fixtures/failure-missing-summary.json).

## What it does

A Markdown checklist with:

- candidates for **update**, **split**, and **bundle**;
- the supplied evidence behind each candidate;
- inferred suggestions separated from known facts; and
- missing material or manual confirmations.

## Run the package check

```bash
./scripts/self-test.sh
```

This check separates package structure from fixture semantics: it verifies the documented evidence for update/split/bundle suggestions and the missing-field stop rule, but does not pretend to be a recommendation engine. Apply the workflow in [SKILL.md](SKILL.md) to your own inventory for real behavior.

## Scope and source note

This Skill only works from content you own or provide. It does not scrape, reproduce, or imitate competitor work. Its public-use reference was [social-media-skills/skills](https://github.com/social-media-skills/skills); the Chinese workflow and examples here are original. Licensed under [MIT-0](LICENSE).

## Install

```bash
npx skills add xxjrq/selfmedia-reuse-map-cn
```
