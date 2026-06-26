#!/usr/bin/env python3
"""
stopping-detector.py — evaluate the 6 goal-driven stopping signals for a deliberation run.

Usage:
    python stopping-detector.py --n-agents N [--state-dir state/] [--rounds-dir rounds/]

Returns 0 if ≥4 of 6 signals satisfied (deliberation should stop).
Returns 1 if <4 signals satisfied (continue).

Signals:
1. Claim refutation rate stabilizes (rolling avg drop)
2. Disagreement slope flat or rising (no sycophancy)
3. All agents have led at least one non-stress round
4. At least N-1 agents have been stress-tested
5. Drift checks pass
6. Pending claim fraction < 30%

See references/stopping-criteria.md for full rationale.
"""

import json
import sys
import argparse
from pathlib import Path
from collections import Counter
from typing import Dict, List, Tuple


def load_jsonl(path: Path) -> List[Dict]:
    entries = []
    if not path.exists():
        return entries
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return entries


def signal_1_claim_refutation_stable(verifications: List[Dict]) -> Tuple[bool, str]:
    """Rolling 3-round avg of status transitions drops below 50% of mid-experiment peak."""
    if not verifications:
        return False, "no verifications"

    rounds = sorted({v["round"] for v in verifications})
    if len(rounds) < 6:
        return False, f"only {len(rounds)} rounds, need ≥6 for trend"

    transitions_per_round = Counter()
    for v in verifications:
        transitions_per_round[v["round"]] += len(v.get("claim_status_changes", []))

    counts = [transitions_per_round.get(r, 0) for r in rounds]
    rolling = [sum(counts[i:i+3]) / 3 for i in range(len(counts) - 2)]
    if not rolling:
        return False, "insufficient rolling-window data"

    peak = max(rolling)
    last_two = rolling[-2:]

    if peak == 0:
        return False, "no transitions observed"
    if all(r < peak * 0.5 for r in last_two):
        return True, f"recent rolling avg ({last_two}) < 50% of peak ({peak:.1f})"
    return False, f"recent rolling avg ({last_two}) not below 50% of peak ({peak:.1f})"


def signal_2_disagreement_slope(verifications: List[Dict]) -> Tuple[bool, str]:
    """OLS slope of disagreement_count over rounds; ≥0 healthy, ≥-0.2 stable."""
    if not verifications:
        return False, "no verifications"

    disagreement_per_round = Counter()
    for v in verifications:
        if v.get("result") in ("BROKEN", "UNCLEAR"):
            disagreement_per_round[v["round"]] += 1

    rounds = sorted(disagreement_per_round.keys())
    if len(rounds) < 3:
        return False, f"only {len(rounds)} rounds with disagreement data"

    xs = rounds
    ys = [disagreement_per_round[r] for r in rounds]
    n = len(xs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den = sum((x - mean_x) ** 2 for x in xs)
    slope = num / den if den else 0

    if slope >= 0:
        return True, f"slope = {slope:.3f} ≥ 0 (anti-sycophantic)"
    if slope >= -0.2:
        return True, f"slope = {slope:.3f} ∈ [-0.2, 0) (stable)"
    return False, f"slope = {slope:.3f} < -0.2 (sycophancy risk)"


def signal_3_all_agents_led(lead_history: List[Dict], n_agents: int) -> Tuple[bool, str]:
    """Each agent has led ≥1 non-stress round."""
    led_agents = {
        entry.get("lead") for entry in lead_history
        if entry.get("lead") not in (None, "system", "none")
        and not entry.get("is_stress", False)
    }

    if len(led_agents) >= n_agents:
        return True, f"{len(led_agents)}/{n_agents} agents have led"
    return False, f"only {len(led_agents)}/{n_agents} agents have led"


def signal_4_stress_tests_done(lead_history: List[Dict], n_agents: int) -> Tuple[bool, str]:
    """At least N-1 agents have been stress-tested."""
    stressed_agents = {
        entry.get("absent_agent") for entry in lead_history
        if entry.get("is_stress", False) and entry.get("absent_agent")
    }

    target = max(1, n_agents - 1)
    if len(stressed_agents) >= target:
        return True, f"{len(stressed_agents)} agents stress-tested (target ≥{target})"
    return False, f"only {len(stressed_agents)} agents stress-tested (target ≥{target})"


def signal_5_drift_checks_pass(rounds_dir: Path) -> Tuple[bool, str]:
    """All drift checks PASS, or most recent PASS after a prior FAIL was addressed."""
    if not rounds_dir.exists():
        return False, "rounds directory not found"

    drift_results = []
    for round_md in sorted(rounds_dir.glob("round_*.md")):
        text = round_md.read_text(encoding='utf-8')
        # Look for drift check section verdict
        lower = text.lower()
        if "drift check" in lower:
            # Naive verdict extraction
            if "drift check: pass" in lower or "drift_check: pass" in lower:
                drift_results.append("PASS")
            elif "drift check: fail" in lower or "drift_check: fail" in lower:
                drift_results.append("FAIL")
            elif "drift check: partial" in lower or "drift_check: partial" in lower:
                drift_results.append("PARTIAL")

    if not drift_results:
        return False, "no drift check results found"

    if all(r == "PASS" for r in drift_results):
        return True, f"all {len(drift_results)} drift checks PASS"
    if drift_results[-1] == "PASS" and "FAIL" in drift_results:
        return True, f"recent PASS after prior FAIL: {drift_results}"
    return False, f"drift check results: {drift_results}"


def signal_6_pending_fraction(claims: List[Dict]) -> Tuple[bool, str]:
    """Pending claim fraction < 30%."""
    if not claims:
        return False, "no claims"

    total = len(claims)
    pending = sum(1 for c in claims if c.get("status") == "pending")
    fraction = pending / total

    if fraction < 0.3:
        return True, f"pending fraction = {fraction:.1%} (< 30%)"
    return False, f"pending fraction = {fraction:.1%} (≥ 30%)"


def main():
    parser = argparse.ArgumentParser(description="Evaluate stopping signals.")
    parser.add_argument("--state-dir", default="state", help="Path to state directory")
    parser.add_argument("--rounds-dir", default="rounds", help="Path to rounds directory")
    parser.add_argument("--n-agents", type=int, required=True, help="Number of agents")
    args = parser.parse_args()

    state_dir = Path(args.state_dir).resolve()
    rounds_dir = Path(args.rounds_dir).resolve()

    claims = load_jsonl(state_dir / "claims.jsonl")
    verifications = load_jsonl(state_dir / "verifications.jsonl")
    lead_history = load_jsonl(state_dir / "lead_history.jsonl")

    signals = [
        ("Signal 1 — claim refutation rate stable", signal_1_claim_refutation_stable(verifications)),
        ("Signal 2 — disagreement slope ≥ -0.2", signal_2_disagreement_slope(verifications)),
        ("Signal 3 — all agents led", signal_3_all_agents_led(lead_history, args.n_agents)),
        ("Signal 4 — stress tests done", signal_4_stress_tests_done(lead_history, args.n_agents)),
        ("Signal 5 — drift checks pass", signal_5_drift_checks_pass(rounds_dir)),
        ("Signal 6 — pending fraction < 30%", signal_6_pending_fraction(claims)),
    ]

    satisfied = sum(1 for _, (ok, _) in signals if ok)

    print(f"=== Stopping Signal Evaluation ===")
    for name, (ok, detail) in signals:
        marker = "✓" if ok else "✗"
        print(f"  {marker} {name}: {detail}")
    print(f"\nSatisfied: {satisfied}/6")

    should_stop = satisfied >= 4
    print(f"Verdict: {'STOP (consider synthesis round next)' if should_stop else 'CONTINUE'} (threshold: ≥4 of 6)")

    sys.exit(0 if should_stop else 1)


if __name__ == "__main__":
    main()
