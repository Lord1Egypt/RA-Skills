# Solar Quote Verifier

**Recompute a solar proposal's math before you sign anything.**

## The problem

Solar sales is a numbers game played on asymmetric information. Proposals
routinely: model production at ideal orientation with no shade, quote payback
before inverter replacement and degradation, embed a 10–15% "dealer fee" in
"low-APR" loans, run lease escalators (2.9%/yr) hotter than utility rate
escalation (~2.5%/yr) so savings invert mid-term, and claim the 30% ITC
credit value even when the lease company takes it. Homeowners sign 20–25-year
contracts based on numbers they cannot check — until now.

## What it does

`scripts/solar_quote_check.py` (stdlib-only, offline):

1. **$/W pricing band** — $2.50–3.50/W pre-ITC is fair; higher is flagged
   with negotiation ammo (every $0.10/W on 8 kW = $800).
2. **Production sanity** — recomputes kWh from regional sun-hours × 0.84
   derate × orientation; >10% overstatement = RED FLAG (the #1 proposal lie).
3. **Honest payback** — models 0.5%/yr degradation, 2.5%/yr rate escalation,
   $150/yr O&M, inverter replacement at year 13 ($0.35/W) inside a 25-yr
   net-savings curve; compares against the proposal's claimed payback.
4. **Loan X-ray** — monthly/total payments; warns when payments exceed
   year-1 solar value; explains the cash-price dealer-fee test.
5. **PPA/lease trap detector** — finds the exact year the escalator-driven
   PPA rate crosses your utility rate (savings go negative).
6. **Conflict checks** — roof older than 10 yr vs 25-yr panels; ITC you
   can't absorb.

Verdicts: **FAIR / OVERPRICED / RED-FLAG** with named levers.

## Example

```bash
python3 scripts/solar_quote_check.py --demo
python3 scripts/solar_quote_check.py --kw 9.6 --cost 44160 \
  --quoted-kwh 16800 --rate 0.16 --region midwest --orientation w \
  --quoted-payback 8 --roof-age 12
```

Demo 1 output highlights: $4.60/W → WALK-AWAY band; quoted production +25%
above the physical model → RED FLAG; honest payback ~year 19 vs claimed 8;
roof 12 yr old → reroof conflict. Demo 2: a 3.5%-escalator PPA crosses grid
parity around year 13.

## Who needs this

The ~4 million US households a year solicited for rooftop solar, anyone
holding 2–3 competing quotes, and anyone offered a lease/PPA "with no money
down". The 20-minute check this script does is worth $1,000s in negotiation
or a bad-contract dodge.

## Honesty

Bands are US mid-2020s defaults and every assumption is printed so it can be
argued with (`--sun-hours`, `--ppa-escalator`... override). Not financial
advice; a verification layer before you sign a 25-year contract.

## License

MIT © 2026 Denis Voronin
