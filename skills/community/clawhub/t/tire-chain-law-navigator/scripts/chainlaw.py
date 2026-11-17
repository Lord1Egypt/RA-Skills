#!/usr/bin/env python3
"""chainlaw.py — winter traction-law verdicts by route, date, and vehicle.

Subcommands:
  routes     list known corridors with jurisdiction + season
  check      verdict for route+date+vehicle (+--conditions)
  equipment  traction-device legality primer by jurisdiction
  dashcard   printable glovebox card

Stdlib only. Knowledge base is curated (see references/traction-laws.md);
ALWAYS confirm with the live info line on travel day.
"""
import argparse
import datetime as dt
import sys
from pathlib import Path

# season: (start_month, start_day, end_month, end_day)
CORRIDORS = {
    "i70-co": {
        "name": "I-70 Colorado mountain corridor (Dotsero-Morrison)",
        "jurisdiction": "Colorado, USA",
        "season": (9, 1, 5, 31),
        "escalation": ["Traction Law (Code 15)", "Passenger Vehicle Chain Law (Code 16)"],
        "info": "CDOT: cotrip.org / dial 511",
        "fine": "$130 violation; ~$650+ if you spin out and block the road",
    },
    "donner-i80": {
        "name": "I-80 Donner Pass (Sacramento-Reno)",
        "jurisdiction": "California, USA",
        "season": (10, 1, 5, 31),
        "escalation": ["R1", "R2", "R3"],
        "info": "Caltrans QuickMap / 1-800-427-7623",
        "fine": "~$100+; $1,000+ if you crash or block (obstruction added)",
    },
    "snoqualmie-i90": {
        "name": "I-90 Snoqualmie Pass (Seattle-Ellensburg)",
        "jurisdiction": "Washington, USA",
        "season": (11, 1, 3, 31),
        "escalation": ["advisory", "chains except AWD+snows", "chains ALL vehicles"],
        "info": "WSDOT wsdot.com/traffic/passes / dial 511",
        "fine": "up to $500 (negligent driving, common charge)",
    },
    "coquihalla-bc": {
        "name": "BC-5 Coquihalla (Hope-Kamloops)",
        "jurisdiction": "British Columbia, Canada",
        "season": (10, 1, 4, 30),
        "escalation": ["winter-tire mandate", "chain-up when posted"],
        "info": "DriveBC drivebc.ca / 1-800-550-4997",
        "fine": "$157-$595",
    },
    "alps-fr-it": {
        "name": "Alpine crossings France-Italy (Mont Blanc/Frejus approach)",
        "jurisdiction": "France / Italy",
        "season": (11, 1, 3, 31),
        "escalation": ["sign 267 chains mandatory", "closure"],
        "info": "FR bison-fute.gouv.fr / IT autostrade.it",
        "fine": "FR ~135 EUR; IT ~80-318 EUR",
    },
    "grand-canyon-az": {
        "name": "AZ-64 / US-180 Grand Canyon South Rim",
        "jurisdiction": "Arizona, USA (NPS)",
        "season": (11, 1, 4, 15),
        "escalation": ["carry advisory", "chains required all vehicles"],
        "info": "NPS road status line / nps.gov/grca",
        "fine": "federal citation",
    },
}

VEHICLES = {
    "fwd-snows": {"drive": "fwd", "snow_tires": True, "awd": False,
                  "label": "FWD car with 3PMSF/M+S snow tires"},
    "rwd-allseason": {"drive": "rwd", "snow_tires": False, "awd": False,
                      "label": "RWD car with all-season tires"},
    "awd-snows": {"drive": "awd", "snow_tires": True, "awd": True,
                  "label": "AWD/4WD with snow-rated tires"},
    "awd-allseason": {"drive": "awd", "snow_tires": False, "awd": False,
                      "label": "AWD with all-season tires"},
    "cmv-truck": {"drive": "cmv", "snow_tires": True, "awd": False,
                  "label": "Commercial vehicle (CMV)"},
}

EQUIPMENT = {
    "California": {
        "link chains": "legal, gold standard",
        "cable chains": "legal for passenger vehicles (mind clearance)",
        "autosock": "not listed as chain substitute for cars - risky at R2/R3",
        "studded": "legal Nov 1 - Apr 30 (verify current law)",
    },
    "Colorado": {
        "link chains": "legal",
        "cable chains": "legal",
        "autosock": "accepted alternative under Traction Law and PV Chain Law",
        "studded": "legal year-round",
    },
    "Washington/Oregon": {
        "link chains": "legal",
        "cable chains": "legal",
        "autosock": "approved on some WA routes (WAC list - check)",
        "studded": "legal Nov 1 - Mar 31",
    },
    "British Columbia": {
        "link chains": "legal; commercial carry mandate Nov-Apr",
        "cable chains": "legal for many classes",
        "autosock": "accepted alternative on many routes (verify class)",
        "studded": "legal Oct 1 - Apr 30",
    },
    "France": {
        "metal chains": "chaunes metalliques accepted; textiles too",
        "carry law": "prefecture carry orders in mountain depts (Nov-Mar)",
        "studded": "banned (tiny exceptions)",
    },
    "Italy": {
        "chains or winter tires": "equivalent Nov 15 - Apr 15 on signed roads",
        "studded": "legal with limits/regional bans",
    },
}


def season_str(season):
    sm, sd, em, ed = season
    return "%02d-%02d to %02d-%02d" % (sm, sd, em, ed)


def in_season(season, month, day):
    sm, sd, em, ed = season
    if sm <= em:
        return (sm, sd) <= (month, day) <= (em, ed)
    return (month, day) >= (sm, sd) or (month, day) <= (em, ed)


def cmd_routes(args):
    print("%-16s %-48s %-26s %s" % ("ID", "CORRIDOR", "JURISDICTION", "SEASON"))
    for rid, c in CORRIDORS.items():
        print("%-16s %-48s %-26s %s" % (
            rid, c["name"][:48], c["jurisdiction"][:26], season_str(c["season"])))
    print("\nVerdicts: chainlaw.py check --route <id> --date YYYY-MM-DD "
          "--vehicle <class> [--conditions active]")
    return 0


def cmd_check(args):
    c = CORRIDORS.get(args.route)
    if c is None:
        print("Unknown route '%s'. Known: %s" % (args.route, ", ".join(CORRIDORS)))
        return 2
    v = VEHICLES[args.vehicle]

    d = dt.date.fromisoformat(args.date)
    seasonal = in_season(c["season"], d.month, d.day)
    ladder = c.get("escalation", [])

    cond = args.conditions or "none"
    if cond == "none":
        level = "none"
    elif cond in ("active", "r1", "traction"):
        level = ladder[0] if ladder else "Traction requirement"
    elif cond in ("severe", "r2", "r3", "chainlaw"):
        level = ladder[-1] if ladder else "Chains required"
    elif cond == "sign267":
        level = "sign 267 - chains mandatory"
    else:
        level = "unknown"

    print("Route       : %s (%s)" % (c["name"], c["jurisdiction"]))
    print("Date        : %s -> %s" % (d.isoformat(),
          "IN snow/chain season" if seasonal else "OUTSIDE typical season"))
    print("Vehicle     : %s" % v["label"])
    print("Conditions  : %s -> level '%s'" % (cond, level))
    print("")

    if not seasonal:
        print("VERDICT: out of season - no traction law expected on this corridor.")
        print("Still carry chains if snow is in the forecast; mountain weather shifts.")
        print("Live info: %s" % c["info"])
        return 0

    if level == "none":
        may = "YES"
        need = "carry chains in the vehicle (season base requirement)"
    elif level in ("R1", "Traction Law (Code 15)"):
        if v["snow_tires"] or v["awd"]:
            may = "YES - snow tires / AWD satisfy R1 / CO Traction Law"
            need = "carry chains anyway; checkpoints appear fast"
        else:
            may = "NO - install chains first (all-seasons fail R1 / CO Code 15)"
            need = "chains on drive axle"
    elif level == "R2":
        if v["awd"] and v["snow_tires"]:
            may = "YES - AWD + snow-rated tires pass R2"
            need = "carry chains; R3 has no exemptions"
        else:
            may = "NO - chains on drive axle required for 2WD"
            need = "chains installed on drive axle"
    elif level in ("R3", "Passenger Vehicle Chain Law (Code 16)",
                   "chains ALL vehicles", "sign 267 - chains mandatory",
                   "chain-up when posted"):
        may = "NO unless chains fitted - no AWD exemption at this level"
        need = "chains on drive axle (all four if manual/clearance allow)"
    else:
        may = "check checkpoint signage / info line"
        need = "chains carried at minimum"

    print("== VERDICT ==")
    print("You may pass : %s" % may)
    print("Required     : %s" % need)
    print("Fine exposure: %s" % c.get("fine", "varies"))
    print("Ladder       : %s" % " -> ".join(ladder))
    print("Live info    : %s  <- confirm on travel day" % c["info"])
    return 0


def cmd_equipment(args):
    v = VEHICLES[args.vehicle]
    print("Vehicle: %s | clearance: %s\n" % (v["label"], args.clearance))
    print("Device legality by jurisdiction (verify current year):\n")
    for j, devs in EQUIPMENT.items():
        print("%s:" % j)
        for dev, note in devs.items():
            print("  - %-24s %s" % (dev, note))
        print()
    print("Sizing: chains must match the tire spec printed on your sidewall.")
    if args.clearance == "tight":
        print("TIGHT clearance: prefer cable / low-profile chains; some AWD")
        print("vehicles prohibit chains entirely - check the owner's manual.")
    print("Speed on chains: 25-30 mph (30-50 km/h). Re-tighten after 0.5 mile.")
    return 0


def cmd_dashcard(args):
    routes = [r.strip() for r in args.routes.split(",") if r.strip()]
    v = VEHICLES[args.vehicle]
    lines = ["# WINTER DRIVE DASH-CARD", "",
             "Vehicle: %s" % v["label"],
             "Trip date: ______________", ""]
    for rid in routes:
        c = CORRIDORS.get(rid)
        if c is None:
            lines.append("(!) unknown route id: %s" % rid)
            lines.append("")
            continue
        lines += [
            "## %s" % c["name"],
            "Jurisdiction: %s" % c["jurisdiction"],
            "Season: %s" % season_str(c["season"]),
            "Ladder: %s" % " -> ".join(c.get("escalation", [])),
            "Fines : %s" % c.get("fine", ""),
            "Live  : %s" % c["info"],
            "If stopped: window down, hands visible, state your tire/chain setup.",
            "",
        ]
    lines += [
        "## UNIVERSAL",
        "- Chains: 25-30 mph max; re-tighten after half a mile.",
        "- Install ONLY in signed chain-up zones, never on a live lane.",
        "- AWD helps you go, not stop. R3 / PV Chain Law: NO exemptions.",
        "- Practice fitting chains in a dry garage before the trip.",
        "",
    ]
    text = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(text + "\n")
        print("Dash-card -> %s" % args.out)
    else:
        print(text)
    return 0


def main():
    ap = argparse.ArgumentParser(description="Winter traction-law navigator.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("routes", help="list corridors")
    r.set_defaults(func=cmd_routes)

    ch = sub.add_parser("check", help="verdict for route+date+vehicle")
    ch.add_argument("--route", required=True)
    ch.add_argument("--date", required=True, help="YYYY-MM-DD")
    ch.add_argument("--vehicle", required=True, choices=list(VEHICLES))
    ch.add_argument("--conditions", default="none",
                    choices=["none", "active", "r1", "traction",
                             "severe", "r2", "r3", "chainlaw", "sign267"])
    ch.set_defaults(func=cmd_check)

    eq = sub.add_parser("equipment", help="device legality primer")
    eq.add_argument("--vehicle", default="fwd-snows", choices=list(VEHICLES))
    eq.add_argument("--clearance", default="normal",
                    choices=["tight", "normal", "roomy"])
    eq.set_defaults(func=cmd_equipment)

    dc = sub.add_parser("dashcard", help="printable glovebox card")
    dc.add_argument("--routes", required=True, help="comma-separated route ids")
    dc.add_argument("--vehicle", required=True, choices=list(VEHICLES))
    dc.add_argument("--out", help="write to file")
    dc.set_defaults(func=cmd_dashcard)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
