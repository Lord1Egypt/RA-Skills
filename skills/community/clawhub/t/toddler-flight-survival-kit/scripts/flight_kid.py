#!/usr/bin/env python3
"""flight_kid.py — toddler flight planner and packing quantifier (stdlib only).

Subcommands:
  plan   flight-day strategy from age + duration + departure time + nap window
  pack   quantified packing list per awake flight-hour
  seats  seat + restraint strategy by age and aircraft (generic 3-3)
"""
import argparse
import sys
from datetime import datetime, timedelta

def hhmm(t):
    return datetime.strptime(t, "%H:%M")

def fmt(dt):
    return dt.strftime("%H:%M")

def age_band(m):
    if m < 24:
        return "lap-eligible young toddler — hardest flyer (mobile, no reason, 5–10 min attention)"
    if m < 42:
        return "ticketed older toddler — 10–20 min attention, screen-capable, restraint needed"
    return "preschooler — reasoning available, this skill still applies but easier"

def cmd_plan(a):
    dep = hhmm(a.depart)
    print(f"Child {a.age_months} mo | flight {a.duration_h} h | departure {a.depart}")
    print(f"Age band: {age_band(a.age_months)}")
    nap_start, nap_end = None, None
    if a.nap:
        s, e = a.nap.split("-")
        nap_start, nap_end = hhmm(s), hhmm(e)
        nap_len = (nap_end - nap_start).seconds / 3600.0
        print(f"Home nap: {s}–{e} ({nap_len:.1f} h)")
    # duration band
    if a.duration_h < 2:
        band = "short: no nap planning; snack pipeline + 3 novelties"
    elif a.duration_h < 4:
        band = "medium: flight should fully CONTAIN the nap or avoid it — never land mid-nap"
    elif a.duration_h < 7:
        band = "long: two-window structure — pre-nap energy burn, nap attempt, post-nap calm"
    else:
        band = "long-haul: night-align sleep (pjs, skip dinner service if needed), no 'keep awake' myths"
    print(f"Duration band: {band}\n")
    # strategy
    land = dep + timedelta(hours=a.duration_h)
    overlap = 0.0
    if nap_start and nap_end:
        # overlap of nap window with flight window (assume nap can drift to flight-day times)
        ov_start = max(datetime.combine(dep.date(), nap_start.time()), dep)
        ov_end = min(datetime.combine(dep.date(), nap_end.time()), land)
        if ov_end > ov_start:
            overlap = (ov_end - ov_start).seconds / 3600.0
    if overlap >= 1.0:
        strat = "NAP-CONTAINED"
        print(f"Strategy: {strat} — nap overlaps {overlap:.1f} h of the flight")
        print(f"  board sleepy: normal wake time, early lunch,")
        print(f"                NO car nap on the way (or a capped 20-min one)")
        print(f"  target sleep start: wheels-up +15–30 min; dim window, familiar sleep sack/lovey")
        print(f"  post-nap: it's the boredom-cliff protocol — staged novelties, aisle walks")
    elif a.duration_h >= 7 and dep.hour >= 19:
        strat = "NIGHT-ALIGNED"
        print(f"Strategy: {strat} — evening long-haul")
        print("  pj change at boarding, bedtime routine in miniature (book + song), lights plan")
        print("  expect split sleep (4–6 h) — the second half is a normal awake flight")
    else:
        strat = "AWAKE-ENTERTAINED"
        print(f"Strategy: {strat} — no useful nap overlap ({overlap:.1f} h)")
        print("  burn energy pre-boarding (gate area walking, not screens)")
        print("  entertainment staged per the pack list; snack rotation 3 distinct/h")
        print("  protect ONE calm object for descent, deploy nothing early")
    print(f"\nLanding ≈ {fmt(land)} — descent starts ≈ {fmt(land - timedelta(minutes=35))}")
    print("DESCENT PROTOCOL (the hardest window):")
    print("  T-40 min: last bathroom/diaper change")
    print("  T-35 min: start sucking item (straw cup / lollipop ≥4 yr or pacifier); infant = feed")
    print("  T-30 min: calm-object deployed, low-stim only, lights as-is")
    print("  pain-relief dosing: obtained from pediatrician BY WEIGHT before travel day")
    print("\nBoard LAST (no pre-boarding patience burn); one adult + gear boards early.")
    print("Meltdown ladder: name feeling → bounded choices → sensory change → slow snack → screen reserve → containment mode.")
    return 0

def cmd_pack(a):
    awake = a.awake_h or a.duration_h
    m = a.age_months
    print(f"Packing for {awake:.0f} awake flight-hours, child {m} mo:\n")
    snacks = max(4, round(awake * 3))
    nov = max(3, round(awake * 60 / 40))
    print(f"  snacks: {snacks} distinct items (slow-eating weighted: raisin boxes, straw pouches,")
    print(f"           dry cereal threading, cheese sticks; no crumble storms, no sugar spikes)")
    print(f"  novelty items: {nov} (one per 30–45 min awake), HALF never-seen, each wrapped —")
    print(f"           unwrapping IS the activity: stickers, window clings, painter's tape roll,")
    print(f"           pipe cleaners, spiral notebook + washable markers, tiny flashlight")
    wipes = max(20, round(awake * 5))
    diap = round(awake / 2) + 3 if m < 36 else 0
    print(f"  wipes: {wipes}")
    if diap:
        print(f"  diapers: {diap} + changing-pad clutch (airline bathrooms: use the fold-down table)")
    print(f"  clothes: 2 changes for child{' + 1 shirt for you (if <18 mo)' if m < 18 else ''}")
    print(f"  screens: downloaded + OFFLINE-tested the night before, 2x content,")
    print(f"           volume-limited headphones fitted BEFORE the airport")
    print(f"  calm-object: 1 — SEALED for descent, never deployed earlier")
    print(f"  med kit: child pain relief (weight-dosed per pediatrician), saline spray (cabin 10–15% RH),")
    print(f"           thermometer strip, 2 spare masks if airline requires")
    if m < 24:
        print(f"  lap-infant extras: feed bottles for takeoff+descent, light blanket for floor... no,")
        print(f"           for lap warmth; carrier for hands-free airport movement")
    print(f"\nLeave home: loud toys, many-small-parts kits, glitter, the 40-item activity box.")
    return 0

def cmd_seats(a):
    m = a.age_months
    print(f"Seat + restraint strategy, child {m} mo:")
    if m < 24:
        print("  LAP-ELIGIBLE: infant fare ~10% intl / free domestic lap")
        print("  but: safety bodies recommend a ticketed restraint; sanity also does by ~18 mo")
        print("  restraint if ticketed: FAA-approved infant/convertible car seat (label!), window")
    else:
        print("  TICKET REQUIRED (age 2+): window seat = trapped entertainment, adult beside")
        print("  restraint: FAA-label car seat OR CARES harness (1+ yr, 22–44 lb, 1 lb, no bulkhead issue)")
        print("  boosters are NOT allowed in flight — check the car seat at the gate for free")
    print("  pairing: toddler window + adult middle/aisle in 3-3; adult takes the aisle side")
    print("  bulkhead: bassinet space (lap infants, long-haul, bulkhead-mounted) BUT no car seat")
    print("            allowed in most bulkhead rows, no under-seat storage, colder, fixed arms")
    print("  avoid: last row (no recline, near lav queue), exit rows (kids prohibited anyway)")
    print("  gate-check stroller: free on nearly all carriers; bring it to the gate, not the counter")
    return 0

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan")
    p.add_argument("--age-months", type=int, required=True)
    p.add_argument("--duration-h", type=float, required=True)
    p.add_argument("--depart", required=True, help="HH:MM")
    p.add_argument("--nap", help="HH:MM-HH:MM home nap window")
    p.set_defaults(fn=cmd_plan)
    k = sub.add_parser("pack")
    k.add_argument("--age-months", type=int, required=True)
    k.add_argument("--duration-h", type=float, required=True)
    k.add_argument("--awake-h", type=float)
    k.set_defaults(fn=cmd_pack)
    s = sub.add_parser("seats")
    s.add_argument("--age-months", type=int, required=True)
    s.set_defaults(fn=cmd_seats)
    a = ap.parse_args()
    sys.exit(a.fn(a))

if __name__ == "__main__":
    main()
