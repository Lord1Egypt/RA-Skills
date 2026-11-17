# Newsletter Draft Editor (Chinese)

Turn your selected links and notes into an editable Chinese newsletter draft with source links. It is for curated updates, community roundups, and brand newsletters; it does not collect unauthorized mailing lists or send mail.

![Newsletter Draft Editor promo](assets/promo-1600x900.png)

## Input and output

Provide selected links (title, URL, notes), an audience, and section format. The result is Markdown with an introduction, sectioned item summaries, a source link for every item, editorial notes, and a preflight checklist. Missing links, audience, or section structure produce a precise missing-materials request instead of invented content.

See the copyable [successful input](fixtures/success-input.md), [successful delivery](fixtures/success-output.md), [incomplete input](fixtures/failure-input.md), and [missing-materials delivery](fixtures/failure-output.md).

## Install

```bash
npx skills add xxjrq/selfmedia-newsletter-draft-cn
```

## Scope

Process a short article, one chapter, or one scenario at a time; tables are limited to 100 rows. Split larger material into batches. The Skill only writes from supplied material and preserves source URLs.

Reference: the use case was checked against [social-media-skills/skills](https://github.com/social-media-skills/skills/blob/main/skills/email-and-newsletter/SKILL.md); this repository's documentation, workflow, and examples are original. Licensed under [MIT-0](LICENSE).
