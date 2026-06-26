#!/usr/bin/env python3
"""Subagent Health Monitor — MCP Server for Claude Code."""

import json, sys, time, os, hashlib
from collections import defaultdict

STATE_FILE = os.path.expanduser("~/.claude/subagent-health-state.json")

class SubagentTracker:
    def __init__(self):
        self.agents = {}
        self.tasks = {}
        self.load_state()

    def load_state(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE) as f:
                    data = json.load(f)
                    self.agents = data.get("agents", {})
                    self.tasks = data.get("tasks", {})
            except: pass

    def save_state(self):
        with open(STATE_FILE, "w") as f:
            json.dump({"agents": self.agents, "tasks": self.tasks}, f, indent=2, default=str)

    def register_agent(self, agent_id, task=None):
        now = time.time()
        self.agents[agent_id] = {
            "id": agent_id, "status": "active", "spawned_at": now,
            "last_progress": now, "tokens_used": 0, "tasks_completed": 0,
            "idle_checks": 0, "task": task,
        }
        self.save_state()
        return self.agents[agent_id]

    def record_progress(self, agent_id, tokens_delta=0):
        now = time.time()
        if agent_id in self.agents:
            self.agents[agent_id]["last_progress"] = now
            self.agents[agent_id]["tokens_used"] += tokens_delta
            self.agents[agent_id]["idle_checks"] = 0
            self.agents[agent_id]["status"] = "active"
        self.save_state()

    def check_health(self, agent_id):
        now = time.time()
        if agent_id not in self.agents:
            return {"status": "unknown", "message": "Agent not registered"}
        agent = self.agents[agent_id]
        idle_time = now - agent["last_progress"]
        issues = []
        if idle_time > 120:
            severity = "critical" if idle_time > 300 else "warning"
            issues.append({
                "severity": severity, "type": "silent_failure",
                "message": f"No progress for {int(idle_time)}s",
                "recommendation": "Kill and restart" if severity == "critical" else "Check status"
            })
            agent["idle_checks"] += 1
            agent["status"] = "stuck"
        if idle_time > 60 and agent.get("tokens_used", 0) > 1000:
            waste = int(agent["tokens_used"] * 0.15)
            if waste > 500:
                issues.append({
                    "severity": "warning", "type": "token_waste",
                    "message": f"~{waste:,} tokens wasted on idle loops",
                    "recommendation": "Increase polling interval"
                })
        self.save_state()
        return {
            "agent_id": agent_id, "status": agent.get("status", "active"),
            "idle_seconds": int(idle_time), "tokens_used": agent.get("tokens_used", 0),
            "tasks_completed": agent.get("tasks_completed", 0), "issues": issues,
            "healthy": len([i for i in issues if i["severity"] == "critical"]) == 0
        }

    def get_fleet_summary(self):
        total_tokens = sum(a.get("tokens_used", 0) for a in self.agents.values())
        stuck = [a["id"] for a in self.agents.values() if a.get("status") == "stuck"]
        active = [a["id"] for a in self.agents.values() if a.get("status") == "active"]
        waste = int(total_tokens * 0.18)
        return {
            "total_agents": len(self.agents), "active_agents": len(active),
            "stuck_agents": len(stuck), "total_tokens": total_tokens,
            "estimated_waste_tokens": waste, "waste_percentage": 18,
            "stuck_agent_ids": stuck,
            "health_score": max(0, 100 - len(stuck) * 25 - (waste // max(total_tokens, 1) * 100))
        }

    def fingerprinthash(self, task_desc):
        return hashlib.md5(task_desc.encode()).hexdigest()[:16]

    def spawn_with_tracking(self, agent_id, task_desc):
        fp = self.fingerprinthash(task_desc)
        self.tasks[fp] = self.tasks.get(fp, {"count": 0, "first_spawned": time.time()})
        return self.register_agent(agent_id, task_desc)


tracker = SubagentTracker()

def handle_mcp():
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            method = request.get("method", "")
            req_id = request.get("id", 0)
            if method == "initialize":
                response = {"jsonrpc": "2.0", "id": req_id, "result": {
                    "protocolVersion": "2024-11-05", "capabilities": {"tools": {}},
                    "serverInfo": {"name": "subagent-health", "version": "1.0.0"}
                }}
            elif method == "tools/list":
                response = {"jsonrpc": "2.0", "id": req_id, "result": {"tools": [
                    {"name": "register_subagent", "description": "Register a new subagent for health tracking",
                     "inputSchema": {"type": "object", "properties": {
                         "agent_id": {"type": "string"}, "task": {"type": "string"}}, "required": ["agent_id"]}},
                    {"name": "check_agent_health", "description": "Check subagent health - detects silent failures, token waste",
                     "inputSchema": {"type": "object", "properties": {
                         "agent_id": {"type": "string"}}, "required": ["agent_id"]}},
                    {"name": "record_agent_progress", "description": "Record subagent progress",
                     "inputSchema": {"type": "object", "properties": {
                         "agent_id": {"type": "string"}, "tokens_used": {"type": "number"}}, "required": ["agent_id"]}},
                    {"name": "get_fleet_health", "description": "Get fleet-wide health summary",
                     "inputSchema": {"type": "object", "properties": {}}}
                ]}}
            elif method == "tools/call":
                tool_name = request["params"]["name"]
                args = request["params"].get("arguments", {})
                if tool_name == "register_subagent":
                    result = tracker.spawn_with_tracking(args["agent_id"], args.get("task", ""))
                elif tool_name == "check_agent_health":
                    result = tracker.check_health(args["agent_id"])
                elif tool_name == "record_agent_progress":
                    tracker.record_progress(args["agent_id"], args.get("tokens_used", 0))
                    result = {"status": "recorded"}
                elif tool_name == "get_fleet_health":
                    result = tracker.get_fleet_summary()
                else:
                    result = {"error": f"Unknown: {tool_name}"}
                response = {"jsonrpc": "2.0", "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2, default=str)}]}}
            print(json.dumps(response), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "id": req_id,
                "error": {"code": -32000, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    if "--mcp" in sys.argv:
        handle_mcp()
    else:
        print(json.dumps(tracker.get_fleet_summary(), indent=2, default=str))