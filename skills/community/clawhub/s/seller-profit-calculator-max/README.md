# Multi-platform Order Profit Calculator

Upload order exports from **any e-commerce platform or ERP** — automatically calculate net profit per order. Supports TikTok Shop, Allegro, Temu, Amazon, SHEIN, Fruugo, Shopee, Ozon, and all other major platforms.

## Version & Pricing

| Version | Price | Order Limit | Store Limit | Features |
|---------|-------|:-----------:|:-----------:|----------|
| **Free** | ¥0 | 20/mo | 1 | Basic profit calculation |
| **Standard** | ¥9.9/mo | 500/mo | 3 | Full features + report export |
| **Pro** | ¥29/mo | Unlimited | Unlimited | SKU analysis + trend charts |
| **Team** | ¥99/mo | Unlimited | Unlimited | History + multi-user |

### Upgrade to Pro

Visit [https://yk-global.com](https://yk-global.com) to purchase, then configure your API Key:

```bash
export PROFIT_API_KEY=your_api_key
python3 scripts/parse_orders.py orders.xlsx --api
```

---

## Quick Start

```bash
# Local run (Free tier) — auto-detects any platform format
python3 scripts/parse_orders.py orders.xlsx

# Output JSON format
python3 scripts/parse_orders.py orders.xlsx --json result.json
```

**Supported import sources:**
- ERP exports: MiaoshouERP, Qianniu, Dianxiaomi, etc.
- Platform backends: Allegro, Temu, Amazon, TikTok Shop, etc.
- Any Excel file containing order ID, revenue, and cost fields

---

## Supported Platforms

| Platform | Status | Notes |
|----------|:------:|-------|
| TikTok Shop | ✅ | ERP or platform backend export |
| Allegro | ✅ | ERP or platform backend export |
| Temu | ✅ | ERP or platform backend export |
| SHEIN | ✅ | ERP or platform backend export |
| Fruugo | ✅ | ERP or platform backend export |
| Amazon | ✅ | Platform backend export |
| Shopee / Lazada | ✅ | Platform backend export |
| Ozon | ✅ | Platform backend export |
| Walmart / eBay | ✅ | Platform backend export |
| Other platforms | ✅ | Generic auto field detection |

> **Field mapping is automatic.** Not limited to any specific platform. As long as the export contains standard order fields.

---

## Calculation Logic

**Net Profit = Platform Revenue - Platform Expense - Order Cost**

| Module | Description |
|--------|-------------|
| **Platform Revenue** | Buyer paid + shipping income + refund + platform subsidies |
| **Platform Expense** | Commission + tech fee + shipping + refund + penalties + tax |
| **Order Cost** | Cost of goods + first-leg freight + last-mile freight + packaging + warehouse handling + advertising |

---

## Dependencies

- Python 3.8+
- openpyxl (`pip install openpyxl`)

---

## Official Site & Support

- Website: [https://yk-global.com](https://yk-global.com)
- Support: Contact customer service

---

> The free tier is completely free with no time limit. Paid tiers provide hosted API and advanced analytics.
