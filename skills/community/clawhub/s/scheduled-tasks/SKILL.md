---
name: scheduled-tasks
version: 2.1.7
description: >
  Create and manage OpenClaw scheduled tasks (reminders, periodic notifications, automated workflows).
  创建和管理 OpenClaw 定时任务（提醒、定时推送、自动化工作流）。
  Supports OpenClaw Cron API and system crontab with best practices and pitfall avoidance.
  支持 OpenClaw Cron API 和系统 crontab，包含最佳实践和避坑指南。
---

# Scheduled Tasks Skill | 定时任务技能

> **OpenClaw + 飞书定时任务解决方案**  
> **Version | 版本**: 2.1.7  
> **Author | 作者**: 9527  
> **License | 许可证**: MIT  

---

## Overview | 概述

This skill helps you create, manage, and troubleshoot scheduled tasks in OpenClaw. It supports two approaches: **OpenClaw Cron API** (recommended for Agent tasks) and **System Crontab** (for shell scripts).

本技能帮助您创建、管理和调试 OpenClaw 定时任务。支持两种方式：**OpenClaw Cron API**（推荐用于 Agent 任务）和**系统 Crontab**（适用于 Shell 脚本）。

### When to Use | 使用场景

| Scenario | Use OpenClaw Cron | Use System Crontab |
|----------|------------------|-------------------|
| One-time reminder (X minutes later) | ✅ `--at` | ❌ |
| Scheduled Agent task with reply | ✅ `--announce` | ⚠️ Complex |
| Scheduled shell script execution | ⚠️ Possible | ✅ Direct |
| Requires Agent thinking/tools | ✅ | ✅ via `openclaw agent` |
| Multiple Agents | ✅ `--agent` | ✅ `--agent` |
| Model/thinking override | ✅ `--model --thinking` | ❌ |
| Auto-retry on failure | ✅ Built-in | ❌ Manual |

| 场景 | 用 OpenClaw Cron | 用系统 Crontab |
|------|-----------------|---------------|
| 一次性提醒（X 分钟后） | ✅ `--at` | ❌ |
| 定时让 Agent 执行任务并回复 | ✅ `--announce` | ⚠️ 复杂 |
| 定时执行 Shell 脚本 | ⚠️ 可以 | ✅ 更直接 |
| 需要 Agent 思考和工具调用 | ✅ | ✅ 通过 `openclaw agent` |
| 需要指定不同 Agent | ✅ `--agent` | ✅ `--agent` |
| 需要模型/思考级别覆盖 | ✅ `--model --thinking` | ❌ |
| 任务失败自动重试 | ✅ 内置 | ❌ 需自行处理 |

**Principle | 原则**: Prefer OpenClaw Cron unless the task is essentially running a script without Agent involvement.  
**优先使用 OpenClaw Cron**，除非任务本质是运行脚本且不需要 Agent 参与。

---

## Quick Start | 快速开始

### One-Time Reminder | 一次性提醒

```bash
# Remind in 20 minutes | 20 分钟后提醒
openclaw cron add \
  --name "Water Reminder | 喝水提醒" \
  --at "20m" \
  --session main \
  --system-event "Time to drink water! 💧 | 主人，该喝水了 💧" \
  --wake now \
  --delete-after-run
```

### Daily Scheduled Task | 每日定时任务

```bash
# Daily news briefing at 08:00 | 每天 08:00 新闻播报
openclaw cron add \
  --name "Daily News | 每日新闻" \
  --cron "0 8 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --agent <agent-id> \
  --message "Search today's news and send to user | 搜索今日新闻并推送" \
  --announce \
  --channel feishu \
  --to "user:<user_open_id>"
```

---

## Method 1: OpenClaw Cron API (Recommended) | 方式一：OpenClaw Cron API（推荐）

### Basic Commands | 基础命令

```bash
# List all tasks | 查看所有任务
openclaw cron list

# Run task manually | 手动触发任务
openclaw cron run <jobId>

# View run history | 查看运行历史
openclaw cron runs --id <jobId>

# Edit task | 编辑任务
openclaw cron edit <jobId> --message "New message | 新消息"

# Disable task | 禁用任务
openclaw cron edit <jobId> --enabled false

# Remove task | 删除任务
openclaw cron remove <jobId>
```

### Common Patterns | 常见模式

#### Pattern 1: One-Time Reminder | 一次性提醒

```bash
openclaw cron add \
  --name "Meeting Reminder | 会议提醒" \
  --at "2026-03-27T09:00:00+08:00" \
  --session main \
  --system-event "Meeting at 9 AM! | 9 点有会议，请准备" \
  --wake now \
  --delete-after-run
```

#### Pattern 2: Daily Agent Task | 每日 Agent 任务

```bash
openclaw cron add \
  --name "Daily News | 每日新闻" \
  --cron "0 16 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --agent <agent-id> \
  --message "Search today's news | 搜索今日新闻" \
  --announce \
  --channel feishu \
  --to "user:<user_open_id>"
```

#### Pattern 3: Weekday Report | 工作日报告

```bash
openclaw cron add \
  --name "Daily Work Report | 今日工作简报" \
  --cron "55 22 * * 1-5" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "Summarize today's work | 整理今天完成的工作" \
  --announce \
  --channel feishu \
  --to "user:<user_open_id>"
```

---

## Method 2: System Crontab + openclaw agent | 方式二：系统 Crontab + openclaw agent

### Script Template | 脚本模板

Create script at `scripts/daily-task.sh`:

```bash
#!/bin/bash
# Daily scheduled task script | 定时任务脚本
# Cron: 0 16 * * * (Daily at 16:00 | 每天 16:00)

set -e

export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Task started | 任务开始..."

openclaw agent \
  --agent <agent-id> \
  --deliver \
  --reply-account <feishu-account-id> \
  --reply-to "user:<user_open_id>" \
  -m "Your task message | 你的任务指令"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Task completed | 任务完成"
```

### Add to Crontab | 添加到 Crontab

```bash
# Edit crontab | 编辑 crontab
crontab -e

# Add line (daily at 16:00 | 每天 16:00)
0 16 * * * /path/to/scripts/daily-task.sh >> /tmp/task-name.log 2>&1
```

### Cron Expression Reference | Cron 表达式速查

```
┌───────── Minute (0-59) | 分
│ ┌─────── Hour (0-23) | 时
│ │ ┌───── Day of month (1-31) | 日
│ │ │ ┌─── Month (1-12) | 月
│ │ │ │ ┌─ Day of week (0-7, 0&7=Sunday) | 周
│ │ │ │ │
* * * * *

0 9 * * *       Daily at 09:00 | 每天 09:00
0 9 * * 1-5     Weekdays at 09:00 | 工作日 09:00
*/30 * * * *    Every 30 minutes | 每 30 分钟
0 9,16 * * *    Daily at 09:00 and 16:00 | 每天 09:00 和 16:00
0 0 1 * *       First day of month | 每月第一天
```

---

## Common Pitfalls & Solutions | 常见陷阱与解决方案

### ⚠️ Pitfall 1: Missing Delivery Target | 缺少投递目标

```bash
# ❌ WRONG | 错误
openclaw agent --agent x --deliver -m "message"
# Error: "Delivering to Feishu requires target"

# ✅ CORRECT | 正确
openclaw agent --agent x --deliver \
  --reply-account <account-id> \
  --reply-to "user:<user_open_id>" \
  -m "message"
```

### ⚠️ Pitfall 2: Message Position | Message 位置错误

```bash
# ❌ WRONG | 错误
openclaw agent --agent x --deliver "message"

# ✅ CORRECT | 正确
openclaw agent --agent x --deliver -m "message"
```

### ⚠️ Pitfall 3: Timezone Missing | 缺少时区

```bash
# ❌ WRONG (defaults to UTC) | 错误（默认 UTC）
openclaw cron add --at "2026-03-27T09:00:00" ...

# ✅ CORRECT (with timezone) | 正确（带时区）
openclaw cron add --at "2026-03-27T09:00:00+08:00" ...

# ✅ CORRECT (cron with --tz) | 正确（cron 带--tz）
openclaw cron add --cron "0 9 * * *" --tz "Asia/Shanghai" ...
```

### ⚠️ Pitfall 4: Unreliable Sleep | 不可靠的 sleep

```bash
# ❌ NOT RECOMMENDED | 不推荐
sleep 300 && openclaw agent -m "Reminder" --deliver ...

# ✅ RECOMMENDED | 推荐
openclaw cron add --at "5m" --session main \
  --system-event "Reminder" --wake now --delete-after-run
```

### ⚠️ Pitfall 5: Missing PATH in Crontab | Crontab 缺少 PATH

```bash
# ❌ WRONG | 错误
0 9 * * * /path/to/script.sh

# ✅ CORRECT (add to script header) | 正确（脚本开头添加）
#!/bin/bash
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
```

### ⚠️ Pitfall 6: Cross-Agent Communication | 跨 Agent 通信受限

```bash
# ❌ WRONG | 错误
# sessions_send to another Agent will be rejected

# ✅ CORRECT Option 1 | 正确方式 1
openclaw agent --agent target-agent -m "task" --deliver ...

# ✅ CORRECT Option 2 | 正确方式 2
# Write to target Agent's HEARTBEAT.md
```

### ⚠️ Pitfall 7: Feishu Bot Limitations | 飞书 Bot 限制

```bash
# ❌ WRONG | 错误
# Bot A cannot send Feishu message to Bot B

# ✅ CORRECT | 正确
# Use openclaw agent command or human relay
```

### ⚠️ Pitfall 8: No Validation After Creation | 创建后未验证

```bash
# After creating, always verify | 创建后立即检查
openclaw cron list

# Test manually | 手动测试
openclaw cron run <jobId>

# Check results | 查看结果
openclaw cron runs --id <jobId>
```

---

## Troubleshooting Guide | 故障排查指南

### Quick Troubleshooting Table | 快速排查表

| Problem | Check Command |
|---------|--------------|
| Task not executed | `openclaw cron list` (check exists & enabled) |
| Execution failed | `openclaw cron runs --id <jobId>` |
| No Feishu message | Check `--reply-to` & Agent Feishu config |
| Crontab not running | `tail -f /tmp/task-name.log` |
| Wrong time | Check timezone `--tz "Asia/Shanghai"` |

| 问题 | 排查命令 |
|------|---------|
| 任务没执行 | `openclaw cron list` 检查是否存在且 enabled |
| 执行失败 | `openclaw cron runs --id <jobId>` 查看历史 |
| 飞书没收到 | 检查 `--reply-to` 是否正确、Agent 飞书账号是否配置 |
| crontab 没执行 | `tail -f /tmp/task-name.log` 查看日志 |
| 时间不对 | 检查时区配置 `--tz "Asia/Shanghai"` |

### Debug Mode | 调试模式

```bash
# Enable verbose logging | 启用详细日志
export OPENCLAW_DEBUG=1

# Run task with debug | 调试模式运行任务
openclaw cron run <jobId> --debug

# Check OpenClaw logs | 查看 OpenClaw 日志
tail -f ~/.openclaw/logs/openclaw.log
```

---

## Best Practices | 最佳实践

### 1. Naming Convention | 命名规范

```bash
# Good | 好
--name "daily-news-briefing"
--name "daily-news-briefing | 每日新闻播报"

# Bad | 不好
--name "task1"
--name "test"
```

### 2. Timezone Always Specified | 始终指定时区

```bash
# Always include --tz for cron expressions | cron 表达式始终包含--tz
--cron "0 9 * * *" --tz "Asia/Shanghai"

# Always include timezone offset for --at | --at 始终包含时区偏移
--at "2026-03-27T09:00:00+08:00"
```

### 3. Logging | 日志记录

```bash
# For crontab scripts | Crontab 脚本
>> /tmp/task-name.log 2>&1

# For OpenClaw cron | OpenClaw cron
openclaw cron runs --id <jobId>
```

### 4. Testing | 测试

```bash
# 1. Create task | 创建任务
openclaw cron add ...

# 2. Verify exists | 验证存在
openclaw cron list

# 3. Run manually | 手动运行
openclaw cron run <jobId>

# 4. Check result | 检查结果
openclaw cron runs --id <jobId>
```

### 5. Security | 安全

```bash
# ✅ DO: Store credentials in your own environment config | 凭证存于您自己的环境配置
# ✅ DO: Use environment variables in scripts | 脚本中使用环境变量
# ❌ DON'T: Hardcode tokens in scripts | 脚本中硬编码 token
# ❌ DON'T: Put .env in skill package | 技能包中不放.env
```

---

## Examples | 完整示例

### Example 1: Water Reminder | 喝水提醒

```bash
openclaw cron add \
  --name "water-reminder | 喝水提醒" \
  --at "20m" \
  --session main \
  --system-event "Time to drink water! 💧 | 主人，该喝水了 💧" \
  --wake now \
  --delete-after-run
```

### Example 2: Daily News Briefing | 每日新闻播报

```bash
openclaw cron add \
  --name "daily-news | 每日新闻" \
  --cron "0 8 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --agent <agent-id> \
  --message "Search today's news and send to user | 搜索今日新闻并发给用户" \
  --announce \
  --channel feishu \
  --to "user:<user_open_id>"
```

### Example 3: Workday Report | 工作日简报

```bash
openclaw cron add \
  --name "workday-report | 工作日简报" \
  --cron "55 22 * * 1-5" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "Summarize today's work | 整理今天完成的工作" \
  --announce \
  --channel feishu \
  --to "user:<user_open_id>"
```

### Example 4: System Crontab Script | 系统 Crontab 脚本

Script `scripts/daily-news.sh`:

```bash
#!/bin/bash
set -e
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting daily news briefing..."

openclaw agent \
  --agent <agent-id> \
  --deliver \
  --reply-account <feishu-account-id> \
  --reply-to "user:<user_open_id>" \
  -m "Search today's news and send to user"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Completed"
```

Crontab entry:

```bash
0 8 * * * /path/to/scripts/daily-news.sh >> /tmp/daily-news.log 2>&1
```

---

## API Reference | API 参考

### OpenClaw Cron Commands | OpenClaw Cron 命令

| Command | Description |
|---------|-------------|
| `openclaw cron add` | Create new scheduled task |
| `openclaw cron list` | List all tasks |
| `openclaw cron run <id>` | Run task manually |
| `openclaw cron runs --id <id>` | View run history |
| `openclaw cron edit <id>` | Edit task configuration |
| `openclaw cron remove <id>` | Delete task |

| 命令 | 说明 |
|------|------|
| `openclaw cron add` | 创建新定时任务 |
| `openclaw cron list` | 查看所有任务 |
| `openclaw cron run <id>` | 手动运行任务 |
| `openclaw cron runs --id <id>` | 查看运行历史 |
| `openclaw cron edit <id>` | 编辑任务配置 |
| `openclaw cron remove <id>` | 删除任务 |

### Common Options | 常用选项

| Option | Description | Example |
|--------|-------------|---------|
| `--name` | Task name | `"daily-news"` |
| `--at` | One-time execution time | `"20m"`, `"2026-03-27T09:00:00+08:00"` |
| `--cron` | Cron expression | `"0 9 * * *"` |
| `--tz` | Timezone | `"Asia/Shanghai"` |
| `--session` | Session type | `main`, `isolated` |
| `--agent` | Target Agent ID | `news-assistant` |
| `--message` | Task message | `"Search news"` |
| `--announce` | Announce result | (flag) |
| `--channel` | Delivery channel | `feishu` |
| `--to` | Target user | `"user:<user_open_id>"` |
| `--delete-after-run` | Auto-delete after run | (flag) |
| `--wake` | Wake session | `now`, `never` |

---

## Contributing | 贡献

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

---

## License | 许可证

MIT License - See LICENSE file for details.

---

## Support | 支持

- **Documentation | 文档**: https://docs.openclaw.ai
- **Community | 社区**: https://discord.com/invite/clawd
- **Skill Market | 技能市场**: https://clawhub.com

---

*Last Updated | 最后更新*: 2026-03-27  
*Version | 版本*: 2.1.7
