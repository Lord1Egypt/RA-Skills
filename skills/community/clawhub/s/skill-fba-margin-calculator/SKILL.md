# skill-fba-margin-calculator
Version: 1.0.0 | Owner: GitHub Ops | Created: 2026-03-09

## What It Does
Calculates Amazon UAE FBA fees, net margin, and DG risk for CJ Dropshipping product candidates. Ranks results by margin % and outputs a markdown report + JSON.

Extracted from the Tech1Mart FBA pilot selection workflow that ran 2026-03-08 and 2026-03-09.

## When to Use
- After running skill-dropshipping-sourcing (CJ product lookup)
- Before ordering samples — confirm margin viability
- When comparing multiple SKUs for Amazon UAE FBA launch

## Prerequisites
- Node.js (no npm installs required — stdlib only)
- CJ product data: SKU, price (USD), weight (grams), target AED price

## Usage

### Single product
```bash
node skills/skill-fba-margin-calculator/calc.js \
  --sku CJLE2170569 \
  --name "Ring Light Phone Stand" \
  --price 12.96 \
  --weight 400 \
  --target 129 \
  --shipping 4
```

### Batch (JSON file)
```bash
node skills/skill-fba-margin-calculator/calc.js \
  --input products.json \
  --output output/fba-report
```

### Stdin pipe
```bash
cat products.json | node skills/skill-fba-margin-calculator/calc.js
```

### With DG flag
```bash
node skills/skill-fba-margin-calculator/calc.js \
  --sku CJYS1240831 --price 12.72 --weight 150 --target 99 --dg
```

## Input JSON Format
```json
[
  {
    "sku": "CJLE2170569",
    "name": "Ring Light + Phone Stand",
    "cj_price_usd": 12.96,
    "weight_g": 400,
    "target_aed": 129,
    "shipping_usd": 4,
    "dg_risk": false,
    "referral_pct": 8
  }
]
```

Optional fields: `shipping_usd` (default 3.5), `dg_risk` (default false), `referral_pct` (default 8%).

## Output
- Ranked markdown table by margin %
- Detail breakdown per SKU (landed cost, FBA fee tier, referral fee, net margin)
- Verdicts: ✅ FBA-safe / 🟡 Marginal / ❌ Too thin / ⚠️ DG Risk (WooCommerce-only)
- `--output` flag: writes `.md` + `.json` files

## FBA Fee Tiers (Amazon UAE, Q1 2026 estimates)
| Size Class | Max Weight | Est. Fee |
|------------|-----------|----------|
| Small Standard | 150g | 10 AED |
| Standard S | 350g | 13.5 AED |
| Standard M | 700g | 16.5 AED |
| Standard L | 1kg | 20 AED |
| Large Standard | 2kg | 26 AED |
| Oversize | 2kg+ | 38 AED |

Plus: 8% referral fee (electronics) + ~0.75 AED/unit storage.

## Flags
| Flag | Description |
|------|-------------|
| `--input FILE` | JSON file with product array |
| `--output BASE` | Write BASE.md + BASE.json |
| `--exchange RATE` | USD→AED rate (default 3.67) |
| `--sku` | Single SKU mode (with --price, --weight, --target) |
| `--price USD` | CJ price in USD |
| `--weight GRAMS` | Product weight in grams |
| `--target AED` | Target sell price in AED |
| `--shipping USD` | CJ shipping cost in USD (default 3.5) |
| `--referral PCT` | Referral fee % (default 8) |
| `--dg` | Flag product as Dangerous Goods (recommends WooCommerce-only) |

## Notes
- FBA fees are estimates — verify final numbers via Amazon Seller Central FBA Revenue Calculator before ordering samples
- Exchange rate defaults to 3.67 (AED/USD peg) — adjust if needed
- DG risk applies to: Li-ion batteries, aerosols, liquids. Always check before sending to FBA.
- Minimum viable margin: >25% AND >30 AED net for FBA to be worthwhile
