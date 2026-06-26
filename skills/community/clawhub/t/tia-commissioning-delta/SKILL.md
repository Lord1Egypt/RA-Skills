---
name: TIA_COMMISSIONING_DELTA
description: Use TIA Openness to compare latest site backup against yesterday's baseline with focus on process control logic.
tools:
 - shell
 - filesystem
---

You can:
- Access site backups (e.g. from cloud storage or NAS).
- Call external scripts that:
 - extract DB/FB logic via Openness
 - compute diffs for PID blocks, safety blocks, and sequences
- Return structured JSON with:
 - changed PIDs
 - bypassed interlocks
 - changed sequences and alarms.

When the field engineer asks "@OpenClaw diff the latest site backup against yesterday's baseline":
1) Locate both .zap18 archives.
2) Run the commissioning diff script.
3) Return a compact JSON of the most significant changes for the agent to explain.
