#!/usr/bin/env python3
"""
WHOOP Experiment Tracker — define, monitor, and evaluate personal health experiments.

Usage:
  python3 experiment.py plan --name "No alcohol for 30 days" \
    --hypothesis "HRV will increase 10%+" \
    --start 2026-03-01 --end 2026-03-31 \
    --metrics hrv,recovery,sleep_performance

  # With post-workout segmentation (tests hypothesis against recovery AFTER workouts):
  python3 experiment.py plan --name "My supplement experiment" \
    --hypothesis "Post-strength recovery improves 10%+" \
    --start YYYY-MM-DD --end YYYY-MM-DD \
    --metrics hrv,recovery,rhr \
    --segment-workouts \
    --min-strain 5

  python3 experiment.py list
  python3 experiment.py status --id <id>
  python3 experiment.py report --id <id>
"""

import argparse
import json
import os
import subprocess
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
FETCH_SCRIPT = SCRIPT_DIR / "fetch.py"
EXPERIMENTS_FILE = Path(os.environ.get("WHOOP_EXPERIMENTS_FILE",
    Path.home() / ".config/whoop-skill/experiments.json"))

# Standard metric definitions
METRIC_KEYS = {
    "hrv": ("recovery", "score.hrv_rmssd_milli"),
    "recovery": ("recovery", "score.recovery_score"),
    "rhr": ("recovery", "score.resting_heart_rate"),
    "sleep_performance": ("sleep", "score.sleep_performance_percentage"),
    "strain": ("cycle", "score.strain"),
}

# EST offset (UTC-5). Handles dates correctly for Eastern timezone.
# DST awareness: EDT is -4 (mid-Mar through early-Nov), EST is -5 otherwise.
def et_offset_hours(dt_utc: datetime) -> int:
    """Return Eastern Time UTC offset in hours for a given UTC datetime."""
    year = dt_utc.year
    # DST starts second Sunday of March, ends first Sunday of November
    # Approximate: Mar 8–Nov 1 range is close enough for health data
    dst_start = datetime(year, 3, 8, 7, 0, 0, tzinfo=timezone.utc)
    dst_end   = datetime(year, 11, 1, 6, 0, 0, tzinfo=timezone.utc)
    if dst_start <= dt_utc < dst_end:
        return -4  # EDT
    return -5  # EST


def utc_str_to_et_date(utc_str: str) -> str:
    """Convert a UTC ISO string (e.g. '2026-03-04T09:57:56.810Z') to an ET date string."""
    utc_str = utc_str.replace("Z", "+00:00")
    dt = datetime.fromisoformat(utc_str)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    offset = et_offset_hours(dt)
    et = dt + timedelta(hours=offset)
    return et.date().isoformat()


def load_experiments():
    EXPERIMENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not EXPERIMENTS_FILE.exists():
        return []
    with open(EXPERIMENTS_FILE) as f:
        return json.load(f)


def save_experiments(experiments):
    EXPERIMENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(EXPERIMENTS_FILE, "w") as f:
        json.dump(experiments, f, indent=2)


def fetch_endpoint(endpoint, start, end, limit=90):
    cmd = [
        sys.executable, str(FETCH_SCRIPT), endpoint,
        "--start", start, "--end", end,
        "--limit", str(limit),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"ERROR fetching {endpoint}: {e.stderr}", file=sys.stderr)
        return {}


def deep_get(obj, path):
    """Get nested key like 'score.hrv_rmssd_milli'."""
    keys = path.split(".")
    for k in keys:
        if isinstance(obj, dict):
            obj = obj.get(k)
        else:
            return None
    return obj


def build_recovery_map(start, end):
    """
    Fetch all recovery records in [start, end] and return a dict of
    { ET_date_str: { "recovery_score": x, "hrv": y, "rhr": z } }
    """
    # Extend end by a couple days so we catch recovery after late-window workouts
    extended_end = (datetime.strptime(end, "%Y-%m-%d") + timedelta(days=3)).strftime("%Y-%m-%d")
    data = fetch_endpoint("/recovery", start, extended_end)
    records = data.get("records", [])
    by_date = {}
    for r in records:
        created = r.get("created_at", "")
        if not created:
            continue
        date_str = utc_str_to_et_date(created)
        score = deep_get(r, "score.recovery_score")
        hrv   = deep_get(r, "score.hrv_rmssd_milli")
        rhr   = deep_get(r, "score.resting_heart_rate")
        if score is not None:
            by_date[date_str] = {"recovery": score, "hrv": hrv, "rhr": rhr}
    return by_date


def find_workout_dates(start, end, min_strain=0, sport_filter=None):
    """
    Fetch all workouts in [start, end] and return sorted list of ET date strings
    where a qualifying workout occurred (strain >= min_strain).
    Optional sport_filter: substring match on sport_name (e.g. "weightlifting").
    """
    data = fetch_endpoint("/activity/workout", start, end)
    records = data.get("records", [])
    workout_dates = set()
    for r in records:
        # score can be null (e.g. sauna with no HR data)
        strain = deep_get(r, "score.strain") or 0
        if strain < min_strain:
            continue
        if sport_filter:
            sport_name = (r.get("sport_name") or "").lower()
            if sport_filter.lower() not in sport_name:
                continue
        wo_start = r.get("start", "")
        if wo_start:
            date_str = utc_str_to_et_date(wo_start)
            workout_dates.add(date_str)
    return sorted(workout_dates)


def compute_post_workout_metrics(start, end, min_strain=0, days_after=(1, 2), **kwargs):
    """
    For every qualifying workout in [start, end], collect recovery metrics
    for each day in days_after window. Returns:
      - per-metric averages: { "recovery": avg, "hrv": avg, "rhr": avg }
      - list of detail dicts for transparency
    """
    sport_filter = kwargs.get("sport_filter")
    workout_dates = find_workout_dates(start, end, min_strain, sport_filter=sport_filter)
    if not workout_dates:
        return {}, [], workout_dates

    recovery_map = build_recovery_map(start, end)

    details = []
    metric_buckets = {"recovery": [], "hrv": [], "rhr": []}

    for wo_date in workout_dates:
        wo_dt = datetime.strptime(wo_date, "%Y-%m-%d")
        for n in range(days_after[0], days_after[1] + 1):
            check_date = (wo_dt + timedelta(days=n)).strftime("%Y-%m-%d")
            if check_date > end:
                continue
            if check_date in recovery_map:
                row = recovery_map[check_date]
                detail = {
                    "workout_date": wo_date,
                    "recovery_date": check_date,
                    "days_after": n,
                    "recovery_score": row.get("recovery"),
                    "hrv": row.get("hrv"),
                    "rhr": row.get("rhr"),
                }
                details.append(detail)
                for m in ("recovery", "hrv", "rhr"):
                    if row.get(m) is not None:
                        metric_buckets[m].append(row[m])

    avgs = {}
    for m, vals in metric_buckets.items():
        if vals:
            avgs[m] = round(sum(vals) / len(vals), 2)

    return avgs, details, workout_dates


def compute_metric_avg(endpoint, field_path, start, end):
    """Fetch data for a date range and compute simple average for a metric."""
    data = fetch_endpoint(f"/{endpoint}", start, end)
    records = data.get("records", [])
    values = [deep_get(r, field_path) for r in records]
    values = [v for v in values if v is not None]
    if not values:
        return None
    return round(sum(values) / len(values), 2)


def compute_baseline(metrics, start_date, seg_config=None):
    """Compute baseline from 14 days prior to start_date."""
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    baseline_end   = (start_dt - timedelta(days=1)).strftime("%Y-%m-%d")
    baseline_start = (start_dt - timedelta(days=14)).strftime("%Y-%m-%d")

    print(f"Computing baseline from {baseline_start} to {baseline_end}...", file=sys.stderr)

    baseline = {}
    for metric in metrics:
        if metric not in METRIC_KEYS:
            print(f"WARNING: Unknown metric '{metric}', skipping.", file=sys.stderr)
            continue
        endpoint, field_path = METRIC_KEYS[metric]
        avg = compute_metric_avg(endpoint, field_path, baseline_start, baseline_end)
        if avg is not None:
            baseline[metric] = avg
            print(f"  {metric}: {avg}", file=sys.stderr)
        else:
            print(f"  {metric}: no data in baseline window", file=sys.stderr)

    # Post-workout segmented baseline
    pw_baseline = {}
    pw_workout_dates = []
    if seg_config and seg_config.get("enabled"):
        min_strain = seg_config.get("min_strain", 0)
        days_after = tuple(seg_config.get("days_after", [1, 2]))
        print(f"\nComputing post-workout baseline (min_strain={min_strain}, days_after={days_after})...", file=sys.stderr)
        pw_avgs, pw_details, pw_workout_dates = compute_post_workout_metrics(
            baseline_start, baseline_end, min_strain=min_strain, days_after=days_after
        )
        if pw_avgs:
            for m in metrics:
                if m in pw_avgs:
                    pw_baseline[m] = pw_avgs[m]
                    print(f"  post-workout {m}: {pw_avgs[m]} (from {len(pw_workout_dates)} workout days)", file=sys.stderr)
        else:
            print(f"  No qualifying workouts found in baseline window. Baseline will be established from experiment data.", file=sys.stderr)

    return baseline, pw_baseline, baseline_start, baseline_end


def compute_window_avgs(metrics, start_date, end_date):
    avgs = {}
    for metric in metrics:
        if metric not in METRIC_KEYS:
            continue
        endpoint, field_path = METRIC_KEYS[metric]
        avg = compute_metric_avg(endpoint, field_path, start_date, end_date)
        avgs[metric] = avg
    return avgs


def trend_arrow(delta):
    if delta is None:
        return "→"
    return "↑" if delta > 0 else ("↓" if delta < 0 else "→")


def fmt_value(metric, value):
    if value is None:
        return "N/A"
    if metric == "hrv":
        return f"{value:.1f}ms"
    if metric == "rhr":
        return f"{value:.0f}bpm"
    if metric in ("recovery", "sleep_performance"):
        return f"{value:.0f}%"
    return f"{value:.1f}"


def experiment_status_str(exp):
    now = datetime.now(timezone.utc).date().isoformat()
    if now < exp["start_date"]:
        return "planned"
    elif now > exp["end_date"]:
        return "completed"
    else:
        return "running"


# ─────────────────────────────────────────────
# Commands
# ─────────────────────────────────────────────

def cmd_plan(args):
    metrics = [m.strip() for m in args.metrics.split(",")]

    seg_config = None
    if args.segment_workouts:
        days_after = [int(x) for x in args.days_after.split("-")] if "-" in args.days_after else [1, int(args.days_after)]
        seg_config = {
            "enabled": True,
            "min_strain": args.min_strain,
            "days_after": days_after,
        }

    # Baseline
    if any([args.baseline_hrv, args.baseline_recovery, args.baseline_sleep_performance,
            args.baseline_strain, args.baseline_rhr]):
        baseline = {}
        if args.baseline_hrv:             baseline["hrv"] = args.baseline_hrv
        if args.baseline_recovery:        baseline["recovery"] = args.baseline_recovery
        if args.baseline_sleep_performance: baseline["sleep_performance"] = args.baseline_sleep_performance
        if args.baseline_strain:          baseline["strain"] = args.baseline_strain
        if args.baseline_rhr:             baseline["rhr"] = args.baseline_rhr
        pw_baseline = {}
        baseline_start = baseline_end = None
    else:
        baseline, pw_baseline, baseline_start, baseline_end = compute_baseline(metrics, args.start, seg_config)

    exp = {
        "id": str(uuid.uuid4())[:8],
        "name": args.name,
        "hypothesis": args.hypothesis,
        "start_date": args.start,
        "end_date": args.end,
        "metrics": metrics,
        "baseline": baseline,
        "post_workout_baseline": pw_baseline,
        "post_workout_segmentation": seg_config,
        "baseline_window": {"start": baseline_start, "end": baseline_end} if baseline_start else None,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": experiment_status_str({"start_date": args.start, "end_date": args.end}),
    }

    experiments = load_experiments()
    experiments.append(exp)
    save_experiments(experiments)

    print(f"\n✅ Experiment created (id: {exp['id']})")
    print(f"   Name:       {exp['name']}")
    print(f"   Hypothesis: {exp['hypothesis']}")
    print(f"   Period:     {exp['start_date']} → {exp['end_date']}")
    print(f"   Metrics:    {', '.join(metrics)}")
    if seg_config:
        print(f"   Post-workout segmentation: ON (min_strain={seg_config['min_strain']}, days_after={seg_config['days_after']})")
    print(f"\n   Overall baseline:")
    for m, v in baseline.items():
        print(f"     {m}: {fmt_value(m, v)}")
    if pw_baseline:
        print(f"\n   Post-workout baseline:")
        for m, v in pw_baseline.items():
            print(f"     {m}: {fmt_value(m, v)}")
    elif seg_config:
        print(f"\n   Post-workout baseline: not enough workout data yet — will establish from experiment window.")
    print(f"\n   Saved to: {EXPERIMENTS_FILE}")


def cmd_list(args):
    experiments = load_experiments()
    if not experiments:
        print("No experiments found.")
        return

    print(f"\n{'ID':<10} {'Status':<10} {'Segmented':<10} {'Name':<35} {'Period'}")
    print("-" * 88)
    for exp in experiments:
        status = experiment_status_str(exp)
        seg = "✓" if exp.get("post_workout_segmentation", {}) and exp["post_workout_segmentation"].get("enabled") else "-"
        period = f"{exp['start_date']} → {exp['end_date']}"
        print(f"{exp['id']:<10} {status:<10} {seg:<10} {exp['name'][:35]:<35} {period}")


def cmd_status(args):
    experiments = load_experiments()
    exp = next((e for e in experiments if e["id"] == args.id), None)
    if not exp:
        print(f"ERROR: No experiment with id '{args.id}'", file=sys.stderr)
        sys.exit(1)

    status = experiment_status_str(exp)
    now = datetime.now(timezone.utc).date().isoformat()
    window_end = min(now, exp["end_date"])
    window_start = exp["start_date"]

    if window_end < window_start:
        print(f"Experiment '{exp['name']}' hasn't started yet (starts {exp['start_date']}).")
        return

    days_elapsed = (datetime.strptime(window_end, "%Y-%m-%d") - datetime.strptime(window_start, "%Y-%m-%d")).days
    days_total   = (datetime.strptime(exp["end_date"], "%Y-%m-%d") - datetime.strptime(window_start, "%Y-%m-%d")).days

    print(f"\n📊 Status: {exp['name']} [{status}]")
    print(f"   Hypothesis: {exp['hypothesis']}")
    print(f"   Period: {window_start} → {exp['end_date']}  (day {days_elapsed}/{days_total})")

    # ── Overall averages ──────────────────────────────────────────────
    print(f"\n   OVERALL AVERAGES (all days)")
    print(f"   {'Metric':<20} {'Baseline':>10} {'Current':>10} {'Change':>10}")
    print("   " + "─" * 54)

    current_avgs = compute_window_avgs(exp["metrics"], window_start, window_end)
    for metric in exp["metrics"]:
        baseline_val = exp["baseline"].get(metric)
        current_val  = current_avgs.get(metric)
        if baseline_val is not None and current_val is not None:
            delta = current_val - baseline_val
            pct   = (delta / baseline_val) * 100 if baseline_val != 0 else 0
            print(f"   {metric:<20} {fmt_value(metric, baseline_val):>10} {fmt_value(metric, current_val):>10}   {trend_arrow(delta)}{abs(pct):.1f}%")
        else:
            print(f"   {metric:<20} {fmt_value(metric, baseline_val):>10} {'N/A':>10}")

    # ── Post-workout segmented view ───────────────────────────────────
    seg = exp.get("post_workout_segmentation") or {}
    if seg.get("enabled"):
        min_strain  = seg.get("min_strain", 0)
        days_after  = tuple(seg.get("days_after", [1, 2]))

        pw_avgs, pw_details, wo_dates = compute_post_workout_metrics(
            window_start, window_end, min_strain=min_strain, days_after=days_after
        )

        print(f"\n   POST-WORKOUT RECOVERY ({len(wo_dates)} qualifying workouts, days {days_after[0]}–{days_after[1]} after)")
        if not wo_dates:
            print("   No qualifying workouts found yet.")
        else:
            print(f"   {'Metric':<20} {'Baseline':>10} {'Post-WO':>10} {'Change':>10}")
            print("   " + "─" * 54)
            pw_baseline = exp.get("post_workout_baseline") or {}
            for metric in [m for m in exp["metrics"] if m in ("recovery", "hrv", "rhr")]:
                bl_val  = pw_baseline.get(metric) or exp["baseline"].get(metric)
                cur_val = pw_avgs.get(metric)
                if bl_val is not None and cur_val is not None:
                    delta = cur_val - bl_val
                    pct   = (delta / bl_val) * 100 if bl_val != 0 else 0
                    print(f"   {metric:<20} {fmt_value(metric, bl_val):>10} {fmt_value(metric, cur_val):>10}   {trend_arrow(delta)}{abs(pct):.1f}%")
                else:
                    print(f"   {metric:<20} {fmt_value(metric, bl_val):>10} {'N/A':>10}")

            if pw_details:
                print(f"\n   Workout breakdown:")
                for d in pw_details:
                    rec = f"{d['recovery_score']:.0f}%" if d['recovery_score'] is not None else "N/A"
                    hrv = f"{d['hrv']:.1f}ms" if d['hrv'] is not None else "N/A"
                    print(f"     {d['workout_date']} → +{d['days_after']}d ({d['recovery_date']}): recovery {rec}, HRV {hrv}")


def cmd_report(args):
    experiments = load_experiments()
    exp = next((e for e in experiments if e["id"] == args.id), None)
    if not exp:
        print(f"ERROR: No experiment with id '{args.id}'", file=sys.stderr)
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"WHOOP Experiment Report")
    print(f"{'='*60}")
    print(f"Name:       {exp['name']}")
    print(f"Hypothesis: {exp['hypothesis']}")
    print(f"Period:     {exp['start_date']} → {exp['end_date']}")
    print(f"Metrics:    {', '.join(exp['metrics'])}")
    print()

    # ── Overall ───────────────────────────────────────────────────────
    print("OVERALL AVERAGES")
    print(f"{'Metric':<20} {'Baseline':>10} {'Experiment':>12} {'Change':>10}")
    print("─" * 58)

    final_avgs = compute_window_avgs(exp["metrics"], exp["start_date"], exp["end_date"])
    results = {}
    for metric in exp["metrics"]:
        baseline_val = exp["baseline"].get(metric)
        exp_val      = final_avgs.get(metric)
        if baseline_val is not None and exp_val is not None:
            delta = exp_val - baseline_val
            pct   = (delta / baseline_val) * 100 if baseline_val != 0 else 0
            results[metric] = {"baseline": baseline_val, "experiment": exp_val, "delta": delta, "pct": pct}
            print(f"{metric:<20} {fmt_value(metric, baseline_val):>10} {fmt_value(metric, exp_val):>12}   {trend_arrow(delta)}{abs(pct):.1f}%")
        else:
            results[metric] = None
            print(f"{metric:<20} {fmt_value(metric, baseline_val):>10} {'N/A':>12}")

    # ── Post-workout segmented report ─────────────────────────────────
    seg = exp.get("post_workout_segmentation") or {}
    pw_results = {}
    if seg.get("enabled"):
        min_strain = seg.get("min_strain", 0)
        days_after = tuple(seg.get("days_after", [1, 2]))
        pw_avgs, pw_details, wo_dates = compute_post_workout_metrics(
            exp["start_date"], exp["end_date"], min_strain=min_strain, days_after=days_after
        )

        print(f"\nPOST-WORKOUT RECOVERY ({len(wo_dates)} workouts, days {days_after[0]}–{days_after[1]} after)")
        print(f"{'Metric':<20} {'Baseline':>10} {'Post-WO':>12} {'Change':>10}")
        print("─" * 58)

        pw_baseline = exp.get("post_workout_baseline") or {}
        for metric in [m for m in exp["metrics"] if m in ("recovery", "hrv", "rhr")]:
            bl_val  = pw_baseline.get(metric) or exp["baseline"].get(metric)
            cur_val = pw_avgs.get(metric)
            if bl_val is not None and cur_val is not None:
                delta = cur_val - bl_val
                pct   = (delta / bl_val) * 100 if bl_val != 0 else 0
                pw_results[metric] = {"baseline": bl_val, "experiment": cur_val, "delta": delta, "pct": pct}
                print(f"{metric:<20} {fmt_value(metric, bl_val):>10} {fmt_value(metric, cur_val):>12}   {trend_arrow(delta)}{abs(pct):.1f}%")
            else:
                pw_results[metric] = None
                print(f"{metric:<20} {fmt_value(metric, bl_val):>10} {'N/A':>12}")

    # ── Verdict ───────────────────────────────────────────────────────
    print()
    print("─" * 60)
    print("VERDICT")
    print("─" * 60)

    # Primary verdict: use post-workout results if segmentation is on, else overall
    primary_results = pw_results if (seg.get("enabled") and pw_results) else results
    positive_metrics = {"hrv", "recovery", "sleep_performance"}
    negative_metrics = {"rhr"}

    improvements = total = 0
    for metric, res in primary_results.items():
        if res is None:
            continue
        total += 1
        if metric in positive_metrics and res["delta"] > 0:
            improvements += 1
        elif metric in negative_metrics and res["delta"] < 0:
            improvements += 1

    if total == 0:
        verdict = "INCONCLUSIVE — No data available for comparison."
    elif improvements == total:
        verdict = "MET ✅ — All tracked metrics improved."
    elif improvements > total / 2:
        verdict = "PARTIALLY MET 🟡 — Most metrics improved, but not all."
    elif improvements == 0:
        verdict = "NOT MET ❌ — No tracked metrics improved."
    else:
        verdict = "INCONCLUSIVE 🤔 — Mixed results across metrics."

    if seg.get("enabled"):
        print(f"\n{verdict}  (evaluated on post-workout recovery window)")
    else:
        print(f"\n{verdict}")

    print("\nPlain-language summary:")
    for metric, res in primary_results.items():
        if res is None:
            print(f"  • {metric}: insufficient data")
            continue
        direction = "improved" if res["delta"] > 0 else "declined"
        if metric in negative_metrics:
            direction = "improved" if res["delta"] < 0 else "increased"
        print(f"  • {metric}: {direction} by {abs(res['pct']):.1f}% "
              f"({fmt_value(metric, res['baseline'])} → {fmt_value(metric, res['experiment'])})")

    print(f"\n{'='*60}")


def cmd_update_segmentation(args):
    """Add or update post-workout segmentation on an existing experiment."""
    experiments = load_experiments()
    exp = next((e for e in experiments if e["id"] == args.id), None)
    if not exp:
        print(f"ERROR: No experiment with id '{args.id}'", file=sys.stderr)
        sys.exit(1)

    days_after = [int(x) for x in args.days_after.split("-")] if "-" in args.days_after else [1, int(args.days_after)]
    seg_config = {
        "enabled": True,
        "min_strain": args.min_strain,
        "days_after": days_after,
    }

    # Recompute post-workout baseline from original baseline window
    bl_window = exp.get("baseline_window") or {}
    pw_baseline = {}
    if bl_window.get("start") and bl_window.get("end"):
        print(f"Computing post-workout baseline from {bl_window['start']} to {bl_window['end']}...", file=sys.stderr)
        pw_avgs, _, wo_dates = compute_post_workout_metrics(
            bl_window["start"], bl_window["end"],
            min_strain=args.min_strain,
            days_after=tuple(days_after),
        )
        if pw_avgs:
            pw_baseline = {m: pw_avgs[m] for m in exp["metrics"] if m in pw_avgs}
            print(f"  Found {len(wo_dates)} qualifying workouts in baseline window.", file=sys.stderr)
            for m, v in pw_baseline.items():
                print(f"  post-workout {m}: {fmt_value(m, v)}", file=sys.stderr)
        else:
            print(f"  No qualifying workouts in baseline window — baseline will build from experiment data.", file=sys.stderr)

    exp["post_workout_segmentation"] = seg_config
    exp["post_workout_baseline"] = pw_baseline
    save_experiments(experiments)

    print(f"\n✅ Updated experiment '{exp['name']}' (id: {exp['id']})")
    print(f"   Post-workout segmentation: ON")
    print(f"   min_strain: {args.min_strain}")
    print(f"   days_after: {days_after}")
    if pw_baseline:
        print(f"\n   Post-workout baseline:")
        for m, v in pw_baseline.items():
            print(f"     {m}: {fmt_value(m, v)}")
    else:
        print(f"\n   Post-workout baseline: will be established from early experiment data.")


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="WHOOP Experiment Tracker")
    sub = parser.add_subparsers(dest="command")

    # plan
    plan_p = sub.add_parser("plan", help="Create a new experiment")
    plan_p.add_argument("--name", required=True)
    plan_p.add_argument("--hypothesis", required=True)
    plan_p.add_argument("--start", required=True, help="YYYY-MM-DD")
    plan_p.add_argument("--end", required=True, help="YYYY-MM-DD")
    plan_p.add_argument("--metrics", required=True,
        help="Comma-separated: hrv,recovery,sleep_performance,rhr,strain")
    # Segmentation options
    plan_p.add_argument("--segment-workouts", action="store_true",
        help="Enable post-workout recovery segmentation")
    plan_p.add_argument("--min-strain", type=float, default=5.0,
        help="Minimum workout strain to qualify (default: 5.0)")
    plan_p.add_argument("--days-after", default="1-2",
        help="Days after workout to measure (e.g. '1-2' or '1'). Default: 1-2")
    # Manual baseline overrides
    plan_p.add_argument("--baseline-hrv", type=float)
    plan_p.add_argument("--baseline-recovery", type=float)
    plan_p.add_argument("--baseline-sleep-performance", type=float)
    plan_p.add_argument("--baseline-strain", type=float)
    plan_p.add_argument("--baseline-rhr", type=float)

    # list
    sub.add_parser("list", help="List all experiments")

    # status
    status_p = sub.add_parser("status", help="Current status of a running experiment")
    status_p.add_argument("--id", required=True)

    # report
    report_p = sub.add_parser("report", help="Final report for a completed experiment")
    report_p.add_argument("--id", required=True)

    # add-segmentation (patch an existing experiment)
    seg_p = sub.add_parser("add-segmentation",
        help="Add post-workout segmentation to an existing experiment")
    seg_p.add_argument("--id", required=True)
    seg_p.add_argument("--min-strain", type=float, default=5.0)
    seg_p.add_argument("--days-after", default="1-2")

    args = parser.parse_args()

    if args.command == "plan":
        cmd_plan(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "report":
        cmd_report(args)
    elif args.command == "add-segmentation":
        cmd_update_segmentation(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
