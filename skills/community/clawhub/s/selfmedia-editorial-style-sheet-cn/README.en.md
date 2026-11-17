# Editorial Style Sheet

Turn three to five approved articles from one editorial column into a reusable Markdown style sheet. It helps future pieces stay consistent in tone, sentence length, terminology, and number formatting without copying an author's distinctive passages.

![Editorial Style Sheet promo](assets/promo-1600x900.png)

## Input and delivery

Provide 3–5 mature, user-owned articles (up to 8,000 Chinese characters total), target readers, an approved glossary, and expressions that must be retained. The delivery is a reusable style sheet with short evidence excerpts and a checklist for the next article.

If representative articles are missing or the samples are too inconsistent, the Skill asks for an explicit baseline. It never infers a style from an account name or slogan.

## Install

```bash
npx skills add xxjrq/selfmedia-editorial-style-sheet-cn
```

Copyable examples: [successful input](fixtures/success-input.md), [successful delivery](fixtures/success-output.md), [missing-material input](fixtures/failure-input.md), and [missing-material response](fixtures/failure-output.md).

## Scope

This Skill standardizes article expression only. It does not create profile copy, account positioning, editorial calendars, or long-form stylistic imitation.

## Self-test

```bash
node scripts/self-test.mjs
```

The test runs only inside this repository and checks required release files, names, icon dimensions, and the concrete success/failure deliveries.

## Source and license

The public [marketingskills repository](https://github.com/coreyhaines31/marketingskills) and its [copy-editing Skill](https://github.com/coreyhaines31/marketingskills/blob/main/skills/copy-editing/SKILL.md) were consulted for business purpose only. This repository contains original instructions and examples and does not copy external prose or source code. Licensed under [MIT-0](LICENSE).
