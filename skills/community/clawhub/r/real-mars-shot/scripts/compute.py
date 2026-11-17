#!/usr/bin/env python3
"""Physics questions that do not spend a turn: rocket, dose, consumables, windows, people, comms."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rms.present import compute_answer
from rms.state import load_game


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute a Real Mars Shot figure")
    parser.add_argument("--topic", required=True, choices=["rocket", "dose", "consumables", "windows", "people", "comms", "mission"])
    parser.add_argument("--user-id")
    parser.add_argument("--isp", type=float, default=450)
    parser.add_argument("--dv", type=float, default=3600)
    parser.add_argument("--payload-kg", type=float, default=10000)
    parser.add_argument("--crew", type=int, default=6)
    parser.add_argument("--days", type=float, default=860)
    parser.add_argument("--water-recovery", type=float, default=0.98)
    parser.add_argument("--food-closure", type=float, default=0.0)
    parser.add_argument("--o2-mode", default="sabatier")
    parser.add_argument("--transit-shield", type=float, default=0)
    parser.add_argument("--surface-shield", type=float, default=0)
    parser.add_argument("--year", type=int)
    parser.add_argument("--month", type=int)
    parser.add_argument("--profile")
    parser.add_argument("--destination")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    state = None
    if args.user_id:
        loaded = load_game(args.user_id)
        if not loaded.get("exists"):
            print(json.dumps({"ok": False, "error": "no save"}))
            sys.exit(2)
        state = loaded["data"]
    action = {
        "type": "compute",
        "topic": args.topic,
        "isp": args.isp,
        "dv": args.dv,
        "payload_kg": args.payload_kg,
        "crew": args.crew,
        "days": args.days,
        "water_recovery": args.water_recovery,
        "food_closure": args.food_closure,
        "o2_mode": args.o2_mode,
        "transit_shield": args.transit_shield,
        "surface_shield": args.surface_shield,
        "year": args.year,
        "month": args.month,
        "profile": args.profile,
        "destination": args.destination,
    }
    if args.topic == "mission":
        if state is None or not args.profile:
            print(json.dumps({"ok": False, "error": "mission topic needs --user-id and --profile"}))
            sys.exit(1)
        from rms.missions import plan_mission

        answer = plan_mission(state, {"profile": args.profile, "destination": args.destination} if args.destination else {"profile": args.profile})
    else:
        answer = compute_answer(state, action)
    print(json.dumps({"ok": True, "answer": answer}, ensure_ascii=False, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
