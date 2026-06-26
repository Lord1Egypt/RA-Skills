---
name: shopify-jsonld-parser
description: >
  Parse JSON-LD structured data from Shopify product pages to extract commerce details
  like product info, offers (price, currency, availability), and inventory status from
  schema.org/Product and Offer. Use when: (1) analyzing Shopify HTML for product
  offers/pricing/stock, (2) extracting structured commerce data from web pages or local
  files, (3) querying JSON-LD for availability (InStock/OutOfStock/PreOrder), prices
  across variants, or offer counts. Handles @graph arrays and multiple scripts.
---

# Shopify JSON-LD Parser

Parse JSON-LD from Shopify product pages (or any schema.org/Product JSON-LD) to extract structured commerce data reliably.

## Quick Start

1. Fetch HTML: `web_fetch` a product page URL.
2. Parse: Run `scripts/parse_shopify_jsonld.py input.html` (outputs JSON).
3. Query output for offers, availability, etc.

Example:
```
exec command="python3 skills/shopify-jsonld-parser/scripts/parse_shopify_jsonld.py page.html"
```

## Workflow

1. **Input**: HTML file/path with JSON-LD (from `web_fetch`, `read`, or local).
2. **Find JSON-LD**: Script extracts all `<script type="application/ld+json">` contents.
3. **Parse Product**: Traverse @graph or root for `@type: Product`, extract:
   - name, description, image, sku, brand
   - offers: array of Offer objects → price, priceCurrency, availability, url, itemCondition
   - availability (product-level or per-offer): http://schema.org/InStock, OutOfStock, PreOrder, etc.
   - Variants: Infer from multiple offers or hasVariant.
4. **Output**: Clean JSON: `{product: {...}, offers: [...], inventory_status: "InStock|OutOfStock|Limited|Unknown"}`

Inventory is typically **availability enum**, not exact quantity (use Shopify API for levels). Map:
- InStock → available
- OutOfStock → unavailable
- PreOrder/BackOrder → preorder

## Usage Examples

**Extract offers from page:**
```
read path="shopify-page.html" → html
write path="tmp.html" content=html
exec command="python3 skills/shopify-jsonld-parser/scripts/parse_shopify_jsonld.py tmp.html" → parsed.json
read path="parsed.json"
```

**Query CLI-style:**
Add `--query price` or `--field offers[0].availability` flags to script.

## Script Reference

`scripts/parse_shopify_jsonld.py [input.html] [--query FIELD] [--output json|yaml]`

- Handles malformed JSON-LD gracefully.
- Supports multiple @graph items.
- Validates schema.org types.

## Schema Reference

See `references/schema.md` for schema.org/Product + Offer properties.

## Troubleshooting

- No JSON-LD: Returns `{error: "No product JSON-LD found"}`
- Multiple products: Takes first @type:Product.
- Dynamic Liquid: Static HTML only (no JS-rendered).
