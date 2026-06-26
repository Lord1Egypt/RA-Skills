# Zim

Agent travel middleware for assembling booking-ready travel options.

## What it does
- searches flights, hotels, and cars
- assembles policy-aware itineraries
- stores traveler preferences and approval state
- creates Stripe Checkout sessions for payment collection
- does **not** complete supplier reservations unless a real executor is added

## Runtime
- Python 3.10+
- bash, curl, jq

## Install
```bash
python3 -m pip install .
```

## Key env vars
- `TRAVELPAYOUTS_TOKEN`
- `TRAVELPAYOUTS_MARKER`
- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`
- `ZIM_BASE_URL` (optional)

## Truthfulness boundary
Payment collection may be implemented, but provider booking execution is still placeholder-only in the current package.
