---
name: seller-profit-calculator
description: Multi-platform Order Profit Calculator — upload order exports from any e-commerce platform or ERP, get instant profit reports by order, store, SKU, and platform.
display_name: Seller Profit Calculator
version: 1.0.0
author: YKGlobal
tags: [ecommerce, profit-calculation, orders, temu, shein, allegro, tiktok-shop, amazon, shopee, ozon, walmart, ebay, china]
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
  "交易收入": "buyer_total_paid",
  "采购金额": "cost_of_goods",
  "利润": "net_profit",
  "店铺": "store_name",
  "站点": "country"
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
python3 scripts/parse_orders.py orders.xlsx --field-map '{"交易收入":"buyer_paid","采购金额":"item_cost"}'

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
| Temu 半托管 | ERP / Platform backend | ✅ Verified |
| TikTok Shop | ERP / Platform backend | ✅ Verified |
| SHEIN | ERP / Platform backend | ✅ Verified |
| Fruugo | ERP / Platform backend | ✅ Verified |
| Amazon | ERP / Platform backend | ✅ Compatible |
| Shopee / Lazada | ERP / Platform backend | ✅ Compatible |
| Ozon | ERP / Platform backend | ✅ Compatible |
| Walmart | ERP / Platform backend | ✅ Compatible |
| eBay | ERP / Platform backend | ✅ Compatible |
| 其他平台 | ERP / Platform backend | ✅ Generic |

**Field mapping is automatic.** 只要导出文件包含以下标准字段就能计算：订单编号、交易收入、采购成本、运费、利润。

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

Upload your order export Excel file from **any platform or ERP** — 妙手ERP, 千牛, 店小秘, Allegro后台, Temu后台, 亚马逊卖家中心, etc.
Supported extensions: `.xlsx`, `.xls`.

### Output

**Markdown report** printed to stdout:

```
📊 订单利润分析报告

## 📋 整体概况
| 指标 | 数值 |
|------|------|
| 总订单 | 21 |
| 平台总收入 | ¥14,145.40 |
| 平台总支出 | ¥576.66 |
| 订单总成本 | ¥12,554.53 |
| 计算净利润 | ¥1,014.21 |
| 净利率 | 7.2% |

## 🌍 按平台汇总
...

## 🔴 亏损最严重的5单
...

## 🟢 盈利最高的5单
...
```

---

## Calculation Logic

### Net Profit Formula

```
净利润 = 平台收入 - 平台支出 - 订单成本
```

### Platform Income (平台收入)
```
平台收入 = 交易收入 + 运费收入(绝对值) + 退款 + 其他平台补贴
```

### Platform Expense (平台支出)
```
平台支出 = 平台佣金 + 技术服务费 + 运费(平台侧)
         + 退款金额 + 违规扣款 + 关税 + VAT + 其他平台费用
```

### Order Cost (订单成本)
```
订单成本 = 采购成本 + 头程运费 + 尾程运费 + 包材费
         + 仓库操作费 + 广告成本 + 运营成本 + 其他成本
```

**Field mapping is automatic.** 字段名自动归一化，不管导出的是"买家实付金额"还是"交易收入"还是"order_amount"，都能正确识别。

---

## Pricing (参考)

| Tier | Price | Limits | Target |
|------|-------|--------|--------|
| Free | ¥0 | 10 orders/mo, 1 store | Trial |
| Basic | ¥9.9/mo | 200 orders/mo, 3 stores | Small sellers |
| Standard | ¥29/mo | 1000 orders/mo, unlimited stores | Medium sellers |
| Pro | ¥69/mo | Unlimited orders + SKU analysis | Active sellers |
| Enterprise | ¥149/mo | Unlimited + history + alerts | Teams |

**Note:** This Skill itself is free to install. The tiers above apply to the hosted API version (coming soon at yk-global.com).

---

## Validation


Validated against real order data from multiple platforms — per-order profit match rate 100%:

| Platform | Orders | Per-order Accuracy |
|----------|--------|-------------------|
| Allegro | 21 | ✅ Exact |
| Temu 半托管 | 28 | ✅ Exact (28/28) |

---

## FAQ

**Q: 我的平台不在列表里，能用吗？**
A: 能用。只要导出文件包含订单号、收入、成本字段就能计算。自动识别字段映射，不限制平台。

**Q: 支持 CSV 吗？**
A: 目前仅支持 Excel (.xlsx / .xls)。CSV 支持在 v2.0 计划中。

**Q: 利润计算为什么不等于平台后台的数字？**
A: 逐单计算时，字段透明则结果精确。汇总时某些平台会有额外费用（汇率差、内部结算调整），这类费用不在导出字段中，无法通过计算还原。此时本工具的价值在于：**精确定位哪一单亏、哪一单赚**，为运营决策提供数据依据。

**Q: 支持结算单（settlement report）吗？**
A: v2.0 计划支持。目前 v1.0 读取订单维度的利润数据。

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

## License

MIT — YKGlobal
