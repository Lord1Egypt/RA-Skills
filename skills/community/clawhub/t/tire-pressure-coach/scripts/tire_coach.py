#!/usr/bin/env python3
"""Tire Pressure Coach — cold/hot pressure physics, tread verdicts, leak radar.

Commands:
  placard  record a vehicle's door-placard cold pressures (+ optional spare)
  check    measured per-tire psi -> per-tire verdict + exact fill-to number,
           temperature- and altitude-corrected; --hot for warm-tire fills
  tread    per-tire tread mm -> safety verdict (wet-grip aware, not just legal)
  schedule monthly check dates with seasonal expectations
  log      history per vehicle; flags tires losing pressure faster than axle-mate

Stdlib only. Store: tire_coach.json next to script (--store overrides).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

DEFAULT_STORE = Path(__file__).resolve().parent / "tire_coach.json"
K = 273.15                     # Celsius -> Kelvin offset
PSI_PER_METER = 0.0145         # gauge psi gained per meter of altitude
HOT_DELTA_DEFAULT = 3.0        # psi a driven tire typically reads above cold
TOLERANCE = 1.0                # psi band around target considered OK
AXLE_GAP_FLAG = 2.0            # side-to-side gap that flags leak/alignment


def load(store: Path) -> dict:
    if not store.exists():
        sys.exit(f"No store at {store}. Run `placard` first.")
    return json.loads(store.read_text())


def save(store: Path, d: dict) -> None:
    store.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")


def today() -> date:
    return date.today()


def temp_correct(psi: float, t_from: float, t_to: float) -> float:
    """Gauge pressure expected when ambient goes t_from -> t_to (°C)."""
    p_abs = psi + 14.7
    return round(p_abs * (t_to + K) / (t_from + K) - 14.7, 1)


# ------------------------------------------------------------------ placard
def cmd_placard(args) -> None:
    store = args.store
    d = json.loads(store.read_text()) if store.exists() else {"vehicles": {}}
    v = d["vehicles"].setdefault(args.vehicle, {})
    v["front"] = args.front
    v["rear"] = args.rear
    v["spare"] = args.spare
    v["placard_date"] = today().isoformat()
    v.setdefault("checks", [])
    v.setdefault("treads", [])
    save(store, d)
    print(f"{args.vehicle}: placard {args.front} psi front / {args.rear} psi rear"
          + (f" / spare {args.spare} psi" if args.spare else ""))
    print("Placard values are COLD targets (door jamb sticker), never sidewall max.")


# ------------------------------------------------------------------ check
def cmd_check(args) -> None:
    d = load(args.store)
    v = d["vehicles"].get(args.vehicle) or sys.exit(f'Unknown vehicle "{args.vehicle}"')
    # temperature-adjusted targets
    ref_c = args.ref_temp if args.ref_temp is not None else None
    out = []
    for pos, meas, axle in (("LF", args.lf, "front"), ("RF", args.rf, "front"),
                            ("LR", args.lr, "rear"), ("RR", args.rr, "rear")):
        if meas is None:
            continue
        target = v[axle]
        note = ""
        if ref_c is not None and abs(args.temp_c - ref_c) > 2:
            adj = temp_correct(target, ref_c, args.temp_c)
            note = f" [target {target}-> {adj} at {args.temp_c}°C]"
            target = adj
        if args.altitude:
            target = round(target + PSI_PER_METER * args.altitude, 1)
            note += f" (+{PSI_PER_METER*args.altitude:.1f} altitude)"
        if args.hot:
            fill_to = round(meas + max(0.0, target + HOT_DELTA_DEFAULT - meas), 1)
            verdict = f"HOT fill to {fill_to} now, verify cold next morning"
        else:
            delta = round(meas - target, 1)
            if abs(delta) <= TOLERANCE:
                verdict = "OK"
            elif delta < 0:
                verdict = f"ADD {round(target-meas,1)} psi (fill to {target})"
            else:
                verdict = f"BLEED {round(meas-target,1)} psi (down to {target})"
        out.append((pos, meas, target, verdict, note))
        v["checks"].append({"date": today().isoformat(), "pos": pos,
                            "measured": meas, "target": target,
                            "hot": bool(args.hot)})
    save(args.store, d)
    print(f"{args.vehicle} — {'HOT' if args.hot else 'COLD'} check "
          f"({args.temp_c}°C ambient)")
    for pos, meas, target, verdict, note in out:
        print(f"  {pos}: {meas:5.1f} psi vs target {target:5.1f} → {verdict}{note}")
    # axle gap flags
    for a, l, r in (("Front", args.lf, args.rf), ("Rear", args.lr, args.rr)):
        if l is not None and r is not None and abs(l - r) > AXLE_GAP_FLAG:
            print(f"  ⚠ {a} axle side-to-side gap {abs(l-r):.1f} psi — "
                  "leak or alignment; investigate this week")
    if v.get("spare"):
        print(f"  (spare: check too — spacesavers want {v['spare']} psi)")


# ------------------------------------------------------------------ tread
def cmd_tread(args) -> None:
    d = load(args.store)
    v = d["vehicles"].get(args.vehicle) or sys.exit(f'Unknown vehicle "{args.vehicle}"')
    for pos, mm in (("LF", args.lf), ("RF", args.rf), ("LR", args.lr), ("RR", args.rr)):
        if mm is None:
            continue
        v["treads"].append({"date": today().isoformat(), "pos": pos, "mm": mm})
        if mm < 1.6:
            v_ = f"REPLACE NOW — below legal minimum (1.6 mm); wet braking severely degraded"
        elif mm < 3.0:
            v_ = f"URGENT — {mm} mm: replace now, especially before wet/winter season"
        elif mm < 4.0:
            v_ = f"CAUTION — {mm} mm: wet-grip cliff at 4 mm; plan replacement"
        elif mm < 5.0 and args.winter:
            v_ = f"CAUTION — winter tire at {mm} mm: below practical winter minimum"
        else:
            v_ = f"OK — {mm} mm"
        print(f"  {pos}: {mm} mm → {v_}")
    save(args.store, d)
    print("Legal limit ≠ safe limit. Field test: quarter head-down — top of "
          "Washington's head visible ≈ 3.2 mm.")


# ------------------------------------------------------------------ schedule / log
def cmd_schedule(args) -> None:
    d = load(args.store)
    v = d["vehicles"].get(args.vehicle) or sys.exit(f'Unknown vehicle "{args.vehicle}"')
    n = today()
    print(f"Monthly checks for {args.vehicle} (5 min, cold, all four + spare):")
    for i in range(1, 7):
        m = n.replace(day=1) + timedelta(days=32 * i)
        m = m.replace(day=1)
        season = "expect −2 psi vs summer" if m.month in (11, 12, 1, 2) else \
                 "expect +1..2 psi vs winter" if m.month in (5, 6, 7, 8) else ""
        print(f"  {m.isoformat()}  {season}")
    print("TPMS warns at 25% below placard — by then you're already deep "
          "under; monthly manual checks win.")


def cmd_log(args) -> None:
    d = load(args.store)
    v = d["vehicles"].get(args.vehicle) or sys.exit(f'Unknown vehicle "{args.vehicle}"')
    checks = v.get("checks", [])
    if not checks:
        print("No checks logged yet.")
        return
    by_pos: dict[str, list] = {}
    for c in checks:
        if not c["hot"]:
            by_pos.setdefault(c["pos"], []).append(c)
    print(f"{args.vehicle} — cold-check history:")
    for pos, entries in by_pos.items():
        entries.sort(key=lambda c: c["date"])
        line = "  " + pos + ": " + " → ".join(
            f"{c['date'][5:]}:{c['measured']}" for c in entries[-6:])
        if len(entries) >= 2:
            days = (datetime.fromisoformat(entries[-1]["date"])
                    - datetime.fromisoformat(entries[0]["date"])).days
            if days > 0:
                rate = (entries[0]["measured"] - entries[-1]["measured"]) / days * 30
                if rate > 1.0:
                    line += f"  ⚠ losing ~{rate:.1f} psi/month — slow leak?"
        print(line)


# ------------------------------------------------------------------ cli
def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--store", default=str(DEFAULT_STORE))
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("placard")
    sp.add_argument("--vehicle", required=True)
    sp.add_argument("--front", type=float, required=True)
    sp.add_argument("--rear", type=float, required=True)
    sp.add_argument("--spare", type=float, default=None)
    sp.set_defaults(fn=cmd_placard)

    sp = sub.add_parser("check")
    sp.add_argument("--vehicle", required=True)
    sp.add_argument("--lf", type=float)
    sp.add_argument("--rf", type=float)
    sp.add_argument("--lr", type=float)
    sp.add_argument("--rr", type=float)
    sp.add_argument("--temp-c", type=float, default=20.0, help="current ambient °C")
    sp.add_argument("--ref-temp", type=float, default=None,
                    help="placard reference temp °C (default: no correction)")
    sp.add_argument("--altitude", type=float, default=0.0, help="meters ABOVE placard reference")
    sp.add_argument("--hot", action="store_true", help="tires warm: compute fill-to")
    sp.set_defaults(fn=cmd_check)

    sp = sub.add_parser("tread")
    sp.add_argument("--vehicle", required=True)
    sp.add_argument("--lf", type=float)
    sp.add_argument("--rf", type=float)
    sp.add_argument("--lr", type=float)
    sp.add_argument("--rr", type=float)
    sp.add_argument("--winter", action="store_true")
    sp.set_defaults(fn=cmd_tread)

    sp = sub.add_parser("schedule")
    sp.add_argument("--vehicle", required=True)
    sp.set_defaults(fn=cmd_schedule)

    sp = sub.add_parser("log")
    sp.add_argument("--vehicle", required=True)
    sp.set_defaults(fn=cmd_log)

    args = p.parse_args()
    args.store = Path(args.store)
    args.fn(args)


if __name__ == "__main__":
    main()
