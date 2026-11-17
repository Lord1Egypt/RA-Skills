#!/usr/bin/env python3
"""PTO Maximizer — turn N vacation days into maximum long weekends.

Computes public holidays for US/UK/DE/FR (fixed + Easter-based + observance
shifts), generates every PTO bridge candidate around holidays and weekends,
scores each by efficiency (consecutive days off per PTO day), and greedily
builds an annual plan within a budget with quarter-balancing. Exports ICS.

stdlib only. No network.
"""
import argparse
import datetime as dt
import json
import sys

D = dt.date

# ----------------------------- holidays -----------------------------------

def easter(year: int) -> D:
    """Anonymous Gregorian algorithm."""
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return D(year, month, day)


def nth_weekday(year, month, weekday, n):
    """nth <weekday> (Mon=0) of month; n=-1 = last."""
    if n == -1:
        d = D(year, month + 1, 1) - dt.timedelta(days=1) if month < 12 else D(year, 12, 31)
        while d.weekday() != weekday:
            d -= dt.timedelta(days=1)
        return d
    d = D(year, month, 1)
    while d.weekday() != weekday:
        d += dt.timedelta(days=1)
    return d + dt.timedelta(weeks=n - 1)


def observed_us(d: D) -> D:
    """US federal observance: Sat -> Fri before, Sun -> Mon after."""
    if d.weekday() == 5:
        return d - dt.timedelta(days=1)
    if d.weekday() == 6:
        return d + dt.timedelta(days=1)
    return d


def holidays(country: str, year: int):
    """Return {date: name} of observed public holidays."""
    E = easter(year)
    hd = {}

    def add(d, name, shift_us=False):
        if shift_us and country == "US":
            d = observed_us(d)
        if d.year == year:
            hd[d] = name

    if country == "US":
        add(D(year, 1, 1), "New Year's Day", shift_us=True)
        add(nth_weekday(year, 1, 0, 3), "MLK Day")
        add(nth_weekday(year, 2, 0, 3), "Presidents' Day")
        add(nth_weekday(year, 5, 0, -1), "Memorial Day")
        add(D(year, 6, 19), "Juneteenth", shift_us=True)
        add(D(year, 7, 4), "Independence Day", shift_us=True)
        add(nth_weekday(year, 9, 0, 1), "Labor Day")
        add(nth_weekday(year, 10, 0, 2), "Columbus Day")
        add(D(year, 11, 11), "Veterans Day", shift_us=True)
        add(nth_weekday(year, 11, 3, 4), "Thanksgiving")
        add(D(year, 12, 25), "Christmas Day", shift_us=True)
    elif country == "UK":
        def bank(d, name):
            # substitution: weekend -> next Monday
            while d.weekday() >= 5:
                d += dt.timedelta(days=1)
            hd[d] = name
        bank(D(year, 1, 1), "New Year's Day")
        bank(D(year, 1, 1) + dt.timedelta(days=1) if D(year, 1, 1).weekday() == 5 else nth_weekday(year, 1, 0, 1), "2 Jan (sub)")
        # Good Friday / Easter Monday
        hd[E - dt.timedelta(days=2)] = "Good Friday"
        hd[E + dt.timedelta(days=1)] = "Easter Monday"
        bank(nth_weekday(year, 5, 0, 1), "Early May Bank Holiday")
        bank(nth_weekday(year, 5, 0, -1), "Spring Bank Holiday")
        bank(nth_weekday(year, 8, 0, -1), "Summer Bank Holiday")
        bank(D(year, 12, 25), "Christmas Day")
        bank(D(year, 12, 26), "Boxing Day")
    elif country == "DE":
        hd[D(year, 1, 1)] = "Neujahr"
        hd[E - dt.timedelta(days=2)] = "Karfreitag"
        hd[E + dt.timedelta(days=1)] = "Ostermontag"
        hd[D(year, 5, 1)] = "Tag der Arbeit"
        hd[E + dt.timedelta(days=39)] = "Christi Himmelfahrt"
        hd[E + dt.timedelta(days=50)] = "Pfingstmontag"
        hd[D(year, 10, 3)] = "Tag der Deutschen Einheit"
        hd[D(year, 12, 25)] = "1. Weihnachtstag"
        hd[D(year, 12, 26)] = "2. Weihnachtstag"
    elif country == "FR":
        hd[D(year, 1, 1)] = "Jour de l'An"
        hd[E - dt.timedelta(days=2)] = "Vendredi Saint"  # Alsace/Moselle only, kept informational
        hd[E + dt.timedelta(days=1)] = "Lundi de Pâques"
        hd[D(year, 5, 1)] = "Fête du Travail"
        hd[D(year, 5, 8)] = "Victoire 1945"
        hd[E + dt.timedelta(days=39)] = "Ascension"
        hd[E + dt.timedelta(days=50)] = "Pentecôte"
        hd[D(year, 7, 14)] = "Fête Nationale"
        hd[D(year, 8, 15)] = "Assomption"
        hd[D(year, 11, 1)] = "Toussaint"
        hd[D(year, 11, 11)] = "Armistice"
        hd[D(year, 12, 25)] = "Noël"
    else:
        sys.exit(f"country '{country}' not in US/UK/DE/FR")
    return hd


# ----------------------------- bridges -------------------------------------

def weekends_free(d: D) -> bool:
    return d.weekday() >= 5


def expand_run(start: D, off_days: set, holidays_set: set):
    """Longest consecutive run of off days containing start."""
    # walk back
    s = start
    while (s - dt.timedelta(days=1)) in off_days or (s - dt.timedelta(days=1)) in holidays_set or weekends_free(s - dt.timedelta(days=1)):
        s -= dt.timedelta(days=1)
    e = start
    nxt = lambda x: x + dt.timedelta(days=1)
    while (nxt(e) in off_days) or (nxt(e) in holidays_set) or weekends_free(nxt(e)):
        e = nxt(e)
    return s, e


def build_bridges(hd: dict, year: int):
    """Generate bridge candidates: for each holiday, try bridging PTO days
    before/after (1-4 days each side), compute consecutive-off run."""
    cands = []
    hdates = sorted(hd)
    for h in hdates:
        for pre in range(0, 4):        # PTO days before holiday
            for post in range(0, 4):   # PTO days after holiday
                if pre + post == 0 or pre + post > 4:
                    continue
                pto = set()
                ok = True
                for i in range(1, pre + 1):
                    d = h - dt.timedelta(days=i)
                    if d.year != year or d.weekday() >= 5 or d in hd:
                        ok = False
                        break
                    pto.add(d)
                if not ok:
                    continue
                for i in range(1, post + 1):
                    d = h + dt.timedelta(days=i)
                    if d.year != year or d.weekday() >= 5 or d in hd:
                        ok = False
                        break
                    pto.add(d)
                if not ok:
                    continue
                s, e = expand_run(h, pto, set(hdates))
                run = (e - s).days + 1
                eff = run / len(pto)
                cands.append({
                    "holiday": hd[h], "holiday_date": h.isoformat(),
                    "pto_days": sorted(d.isoformat() for d in pto),
                    "run_start": s.isoformat(), "run_end": e.isoformat(),
                    "consecutive_off": run, "pto_count": len(pto),
                    "efficiency": round(eff, 2),
                })
    # dedupe by identical PTO sets
    seen = {}
    for c in cands:
        key = tuple(c["pto_days"])
        if key not in seen or c["efficiency"] > seen[key]["efficiency"]:
            seen[key] = c
    return sorted(seen.values(), key=lambda c: (-c["efficiency"], -c["consecutive_off"]))


def overlaps(a_dates: list, taken: set) -> bool:
    return any(d in taken for d in a_dates)


def plan(bridges, budget: int, min_eff: float, year: int, quarter_cap: float = 0.45):
    taken = set()
    claimed_runs = set()
    chosen = []
    q_spend = {1: 0, 2: 0, 3: 0, 4: 0}
    total_budget = budget
    for c in bridges:
        if c["efficiency"] < min_eff:
            continue
        n = c["pto_count"]
        if n > budget:
            continue
        run_days = set()
        d = dt.date.fromisoformat(c["run_start"])
        e = dt.date.fromisoformat(c["run_end"])
        while d <= e:
            run_days.add(d.isoformat())
            d += dt.timedelta(days=1)
        if overlaps(c["pto_days"], taken) or run_days & claimed_runs:
            continue
        # quarter balance: don't exceed cap of TOTAL budget per quarter
        q = (dt.date.fromisoformat(c["holiday_date"]).month - 1) // 3 + 1
        if q_spend[q] + n > total_budget * quarter_cap and total_budget >= 6:
            continue
        chosen.append(c)
        taken.update(c["pto_days"])
        claimed_runs.update(run_days)
        q_spend[q] += n
        budget -= n
        if budget <= 0:
            break
    return chosen, budget, q_spend


BLACKOUTS = {
    "US": [("Nov 15 – Dec 26", "retail/logistics Q4 freeze; corporate EYC crunch")],
    "UK": [("late Jul – Aug", "school-holiday peak pricing; office skeleton crews (good for time off, bad for deals)")],
    "DE": [("Dec 20 – Jan 5", "Betriebsferien common in industry")],
    "FR": [("Aug", "tout fermé — great for vacation, book early")],
}


def ics_export(chosen, path, year):
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//pto-maximizer//EN"]
    for i, c in enumerate(chosen):
        for d in c["pto_days"]:
            dd = dt.date.fromisoformat(d)
            lines += ["BEGIN:VEVENT",
                      f"UID:pto-{year}-{i}-{d}@pto-maximizer",
                      f"DTSTAMP:{year}0101T000000Z",
                      f"DTSTART;VALUE=DATE:{dd.strftime('%Y%m%d')}",
                      f"DTEND;VALUE=DATE:{(dd + dt.timedelta(days=1)).strftime('%Y%m%d')}",
                      f"SUMMARY:PTO (bridge: {c['holiday']}, {c['consecutive_off']} days off)",
                      "END:VEVENT"]
        s = dt.date.fromisoformat(c["run_start"])
        e = dt.date.fromisoformat(c["run_end"])
        lines += ["BEGIN:VEVENT",
                  f"UID:pto-off-run-{year}-{i}@pto-maximizer",
                  f"DTSTAMP:{year}0101T000000Z",
                  f"DTSTART;VALUE=DATE:{s.strftime('%Y%m%d')}",
                  f"DTEND;VALUE=DATE:{(e + dt.timedelta(days=1)).strftime('%Y%m%d')}",
                  f"SUMMARY:OFF {c['consecutive_off']} days ({c['holiday']} bridge)",
                  "TRANSP:TRANSPARENT",
                  "END:VEVENT"]
    lines.append("END:VCALENDAR")
    with open(path, "w") as f:
        f.write("\r\n".join(lines) + "\r\n")
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--country", default="US", choices=["US", "UK", "DE", "FR"])
    ap.add_argument("--year", type=int, required=True)
    ap.add_argument("--budget", type=int, required=True, help="PTO days available")
    ap.add_argument("--min-eff", type=float, default=2.0, help="min efficiency (off-days per PTO day)")
    ap.add_argument("--reserve-summer", type=int, default=0,
                    help="hold this many days out of the greedy plan (for a real week off)")
    ap.add_argument("--ics", help="export chosen plan to an .ics file")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    hd = holidays(args.country, args.year)
    bridges = build_bridges(hd, args.year)

    budget = args.budget - args.reserve_summer
    chosen, remaining, q_spend = plan(bridges, budget, args.min_eff, args.year)

    total_off = sum(c["consecutive_off"] for c in chosen)
    total_pto = sum(c["pto_count"] for c in chosen)

    if args.json:
        print(json.dumps({
            "country": args.country, "year": args.year,
            "budget": args.budget, "reserved_summer": args.reserve_summer,
            "holidays": {d.isoformat(): n for d, n in sorted(hd.items())},
            "plan": chosen,
            "pto_used": total_pto,
            "unallocated": remaining + args.reserve_summer,
            "quarter_spend": q_spend,
            "blackouts": BLACKOUTS.get(args.country, []),
        }, indent=2))
        if args.ics:
            ics_export(chosen, args.ics, args.year)
        return 0

    print(f"\n===== PTO PLAN {args.country} {args.year} — budget {args.budget} days "
          f"(reserved {args.reserve_summer} for a real week) =====\n")
    print("Public holidays:")
    for d, n in sorted(hd.items()):
        print(f"  {d.isoformat()} {d.strftime('%a')}  {n}")
    print(f"\nChosen bridges (min efficiency {args.min_eff}):")
    for c in chosen:
        ps = ", ".join(dt.date.fromisoformat(x).strftime("%b %d") for x in c["pto_days"])
        print(f"  {c['run_start']} → {c['run_end']}  {c['consecutive_off']:2d} days off  "
              f"[{c['pto_count']} PTO: {ps}]  eff {c['efficiency']:.1f}  ({c['holiday']})")
    print(f"\nTOTAL: {total_pto} PTO days → {total_off} consecutive days off "
          f"(avg eff {total_off/max(total_pto,1):.1f})")
    print(f"Quarter spend: " + ", ".join(f"Q{k}={v}" for k, v in q_spend.items()))
    print(f"Unallocated: {remaining + args.reserve_summer} days (reserve + leftovers)")
    if args.country in BLACKOUTS:
        print("Blackout notes:")
        for w, why in BLACKOUTS[args.country]:
            print(f"  ! {w}: {why}")
    if args.ics:
        ics_export(chosen, args.ics, args.year)
        print(f"\nICS written: {args.ics}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
