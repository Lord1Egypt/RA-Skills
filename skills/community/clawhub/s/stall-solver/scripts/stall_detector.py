#!/usr/bin/env python3
"""stall_detector.py - toilet stall / urinal demand vs supply analyzer.

Modes:
  demand - expected simultaneous demand for a venue + duration
  event  - simulate an event (peak arrival math: halftime, session break)
  audit  - fixture-count adequacy verdict from code minimums + queuing

Model: Poisson arrivals, expected queue via M/M/c-lite approximation
(Erlang-C is overkill; we use a utilization-based waiting estimate).
Fixture minimums follow International Plumbing Code (IPC) tables and
IAPMO/UPC occupancy buckets for business/assembly classifications.

Zero dependencies (Python 3.8+ stdlib).
"""
import argparse
import json
import math
import sys

# ------------------------------------------------- usage rates
# bladder-driven urinal visits per attendee per hour (event-tuned)
VISITS_PER_HOUR = {
    "conference": 0.35,
    "concert": 0.45,
    "sports": 0.50,
    "festival": 0.55,
    "theater": 0.30,
    "wedding": 0.40,
    "school-day": 0.30,
    "office": 0.25,
}

# median seconds a fixture is occupied per visit
OCCUPANCY_SEC = {
    "urinal": 35,
    "stall": 95,
    "sink": 20,
}

# split of restroom demand male/female (unisex venues: all stalls)
DEFAULT_FEMALE_SHARE = 0.5

# ------------------------------------------------- code minimums (IPC-style)
# occupancy bucket -> (water closets female, wc male + urinals, lavs)
# simplified assembly/business tables; always verify against the local
# adopted code edition and amendments.
IPC_ASSEMBLY = [
    # (occupants, female WC, male WC, male urinals, lavs F, lavs M)
    (25, 1, 1, 1, 1, 1),
    (50, 2, 1, 1, 1, 1),
    (75, 3, 2, 1, 2, 2),
    (100, 4, 2, 1, 2, 2),
    (150, 6, 3, 2, 3, 3),
    (250, 8, 4, 3, 4, 4),
    (400, 12, 6, 4, 6, 5),
    (600, 16, 8, 6, 8, 7),
    (800, 20, 10, 8, 10, 8),
    (1200, 30, 15, 12, 15, 12),
]

VENUE_CLASS = {
    "conference": "assembly",
    "concert": "assembly",
    "sports": "assembly",
    "festival": "assembly",
    "theater": "assembly",
    "wedding": "assembly",
    "school-day": "business",
    "office": "business",
}


def code_minimum(occupancy, cls="assembly"):
    table = IPC_ASSEMBLY  # business uses same ladder shifted; see note
    prev = table[0]
    for row in table:
        if occupancy <= row[0]:
            return row
        prev = row
    # scale linearly beyond table
    base_occ, f_wc, m_wc, m_ur, f_lav, m_lav = prev
    over = occupancy - base_occ
    return (occupancy,
            f_wc + int(over / 100) + 1,
            m_wc + int(over / 200) + 1,
            m_ur + int(over / 200) + 1,
            f_lav + int(over / 150) + 1,
            m_lav + int(over / 150) + 1)


def erlang_c_wait(lam, mu, c):
    """Approximate expected wait (sec) in M/M/c.

    lam = arrivals/sec, mu = service rate 1/sec per fixture,
    c = fixtures. Returns float('inf') if unstable (rho >= 1).
    """
    rho = lam / (c * mu)
    if rho >= 1.0:
        return float("inf")
    # Erlang-B recursion then Erlang-C
    b = 1.0
    for k in range(1, c + 1):
        b = (b * (lam / mu) / k) / (1 + b * (lam / mu) / k)
    pw = b * c * mu / (c * mu - lam)  # Erlang-C probability of waiting
    wq = pw / (c * mu - lam)
    return wq


def fmt_wait(sec):
    if sec == float("inf") or math.isnan(sec):
        return "OVERLOAD"
    if sec < 90:
        return "%.0f sec" % sec
    return "%.1f min" % (sec / 60.0)


# ------------------------------------------------- modes
def cmd_demand(args):
    venue = args.venue
    if venue not in VISITS_PER_HOUR:
        sys.exit("unknown venue %r; choose: %s" %
                 (venue, ", ".join(sorted(VISITS_PER_HOUR))))
    visits = VISITS_PER_HOUR[venue]
    n = args.attendees
    fem = n * args.female_share
    mal = n * (1 - args.female_share)
    print("Venue profile: %s (%s)" % (venue, VENUE_CLASS[venue]))
    print("Attendees: %d  (F %.0f / M %.0f)" % (n, fem, mal))
    print("Visit rate: %.2f visits/person/hr" % visits)
    print()
    for fixture, share, users in (("stall", 1.0, fem), ("urinal", 1.0, mal)):
        if fixture == "stall" and args.unisex:
            users = n  # unisex: everyone needs a stall
        occ = OCCUPANCY_SEC[fixture]
        lam = users * visits / 3600.0  # visits/sec sustained
        c = args.fixtures if fixture != "urinal" else args.urinals
        if fixture == "stall" and args.unisex:
            c = args.fixtures  # all stalls
        if c <= 0:
            print("%-7s: 0 fixtures -> cannot serve demand" % fixture)
            continue
        wq = erlang_c_wait(lam, 1.0 / occ, c)
        rho = lam / (c * (1.0 / occ))
        print("%-7s: %2d fixtures | utilization %.0f%% | avg wait %s"
              % (fixture, c, rho * 100, fmt_wait(wq)))
    return 0


def cmd_event(args):
    """Peak burst: a fraction of attendees hit the restroom at T-0."""
    venue = args.venue
    burst_share = args.burst_share
    n_burst = args.attendees * burst_share
    fem = n_burst * args.female_share
    mal = n_burst * (1 - args.female_share)
    window = args.window_min * 60.0
    print("Event break: %.0f%% of %d attendees over %d min = %.0f people"
          % (burst_share * 100, args.attendees, args.window_min, n_burst))
    print()
    ok = True
    for fixture, users in (("stall", fem), ("urinal", mal)):
        c = args.fixtures if fixture == "stall" else args.urinals
        occ = OCCUPANCY_SEC[fixture]
        if c == 0:
            print("%-7s: none installed -> %.0f users overflow" % (fixture, users))
            ok = False
            continue
        lam = users / window
        # how long until the burst clears
        service_cap = c * window / occ  # visits serviceable in window
        clear_time = users * occ / c  # sec to drain everyone
        rho = lam / (c / occ)
        wq = erlang_c_wait(lam, 1.0 / occ, c)
        verdict = "OK" if rho < 0.8 else ("TIGHT" if rho < 1 else "FAIL")
        if rho >= 0.8:
            ok = False
        print("%-7s: %2d fixtures | burst utilization %.0f%% | "
              "avg wait %s | drains in %.1f min | %s"
              % (fixture, c, rho * 100, fmt_wait(wq), clear_time / 60, verdict))
    if not ok:
        print("\nVERDICT: expect queues. Add fixtures or stagger the break.")
    else:
        print("\nVERDICT: burst is serviceable.")
    return 0


def cmd_audit(args):
    """Fixture count vs code minimum + queue check."""
    occ = args.occupancy
    row = code_minimum(occ, VENUE_CLASS[args.venue])
    _, f_wc_min, m_wc_min, m_ur_min, f_lav_min, m_lav_min = row
    print("Code audit for occupancy %d (%s class)" % (occ, VENUE_CLASS[args.venue]))
    print()
    checks = [
        ("female water closets", args.f_wc, f_wc_min),
        ("male water closets", args.m_wc, m_wc_min),
        ("male urinals", args.m_ur, m_ur_min),
        ("female lavatories", args.f_lav, f_lav_min),
        ("male lavatories", args.m_lav, m_lav_min),
    ]
    deficit_total = 0
    for name, have, need in checks:
        if have is None:
            print("%-22s: not supplied (skipped)" % name)
            continue
        d = need - have
        if d > 0:
            deficit_total += d
            print("%-22s: %d provided / %d required  -> SHORT %d"
                  % (name, have, need, d))
        else:
            print("%-22s: %d provided / %d required  -> OK" % (name, have, need))
    if deficit_total:
        print("\nVERDICT: BELOW code minimum by %d fixtures total." % deficit_total)
        print("Fix before occupancy permit; verify against local amendments.")
    else:
        print("\nVERDICT: meets or exceeds table minimums (queue behavior "
              "is a separate check - see `demand`).")
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="mode", required=True)

    sp = sub.add_parser("demand", help="sustained demand profile")
    sp.add_argument("--venue", required=True, choices=sorted(VISITS_PER_HOUR))
    sp.add_argument("--attendees", type=int, required=True)
    sp.add_argument("--fixtures", type=int, required=True, help="stalls (all-gender or female)")
    sp.add_argument("--urinals", type=int, default=0)
    sp.add_argument("--female-share", type=float, default=DEFAULT_FEMALE_SHARE)
    sp.add_argument("--unisex", action="store_true",
                    help="all-restrooms-stalls venue")
    sp.set_defaults(func=cmd_demand)

    sp = sub.add_parser("event", help="burst event simulation")
    sp.add_argument("--venue", required=True, choices=sorted(VISITS_PER_HOUR))
    sp.add_argument("--attendees", type=int, required=True)
    sp.add_argument("--fixtures", type=int, required=True)
    sp.add_argument("--urinals", type=int, default=0)
    sp.add_argument("--burst-share", type=float, default=0.4,
                    help="fraction hitting restrooms at break (default .4)")
    sp.add_argument("--window-min", type=int, default=15,
                    help="break length in minutes")
    sp.add_argument("--female-share", type=float, default=DEFAULT_FEMALE_SHARE)
    sp.set_defaults(func=cmd_event)

    sp = sub.add_parser("audit", help="fixture counts vs code tables")
    sp.add_argument("--venue", required=True, choices=sorted(VISITS_PER_HOUR))
    sp.add_argument("--occupancy", type=int, required=True)
    sp.add_argument("--f-wc", type=int, default=None)
    sp.add_argument("--m-wc", type=int, default=None)
    sp.add_argument("--m-ur", type=int, default=None)
    sp.add_argument("--f-lav", type=int, default=None)
    sp.add_argument("--m-lav", type=int, default=None)
    sp.set_defaults(func=cmd_audit)

    args = p.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
