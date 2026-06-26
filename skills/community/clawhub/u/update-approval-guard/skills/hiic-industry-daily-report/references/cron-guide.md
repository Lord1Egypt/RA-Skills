# 定时任务配置指南

本文档说明如何使用 OpenClaw 的 cron 功能设置产业简报的定时推送。

## 快速开始

### 1. 每日推送（最常用）

每天早上 9:00 生成并推送简报：

```bash
openclaw cron add "0 9 * * *" "node ~/.openclaw/workspace/skills/industry-news-aggregator/scripts/generate-report.mjs --push"
```

### 2. 每周推送

每周一早上 9:00：

```bash
openclaw cron add "0 9 * * 1" "node ~/.openclaw/workspace/skills/industry-news-aggregator/scripts/generate-report.mjs --push --days 7"
```

### 3. 自定义时间

每天下午 2:30：

```bash
openclaw cron add "30 14 * * *" "node ~/.openclaw/workspace/skills/industry-news-aggregator/scripts/generate-report.mjs --push"
```

## Cron 表达式说明

格式：`分钟 小时 日 月 星期`

常用示例：

| 表达式 | 说明 |
|--------|------|
| `0 9 * * *` | 每天 9:00 |
| `0 9,18 * * *` | 每天 9:00 和 18:00 |
| `0 9 * * 1-5` | 周一到周五 9:00 |
| `0 9 * * 1` | 每周一 9:00 |
| `0 9 1 * *` | 每月 1 号 9:00 |
| `*/30 * * * *` | 每 30 分钟 |

## 管理定时任务

### 查看所有任务

```bash
openclaw cron list
```

### 删除任务

```bash
# 先列出任务获取 ID
openclaw cron list

# 删除指定任务
openclaw cron remove <task-id>
```

### 暂停/恢复任务

```bash
openclaw cron pause <task-id>
openclaw cron resume <task-id>
```

## 高级配置

### 1. 指定配置文件

```bash
openclaw cron add "0 9 * * *" \
  "node ~/.openclaw/workspace/skills/industry-news-aggregator/scripts/generate-report.mjs --config /path/to/my-config.json --push"
```

### 2. 保存到文件

```bash
openclaw cron add "0 9 * * *" \
  "node ~/.openclaw/workspace/skills/industry-news-aggregator/scripts/generate-report.mjs --output ~/reports/daily-$(date +\\%Y\\%m\\%d).md"
```

### 3. 多个简报

为不同的产业配置创建多个定时任务：

```bash
# AI 简报 - 每天 9:00
openclaw cron add "0 9 * * *" \
  "node ~/.openclaw/workspace/skills/industry-news-aggregator/scripts/generate-report.mjs --config ~/.openclaw/workspace/ai-news-config.json --push"

# 新能源简报 - 每天 10:00
openclaw cron add "0 10 * * *" \
  "node ~/.openclaw/workspace/skills/industry-news-aggregator/scripts/generate-report.mjs --config ~/.openclaw/workspace/ev-news-config.json --push"
```

## 配置文件中的定时设置

在 `config.json` 中也可以配置定时：

```json
{
  "schedule": {
    "enabled": true,
    "frequency": "daily",
    "time": "09:00",
    "timezone": "Asia/Shanghai",
    "skipWeekends": true,
    "skipHolidays": true
  }
}
```

**注意**：配置文件中的 `schedule` 设置目前需要配合外部调度器（如 cron）使用。未来的版本将支持自动注册。

## 推送渠道配置

### 飞书

1. 获取群组 chat_id
2. 在配置文件中添加：

```json
{
  "push": {
    "channels": [
      {
        "type": "feishu",
        "enabled": true,
        "chatId": "oc_xxxxxxxxxxxxx"
      }
    ]
  }
}
```

### 企业微信

```json
{
  "push": {
    "channels": [
      {
        "type": "wecom",
        "enabled": true,
        "chatId": "xxxxxxxx"
      }
    ]
  }
}
```

### Telegram

```json
{
  "push": {
    "channels": [
      {
        "type": "telegram",
        "enabled": true,
        "chatId": "-1001234567890"
      }
    ]
  }
}
```

## 故障排查

### 任务没有执行

1. 检查 OpenClaw 是否在运行：`openclaw status`
2. 查看任务日志：`openclaw cron logs <task-id>`
3. 手动测试命令是否正常

### 搜索失败

1. 检查 API Key 是否配置：`env | grep -E "(TAVILY|BRAVE)"`
2. 测试搜索脚本：`node scripts/search-aggregator.mjs "测试" --verbose`

### 推送失败

1. 确认目标渠道已配置
2. 检查 chat_id 是否正确
3. 查看 OpenClaw 日志

## 最佳实践

1. **合理设置频率**：避免过于频繁的推送，建议每日或每周
2. **精确关键词**：使用具体的关键词，减少噪音
3. **测试先行**：正式部署前先手动运行测试
4. **监控配额**：关注 Tavily 和 Brave 的 API 使用量
5. **备选方案**：保存生成的简报到文件，便于历史查询
