#!/usr/bin/env python3
"""Sourdough starter management: feeding math, hydration conversion, readiness,
diagnosis, vacation hibernation, levain build timing."""
import argparse
from datetime import datetime, timedelta

# Peak hours after feeding for 1:S:S feeds by temperature (approx, wheat)
PEAK_HRS = {20: 18.0, 22: 14.0, 24: 11.0, 26: 8.0, 28: 6.5, 30: 5.0}


def peak_hours(temp, ratio_scale=1.0):
    temps = sorted(PEAK_HRS)
    h = PEAK_HRS[temps[0]]  # default for temps below table
    if temp <= temps[0]:
        h = PEAK_HRS[temps[0]]
    elif temp >= temps[-1]:
        h = PEAK_HRS[temps[-1]]
    else:
        for lo, hi in zip(temps, temps[1:]):
            if lo <= temp <= hi:
                f = (temp - lo) / (hi - lo)
                h = PEAK_HRS[lo] + f * (PEAK_HRS[hi] - PEAK_HRS[lo])
                break
    # smaller feeds (1:1:1) peak ~35% faster than 1:5:5
    return h * (0.65 if ratio_scale < 3 else 1.0)


def cmd_feed(a):
    t = a.temp
    if a.style == "stiff":
        print(f"STIFF (60% hydration) routine @ {t}C:")
        print("  Daily: 20g starter + 50g flour + 30g water (1:2.5:1.5)")
        print("  - tangier (acetic), slower peak; good for schedule control")
        print(f"  - peak approx {peak_hours(t) * 1.3:.0f} h after feeding")
        return
    ph = peak_hours(t, ratio_scale=5)  # standard 1:5:5 feed
    if t <= 22:
        ratio, feeds, peak = "1:5:5", "once/day", ph
    elif t <= 26:
        ratio, feeds, peak = "1:5:5", "once/day (twice if baking)", ph
    else:
        ratio, feeds, peak = "1:8:8", "twice/day", ph * (8 / 5)
    print(f"100% hydration routine @ {t}C:")
    print(f"  Feed {ratio} by WEIGHT (e.g. 10g starter + 50g flour + 50g water)")
    print(f"  Rhythm: {feeds}")
    print(f"  Expected peak (2x rise): ~{peak:.0f} h after feeding")
    print(f"  Jar mark: rubber band at feed line; feed at peak or 2-3 h after")
    print()
    print("  Fridge alternative: feed 1:2:2, sit 2 h at room temp, chill;")
    print("  revive with 2-3 cycles before baking. Holds ~2 weeks.")


def cmd_hydration(a):
    have, target, mass = a.have, a.target, a.mass
    # current mix composition
    flour = mass / (1 + have / 100.0)
    water = mass - flour
    # target composition
    t_flour = flour  # flour conserved
    t_water = flour * target / 100.0
    dw = t_water - water
    print(f"Converting {mass}g of {have}% hydration starter to {target}%:")
    print(f"  Currently: {flour:.0f}g flour + {water:.0f}g water")
    if dw >= 0:
        print(f"  ADD {dw:.0f}g water — instant conversion (flour mass unchanged)")
    else:
        print(f"  Need to REMOVE {-dw:.0f}g water — impractical; instead:")
    print()
    print("  NOTE: feeding at target hydration only shifts the blend toward")
    print("  target asymptotically. Fastest correct route: discard down to")
    print("  20g, then feed 50g flour + %.0fg water per cycle." % (50 * target / 100))
    print("  After 2-3 such cycles the starter IS ~%d%% hydration." % target)


def cmd_readiness(a):
    ph = peak_hours(a.temp, a.ratio)
    print(f"Readiness @ {a.temp}C after a 1:{a.ratio}:{a.ratio} feed:")
    print(f"  Expected peak: ~{ph:.1f} h (2x volume if healthy)")
    print(f"  Ready-to-mix window: peak to peak+1 h")
    print()
    print("  Float test: reliable ONLY inside that window;")
    print("  false-floats right after feeding (air pockets) and 3+ h post-peak.")
    print("  Jar rise mark beats the float test every time.")
    print()
    print("  Healthy visual at peak: domed top, open bubbles, pleasant")
    print("  yogurt-and-apple aroma. Flat + boozy = past peak; wait for next cycle.")


DIAG = [
    (["no rise", "never doubles", "not rising", "slow"],
     "COLD or OVER-DILUTED culture",
     ["Find a 24-26C spot (top of fridge, cupboard + lamp); not windowsill (night cold)",
      "Feed 1:1:1 twice a day for 2 days (revival density), then 1:5:5",
      "Use some whole-grain flour (rye) for 2 feeds — minerals/enzymes wake yeast",
      "Mark the jar: 1.5x in 12 h at 24C = alive, just slow; 0 rise for 48 h at 26C = truly dead"]),
    (["acetone", "nail polish", "paint thinner"],
     "YEAST STARVATION (bacteria overproducing solvents)",
     ["Pour off any liquid; discard all but 10g",
      "Feed 1:5:5 every 12 h at 24-26C for 2-3 days",
      "Aroma should return to yogurt/applesauce within 2 days",
      "Cause: too-long gaps between feeds or too-warm spot"]),
    (["hooch", "liquid on top", "water on top", "gray liquid"],
     "UNDERFED (normal, not fatal)",
     ["Pour off the hooch (or stir it in for a tangier bread)",
      "Feed 1:2:2 now, then resume normal rhythm",
      "Post-fridge hooch is expected — revival cycle handles it"]),
    (["mold", "fuzzy", "colored spots", "pink", "orange"],
     "MOLD CONTAMINATION",
     ["Fuzzy colored growth = discard the whole jar; not worth rescuing",
      "Pink/orange streaks throughout = bacterial takeover; start fresh",
      "Prevention: clean jar rims, feed with clean utensils, no dunking hands",
      "White liquid hooch is NOT mold; fuzzy is"]),
    (["sluggish after fridge", "won't wake", "hibernation"],
     "DORMANT CULTURE (needs cycles, not hours)",
     ["Feed 1:1:1 at room temp; repeat every 12 h",
      "Expect first doubling by cycle 2-3 (24-48 h)",
      "Do NOT bake from a starter until it doubles twice in a row",
      "Next fridge trip: feed 1:2:2, wait 2 h before chilling"]),
    (["rose and collapsed", "deflated", "fell back", "gummy"],
     "PEAKED AND OVER-FERMENTED",
     ["It's alive — you just missed the peak; this is a timing problem",
      "Feed more dilute (1:8:8) to stretch peak time overnight",
      "Cooler spot also delays the peak",
      "Bake at 2x mark next time: set a jar alarm at 1.8x"]),
    (["smells like alcohol", "boozy"],
     "ACID/ALCOHOL ACCUMULATION",
     ["Discard down to 10g, feed 1:5:5, keep at 24C",
      "Repeat 12-hourly until aroma turns creamy/yogurt",
      "Long-term: larger feeds, shorter warm gaps"]),
    (["bubbles but no rise", "small bubbles"],
     "EARLY DAYS or weak gluten network",
     ["Young starters (day 3-5) bubble before they rise; keep feeding",
      "Switch feeds to 50/50 white+whole grain for structure",
      "True rise usually arrives day 5-7 at 24-26C",
      "If >10 days without rise: restart with pineapple-juice method (pH control)"]),
    (["died", "dead", "gone"],
     "CHECK BEFORE FUNERAL",
     ["Very few things actually kill a starter: heat >45C, mold, soap residue",
      "Chill/hibernation/stress look like death but revive in 2-3 cycles",
      "Keep 1 tbsp even from a bad jar — recovery odds are high"]),
    (["too sour", "tangy", "acidic bread"],
     "ACETIC PHASE DOMINANT",
     ["Feed 1:10:10 (more dilute), keep warmer (26C) — shifts to lactic/mild",
      "Stiff cold levain = MORE tang; warm liquid = less",
      "Shorten time between feeds"]),
]


def cmd_diagnose(a):
    q = a.symptom.lower()
    for kws, cause, steps in DIAG:
        if any(k in q for k in kws):
            print(f"Symptom: {a.symptom}")
            print(f"Likely cause: {cause}")
            print("Recovery protocol:")
            for i, s in enumerate(steps, 1):
                print(f"  {i}. {s}")
            return
    print(f"Symptom '{a.symptom}' not in table.")
    print("Describe with: rise behavior, smell, appearance, temperature, feeding gap.")
    print("Run `feed --temp` to reset a sane baseline first.")


def cmd_vacation(a):
    w = a.weeks
    print(f"Vacation plan for {w} week(s):")
    if w <= 2:
        print("  FRIDGE: feed 1:2:2, sit 2 h at room temp, refrigerate.")
        print("  Revival on return: 1:1:1 every 12 h; doubling by cycle 2-3.")
        print("  First bake-ready: ~48 h after return.")
    elif w <= 6:
        print("  FRIDGE DEEP: feed 1:2:2, room temp 2 h, chill in the BACK")
        print("  (coldest zone). Expect serious hooch on return — normal.")
        print("  Revival: pour off hooch, 1:1:1 twice a day; allow 2-3 days.")
        print("  Backup: dry chips (below) — flour is cheaper than heartbreak.")
    else:
        print("  DRY CHIPS: spread 100g thin starter on parchment, dry 24-48 h")
        print("  to glass-hard chips, store airtight in a dark jar (months-years).")
        print("  Revival: soak 10 chips in 50g water 2 h, +50g flour,")
        print("  feed 12-hourly — bubbling day 2, doubling day 3-5.")
        print("  Also keep the fridge jar as belt-and-suspenders.")
    print()
    print("Universal rule: name a fridge-sitter or accept the dry-chip route;")
    print("starters forgive neglect far better than heat or mold.")


def cmd_levain(a):
    bake = datetime.strptime(a.bake, "%H:%M")
    ph = peak_hours(a.temp, 5)
    # 1:1:5 build peaks slightly faster than 1:5:5 (more inoculum)
    build_peak = ph * 0.75
    start = bake - timedelta(hours=build_peak)
    mix_time = start
    print(f"Bake (mix dough) at {a.bake}, kitchen {a.temp}C:")
    print(f"  Build levain 1:1:5 (20g starter + 20g flour + 100g water)")
    print(f"  START the build at {start.strftime('%H:%M')} "
          f"(peak ~{build_peak:.1f} h later)")
    print(f"  Use levain at peak (domed, 2-2.5x) — i.e. right at {a.bake} mixing.")
    print()
    print("  Evening alternative: 1:2:4 before bed at 20-21C peaks in ~10-12 h")
    print("  for a morning bake; mark the jar and trust the mark over the clock.")


def main():
    p = argparse.ArgumentParser(description="Sourdough starter management tool.")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("feed"); s.add_argument("--temp", type=float, required=True, help="C where jar lives"); s.add_argument("--style", choices=["liquid", "stiff"], default="liquid"); s.set_defaults(f=cmd_feed)
    s = sub.add_parser("hydration"); s.add_argument("--have", type=float, required=True); s.add_argument("--target", type=float, required=True); s.add_argument("--mass", type=float, default=200); s.set_defaults(f=cmd_hydration)
    s = sub.add_parser("readiness"); s.add_argument("--temp", type=float, required=True); s.add_argument("--ratio", type=float, default=5); s.set_defaults(f=cmd_readiness)
    s = sub.add_parser("diagnose"); s.add_argument("--symptom", required=True); s.set_defaults(f=cmd_diagnose)
    s = sub.add_parser("vacation"); s.add_argument("--weeks", type=float, required=True); s.set_defaults(f=cmd_vacation)
    s = sub.add_parser("levain"); s.add_argument("--bake", required=True, help="HH:MM dough-mix time"); s.add_argument("--temp", type=float, default=24); s.set_defaults(f=cmd_levain)
    a = p.parse_args(); a.f(a)


if __name__ == "__main__":
    import sys
    try:
        main()
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass
