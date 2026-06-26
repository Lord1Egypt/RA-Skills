---
name: qqbot-time-reminder
description: 创建每分钟发送当前时间的QQ定时提醒任务。用于：(1) 用户要求每分钟报时 (2) 用户想要定期收到时间提醒 (3) 测试定时任务功能
---

# QQ 每分钟时间提醒

创建定时任务，每分钟向QQ用户发送当前时间。

## 使用方式

用户说"每分钟提醒时间"、"每小时报时"等时，使用此Skill。

## 创建步骤

1. **获取用户openid**：从用户发送的消息中提取，或直接询问用户
2. **执行cron命令**：

```bash
openclaw cron add \
  --name "每分钟时间提醒" \
  --cron "* * * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --wake now \
  --message "[直接输出] 当前时间：" \
  --deliver \
  --channel qqbot \
  --to "{用户openid}"
```

3. **返回结果**：告知用户任务ID和取消方法

## 取消任务

用户说"取消时间提醒"时：

```bash
openclaw cron rm <任务ID>
```

或先列出任务再删除：

```bash
openclaw cron list
openclaw cron rm <任务ID>
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `--cron "* * * * *"` | 每分钟执行 |
| `--tz "Asia/Shanghai"` | 使用上海时区 |
| `--session isolated` | 隔离会话执行 |
| `--deliver` | 启用消息投递 |
| `--channel qqbot` | QQ机器人渠道 |
| `--to` | 用户openid |