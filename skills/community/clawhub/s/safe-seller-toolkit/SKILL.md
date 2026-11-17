---
name: safe-seller-toolkit
description: "Use when selling personal items on marketplaces (Facebook Marketplace, Craigslist, OfferUp, eBay) — prices used goods with category depreciation curves, triages inbound buyer messages for the 9 scam families (overpayment, code phishing, fake shipping, off-platform payment) with BLOCK/PROCEED verdicts and safe replies, generates meetup safety checklists scaled by deal value, and shipping checklists with do-not-ship fraud rules."
version: 1.0.1
author: Denis Voronin
license: MIT
tags: [marketplace, selling, scam-prevention, pricing, safety]
---

# Safe Seller Toolkit

## Overview
Peer-to-peer marketplaces move enormous volumes of secondhand goods — and
concentrate fraud. The Internet Crime Complaint Center logged billions in
losses from non-delivery/non-payment fraud alone; marketplace scams
(overpayment, Google-Voice code hijack, fake shipping labels, off-platform
payment) are the everyday layer beneath that. Casual sellers list a phone,
get four messages in an hour, and three are scripts written by professionals.

This skill gives the seller four instruments:

1. **price** — 16 category depreciation curves × 5 condition grades →
   list/expect/floor price band plus market-behavior notes.
2. **message** — inbound buyer text scored against 9 scam families (40+
   trigger phrases) → 0-100 scam likelihood, BLOCK/PROCEED verdict, and a
   safe one-line reply.
3. **meetup** — value-scaled in-person safety checklist (police exchange
   zones, IMEI verification, bank-lobby protocol for high-value deals) plus
   hard no-go conditions.
4. **labels** — shipping service comparison, packaging rules, proof-pack
   photography, and the do-not-ship fraud list.

Pure stdlib, offline, logs nothing.

## When to Use
- "Someone offered to pay full price without questions — is this a scam?"
- "How much should I list my 2-year-old iPhone / laptop / couch for?"
- "A buyer wants me to ship to their agent / send a code / take Zelle"
- Preparing a first in-person sale (meetup checklist)
- "Got an offer on Marketplace, feels off, check this message"
- Selling high-value items ($300+ phones, bikes, cameras, laptops)

**Don't use for:** business/inventory-scale selling (different economics),
real-estate or vehicle-title transfers (legal process beyond scope), or as a
substitute for platform-specific dispute processes once fraud already
happened (report + chargeback paths differ by platform).

## How It Works — Numbered Steps
1. Price the item:
   `python3 scripts/seller_toolkit.py price --category iphone --condition good --original 799 --age-years 2`
   → list $447 / expect $388 / floor $330. Cross-check against *sold*
   listings for the exact model; the band is a starting anchor, not gospel.
2. List with the safe-reply ready. When messages arrive, triage each:
   `python3 scripts/seller_toolkit.py message --text "I'll send a 6-digit code..."`
   → per-signal breakdown, score, verdict (BLOCK / PROCEED WITH RULES /
   LIKELY FINE), and a safe reply line.
3. Arrange the meetup with the checklist:
   `python3 scripts/seller_toolkit.py meetup --item "iPhone 13" --price 350`
   High-value deals escalate automatically (bank lobby, IMEI/serial checks).
4. If shipping instead: 
   `python3 scripts/seller_toolkit.py labels --weight-lb 3.2 --dimensions 12x9x4 --value 350`
   Ship only after payment reads COMPLETED, never 'pending'.
5. Walk away on any no-go condition. The sale you lose to a scammer costs
   more than the sale you decline from a weird-but-honest buyer.

## The 9 Scam Families (message triage)
| Family | Points | Core move |
|---|---|---|
| verification-code phishing | 40 | hijacks your number (Google Voice port) |
| overpayment / 'accidental' extra | 35 | fake payment + refund of real money |
| off-platform payment | 30 | Zelle/Venmo/gift cards/crypto = no protection |
| off-platform shipping / courier | 30 | fake labels, fake payment emails |
| too-good offer | 30 | pays above asking — always a setup |
| escrow / agent theater | 20 | third-party payment misdirection |
| switch / swap bait | 18 | hands back a different item |
| pressure / urgency | 15 | rushes you past your own judgment |
| price-blind buyer | 12 | zero questions = reseller or switch scam |

Score ≥40 → BLOCK. 15-39 → PROCEED WITH RULES (one terms reply, second
offense = block). Under 15 → normal caution.

## Common Pitfalls
1. **Sharing ANY verification code.** The "buyer" is porting your number to
   Google Voice to run scams as you. Codes are never shared, ever.
2. **Accepting 'pending' payments.** Zelle/Venmo/payments can be reversed or
   fake-screenshotted. Cleared and completed, or cash counted in hand.
3. **Refunding an overpayment.** Their payment bounces; your refund is real.
4. **Shipping on the buyer's label.** Fake labels get your package stolen
   or delivered nowhere; you have no proof of delivery for disputes.
5. **Meeting at home because it's heavy.** Couch sellers get robbed. Meet in
   the driveway with a friend, or pay a mover — never alone inside.
6. **Pricing from active listings.** Active = unsold = overpriced. Search
   SOLD/completed listings and undercut the cheapest comparable.
7. **Answering scam scripts with engagement.** Every reply confirms your
   account is active and human. Block, don't debate.
8. **Skipping the proof pack.** Photograph the item powered on + serial
   before boxing. It's your only evidence in a 'item not as described' scam.

## Example
```
Seller listing a 2-year-old iPhone 13, gets an instant message.

$ price --category iphone --condition good --original 799 --age-years 2
→ List $447 / expect $388 / floor $330 (retention 49%)

Buyer: "I'm out of town, my shipper will pick it up. I'll send a 6-digit
code to confirm, zelle you extra $50, text me asap."

$ message --text "<paste>"
→ [+40] code phishing  [+30] off-platform payment
  [+30] courier shipping  [+15] urgency
→ SCAM LIKELIHOOD 100/100 — VERDICT: BLOCK
  Safe reply: "Cash in person only. No codes, no shipping, no agents."

Second buyer: "Is the battery health above 85%? Can we meet at the
police station exchange zone tomorrow?"
→ 0 signals, LIKELY FINE → meetup checklist, station flag on.
```

## References
- `references/scam-field-guide.md` — each scam family anatomy: the script,
   the psychology, the exact counter, and what to do if already hit.
- `references/pricing-curves.md` — the depreciation model, category table,
   condition multipliers, and local-market calibration method.
