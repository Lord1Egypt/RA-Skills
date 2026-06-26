# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "python-dotenv",
# ]
# ///
"""
Meta Ads Performance Analytics (Marketing API)

Fetches campaign, ad set, ad, and creative performance metrics from Meta Ads.
Saves data to Analytics/meta-ads/ for cross-channel analysis.

Usage:
    uv run scripts/meta-ads-analytics.py --setup                 # Credential setup guide
    uv run scripts/meta-ads-analytics.py --summary               # Account overview (last 7 days)
    uv run scripts/meta-ads-analytics.py --campaigns             # All campaigns with metrics
    uv run scripts/meta-ads-analytics.py --campaign CAMPAIGN_ID  # Deep dive (daily + ad sets + ads)
    uv run scripts/meta-ads-analytics.py --adsets                # Ad set performance
    uv run scripts/meta-ads-analytics.py --ads                   # Ad-level performance
    uv run scripts/meta-ads-analytics.py --creative              # Asset-level breakdowns
    uv run scripts/meta-ads-analytics.py --audience              # Age/gender/placement/device
    uv run scripts/meta-ads-analytics.py --period 30             # Custom lookback (default 7)
    uv run scripts/meta-ads-analytics.py --sync                  # Save all data to Analytics/
    uv run scripts/meta-ads-analytics.py --export results.csv    # Export to CSV

Environment variables (or .env file):
    META_ADS_ACCESS_TOKEN - System User token with ads_read permission
    META_ADS_ACCOUNT_ID   - Ad account ID (format: act_XXXXXXXXX)
"""

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load environment variables from current working directory
PROJECT_ROOT = Path.cwd()
load_dotenv(PROJECT_ROOT / ".env")

ACCESS_TOKEN = os.getenv("META_ADS_ACCESS_TOKEN", "")
ACCOUNT_ID = os.getenv("META_ADS_ACCOUNT_ID", "")

DATA_DIR = PROJECT_ROOT / "Analytics" / "meta-ads"
API_BASE = "https://graph.facebook.com/v21.0"

# Standard insight fields
INSIGHT_FIELDS = (
    "impressions,reach,clicks,ctr,cpc,cpm,cpp,spend,"
    "actions,cost_per_action_type,purchase_roas,"
    "frequency,unique_clicks,cost_per_unique_click"
)


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def api_request(
    endpoint: str,
    params: dict | None = None,
    max_retries: int = 5,
) -> dict | None:
    """Make authenticated GET request with rate limiting and exponential backoff."""
    params = params or {}
    params["access_token"] = ACCESS_TOKEN

    url = f"{API_BASE}/{endpoint}"

    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=60)

            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 2 ** attempt))
                print(f"  Rate limited. Waiting {retry_after}s...")
                time.sleep(retry_after)
                continue

            if response.status_code != 200:
                error = response.json().get("error", {})
                error_msg = error.get("message", response.text[:300])
                error_code = error.get("code", "")

                # Transient errors — retry
                if error_code in (1, 2, 4, 17):
                    wait = 2 ** attempt
                    print(f"  Transient API error (code {error_code}). Retrying in {wait}s...")
                    time.sleep(wait)
                    continue

                print(f"  API Error [{error_code}]: {error_msg}")
                return None

            return response.json()

        except requests.RequestException as e:
            if attempt < max_retries - 1:
                wait = 2 ** attempt
                print(f"  Request error: {e}. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"  Request failed after {max_retries} attempts: {e}")
                return None

    return None


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def save_data(filename: str, data: dict) -> None:
    """Save data to JSON file in Analytics/meta-ads/."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    filepath = DATA_DIR / filename
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"  Saved to {filepath.relative_to(PROJECT_ROOT)}")


def load_data(filename: str) -> dict | None:
    """Load data from JSON file."""
    filepath = DATA_DIR / filename
    if filepath.exists():
        with open(filepath) as f:
            return json.load(f)
    return None


def save_sync_state(key: str) -> None:
    """Update sync state timestamp."""
    state_file = DATA_DIR / "sync-meta.json"
    state = {}
    if state_file.exists():
        with open(state_file) as f:
            state = json.load(f)
    state[key] = datetime.now(timezone.utc).isoformat()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(state_file, "w") as f:
        json.dump(state, f, indent=2)


def date_range(days: int) -> tuple[str, str]:
    """Return (since, until) date strings for the given lookback period."""
    until = datetime.now(timezone.utc).date()
    since = until - timedelta(days=days)
    return str(since), str(until)


def extract_action_value(actions: list | None, action_type: str) -> float:
    """Extract a specific action value from the actions list."""
    if not actions:
        return 0
    for a in actions:
        if a.get("action_type") == action_type:
            return float(a.get("value", 0))
    return 0


def extract_roas(roas_list: list | None) -> float:
    """Extract purchase ROAS value."""
    if not roas_list:
        return 0
    for r in roas_list:
        if r.get("action_type") == "omni_purchase":
            return float(r.get("value", 0))
    return 0


def extract_cost_per_action(cost_list: list | None, action_type: str) -> float:
    """Extract cost per specific action."""
    if not cost_list:
        return 0
    for c in cost_list:
        if c.get("action_type") == action_type:
            return float(c.get("value", 0))
    return 0


# ---------------------------------------------------------------------------
# Insight fetching
# ---------------------------------------------------------------------------

def get_account_insights(days: int = 7) -> dict | None:
    """Account-level insights for the given period."""
    since, until = date_range(days)
    print(f"Fetching account insights ({since} to {until})...")

    result = api_request(
        f"{ACCOUNT_ID}/insights",
        params={
            "fields": INSIGHT_FIELDS,
            "time_range": json.dumps({"since": since, "until": until}),
            "level": "account",
        },
    )

    if result and result.get("data"):
        return result["data"][0]
    return None


def get_campaigns_insights(days: int = 7) -> list:
    """Campaign-level insights."""
    since, until = date_range(days)
    print(f"Fetching campaign insights ({since} to {until})...")

    result = api_request(
        f"{ACCOUNT_ID}/insights",
        params={
            "fields": f"campaign_id,campaign_name,{INSIGHT_FIELDS}",
            "time_range": json.dumps({"since": since, "until": until}),
            "level": "campaign",
            "limit": 100,
        },
    )

    return result.get("data", []) if result else []


def get_adset_insights(days: int = 7) -> list:
    """Ad set-level insights."""
    since, until = date_range(days)
    print(f"Fetching ad set insights ({since} to {until})...")

    result = api_request(
        f"{ACCOUNT_ID}/insights",
        params={
            "fields": f"adset_id,adset_name,campaign_name,{INSIGHT_FIELDS}",
            "time_range": json.dumps({"since": since, "until": until}),
            "level": "adset",
            "limit": 200,
        },
    )

    return result.get("data", []) if result else []


def get_ad_insights(days: int = 7) -> list:
    """Ad-level insights."""
    since, until = date_range(days)
    print(f"Fetching ad-level insights ({since} to {until})...")

    result = api_request(
        f"{ACCOUNT_ID}/insights",
        params={
            "fields": f"ad_id,ad_name,adset_name,campaign_name,{INSIGHT_FIELDS}",
            "time_range": json.dumps({"since": since, "until": until}),
            "level": "ad",
            "limit": 500,
        },
    )

    return result.get("data", []) if result else []


def get_campaign_deep_dive(campaign_id: str, days: int = 7) -> dict:
    """Single campaign with daily time series + breakdowns."""
    since, until = date_range(days)
    print(f"Fetching deep dive for campaign {campaign_id}...")

    # Daily trend
    daily = api_request(
        f"{campaign_id}/insights",
        params={
            "fields": INSIGHT_FIELDS,
            "time_range": json.dumps({"since": since, "until": until}),
            "time_increment": 1,
        },
    )

    # Campaign info
    info = api_request(
        campaign_id,
        params={"fields": "id,name,status,effective_status,objective,daily_budget"},
    )

    # Ad set breakdown
    adsets = api_request(
        f"{campaign_id}/insights",
        params={
            "fields": f"adset_id,adset_name,{INSIGHT_FIELDS}",
            "time_range": json.dumps({"since": since, "until": until}),
            "level": "adset",
            "limit": 50,
        },
    )

    # Ad breakdown
    ads = api_request(
        f"{campaign_id}/insights",
        params={
            "fields": f"ad_id,ad_name,{INSIGHT_FIELDS}",
            "time_range": json.dumps({"since": since, "until": until}),
            "level": "ad",
            "limit": 100,
        },
    )

    return {
        "campaign": info or {},
        "daily": daily.get("data", []) if daily else [],
        "adsets": adsets.get("data", []) if adsets else [],
        "ads": ads.get("data", []) if ads else [],
    }


def get_audience_breakdowns(days: int = 7) -> dict:
    """Age, gender, placement, device breakdowns."""
    since, until = date_range(days)
    print(f"Fetching audience breakdowns ({since} to {until})...")

    breakdowns = {}

    for breakdown_name in ["age", "gender", "publisher_platform", "device_platform"]:
        result = api_request(
            f"{ACCOUNT_ID}/insights",
            params={
                "fields": INSIGHT_FIELDS,
                "time_range": json.dumps({"since": since, "until": until}),
                "breakdowns": breakdown_name,
                "level": "account",
                "limit": 100,
            },
        )
        breakdowns[breakdown_name] = result.get("data", []) if result else []

    return breakdowns


# ---------------------------------------------------------------------------
# Display functions
# ---------------------------------------------------------------------------

def print_summary(insights: dict, days: int) -> None:
    """Print account summary."""
    print(f"\n{'='*70}")
    print(f"META ADS ACCOUNT SUMMARY (last {days} days)")
    print(f"{'='*70}")

    spend = float(insights.get("spend", 0))
    impressions = int(insights.get("impressions", 0))
    reach = int(insights.get("reach", 0))
    clicks = int(insights.get("clicks", 0))
    ctr = float(insights.get("ctr", 0))
    cpc = float(insights.get("cpc", 0))
    cpm = float(insights.get("cpm", 0))
    frequency = float(insights.get("frequency", 0))

    purchases = extract_action_value(insights.get("actions"), "omni_purchase")
    add_to_cart = extract_action_value(insights.get("actions"), "omni_add_to_cart")
    roas = extract_roas(insights.get("purchase_roas"))
    cpa = extract_cost_per_action(insights.get("cost_per_action_type"), "omni_purchase")

    print(f"\n  Spend:        ${spend:,.2f}")
    print(f"  Impressions:  {impressions:,}")
    print(f"  Reach:        {reach:,}")
    print(f"  Frequency:    {frequency:.2f}")
    print(f"  Clicks:       {clicks:,}")
    print(f"  CTR:          {ctr:.2f}%")
    print(f"  CPC:          ${cpc:.2f}")
    print(f"  CPM:          ${cpm:.2f}")

    print(f"\n  Conversions:")
    print(f"    Purchases:    {purchases:.0f}")
    print(f"    Add to Cart:  {add_to_cart:.0f}")
    print(f"    CPA:          ${cpa:.2f}" if cpa else "    CPA:          N/A")
    print(f"    ROAS:         {roas:.2f}x" if roas else "    ROAS:         N/A")

    # DTC benchmark comparison
    print(f"\n  DTC Benchmarks:")
    ctr_status = "GOOD" if ctr >= 1.0 else "LOW" if ctr < 0.5 else "OK"
    cpm_status = "GOOD" if cpm <= 20 else "HIGH" if cpm > 30 else "OK"
    cpa_status = "GOOD" if 0 < cpa <= 30 else "HIGH" if cpa > 60 else "OK" if cpa > 0 else "N/A"
    roas_status = "GOOD" if roas >= 3.0 else "LOW" if 0 < roas < 2.0 else "OK" if roas > 0 else "N/A"

    print(f"    CTR {ctr:.2f}% [{ctr_status}] (target: 1-2.5%)")
    print(f"    CPM ${cpm:.2f} [{cpm_status}] (target: $10-30)")
    print(f"    CPA ${cpa:.2f} [{cpa_status}] (target: $20-60)" if cpa else f"    CPA N/A (target: $20-60)")
    print(f"    ROAS {roas:.2f}x [{roas_status}] (target: 2-4x)" if roas else f"    ROAS N/A (target: 2-4x)")

    print(f"\n{'='*70}")


def print_campaign_table(campaigns: list) -> None:
    """Print campaign metrics table."""
    print(f"\n{'='*100}")
    print("CAMPAIGN PERFORMANCE")
    print(f"{'='*100}")

    print(f"\n{'Campaign':<30} {'Spend':>10} {'Impr':>10} {'Clicks':>8} {'CTR':>7} {'CPC':>7} {'Purch':>7} {'ROAS':>7}")
    print(f"{'-'*30} {'-'*10} {'-'*10} {'-'*8} {'-'*7} {'-'*7} {'-'*7} {'-'*7}")

    for c in campaigns:
        name = c.get("campaign_name", "")[:29]
        spend = float(c.get("spend", 0))
        impressions = int(c.get("impressions", 0))
        clicks = int(c.get("clicks", 0))
        ctr = float(c.get("ctr", 0))
        cpc = float(c.get("cpc", 0))
        purchases = extract_action_value(c.get("actions"), "omni_purchase")
        roas = extract_roas(c.get("purchase_roas"))

        roas_str = f"{roas:.1f}x" if roas else "—"
        purch_str = f"{purchases:.0f}" if purchases else "—"

        print(f"{name:<30} ${spend:>9,.2f} {impressions:>10,} {clicks:>8,} {ctr:>6.2f}% ${cpc:>5.2f} {purch_str:>7} {roas_str:>7}")

    print(f"\n{'='*100}")


def print_adset_table(adsets: list) -> None:
    """Print ad set metrics table."""
    print(f"\n{'='*100}")
    print("AD SET PERFORMANCE")
    print(f"{'='*100}")

    print(f"\n{'Ad Set':<30} {'Campaign':<20} {'Spend':>10} {'Impr':>9} {'CTR':>7} {'CPC':>7} {'ROAS':>7}")
    print(f"{'-'*30} {'-'*20} {'-'*10} {'-'*9} {'-'*7} {'-'*7} {'-'*7}")

    for a in adsets:
        name = a.get("adset_name", "")[:29]
        campaign = a.get("campaign_name", "")[:19]
        spend = float(a.get("spend", 0))
        impressions = int(a.get("impressions", 0))
        ctr = float(a.get("ctr", 0))
        cpc = float(a.get("cpc", 0))
        roas = extract_roas(a.get("purchase_roas"))
        roas_str = f"{roas:.1f}x" if roas else "—"

        print(f"{name:<30} {campaign:<20} ${spend:>9,.2f} {impressions:>9,} {ctr:>6.2f}% ${cpc:>5.2f} {roas_str:>7}")

    print(f"\n{'='*100}")


def print_ad_table(ads: list) -> None:
    """Print ad-level metrics table."""
    print(f"\n{'='*100}")
    print("AD PERFORMANCE")
    print(f"{'='*100}")

    print(f"\n{'Ad Name':<35} {'Spend':>10} {'Impr':>9} {'CTR':>7} {'CPC':>7} {'Purch':>7} {'ROAS':>7}")
    print(f"{'-'*35} {'-'*10} {'-'*9} {'-'*7} {'-'*7} {'-'*7} {'-'*7}")

    for a in ads:
        name = a.get("ad_name", "")[:34]
        spend = float(a.get("spend", 0))
        impressions = int(a.get("impressions", 0))
        ctr = float(a.get("ctr", 0))
        cpc = float(a.get("cpc", 0))
        purchases = extract_action_value(a.get("actions"), "omni_purchase")
        roas = extract_roas(a.get("purchase_roas"))

        roas_str = f"{roas:.1f}x" if roas else "—"
        purch_str = f"{purchases:.0f}" if purchases else "—"

        print(f"{name:<35} ${spend:>9,.2f} {impressions:>9,} {ctr:>6.2f}% ${cpc:>5.2f} {purch_str:>7} {roas_str:>7}")

    print(f"\n{'='*100}")


def print_campaign_deep_dive(data: dict, days: int) -> None:
    """Print campaign deep dive with daily trend."""
    campaign = data.get("campaign", {})
    daily = data.get("daily", [])
    adsets = data.get("adsets", [])
    ads = data.get("ads", [])

    print(f"\n{'='*70}")
    print(f"CAMPAIGN DEEP DIVE (last {days} days)")
    print(f"{'='*70}")
    print(f"  Name:      {campaign.get('name', 'N/A')}")
    print(f"  Status:    {campaign.get('effective_status', campaign.get('status', 'N/A'))}")
    print(f"  Objective: {campaign.get('objective', 'N/A')}")

    if daily:
        print(f"\n  Daily Trend:")
        print(f"  {'Date':<12} {'Spend':>10} {'Impr':>9} {'Clicks':>8} {'CTR':>7} {'Purch':>7}")
        print(f"  {'-'*12} {'-'*10} {'-'*9} {'-'*8} {'-'*7} {'-'*7}")

        for day in daily:
            date = day.get("date_start", "")
            spend = float(day.get("spend", 0))
            impressions = int(day.get("impressions", 0))
            clicks = int(day.get("clicks", 0))
            ctr = float(day.get("ctr", 0))
            purchases = extract_action_value(day.get("actions"), "omni_purchase")
            purch_str = f"{purchases:.0f}" if purchases else "—"

            print(f"  {date:<12} ${spend:>9,.2f} {impressions:>9,} {clicks:>8,} {ctr:>6.2f}% {purch_str:>7}")

    if adsets:
        print(f"\n  Ad Set Breakdown:")
        for a in adsets:
            name = a.get("adset_name", "")
            spend = float(a.get("spend", 0))
            ctr = float(a.get("ctr", 0))
            roas = extract_roas(a.get("purchase_roas"))
            roas_str = f"{roas:.1f}x" if roas else "—"
            print(f"    {name}: ${spend:,.2f} spend, {ctr:.2f}% CTR, {roas_str} ROAS")

    if ads:
        print(f"\n  Top Ads:")
        sorted_ads = sorted(ads, key=lambda x: float(x.get("spend", 0)), reverse=True)
        for a in sorted_ads[:10]:
            name = a.get("ad_name", "")[:40]
            spend = float(a.get("spend", 0))
            ctr = float(a.get("ctr", 0))
            roas = extract_roas(a.get("purchase_roas"))
            roas_str = f"{roas:.1f}x" if roas else "—"
            print(f"    {name}: ${spend:,.2f} spend, {ctr:.2f}% CTR, {roas_str} ROAS")

    print(f"\n{'='*70}")


def print_audience_breakdowns(breakdowns: dict) -> None:
    """Print audience breakdown tables."""
    print(f"\n{'='*70}")
    print("AUDIENCE BREAKDOWNS")
    print(f"{'='*70}")

    for breakdown_name, data in breakdowns.items():
        if not data:
            continue

        label = breakdown_name.replace("_", " ").title()
        print(f"\n  {label}:")
        print(f"  {'Segment':<25} {'Spend':>10} {'Impr':>10} {'CTR':>7} {'CPC':>7}")
        print(f"  {'-'*25} {'-'*10} {'-'*10} {'-'*7} {'-'*7}")

        for row in data:
            segment = row.get(breakdown_name, "unknown")
            spend = float(row.get("spend", 0))
            impressions = int(row.get("impressions", 0))
            ctr = float(row.get("ctr", 0))
            cpc = float(row.get("cpc", 0))
            print(f"  {segment:<25} ${spend:>9,.2f} {impressions:>10,} {ctr:>6.2f}% ${cpc:>5.2f}")

    print(f"\n{'='*70}")


# ---------------------------------------------------------------------------
# Export & sync
# ---------------------------------------------------------------------------

def export_to_csv(data: list, filepath: Path) -> None:
    """Export insight rows to CSV."""
    if not data:
        print("  No data to export")
        return

    # Flatten actions into columns
    rows = []
    for row in data:
        flat = {}
        for k, v in row.items():
            if k in ("actions", "cost_per_action_type", "purchase_roas"):
                continue
            flat[k] = v

        flat["purchases"] = extract_action_value(row.get("actions"), "omni_purchase")
        flat["add_to_cart"] = extract_action_value(row.get("actions"), "omni_add_to_cart")
        flat["roas"] = extract_roas(row.get("purchase_roas"))
        flat["cost_per_purchase"] = extract_cost_per_action(
            row.get("cost_per_action_type"), "omni_purchase"
        )
        rows.append(flat)

    if not rows:
        return

    fieldnames = list(rows[0].keys())
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"  Exported {len(rows)} rows to {filepath}")


def sync_all_data(days: int) -> None:
    """Full sync of all insight data to Analytics/meta-ads/."""
    print(f"\nSyncing all Meta Ads data (last {days} days)...\n")

    # Account insights
    account = get_account_insights(days)
    if account:
        account["_fetched_at"] = datetime.now(timezone.utc).isoformat()
        account["_days"] = days
        save_data("insights-account.json", account)
        save_sync_state("insights-account")

    # Campaign insights
    campaigns = get_campaigns_insights(days)
    if campaigns:
        save_data("insights-campaigns.json", {
            "data": campaigns,
            "_fetched_at": datetime.now(timezone.utc).isoformat(),
            "_days": days,
        })
        save_sync_state("insights-campaigns")

    # Ad set insights
    adsets = get_adset_insights(days)
    if adsets:
        save_data("adsets.json", {
            "data": adsets,
            "_fetched_at": datetime.now(timezone.utc).isoformat(),
            "_days": days,
        })
        save_sync_state("adsets")

    # Campaign list
    campaigns_list = api_request(
        f"{ACCOUNT_ID}/campaigns",
        params={
            "fields": "id,name,status,effective_status,objective,daily_budget,created_time",
            "limit": 100,
        },
    )
    if campaigns_list and campaigns_list.get("data"):
        save_data("campaigns.json", {
            "data": campaigns_list["data"],
            "_fetched_at": datetime.now(timezone.utc).isoformat(),
        })
        save_sync_state("campaigns")

    # Audience breakdowns
    audience = get_audience_breakdowns(days)
    if audience:
        audience["_fetched_at"] = datetime.now(timezone.utc).isoformat()
        audience["_days"] = days
        save_data("insights-audience.json", audience)
        save_sync_state("insights-audience")

    print(f"\nSync complete. Data saved to {DATA_DIR.relative_to(PROJECT_ROOT)}/")


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

def print_setup_guide() -> None:
    """Print credential setup instructions."""
    print("""
META ADS ANALYTICS SETUP GUIDE
===============================

To use this script, you need:
1. META_ADS_ACCESS_TOKEN - System User token with ads_read permission
2. META_ADS_ACCOUNT_ID   - Ad account ID (format: act_XXXXXXXXX)

If you already set up meta-ads-publish.py, the same credentials work here.

STEP 1: Create a System User in Business Manager
-------------------------------------------------
1. Go to business.facebook.com/settings
2. Navigate to Users > System Users
3. Click "Add" to create a new System User
4. Set role to "Admin"

STEP 2: Generate an Access Token
---------------------------------
1. Click on the System User you created
2. Click "Generate New Token"
3. Select your app
4. Select permissions:
   - ads_read (required - read campaign metrics)
   - ads_management (optional - if also using publish script)
5. Click "Generate Token"

STEP 3: Get Your Ad Account ID
-------------------------------
1. Go to business.facebook.com/settings
2. Navigate to Accounts > Ad Accounts
3. Copy the account ID (format: act_XXXXXXXXX)

STEP 4: Add to .env
--------------------
META_ADS_ACCESS_TOKEN=your_system_user_token
META_ADS_ACCOUNT_ID=act_XXXXXXXXX

STEP 5: Verify
--------------
uv run scripts/meta-ads-analytics.py --summary

AVAILABLE METRICS
=================
  --summary    Account overview with DTC benchmarks
  --campaigns  Campaign-level metrics table
  --campaign   Single campaign deep dive (daily trend + ad sets)
  --adsets     Ad set performance
  --ads        Ad-level performance
  --audience   Age, gender, platform, device breakdowns
  --sync       Save all data to Analytics/meta-ads/
  --export     Export to CSV for spreadsheet analysis
  --period N   Change lookback period (default: 7 days)
""")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Meta Ads Performance Analytics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run scripts/meta-ads-analytics.py --summary
  uv run scripts/meta-ads-analytics.py --campaigns --period 30
  uv run scripts/meta-ads-analytics.py --campaign 12345678
  uv run scripts/meta-ads-analytics.py --audience
  uv run scripts/meta-ads-analytics.py --sync
  uv run scripts/meta-ads-analytics.py --export results.csv
        """,
    )

    parser.add_argument("--setup", action="store_true", help="Show setup guide")
    parser.add_argument("--summary", action="store_true", help="Account overview")
    parser.add_argument("--campaigns", action="store_true", help="All campaigns with metrics")
    parser.add_argument("--campaign", metavar="ID", help="Deep dive into specific campaign")
    parser.add_argument("--adsets", action="store_true", help="Ad set performance")
    parser.add_argument("--ads", action="store_true", help="Ad-level performance")
    parser.add_argument("--creative", action="store_true", help="Creative/asset breakdowns")
    parser.add_argument("--audience", action="store_true", help="Audience breakdowns")
    parser.add_argument("--period", type=int, default=7, help="Lookback period in days (default: 7)")
    parser.add_argument("--sync", action="store_true", help="Save all data to Analytics/meta-ads/")
    parser.add_argument("--export", metavar="FILE", help="Export campaign data to CSV")

    args = parser.parse_args()

    if args.setup:
        print_setup_guide()
        return

    # All other commands need credentials
    if not ACCESS_TOKEN or not ACCOUNT_ID:
        print("Error: Missing Meta Ads credentials")
        print("\nRequired environment variables:")
        print("  META_ADS_ACCESS_TOKEN - System User token")
        print("  META_ADS_ACCOUNT_ID   - Ad account ID (act_XXXXXXXXX)")
        print("\nRun with --setup for configuration instructions:")
        print("  uv run scripts/meta-ads-analytics.py --setup")
        sys.exit(1)

    days = args.period

    # Default to summary if no action specified
    has_action = any([
        args.summary, args.campaigns, args.campaign, args.adsets,
        args.ads, args.creative, args.audience, args.sync, args.export,
    ])
    if not has_action:
        args.summary = True

    if args.summary:
        insights = get_account_insights(days)
        if insights:
            print_summary(insights, days)
        else:
            print("  No data available for this period")

    if args.campaigns:
        campaigns = get_campaigns_insights(days)
        if campaigns:
            print_campaign_table(campaigns)
        else:
            print("  No campaign data available")

    if args.campaign:
        data = get_campaign_deep_dive(args.campaign, days)
        print_campaign_deep_dive(data, days)

    if args.adsets:
        adsets = get_adset_insights(days)
        if adsets:
            print_adset_table(adsets)
        else:
            print("  No ad set data available")

    if args.ads or args.creative:
        ads = get_ad_insights(days)
        if ads:
            print_ad_table(ads)
        else:
            print("  No ad data available")

    if args.audience:
        breakdowns = get_audience_breakdowns(days)
        print_audience_breakdowns(breakdowns)

    if args.sync:
        sync_all_data(days)

    if args.export:
        campaigns = get_campaigns_insights(days)
        export_path = Path(args.export)
        export_to_csv(campaigns, export_path)


if __name__ == "__main__":
    main()
