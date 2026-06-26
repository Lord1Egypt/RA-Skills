#!/usr/bin/env python3
"""Show solopreneur business dashboard."""
import json
import os
from datetime import datetime

SOLO_DIR = os.path.expanduser("~/.openclaw/workspace/memory/solopreneur")

def load_data():
    dashboard_file = os.path.join(SOLO_DIR, "dashboard.json")
    if os.path.exists(dashboard_file):
        with open(dashboard_file, 'r') as f:
            return json.load(f)
    return {
        "revenue_ytd": 0,
        "active_clients": 0,
        "outstanding_invoices": 0,
        "pipeline_value": 0
    }

def main():
    print("\n📊 BUSINESS DASHBOARD")
    print("=" * 60)
    
    data = load_data()
    
    print("\n💰 REVENUE")
    print(f"  YTD: ${data.get('revenue_ytd', 0):,.2f}")
    print(f"  Monthly avg: ${data.get('revenue_ytd', 0) / max(1, datetime.now().month):,.2f}")
    
    print("\n👥 CLIENTS")
    print(f"  Active: {data.get('active_clients', 0)}")
    print(f"  Outstanding invoices: {data.get('outstanding_invoices', 0)}")
    
    print("\n📈 PIPELINE")
    print(f"  Total value: ${data.get('pipeline_value', 0):,.2f}")
    print(f"  Prospects: {data.get('prospect_count', 0)}")
    
    print("\n🎯 TOP PRIORITIES")
    print("  1. [Add priority via set_priority.py]")
    print("  2. [Add priority via set_priority.py]")
    print("  3. [Add priority via set_priority.py]")
    
    print("\n⚡ QUICK ACTIONS")
    print("  • Follow up on cold leads (7+ days)")
    print("  • Send outstanding invoices")
    print("  • Review weekly goals")

if __name__ == '__main__':
    main()
