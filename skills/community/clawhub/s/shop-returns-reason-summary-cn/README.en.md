# Return-Reason Summary & Product Improvements

![Return-reason summary promotion](assets/promo-1600x900.png)

Turn de-identified return or refund reasons and product details into auditable counts and practical, testable listing improvements.

Built for Chinese-speaking small-shop operators, fiction authors, and self-media creators reviewing existing after-sales feedback. It does not invent missing data, make financial conclusions, or replace customer-service replies.

## Use

Provide JSON, CSV, a table, or a list. Each record needs a product name (or product ID) and a return/refund reason. An anonymized order ID, date, variant, and note are useful optional fields.

The workflow returns traceable reason categories, counts by category and product, recommendations explicitly separated from known facts, and any missing or excluded records. [fixtures/success.json](fixtures/success.json) pairs de-identified `input_records` with a complete expected workflow result, including count conservation and product-level facts. [fixtures/failure-missing-reason.json](fixtures/failure-missing-reason.json) demonstrates the required explicit error when a reason is absent; it must not be inferred.

Run `sh scripts/self-test.sh` from this repository to validate package structure and fixture contracts, including count conservation and fact/recommendation separation. This is not a business engine; see [SKILL.md](SKILL.md) for the live Markdown workflow.

## Source and license

The implementation and documentation are original. Saleor was consulted only as public e-commerce domain context; no code or copy was used: [Saleor](https://github.com/saleor/saleor) (BSD-3-Clause). This repository is licensed under the [MIT-0](LICENSE).
