---
name: Windmill
description: Build automation workflows and internal tools with Windmill's code-first platform.
metadata: {"clawdbot":{"emoji":"🌀","os":["linux","darwin","win32"]}}
---

## Script Traps
- Main function signature determines input schema — Windmill infers from type hints, wrong types break the UI form
- Return value is the script output — forgetting to return means downstream steps get nothing
- Python dependencies go in inline `requirements.txt` comment — not a global file, each script is isolated
- TypeScript runs on Bun — Node.js-specific APIs may not work

## Flow Execution
- `results.step_name` fails if step hasn't run yet — conditional branches cause undefined access errors
- Parallel branches need explicit configuration — default is sequential, not concurrent
- Suspend steps wait forever without timeout — set explicit timeout or flow hangs indefinitely
- Error handlers only catch step failures — script syntax errors bypass handlers

## Scheduling Pitfalls
- Timezone defaults to server timezone — set explicitly or jobs fire at unexpected times
- Concurrent execution allowed by default — add mutex lock if jobs shouldn't overlap
- Schedules attach to scripts/flows — no standalone schedule entities, delete script = delete schedule

## Secrets and Variables
- Secrets cannot be read back from UI after creation — store originals securely elsewhere
- Variables are plaintext and visible — never put sensitive data in variables, only secrets
- Path format matters — `u/username/secret` for user, `f/folder/secret` for shared

## Self-Hosting
- PostgreSQL is the only state — workers are stateless, back up only the database
- Single container includes workers — fine for small loads, separate workers for scale
- Worker count determines parallelism — one worker = one concurrent script execution

## Webhook Triggers
- Each script/flow gets unique webhook URL — changes if you rename the script
- Webhook payload becomes script input — schema must match expected arguments
- No built-in auth on webhooks — validate tokens in script logic or use reverse proxy

## Common Mistakes
- Testing flows without testing scripts first — debug scripts individually
- Expecting state between runs — use variables or external storage for persistence
- Hardcoding paths — use `wmill.get_resource()` for portability between workspaces
