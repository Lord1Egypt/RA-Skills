#!/usr/bin/env python3
"""
rental_return_shield.py — leave the lot defended and come back clean.

Commands:
  pickup    Pickup inspection: what to photograph, existing-damage
            logging with tire-tread/burn-hole rule-of-thumb sizes, and
            the 10 things to verify BEFORE driving off.
  fuel      Fuel math: refuel-yourself vs they-refuel pricing; the
            local-station-vs-highway-station spread; receipt discipline.
  dropoff   Return protocol: the 8-step defended return that makes
            damage claims impossible, with timestamped log.
  dispute   Fight a post-return damage/charge claim: evidence index,
            timeline builder, and the dispute letter.

Stdlib only. Offline. Consumer information, not legal advice.
"""
import argparse
from datetime import date, datetime

PICKUP_SHOTS = [
    "Front — full head-on (plate visible)",
    "Rear — full (plate visible)",
    "Left side — full profile",
    "Right side — full profile",
    "Front-left corner close (bumper+quarter)",
    "Front-right corner close",
    "Rear-left corner close",
    "Rear-right corner close",
    "Roof (hail/branch damage is claimed later)",
    "Hood + windshield (chips: zoom on existing stars)",
    "Rear windshield + trunk lid",
    "All 4 wheels: rim faces (curb rash is the #1 claim)",
    "All 4 tires: tread (close-up, sidewalls)",
    "Interior front: seats, dash, headliner",
    "Interior rear + cargo area",
    "Odometer + fuel gauge (one frame)",
    "Windshield glass from inside (existing crack check)",
    "Floor mats + trunk floor (stains)",
]

PICKUP_CHECKS = [
    "Damage marked on THEIR form matches what YOU see — anything unmarked, note + photo",
    "Spare tire/jack present (charged $ for missing at return)",
    "Fuel level matches contract ('full' means FULL, photograph gauge)",
    "Headlights, brake lights, turn signals, wipers work",
    "AC/heat actually blows cold/hot",
    "Phone charger + USB ports work",
    "Registration + insurance card in glovebox",
    "24/7 roadside number saved in YOUR phone",
    "Odometer photo (mileage disputes are real)",
    "Walk-around video, slow, narrated — 90 seconds",
]

FUEL_RULES = (
    "Fuel rules (US): most majors are return-full-else-refuel-service-charge.\n"
    "  - Their refuel 'service': $8-15/gal vs pump ~$3-4 — 3-4x penalty.\n"
    "  - Prepaid fuel option: only wins if you return EMPTY; usually a loss.\n"
    "  - FPO-style 'we'll top it up, just bring it close' = fine, capped fee — read cap.\n"
    "  - EVs: return between the stated % window (often 60-80%); over = gift, under = fee."
)


def cmd_pickup(a):
    print("PICKUP INSPECTION — before you drive off\n")
    print(f"PHOTO LIST ({len(PICKUP_SHOTS)} shots, timestamp on):")
    for i, s in enumerate(PICKUP_SHOTS, 1):
        print(f"  {i:2}. {s}")
    print("Rule of thumb for damage size words (photos must show a size "
          "reference — fingertip or coin IN the shot):")
    print("  - 'Dime-sized' chips/scuffs: photograph anyway; small doesn't stay small on claims")
    print("  - Tire tread: insert a coin; if the top of the design is worn flush = note it")
    print("  - Burn holes/interior stains: measure + photo; these are charged per-item")
    print("\nVERIFY (10 checks):")
    for i, c in enumerate(PICKUP_CHECKS, 1):
        print(f"  {i:2}. {c}")
    print("\nIf damage is NOT on their form and they refuse to note it:")
    print("  email yourself photos + a note BEFORE leaving the lot; that timestamp")
    print("  is your proof it pre-existed. 60 seconds now beats a $600 fight later.")


def cmd_fuel(a):
    print(FUEL_RULES + "\n")
    if a.tank_gallons:
        pump_total = a.tank_gallons * a.pump_price * a.fraction
        their_total = a.tank_gallons * a.service_price * a.fraction
        print(f"Tank ~{a.tank_gallons} gal x {a.fraction:.0%} needed:")
        print(f"  Refuel yourself @ ${a.pump_price:.2f}/gal  = ${pump_total:,.2f}")
        print(f"  Let them refuel @ ${a.service_price:.2f}/gal = ${their_total:,.2f}")
        print(f"  Penalty for laziness: ${their_total - pump_total:,.2f}")
        print("\nStation strategy: fill 5-10 miles from the return point, not at")
        print("airport-adjacent stations (+$0.40-0.80/gal). Keep the receipt —")
        print("some counters ask for it within 10 miles of return; a receipt from")
        print("a station 50 miles away still satisfies 'full' but not policies")
        print("requiring 'receipt within X miles'. Photo of gauge at return.")


def cmd_dropoff(a):
    print("RETURN PROTOCOL — the defended drop-off\n")
    steps = [
        "Refuel 5-10 mi out; keep receipt; photo of fuel gauge.",
        "Remove EVERYTHING (glovebox, trunk, seat pockets, chargers, sunglasses).",
        "Re-walk the photo list from pickup: same 18 angles. New marks = photograph.",
        "Wheels/tires close-up again (curb rash is claimed post-return when you can't inspect).",
        "Interior: crumbs, stains, pet hair — 5 min with a trash bag beats a $150 'detailing fee'.",
        "Video the odometer + fuel gauge + exterior, narrated.",
        "GET A REPs SIGNATURE/PRINTOUT: 'returned, no damage noted'. No rep (after-hours drop)?",
        "  Photograph the car IN THE RETURN BAY, keys location, time-stamp everything,",
        "  note the bay number/lot location. After-hours = claims happen next morning.",
        "Keep contract + return receipt + photos until the final bill clears your card + 60 days.",
    ]
    for i, s in enumerate(steps, 1):
        print(f"  {i}. {s}")
    print(f"\nLog entry: returned {date.today().isoformat()} {datetime.now().strftime('%H:%M')} —")
    print("  [location], [rep name / after-hours], photos archived: [WHERE].")


def cmd_dispute(a):
    print("POST-RETURN DISPUTE — damage/charge you don't accept\n")
    print("Evidence index (assemble before writing anything):")
    ev = [
        "Pickup photos (timestamped) covering the claimed area",
        "Pickup damage form / contract markings",
        "Return photos + signed no-damage receipt (if you got one)",
        "Final bill: what exactly is claimed (damage vs cleaning vs fuel vs admin)",
        "Your fuel receipt + gauge photos (fuel charges)",
        "Walk-around videos (both ends of the rental)",
    ]
    for i, e in enumerate(ev, 1):
        print(f"  {i}. {e}")
    print("\nTimeline (fill in, attach):")
    print(f"  [date] Rented at [location]; pre-existing damage photo: [ref]")
    print(f"  [date] Returned at [time]; rep inspection: [result]")
    print(f"  [date] Charge appeared: ${a.amount:.2f} for [ITEM]")
    print(f"  [date] Dispute opened with: [card issuer / company / both]")
    letter = f"""
[Your name / address / rental agreement #]

RE: Disputed charge — ${a.amount:.2f} — "[DESCRIPTION]" — Agreement {a.agreement}

To whom it may concern,

On [RETURN DATE] I returned vehicle [PLATE/MODEL] at [LOCATION] in the
same condition as received, documented by [N] timestamped photographs
taken at pickup on [PICKUP DATE] and at return (attached, Exhibits A-B).
The return was processed by [REP NAME / after-hours protocol] with
[no damage noted / signed receipt, Exhibit C].

The charge of ${a.amount:.2f} for "[DESCRIPTION]" is therefore disputed.
The damage (if any) pre-existed my rental or is not attributable to it.
I request: (1) copies of the damage documentation the charge is based
on, including inspection reports and repair invoices, and (2) reversal
of the charge.

If this is not resolved within 30 days, I will dispute the charge with
my card issuer and file complaints with the state Attorney General's
consumer division and the Better Business Bureau.

Sincerely,
[NAME]"""
    print("\nDISPUTE LETTER:\n" + letter)
    print("\nSend to: the rental company's customer care AND dispute with your")
    print("card issuer within 60 days of the statement (chargeback deadline).")
    print("Credit-card disputes have a hard clock — open it NOW, letter in parallel.")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("pickup", help="inspection photo list + 10 pre-drive checks")
    f = sub.add_parser("fuel", help="fuel math: self vs service refuel")
    f.add_argument("--tank-gallons", type=float, default=15.0)
    f.add_argument("--fraction", type=float, default=0.5,
                   help="fraction of tank you'll need to replace")
    f.add_argument("--pump-price", type=float, default=3.60)
    f.add_argument("--service-price", type=float, default=11.50)
    sub.add_parser("dropoff", help="8-step defended return protocol")
    d = sub.add_parser("dispute", help="evidence index + dispute letter")
    d.add_argument("--amount", type=float, default=0.0)
    d.add_argument("--agreement", default="[AGREEMENT #]")
    a = ap.parse_args()
    {"pickup": cmd_pickup, "fuel": cmd_fuel,
     "dropoff": cmd_dropoff, "dispute": cmd_dispute}[a.cmd](a)


if __name__ == "__main__":
    main()
