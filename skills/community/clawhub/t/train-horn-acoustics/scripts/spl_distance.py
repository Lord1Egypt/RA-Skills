#!/usr/bin/env python3
"""Train-horn acoustics helpers: inverse-square SPL and occupational durations.

Free-field point-source estimate:

    L2 = L1 - 20 * log10(r2 / r1)

NIOSH 98-126 allowed duration (minutes) for a continuous A-weighted level L:

    T = 480 / 2 ** ((L - 85) / 3)

OSHA 29 CFR 1910.95 Table G-16 uses a 5 dB exchange rate from 90 dBA / 8 h:

    T_hours = 8 / 2 ** ((L - 90) / 5)

These duration figures assume a steady level for the whole interval. They are
not a measurement of a horn blast and are not a compliance determination.
"""

from __future__ import annotations

import argparse
import math
import sys


def spl_at_distance(level_db: float, at_m: float, to_m: float) -> float:
    if at_m <= 0 or to_m <= 0:
        raise ValueError("distances must be positive")
    return level_db - 20.0 * math.log10(to_m / at_m)


def niosh_allowed_minutes(level_dba: float) -> float:
    """Allowed duration in minutes at a continuous A-weighted level (NIOSH REL)."""
    return 480.0 / (2.0 ** ((level_dba - 85.0) / 3.0))


def osha_allowed_hours(level_dba: float) -> float:
    """Allowed duration in hours at a continuous A-weighted level (Table G-16 rate)."""
    return 8.0 / (2.0 ** ((level_dba - 90.0) / 5.0))


def _fmt(n: float) -> str:
    if abs(n) >= 100:
        return f"{n:.1f}"
    return f"{n:.2f}"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Estimate free-field SPL vs distance and NIOSH/OSHA durations."
    )
    p.add_argument("--level-db", type=float, help="Reference sound level in dB")
    p.add_argument("--at-m", type=float, help="Distance of the reference level, metres")
    p.add_argument("--to-m", type=float, help="Distance at which to estimate the level, metres")
    p.add_argument(
        "--continuous-dba",
        type=float,
        help="Continuous A-weighted level for occupational duration estimates",
    )
    p.add_argument(
        "--duration",
        action="store_true",
        help="Print NIOSH and OSHA allowed durations for --continuous-dba",
    )
    args = p.parse_args(argv)

    if args.level_db is not None or args.at_m is not None or args.to_m is not None:
        if None in (args.level_db, args.at_m, args.to_m):
            p.error("--level-db, --at-m and --to-m must be used together")
        try:
            est = spl_at_distance(args.level_db, args.at_m, args.to_m)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        print(
            f"Estimated free-field SPL: {_fmt(est)} dB at {args.to_m:g} m "
            f"(reference {_fmt(args.level_db)} dB at {args.at_m:g} m; "
            f"inverse-square, 6 dB per distance doubling)."
        )

    if args.duration or args.continuous_dba is not None:
        if args.continuous_dba is None:
            p.error("--duration requires --continuous-dba")
        niosh_min = niosh_allowed_minutes(args.continuous_dba)
        osha_h = osha_allowed_hours(args.continuous_dba)
        print(
            f"NIOSH 98-126 (85 dBA / 8 h, 3 dB exchange): "
            f"{_fmt(niosh_min)} minutes at a continuous {args.continuous_dba:g} dBA."
        )
        print(
            f"OSHA 29 CFR 1910.95 Table G-16 rate (90 dBA / 8 h, 5 dB exchange): "
            f"{_fmt(osha_h)} hours at a continuous {args.continuous_dba:g} dBA."
        )
        print(
            "These durations apply to a steady level over a work-shift calculation, "
            "not to a single train horn blast."
        )

    if (
        args.level_db is None
        and args.continuous_dba is None
        and not args.duration
    ):
        p.print_help()
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
