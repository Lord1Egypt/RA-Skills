# Rental Car Return Shield

Procedural defense against rental-car damage claims: the 10-minute
pickup inspection protocol, fuel economics math, the defended
drop-off, and the post-return dispute kit.

## The Real Problem

Rental damage claims are an asymmetry business: they document with an
industrial process, you return at 6 AM rushing for a flight with zero
evidence — and weeks later a "$612.50 curb rash + admin fee" charge
arrives when you can't inspect the car or remember the rim. Every
consumer-agency guide says "document condition" but nobody ships the
actual shot list, the after-hours protocol, the fuel math, or the
dispute letter. This skill is those artifacts.

## What It Does

- **pickup** — 18-shot timestamped photo list (wheels close-up: the #1
  claim is curb rash), 10 pre-drive checks, unmarked-damage protocol
- **fuel** — self-refuel vs their $8-15/gal service with real numbers,
  prepaid-fuel trap, EV % windows, station strategy
- **dropoff** — 8-step return: re-walk photos, interior reset,
  signed no-damage receipt, after-hours bay protocol
- **dispute** — evidence index, timeline, dispute letter demanding
  their inspection docs + invoices, dual-track with the 60-day
  chargeback clock
- **references/** — damage-recovery economics (repair + loss-of-use +
  diminished value + admin stacking), CDW/insurance interactions,
  EU vs US differences, escalation ladder, fee menu decoder

## Quick Start

```bash
python3 scripts/rental_return_shield.py pickup
python3 scripts/rental_return_shield.py fuel --tank-gallons 16 --fraction 0.5
python3 scripts/rental_return_shield.py dropoff
python3 scripts/rental_return_shield.py dispute --amount 612.50
```

Stdlib only, offline. Consumer information, not legal advice.

## License

MIT © Denis Voronin
