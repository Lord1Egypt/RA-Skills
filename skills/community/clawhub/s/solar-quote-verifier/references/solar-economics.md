# Solar Quote Verifier — Reference

## 1. Regional insolation (peak sun-hours/day, annual average)

| Region (US-centric) | Sun-h/day | Examples |
|---|---|---|
| southwest | 6.0 | AZ, NV, inland SoCal, NM |
| west | 5.0 | coastal CA, CO high plains at 5.5 |
| midwest | 4.4 | KS, MO, IL, IN, OH |
| southeast | 4.8 | FL, GA, SC, TX east |
| northeast | 4.2 | NY, MA, NJ, PA, MI |
| northwest | 3.6 | WA, OR west of Cascades |
| alaska | 2.8 | worst-case US |
| hawaii | 5.5 | but very high rates |
| Override | any | --sun-hours 5.2 |

## 2. Production model

```
annual_kwh = kW_dc × sun_hours × 365 × derate
derate = 0.84  (soiling, wiring, inverter, temperature; 0.79 for hot
                climates/poor airflow, 0.87 for microinverters+breezy site)
orientation multiplier vs the table's south assumption:
  south 1.00 | southeast/southwest 0.96 | east or west 0.86 | north 0.60
pitch: 15-40° ≈ 1.00; flat ≈ 0.97 (with minor soiling loss)
```

If quoted_kwh exceeds the model by >10% → RED FLAG (overstated production,
the most common proposal lie, usually from ideal-condition PVWatts runs).

## 3. $/W market bands (residential, US, pre-ITC, mid-2020s)

| $/W DC | Verdict |
|---|---|
| ≤ 2.50 | exceptional (verify equipment quality/warranty) |
| 2.50–3.50 | FAIR market range |
| 3.50–4.00 | OVERPRICED — negotiate or bid against |
| > 4.00 | walk away unless special conditions |

Notes: small systems (<6 kW) carry higher $/W; Tesla-style standardized
installs historically undercut; two-story/steep roofs add 5–15%.

## 4. Honest payback math

```
net_cost = price × (1 - itc)          # 0.30 if eligible, else 0
year-1 value = production × utility_rate
escalate rate 2.5%/yr; degrade production 0.5%/yr
inverter replacement: year 13, $0.35/W (string) — add if term ≥ 13 yr
payback = first year cumulative net value ≥ net_cost
```

25-yr net savings = cumulative value − net_cost − inverter − O&M
($150/yr suggested: monitoring, cleaning, minor repairs).

Utility rate escalation matters as much as sun: 2.5% is the long-term US
average; some states (CA NEM 3.0 export rates) broke the old math — if your
net-metering pays wholesale for exports, self-consumption fraction (often
only 30–40%) must multiply the value, not 100%.

## 5. Financing traps

- **Dealer-fee loans:** "low APR" loans embed a 10–15% dealer fee in the
  price. Test: ask for the cash price; if loan price > cash price by >5%,
  you're paying the fee.
- **Lease/PPA escalator:** typical 2.9%/yr. If utility escalation is 2.5%,
  the gap compounds: year-20 PPA rate ≈ initial × 1.029^20 = 1.77× vs
  utility × 1.025^20 = 1.64× — savings inverted around year 12–18.
- **Lease/PPA and selling the house:** lease transfer to buyer requires
  credit approval (deals fall through) or a buyout at inflated residual.
- **ITC ownership:** lease/PPA company takes the 30% credit; "we handle all
  the paperwork" means "we take the incentives."

## 6. Roof and structure

- Asphalt shingle: 20–25 yr life. Panels warranted 25 yr. Reroof BEFORE
  installing if shingle is >10 yr old, or budget $2,000–6,000 for
  remove-and-reinstall later.
- Tile roofs: +$1–2/W install complexity.
- Ground mount: usually +$0.5–1/W but no roof conflict.

## 7. Sales-tactic fingerprint list

- "Your utility is raising rates 6%/yr" (US long-term average ≈ 2.5%)
- "Free panels" (lease)
- "Sign today for this price" (pressure; solar prices don't spike overnight)
- Production quoted without shade/azimuth derate
- Payback quoted on gross savings with no degradation, no inverter, no O&M
- Warranty described as "25 years" without separating product/performance/
  workmanship (workmanship is often 5–10 yr)

## 8. Questions that expose a bad quote

1. What is the cash price, separate from financing?
2. Which PVWatts assumptions (azimuth, tilt, shade, derate) produced the
   production estimate?
3. Is the inverter warranty 25 yr (micro) or 12 yr (string), and what
   replaces it when it dies?
4. Who takes the ITC, and what's my basis if I can't use the full credit?
5. What is the remove-and-reinstall cost if I reroof in 10 years?
6. What is my export rate under the CURRENT net-metering tariff, not last
   year's?
