# Used Car Sentinel

**Decode a used-car listing into a risk picture before you waste a Saturday — or worse.**

## The problem

Used-car listings are adversarial documents. From a photo set, a price, an
age, a mileage, and (if you're lucky) a VIN, you must decide whether to spend
a weekend and a deposit. Meanwhile:

- Odometer fraud is still rampant — the "68,000 km" 8-year-old may have done 168,000.
- Private-listing asking prices routinely run 10–25% over real transaction values.
- A typo'd or cloned VIN means the car you inspect isn't the car you're buying.
- The EU's EES-style digitization of everything means the sloppy-counting era is over — for sellers too: history reports and title brands surface at the worst moment for the unprepared buyer.

## What it does

| Command | What you get |
|---|---|
| `vin decode <VIN>` | Structure check, ISO 3779 **check-digit verification** (catches typos & counterfeit plates), maker/country, model year, plant |
| `screen` | Mileage plausibility vs class norms, fair-price band, opening/walk-away offer, risk flags, GREEN/YELLOW/RED verdict |
| `negotiate` | Screen + objective talking points with dollar values |
| `inspect` | The 30-minute inspection sheet: cold start, fluids, panel gaps, flood-car tells, test-drive route, paperwork |

All offline, stdlib only — works standing in a parking lot with one bar of signal.

## Quick start

```bash
# Seller sent the VIN? Verify before traveling.
python3 scripts/sentinel.py vin decode 1HGCM82633A004352

# Screen the listing
python3 scripts/sentinel.py screen --year 2018 --km 68000 --price 11500 --class compact

# Print the inspection sheet for the viewing
python3 scripts/sentinel.py inspect

# Negotiation ammunition
python3 scripts/sentinel.py negotiate --year 2018 --km 68000 --price 11500 --class compact
```

## Who needs this

Anyone buying a used car privately or from a small dealer — which is most
used-car buyers, everywhere, always. Second-hand cars are one of the few
remaining high-stakes asymmetric-information purchases in daily life.

## Honest limits

A relative price band, not a trim-level price guide. A valid check digit
proves consistency, not authenticity (cloned cars use real donor VINs).
Nothing here replaces a history report or a $150 independent pre-purchase
inspection — it tells you whether those are worth buying *for this car*.

MIT License. © 2026 Denis Voronin
