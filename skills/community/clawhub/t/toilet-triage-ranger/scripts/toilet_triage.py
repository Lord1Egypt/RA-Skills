#!/usr/bin/env python3
"""Toilet Triage Ranger — diagnose running/weak toilets, waste math,
DIY protocols. Stdlib only."""
import argparse

SYMPTOMS = {
    "runs-constantly": {
        "name": "toilet runs constantly",
        "causes": [
            ("FLAPPER not sealing (warped, mineral, chain propping)", 0.55,
             "Dye test: food coloring in tank, wait 15 min NO flush; color appears in bowl = flapper leak. Also: is the chain holding it slightly open?", "flapper"),
            ("Fill valve not shutting off — water rises over overflow tube and trickles to bowl", 0.30,
             "Open lid: is waterline ABOVE the overflow tube top, with steady trickle into it? Lift the float arm fully — water should STOP; if not, the valve diaphragm is done.", "fill-valve"),
            ("Float set too high", 0.15,
             "Waterline should sit 1-2 cm below overflow tube top. Bend arm down / turn adjustment screw.", "fill-valve"),
        ],
    },
    "phantom-refill": {
        "name": "tank refills by itself every few minutes (phantom flush)",
        "causes": [
            ("FLAPPER slow-passing — tank drains until float triggers refill", 0.70,
             "Dye test (15 min, no flush). Also mark water level, wait 30 min: drop = tank leaking to bowl.", "flapper"),
            ("Water level above overflow tube", 0.20,
             "Lid off: waterline vs tube top; trickle sound into tube = level/valve.", "fill-valve"),
            ("Fill valve slow internal leak keeps trickling", 0.10,
             "Lift float fully — must stop instantly; dripping sound at valve = replace.", "fill-valve"),
        ],
    },
    "hisses": {
        "name": "hissing sound between flushes",
        "causes": [
            ("Fill valve passing slowly, refilling what leaks past flapper", 0.60,
             "Combined check: dye test for flapper; float-lift for valve. Whichever fails is the cause; if both pass, the valve's internal gasket seeps — replace valve.", "fill-valve"),
            ("Refill tube inserted too deep / clamped into overflow, siphoning", 0.40,
             "The small tube into the overflow top should just CLIP at the top, not reach the water — if submerged it siphons continuously.", "fill-valve"),
        ],
    },
    "weak-flush": {
        "name": "weak / incomplete flush",
        "causes": [
            ("Rim jet holes clogged (mineral) — weak swirl, water rises then spirals down", 0.40,
             "Mirror under the rim: crusty holes? Clean with vinegar-soaked cloth + pin. Also the direct jet hole at bowl bottom front.", "weak"),
            ("Tank water level too LOW (short drop = weak siphon start)", 0.30,
             "Waterline should be at the fill line mark / 1-2 cm below overflow top. Raise float.", "weak"),
            ("Partial flapper lift (chain too loose / handle sloppy)", 0.20,
             "Flush with lid off: flapper should jump fully up. Shorten chain by 1-2 links.", "weak"),
            ("Venting problem (glugging, other fixtures gurgle when flushed)", 0.10,
             "Slow glug + siphon breaks early = blocked roof vent. Different job (roof), plumber territory if you can't clear it.", "weak"),
        ],
    },
    "water-floor": {
        "name": "water on the floor around the base",
        "causes": [
            ("Wax ring / flange seal failed, often after toilet rocked for months", 0.60,
             "Rock test: gentle side-to-side. Any rock = ring compressed/broken. ALSO check supply hose and tank-bolt seals first (cheaper causes).", "flange"),
            ("Tank-to-bowl gasket or bolts weeping (water trails down bowl back)", 0.30,
             "Dry everything, lay paper towel under the tank-bowl seam, flush: wet = gasket/bolts.", "flange"),
            ("Condensation (cold water, humid room) — not a leak", 0.10,
             "Tank sweat in humid weather; vanishes in dry season. Tank liner or mixing valve fixes it.", "none"),
        ],
    },
}

RATES = {  # L/min
    "drip": 0.05,
    "trickle": 0.4,
    "running": 1.5,
    "loud": 4.0,
}

PHANTOM = {"every-5-min": 5.0, "every-10-min": 3.0, "every-30-min": 1.5}  # L/event approx

FIXES = {
    "flapper": {
        "title": "FLAPPER REPLACEMENT — 10 minutes, ~$8",
        "steps": [
            "Water OFF at the wall supply valve (clockwise). Gentle — if stuck, see rescue note.",
            "Flush to empty the tank; sponge out the remainder.",
            "Unhook chain from the flush lever arm.",
            "Slide old flapper off the overflow-tube ears (or unscrew old-style ring).",
            "CLEAN THE SEAT: scrub the rim the flapper sits on with a scrubbie + vinegar; run a finger around it — must feel smooth. Steel wool NO.",
            "Seat the new flapper flat; reattach chain with ½-1 cm slack.",
            "Water ON; let tank fill; watch the flapper: full lift on flush, clean drop, quiet seal.",
            "VERIFY: dye test — clear bowl after 20 min, no refill cycles for an hour.",
        ],
        "tools": ["sponge", "scrubbie", "white vinegar", "new universal flapper (match old style roughly)"],
        "rescue": "STUCK SHUTOFF VALVE: do NOT force. Work the handle gently loose (open-close ¼ in). Still stuck: close the house main (or bathroom upstream valve), replace the supply valve's washer or the whole angle stop — 20 min with a wrench once water is off upstream.",
    },
    "fill-valve": {
        "title": "FILL VALVE REPLACEMENT — 30 minutes, ~$15",
        "steps": [
            "Water OFF; flush; sponge tank dry.",
            "Disconnect supply nut under the tank (bucket under it — a cup escapes).",
            "Unscrew the old valve's locking nut OUTSIDE the tank bottom.",
            "Lift old valve out; set new one per its height gauge (or cut tube to size).",
            "Rubber washer inside, locking nut outside — SNUG, not gorilla (porcelain!).",
            "Refill tube clips at the overflow tube TOP — never inserted deep.",
            "Water ON slowly; set float so waterline sits 1-2 cm BELOW overflow tube top.",
            "Flush-test x3: full refill, clean stop, no trickle into the tube after stop.",
        ],
        "tools": ["adjustable wrench", "bucket", "sponge", "new fill valve (height-adjustable recommended)"],
        "rescue": "If the new valve hisses at full shutoff, debris is in the line: close water, remove valve top cap per its manual, rinse the seal, reassemble.",
    },
    "flange": {
        "title": "WAX RING / TANK-BOLT JOB — 60-90 minutes, ~$15 (muscle required)",
        "steps": [
            "Water OFF; flush; sponge tank AND bowl dry.",
            "If tank-bowl seam leak: just the bolts/gasket — remove bolts, replace rubber washers+gasket, reseat. 30 min.",
            "If base leak with rock: full reset — remove bolt caps at the base, unscrew flange bolts, lift the whole toilet straight up (40-60 kg; two people or a helper for wall-hugging WCs).",
            "Scrape the old wax ring off the flange completely; check flange condition (broken ear = repair ring).",
            "New wax ring on the flange (or on the toilet horn), toilet down SQUARE — no twisting after contact.",
            "New bolts, washers; tighten alternately by hand then wrench: SNUG + ¼ turn. Porcelain cracks are permanent.",
            "Reconnect supply; test: flush x3, dry paper around the base after 10 min.",
            "Caulk the base (leave a gap at the back so future leaks show, not hide).",
        ],
        "tools": ["wax ring (or waxless gasket)", "bolt set", "putty knife", "wrench", "gloves", "helper for lifting"],
        "rescue": "Flange below floor level / broken: use a flange repair ring or extra-thick wax ring. Sewer gas smell after reassembly = reseat needed; do not caulk over it.",
    },
}

def cmd_diagnose(a):
    s = SYMPTOMS[a.symptom]
    print(f"SYMPTOM: {s['name']}")
    for i, (cause, p, confirm, part) in enumerate(sorted(s["causes"], key=lambda c: -c[1]), 1):
        print(f"\n {i}. [{p*100:.0f}%] {cause}")
        print(f"    CONFIRM: {confirm}")
        if part != "none":
            print(f"    FIX: run  fix --part {part}")
    print("\nSafety: tank water is CLEAN (no chemicals). The two real risks:")
    print("over-tightening porcelain (crack) and forcing a stuck shutoff valve.")

def cmd_waste(a):
    price = a.price or 4.0
    cur = a.currency or "USD"
    if a.rate in RATES:
        lpm = RATES[a.rate]
        daily = lpm * 60 * 24
        label = a.rate
    else:
        interval = {"every-5-min": 5, "every-10-min": 10, "every-30-min": 30}[a.rate]
        daily = PHANTOM[a.rate] * (1440 / interval)
        lpm = daily / 1440
        label = f"phantom refill {a.rate}"
    monthly = daily * 30
    yearly = daily * 365
    print(f"WASTE ESTIMATE — {label} (~{lpm:.2f} L/min):")
    print(f"  per day:    {daily:8,.0f} L   ≈ {price*daily/1000:8.2f} {cur}")
    print(f"  per month:  {monthly:8,.0f} L   ≈ {price*monthly/1000:8.2f} {cur}")
    print(f"  per year:   {yearly:8,.0f} L   ≈ {price*yearly/1000:8.2f} {cur}")
    print(f"\nReference: a 2-person household uses ~11,000-14,000 L/month TOTAL.")
    if monthly > 4000:
        print("VERDICT: this dwarfs your normal use — fix TODAY (likely a $8 flapper).")
    elif monthly > 800:
        print("VERDICT: worth fixing this week — real money, easy repair.")
    else:
        print("VERDICT: small leak, fix when convenient; still a 10-min repair.")
    print("\nMETER VERIFY (30 min): read the water meter, flush nothing, wait")
    print("30 min, re-read. Difference × 48 = daily liters. Facts beat estimates.")

def cmd_decide(a):
    renter = a.renter
    sym = a.symptom
    urgent = sym in ("runs-constantly", "phantom-refill")
    print(f"DECISION — symptom: {sym}" + (" (rental: document + notify)" if renter else ""))
    if sym == "water-floor":
        print("  WATER OFF NOW at the supply valve. If the cause is the base ring,")
        print("  it's sewage-adjacent — landlord/plumber job in rentals, DIY-able")
        print("  for owners with the flange protocol (muscle required).")
    elif urgent:
        print("  Fix TODAY: top cause is a flapper — 10 min, ~$8, no plumber.")
        print("  If the dye test and float-lift both fail differently, use the")
        print("  fill-valve protocol; still under 30 min.")
    else:
        print("  Fix this week; symptoms are quality-of-life, not money-bleeding.")
    if renter:
        print("\n  RENTAL PATH: photograph + meter-read, written notice TODAY with")
        print("  the waste numbers (weekly refill logs if landlord is slow).")
        print("  Running toilets are habitability items in most jurisdictions;")
        print("  the paper trail matters more than the repair speed.")
    print("\n  PLUMBER IF: porcelain cracked, flange broken, venting suspicion,")
    print("  or supply valve snaps. Everything else is a $8-20 part.")

def cmd_fix(a):
    f = FIXES[a.part]
    print(f"=== {f['title']} ===\nTOOLS: {', '.join(f['tools'])}\n")
    for i, s in enumerate(f["steps"], 1):
        print(f" {i:2d}. {s}")
    print(f"\nRESCUE NOTE: {f['rescue']}")

def cmd_weak(a):
    print("WEAK FLUSH — check in this order (cheapest first):")
    print("  1. Tank level: waterline at fill mark / 1-2 cm below overflow top?")
    print("     Low = weak drop. Raise float (bend arm / screw). 1 min.")
    print("  2. Rim jets: mirror under rim — crust? Vinegar cloth 30 min, pin")
    print("     the holes clear. Also the jet hole at bowl bottom-front. 30 min.")
    print("  3. Flapper lift: lid off, flush — full jump? Shorten chain 1-2 links.")
    print("  4. Venting: glug-sound + other drains gurgle = roof vent partial")
    print("     blockage (bird nest, leaves). Plumber/roof ladder territory.")
    print("\nWHY flushes work at all: the sudden water drop STARTS a siphon in the")
    print("trap; anything slowing the drop (low level, clogged jets, partial")
    print("flapper) weakens the siphon. It's not 'more water' — it's water SPEED.")

def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("diagnose")
    d.add_argument("--symptom", required=True, choices=sorted(SYMPTOMS))
    d.set_defaults(fn=cmd_diagnose)

    w = sub.add_parser("waste")
    w.add_argument("--rate", required=True, choices=sorted(list(RATES) + list(PHANTOM)))
    w.add_argument("--price", type=float, default=None, help="price per 1000 L (per kL)")
    w.add_argument("--currency", default=None)
    w.set_defaults(fn=cmd_waste)

    dec = sub.add_parser("decide")
    dec.add_argument("--symptom", required=True, choices=sorted(SYMPTOMS))
    dec.add_argument("--renter", action="store_true")
    dec.set_defaults(fn=cmd_decide)

    f = sub.add_parser("fix")
    f.add_argument("--part", required=True, choices=sorted(FIXES))
    f.set_defaults(fn=cmd_fix)

    wk = sub.add_parser("weak")
    wk.set_defaults(fn=cmd_weak)

    a = p.parse_args()
    a.fn(a)

if __name__ == "__main__":
    main()
