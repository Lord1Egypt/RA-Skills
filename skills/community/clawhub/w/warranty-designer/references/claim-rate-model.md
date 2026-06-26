# Claim Rate Model

A simple, defensible model for warranty claim rate, reserve, and unit-economics impact. Use a spreadsheet with one tab per SKU.

## Inputs you need

- Annual unit volume forecast.
- Average remedy cost (weighted across repair / replace / refund).
- Defect rate at month 0–3 (early failure).
- Steady-state defect rate after month 3.
- Warranty length in months.
- Failure curve shape: front-loaded, flat, or U-shaped (failures spike at end-of-life).

## Method

### Step 1 — Estimate cumulative claim rate

If you have prior data, fit a Weibull or simple piecewise model. If you don't, use this conservative starter:

```
Cumulative claim rate over warranty term ≈
  early_defect_rate (months 0–3)
+ steady_state_rate × (warranty_length_months − 3) / 12
```

Example: early defect 1.2%, steady-state 0.4%/yr, 24-month warranty:

```
1.2% + 0.4% × (24 − 3) / 12 = 1.2% + 0.7% = 1.9% cumulative claim rate
```

### Step 2 — Average remedy cost

```
avg_remedy = (P_repair × cost_repair)
           + (P_replace × cost_replace)
           + (P_refund × selling_price)
```

Where P_x are the conditional probabilities given a valid claim. For most products, P_repair ≈ 0.55, P_replace ≈ 0.40, P_refund ≈ 0.05.

### Step 3 — Annual warranty cost

```
Annual warranty cost = Annual units × cumulative_claim_rate × avg_remedy
```

### Step 4 — Reserve

Set initial reserve at 1.5× the annual warranty cost. Review quarterly. If actual claims are within ±10%, reserve is right. Outside that band, adjust.

### Step 5 — Per-unit warranty cost

```
per_unit_warranty_cost = annual_warranty_cost / annual_units
```

Bake this into your unit economics. If it changes the gross margin by more than 1 percentage point, the warranty is materially priced into your COGS.

## Worked example — apparel brand, $80 hoodie

- Annual volume: 50,000 units.
- Early defect rate: 0.8% (stitching, dye lots).
- Steady-state rate: 0.2%/yr (wear).
- Warranty length: 12 months.
- avg_remedy: $32 (mostly replace from B-stock at COGS, some refunds).

```
Cumulative claim rate = 0.8% + 0.2% × (12 − 3) / 12 = 0.8% + 0.15% = 0.95%
Annual warranty cost = 50,000 × 0.95% × $32 = $15,200
Reserve = 1.5 × $15,200 = $22,800
Per-unit warranty cost = $15,200 / 50,000 = $0.30
```

A 30 cent per-unit cost on an $80 hoodie is trivial — this warranty is well-designed.

## Worked example — $400 electronics device

- Annual volume: 20,000 units.
- Early defect rate: 2.5%.
- Steady-state rate: 1.2%/yr.
- Warranty length: 24 months.
- avg_remedy: $180 (mostly replace from new, refurb pipeline still ramping).

```
Cumulative claim rate = 2.5% + 1.2% × (24 − 3) / 12 = 2.5% + 2.1% = 4.6%
Annual warranty cost = 20,000 × 4.6% × $180 = $165,600
Reserve = 1.5 × $165,600 = $248,400
Per-unit warranty cost = $165,600 / 20,000 = $8.28
```

$8.28 per unit is meaningful — that's about 2% of selling price. Two levers help: lower the avg_remedy (refurb pipeline), or shorten the warranty.

## When to redesign the warranty

- Actual claim rate >1.3× model: investigate the failure mode and consider tightening exclusions or fixing the product.
- Average remedy cost rising: refurb pipeline is broken, or B-stock is depleting faster than refurbs come in.
- Concentration of claims in one batch: not a warranty problem; it's a quality problem. Run a batch recall.
- Customer NPS driven by claims experience (positive or negative): warranty is a marketing input — feed insights to product and brand teams.
