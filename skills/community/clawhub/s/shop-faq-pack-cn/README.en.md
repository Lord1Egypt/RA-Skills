# Store FAQ Knowledge Base

![Store FAQ knowledge-base artwork](assets/promo-1600x900.png)

Turn approved shipping, delivery, returns, and product-specification policies into a reusable Chinese FAQ. Missing evidence becomes an explicit merchant follow-up item—never an invented customer promise.

## What you provide

Provide approved, customer-facing policy text or structured fields for shipping, delivery timing, after-sales/returns, and product specifications. Preserve exact amounts, regions, timeframes, and restrictions.

## What you receive

A Markdown knowledge base grouped into ordering & shipping, dispatch & delivery, returns & refunds, and product specifications. Each answer retains its policy basis, followed by a list of fields the merchant must supply. This Skill creates content only; it does not connect to or send messages through customer-service chat.

## Complete examples

The [success policy input](fixtures/success.json) is an explicitly fictional offline merchant simulation. Its [FAQ output](fixtures/success-output.md) covers shipping, delivery, return and exchange conditions and shipping responsibility, refund method, and specifications; every answer cites its source field. It validates the example contract only and proves no real merchant approval or policy.

The [former unapproved input](fixtures/partial-unapproved-input.json) and [partial output](fixtures/partial-unapproved-output.md) preserve the prior facts as a draft, with approval and exchange-policy gaps called out.

The [incomplete input](fixtures/failure-missing-fields.json) has an [actual missing-material response](fixtures/failure-output.md). Vague free-shipping, fast-dispatch, and after-sales wording is not expanded into invented thresholds, deadlines, or eligibility.

The [forward records](fixtures/forward-success.md) document a prior draft-only run; they are not evidence for the fictional success example and do not claim a store visit or customer message.

## Quick check

Run from this repository:

```bash
python3 scripts/self_test.py
```

The self-test checks package structure, the fictional approved success example, preserved unapproved partial example, per-answer policy citations, missing approval/exchange rules, and image dimensions. It does not validate any real-world merchant authorization or policy truth.

The failure fixture is intentionally incomplete beyond product specifications: its vague shipping, delivery, and after-sales statements also require concrete conditions, charges or timing, regional or holiday rules, eligibility, deadlines, shipping-cost responsibility, and refund method.

## Attribution and license

The original Chinese content and fixtures here were independently written. The public [marketingskills sales-enablement Skill](https://github.com/coreyhaines31/marketingskills/blob/main/skills/sales-enablement/SKILL.md) was consulted only for its general use case; no source code or copy was reused. Licensed under [MIT-0](LICENSE).
