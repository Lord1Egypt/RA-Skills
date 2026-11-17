#!/usr/bin/env python3
"""
Tennis Live-State Gate — status probe.

Read-only. Shows what the gate sees for a given pair of players right now:
the resolved match, the score snapshot, the derived break-point flag, and the
gate decision. Places no orders.

Usage:
    export LIVETENNIS_API_KEY=...      # FREE key: livetennisapi.com/subscribe/free
    python scripts/status.py "Carlos Alcaraz" "Jannik Sinner"
"""
import os
import sys

sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tennis_live_gate_skill import (  # noqa: E402
    DEFAULT_BASE_URL,
    fetch_live_tennis_state,
    live_tennis_state_gate,
)


def main() -> int:
    if len(sys.argv) != 3:
        print('Usage: python scripts/status.py "Player One" "Player Two"')
        return 2

    api_key = os.environ.get("LIVETENNIS_API_KEY")
    if not api_key:
        print("Error: LIVETENNIS_API_KEY not set.")
        print("   Get a FREE key at https://livetennisapi.com/subscribe/free")
        return 1

    base_url = os.environ.get("LIVETENNIS_BASE_URL", DEFAULT_BASE_URL)
    players = [sys.argv[1], sys.argv[2]]

    print(f"Resolving live match for: {players[0]} vs {players[1]}\n")
    try:
        state = fetch_live_tennis_state(players, api_key=api_key, base_url=base_url)
    except Exception as e:  # noqa: BLE001
        print(f"API error: {e}")
        return 1

    if state is None:
        print("No live match found for those players.")
        return 0

    decision = live_tennis_state_gate(state)

    print("=" * 50)
    print("MATCH STATE")
    print("=" * 50)
    print(f"  match_id:    {state.match_id}")
    print(f"  status:      {state.status}")
    print(f"  as_of:       {state.as_of}")
    print(f"  age (s):     {state.age_s}")
    print(f"  server:      {decision.server}")
    print(f"  break_point: {decision.break_point}  (None = UNDEF)")
    print(f"  is_tiebreak: {decision.is_tiebreak}")
    print("=" * 50)
    print("GATE DECISION")
    print("=" * 50)
    verdict = "ALLOW" if decision.allowed else "SKIP"
    print(f"  {verdict}  reason={decision.reason}  size_factor={decision.size_factor:.2f}")
    print("=" * 50)
    print("\n(observe-only — this probe places no orders)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
