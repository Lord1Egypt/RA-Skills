# Product Review Need Miner (Chinese)

![Product review insight visual](assets/promo-1600x900.png)

Turn lawfully provided real product reviews into practical Markdown for product improvements and detail-page updates: recurring needs, positive and negative themes, page additions, and open validation questions. It also works for reader feedback on fiction and audience feedback for Chinese-language creators.

## Input and output

Provide a product/work name, category, and review text (all required), plus any available source fields such as rating, date, use case, or version. [SKILL.md](SKILL.md) returns a brief that separates known evidence from recommendations.

If the product/work name, category, or review text is absent, the Skill reports each gap and stops rather than inventing an answer. It does not scrape platform comments, compare public lookalike prices, or replace Douyin-comment research.

## Quick use

```text
Use $shop-review-miner-cn to analyze these lawfully provided real product reviews. Keep source field values unchanged and return recurring needs, positive/negative themes, and detail-page additions. State missing information when evidence is insufficient.
```

See the [valid fixture](fixtures/success.json) and [missing-review fixture](fixtures/failure-missing-reviews.json).

## Self-test

Run `python3 scripts/self_test.py` from the repository root. It checks packaging, fields, image dimensions, and explicit fixture expectations: a one-off signal is not recurring, evidence is separated from recommendations, and missing review text stops analysis. It does not run or claim to run qualitative analysis; assess that against real authorized material.

## Source and license

The use case was informed by [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills), specifically its customer-research Skill. No source code or copy was reproduced; this repository's instructions, workflow, and fixtures are original. The referenced repository uses MIT; this ClawHub package is licensed under [MIT-0](LICENSE).
