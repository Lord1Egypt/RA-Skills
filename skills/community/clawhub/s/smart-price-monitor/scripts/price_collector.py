#!/usr/bin/env python3
"""
Smart Price Monitor - Data Collection & Analysis Engine
Collects prices, analyzes trends, and generates alerts.
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean, stdev

# ─── Configuration ───────────────────────────────────────────────────────────

DATA_DIR = Path(os.environ.get("PRICE_MONITOR_DATA", "./price-monitor-data"))
MONITORS_FILE = DATA_DIR / "monitors.json"
HISTORY_DIR = DATA_DIR / "history"
REPORTS_DIR = DATA_DIR / "reports"
ALERTS_DIR = DATA_DIR / "alerts"


def ensure_dirs():
    """Create data directories if they don't exist."""
    for d in [DATA_DIR, HISTORY_DIR, REPORTS_DIR, ALERTS_DIR]:
        d.mkdir(parents=True, exist_ok=True)


# ─── Monitor Management ─────────────────────────────────────────────────────

def load_monitors() -> dict:
    """Load monitoring configurations."""
    if MONITORS_FILE.exists():
        return json.loads(MONITORS_FILE.read_text())
    return {
        "monitors": [],
        "settings": {
            "currency": "USD",
            "timezone": "America/Los_Angeles",
            "report_format": "markdown"
        }
    }


def save_monitors(data: dict):
    """Save monitoring configurations."""
    ensure_dirs()
    MONITORS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def add_monitor(name: str, source: str, monitor_type: str = "product_url",
                check_interval: str = "6h", price_drop_pct: float = 5.0,
                price_target: float = None, restock_alert: bool = False) -> str:
    """Add a new monitoring target. Returns the monitor ID."""
    data = load_monitors()
    monitor_id = f"monitor-{len(data['monitors']) + 1:03d}"

    monitor = {
        "id": monitor_id,
        "name": name,
        "type": monitor_type,
        "source": source,
        "check_interval": check_interval,
        "alert_rules": {
            "price_drop_pct": price_drop_pct,
            "price_target": price_target,
            "restock_alert": restock_alert
        },
        "created_at": datetime.now(timezone.utc).isoformat(),
        "last_checked": None,
        "status": "active"
    }

    data["monitors"].append(monitor)
    save_monitors(data)
    return monitor_id


def remove_monitor(monitor_id: str) -> bool:
    """Remove a monitoring target."""
    data = load_monitors()
    data["monitors"] = [m for m in data["monitors"] if m["id"] != monitor_id]
    save_monitors(data)
    return True


def list_monitors() -> list:
    """List all active monitors with their latest prices."""
    data = load_monitors()
    result = []
    for m in data["monitors"]:
        history = load_history(m["id"])
        latest = history[-1] if history else None
        result.append({
            "id": m["id"],
            "name": m["name"],
            "source": m["source"],
            "status": m.get("status", "active"),
            "latest_price": latest["price"] if latest else None,
            "last_checked": latest["timestamp"] if latest else None,
            "alert_rules": m["alert_rules"]
        })
    return result


# ─── History Management ──────────────────────────────────────────────────────

def load_history(monitor_id: str) -> list:
    """Load price history for a monitor."""
    history_file = HISTORY_DIR / f"{monitor_id}.json"
    if history_file.exists():
        return json.loads(history_file.read_text())
    return []


def save_history(monitor_id: str, history: list):
    """Save price history for a monitor."""
    ensure_dirs()
    history_file = HISTORY_DIR / f"{monitor_id}.json"
    history_file.write_text(json.dumps(history, indent=2, ensure_ascii=False))


def add_price_entry(monitor_id: str, price: float, original_price: float = None,
                    currency: str = "USD", in_stock: bool = True,
                    seller: str = None, shipping: str = None,
                    source_url: str = None) -> dict:
    """Record a new price data point."""
    history = load_history(monitor_id)

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "price": price,
        "original_price": original_price,
        "currency": currency,
        "in_stock": in_stock,
        "seller": seller,
        "shipping": shipping,
        "source_url": source_url
    }

    history.append(entry)
    save_history(monitor_id, history)
    return entry


# ─── Analysis ────────────────────────────────────────────────────────────────

def calculate_deal_score(current_price: float, history: list) -> int:
    """Calculate deal score (0-100). Higher = better deal."""
    if not history or len(history) < 2:
        return 50  # Not enough data

    prices = [h["price"] for h in history if h.get("price")]
    if not prices:
        return 50

    avg_price = mean(prices)
    if avg_price == 0:
        return 50

    score = ((avg_price - current_price) / avg_price) * 200 + 50
    return max(0, min(100, int(score)))


def analyze_trend(history: list, window_days: int = 30) -> dict:
    """Analyze price trends over a given window."""
    if not history:
        return {"direction": "unknown", "change_pct": 0, "volatility": "low"}

    cutoff = datetime.now(timezone.utc) - timedelta(days=window_days)
    recent = []
    for h in history:
        try:
            ts = datetime.fromisoformat(h["timestamp"].replace("Z", "+00:00"))
            if ts >= cutoff:
                recent.append(h)
        except (ValueError, KeyError):
            continue

    if len(recent) < 2:
        return {"direction": "insufficient_data", "change_pct": 0, "volatility": "unknown"}

    prices = [h["price"] for h in recent]
    first_price = prices[0]
    last_price = prices[-1]
    change_pct = ((last_price - first_price) / first_price) * 100 if first_price else 0

    # Determine direction
    if change_pct > 2:
        direction = "rising"
    elif change_pct < -2:
        direction = "falling"
    else:
        direction = "stable"

    # Calculate volatility
    if len(prices) >= 3:
        price_stdev = stdev(prices)
        avg = mean(prices)
        cv = (price_stdev / avg) * 100 if avg else 0
        volatility = "high" if cv > 10 else ("medium" if cv > 5 else "low")
    else:
        volatility = "unknown"

    return {
        "direction": direction,
        "change_pct": round(change_pct, 2),
        "volatility": volatility,
        "min_price": min(prices),
        "max_price": max(prices),
        "avg_price": round(mean(prices), 2),
        "data_points": len(prices),
        "period_days": window_days
    }


def get_price_stats(monitor_id: str) -> dict:
    """Get comprehensive price statistics for a monitor."""
    history = load_history(monitor_id)
    if not history:
        return {"error": "No price data available"}

    prices = [h["price"] for h in history if h.get("price")]
    if not prices:
        return {"error": "No valid prices in history"}

    current = prices[-1]
    return {
        "current_price": current,
        "min_price": min(prices),
        "max_price": max(prices),
        "avg_price": round(mean(prices), 2),
        "stdev": round(stdev(prices), 2) if len(prices) > 1 else 0,
        "total_entries": len(prices),
        "deal_score": calculate_deal_score(current, history),
        "trend_30d": analyze_trend(history, 30),
        "trend_7d": analyze_trend(history, 7),
        "first_seen": history[0]["timestamp"],
        "last_updated": history[-1]["timestamp"]
    }


# ─── Alert Detection ────────────────────────────────────────────────────────

def check_alerts(monitor_id: str) -> list:
    """Check if any alert conditions are met for a monitor."""
    data = load_monitors()
    monitor = next((m for m in data["monitors"] if m["id"] == monitor_id), None)
    if not monitor:
        return []

    history = load_history(monitor_id)
    if len(history) < 2:
        return []

    alerts = []
    current = history[-1]
    previous = history[-2]
    rules = monitor["alert_rules"]
    prices = [h["price"] for h in history if h.get("price")]

    # Price drop alert
    if previous["price"] and current["price"]:
        drop_pct = ((previous["price"] - current["price"]) / previous["price"]) * 100
        if drop_pct >= rules.get("price_drop_pct", 5):
            alerts.append({
                "type": "PRICE_DROP",
                "monitor_id": monitor_id,
                "monitor_name": monitor["name"],
                "current_price": current["price"],
                "previous_price": previous["price"],
                "drop_pct": round(drop_pct, 1),
                "savings": round(previous["price"] - current["price"], 2),
                "deal_score": calculate_deal_score(current["price"], history),
                "timestamp": current["timestamp"]
            })

    # Target price alert
    target = rules.get("price_target")
    if target and current["price"] and current["price"] <= target:
        alerts.append({
            "type": "TARGET_REACHED",
            "monitor_id": monitor_id,
            "monitor_name": monitor["name"],
            "current_price": current["price"],
            "target_price": target,
            "timestamp": current["timestamp"]
        })

    # New all-time low
    if prices and current["price"] and current["price"] <= min(prices[:-1]):
        alerts.append({
            "type": "NEW_LOW",
            "monitor_id": monitor_id,
            "monitor_name": monitor["name"],
            "current_price": current["price"],
            "previous_low": min(prices[:-1]),
            "timestamp": current["timestamp"]
        })

    # Restock alert
    if rules.get("restock_alert"):
        if not previous.get("in_stock") and current.get("in_stock"):
            alerts.append({
                "type": "RESTOCK",
                "monitor_id": monitor_id,
                "monitor_name": monitor["name"],
                "current_price": current["price"],
                "timestamp": current["timestamp"]
            })

    # Save alerts
    if alerts:
        save_alerts(alerts)

    return alerts


def save_alerts(new_alerts: list):
    """Save generated alerts."""
    ensure_dirs()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    alerts_file = ALERTS_DIR / f"alerts-{today}.json"

    existing = []
    if alerts_file.exists():
        existing = json.loads(alerts_file.read_text())

    existing.extend(new_alerts)
    alerts_file.write_text(json.dumps(existing, indent=2, ensure_ascii=False))


# ─── Report Generation ───────────────────────────────────────────────────────

def generate_daily_report() -> str:
    """Generate a daily summary report in markdown."""
    data = load_monitors()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    lines = [
        f"# Price Monitor Daily Report — {today}",
        "",
        f"**Monitors Active:** {len(data['monitors'])}",
        "",
        "## Current Prices",
        "",
        "| Product | Current Price | Change | Deal Score | Status |",
        "|---------|-------------|--------|------------|--------|"
    ]

    deals = []

    for m in data["monitors"]:
        history = load_history(m["id"])
        if not history:
            lines.append(f"| {m['name']} | — | — | — | No data |")
            continue

        current = history[-1]
        price = current.get("price", 0)
        in_stock = current.get("in_stock", True)

        # Calculate change
        if len(history) >= 2:
            prev = history[-2]["price"]
            if prev and price:
                change = ((price - prev) / prev) * 100
                change_str = f"{'+'if change > 0 else ''}{change:.1f}%"
            else:
                change_str = "—"
        else:
            change_str = "New"

        score = calculate_deal_score(price, history) if price else 0
        status = "In Stock" if in_stock else "Out of Stock"

        lines.append(
            f"| {m['name']} | ${price:,.2f} | {change_str} | {score}/100 | {status} |"
        )

        if score >= 70:
            deals.append((m["name"], price, score))

    # Top deals section
    if deals:
        lines.extend(["", "## Top Deals Today", ""])
        deals.sort(key=lambda x: x[2], reverse=True)
        for name, price, score in deals:
            emoji = "🔥" if score >= 90 else ("⭐" if score >= 80 else "👍")
            lines.append(f"- {emoji} **{name}** — ${price:,.2f} (Deal Score: {score}/100)")

    # Alerts section
    alerts_file = ALERTS_DIR / f"alerts-{today}.json"
    if alerts_file.exists():
        alerts = json.loads(alerts_file.read_text())
        if alerts:
            lines.extend(["", "## Alerts", ""])
            for a in alerts:
                if a["type"] == "PRICE_DROP":
                    lines.append(
                        f"- **PRICE DROP** {a['monitor_name']}: "
                        f"${a['current_price']:,.2f} (-{a['drop_pct']}%)"
                    )
                elif a["type"] == "TARGET_REACHED":
                    lines.append(
                        f"- **TARGET REACHED** {a['monitor_name']}: "
                        f"${a['current_price']:,.2f} (target: ${a['target_price']:,.2f})"
                    )
                elif a["type"] == "RESTOCK":
                    lines.append(f"- **RESTOCKED** {a['monitor_name']}")
                elif a["type"] == "NEW_LOW":
                    lines.append(
                        f"- **NEW ALL-TIME LOW** {a['monitor_name']}: "
                        f"${a['current_price']:,.2f}"
                    )

    report = "\n".join(lines)

    # Save report
    ensure_dirs()
    report_file = REPORTS_DIR / f"daily-{today}.md"
    report_file.write_text(report)

    return report


def generate_comparison_table(monitor_ids: list = None) -> str:
    """Generate a price comparison table across monitors."""
    data = load_monitors()
    monitors = data["monitors"]
    if monitor_ids:
        monitors = [m for m in monitors if m["id"] in monitor_ids]

    lines = [
        "# Price Comparison",
        "",
        "| Product | Price | Seller | Shipping | In Stock | Deal Score |",
        "|---------|-------|--------|----------|----------|------------|"
    ]

    for m in monitors:
        history = load_history(m["id"])
        if not history:
            continue
        latest = history[-1]
        score = calculate_deal_score(latest.get("price", 0), history)
        lines.append(
            f"| {m['name']} | ${latest.get('price', 0):,.2f} | "
            f"{latest.get('seller', '—')} | {latest.get('shipping', '—')} | "
            f"{'Yes' if latest.get('in_stock') else 'No'} | {score}/100 |"
        )

    return "\n".join(lines)


# ─── CLI Interface ───────────────────────────────────────────────────────────

def main():
    """CLI entry point for the price monitor."""
    if len(sys.argv) < 2:
        print("Usage: python price_collector.py <command> [args]")
        print("Commands: add, remove, list, record, stats, alerts, report, compare")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "add":
        if len(sys.argv) < 4:
            print("Usage: add <name> <source> [type] [interval] [drop_pct] [target]")
            sys.exit(1)
        name = sys.argv[2]
        source = sys.argv[3]
        mtype = sys.argv[4] if len(sys.argv) > 4 else "product_url"
        interval = sys.argv[5] if len(sys.argv) > 5 else "6h"
        drop_pct = float(sys.argv[6]) if len(sys.argv) > 6 else 5.0
        target = float(sys.argv[7]) if len(sys.argv) > 7 else None
        mid = add_monitor(name, source, mtype, interval, drop_pct, target)
        print(f"Monitor created: {mid}")

    elif cmd == "remove":
        remove_monitor(sys.argv[2])
        print(f"Monitor {sys.argv[2]} removed")

    elif cmd == "list":
        monitors = list_monitors()
        print(json.dumps(monitors, indent=2, ensure_ascii=False))

    elif cmd == "record":
        if len(sys.argv) < 4:
            print("Usage: record <monitor_id> <price> [in_stock] [seller] [shipping]")
            sys.exit(1)
        mid = sys.argv[2]
        price = float(sys.argv[3])
        in_stock = sys.argv[4].lower() == "true" if len(sys.argv) > 4 else True
        seller = sys.argv[5] if len(sys.argv) > 5 else None
        shipping = sys.argv[6] if len(sys.argv) > 6 else None
        entry = add_price_entry(mid, price, in_stock=in_stock, seller=seller, shipping=shipping)
        print(f"Recorded: ${price} at {entry['timestamp']}")

    elif cmd == "stats":
        mid = sys.argv[2] if len(sys.argv) > 2 else None
        if mid:
            stats = get_price_stats(mid)
            print(json.dumps(stats, indent=2))
        else:
            data = load_monitors()
            for m in data["monitors"]:
                print(f"\n--- {m['name']} ({m['id']}) ---")
                stats = get_price_stats(m["id"])
                print(json.dumps(stats, indent=2))

    elif cmd == "alerts":
        mid = sys.argv[2] if len(sys.argv) > 2 else None
        if mid:
            alerts = check_alerts(mid)
            print(json.dumps(alerts, indent=2))
        else:
            data = load_monitors()
            all_alerts = []
            for m in data["monitors"]:
                all_alerts.extend(check_alerts(m["id"]))
            print(json.dumps(all_alerts, indent=2))

    elif cmd == "report":
        report = generate_daily_report()
        print(report)

    elif cmd == "compare":
        ids = sys.argv[2:] if len(sys.argv) > 2 else None
        table = generate_comparison_table(ids)
        print(table)

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
