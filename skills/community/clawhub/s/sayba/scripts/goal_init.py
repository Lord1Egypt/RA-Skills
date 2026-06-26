#!/usr/bin/env python3
"""Sayba Skill 14: Initialize Goal-Driven Planning
Usage: python3 goal_init.py <api_key>
After calling this, the robot will automatically execute goals via server cron.
"""
import sys
import json
import urllib.request

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 goal_init.py <api_key>")
        sys.exit(1)
    
    api_key = sys.argv[1]
    url = "https://ai.sayba.com/api/v1/robot/goals/initialize"
    
    req = urllib.request.Request(url, method="POST", data=b"{}")
    req.add_header("Content-Type", "application/json")
    req.add_header("x-api-key", api_key)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
        
        if result.get("success"):
            data = result["data"]
            settings = data.get("settings", {})
            goal = data.get("goal")
            
            print("✅ Goal-driven planning enabled!")
            print(f"   auto_execute: {settings.get('auto_execute')}")
            print(f"   max_daily_actions: {settings.get('max_daily_actions')}")
            
            if goal:
                print(f"   Goal: {goal.get('title')}")
                plan = goal.get("plan")
                if plan and isinstance(plan, dict) and plan.get("steps"):
                    print(f"   Steps: {len(plan['steps'])}")
                    for s in plan["steps"]:
                        print(f"     {s['order']}. {s['title']} ({s.get('skill')})")
            
            print()
            print("Server cron will execute steps automatically every 15 minutes.")
            print("No local cron needed - the server handles everything!")
        else:
            print(f"❌ Failed: {result.get('message')}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
