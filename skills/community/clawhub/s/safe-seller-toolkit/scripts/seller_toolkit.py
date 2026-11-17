#!/usr/bin/env python3
"""safe-seller-toolkit: sell stuff online without getting scammed or hurt.

Pure-stdlib. Four tools:
  price    -- item condition + original price -> used-price bands by category
              with depreciation curves (furniture/electronics/bikes/kids/...).
  message  -- buyer message -> scam-likelihood triage (overpayment, code
              verification, shipping off-platform, courier pickup, gift cards)
              with a safe reply suggestion.
  meetup   -- meetup safety checklist + "no-go" conditions from listing details.
  labels   -- generate a printable shipping label info sheet (weights, dims,
              service cost tiers, do-not-ship list for fraud-prone routes).

Usage:
  python3 seller_toolkit.py price --category electronics --condition good \
      --original 599 --age-years 2
  python3 seller_toolkit.py message --text "I'll send you a 6-digit code..."
  python3 seller_toolkit.py meetup --item "iPhone 13" --price 350 --station
  python3 seller_toolkit.py labels --weight-lb 3.2 --dimensions 12x9x4 --value 350
"""
from __future__ import annotations

import argparse
import sys

# Deprecation: surviving value fraction by condition (new-in-box, excellent,
# good, fair, poor) per year of age, category base multiplier.
CATEGORIES = {
    # name: (base_retain_1y, yearly_decay_after, floor_frac, demand_note)
    "iphone":          (0.65, 0.12, 0.10, "high demand: sells in days if priced at band"),
    "android-phone":   (0.55, 0.14, 0.08, "flagships only hold value; midrange collapses"),
    "laptop":          (0.60, 0.15, 0.10, "MacBooks hold; Windows fades faster"),
    "tablet":          (0.50, 0.15, 0.08, "weak market, expect slow sale"),
    "tv":              (0.45, 0.18, 0.05, "bulky = local pickup only usually"),
    "camera":          (0.65, 0.10, 0.15, "enthusiast market, lenses hold value"),
    "game-console":    (0.60, 0.10, 0.15, "strong resale, esp. with extras"),
    "furniture":       (0.35, 0.10, 0.05, "IKEA: nearly worthless used; solid wood: strong"),
    "bike":            (0.50, 0.08, 0.15, "spring sells; verify serial not stolen"),
    "kids-gear":       (0.40, 0.15, 0.05, "strollers/car seats: check recall + expiry"),
    "appliance-small": (0.40, 0.12, 0.05, "works-or-scrap, no middle market"),
    "appliance-large": (0.35, 0.12, 0.05, "local pickup, working demo required"),
    "tools-power":     (0.55, 0.08, 0.20, "pro brands (DeWalt/Makita) hold strong"),
    "clothing":        (0.20, 0.20, 0.02, "brand names only; otherwise donate"),
    "watch":           (0.60, 0.08, 0.20, "luxity watches hold; fashion watches die"),
    "other":           (0.40, 0.12, 0.05, "generic curve: expect pennies after 5y"),
}

CONDITION_MULT = {"new-in-box": 1.15, "excellent": 1.0, "good": 0.85, "fair": 0.65, "poor": 0.4}

# (label, keywords tuple, points, why)
SCAM_SIGNALS = [
    ("overpayment / 'accidental' extra", ("overpay", "sent too much", "extra $", "refund the difference", "mistake and sent", "cash app you the extra", "keep the change"), 35,
     "Classic fake-payment: their 'payment' will bounce after you refund real money. Never refund anything."),
    ("verification-code phishing", ("6-digit", "six digit", "verification code", "code i sent", "read me the code", "google voice code", "sent a code to your phone", "confirm the code"), 40,
     "They're hijacking your phone number (Google Voice port scam). NEVER share codes with anyone."),
    ("off-platform payment", ("zelle", "venmo friends", "cashapp", "cash app", "paypal friends and family", "gift card", "apple pay", "crypto", "bitcoin", "wire transfer", "western union", "moneygram"), 30,
     "Off-platform = zero buyer-seller protection and platform ban. On-platform payment only, or cash in hand."),
    ("off-platform shipping / courier", ("i'll arrange shipping", "arrange a courier", "my shipper will", "movers will pick", "logistics company", "i'm out of town, my agent", "prepaid shipping label", "email me at", "text me at"), 30,
     "Fake-shipping scams: fake labels, fake payment emails. Meet in person or ship only after real payment clears."),
    ("pressure / urgency", ("right now", "asap", "today only", "last one", "i need it before", "don't tell", "keep this between", "first to pay"), 15,
     "Urgency + secrecy is social engineering. Real buyers can wait an hour."),
    ("price-blind buyer", ("what's the lowest", "final price", "last price without seeing", "i'll take it sight unseen", "no questions"), 12,
     "Buyers who don't ask a single question about condition are often resellers or setting up a switch scam."),
    ("switch / swap bait", ("open the package", "swap", "trade my", "i'll bring my old one", "exchange plus cash"), 18,
     "Item-switch at meetup: they hand back a different/broken unit. Verify serials before money moves."),
    ("escrow / agent nonsense", ("escrow", "my agent", "my assistant will handle", "broker", "on behalf of my client", "company account"), 20,
     "Third-party payment theater. You deal with the buyer in person or not at all."),
    ("too-good offer", ("i'll pay double", "above asking", "add extra for your trouble", "i'll pay $500 more"), 30,
     "Overpayment family. Nobody pays above asking on used goods. Block."),
]

NO_GO_REASONS = [
    "buyer refuses to meet in public / insists on your home",
    "buyer wants to pay more than asking (overpayment scam)",
    "any mention of verification codes",
    "payment arrives before meetup, 'as a deposit', or via link",
    "buyer sends a shipping label instead of paying you",
    "gut says no. your listing, your rules — you can always walk.",
]

MEETUP_RULES = [
    "police-station exchange zones: many departments offer camera-monitored swap spots — use them for phones/electronics",
    " daylight only, busy public place, interior if possible (bank lobby, coffee shop)",
    "bring a friend; tell someone where you're going and when you're back",
    "cash only, count it before handing the item; prefer bills you can verify under light",
    "for phones: meet at carrier store, verify IMEI on the spot (dial *#06#)",
    "for high-value: bank lobby meetup, deposit the cash immediately",
    "never share your exact address until the deal is confirmed",
    "if buyer brings a different person than expected, restart the safety checklist",
    "trust decline-and-leave authority: you owe no one a sale",
]

DO_NOT_SHIP = [
    "any buyer 'arranging their own shipping' (label fraud)",
    "addresses that are freight forwarders / package reshippers",
    "deals where payment notification arrives by EMAIL ONLY — log into the platform/app yourself",
    "any request to ship before payment posts and clears (not 'pending')",
]

SERVICE_TIERS = [
    ("USPS Ground Advantage", "cheapest to 1 lb; includes $100 insurance", 0.55),
    ("USPS Priority Mail", "1-3 day flat-rate boxes win for dense items", 0.85),
    ("UPS Ground", "better for 5+ lb; strong tracking", 0.70),
    ("UPS/FedEx 2Day", "only if buyer paid for speed", 1.60),
]


def cmd_price(args):
    if args.category not in CATEGORIES:
        print(f"Unknown category '{args.category}'. Choose from: {', '.join(CATEGORIES)}")
        return 1
    base, decay, floor, note = CATEGORIES[args.category]
    retain = base * ((1 - decay) ** max(0, args.age_years - 1))
    retain = max(retain, floor)
    cond_mult = CONDITION_MULT[args.condition]
    point = args.original * retain * cond_mult
    low, high = point * 0.85, point * 1.15

    print("=" * 62)
    print(f"PRICE BAND — {args.category} ({args.condition}, {args.age_years}y old)")
    print("=" * 62)
    print(f"Original: ${args.original:,.0f}   retention: {retain * cond_mult:.0%}")
    print(f"List at:   ${high:,.0f}   (negotiation headroom built in)")
    print(f"Expect:    ${point:,.0f}")
    print(f"Floor:     ${low:,.0f}   below this, keep it / donate it")
    print(f"Market note: {note}")
    print("\nSanity checks:")
    print(f"  - search sold listings (not active) for your exact model")
    print(f"  - price 5-10% under the lowest comparable SOLD price to move fast")
    print(f"  - bundles (chargers, cases, box) add 5-15%, not 30%")
    return 0


def cmd_message(args):
    text = args.text.lower()
    hits = []
    score = 0
    for label, kws, pts, why in SCAM_SIGNALS:
        found = [k for k in kws if k in text]
        if found:
            hits.append((label, pts, found[0], why))
            score += pts

    print("=" * 62)
    print("BUYER MESSAGE TRIAGE")
    print("=" * 62)
    if not hits:
        print("No scam patterns matched. Still: stay on-platform, meet in public,")
        print("cash or cleared payment only. Normal buyers ask questions about")
        print("the item's condition.")
        return 0

    for label, pts, kw, why in hits:
        print(f"[+{pts}] {label}")
        print(f"       trigger: \"{kw}\"")
        print(f"       {why}")
    score = min(score, 100)
    print(f"\nSCAM LIKELIHOOD: {score}/100")
    if score >= 40:
        print("VERDICT: BLOCK. Do not reply with anything but 'no'.")
        print("Safe reply: \"Cash in person only, or on-platform payment. No codes,")
        print("no shipping arrangements, no agents.\" Then block on second ask.")
    elif score >= 15:
        print("VERDICT: PROCEED WITH RULES. Reply once with your terms:")
        print("\"Public meetup, cash only, price is firm.\" If they push any")
        print("flagged topic again, treat as BLOCK.")
    else:
        print("VERDICT: LIKELY FINE. Standard caution applies.")
    return 0


def cmd_meetup(args):
    print("=" * 62)
    print(f"MEETUP SAFETY — {args.item} @ ${args.price:,.0f}")
    print("=" * 62)
    if args.station:
        print("GOOD: police-station exchange zone requested.")
    if args.price >= 300:
        print("HIGH-VALUE DEAL: bank lobby meetup + immediate deposit recommended.")
        print("  Verify phone IMEI (*#06#) or serial numbers BEFORE cash moves.")
    if args.price >= 1000:
        print("  Consider a cashier's check drawn in person at their bank,")
        print("  or complete the sale inside your bank with a teller witness.")
    print("\nChecklist:")
    for r in MEETUP_RULES:
        print(f"  [ ] {r.strip()}")
    print("\nNO-GO conditions (any one = walk away):")
    for r in NO_GO_REASONS:
        print(f"  ✗   {r}")
    return 0


def cmd_labels(args):
    w = args.weight_lb
    dims = args.dimensions.lower().split("x")
    try:
        dims = [float(d) for d in dims]
        girth = 2 * (dims[1] + dims[2])
    except (ValueError, IndexError):
        print("Dimensions must look like 12x9x4 (inches)")
        return 1
    print("=" * 62)
    print(f"SHIP SHEET — {w} lb, {args.dimensions} in, declared ${args.value:,.0f}")
    print("=" * 62)
    print("Service tiers (relative cost index vs Ground=0.70):")
    for name, note, cost in SERVICE_TIERS:
        est = args.value * 0.031 * cost * max(1, w / 3)  # rough index, not a quote
        print(f"  {name:22} {note:44} ~${est:5.2f}")
    print("\nPackaging rules:")
    print("  - 2 inches of padding on every side; item must not shift")
    print("  - remove old shipping labels completely (misroutes cause losses)")
    print("  - photograph item powered-on + serial before boxing (proof pack)")
    print("  - insure for sold price; keep the receipt in the box photo set")
    print("\nDO NOT SHIP when:")
    for r in DO_NOT_SHIP:
        print(f"  ✗   {r}")
    print("\nOnly ship after payment shows COMPLETED (not pending) in the app.")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="Marketplace seller safety toolkit")
    sub = p.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("price")
    pr.add_argument("--category", required=True)
    pr.add_argument("--condition", default="good",
                    choices=list(CONDITION_MULT))
    pr.add_argument("--original", type=float, required=True)
    pr.add_argument("--age-years", type=int, default=1)

    m = sub.add_parser("message")
    m.add_argument("--text", required=True)

    me = sub.add_parser("meetup")
    me.add_argument("--item", required=True)
    me.add_argument("--price", type=float, required=True)
    me.add_argument("--station", action="store_true",
                    help="meeting at a police-station exchange zone")

    la = sub.add_parser("labels")
    la.add_argument("--weight-lb", type=float, required=True)
    la.add_argument("--dimensions", required=True, help="LxWxH inches, e.g. 12x9x4")
    la.add_argument("--value", type=float, required=True)

    args = p.parse_args(argv)
    return {"price": cmd_price, "message": cmd_message,
            "meetup": cmd_meetup, "labels": cmd_labels}[args.cmd](args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
