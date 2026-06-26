#!/usr/bin/env python3
"""SLO/Error Budget Calculator — Calculate uptime targets, allowed downtime, error budgets, and burn rates."""

import argparse
import json
import sys
from datetime import timedelta

VERSION = "1.0.0"

# Common SLO targets
COMMON_SLOS = {
    "99": 99.0,
    "99.9": 99.9,
    "99.95": 99.95,
    "99.99": 99.99,
    "99.999": 99.999,
    "two-nines": 99.0,
    "three-nines": 99.9,
    "four-nines": 99.99,
    "five-nines": 99.999,
}

PERIODS = {
    "year": timedelta(days=365),
    "quarter": timedelta(days=91),
    "month": timedelta(days=30),
    "week": timedelta(days=7),
    "day": timedelta(days=1),
}


def format_duration(seconds):
    """Format seconds into human-readable duration."""
    if seconds < 1:
        return f"{seconds * 1000:.1f}ms"
    if seconds < 60:
        return f"{seconds:.1f}s"
    if seconds < 3600:
        m = int(seconds // 60)
        s = seconds % 60
        return f"{m}m {s:.0f}s" if s >= 1 else f"{m}m"
    if seconds < 86400:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        return f"{h}h {m}m" if m > 0 else f"{h}h"
    d = int(seconds // 86400)
    h = int((seconds % 86400) // 3600)
    return f"{d}d {h}h" if h > 0 else f"{d}d"


def parse_slo(value):
    """Parse SLO value from string (e.g., '99.9', '99.9%', 'three-nines')."""
    value = value.strip().rstrip("%")
    if value.lower() in COMMON_SLOS:
        return COMMON_SLOS[value.lower()]
    try:
        slo = float(value)
        if 0 < slo <= 100:
            return slo
        raise ValueError
    except ValueError:
        print(f"Error: Invalid SLO value '{value}'. Use a percentage (e.g., 99.9) or alias (e.g., three-nines).", file=sys.stderr)
        sys.exit(1)


def cmd_budget(args):
    """Calculate error budget for given SLO and period."""
    slo = parse_slo(args.slo)
    error_pct = 100.0 - slo

    results = []
    periods = args.periods if args.periods else list(PERIODS.keys())

    for period_name in periods:
        if period_name not in PERIODS:
            print(f"Warning: Unknown period '{period_name}', skipping.", file=sys.stderr)
            continue
        total_seconds = PERIODS[period_name].total_seconds()
        allowed_downtime = total_seconds * (error_pct / 100.0)

        results.append({
            "period": period_name,
            "total_seconds": total_seconds,
            "slo_percent": slo,
            "error_budget_percent": round(error_pct, 6),
            "allowed_downtime_seconds": round(allowed_downtime, 2),
            "allowed_downtime_human": format_duration(allowed_downtime),
        })

    if args.format == "json":
        print(json.dumps(results, indent=2))
    elif args.format == "markdown":
        print(f"# Error Budget: {slo}% SLO\n")
        print("| Period | Allowed Downtime | Seconds |")
        print("|--------|-----------------|---------|")
        for r in results:
            print(f"| {r['period'].capitalize()} | {r['allowed_downtime_human']} | {r['allowed_downtime_seconds']}s |")
    else:
        print(f"SLO: {slo}% (error budget: {error_pct}%)\n")
        for r in results:
            print(f"  {r['period'].capitalize():>8}: {r['allowed_downtime_human']:>12}  ({r['allowed_downtime_seconds']}s)")


def cmd_burn(args):
    """Calculate burn rate and time to exhaust error budget."""
    slo = parse_slo(args.slo)
    error_pct = 100.0 - slo
    period = args.period

    if period not in PERIODS:
        print(f"Error: Unknown period '{period}'. Use: {', '.join(PERIODS.keys())}", file=sys.stderr)
        sys.exit(1)

    total_seconds = PERIODS[period].total_seconds()
    budget_seconds = total_seconds * (error_pct / 100.0)

    # Parse consumed downtime
    consumed = parse_duration(args.consumed)

    # Calculate
    budget_remaining = max(0, budget_seconds - consumed)
    budget_used_pct = min(100, (consumed / budget_seconds) * 100) if budget_seconds > 0 else 100

    # Burn rate: how fast budget is being consumed relative to ideal
    elapsed = parse_duration(args.elapsed) if args.elapsed else None
    burn_rate = None
    time_to_exhaust = None

    if elapsed and elapsed > 0:
        ideal_burn = elapsed / total_seconds  # fraction of period elapsed
        actual_burn = consumed / budget_seconds if budget_seconds > 0 else float('inf')
        burn_rate = actual_burn / ideal_burn if ideal_burn > 0 else float('inf')

        if burn_rate > 0 and budget_remaining > 0:
            # At current rate, how long until budget exhausted
            remaining_period = total_seconds - elapsed
            if remaining_period > 0:
                budget_burn_per_sec = consumed / elapsed if elapsed > 0 else 0
                if budget_burn_per_sec > 0:
                    time_to_exhaust = budget_remaining / budget_burn_per_sec

    result = {
        "slo_percent": slo,
        "period": period,
        "total_budget_seconds": round(budget_seconds, 2),
        "consumed_seconds": round(consumed, 2),
        "remaining_seconds": round(budget_remaining, 2),
        "remaining_human": format_duration(budget_remaining),
        "budget_used_percent": round(budget_used_pct, 2),
        "burn_rate": round(burn_rate, 3) if burn_rate is not None else None,
        "time_to_exhaust_seconds": round(time_to_exhaust, 2) if time_to_exhaust is not None else None,
        "time_to_exhaust_human": format_duration(time_to_exhaust) if time_to_exhaust is not None else None,
        "status": "EXHAUSTED" if budget_remaining <= 0 else "CRITICAL" if budget_used_pct > 90 else "WARNING" if budget_used_pct > 70 else "OK",
    }

    if args.format == "json":
        print(json.dumps(result, indent=2))
    elif args.format == "markdown":
        print(f"# Burn Rate: {slo}% SLO ({period})\n")
        print(f"| Metric | Value |")
        print(f"|--------|-------|")
        print(f"| Total Budget | {format_duration(budget_seconds)} |")
        print(f"| Consumed | {format_duration(consumed)} |")
        print(f"| Remaining | {result['remaining_human']} |")
        print(f"| Used | {result['budget_used_percent']}% |")
        print(f"| Status | {result['status']} |")
        if burn_rate is not None:
            print(f"| Burn Rate | {result['burn_rate']}x |")
        if time_to_exhaust is not None:
            print(f"| Time to Exhaust | {result['time_to_exhaust_human']} |")
    else:
        print(f"SLO: {slo}% | Period: {period} | Status: {result['status']}\n")
        print(f"  Budget:    {format_duration(budget_seconds)} total")
        print(f"  Consumed:  {format_duration(consumed)} ({budget_used_pct:.1f}%)")
        print(f"  Remaining: {result['remaining_human']}")
        if burn_rate is not None:
            print(f"  Burn rate: {burn_rate:.2f}x {'⚠️' if burn_rate > 1 else '✅'}")
        if time_to_exhaust is not None:
            print(f"  Exhausts in: {result['time_to_exhaust_human']}")


def parse_duration(s):
    """Parse duration string like '5m', '2h30m', '45s', '1d12h', or raw seconds."""
    s = s.strip()
    try:
        return float(s)
    except ValueError:
        pass

    total = 0
    current = ""
    for c in s:
        if c.isdigit() or c == '.':
            current += c
        elif c in ('d', 'h', 'm', 's'):
            if not current:
                continue
            val = float(current)
            if c == 'd':
                total += val * 86400
            elif c == 'h':
                total += val * 3600
            elif c == 'm':
                total += val * 60
            elif c == 's':
                total += val
            current = ""
        else:
            print(f"Error: Invalid duration '{s}'. Use format like '5m', '2h30m', '1d'.", file=sys.stderr)
            sys.exit(1)

    if current:
        # Trailing number without unit = seconds
        total += float(current)

    return total


def cmd_compare(args):
    """Compare multiple SLO targets side by side."""
    slos = [parse_slo(s) for s in args.slos]
    period = args.period

    if period not in PERIODS:
        print(f"Error: Unknown period '{period}'.", file=sys.stderr)
        sys.exit(1)

    total_seconds = PERIODS[period].total_seconds()

    results = []
    for slo in slos:
        error_pct = 100.0 - slo
        allowed = total_seconds * (error_pct / 100.0)
        results.append({
            "slo_percent": slo,
            "nines": count_nines(slo),
            "error_budget_percent": round(error_pct, 6),
            "allowed_downtime_seconds": round(allowed, 2),
            "allowed_downtime_human": format_duration(allowed),
        })

    if args.format == "json":
        print(json.dumps({"period": period, "comparisons": results}, indent=2))
    elif args.format == "markdown":
        print(f"# SLO Comparison ({period})\n")
        print("| SLO | Nines | Error Budget | Allowed Downtime |")
        print("|-----|-------|-------------|-----------------|")
        for r in results:
            print(f"| {r['slo_percent']}% | {r['nines']} | {r['error_budget_percent']}% | {r['allowed_downtime_human']} |")
    else:
        print(f"SLO Comparison (per {period}):\n")
        for r in results:
            print(f"  {r['slo_percent']:>8}% ({r['nines']:>1} nines): {r['allowed_downtime_human']:>12} downtime allowed")


def count_nines(slo):
    """Count number of nines in SLO percentage."""
    s = f"{slo:.10f}".rstrip('0')
    # Count 9s after the decimal if starts with 99
    if slo < 99:
        return 1 if slo >= 90 else 0
    count = 2  # two nines from 99
    after_dot = s.split('.')[1] if '.' in s else ''
    for c in after_dot:
        if c == '9':
            count += 1
        else:
            break
    return count


def cmd_uptime(args):
    """Calculate SLO from observed uptime/downtime."""
    period = args.period

    if period not in PERIODS:
        print(f"Error: Unknown period '{period}'.", file=sys.stderr)
        sys.exit(1)

    total_seconds = PERIODS[period].total_seconds()

    if args.downtime:
        down = parse_duration(args.downtime)
        up = total_seconds - down
    elif args.uptime_seconds:
        up = parse_duration(args.uptime_seconds)
        down = total_seconds - up
    else:
        print("Error: Provide --downtime or --uptime.", file=sys.stderr)
        sys.exit(1)

    uptime_pct = (up / total_seconds) * 100 if total_seconds > 0 else 0
    nines = count_nines(uptime_pct)

    # Check against common SLO targets
    meets = []
    fails = []
    for name, target in sorted(COMMON_SLOS.items(), key=lambda x: x[1]):
        if name in ("two-nines", "three-nines", "four-nines", "five-nines"):
            continue
        if uptime_pct >= target:
            meets.append(f"{target}%")
        else:
            fails.append(f"{target}%")

    result = {
        "period": period,
        "total_seconds": total_seconds,
        "uptime_seconds": round(up, 2),
        "downtime_seconds": round(down, 2),
        "downtime_human": format_duration(down),
        "uptime_percent": round(uptime_pct, 6),
        "nines": nines,
        "meets_slo": meets,
        "fails_slo": fails,
    }

    if args.format == "json":
        print(json.dumps(result, indent=2))
    elif args.format == "markdown":
        print(f"# Uptime Report ({period})\n")
        print(f"| Metric | Value |")
        print(f"|--------|-------|")
        print(f"| Uptime | {uptime_pct:.4f}% |")
        print(f"| Downtime | {result['downtime_human']} |")
        print(f"| Nines | {nines} |")
        print(f"| Meets | {', '.join(meets) if meets else 'None'} |")
        print(f"| Fails | {', '.join(fails) if fails else 'None'} |")
    else:
        print(f"Uptime: {uptime_pct:.4f}% ({nines} nines)")
        print(f"Downtime: {result['downtime_human']} ({round(down, 1)}s)")
        if meets:
            print(f"Meets: {', '.join(meets)}")
        if fails:
            print(f"Fails: {', '.join(fails)}")


def cmd_multi_window(args):
    """Multi-window SLO analysis (e.g., 30d, 7d, 1d rolling windows)."""
    slo = parse_slo(args.slo)
    error_pct = 100.0 - slo

    windows = []
    for spec in args.windows:
        parts = spec.split(":")
        if len(parts) != 2:
            print(f"Error: Window spec '{spec}' must be 'period:downtime' (e.g., 'month:15m').", file=sys.stderr)
            sys.exit(1)

        period_name, downtime_str = parts
        if period_name not in PERIODS:
            print(f"Error: Unknown period '{period_name}'.", file=sys.stderr)
            sys.exit(1)

        total = PERIODS[period_name].total_seconds()
        budget = total * (error_pct / 100.0)
        consumed = parse_duration(downtime_str)
        remaining = max(0, budget - consumed)
        used_pct = min(100, (consumed / budget) * 100) if budget > 0 else 100

        windows.append({
            "window": period_name,
            "budget_seconds": round(budget, 2),
            "budget_human": format_duration(budget),
            "consumed_seconds": round(consumed, 2),
            "consumed_human": format_duration(consumed),
            "remaining_seconds": round(remaining, 2),
            "remaining_human": format_duration(remaining),
            "used_percent": round(used_pct, 2),
            "status": "EXHAUSTED" if remaining <= 0 else "CRITICAL" if used_pct > 90 else "WARNING" if used_pct > 70 else "OK",
        })

    if args.format == "json":
        print(json.dumps({"slo_percent": slo, "windows": windows}, indent=2))
    elif args.format == "markdown":
        print(f"# Multi-Window SLO: {slo}%\n")
        print("| Window | Budget | Consumed | Remaining | Used | Status |")
        print("|--------|--------|----------|-----------|------|--------|")
        for w in windows:
            print(f"| {w['window'].capitalize()} | {w['budget_human']} | {w['consumed_human']} | {w['remaining_human']} | {w['used_percent']}% | {w['status']} |")
    else:
        print(f"SLO: {slo}% — Multi-Window Analysis\n")
        for w in windows:
            bar = "█" * int(w['used_percent'] / 5) + "░" * (20 - int(w['used_percent'] / 5))
            print(f"  {w['window'].capitalize():>8}: [{bar}] {w['used_percent']:>5.1f}% used — {w['remaining_human']} left — {w['status']}")


def cmd_table(args):
    """Print reference table of common SLO targets."""
    targets = [90.0, 95.0, 99.0, 99.5, 99.9, 99.95, 99.99, 99.999]
    period = args.period

    if period not in PERIODS:
        print(f"Error: Unknown period '{period}'.", file=sys.stderr)
        sys.exit(1)

    total = PERIODS[period].total_seconds()

    rows = []
    for slo in targets:
        error = 100.0 - slo
        allowed = total * (error / 100.0)
        rows.append({
            "slo_percent": slo,
            "nines": count_nines(slo),
            "error_percent": round(error, 6),
            "allowed_seconds": round(allowed, 2),
            "allowed_human": format_duration(allowed),
        })

    if args.format == "json":
        print(json.dumps({"period": period, "targets": rows}, indent=2))
    elif args.format == "markdown":
        print(f"# SLO Reference Table ({period})\n")
        print("| SLO | Nines | Error Budget | Allowed Downtime |")
        print("|-----|-------|-------------|-----------------|")
        for r in rows:
            print(f"| {r['slo_percent']}% | {r['nines']} | {r['error_percent']}% | {r['allowed_human']} |")
    else:
        print(f"SLO Reference Table (per {period}):\n")
        print(f"  {'SLO':>10}  {'Nines':>5}  {'Downtime':>14}")
        print(f"  {'─' * 10}  {'─' * 5}  {'─' * 14}")
        for r in rows:
            print(f"  {r['slo_percent']:>9}%  {r['nines']:>5}  {r['allowed_human']:>14}")


def main():
    parser = argparse.ArgumentParser(
        prog="slo",
        description="SLO/Error Budget Calculator — Calculate uptime targets, allowed downtime, error budgets, and burn rates.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")

    sub = parser.add_subparsers(dest="command", required=True)

    # budget
    p_budget = sub.add_parser("budget", help="Calculate error budget for an SLO target")
    p_budget.add_argument("slo", help="SLO target (e.g., 99.9, 99.9%%, three-nines)")
    p_budget.add_argument("periods", nargs="*", help="Periods to calculate (default: all)")
    p_budget.add_argument("-f", "--format", choices=["text", "json", "markdown"], default="text")

    # burn
    p_burn = sub.add_parser("burn", help="Calculate burn rate and remaining budget")
    p_burn.add_argument("slo", help="SLO target")
    p_burn.add_argument("consumed", help="Downtime consumed so far (e.g., 15m, 2h30m)")
    p_burn.add_argument("-p", "--period", default="month", help="SLO period (default: month)")
    p_burn.add_argument("-e", "--elapsed", help="Time elapsed in period (e.g., 15d)")
    p_burn.add_argument("-f", "--format", choices=["text", "json", "markdown"], default="text")

    # compare
    p_compare = sub.add_parser("compare", help="Compare multiple SLO targets")
    p_compare.add_argument("slos", nargs="+", help="SLO targets to compare")
    p_compare.add_argument("-p", "--period", default="month", help="Period (default: month)")
    p_compare.add_argument("-f", "--format", choices=["text", "json", "markdown"], default="text")

    # uptime
    p_uptime = sub.add_parser("uptime", help="Calculate SLO from observed downtime")
    p_uptime.add_argument("-p", "--period", default="month", help="Period (default: month)")
    p_uptime.add_argument("-d", "--downtime", help="Total downtime (e.g., 15m, 2h)")
    p_uptime.add_argument("-u", "--uptime-seconds", help="Total uptime")
    p_uptime.add_argument("-f", "--format", choices=["text", "json", "markdown"], default="text")

    # multi-window
    p_multi = sub.add_parser("multi-window", help="Multi-window SLO analysis")
    p_multi.add_argument("slo", help="SLO target")
    p_multi.add_argument("windows", nargs="+", help="Window specs as period:downtime (e.g., month:15m week:3m day:30s)")
    p_multi.add_argument("-f", "--format", choices=["text", "json", "markdown"], default="text")

    # table
    p_table = sub.add_parser("table", help="Print SLO reference table")
    p_table.add_argument("-p", "--period", default="month", help="Period (default: month)")
    p_table.add_argument("-f", "--format", choices=["text", "json", "markdown"], default="text")

    args = parser.parse_args()

    commands = {
        "budget": cmd_budget,
        "burn": cmd_burn,
        "compare": cmd_compare,
        "uptime": cmd_uptime,
        "multi-window": cmd_multi_window,
        "table": cmd_table,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
