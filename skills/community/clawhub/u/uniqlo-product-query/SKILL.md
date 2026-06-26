---
name: uniqlo-product-query
description: Query Uniqlo discounted products for men, women, kids, and baby clothing. Generates a Markdown file with product images, prices, discount rates, and purchase links. Use when the user asks about Uniqlo sales, discounts, promotions, or mentions 优衣库、男装、女装、童装、婴幼儿装、折扣、促销、特价.
---

# Uniqlo Product Query

## Overview

Queries Uniqlo's Chinese API for discounted products and generates a sorted Markdown report with images, pricing, and links.

**Size filtering**: Optional. If user specifies a size, filters by that size. If no size is specified, returns all sizes.

## Usage

```python
from uniqlo_product_query import process_query

# With size filter
response = process_query("查询优衣库女装S码")

# Without size filter (all sizes)
response = process_query("查询优衣库女装")
print(response)
```

Output files are saved to `unique/` directory in the current working directory.

## Categories and Size

| Category | Trigger keywords | API code |
|----------|-----------------|----------|
| Men (男装) | 男装, 男装折扣 | SALE_M |
| Women (女装) | 女装, 女装折扣 | SALE_W |
| Kids (童装) | 童装, 童装折扣 | SALE_K |
| Baby (婴幼儿装) | 婴幼儿装, 婴幼儿装折扣 | SALE_B |

**Size filtering**: Optional. Extracted from user input. If no size is specified, no size filtering is applied. Supports: XXS, XS, S, M, L, XL, XXL, and Chinese sizes (150/76A–180/100A).

## Output

- File format: `{project_root}/unique/优衣库{类别}{尺码}尺码折扣商品清单_{timestamp}.md`
- Products sorted by discount rate ascending (best deals first)
- Only includes products with discount rate ≤ 60%
- Each entry: image, name, original price, current price, discount rate, purchase link

## Dependencies

- requests

