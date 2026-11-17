# Storage Unit Verdict

**Roughly 1 in 10 US households pays for a storage unit, and the average unit stays rented ~2 years — long past whatever life event justified it.** The industry runs on one exploitable fact: $140/month doesn't feel like a decision. This skill runs the math nobody runs: what's inside worth *today* (depreciated), versus what you've paid and will keep paying.

## The One Calculation

> A unit holding $2,500 of depreciated furniture at $140/mo crosses the **rent-exceeds-value line in 18 months**. Most audited units are already past it — the tenant is paying $140/month to avoid one 4-hour sorting weekend that costs less than two months' rent.

```bash
# Audit your unit: contents -> depreciation bands -> verdict
python3 scripts/unit_verdict.py audit --rent 140 --months-held 26 \
    --contents "dining set:1200:wood,sofa:900:uphol,boxes clothes:300:clothes,tools:800:tools"
# -> contents worth $795-1475 today; $3640 already paid
# -> VERDICT: ALREADY-LOST — the unit is storing avoidance, not wealth

# Considering a unit during a bounded move/renovation?
python3 scripts/unit_verdict.py consider --rent 165 --months 4 \
    --contents "apartment contents:6500:mixed" --exit-date 2027-03-01

# Are you paying climate-control rates for lawn chairs?
python3 scripts/unit_verdict.py climate --contents "leather sofa,comics,metal shelves"

# Dated 30-day exit plan (weekend-by-weekend, labour < 2 months' rent)
python3 scripts/unit_verdict.py exit-plan --rent 140 --unit "10x10"
```

## Verdicts

- **KEEP (short bridge)** — contents value >> rent with a real exit date. Fine.
- **KEEP (high-value)** — tools/antiques worth more than replacement. Re-audit yearly.
- **DOWNGRADE** — purge pass + one size class down = instant 30-45% saving; shelving racks make a 5×10 hold a 10×10's floor-spread contents.
- **PURGE / ALREADY-LOST** — dated 30-day plan: photos home first, sell tier at real resale prices, charity pickup comes to the unit, written cancellation with confirmation.

## The Honest Rules

- Contents valued at **resale**, not purchase: sofas 5-15%, solid wood 30-50%, mattresses ~$0, tools 40-60%.
- **Untouched 12 months = you don't need it** (exceptions: documented horizon date, true archive).
- Rate increases of 5-15%/yr mean your $140 unit is a $190 unit in 3 years — renewal letter = re-run the audit.
- Lien auctions can liquidate everything within 60-90 days of missed payments — exit deliberately, not by neglect.
- Sell-and-rebuy usually beats storing low-value goods: 11 months at $140/mo = $1,500, the full resale value of the contents.

## Who Needs This

Anyone paying for a unit (or asked to keep paying), executors auditing an estate (heirs overestimate furniture value), divorcing couples splitting contents with a deadline, people between homes, and anyone considering a unit who wants the bounded-horizon math done before signing a month-to-month forever-lease.

## License

MIT © Denis Voronin
