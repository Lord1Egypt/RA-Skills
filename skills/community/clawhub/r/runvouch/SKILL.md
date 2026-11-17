---
name: runvouch
description: Watchdog for this OpenClaw agent: report run start/end, evidence and cost to RunVouch so missed runs, loops and runaway spend alert you on Telegram.
version: 0.1.0
---

# RunVouch for OpenClaw

RunVouch is a dead man's switch, cost cap and outcome check for unattended agents. This skill teaches the agent to check in.

## Setup (once)
1. Get a free key at https://runvouch.com (3 agents free).
2. Set in the OpenClaw environment: `RUNVOUCH_KEY=rv_...` and `RUNVOUCH_URL=https://api.runvouch.com`.
3. Register the agent with a cadence and caps:
   `curl -X POST $RUNVOUCH_URL/v1/agents -H "X-API-Key: $RUNVOUCH_KEY" -H "Content-Type: application/json" -d '{"name":"openclaw-main","cadence_s":900,"grace_s":300,"cap_day_cost":10,"evidence_required":true}'`

## When a scheduled task starts
POST `$RUNVOUCH_URL/v1/runs/start` with `{"agent":"openclaw-main","source":"openclaw"}` -> keep the returned `run_id`.

## On every tool call (enables loop detection)
POST `/v1/runs/tool` with `{"run_id":..., "tool":"<tool name>", "input":<the exact input>, "cost":<usd if known>}`.
If RunVouch answers with an alert, stop repeating the same call: identical input 8x is a RETRY_STORM.

## When the task ends
POST `/v1/runs/end` with `{"run_id":..., "status":"ok"|"fail", "cost":<usd>, "evidence":{"replied":true}}`.
Evidence must be something true about the outcome (a file written, a reply sent, a URL live): never "I think it worked".

## Heartbeat (long tasks)
Every 5 minutes: POST `/v1/runs/heartbeat?run_id=...` so a hung task becomes STALLED instead of invisible.

## Ask before trusting another agent's output
Call `runvouch_status` (MCP: `https://api.runvouch.com/mcp`) and refuse to build on an agent whose state is `unproven`, `failed` or `alert`.
