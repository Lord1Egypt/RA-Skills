---
name: seller-profit-calculator
description: Multi-platform Order Profit Calculator — upload order exports from any e-commerce platform or ERP, get instant profit reports by order, store, SKU, and platform.
display_name: Seller Profit Calculator
version: 1.0.0
author: YKGlobal
tags: [ecommerce, profit-calculation, orders, temu, shein, allegro, tiktok-shop, amazon, shopee, ozon, walmart, ebay]
---

# Seller Profit Calculator

Upload order exports from **any e-commerce platform or ERP** → get instant profit breakdown by order, store, SKU, and platform.

![Profit Report](https://img.shields.io/badge/profit-report-green)
![All Platforms](https://img.shields.io/badge/-All%20Platforms-blue)
![Auto-detect](https://img.shields.io/badge/-Auto--detect-orange)

## What It Does

**Upload one Excel file → get a complete profit breakdown:**

- 📋 **Overall summary**: total orders, completed, cancelled, total revenue, total cost, net profit, net margin %
- 🌍 **By platform**: revenue / expense / cost / profit per platform
- 🏪 **By store**: revenue / expense / cost / profit per store
- 🔴 **Bottom 5 orders**: worst loss-making orders highlighted
- 🟢 **Top 5 orders**: best performing orders highlighted
- ✅ **Cross-check**: calculated profit vs platform-declared profit — validates accuracy per order

---

## How It Works — Agent-Powered Field Mapping

This Skill is not a static field-mapping tool. The AI Agent handles the messy reality of real export files.

### The Workflow

```
You upload any Excel order export
        ↓
Agent reads headers + sample rows (analyze_headers.py)
        ↓
Agent identifies each column's meaning (LLM reasoning)
        ↓
Agent builds field_map JSON → passes to parse_orders.py
        ↓
parse_orders.py calculates with full field context
        ↓
Report with per-order breakdown + accuracy notes
```

### Field Map Example

```json
{
  "buyer_total_paid": "buyer_total_paid",
  "cost_of_goods": "cost_of_goods",
  "net_profit": "net_profit",
  "store_name": "store_name",
  "country": "country"
}
```

### What the Agent Does

1. **Auto-detects standard fields** — 38 standard field names recognized across Allegro, Temu, TikTok, Amazon, etc.
2. **Semantic matching for unknown columns** — if a column isn't in the standard list, the Agent infers its meaning from the column name + sample values
3. **Handles missing fields** — if a required field is absent, the Agent notes it and estimates impact
4. **Produces field_map JSON** — passed directly to the parser via `--field-map`

### CLI Usage

```bash
# Auto-detect (works if column names match standard fields)
python3 scripts/parse_orders.py orders.xlsx

# With Agent-provided field mapping
python3 scripts/parse_orders.py orders.xlsx --field-map '{"buyer_paid":"buyer_paid","item_cost":"item_cost"}'

# Or load from file
python3 scripts/parse_orders.py orders.xlsx --field-map @my_mapping.json

# Analyze file headers first (for Agent to inspect)
python3 scripts/analyze_headers.py orders.xlsx --json headers.json
```

---

## Supported Platforms

All e-commerce platforms and ERPs that export order data with standard fields: order ID, revenue, costs, profit.

| Platform | Export Source | Status |
|----------|-------------|--------|
| Allegro | ERP / Platform backend | ✅ Verified |
| Temu | ERP / Platform backend | ✅ Verified |
| TikTok Shop | ERP / Platform backend | ✅ Verified |
| SHEIN | ERP / Platform backend | ✅ Verified |
| Fruugo | ERP / Platform backend | ✅ Verified |
| Amazon | ERP / Platform backend | ✅ Compatible |
| Shopee / Lazada | ERP / Platform backend | ✅ Compatible |
| Ozon | ERP / Platform backend | ✅ Compatible |
| Walmart | ERP / Platform backend | ✅ Compatible |
| eBay | ERP / Platform backend | ✅ Compatible |
| Others | ERP / Platform backend | ✅ Generic |

**Field mapping is automatic.** Works as long as the export contains standard fields: order ID, revenue, cost, profit.

---

## Installation

```bash
openclaw skill install seller-profit-calculator
```

Or use the ClawHub import URL:
```
https://clawhub.ai/import
```

---

## Usage

### Quick Start

```bash
# Auto-detects format — works with any platform's export
python scripts/parse_orders.py orders.xlsx

# Output JSON for further processing
python scripts/parse_orders.py orders.xlsx --json result.json
```

### Input

Upload your order export Excel file from **any platform or ERP**.
Supported extensions: `.xlsx`, `.xls`.

### Output

**Markdown report** printed to stdout:

```
📊 Order Profit Analysis Report

## 📋 Overall Summary
| Metric | Value |
|--------|-------|
| Total Orders | 21 |
| Platform Revenue | ¥14,145.40 |
| Platform Expense | ¥576.66 |
| Order Cost | ¥12,554.53 |
| Net Profit | ¥1,014.21 |
| Net Margin | 7.2% |

## 🌍 By Platform
...

## 🔴 Bottom 5 Orders (Worst Loss)
...

## 🟢 Top 5 Orders (Best Profit)
...
```

---

## Calculation Logic

### Net Profit Formula

```
Net Profit = Platform Revenue - Platform Expense - Order Cost
```

### Platform Income
```
Platform Income = Buyer Paid + Shipping Income (absolute) + Refund + Other Platform Subsidies
```

### Platform Expense
```
Platform Expense = Platform Commission + Tech Service Fee + Shipping (platform side)
                 + Refund Amount + Penalty Deductions + Customs + VAT + Other Platform Fees
```

### Order Cost
```
Order Cost = Cost of Goods + First-leg Freight + Last-mile Freight + Packaging
           + Warehouse Handling + Advertising Cost + Operating Cost + Other Costs
```

---

## Pricing

| Tier | Price | Order Limit | Store Limit | Features |
|------|-------|------------|-------------|----------|
| Free | ¥0 | 10/mo | 1 | Basic profit calculation |
| Basic | ¥9.9/mo | 200/mo | 3 | Full features + report export |
| Standard | ¥29/mo | 1000/mo | Unlimited | SKU analysis + trend charts |
| Pro | ¥69/mo | Unlimited | Unlimited | Unlimited + SKU analysis + alerts |
| Enterprise | ¥149/mo | Unlimited | Unlimited | Unlimited + history + team |

**Note:** This Skill is free to install. Paid tiers apply to the hosted API version at yk-global.com.

---

## Validation

Validated against real order data from multiple platforms — per-order profit match rate 100%:

| Platform | Orders | Per-order Accuracy |
|----------|--------|-------------------|
| Allegro | 21 | ✅ Exact |
| Temu | 28 | ✅ Exact (28/28) |

---

## FAQ

**Q: My platform is not on the list. Will it work?**
A: Yes. As long as your export contains order ID, revenue, and cost fields, it will calculate. Automatic field mapping works regardless of platform.

**Q: Does it support CSV?**
A: Currently only Excel (.xlsx / .xls). CSV support is planned for v2.0.

**Q: Why doesn't the calculated profit match the platform dashboard?**
A: Per-order calculation is exact when fields are transparent. For summaries, some platforms have additional fees (FX differences, internal settlement adjustments) not present in the export. The value of this tool is: **precisely identifying which orders lose money and which make money**, providing data-driven operational decisions.

**Q: Does it support settlement reports?**
A: Settlement report support is planned for v2.0. Currently v1.0 reads order-level profit data.

---

## File Structure

```
seller-profit-calculator/
├── SKILL.md               ← This file
├── README.md              ← User-facing documentation
└── scripts/
    ├── parse_orders.py    ← Core parser (supports --field-map)
    └── analyze_headers.py ← Header + sample analyzer for Agent use
```

---

> For paid plans, visit [YK-Global.com](https://yk-global.com)
