# Trade Compass

**Global landed cost calculator for traders shipping to the US** — combines live USITC tariffs (Section 232, 301, AD/CVD), real-time exchange rates (ECB, 18 currencies), ocean freight costs (25+ routes), regulatory compliance (UFLPA), and customs entry fees into a single per-unit cost. Supports 18+ origin countries.

---

## What It Does

Given a product HTS code, country of origin, and cost of goods, Tariff Watch returns:

- **Total landed cost per unit** — the one number every trader needs
- **MFN base rate** — from live USITC data (auto-refreshed, 1-hour cache)
- **Section 232/301 surcharges** — steel/aluminum +25%/+10%, China trade-war duties
- **AD/CVD warning** — anti-dumping orders with worst-case rates
- **Exchange rate impact** — 18 currencies, 30-day trends, COG impact calculator
- **Ocean freight costs** — 25+ routes, FCL/LCL pricing, 30-day rate history
- **Compliance flags** — CPSC, FDA, FCC, EPA, DOT certification requirements
- **UFLPA risk** — forced-labor detention risk assessment
- **Customs entry costs** — broker, ISF, bond, MPF, HMF (amortized per unit)
- **Advisory notices** — Section 122 temporary surcharge and other pending actions

---

## Backend Setup

The skill requires a local FastAPI backend running on `http://localhost:8000`.

**Source code:** [github.com/zhaoningliu1-lang/tariff-watch](https://github.com/zhaoningliu1-lang/tariff-watch)

### 1. Install

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Start the API

```bash
uvicorn tariff_watch.api:app --reload --port 8000
```

The API connects to USITC on first request and caches the full HTS table in memory for 1 hour. No database required for live lookups.

### 3. Verify

```bash
curl http://localhost:8000/health
# → {"status": "ok", "version": "3.2.0"}
```

---

## Example Queries

### Effective tariff for Chinese aluminum profiles

```bash
curl "http://localhost:8000/tariff/7604101000/effective?origin=CN"
```

```json
{
  "origin": "CN",
  "origin_display": "China",
  "hts_code": "7604101000",
  "base_mfn_pct": 5.0,
  "section_232_pct": 10.0,
  "section_301_pct": 25.0,
  "total_additional_pct": 35.0,
  "effective_total_pct": 40.0,
  "adcvd": {
    "estimated_additional_pct": 32.79,
    "risk_level": "moderate",
    "matching_orders_count": 1,
    "worst_case_total_pct": 72.79,
    "warning": "AD/CVD duties could add +32.8% on top of all other duties..."
  },
  "compliance_flags": ["UL / NRTL"],
  "notes": ["..."],
  "advisory": ["Section 122 ..."]
}
```

### AD/CVD order check

```bash
curl "http://localhost:8000/adcvd/7604101000?origin=CN"
```

### Compliance report for toys

```bash
curl "http://localhost:8000/compliance/9503000013?origin=CN"
```

### Customs entry costs

```bash
curl "http://localhost:8000/compliance/entry-costs?origin=CN&estimated_value_usd=10000"
```

### Profit with customs costs + AD/CVD

```bash
curl "http://localhost:8000/amazon/profit/B08Y8NXGKJ?origin=CN&include_adcvd=true"
```

### Full landed cost (the key endpoint)

```bash
curl "http://localhost:8000/landed-cost?hts_code=7604101000&origin=CN&cog_local=32&units=500&cbm=5&destination=USWC"
```

Returns tariff + FX conversion + shipping + customs = total per-unit landed cost in USD.

### Exchange rate check

```bash
# Current rate + 30-day trend
curl "http://localhost:8000/fx/CNY"

# FX impact on your costs
curl "http://localhost:8000/fx/CNY/impact?cog_local=32&units=500"
```

### Shipping rates

```bash
# Current rates China → US West Coast
curl "http://localhost:8000/shipping/CN?destination=USWC"

# Per-unit shipping cost estimate
curl "http://localhost:8000/shipping/CN/cost?destination=USWC&cbm=5&units=500"
```

### Compare origins for the same product

```bash
# China
curl "http://localhost:8000/tariff/7604101000/effective?origin=CN"
# → effective_total_pct: 40.0% (worst case with AD/CVD: 72.79%)

# Vietnam
curl "http://localhost:8000/tariff/7604101000/effective?origin=VN"
# → effective_total_pct: 15.0%  (MFN 5% + S232 aluminum 10%, no S301, no AD/CVD)

# Mexico (USMCA)
curl "http://localhost:8000/tariff/7604101000/effective?origin=MX"
# → effective_total_pct: 5.0%   (MFN only, S232 waived)
```

### Supported origin codes

| Code | Country | Currency | Notes |
|---|---|---|---|
| `CN` | China | CNY | S301 + S232 + AD/CVD where applicable |
| `VN` | Vietnam | VND | S232 only |
| `IN` | India | INR | S232 only |
| `BD` | Bangladesh | BDT | S232 only |
| `TH` | Thailand | THB | S232 only |
| `ID` | Indonesia | IDR | S232 only |
| `MY` | Malaysia | MYR | S232 only |
| `PH` | Philippines | PHP | S232 only |
| `PK` | Pakistan | PKR | S232 only |
| `KR` | South Korea | KRW | S232 only |
| `JP` | Japan | JPY | S232 only |
| `TW` | Taiwan | TWD | S232 only |
| `DE` | Germany | EUR | S232 only |
| `GB` | United Kingdom | GBP | S232 only |
| `BR` | Brazil | BRL | S232 only |
| `TR` | Turkey | TRY | S232 only |
| `MX` | Mexico | MXN | USMCA — S232 waived |
| `CA` | Canada | CAD | USMCA — S232 waived |

Also accepts ISO-3 codes (`CHN`, `VNM`) and common English names (`China`, `Vietnam`).

---

## Current Tariff Status (as of 2026-02-26)

| Tariff | Status | Rate |
|---|---|---|
| Section 301 (Lists 1–4A) | **In effect** | +25% on most Chinese goods |
| Section 301 (List 4B) | **In effect** | +7.5% on Chinese apparel/footwear |
| Section 232 — Aluminum | **In effect** | +10% all origins except USMCA |
| Section 232 — Steel | **In effect** | +25% all origins except USMCA |
| AD/CVD orders | **In effect** | Company-specific; "all others" rates 32–295% |
| IEEPA reciprocal tariffs | **Struck down** | SCOTUS 2026-02-20; CBP stopped collecting 2026-02-24 |
| IEEPA fentanyl tariff on China | **Struck down** | Same ruling |
| Section 122 global surcharge | **In effect (advisory)** | +10% all origins; expires 2026-07-24; excluded from calculated total |

---

## API Reference

### Tariff & Trade

| Endpoint | Description |
|---|---|
| `GET /tariff/{hts_code}/effective?origin=CN` | Full effective tariff with per-layer breakdown + AD/CVD + compliance |
| `GET /live/tariff/{hts_code}` | Raw USITC MFN rate only |
| `GET /tariff/{hts_code}/history` | Weekly snapshot history |
| `GET /changes?since=YYYY-MM-DD&hts=XXXX` | Detected rate changes |
| `GET /notices?limit=20` | Federal Register tariff notices |
| `GET /tariff/news` | Trade policy news feed |
| `GET /adcvd/{hts_code}?origin=CN` | AD/CVD order matching and risk |
| `GET /adcvd/orders?origin=CN&chapter=76` | All active AD/CVD orders |
| `GET /compliance/{hts_code}?origin=CN` | Full compliance report (regulatory + UFLPA + marking) |
| `GET /compliance/entry-costs?origin=CN&estimated_value_usd=5000` | Customs entry cost breakdown |

### Exchange Rates

| Endpoint | Description |
|---|---|
| `GET /fx/rates` | All 18 tracked currencies with 30-day trends |
| `GET /fx/{currency}` | Single currency rate + trend (e.g. `/fx/CNY`) |
| `GET /fx/{currency}/history` | 30-day daily FX history |
| `GET /fx/{currency}/impact?cog_local=32&units=500` | FX impact on cost of goods |

### Ocean Freight

| Endpoint | Description |
|---|---|
| `GET /shipping/routes?origin=CN` | All shipping routes with current rates |
| `GET /shipping/{origin}?destination=USWC` | Rates for a specific origin → destination |
| `GET /shipping/{origin}/history` | 30-day freight rate history |
| `GET /shipping/{origin}/cost?cbm=2.5&units=500` | Per-unit shipping cost (LCL + FCL options) |

### Landed Cost & Profit

| Endpoint | Description |
|---|---|
| `GET /landed-cost?hts_code=...&origin=CN&cog_local=32&units=500&cbm=5` | **Comprehensive landed cost** — tariff + FX + shipping + customs in one call |
| `GET /amazon/profit/{asin}?origin=CN&include_adcvd=true` | Profit breakdown: COG + shipping + tariff + customs + FBA + referral |
| `GET /data-sources` | Show active data sources, last refresh times, and ECB coverage gaps |
| `GET /health` | Health check |

Interactive docs: `http://localhost:8000/docs`

---

## Data Sources & Auto-Refresh

### Sources

- **USITC HTS Schedule** — [hts.usitc.gov](https://hts.usitc.gov/) — official US tariff rates, auto-refreshed weekly
- **ECB Exchange Rates** — [frankfurter.app](https://www.frankfurter.app/) — 14 currencies, auto-refreshed daily (free, no key)
- **Federal Register** — tariff-related notices and USTR announcements
- **AD/CVD orders** — [Commerce Dept. ITA](https://enforcement.trade.gov/antidumping/antidumping.html)
- **UFLPA** — [CBP UFLPA Entity List](https://www.cbp.gov/trade/forced-labor/UFLPA)
- **Shipping** — calibrated simulation based on FBX index levels (or real Freightos data with API key)

### Auto-Refresh Schedule

| Data | Frequency | Source |
|---|---|---|
| Exchange rates | Daily | ECB (free) or exchangerate-api.com (optional) |
| Shipping rates | Daily | Simulated or Freightos API (optional) |
| USITC tariffs | Weekly (Monday) | USITC live |

First startup automatically backfills 30 days of FX + shipping history into SQLite.

### Optional Premium APIs

For more accurate data, you can register for paid APIs. The skill automatically detects and uses them — no code changes needed:

| Env Variable | Provider | Free Tier | What It Unlocks |
|---|---|---|---|
| `EXCHANGERATE_API_KEY` | [exchangerate-api.com](https://www.exchangerate-api.com/) | 1,500 calls/month | Real rates for VND, BDT, PKR, TWD |
| `FREIGHTOS_API_KEY` | [Freightos](https://www.freightos.com/api/) | Paid only | Real container shipping rates |
| `TARIFF_WATCH_DATA_DIR` | — | — | Custom SQLite data path (default: `~/.tariff-watch/`) |

Without any API keys, the skill works fully using free ECB data + calibrated shipping simulation.

### ECB Currency Gap

ECB does not cover: **VND, BDT, PKR, TWD**. These use calibrated simulation (marked `source: "simulated"`). Set `EXCHANGERATE_API_KEY` for full 18-currency coverage.

---

## Disclaimer

For informational purposes only. Tariff rates are subject to change and may differ based on product classification, country of origin documentation, and CBP determinations. AD/CVD rates are company-specific — the "all others" rate is a worst case. Always verify import duty obligations with a licensed customs broker or qualified trade counsel before making business decisions.
