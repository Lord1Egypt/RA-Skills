---
name: used-car-sentinel
description: "Use when you are shopping for a used car and must decode a vehicle listing (VIN, mileage, price, age) into a real risk picture before you drive anywhere or pay a deposit. VIN validation + decoding (WMI country/manufacturer, model-year code, check-digit verification, sequential-number red flags), mileage-plausibility analysis against age and class (detects odometer rollbacks and clocked clocks), holistic price-vs-market fair-offer model, deal-breaker screening (salvage/rebuilt/flood/title brands, TSI taxi/fleet patterns, untold collision age gaps), and a structured 30-minute test-drive inspection sheet. All offline — works when you are standing in a parking lot with one bar of signal."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [used-car, vin, odometer, inspection, buying-guide, marketplace, due-diligence]
---

# Used Car Sentinel — Listing Decoder & Deal Screener

## Overview

Used-car listings are adversarial documents. The seller — professional or
private — presents the car in the best light the truth allows and some light it
doesn't. The buyer has one photo set, a price, an age, a mileage, and (if
lucky) a VIN, and must decide: is this car worth a 90-minute round trip and a
deposit?

Every year, buyers lose billions to:

- **Rolled-back odometers** — still common (interstate commerce makes prosecution rare); a 5-year-old car "with 68,000 km" that actually has 168,000.
- **Salvage/rebuilt titles** laundered state-to-state or simply not mentioned.
- **Fair-price blindness** — asking prices on private-marketplace listings routinely run 10–25% over real transaction values; buyers negotiate $500 off a $3,000 markup and feel victorious.
- **Wasted weekends** — the listing was junk; the photos were old; the "one owner" was a rental fleet.

This skill is a **pre-contact screening tool**. It takes what the listing
gives you and returns a risk-ranked verdict before you ever send a message:

1. **VIN Intelligence** — structural validation (17 chars, no I/O/Q, correct
   check digit per ISO 3779), WMI decode (country + manufacturer), model-year
   code extraction with a 30-year cycle disambiguation, plant code. A VIN
   that fails the check digit is a forgery flag, full stop.
2. **Mileage plausibility** — km/year vs class norms (city runabout ~12k,
   average ~15–20k, highway cruiser ~25–35k, taxi/fleet 50k+); flags both
   suspiciously low (rollback or garage queen rot) and unusually high (fleet
   or engine near end-of-life). Age-band tables: what mileage is normal for a
   3/5/8/12-year-old car.
3. **Fair-offer model** — asking price vs computed market band from age,
   mileage, and class depreciation curves; suggests an opening offer, a
   walk-away price, and the exact negotiation talking points derived from the
   car's own risk flags.
4. **Deal-breaker screen** — the patterns that end the analysis: title brands,
   missing VIN plate, mileage inconsistent with service history gaps, price
   too good to be true (>30% below modeled market = almost certainly a scam
   or salvage).
5. **Pre-purchase protocol** — what to demand before travel (VIN photos,
   service-book pages, title photo), the 30-minute inspection sheet, the
   test-drive route that exposes head gasket, transmission, and suspension
   faults, and when to pay for an independent inspection ($100–200 that saves
   $4,000).

All offline. No API keys. Runs in a parking lot on a phone.

## When to Use

- Screening any private-party or small-dealer used-car listing before contact
- Validating a VIN the seller sent (or refusing to travel until they do)
- Sanity-checking mileage vs age before believing "little old lady, weekend use"
- Building a negotiation sheet from objective risk flags
- Running the 30-minute inspection at the viewing (printable checklist)
- Don't use for: new cars (different economics), collector/enthusiast vehicles
  (value is condition+provenance, not depreciation curves), or as a substitute
  for a professional pre-purchase inspection, a vehicle-history report
  (Carfax/Autocode/local equivalent), or legal advice. This narrows the odds;
  it doesn't replace diligence that costs money.

## How It Works

1. `vin decode <VIN>` — validate structure + check digit, decode WMI
   (country/manufacturer), extract year/plant, flag mismatches (e.g. "2019
   model year" VIN on a listing that says 2021).
2. `screen --year 2018 --km 68000 --price 11500 --class compact` — the full
   pre-contact workup: mileage plausibility, market band, offer strategy,
   risk list, verdict (GREEN / YELLOW / RED).
3. `inspect` — prints the 30-minute inspection sheet + test-drive protocol.
4. `negotiate --year 2018 --km 68000 --price 11500 --class compact` — talking
   points derived from the risk flags, with dollar values attached.

## Commands

```bash
# VIN first (get it from the seller before traveling)
python3 scripts/sentinel.py vin decode 1HGCM82633A004352
# → check digit OK, Honda JP/US plant, year 2003 — structure valid

python3 scripts/sentinel.py vin decode 5YJ3E1EA7KF317000
# → Tesla, 2019, valid structure

# Full screening of the listing
python3 scripts/sentinel.py screen --year 2018 --km 68000 --price 11500 --class compact
# → mileage PLAUSIBLE-LOW 11.3k km/yr ... verdict YELLOW: negotiate from 9800

# Inspection sheet for the viewing
python3 scripts/sentinel.py inspect

# Negotiation sheet
python3 scripts/sentinel.py negotiate --year 2018 --km 68000 --price 11500 --class compact
```

## VIN Check-Digit Math (why it catches forgeries)

Position 9 of the VIN is a check digit computed from the other 16 via a
published letter→number table and weight loop (ISO 3779). Legitimate
manufacturers compute it; counterfeit plates, typo'd listings, and cloned
identities frequently get it wrong. `vin decode` recomputes it and says
VALID / MISMATCH / NOT-COMPUTABLE (EU VINs sometimes skip it — noted, not
flagged red by itself).

## Common Pitfalls

1. **Trusting the listing year over the VIN year.** The VIN's position-10
   code is the model year; a mismatch means the listing (or the seller) is
   wrong. Always reconcile.
2. **Believing round mileage.** 68,000 exactly on an 8-year-old car is either
   true or rolled back to a number humans like. Ask for the service book and
   cross-check every stamp.
3. **Negotiating from the asking price.** Negotiate from *your* computed band.
   Anchoring on their number is how a $3,000 markup becomes a $2,500 "win".
4. **Skipping the check digit.** A VIN with a bad check digit means the plate
   is counterfeit or mistyped — either way, walk.
5. **Confusing "no accidents reported" with "no accidents".** History reports
   only show what was reported to insurance/police. The inspection sheet
   covers panel gaps, paint texture, and weld beads for a reason.
6. **Testing the stereo before the cold start.** The inspection sequence is
   ordered so the expensive faults (cold-start knocks, head gasket, sludging)
   surface first. Follow the order.
7. **Paying a deposit to "hold" a car you haven't inspected.** Deposits on
   GREEN/YELLOW cars are refundable only in your imagination.
8. **Buying flood cars by smell alone.** Modern flood cars are detailed
   professionally. The sheet checks under-seat bolts, harness connectors, and
   spare-wheel wells for silt lines and corrosion.

## Verification Checklist

- [ ] `vin decode` validates 17-char structure, rejects I/O/Q, computes the ISO 3779 check digit
- [ ] WMI table covers major markets (US, JP, DE, KR, CN, FR, IT, GB, SE, ES, CZ, TR, MX, BR, IN, RU)
- [ ] `screen` outputs: mileage verdict, market band, opening/walk-away offer, risk flags, GREEN/YELLOW/RED
- [ ] Price >30% under modeled market triggers a SCAM/SALVAGE warning, not excitement
- [ ] `inspect` sheet covers cold start, fluids, panel gaps, OBD port, test-drive route, paperwork
- [ ] Everything runs offline with stdlib only

## References

- `references/vin-math.md` — check-digit computation worked through, WMI table
  excerpt, year-code cycle, market-band model assumptions, inspection rationale
