#!/usr/bin/env python3
"""Turn the podcast ledger's prediction scoreboard into a publishable
report — the "who called it right" leaderboard, not a raw findings dump.

Zero LLM calls. Every number here is already sitting in state/<show>.json
from `ledger.py record`/`check-prediction`, done as those episodes were
mined; this script only reads and formats it. That's the point: the
scoreboard report is a free side-effect of mining you were already doing,
not a new extraction pass, so it costs nothing extra to publish on a
cadence and use as a public growth loop (a "grading the pundits" report is
inherently shareable in a way a private findings digest isn't).

Usage:
    python3 scoreboard_report.py [--by-guest] [--min-tested 1] out.html [out.md]

Pulls from ledger.py in this same directory (scoreboard, predictions --all).
Builds a render_report.py payload — tiers are hit-rate bands, not topic —
then renders it exactly like any other report in this skill family.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
LEDGER = ROOT / "ledger.py"

sys.path.insert(0, str(ROOT))
from ledger import STATE_DIR  # noqa: E402
from render_report import PayloadError, render_to  # noqa: E402

TIER_BANDS = [
    # (floor, name, label, color)
    (0.8, "Elite calls", "80%+ of tested predictions confirmed", "sig"),
    (0.5, "Solid track record", "50-79% of tested predictions confirmed", "mid"),
    (0.0, "Overconfident", "Under 50% of tested predictions confirmed", "alert"),
]
UNRATED = ("Too early to grade", "No tested predictions yet (still open or stale only)", "off")


def _run_ledger(*args):
    out = subprocess.run(
        [sys.executable, str(LEDGER), *args], capture_output=True, text=True, check=True
    ).stdout
    return json.loads(out)


def _tier_for(hit_rate):
    if hit_rate is None:
        return UNRATED
    for floor, name, label, color in TIER_BANDS:
        if hit_rate >= floor:
            return name, label, color
    return UNRATED


def _examples(preds, key, by_guest):
    field = "speaker" if by_guest else "show"
    confirmed = next((p for p in preds if p.get(field) == key and p["status"] == "confirmed"), None)
    failed = next((p for p in preds if p.get(field) == key and p["status"] == "failed"), None)
    bits = []
    if confirmed:
        bits.append(f"Right: \"{confirmed['text']}\" ({confirmed['show']}).")
    if failed:
        bits.append(f"Wrong: \"{failed['text']}\" ({failed['show']}).")
    return " ".join(bits) if bits else "No individually-cited example on record yet."


def build_payload(by_guest, min_tested):
    board = _run_ledger("scoreboard", *(["--by-guest"] if by_guest else []))
    preds = _run_ledger("predictions", "--all")

    key_field = "by_guest" if by_guest else "show"
    tiers = {}
    for row in board:
        tested = row["confirmed"] + row["failed"]
        if tested < min_tested and row["hit_rate"] is not None:
            continue
        name, label, color = _tier_for(row["hit_rate"])
        tier = tiers.setdefault(name, {"name": name, "label": label, "color": color, "items": []})
        rate_pct = f"{round(row['hit_rate'] * 100)}%" if row["hit_rate"] is not None else "unrated"
        tier["items"].append({
            "claim": f"{row[key_field]}: {row['confirmed']}/{tested} calls confirmed" if tested
                     else f"{row[key_field]}: no resolved predictions yet",
            "tag": rate_pct,
            "tag_class": color,
            "reasoning": _examples(preds, row[key_field], by_guest),
            "source": f"{row['confirmed']} confirmed, {row['failed']} failed, "
                      f"{row['stale']} stale, {row['open']} still open",
        })

    ordered_names = [b[1] for b in TIER_BANDS] + [UNRATED[0]]
    payload_tiers = []
    for i, name in enumerate(ordered_names):
        t = tiers.get(name)
        if not t:
            continue
        rank = len(TIER_BANDS) - i if name != UNRATED[0] else 1
        payload_tiers.append({
            "name": t["name"], "label": t["label"], "rank": max(rank, 1), "of": len(TIER_BANDS),
            "color": t["color"], "items": t["items"],
        })

    scope = "guests" if by_guest else "shows"
    return {
        "title": f"Prediction Scoreboard: {scope} graded on their own calls",
        "eyebrow": f"{sum(len(t['items']) for t in payload_tiers)} {scope} tracked",
        "headline": "Who's actually been right, graded against their own predictions",
        "query": f"Every {scope[:-1]} with a tracked prediction, ranked by confirmed hit rate, not by follower count or vibes.",
        "tiers": payload_tiers,
        "footer_left": str(STATE_DIR),
        "footer_right": str(LEDGER),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--by-guest", action="store_true", help="grade individual speakers instead of shows")
    ap.add_argument("--min-tested", type=int, default=0, help="drop rated rows below this many tested predictions")
    ap.add_argument("outputs", nargs="+", help="one or more output paths (.html and/or .md)")
    args = ap.parse_args()

    payload = build_payload(args.by_guest, args.min_tested)
    if not any(t["items"] for t in payload["tiers"]):
        print("no predictions recorded yet — nothing to grade", file=sys.stderr)
        sys.exit(1)

    for dest in args.outputs:
        dst = Path(dest)
        try:
            output = render_to(payload, dst)
        except PayloadError as e:
            print(f"payload error: {e}", file=sys.stderr)
            sys.exit(1)
        dst.write_text(output)
        print(f"wrote {dst} ({len(output)} bytes)")


if __name__ == "__main__":
    main()
