---
name: trade-compass
description: "Global landed cost calculator for traders shipping to the US. Combines live USITC tariffs, Section 232/301/AD-CVD duties, real-time exchange rates (ECB), ocean freight costs, UFLPA compliance, and customs entry fees into a single per-unit cost. Supports 18+ origin countries."
license: MIT
metadata:
  author: zhaoningliu1-lang
  homepage: https://github.com/zhaoningliu1-lang/tariff-watch
  tags: tariff, customs, hts, trade, compliance, import, ecommerce, shipping, exchange-rate, landed-cost, freight, fx
  emoji: "🧭"
---

# SKILL: Trade Compass

> ClawHub Skill · v3.2.0 · Python 3.11+ · FastAPI backend required

## Overview

Trade Compass answers the question: **"What does it actually cost me to land this product in the US?"**

It combines **tariffs** (USITC base + Section 232/301 + AD/CVD), **exchange rates** (18 currencies with 30-day trends), **ocean freight** (25+ routes from global ports to US coasts), **compliance** (CPSC/FDA/FCC/UFLPA), and **customs costs** (broker, ISF, bond, MPF, HMF) into a single landed-cost-per-unit calculation.

Designed for **global traders from any country** shipping to the United States — not just China.

---

## Capabilities (v3.2)

| Feature | Description |
|---|---|
| **Live HTS lookup** | Fetches current MFN base rate directly from USITC (auto-discovers latest revision) |
| **Section 232 overlay** | Adds steel (+25%) or aluminum (+10%) surcharge for all non-USMCA origins |
| **Section 301 overlay** | China-specific: +25% (most goods) or +7.5% (apparel/footwear ch. 61–64) |
| **AD/CVD orders** | Checks 16+ active anti-dumping/countervailing duty orders against China; shows "all others" rate and risk level |
| **Live exchange rates** | 14 currencies from ECB (daily auto-refresh) + 4 simulated; optional premium API for all 18 |
| **Ocean freight rates** | 25+ routes from global ports to US West/East Coast, with FCL/LCL pricing and 30-day trends |
| **Landed cost calculator** | One-stop endpoint: tariff + FX + shipping + customs = total per-unit landed cost |
| **Auto-refresh scheduler** | APScheduler: FX daily, shipping daily, USITC weekly — data persisted in SQLite |
| **Compliance report** | Maps HTS chapter to regulatory agencies (CPSC, FDA, FCC, EPA, DOT) with certification requirements |
| **UFLPA risk assessment** | Flags cotton, polysilicon, tomato, aluminum, PVC products for CBP detention risk |
| **Customs entry costs** | Calculates broker fee, ISF filing, bond, MPF, HMF, and exam risk — amortized per unit |
| **Section 122 advisory** | Flags the temporary 10% global surcharge (in effect 2026-02-24, expires 2026-07-24) |
| **18+ origin countries** | CN, VN, IN, BD, TH, ID, MY, PH, PK, KR, JP, TW, DE, GB, MX, CA, BR, TR and more |
| **Profit calculator** | Full breakdown: COG + shipping + tariff + customs + FBA fee + referral fee |

---

## How Claude Uses This Skill

When invoked, Claude should:

1. **Identify the HTS code** from the user's product description.
   - Use Claude's built-in HTS knowledge to suggest the most specific 10-digit code.
   - If uncertain, start with a 4- or 6-digit prefix.

2. **Call the effective tariff endpoint:**
   ```
   GET http://localhost:8000/tariff/{hts_code}/effective?origin={ISO2}
   ```
   Default origin: `CN` (China). Accept natural-language origin ("Vietnam" → `VN`).

3. **Present the result clearly:**
   - List each duty layer (MFN base, Section 232, Section 301) with its rate and legal basis.
   - Show `effective_total_pct` as the confirmed total.
   - If `adcvd` is present, highlight the AD/CVD risk and worst-case total.
   - If `compliance_flags` is present, list the regulatory agencies.
   - Always display the `advisory` field if non-empty — the user needs to know about Section 122.
   - Remind the user to verify with a licensed customs broker.

4. **For full landed cost** (the most powerful endpoint), call:
   ```
   GET http://localhost:8000/landed-cost?hts_code={code}&origin={ISO2}&cog_local=32&units=500&cbm=5&destination=USWC
   ```
   This combines tariff + FX + shipping + customs into one response.

5. **For exchange rate impact**, call:
   ```
   GET http://localhost:8000/fx/{currency}/impact?cog_local=32&units=500
   ```

6. **For shipping rates**, call:
   ```
   GET http://localhost:8000/shipping/{origin}?destination=USWC
   ```

7. **For AD/CVD, compliance, or profit**, call the respective endpoints below.

---

## API Endpoints Reference

| Method | Path | Description |
|---|---|---|
| `GET` | `/landed-cost?hts_code=...&origin=CN&cog_local=32&units=500&cbm=5` | **Comprehensive landed cost** — tariff + FX + shipping + customs in one call |
| `GET` | `/tariff/{hts_code}/effective?origin=CN` | Effective tariff with per-layer breakdown + AD/CVD + compliance flags |
| `GET` | `/live/tariff/{hts_code}` | Raw USITC MFN rate only (no overlay) |
| `GET` | `/fx/rates` | All tracked exchange rates with 30-day trends |
| `GET` | `/fx/{currency}` | Single currency rate + trend |
| `GET` | `/fx/{currency}/history` | 30-day daily FX history |
| `GET` | `/fx/{currency}/impact?cog_local=32&units=500` | FX impact on cost of goods |
| `GET` | `/shipping/routes?origin=CN` | All shipping routes with current rates |
| `GET` | `/shipping/{origin}?destination=USWC` | Rates for a specific route |
| `GET` | `/shipping/{origin}/history` | 30-day freight rate history |
| `GET` | `/shipping/{origin}/cost?cbm=2.5&units=500` | Per-unit shipping cost (LCL/FCL) |
| `GET` | `/adcvd/{hts_code}?origin=CN` | AD/CVD order matching |
| `GET` | `/compliance/{hts_code}?origin=CN` | Compliance report (regulatory + UFLPA + marking) |
| `GET` | `/compliance/entry-costs?origin=CN&estimated_value_usd=5000` | Customs entry costs |
| `GET` | `/amazon/profit/{asin}?origin=CN&include_adcvd=true` | Amazon FBA profit with full tariff + customs |
| `GET` | `/data-sources` | Show active data sources and last refresh times |
| `GET` | `/health` | API health check |

---

## Data Sources & Auto-Refresh

| Data Type | Free Source | Refresh | Premium Source (optional) |
|---|---|---|---|
| **Tariff rates** | USITC live (always free) | Weekly (Monday) | — |
| **Exchange rates** | ECB via frankfurter.app (14 currencies) | Daily | exchangerate-api.com (all 18 currencies) |
| **Shipping rates** | Calibrated simulation (based on FBX index) | Daily | Freightos API (real container rates) |

### ECB Currency Gap

The free ECB feed does not cover: **VND, BDT, PKR, TWD**. These 4 currencies use calibrated simulation and are marked with `source: "simulated"` in the response. Set `EXCHANGERATE_API_KEY` to get real rates for all 18 currencies.

### Optional Premium API Keys

For more accurate data, users can register for paid APIs. The skill will automatically detect and use them:

| Env Variable | Provider | Free Tier | What It Unlocks |
|---|---|---|---|
| `EXCHANGERATE_API_KEY` | [exchangerate-api.com](https://www.exchangerate-api.com/) | 1,500 calls/month | Real rates for VND, BDT, PKR, TWD + sub-daily updates |
| `FREIGHTOS_API_KEY` | [Freightos](https://www.freightos.com/api/) | Paid only | Real container shipping rates from carriers |
| `TARIFF_WATCH_DATA_DIR` | — | — | Custom path for SQLite data (default: `~/.tariff-watch/`) |

Without any API keys, the skill works fully using free ECB data + calibrated simulation. No registration required.

### Data Refresh Schedule

- **FX rates**: Updated daily (after ECB publishes)
- **Shipping rates**: Updated daily (simulation or Freightos)
- **USITC tariffs**: Updated weekly (Monday)
- **First startup**: Automatically backfills 30 days of history

---

## Tariff Logic (Current as of 2026-02-26)

### Confirmed in-force duties

| Layer | Authority | Rate | Scope |
|---|---|---|---|
| MFN base | USITC HTS | Varies (0–6.5% typical) | All countries |
| Section 232 — Steel | Trade Expansion Act s.232 | +25% | All except USMCA (ch. 72–73) |
| Section 232 — Aluminum | Trade Expansion Act s.232 | +10% | All except USMCA (ch. 76) |
| Section 301 — Lists 1–4A | Trade Act of 1974 s.301 | +25% | China only (most goods) |
| Section 301 — List 4B | Trade Act of 1974 s.301 | +7.5% | China only (apparel/footwear ch. 61–64) |

### AD/CVD orders (company-specific — "all others" rate shown)

| Product | Case | All Others Rate |
|---|---|---|
| Aluminum Extrusions | A-570-967 / C-570-968 | 32.79% |
| Aluminum Foil | A-570-116 / C-570-117 | 48.64% |
| Steel Nails | A-570-900 / C-570-901 | 118.04% |
| Wooden Bedroom Furniture | A-570-847 | 198.08% |
| Quartz Surface Products | A-570-082 / C-570-083 | 294.57% |
| *… and 11 more orders* | | |

### Struck down — NOT applied

| Layer | Reason |
|---|---|
| IEEPA reciprocal tariffs | SCOTUS ruling 2026-02-20 (*Learning Resources v. Trump*) |
| IEEPA fentanyl tariff on China | Same ruling; CBP stopped collection 2026-02-24 |

### Advisory — shown but NOT added to calculated total

| Layer | Status |
|---|---|
| Section 122 +10% global surcharge (HTS 9903.03.01) | In effect 2026-02-24 to 2026-07-24; Congress must act to extend |

---

## Limitations & Disclaimer

- **Data source:** USITC publishes the official HTS schedule; this skill reads it directly. Rate data is as current as the latest USITC revision.
- **Section 122** is confirmed in effect but deliberately excluded from `effective_total_pct` due to its temporary, politically fluid nature — always check the `advisory` field.
- **AD/CVD rates** are company-specific. The "all others" rate shown is applied to exporters without an individual rate from a Commerce Dept. administrative review. Your actual rate may be lower.
- **Compliance data** covers major agencies but is not exhaustive. Some products have additional state-level or industry-specific requirements.
- **For informational purposes only.** Always verify tariff obligations with CBP binding rulings, a licensed customs broker, or qualified trade counsel before making import decisions.
