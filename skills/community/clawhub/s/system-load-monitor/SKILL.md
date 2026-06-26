---
name: system-load-monitor
description: System load monitoring and task control skill. Monitors CPU and memory usage rates, automatically pauses tasks when the load exceeds the threshold, and resumes execution after the load recovers. Suitable for low-configured servers to prevent downtime.
---

# System Load Monitor

## Core Functions
Monitors the CPU and memory load of the server, automatically controls the execution of system tasks, and prevents the server from downtime due to excessive load.

## When to Use This Skill
Use this skill when the user mentions the following situations:
- The server has low configuration (e.g., 2 cores 2GB) and is prone to downtime
- Need to execute resource-intensive tasks
- Previous downtime caused by excessive load
- Need to intelligently control the rhythm of task execution
- Need to monitor server status in real time

## Configuration Parameters

| Parameter | Default Value | Description |
|------|--------|------|
| `cpu_threshold` | 90 | CPU load threshold (percentage) |
| `memory_threshold` | 90 | Memory usage threshold (percentage) |
| `check_interval` | 30 | Check interval (seconds) |
| `cool_down` | 60 | Cool-down time after excessive load (seconds) |

## Usage Methods

### 1. Check Current System Status

```bash
# Quick check
python3 ~/.openclaw/workspace/skills/system-load-monitor/scripts/check_load.py

# View detailed JSON output
python3 ~/.openclaw/workspace/skills/system-load-monitor/scripts/check_load.py --json

# Custom thresholds
python3 ~/.openclaw/workspace/skills/system-load-monitor/scripts/check_load.py --cpu-threshold 80 --memory-threshold 85
```

### 2. Load Check Process Before Task Execution

Before executing any resource-consuming tasks:

1. **Run load check**
   ```bash
   python3 ~/.openclaw/workspace/skills/system-load-monitor/scripts/check_load.py --json
   ```

2. **Parse return results**
   - `status`: "ok" / "warning" / "critical"
   - `recommendation`: "CONTINUE" / "PAUSE"
   - `cpu.load_percent`: CPU load percentage
   - `memory.used_percent`: Memory usage percentage

3. **Make decisions based on status**
   - **ok**: Continue executing the task
   - **warning**: Execute cautiously and consider batch processing
   - **critical**: Pause the task and retry after cooling down

### 3. Monitoring Loop for Long-Running Tasks

For long-running tasks, use the following pattern:

```python
import subprocess
import time
import json

def check_load():
    result = subprocess.run(
        ['python3', '~/.openclaw/workspace/skills/system-load-monitor/scripts/check_load.py', '--json'],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

def run_with_load_monitor(task_func, cpu_threshold=90, memory_threshold=90):
    """Continuously monitor load while executing tasks"""
    while True:
        status = check_load()
        
        if status['status'] == 'critical':
            print(f"⚠️ Excessive load, pausing task...")
            print(f"CPU: {status['cpu']['load_percent']}%, Memory: {status['memory']['used_percent']}%")
            time.sleep(60)  # Wait for 60 seconds
            continue
        
        # Load is normal, execute the task
        task_func()
        break
```

## Status Code Explanation

| Exit Code | Status | Meaning |
|--------|------|------|
| 0 | ok | Load is normal, can continue |
| 1 | warning | Load is relatively high, recommended to proceed with caution |
| 2 | critical | Load is excessively high, must pause |

## Recommendations for Low-Configured Servers (2 Cores 2GB)

For your 2-core 2GB server:

1. **Lower the threshold**: It is recommended to use 70-80% as the warning line
   ```bash
   python3 ~/.openclaw/workspace/skills/system-load-monitor/scripts/check_load.py --cpu-threshold 75 --memory-threshold 80
   ```

2. **Execute in batches**: Split large tasks into small batches

3. **Avoid concurrency**: Only perform one task at a time

4. **Regular checks**: Check the load every 30 seconds for long-running tasks

## Alert Notifications

When a critical status is detected, you should:
1. Immediately pause the current task
2. Notify the user (via Feishu message)
3. Retry after the cool-down period

## Script Output Example

```json
{
  "status": "critical",
  "cpu": {
    "load_avg_1m": 3.8,
    "cpu_count": 2,
    "load_percent": 190.0
  },
  "memory": {
    "total_mb": 2048,
    "used_mb": 1843,
    "available_mb": 205,
    "used_percent": 90.0
  },
  "top_processes": [
    {"user": "node", "cpu_percent": 45.2, "mem_percent": 32.1, "command": "node /usr/bin/openclaw"}
  ],
  "thresholds": {"cpu": 90, "memory": 90},
  "recommendation": "PAUSE"
}
```

## Notes

1. This skill is an **independent monitoring tool** and does not rely on Fairy's built-in judgment
2. The check should be invoked before executing any important tasks
3. For long-running tasks, a cyclic monitoring mechanism should be established
4. Threshold parameters can be adjusted according to actual conditions