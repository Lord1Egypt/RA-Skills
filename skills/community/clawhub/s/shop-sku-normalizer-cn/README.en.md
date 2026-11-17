# Product Specification & SKU Normalizer

![Product Specification & SKU Normalizer promo](assets/promo-1600x900.png)

Turn a messy product name, color, size, and model table into consistent naming, duplicate/missing-spec reports, and a reviewable CSV import draft. It helps Chinese small-shop owners and creators catch data issues before publishing.

## What it does

- Works only with up to 100 rows supplied by the user.
- Preserves accurate source values and labels normalization as a suggestion.
- Flags duplicate combinations, missing fields, and items needing confirmation without inventing data; every row in a duplicate group needs confirmation with a stable reason.
- Produces a reviewable CSV draft; it never reads inventory vaults, connects to a back office, or imports data.

## Input and output

Provide a table, CSV, TSV, or plain text with `商品名称` (product name), `颜色` (color), `尺寸` (size), and `型号` (model). The output is a normalized naming table, an issue report, and a CSV import draft. The draft includes a `待确认原因` (reason for review) column, and every duplicate row is marked `待确认` (needs review). If a key field is absent, the skill reports it and does not make an importable draft.

See [success fixture](fixtures/success-products.txt) and [failure fixture](fixtures/failure-missing-field.txt). Run `bash scripts/self-test.sh` to validate the package structure, metadata, image dimensions, and fixture shapes. It does not simulate the Markdown workflow's real behavior.

## Source and license

This is original documentation and examples. [ERPNext](https://github.com/frappe/erpnext) was consulted only for the public project use case; no code or copy was reused. Licensed under [MIT-0](LICENSE).

## Install

```bash
npx skills add xxjrq/shop-sku-normalizer-cn
```

## Complete response examples

See the [success response](fixtures/forward-success.md) and [missing-information response](fixtures/forward-failure.md) alongside the input fixtures.
