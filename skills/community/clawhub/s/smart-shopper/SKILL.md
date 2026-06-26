---
name: smart-shopper
description: >
  Find and compare products across Amazon, Temu, SHEIN and local stores. Use when a user wants to:
  (1) Shop for products or find best deals, (2) Compare prices across platforms,
  (3) Find items locally or online, (4) Create shopping lists with buy links,
  (5) Filter by budget (low/mid/high or "$X"), brand, features, color.
  Supports dual-mode search (online + local stores). Integrates SkillPay.me at 0.001 USDT/call.
---

# Smart Shopper

Find & compare products across Amazon, Temu, SHEIN and local stores. 0.001 USDT/call.

## Commands

| Command | Script | Description |
|:---|:---|:---|
| **search** | `scripts/search.py` | Search products across platforms |
| **compare** | `scripts/compare.py` | Compare specific products side-by-side |
| **local** | `scripts/local_search.py` | Find products in nearby stores |
| **list** | `scripts/shopping_list.py` | Generate/manage shopping lists |
| **track** | `scripts/price_tracker.py` | Track prices over time + alerts (NEW) |
| **billing** | `scripts/billing.py` | SkillPay charge/balance/payment |

## Workflow

```
1. Billing:  python3 scripts/billing.py --charge --user-id <id>
2. Search:   python3 scripts/search.py --query "wireless earbuds" --budget mid
3. Compare:  python3 scripts/compare.py --query "iPhone 15 case" --platforms amazon,temu,shein
4. Local:    python3 scripts/local_search.py --query "coffee maker" --location "New York"
5. List:     python3 scripts/shopping_list.py --action add --item "earbuds" --url "..."
```

## Examples

```bash
# Search with budget
python3 scripts/search.py --query "running shoes" --budget low
python3 scripts/search.py --query "laptop stand" --budget "$30"

# Compare across platforms
python3 scripts/compare.py --query "USB-C hub" --platforms amazon,temu

# Filter by preferences
python3 scripts/search.py --query "backpack" --brand "Nike" --color "black"

# Local store search
python3 scripts/local_search.py --query "batteries" --location "Shanghai"

# Shopping list
python3 scripts/shopping_list.py --action show
python3 scripts/shopping_list.py --action add --item "earbuds" --price 25.99 --url "https://..."
python3 scripts/shopping_list.py --action export
```

## Config

| Env Var | Required | Description |
|:---|:---:|:---|
| `SKILLPAY_API_KEY` | Yes | SkillPay.me API key |

## References

See `references/platforms.md` for platform-specific search patterns.
