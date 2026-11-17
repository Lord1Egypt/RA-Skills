# Safe Seller Toolkit

**Sell your stuff without getting scammed, robbed, or lowballed.**

Marketplaces (Facebook Marketplace, Craigslist, OfferUp, eBay) are the
easiest way to turn unused items into cash — and the easiest way to lose
money, an iPhone, or your phone number to a professional fraud script. Most
sellers can't tell a real buyer's message from a scammer's opener, price by
guesswork, and meet strangers with no protocol.

## The problem
1. **Scam scripts are professional.** Overpayment, Google-Voice code
   hijacking, fake shipping labels, off-platform payment — these are
   industrialized playbooks; casual sellers are their raw material.
2. **Pricing is guesswork.** "How much for my 2-year-old laptop?" gets
   answers ranging from $200 to $700; most sellers leave 30% on the table
   or never sell at all.
3. **Meetups have no safety culture.** Robberies arranged via marketplace
   listings are a documented, recurring crime pattern in every metro area.

## What this toolkit does
- `price` — 16 category depreciation curves × 5 condition grades →
  list/expect/floor band, with market-behavior notes per category.
- `message` — scores inbound buyer messages against 9 scam families
  (40+ trigger phrases) → 0-100 likelihood, BLOCK/PROCEED verdict, safe
  reply.
- `meetup` — deal-value-scaled safety checklist with hard no-go conditions
  ($300+ triggers bank-lobby protocol, $1000+ teller-verified funds).
- `labels` — shipping tiers, packaging rules, proof-pack photography, and
  the do-not-ship fraud list.

## Quick start
```bash
# Price a 2-year-old iPhone in good condition
python3 scripts/seller_toolkit.py price --category iphone --condition good \
    --original 799 --age-years 2

# Triage a suspicious buyer message
python3 scripts/seller_toolkit.py message \
    --text "I'll send a 6-digit code to verify, zelle you extra for trouble, my shipper picks up"

# In-person sale safety checklist
python3 scripts/seller_toolkit.py meetup --item "iPhone 13" --price 350

# Shipping sheet with fraud rules
python3 scripts/seller_toolkit.py labels --weight-lb 3.2 --dimensions 12x9x4 --value 350
```

Pure Python 3 stdlib. Works offline. Nothing is logged or sent anywhere.

## Who needs this
- The ~50% of adults who used a peer-to-peer marketplace in the past year
- Parents selling kids' gear (recall/expiry traps), gamers, photographers
- Anyone whose instinct says "this buyer seems off" but can't articulate why
- Frequent declutterers who want a repeatable, safe selling process

## License
MIT — see LICENSE.
