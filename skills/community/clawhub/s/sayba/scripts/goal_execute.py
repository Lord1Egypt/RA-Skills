#!/usr/bin/env python3
"""Sayba Skill 14: Execute a pending step
Usage: python3 goal_execute.py <api_key> [goal_id] [step_id]
If no goal_id/step_id provided, executes the next pending step.
"""
import sys
import json
import urllib.request

def get_goals(api_key):
    url = "https://ai.sayba.com/api/v1/robot/goals"
    req = urllib.request.Request(url)
    req.add_header("x-api-key", api_key)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())

def execute_step(api_key, goal_id, step_id):
    url = f"https://ai.sayba.com/api/v1/robot/goals/{goal_id}/plan/steps/{step_id}/execute"
    req = urllib.request.Request(url, method="POST", data=b"{}")
    req.add_header("Content-Type", "application/json")
    req.add_header("x-api-key", api_key)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 goal_execute.py <api_key> [goal_id] [step_id]")
        sys.exit(1)
    
    api_key = sys.argv[1]
    
    # Find next pending step
    result = get_goals(api_key)
    if not result.get("success"):
        print(f"❌ Failed to get goals: {result.get('message')}")
        return
    
    for g in result["data"].get("goals", []):
        if g.get("status") != "active":
            continue
        plan = g.get("plan")
        if not plan or not isinstance(plan, dict):
            continue
        for s in plan.get("steps", []):
            if s.get("status") == "pending":
                goal_id = g["id"]
                step_id = s["id"]
                print(f"Executing: {s['title']} ({s.get('skill')})...")
                
                exec_result = execute_step(api_key, goal_id, step_id)
                if exec_result.get("success"):
                    step = exec_result["data"]["step"]
                    print(f"  Status: {step['status']}")
                    if step.get("result"):
                        r = step["result"]
                        if isinstance(r, dict):
                            if r.get("post"):
                                print(f"  Post: {r['post'].get('title', '')}")
                            if r.get("topics"):
                                print(f"  Topics: {r['topics'][:100]}...")
                            if r.get("summary"):
                                print(f"  Summary: {r['summary'][:100]}...")
                    if step.get("error"):
                        print(f"  Error: {step['error']}")
                else:
                    print(f"  ❌ Failed: {exec_result.get('message')}")
                return
    
    print("No pending steps to execute.")

if __name__ == "__main__":
    main()
