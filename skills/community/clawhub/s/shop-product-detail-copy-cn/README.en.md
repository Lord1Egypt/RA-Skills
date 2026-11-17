# Product Detail Page Copy (Chinese)

![Product-detail-copy promo](assets/promo-1600x900.png)

Turn merchant-confirmed product facts into a ready-to-publish Chinese product detail page: hero copy, evidence-backed selling points, specifications, image captions, and FAQs. Facts, suggestions, and unanswered questions remain visibly separate.

This is a Markdown-only Skill with no browser, service, or third-party API dependency. It is for complete store detail modules, not second-hand listing titles or generic customer-service replies.

## Input

Provide `product_name`, `specifications`, `image_notes`, and `target_audience`. Preserve the merchant's original values for factual fields. Optional `known_facts` and `suggestions` make the evidence boundary explicit.

See [SKILL.md](SKILL.md) for the exact input and output contract, and [fixtures](fixtures/) for valid and missing-field examples.

## Result

The output contains a fixed, usable module sequence: hero value proposition, selling points with evidence, a specification table, image captions, gentle suitability notes, FAQ, and a fact/suggestion/pending-confirmation boundary.

## Self-test

```bash
bash scripts/self-test.sh
```

The test checks distributable structure, manifest fields, image dimensions, and fixture structure only. It does not claim to validate copy quality.

## Attribution and license

The use case was informed by [marketingskills](https://github.com/coreyhaines31/marketingskills) and its [copywriting Skill](https://github.com/coreyhaines31/marketingskills/blob/main/skills/copywriting/SKILL.md). This repository's Chinese instructions, workflow, and examples are original and do not copy their source or copy. Licensed under [MIT-0](LICENSE).

## Install

```bash
npx skills add xxjrq/shop-product-detail-copy-cn
```

## Complete response examples

See the [success response](fixtures/forward-success.md) and [missing-information response](fixtures/forward-failure.md) alongside the input fixtures.
