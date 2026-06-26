---
name: system-watchdog
description: System resource monitoring. Detects actionable anomalies (memory pressure, runaway processes, disk pressure) and reports only when something needs attention. Optimized for few, high-signal alerts. Works on both Linux and macOS.
---

# System Watchdog

System watchdog for your machine. Detect real, actionable anomalies and stay quiet about normal steady-state conditions. Auto-detects Linux vs macOS.

## Goal

Optimize for **few, high-signal alerts**.

Do **not** alert on:
- process age alone (long-running is not "stale")
- Docker/container/virtualization baseline memory usage
- absolute disk-used GB unless near a real limit
- generic top-process lists without an actual anomaly

Do alert on:
- **memory pressure that is worsening** (swap growth, low available memory, macOS compressor pressure)
- **runaway process growth** (memory leak signals via delta tracking)
- **sustained abnormal CPU burn** (>2 cores for >15 min)
- **disk pressure near a practical limit** (>90% or <20 GB free)

## How to Invoke

```bash
bash ~/.openclaw/skills/system-watchdog/check.sh
```

The script outputs JSON to stdout. Parse the output and decide whether to report.

Override the state file path: `SYSTEM_WATCHDOG_STATE=/path/to/state.json`

## Output Format

```json
{
  "suspicious": true,
  "verdict": "watch|investigate|act_now|ok",
  "os": "Darwin|Linux",
  "summary": {
    "ram": "19.3/32.0 GB (60.4%)",
    "swap": "1.6/3.0 GB",
    "swap_delta": "+0.2 GB",
    "load": "3.30/2.21/2.17",
    "cores": 10,
    "disk": "14/926 GB (3%)",
    "available": "8.50 GB available",
    "free": "0.08 GB truly free",
    "inactive": "11.88 GB inactive/speculative",
    "compressed": "5.16 GB compressed"
  },
  "issues": [ ],
  "top_processes": [ ],
  "ignored_normals": [ ]
}
```

Note: `available` is Linux-only (MemAvailable). `free`, `inactive`, `compressed` are macOS-only (vm_stat breakdown).

## Detection Philosophy

### 1. Memory pressure, not just RAM usage
High RAM usage alone is noisy. The script tracks **swap growth since last run** and low available/free memory as stronger signals. On macOS, high compressor usage with low free pages is also flagged.

### 2. Runaway behavior, not stale age
Never flag a process just because it has been running a long time. Look for memory growth (delta since last run) and sustained CPU instead.

### 3. Disk only when it matters
Ignore absolute disk usage. Only report disk when it is actually nearing a practical limit.

## Agent Workflow

1. Run `check.sh`
2. Parse the JSON output
3. If `suspicious` is `false` → do nothing (no message)
4. If `suspicious` is `true` → format a concise report
5. Lead with the **verdict** and the 1–3 most important findings

## Report Format

```
⚠️ System Watchdog — VERDICT

Why this matters:
- <1–3 concise findings from issues[].why>

Evidence:
- RAM <summary.ram>
- Swap <summary.swap> (<summary.swap_delta>)
- Load <summary.load>

Recommended:
- <issue suggested_action>

Ignored: process age, Docker baseline, disk absolute usage
```

Keep it short. Do **not** dump every top process unless it directly supports an issue.

## State Tracking

The script persists lightweight state to `~/.openclaw/workspace/state/system-watchdog-state.json` so it can detect **changes since last run** (swap growth, per-process memory growth) rather than only snapshot values.
