#!/usr/bin/env python3
"""
Subconscious Weekly Benchmark
Compares current state to baseline and outputs a comparison report.
Run via: python3 subconscious_benchmark.py
"""
import json
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(__file__).parent.parent.resolve()
BASELINE_FILE = WORKSPACE / "memory" / "subconscious" / "benchmark_baseline.json"
OUTPUT_DIR = WORKSPACE / "memory" / "subconscious" / "benchmarks"
LEARNINGS_DIR = WORKSPACE / ".learnings"
STORE_DIR = WORKSPACE / "memory" / "subconscious"

def load_baseline():
    if not BASELINE_FILE.exists():
        return None
    with open(BASELINE_FILE) as f:
        return json.load(f)

def load_current():
    current = {
        "captured_at": datetime.now().isoformat(),
        "learnings_summary": {},
        "live_items": [],
        "pending_count": 0,
        "metrics": {}
    }

    # Learnings
    for f in ["LEARNINGS.md", "ERRORS.md", "FEATURES.md"]:
        path = LEARNINGS_DIR / f
        if path.exists():
            lines = [l.strip() for l in path.read_text().splitlines()
                     if l.strip() and not l.startswith("#")]
            current["learnings_summary"][f] = {
                "entries": len(lines),
                "preview": lines[:3]
            }

    # Live
    live_path = STORE_DIR / "live.json"
    if live_path.exists():
        live = json.loads(live_path.read_text())
        for item in live.get("items", []):
            current["live_items"].append({
                "id": item.get("id"),
                "kind": item.get("kind"),
                "text": item.get("text", "")[:80],
                "confidence": item.get("confidence"),
                "reinforcement": item.get("reinforcement", {}).get("count")
            })

    # Pending
    pending_path = STORE_DIR / "pending.jsonl"
    current["pending_count"] = len([
        l for l in pending_path.read_text().splitlines() if l.strip()
    ])

    # Snapshots
    snaps = list((STORE_DIR / "snapshots").glob("*.json"))
    current["metrics"]["snapshots"] = len(snaps)

    return current

def compare(baseline, current):
    lines = []
    lines.append("=" * 60)
    lines.append(f"SUBCONSCIOUS BENCHMARK — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 60)

    # Learnings
    lines.append("\n📚 LEARNINGS VOLUME")
    for f in ["LEARNINGS.md", "ERRORS.md", "FEATURES.md"]:
        b = baseline["learnings_summary"].get(f, {}).get("entries", 0)
        c = current["learnings_summary"].get(f, {}).get("entries", 0)
        delta = c - b
        sign = "+" if delta > 0 else ""
        lines.append(f"  {f:20s}  {b:3d} → {c:3d}  ({sign}{delta})")

    # Live items
    lines.append(f"\n🧠 LIVE BIASES: {len(baseline['live_items'])} → {len(current['live_items'])}")
    new_biases = [i for i in current["live_items"]
                  if i["id"] not in [b["id"] for b in baseline["live_items"]]]
    if new_biases:
        lines.append("  New biases promoted:")
        for b in new_biases:
            lines.append(f"    [{b['kind']}] {b['text']}")

    # Pending
    b_pend = baseline["pending_count"]
    c_pend = current["pending_count"]
    lines.append(f"\n📬 PENDING QUEUE: {b_pend} → {c_pend}")

    # Snapshots
    b_snap = baseline["metrics"].get("snapshots", 0)
    c_snap = current["metrics"].get("snapshots", 0)
    lines.append(f"\n💾 SNAPSHOTS: {b_snap} → {c_snap}")

    # Error recurrence (proxy for learning effectiveness)
    b_errors = baseline["learnings_summary"].get("ERRORS.md", {}).get("entries", 0)
    c_errors = current["learnings_summary"].get("ERRORS.md", {}).get("entries", 0)
    lines.append(f"\n⚠️  ERROR ENTRIES: {b_errors} → {c_errors}")
    if c_errors < b_errors:
        lines.append("  ↓ Fewer errors recorded — subconscious may be helping")
    elif c_errors > b_errors:
        lines.append(f"  ↑ {c_errors - b_errors} new errors — system still learning patterns")

    # Delta time
    b_time = datetime.fromisoformat(baseline["captured_at"])
    c_time = datetime.fromisoformat(current["captured_at"])
    days = (c_time - b_time).days
    lines.append(f"\n📅 Period: {days} days since baseline")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)

def save_snapshot(current):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d")
    out = OUTPUT_DIR / f"benchmark_{stamp}.json"
    with open(out, 'w') as f:
        json.dump(current, f, indent=2, ensure_ascii=False)
    return out

if __name__ == "__main__":
    baseline = load_baseline()
    current = load_current()

    if baseline is None:
        print("No baseline found. Run benchmark_capture first or create benchmark_baseline.json")
        exit(1)

    report = compare(baseline, current)
    print(report)

    snap = save_snapshot(current)
    print(f"\nSnapshot saved: {snap}")
