---
name: compare
description: |
  Cross-platform second-hand price search by keyword across multiple marketplaces.
  Triggers on: compare prices, find deals, cheapest, best deal,
  比价, 找低价, 价格对比, 便宜货.
version: 0.6.4
---

# Price comparison

Search second-hand listings by keyword across platforms and return price-sorted results.

> If the user writes in Chinese, see [../../references/zh-CN.md](../../references/zh-CN.md) (Compare section).

## Skill boundaries (mandatory)

**Allowed CLI subcommands only:**

| Subcommand | Purpose |
|------------|---------|
| `compare` | Cross-platform price search |
| `platforms` | List supported platforms |
| `install` | Install bb-browser site adapters |

---

## Intent routing

1. User wants compare / cheapest / best deal / 比价 → run compare flow.
2. User gives product name and optional city → search directly.
3. User asks which platforms are supported → run `platforms`.

## Workflow

### Cross-platform compare (search all platforms unless user narrows scope)

```bash
# Basic compare (UK default)
python scripts/cli.py compare \
  --keyword "iPhone 15 Pro" \
  --city london \
  --country uk

# Specific platforms
python scripts/cli.py compare \
  --keyword "MacBook Air M2" \
  --platforms ok,gumtree

# City and top N
python scripts/cli.py compare \
  --keyword "PS5" \
  --city london \
  --top 10
```

### Parameters

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `--keyword` | Search keywords | Yes | — |
| `--city` | City slug (`london`, `los-angeles`, etc.) | No | `london` (UK focus) |
| `--country` | Country code for OK.com | No | `uk` |
| `--platforms` | Comma-separated (`ok,gumtree,ebay,amazon`) | No | all |
| `--top` | Top N lowest per platform | No | `5` |

### Output format

Present a table with price, platform, title, and link:

```
📊 iPhone 15 Pro — cross-platform results (London)

Rank | Price   | Platform  | Title                         | Link
1    | £750.00 | Gumtree   | iPhone 15 Pro 128GB Unlocked  | https://www.gumtree.com/...
2    | £780.00 | eBay UK   | iPhone 15 Pro like new        | https://www.ebay.co.uk/itm/...
3    | £799.00 | Amazon UK | iPhone 15 Pro 256GB Renewed   | https://www.amazon.co.uk/dp/...
```

> **Important**: Every row must include a clickable listing URL (`url` field).

### Relevance filtering (prompt layer)

- Filter results clearly unrelated to the query (accessories, empty boxes, wanted posts, wrong model).
- If you filter, tell the user that keyword relevance filtering was applied.
- When unsure, keep the listing and note possible noise.

After compare, suggest the **evaluate** sub-skill for shortlisted URLs.
