# Salary Negotiator

**Prepare salary negotiations with structured math and scripts — never accept the first number again.**

The 10 minutes of a compensation conversation move more money per minute than
anything else in a career. Most people walk in unprepared, accept the first
number, and leave 10–30% on the table — a gap that compounds for years
through raises, matches, and bonuses that are all computed from base.

## The Problem

- You get an offer that "feels okay" but have no idea what's negotiable
- "0.5% equity in a $60M startup" vs "$60k/yr RSUs at BigCo" — nobody taught
  you how to compare these
- Raise conversations get deflected with "budget's locked" and you have no
  counters ready
- Negotiation advice online is generic ("know your worth!") with no numbers

## What It Does

`scripts/salary_negotiator.py` (offline, stdlib-only) runs the numbers that
matter before any negotiation:

| Command | What it computes |
|---|---|
| `floor` | Your walk-away number from monthly costs, runway, and benefit gaps |
| `offer` | Market anchor (target/stretch/floor) + risk-weighted total-comp EV of the offer + round-1 script |
| `compare` | Two differently-shaped offers normalized to comparable EV, years 1–3 |
| `raise` | Raise-conversation script built from impact bullets + market delta |
| `demo` | Full walkthrough with sample data |

Key ideas:

- **Total comp = expected value, not paper value.** Bonuses weighted at 85%
  payout, RSUs at 90% retention, startup options at 15% of paper value —
  documented assumptions you can override.
- **One number, never a range.** The anchor builder produces a target with a
  rationale you can say out loud.
- **Scripts, not vibes.** Every scenario has fill-in-the-blank words plus
  counters for the standard pushbacks ("band is fixed", "budget's locked").

## Quick Start

```bash
# Build the strategy for an offer
python3 scripts/salary_negotiator.py offer \
  --role "Senior Backend Engineer" --location "Remote US" \
  --offer-base 145000 --offer-bonus 10 --offer-signon 15000 \
  --offer-rsu-annual 40000 --market-min 130000 --market-med 160000 --market-max 210000

# What's my walk-away number?
python3 scripts/salary_negotiator.py floor --monthly-costs 4200 --runway-months 6

# BigCo vs Startup
python3 scripts/salary_negotiator.py compare \
  --a "BigCo: base 150k, bonus 15%, RSU 60k/yr, 401k match 4%" \
  --b "Startup: base 130k, options 0.5%, strike 1.50, valuation 60M"

python3 scripts/salary_negotiator.py demo
python3 scripts/salary_negotiator.py --help
```

## Test

```bash
python3 scripts/test_salary_negotiator.py   # → "N passed, 0 failed"
```

## References

- [`references/comp-structures.md`](references/comp-structures.md) — how to
  value every comp component: equity types, vesting, bonus shapes, benefits
- [`references/scripts.md`](references/scripts.md) — the full script library:
  offers, counters, raises, competing offers, silence technique, Q&A sheet

## Scope & Disclaimer

For employees comparing salaried offers and raises. For freelance/contract
rate-setting, use a freelance-rate-calculator approach (different tax and
overhead math). Educational tool, not legal or financial advice — have an
attorney review non-competes and equity agreements.

## License

MIT © Denis Voronin
