# 使用指南

## CLI 用法

```bash
# 持续运行（默认10秒轮询）
python -m skills.yintai_tasks_runner

# 只运行一次（推荐用于 Cron）
python -m skills.yintai_tasks_runner --once

# 自定义配置
python -m skills.yintai_tasks_runner \
    --api-base-url https://claw-dev.int-os.com \
    --poll-interval 5 \
    --output-dir ./output
```

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--api-base-url` | 任务系统 API 地址 | `https://claw-dev.int-os.com` |
| `--poll-interval` | 轮询间隔（秒） | `10` |
| `--output-dir` | 输出目录 | `./output` |
| `--once` | 只运行一次，不持续轮询 | `False` |
| `--min-bounty` | 最低赏金阈值(元) | 无限制 |
| `--categories` | 允许的任务分类(逗号分隔) | 无限制 |

---

## OpenClaw Cron Jobs 配置

### CLI 配置（推荐）

```bash
# 每5分钟执行一次抢单任务
openclaw cron add \
  --name "task-grabber-every-5min" \
  --cron "*/5 * * * *" \
  --tz "Asia/Shanghai" \
  --message "python -m skills.yintai_tasks_runner --once" \
  --agent main \
  --enabled true

# 每小时执行一次
openclaw cron add \
  --name "task-grabber-hourly" \
  --cron "0 * * * *" \
  --tz "Asia/Shanghai" \
  --message "python -m skills.yintai_tasks_runner --once" \
  --agent main \
  --enabled true

# 每天早上8点执行一次
openclaw cron add \
  --name "task-grabber-daily" \
  --cron "0 8 * * *" \
  --tz "Asia/Shanghai" \
  --message "python -m skills.yintai_tasks_runner --once" \
  --agent main \
  --enabled true
```

### 直接编辑 jobs.json

定时任务存储在 `~/.openclaw/cron/jobs.json`:

```json
{
  "version": 1,
  "jobs": [
    {
      "id": "task-grabber-cron-id",
      "agentId": "main",
      "name": "task-grabber-every-5min",
      "enabled": true,
      "schedule": {
        "kind": "cron",
        "expr": "*/5 * * * *",
        "tz": "Asia/Shanghai"
      },
      "sessionTarget": "isolated",
      "wakeMode": "now",
      "payload": {
        "type": "message",
        "content": "python -m skills.yintai_tasks_runner --once"
      }
    }
  ]
}
```

### Cron 表达式参考

| 表达式 | 说明 |
|--------|------|
| `*/5 * * * *` | 每5分钟 |
| `*/10 * * * *` | 每10分钟 |
| `0 * * * *` | 每小时整点 |
| `0 8 * * *` | 每天早上8点 |
| `0 8 * * 1-5` | 工作日早上8点 |
| `0 8 * * 0,6` | 周末早上8点 |

验证表达式: https://crontab.guru

### Cron 管理命令

```bash
# 列出所有定时任务
openclaw cron list

# 查看任务状态
openclaw cron status

# 立即执行某个任务
openclaw cron run <job-id>

# 编辑任务
openclaw cron edit <job-id>

# 删除任务
openclaw cron delete <job-id>

# 重启 Gateway 使配置生效
openclaw gateway restart
```

---

## 交付物格式

执行完成后，会在 `output_dir` 生成：

### ZIP 文件结构

```
delivery_{task_id}_{random}.zip
├── metadata.json      # 任务元数据
├── result.txt        # 任务执行报告
└── output/          # 执行产物目录
    └── artifacts.txt
```

### metadata.json

```json
{
  "task_id": "uuid",
  "title": "任务标题",
  "category": "coding",
  "bounty": "100.00",
  "status": "completed",
  "completed_at": "2026-03-25T10:00:00Z"
}
```
