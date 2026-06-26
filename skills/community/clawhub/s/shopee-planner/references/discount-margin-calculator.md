# Discount & Margin Calculator

Reference formulas and worked examples for Shopee campaign pricing decisions.

---

## Core Formulas

### 1. Floor Price (Minimum Viable Price)

```
Floor Price = (Unit Cost + Shopee Commission + Payment Fee + Shipping Subsidy) × (1 + Minimum Margin %)
```

**Shopee fee components** (approximate — verify in your Seller Centre):
- Transaction/Commission fee: 1–5% of selling price (varies by category and Preferred Seller status)
- Payment processing fee: ~2% of selling price
- Shipping subsidy (if offering free shipping): varies by weight and distance; typical range SGD 1.50–4.00 or MYR 3–8 per order

**Worked example (Malaysia)**:
- Unit cost (COGS): MYR 28
- Shopee commission (2.5%): MYR 2.50 on MYR 100 normal price
- Payment fee (2%): MYR 2.00
- Shipping subsidy: MYR 5.00
- Total fulfillment cost: MYR 37.50
- Target minimum margin: 10%
- Floor Price = MYR 37.50 × 1.10 = **MYR 41.25**

Any Flash Sale or voucher price set below MYR 41.25 loses money.

---

### 2. Gross Margin at Discounted Price

```
Gross Margin % = ((Discounted Price - Unit Cost - Shopee Fees - Shipping) / Discounted Price) × 100
```

**Worked example**:
- Normal price: MYR 89
- Flash Sale price (20% off): MYR 71.20
- Unit cost: MYR 28
- Shopee fees (4.5% of sale price): MYR 3.20
- Shipping subsidy: MYR 5.00
- Total cost: MYR 36.20
- Gross Margin = (MYR 71.20 − MYR 36.20) / MYR 71.20 = **49.2%**  ✅ Healthy

---

### 3. Voucher Cost Calculation

```
Total Voucher Cost = Discount Amount × Expected Redemptions
Expected Redemptions = Issuance Cap × Redemption Rate %
```

**Worked example**:
- Voucher: MYR 8 off, min spend MYR 60
- Issuance cap: 300 vouchers
- Expected redemption rate: 25%
- Expected redemptions: 75
- Total voucher cost: 75 × MYR 8 = **MYR 600**

Add this to your campaign budget. Ensure the incremental orders generated cover the voucher cost via contribution margin.

**Break-even redemption check**:
```
Break-even Orders = Voucher Cost / (AOV × Gross Margin %)
Break-even Orders = MYR 600 / (MYR 89 × 45%) = 600 / 40.05 = ~15 incremental orders
```
If vouchers drive ≥15 orders above your baseline, the campaign is profitable.

---

### 4. Coins Cashback Subsidy Cost

```
Coins Subsidy = Selling Price × Coins Rate % × Units Sold
```

**Note**: Shopee coins are issued 1:1 with MYR/SGD (1 coin = MYR 0.01 / SGD 0.01). The cost is debited from your Shopee Seller wallet.

**Worked example**:
- Product price: MYR 65
- Coins rate: 7%
- Expected units sold (coins period): 40
- Coins subsidy cost = MYR 65 × 7% × 40 = **MYR 182**

Ensure your gross margin on those 40 units covers MYR 182:
- Gross margin per unit: MYR 65 × 42% = MYR 27.30
- Total margin: 40 × MYR 27.30 = MYR 1,092
- Net profit after coins: MYR 1,092 − MYR 182 = **MYR 910** ✅

---

### 5. Return on Ad Spend (ROAS) for Campaign

```
Campaign ROAS = Campaign GMV / Total Campaign Spend
Total Campaign Spend = Voucher Cost + Coins Subsidy + Any Shopee Ads Spend
```

**Target benchmarks**:
- ROAS ≥ 5× for Flash Sale periods (high-traffic events)
- ROAS ≥ 3× for evergreen voucher campaigns
- ROAS ≥ 4× for Coins Cashback SKUs

**Worked example**:
- Flash Sale GMV: MYR 8,400
- Voucher cost: MYR 600
- Coins subsidy: MYR 182
- Shopee Ads: MYR 300
- Total spend: MYR 1,082
- ROAS = MYR 8,400 / MYR 1,082 = **7.8×** ✅ Excellent

---

### 6. Optimal Voucher Minimum Spend

```
Optimal Min Spend = Current AOV × Multiplier
```

Multiplier guidelines:
- Store-wide acquisition voucher: 1.5–2.0× AOV
- Follower/loyalty retention voucher: 1.2–1.5× AOV
- Bundle upsell voucher: 1.8–2.5× AOV

**Worked example**:
- AOV = MYR 55
- Store-wide event voucher target min spend = MYR 55 × 1.6 = **MYR 88**
- Rounds to MYR 90 (clean number, psychologically easier to hit)

---

## Quick Reference Table — Shopee MY Fee Estimates by Category

| Category | Approx. Commission Rate |
|----------|------------------------|
| Electronics & Gadgets | 2.0–3.0% |
| Fashion & Apparel | 3.0–4.5% |
| Health & Beauty | 3.0–4.0% |
| Home & Living | 2.5–3.5% |
| Sports & Outdoors | 3.0–4.0% |
| Food & Beverages | 2.5–3.5% |
| Baby & Toys | 3.0–4.0% |

> **Important**: Always verify current commission rates in your Seller Centre → Account Health → Commission & Fees. Rates change periodically and vary by seller tier (Normal, Preferred, Mall).

---

## Margin Sanity Check Cheatsheet

Before any campaign, run this quick check:

| Check | Formula | Pass Threshold |
|-------|---------|----------------|
| Flash Sale floor price | COGS + Fees + Shipping × 1.05 | Sale price > floor price |
| Gross margin at sale price | (Sale price − total cost) / sale price | ≥ 20% minimum |
| Voucher break-even | Voucher cost / (AOV × margin%) | ≤ 15% of expected orders |
| Coins subsidy affordable? | Coins cost / total margin | ≤ 20% of gross margin |
| Blended campaign ROAS | Total GMV / total spend | ≥ 3× |
