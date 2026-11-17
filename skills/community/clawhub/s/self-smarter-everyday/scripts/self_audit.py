#!/usr/bin/env python3
"""
self_audit.py — Self-audit script for quality metrics.

Checks:
  - Response quality (error rate, retry rate)
  - Memory usage (state directory size, entry counts)
  - Error patterns (frequency, categories)
  - Token efficiency (estimated tokens per task)

Outputs an audit report as JSON and prints a summary.

Usage:
  python3 self_audit.py [--state-dir DIR] [--output PATH]
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_STATE_DIR = os.path.expanduser("~/self-smarter/state")
DEFAULT_LOG_DIR = os.path.expanduser("~/self-smarter/logs")

# ---------------------------------------------------------------------------
# Metric collectors
# ---------------------------------------------------------------------------
def collect_memory_metrics(state_dir: Path) -> dict:
    """Measure state directory size and entry counts."""
    total_size = 0
    file_count = 0
    dir_sizes = {}
    if state_dir.exists():
        for dirpath, dirnames, filenames in os.walk(state_dir):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    size = os.path.getsize(fp)
                    total_size += size
                    file_count += 1
                    rel = os.path.relpath(dirpath, state_dir)
                    dir_sizes[rel] = dir_sizes.get(rel, 0) + size
                except OSError:
                    pass
    return {
        "total_size_bytes": total_size,
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "file_count": file_count,
        "directory_breakdown": dir_sizes,
    }

def collect_error_metrics(state_dir: Path) -> dict:
    """Analyze error patterns from nightly routine logs."""
    log_dir = Path(DEFAULT_LOG_DIR)
    error_count = 0
    total_runs = 0
    error_categories = {}
    if log_dir.exists():
        for log_file in sorted(log_dir.glob("nightly_*.log")):
            total_runs += 1
            with open(log_file, "r") as f:
                for line in f:
                    if "ERROR" in line or "failed" in line.lower():
                        error_count += 1
                        # Extract category from log message
                        if "timeout" in line.lower():
                            error_categories["timeout"] = error_categories.get("timeout", 0) + 1
                        elif "not found" in line.lower():
                            error_categories["missing_resource"] = error_categories.get("missing_resource", 0) + 1
                        else:
                            error_categories["general"] = error_categories.get("general", 0) + 1
    error_rate = error_count / max(total_runs, 1)
    return {
        "total_runs": total_runs,
        "error_count": error_count,
        "error_rate": round(error_rate, 4),
        "error_categories": error_categories,
    }

def collect_performance_metrics(state_dir: Path) -> dict:
    """Collect performance metrics from phase results."""
    state_file = state_dir / "routine_state.json"
    if not state_file.exists():
        return {"run_count": 0, "avg_phase_duration_ms": 0, "success_rate": 0}
    with open(state_file, "r") as f:
        state = json.load(f)
    results = state.get("phase_results", {})
    total = len(results)
    completed = sum(1 for r in results.values() if r.get("status") == "completed")
    return {
        "run_count": state.get("run_count", 0),
        "last_run": state.get("last_run", "never"),
        "phases_executed": total,
        "phases_completed": completed,
        "success_rate": round(completed / max(total, 1), 4),
    }

def collect_token_efficiency(state_dir: Path) -> dict:
    """Estimate token efficiency from reflection data."""
    reflections_dir = state_dir / "reflections"
    total_entries = 0
    total_lessons = 0
    if reflections_dir.exists():
        for rf in reflections_dir.glob("*.json"):
            with open(rf, "r") as f:
                entry = json.load(f)
                total_entries += 1
                total_lessons += len(entry.get("lessons_learned", []))
    # Efficiency = lessons per entry (higher is better, max 1.0 target)
    efficiency = min(total_lessons / max(total_entries, 1), 1.0)
    return {
        "reflection_entries": total_entries,
        "total_lessons_captured": total_lessons,
        "token_efficiency": round(efficiency, 4),
    }

# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------
def generate_report(state_dir: Path) -> dict:
    """Generate a comprehensive audit report."""
    report = {
        "audit_timestamp": datetime.now().isoformat(),
        "state_directory": str(state_dir),
        "memory": collect_memory_metrics(state_dir),
        "errors": collect_error_metrics(state_dir),
        "performance": collect_performance_metrics(state_dir),
        "token_efficiency": collect_token_efficiency(state_dir),
    }
    # Overall health score (0-100)
    health = 100
    if report["errors"]["error_rate"] > 0.1:
        health -= 20
    if report["token_efficiency"]["token_efficiency"] < 0.3:
        health -= 15
    if report["memory"]["total_size_mb"] > 500:
        health -= 10
    if report["performance"]["success_rate"] < 0.8:
        health -= 15
    report["health_score"] = max(health, 0)
    return report

def print_summary(report: dict):
    """Print a human-readable summary."""
    print("\n" + "=" * 50)
    print("  SELF-AUDIT REPORT")
    print("=" * 50)
    print(f"  Timestamp:      {report['audit_timestamp']}")
    print(f"  Health Score:   {report['health_score']}/100")
    print(f"  Memory Usage:   {report['memory']['total_size_mb']} MB ({report['memory']['file_count']} files)")
    print(f"  Error Rate:     {report['errors']['error_rate']:.1%}")
    print(f"  Success Rate:   {report['performance']['success_rate']:.1%}")
    print(f"  Token Eff:      {report['token_efficiency']['token_efficiency']:.1%}")
    print("=" * 50 + "\n")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Self-audit metrics")
    parser.add_argument("--state-dir", type=str, default=DEFAULT_STATE_DIR)
    parser.add_argument("--output", type=str, help="Write report to file")
    args = parser.parse_args()

    state_dir = Path(args.state_dir)
    report = generate_report(state_dir)
    print_summary(report)

    # Always save latest audit
    audit_file = state_dir / "audit_latest.json"
    state_dir.mkdir(parents=True, exist_ok=True)
    with open(audit_file, "w") as f:
        json.dump(report, f, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2)
        print(f"Report saved to: {args.output}")

if __name__ == "__main__":
    main()
