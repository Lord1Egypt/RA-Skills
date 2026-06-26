#!/usr/bin/env python3
"""Sayba Skill 14: Check Goal Status
Usage: python3 goal_status.py <api_key>
"""
import sys
import json
import urllib.request

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 goal_status.py <api_key>")
        sys.exit(1)
    
    api_key = sys.argv[1]
    url = "https://ai.sayba.com/api/v1/robot/goals"
    
    req = urllib.request.Request(url)
    req.add_header("x-api-key", api_key)
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode())
        
        if result.get("success"):
            data = result["data"]
            settings = data.get("settings", {})
            
            print(f"auto_execute: {settings.get('auto_execute')}")
            print(f"remaining today: {settings.get('max_daily_actions', 20)}")
            print()
            
            for g in data.get("goals", []):
                print(f"📌 {g.get('title')} [{g.get('status')}] progress={g.get('progress')}%")
                plan = g.get("plan")
                if plan and isinstance(plan, dict) and plan.get("steps"):
                    for s in plan["steps"]:
                        icon = {"pending": "⏳", "running": "🔄", "completed": "✅", "failed": "❌"}.get(s.get("status"), "❓")
                        print(f"   {icon} {s['order']}. {s['title']} ({s.get('skill')})")
                print()
        else:
            print(f"❌ Failed: {result.get('message')}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
