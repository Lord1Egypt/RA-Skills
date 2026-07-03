---
name: screen-activity-tracker
description: "Screen activity tracking. Trigger: track screen activity, start/stop tracking, daily summary, search history, 开始追踪屏幕, 屏幕活动总结, 整理今天的操作. Uses cron tool for tracking and bash for summary/search."
version: "1.0.0"
license: "MIT"
author: "zeject"
homepage: "https://github.com/zeject/screen-activity-tracker"
metadata:
  openclaw:
    emoji: "🖥️"
    os: ["darwin"]
    requires:
      bins: ["peekaboo", "python3"]
    install:
      - kind: "npm-global"
        pkg: "@steipete/peekaboo"
        bins: ["peekaboo"]
        label: "Install Peekaboo (npm)"
      - id: "python3"
        kind: "system"
        label: "Python 3.x required"
---

# Screen Activity Tracker

Periodically capture screenshots, analyze with a VL model, and log activity to SiYuan Note or local markdown files.

## ⚠️ CRITICAL: Tool Usage Rules

**NEVER call `skill_workshop` tool.** It will error. Only use:

| User Intent | Tool | How |
|-------------|------|-----|
| Start tracking | `cron` | `{"operation":"add","name":"屏幕活动记录","command":"...","cron":"*/5 * * * *"}` |
| Stop/Resume/List | `cron` | `{"operation":"edit","jobId":"...","enabled":false}` or `{"operation":"list"}` |
| Daily summary | **bash** | `python3 <SKILL_DIR>/scripts/activity-analyzer.py summary` |
| Search history | **bash** | `python3 <SKILL_DIR>/scripts/activity-analyzer.py search "keyword"` |

---

## Start Tracking

1. Read `<SKILL_DIR>/config.json` for `interval_minutes` (default 5 → `*/5 * * * *`)
2. Call `cron` tool:
```json
{
  "operation": "add",
  "name": "屏幕活动记录",
  "command": "sh -lc '/bin/bash <SKILL_DIR>/scripts/screen-activity.sh'",
  "cron": "*/5 * * * *",
  "timeoutSeconds": 90
}
```
3. Report job ID + interval to user.

## Stop / Edit

```json
{"operation": "edit", "jobId": "<id>", "enabled": false}
{"operation": "edit", "jobId": "<id>", "cron": "*/10 * * * *"}
{"operation": "list"}
```

## Summary & Search (bash)

```bash
python3 <SKILL_DIR>/scripts/activity-analyzer.py summary
python3 <SKILL_DIR>/scripts/activity-analyzer.py search "VS Code"
```

## Config (config.json)

```json
{
  "backend": "siyuan",
  "siyuan": {"url":"http://192.168.1.100:6806","token":"...","notebook_id":"..."},
  "local": {"output_dir":"~/screen-activity","keep_days":7},
  "mlx_url": "http://192.168.1.198:18000/v1",
  "analysis_mode": "simple",
  "interval_minutes": 5
}
```

## License

MIT
