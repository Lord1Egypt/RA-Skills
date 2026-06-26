#!/usr/bin/env python3
"""Revenue Dashboard — consolidated Stripe metrics with goals and anomaly detection.

Pulls charges and refunds across multiple Stripe accounts with period comparison,
goal tracking, and anomaly flagging.

Usage:
    python3 revenue.py --period today
    python3 revenue.py --period yesterday --format markdown --goals --anomalies
    python3 revenue.py --period month --format summary
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# --- Config ---
CONFIG_PATH = os.path.expanduser("~/.config/revenue-dashboard/config.json")
STRIPE_KEY_PATH = os.path.expanduser("~/.config/stripe/api_key")


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {"accounts": {}, "goals": {}, "currency": "usd", "anomaly_threshold": 2.0}


def load_stripe_key():
    if not os.path.exists(STRIPE_KEY_PATH):
        print(json.dumps({"error": f"Stripe key not found at {STRIPE_KEY_PATH}. Create it with your Stripe secret key."}))
        sys.exit(1)
    return open(STRIPE_KEY_PATH).read().strip()


def parse_args():
    args = {
        "period": "today",
        "format": "json",
        "goals": False,
        "anomalies": False,
    }
    argv = sys.argv[1:]
    i = 0
    while i < len(argv):
        if argv[i] == "--period" and i + 1 < len(argv):
            args["period"] = argv[i + 1]
            i += 2
        elif argv[i] == "--format" and i + 1 < len(argv):
            args["format"] = argv[i + 1]
            i += 2
        elif argv[i] == "--goals":
            args["goals"] = True
            i += 1
        elif argv[i] == "--anomalies":
            args["anomalies"] = True
            i += 1
        else:
            i += 1
    return args


def get_period_range(period):
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    periods = {
        "today": (today_start, now, today_start - timedelta(days=1), today_start),
        "yesterday": (today_start - timedelta(days=1), today_start, today_start - timedelta(days=2), today_start - timedelta(days=1)),
        "week": (now - timedelta(days=7), now, now - timedelta(days=14), now - timedelta(days=7)),
        "month": (now - timedelta(days=30), now, now - timedelta(days=60), now - timedelta(days=30)),
        "quarter": (now - timedelta(days=90), now, now - timedelta(days=180), now - timedelta(days=90)),
        "year": (now - timedelta(days=365), now, now - timedelta(days=730), now - timedelta(days=365)),
        "all": (datetime(2020, 1, 1, tzinfo=timezone.utc), now, None, None),
    }

    if period in periods:
        return periods[period]

    return periods["today"]


def stripe_api(endpoint, stripe_key, acct_id=None):
    """Make a Stripe API request with pagination support."""
    headers = ["-u", f"{stripe_key}:", "-H", "Stripe-Version: 2025-01-27.acacia"]
    if acct_id:
        headers.extend(["-H", f"Stripe-Account: {acct_id}"])

    all_data = []
    url = f"https://api.stripe.com/v1/{endpoint}"

    while url:
        result = subprocess.run(
            ["curl", "-s", "-g", url] + headers,
            capture_output=True, text=True
        )
        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            break

        if "error" in data:
            return {"error": data["error"].get("message", "Unknown error")}

        items = data.get("data", [])
        all_data.extend(items)

        if data.get("has_more") and items:
            separator = "&" if "?" in endpoint else "?"
            url = f"https://api.stripe.com/v1/{endpoint}{separator}starting_after={items[-1]['id']}"
        else:
            url = None

    return all_data


def fetch_charges(stripe_key, acct_id, start, end):
    ts_start = int(start.timestamp())
    ts_end = int(end.timestamp())
    endpoint = f"charges?limit=100&created[gte]={ts_start}&created[lt]={ts_end}"
    data = stripe_api(endpoint, stripe_key, acct_id)

    if isinstance(data, dict) and "error" in data:
        return [], data["error"]

    charges = [c for c in data if c.get("paid") and not c.get("refunded")]
    return charges, None


def fetch_refunds(stripe_key, acct_id, start, end):
    ts_start = int(start.timestamp())
    ts_end = int(end.timestamp())
    endpoint = f"refunds?limit=100&created[gte]={ts_start}&created[lt]={ts_end}"
    data = stripe_api(endpoint, stripe_key, acct_id)

    if isinstance(data, dict) and "error" in data:
        return 0, data["error"]

    total = sum(r.get("amount", 0) for r in data)
    return total, None


def fetch_7day_history(stripe_key, acct_id):
    """Fetch last 7 days of daily revenue for anomaly detection."""
    now = datetime.now(timezone.utc)
    daily = []
    for d in range(1, 8):
        day_start = (now - timedelta(days=d)).replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        charges, err = fetch_charges(stripe_key, acct_id, day_start, day_end)
        if err:
            daily.append(0)
        else:
            daily.append(sum(c["amount"] for c in charges))
    return daily


def detect_anomalies(today_gross, history, threshold):
    """Flag anomalies based on 7-day history."""
    if not history or all(h == 0 for h in history):
        return []

    avg = sum(history) / len(history)
    flags = []

    if avg > 0:
        ratio = today_gross / avg
        if ratio > threshold:
            flags.append(f"Revenue spike: {ratio:.1f}x vs 7-day average (${today_gross/100:.2f} vs avg ${avg/100:.2f})")
        elif ratio < (1 / threshold) and today_gross > 0:
            flags.append(f"Revenue drop: {ratio:.1f}x vs 7-day average (${today_gross/100:.2f} vs avg ${avg/100:.2f})")

    if today_gross == 0 and avg > 0:
        flags.append("Zero revenue day — investigate if this is expected")

    return flags


def calculate_goals(net_revenue, goals, period):
    """Calculate goal progress."""
    if not goals:
        return None

    result = {}
    monthly_goal = goals.get("monthly", 0)
    annual_goal = goals.get("annual", 0)
    now = datetime.now(timezone.utc)

    if monthly_goal and period in ("today", "yesterday", "week", "month"):
        day_of_month = now.day
        days_in_month = 30
        if period == "month":
            progress = (net_revenue / monthly_goal) * 100
            pace = (net_revenue / day_of_month) * days_in_month if day_of_month > 0 else 0
            result["monthly"] = {
                "goal": monthly_goal,
                "current": round(net_revenue, 2),
                "progress_pct": round(progress, 1),
                "projected": round(pace, 2),
                "status": "on_pace" if pace >= monthly_goal else "behind",
                "days_remaining": days_in_month - day_of_month,
            }

    if annual_goal and period in ("year", "all"):
        day_of_year = now.timetuple().tm_yday
        progress = (net_revenue / annual_goal) * 100
        pace = (net_revenue / day_of_year) * 365 if day_of_year > 0 else 0
        result["annual"] = {
            "goal": annual_goal,
            "current": round(net_revenue, 2),
            "progress_pct": round(progress, 1),
            "projected": round(pace, 2),
            "status": "on_pace" if pace >= annual_goal else "behind",
        }

    return result if result else None


def format_markdown(results):
    """Format results as a markdown report."""
    lines = [f"## Revenue Report — {results['period'].title()}"]
    lines.append("")

    # Account table
    lines.append("| Account | Gross | Refunds | Net | Txns | Avg Ticket | vs Prior |")
    lines.append("|---------|-------|---------|-----|------|------------|----------|")

    for name, data in results["accounts"].items():
        if "error" in data:
            lines.append(f"| {name} | ⚠️ Error: {data['error']} | | | | | |")
            continue
        growth = f"{data.get('growth_pct', 'N/A')}%" if data.get("growth_pct") is not None else "N/A"
        avg_ticket = f"${data.get('avg_ticket', 0):.2f}"
        lines.append(f"| {name} | ${data['gross']:.2f} | ${data['refunds']:.2f} | ${data['net']:.2f} | {data['transactions']} | {avg_ticket} | {growth} |")

    t = results["total"]
    growth = f"{t.get('growth_pct', 'N/A')}%" if t.get("growth_pct") is not None else "N/A"
    avg_ticket = f"${t.get('avg_ticket', 0):.2f}"
    lines.append(f"| **Total** | **${t['gross']:.2f}** | **${t['refunds']:.2f}** | **${t['net']:.2f}** | **{t['transactions']}** | **{avg_ticket}** | **{growth}** |")

    if t.get("refund_rate") is not None:
        lines.append(f"\nRefund rate: {t['refund_rate']}%")

    # Goals
    if results.get("goals"):
        lines.append("\n### Goal Progress")
        for period_name, g in results["goals"].items():
            status_emoji = "✅" if g["status"] == "on_pace" else "⚠️"
            lines.append(f"- **{period_name.title()}:** ${g['current']:.2f} / ${g['goal']:.2f} ({g['progress_pct']}%) — Projected: ${g['projected']:.2f} {status_emoji}")

    # Anomalies
    if results.get("anomalies"):
        lines.append("\n### ⚠️ Anomalies Detected")
        for flag in results["anomalies"]:
            lines.append(f"- {flag}")

    return "\n".join(lines)


def format_summary(results):
    """Format as a brief text summary."""
    t = results["total"]
    growth_str = f" ({t['growth_pct']:+.1f}% vs prior)" if t.get("growth_pct") is not None else ""
    summary = f"Revenue ({results['period']}): ${t['net']:.2f} net{growth_str}, {t['transactions']} transactions"

    if results.get("goals"):
        for period_name, g in results["goals"].items():
            status = "on pace" if g["status"] == "on_pace" else "behind pace"
            summary += f" | {period_name} goal: {g['progress_pct']}% ({status})"

    if results.get("anomalies"):
        summary += f" | ⚠️ {len(results['anomalies'])} anomal{'y' if len(results['anomalies']) == 1 else 'ies'}"

    return summary


def main():
    args = parse_args()
    config = load_config()
    stripe_key = load_stripe_key()

    accounts = config.get("accounts", {})
    if not accounts:
        print(json.dumps({"error": "No Stripe accounts configured. Edit ~/.config/revenue-dashboard/config.json"}))
        sys.exit(1)

    start, end, cmp_start, cmp_end = get_period_range(args["period"])
    threshold = config.get("anomaly_threshold", 2.0)

    results = {"period": args["period"], "accounts": {}, "total": {}}
    total_gross = total_refunds = total_count = 0
    total_cmp_gross = 0
    all_anomalies = []

    for name, acct_id in accounts.items():
        charges, err = fetch_charges(stripe_key, acct_id, start, end)
        if err:
            results["accounts"][name] = {"error": err}
            continue

        gross = sum(c["amount"] for c in charges)
        refunds, ref_err = fetch_refunds(stripe_key, acct_id, start, end)
        if ref_err:
            refunds = 0

        net = gross - refunds
        count = len(charges)
        avg_ticket = (gross / count / 100) if count > 0 else 0

        entry = {
            "gross": gross / 100,
            "refunds": refunds / 100,
            "net": net / 100,
            "transactions": count,
            "avg_ticket": avg_ticket,
        }

        if gross > 0:
            entry["refund_rate"] = round((refunds / gross) * 100, 1)

        # Period comparison
        if cmp_start and cmp_end:
            cmp_charges, cmp_err = fetch_charges(stripe_key, acct_id, cmp_start, cmp_end)
            if not cmp_err:
                cmp_gross = sum(c["amount"] for c in cmp_charges)
                entry["prior_gross"] = cmp_gross / 100
                entry["growth_pct"] = round((gross - cmp_gross) / cmp_gross * 100, 1) if cmp_gross else None
                total_cmp_gross += cmp_gross

        # Anomaly detection
        if args["anomalies"] and args["period"] in ("today", "yesterday"):
            history = fetch_7day_history(stripe_key, acct_id)
            flags = detect_anomalies(gross, history, threshold)
            if flags:
                all_anomalies.extend([f"[{name}] {f}" for f in flags])
            if gross > 0 and refunds / gross > 0.10:
                all_anomalies.append(f"[{name}] High refund rate: {refunds/gross*100:.1f}%")

        results["accounts"][name] = entry
        total_gross += gross
        total_refunds += refunds
        total_count += count

    # Totals
    total_net = (total_gross - total_refunds) / 100
    results["total"] = {
        "gross": total_gross / 100,
        "refunds": total_refunds / 100,
        "net": total_net,
        "transactions": total_count,
        "avg_ticket": (total_gross / total_count / 100) if total_count > 0 else 0,
    }
    if total_gross > 0:
        results["total"]["refund_rate"] = round((total_refunds / total_gross) * 100, 1)
    if cmp_start and cmp_end:
        results["total"]["prior_gross"] = total_cmp_gross / 100
        results["total"]["growth_pct"] = round((total_gross - total_cmp_gross) / total_cmp_gross * 100, 1) if total_cmp_gross else None

    # Goals
    if args["goals"]:
        goal_data = calculate_goals(total_net, config.get("goals", {}), args["period"])
        if goal_data:
            results["goals"] = goal_data

    # Anomalies
    if args["anomalies"] and all_anomalies:
        results["anomalies"] = all_anomalies

    # Output
    if args["format"] == "markdown":
        print(format_markdown(results))
    elif args["format"] == "summary":
        print(format_summary(results))
    else:
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
