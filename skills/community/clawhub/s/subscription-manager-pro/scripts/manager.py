#!/usr/bin/env python3
"""
Subscription Manager Pro - Track and manage all your subscriptions
"""

import json
import os
import sys
import uuid
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any

# Data directory
DATA_DIR = Path(os.path.expanduser("~/.openclaw/workspace/subscription-manager-pro/data"))
SUBS_FILE = DATA_DIR / "subscriptions.json"
HISTORY_FILE = DATA_DIR / "history.json"

# Category keywords for auto-detection
CATEGORY_KEYWORDS = {
    "entertainment": ["netflix", "spotify", "disney", "hulu", "hbo", "amazon prime video", 
                      "apple tv", "youtube", "twitch", "paramount", "peacock", "crunchyroll",
                      "audible", "kindle unlimited", "xbox", "playstation", "nintendo", "steam"],
    "software": ["adobe", "office 365", "microsoft 365", "jetbrains", "sketch", "figma",
                 "notion", "todoist", "1password", "lastpass", "bitwarden", "dropbox",
                 "google workspace", "zoom", "slack", "canva", "grammarly"],
    "cloud": ["aws", "amazon web services", "azure", "google cloud", "gcp", "digitalocean",
              "vercel", "netlify", "heroku", "cloudflare", "linode", "vultr", "railway"],
    "news": ["nyt", "new york times", "wsj", "wall street journal", "washington post",
             "economist", "substack", "medium", "patreon", "bloomberg"],
    "fitness": ["gym", "peloton", "planet fitness", "strava", "myfitnesspal", "headspace",
                "calm", "noom", "weight watchers", "fitbit"],
    "education": ["coursera", "udemy", "skillshare", "linkedin learning", "masterclass",
                  "brilliant", "duolingo", "rosetta stone", "codecademy", "pluralsight"],
    "utilities": ["phone", "internet", "electricity", "gas", "water", "insurance", "verizon",
                  "at&t", "t-mobile", "comcast", "spectrum"],
    "shopping": ["amazon prime", "costco", "walmart+", "instacart", "doordash", "uber eats"],
    "ai": ["chatgpt", "claude", "anthropic", "openai", "midjourney", "copilot", "perplexity",
           "jasper", "copy.ai", "writesonic"],
}

def ensure_data_dir():
    """Create data directory if it doesn't exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_subscriptions() -> List[Dict[str, Any]]:
    """Load subscriptions from JSON file."""
    ensure_data_dir()
    if SUBS_FILE.exists():
        with open(SUBS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_subscriptions(subs: List[Dict[str, Any]]):
    """Save subscriptions to JSON file."""
    ensure_data_dir()
    with open(SUBS_FILE, 'w') as f:
        json.dump(subs, f, indent=2, default=str)

def detect_category(name: str) -> str:
    """Auto-detect category based on service name."""
    name_lower = name.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in name_lower:
                return category
    return "other"

def get_category_emoji(category: str) -> str:
    """Get emoji for category."""
    emojis = {
        "entertainment": "🎬",
        "software": "💻",
        "cloud": "☁️",
        "news": "📰",
        "fitness": "🏋️",
        "education": "📚",
        "utilities": "🔧",
        "shopping": "🛒",
        "ai": "🤖",
        "other": "📦"
    }
    return emojis.get(category, "📦")

def parse_cost(cost_str: str) -> tuple:
    """Parse cost string like '$15.99' or '15.99 USD'."""
    cost_str = cost_str.strip().replace(',', '')
    # Remove currency symbols
    for symbol in ['$', '€', '£', '¥']:
        cost_str = cost_str.replace(symbol, '')
    # Extract number
    try:
        cost = float(cost_str.split()[0])
        return cost, "USD"  # Default to USD
    except:
        return 0.0, "USD"

def parse_cycle(cycle_str: str) -> str:
    """Parse billing cycle string."""
    cycle_lower = cycle_str.lower()
    if any(x in cycle_lower for x in ['year', 'annual', 'yearly']):
        return "yearly"
    elif any(x in cycle_lower for x in ['quarter', 'quarterly']):
        return "quarterly"
    elif any(x in cycle_lower for x in ['week', 'weekly']):
        return "weekly"
    return "monthly"

def calculate_monthly_cost(cost: float, cycle: str) -> float:
    """Convert any billing cycle to monthly cost."""
    if cycle == "yearly":
        return cost / 12
    elif cycle == "quarterly":
        return cost / 3
    elif cycle == "weekly":
        return cost * 4.33
    return cost

def calculate_yearly_cost(cost: float, cycle: str) -> float:
    """Convert any billing cycle to yearly cost."""
    if cycle == "yearly":
        return cost
    elif cycle == "quarterly":
        return cost * 4
    elif cycle == "weekly":
        return cost * 52
    return cost * 12

def get_next_renewal(day: int, cycle: str) -> datetime:
    """Calculate next renewal date."""
    today = datetime.now()
    
    if cycle == "weekly":
        # Next occurrence of that day of week (0=Monday)
        days_ahead = day - today.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return today + timedelta(days=days_ahead)
    
    elif cycle == "yearly":
        # Assume day is day of year or use month-day logic
        next_date = today.replace(day=min(day, 28))
        if next_date <= today:
            next_date = next_date.replace(year=today.year + 1)
        return next_date
    
    else:  # monthly or quarterly
        # Next occurrence of that day of month
        try:
            next_date = today.replace(day=day)
        except ValueError:
            # Day doesn't exist in this month, use last day
            next_date = (today.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        if next_date <= today:
            # Move to next month
            if today.month == 12:
                next_date = next_date.replace(year=today.year + 1, month=1)
            else:
                try:
                    next_date = next_date.replace(month=today.month + 1)
                except ValueError:
                    next_date = next_date.replace(month=today.month + 2, day=1) - timedelta(days=1)
        
        return next_date

def add_subscription(name: str, cost: float, cycle: str = "monthly", 
                    day: int = 1, category: Optional[str] = None,
                    notes: str = "", cancel_url: str = "",
                    remind_days: int = 3, currency: str = "USD") -> Dict[str, Any]:
    """Add a new subscription."""
    subs = load_subscriptions()
    
    # Check for duplicates
    for sub in subs:
        if sub["name"].lower() == name.lower() and sub["status"] == "active":
            print(f"⚠️ Subscription '{name}' already exists!")
            return sub
    
    # Auto-detect category if not provided
    if not category:
        category = detect_category(name)
    
    sub = {
        "id": str(uuid.uuid4()),
        "name": name,
        "cost": cost,
        "currency": currency,
        "billing_cycle": cycle,
        "renewal_day": day,
        "category": category,
        "status": "active",
        "notes": notes,
        "cancel_url": cancel_url,
        "last_used": None,
        "created_at": datetime.now().isoformat(),
        "remind_days_before": remind_days
    }
    
    subs.append(sub)
    save_subscriptions(subs)
    
    monthly = calculate_monthly_cost(cost, cycle)
    yearly = calculate_yearly_cost(cost, cycle)
    emoji = get_category_emoji(category)
    
    print(f"✅ Added subscription: {name}")
    print(f"   💳 Cost: ${cost:.2f}/{cycle}")
    print(f"   📅 Renews: Day {day} of each {cycle.replace('ly', '')}")
    print(f"   {emoji} Category: {category.capitalize()}")
    print(f"   ⏰ Reminder: {remind_days} days before")
    print(f"   💵 Monthly equivalent: ${monthly:.2f}")
    print(f"   📊 Yearly cost: ${yearly:.2f}")
    
    return sub

def list_subscriptions(status: str = "all", category: Optional[str] = None):
    """List all subscriptions."""
    subs = load_subscriptions()
    
    if not subs:
        print("📭 No subscriptions found. Add one with: add subscription <name> $<cost>/<cycle>")
        return
    
    # Filter by status
    if status != "all":
        subs = [s for s in subs if s["status"] == status]
    
    # Filter by category
    if category:
        subs = [s for s in subs if s["category"].lower() == category.lower()]
    
    if not subs:
        print(f"📭 No {status} subscriptions found" + (f" in {category}" if category else ""))
        return
    
    print(f"\n📋 **Your Subscriptions** ({len(subs)} {'active' if status == 'active' else 'total'})\n")
    print(f"| {'Service':<20} | {'Cost':<12} | {'Cycle':<10} | {'Category':<15} | {'Status':<10} |")
    print(f"|{'-'*22}|{'-'*14}|{'-'*12}|{'-'*17}|{'-'*12}|")
    
    for sub in sorted(subs, key=lambda x: (x["status"] != "active", x["category"], x["name"])):
        emoji = get_category_emoji(sub["category"])
        status_emoji = "✅" if sub["status"] == "active" else "⏸️" if sub["status"] == "paused" else "❌"
        cost_str = f"${sub['cost']:.2f}"
        print(f"| {sub['name']:<20} | {cost_str:<12} | {sub['billing_cycle']:<10} | {emoji} {sub['category']:<12} | {status_emoji} {sub['status']:<7} |")
    
    print()

def get_upcoming_renewals(days: int = 7):
    """Get subscriptions renewing within specified days."""
    subs = load_subscriptions()
    active_subs = [s for s in subs if s["status"] == "active"]
    
    if not active_subs:
        print("📭 No active subscriptions to check")
        return
    
    today = datetime.now()
    upcoming = []
    
    for sub in active_subs:
        next_renewal = get_next_renewal(sub["renewal_day"], sub["billing_cycle"])
        days_until = (next_renewal - today).days
        
        if 0 <= days_until <= days:
            upcoming.append({
                **sub,
                "next_renewal": next_renewal,
                "days_until": days_until
            })
    
    upcoming.sort(key=lambda x: x["days_until"])
    
    if not upcoming:
        print(f"✨ No renewals in the next {days} days!")
        return
    
    total = sum(s["cost"] for s in upcoming)
    
    print(f"\n⏰ **Upcoming Renewals** (Next {days} Days)\n")
    print(f"| {'Service':<20} | {'Date':<12} | {'Days':<6} | {'Amount':<10} |")
    print(f"|{'-'*22}|{'-'*14}|{'-'*8}|{'-'*12}|")
    
    for sub in upcoming:
        date_str = sub["next_renewal"].strftime("%b %d")
        days_str = "TODAY" if sub["days_until"] == 0 else f"{sub['days_until']}d"
        amount_str = f"${sub['cost']:.2f}"
        urgency = "🔴" if sub["days_until"] <= 1 else "🟡" if sub["days_until"] <= 3 else "🟢"
        print(f"| {urgency} {sub['name']:<17} | {date_str:<12} | {days_str:<6} | {amount_str:<10} |")
    
    print(f"\n💰 **Total upcoming:** ${total:.2f}")

def spending_summary():
    """Generate spending summary by category."""
    subs = load_subscriptions()
    active_subs = [s for s in subs if s["status"] == "active"]
    
    if not active_subs:
        print("📭 No active subscriptions to summarize")
        return
    
    # Group by category
    by_category = {}
    for sub in active_subs:
        cat = sub["category"]
        if cat not in by_category:
            by_category[cat] = {"monthly": 0, "yearly": 0, "count": 0}
        
        monthly = calculate_monthly_cost(sub["cost"], sub["billing_cycle"])
        yearly = calculate_yearly_cost(sub["cost"], sub["billing_cycle"])
        
        by_category[cat]["monthly"] += monthly
        by_category[cat]["yearly"] += yearly
        by_category[cat]["count"] += 1
    
    total_monthly = sum(c["monthly"] for c in by_category.values())
    total_yearly = sum(c["yearly"] for c in by_category.values())
    
    print(f"\n📊 **Subscription Spending Summary**\n")
    print(f"| {'Category':<20} | {'Monthly':<12} | {'Yearly':<12} | {'#':<4} |")
    print(f"|{'-'*22}|{'-'*14}|{'-'*14}|{'-'*6}|")
    
    for cat, data in sorted(by_category.items(), key=lambda x: -x[1]["monthly"]):
        emoji = get_category_emoji(cat)
        print(f"| {emoji} {cat.capitalize():<17} | ${data['monthly']:>10.2f} | ${data['yearly']:>10.2f} | {data['count']:<4} |")
    
    print(f"|{'-'*22}|{'-'*14}|{'-'*14}|{'-'*6}|")
    print(f"| {'**TOTAL**':<20} | **${total_monthly:>8.2f}** | **${total_yearly:>8.2f}** | {len(active_subs):<4} |")
    
    # Daily cost
    daily = total_monthly / 30
    
    print(f"\n💡 **Insights:**")
    print(f"   • Daily subscription cost: ${daily:.2f}")
    print(f"   • Monthly cost: ${total_monthly:.2f}")
    print(f"   • Yearly cost: ${total_yearly:.2f}")
    
    if total_yearly > 1000:
        print(f"   ⚠️ You're spending over $1,000/year on subscriptions!")
    
    # Find biggest category
    if by_category:
        biggest = max(by_category.items(), key=lambda x: x[1]["monthly"])
        print(f"   • Biggest category: {biggest[0].capitalize()} (${biggest[1]['monthly']:.2f}/mo)")

def remove_subscription(name: str, permanent: bool = False):
    """Remove or cancel a subscription."""
    subs = load_subscriptions()
    
    found = None
    for sub in subs:
        if sub["name"].lower() == name.lower():
            found = sub
            break
    
    if not found:
        print(f"❌ Subscription '{name}' not found")
        return
    
    if permanent:
        subs.remove(found)
        save_subscriptions(subs)
        print(f"🗑️ Permanently deleted: {name}")
    else:
        found["status"] = "cancelled"
        found["cancelled_at"] = datetime.now().isoformat()
        save_subscriptions(subs)
        print(f"❌ Cancelled subscription: {name}")
        if found.get("cancel_url"):
            print(f"   🔗 Cancel URL: {found['cancel_url']}")

def pause_subscription(name: str):
    """Pause a subscription."""
    subs = load_subscriptions()
    
    for sub in subs:
        if sub["name"].lower() == name.lower():
            sub["status"] = "paused"
            sub["paused_at"] = datetime.now().isoformat()
            save_subscriptions(subs)
            print(f"⏸️ Paused subscription: {name}")
            return
    
    print(f"❌ Subscription '{name}' not found")

def resume_subscription(name: str):
    """Resume a paused subscription."""
    subs = load_subscriptions()
    
    for sub in subs:
        if sub["name"].lower() == name.lower():
            sub["status"] = "active"
            if "paused_at" in sub:
                del sub["paused_at"]
            save_subscriptions(subs)
            print(f"▶️ Resumed subscription: {name}")
            return
    
    print(f"❌ Subscription '{name}' not found")

def export_subscriptions(format: str = "csv"):
    """Export subscriptions to CSV or JSON."""
    subs = load_subscriptions()
    
    if not subs:
        print("📭 No subscriptions to export")
        return
    
    if format == "csv":
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            "name", "cost", "currency", "billing_cycle", "renewal_day",
            "category", "status", "notes", "cancel_url", "created_at"
        ])
        writer.writeheader()
        for sub in subs:
            writer.writerow({k: sub.get(k, "") for k in writer.fieldnames})
        
        csv_content = output.getvalue()
        
        # Save to file
        export_path = DATA_DIR / f"subscriptions_export_{datetime.now().strftime('%Y%m%d')}.csv"
        with open(export_path, 'w') as f:
            f.write(csv_content)
        
        print(f"📤 Exported {len(subs)} subscriptions to: {export_path}")
        print("\nPreview:")
        print(csv_content[:500])
    else:
        export_path = DATA_DIR / f"subscriptions_export_{datetime.now().strftime('%Y%m%d')}.json"
        with open(export_path, 'w') as f:
            json.dump(subs, f, indent=2, default=str)
        
        print(f"📤 Exported {len(subs)} subscriptions to: {export_path}")

def check_reminders():
    """Check for subscriptions needing reminder alerts."""
    subs = load_subscriptions()
    active_subs = [s for s in subs if s["status"] == "active"]
    
    alerts = []
    today = datetime.now()
    
    for sub in active_subs:
        remind_days = sub.get("remind_days_before", 3)
        next_renewal = get_next_renewal(sub["renewal_day"], sub["billing_cycle"])
        days_until = (next_renewal - today).days
        
        if days_until <= remind_days:
            alerts.append({
                "name": sub["name"],
                "cost": sub["cost"],
                "days_until": days_until,
                "renewal_date": next_renewal.strftime("%Y-%m-%d")
            })
    
    if alerts:
        print(f"🔔 **Subscription Reminders** ({len(alerts)} upcoming)\n")
        for alert in sorted(alerts, key=lambda x: x["days_until"]):
            urgency = "🔴" if alert["days_until"] <= 1 else "🟡"
            when = "TODAY!" if alert["days_until"] == 0 else f"in {alert['days_until']} days"
            print(f"{urgency} **{alert['name']}** renews {when} (${alert['cost']:.2f})")
    else:
        print("✅ No upcoming renewals need attention")

def main():
    parser = argparse.ArgumentParser(description="Subscription Manager Pro")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a subscription")
    add_parser.add_argument("--name", "-n", required=True, help="Service name")
    add_parser.add_argument("--cost", "-c", type=float, required=True, help="Cost per billing cycle")
    add_parser.add_argument("--cycle", default="monthly", choices=["weekly", "monthly", "quarterly", "yearly"])
    add_parser.add_argument("--day", "-d", type=int, default=1, help="Renewal day")
    add_parser.add_argument("--category", help="Category (auto-detected if not provided)")
    add_parser.add_argument("--notes", default="", help="Notes")
    add_parser.add_argument("--cancel-url", default="", help="URL to cancel")
    add_parser.add_argument("--remind", type=int, default=3, help="Days before to remind")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List subscriptions")
    list_parser.add_argument("--status", default="all", choices=["all", "active", "paused", "cancelled"])
    list_parser.add_argument("--category", help="Filter by category")
    
    # Upcoming command
    upcoming_parser = subparsers.add_parser("upcoming", help="Show upcoming renewals")
    upcoming_parser.add_argument("--days", "-d", type=int, default=7, help="Days to look ahead")
    
    # Summary command
    subparsers.add_parser("summary", help="Spending summary")
    
    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove/cancel subscription")
    remove_parser.add_argument("--name", "-n", required=True, help="Service name")
    remove_parser.add_argument("--permanent", action="store_true", help="Permanently delete")
    
    # Pause command
    pause_parser = subparsers.add_parser("pause", help="Pause subscription")
    pause_parser.add_argument("--name", "-n", required=True, help="Service name")
    
    # Resume command
    resume_parser = subparsers.add_parser("resume", help="Resume subscription")
    resume_parser.add_argument("--name", "-n", required=True, help="Service name")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export subscriptions")
    export_parser.add_argument("--format", "-f", default="csv", choices=["csv", "json"])
    
    # Reminders command
    subparsers.add_parser("reminders", help="Check reminder alerts")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_subscription(
            name=args.name,
            cost=args.cost,
            cycle=args.cycle,
            day=args.day,
            category=args.category,
            notes=args.notes,
            cancel_url=args.cancel_url,
            remind_days=args.remind
        )
    elif args.command == "list":
        list_subscriptions(status=args.status, category=args.category)
    elif args.command == "upcoming":
        get_upcoming_renewals(days=args.days)
    elif args.command == "summary":
        spending_summary()
    elif args.command == "remove":
        remove_subscription(name=args.name, permanent=args.permanent)
    elif args.command == "pause":
        pause_subscription(name=args.name)
    elif args.command == "resume":
        resume_subscription(name=args.name)
    elif args.command == "export":
        export_subscriptions(format=args.format)
    elif args.command == "reminders":
        check_reminders()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
