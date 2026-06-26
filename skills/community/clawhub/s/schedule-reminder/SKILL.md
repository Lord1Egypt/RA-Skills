---
name: schedule-reminder
description: "双保险智能日程提醒系统。触发词: 提醒我、记得、别忘了、明天、后天、下午、上午、几点、会议、开会、截止、截止日期、日程、安排、计划。即使Gateway失效也能准时提醒。使用场景：(1) 用户说'提醒我XX'时创建提醒, (2) 主动从对话中捕捉日程信息, (3) 每日定时推送日程预览。支持微信、Telegram等多渠道。NOT for: 日历同步, 会议室预定, 项目管理。"
metadata:
  {
    "openclaw":
      {
        "emoji": "⏰",
        "requires": { "tools": ["cron", "message"] },
      },
  }
---

# 双保险智能日程提醒

**核心特性：即使 Gateway 失效，也能准时提醒**

## 快速开始

### 1. 安装

```bash
cd schedule-reminder
node scripts/install.mjs
```

### 2. 配置

编辑 `~/.openclaw/data/schedule-reminder-config.json`：

```json
{
  "primaryChannel": "openclaw-weixin",
  "backupEnabled": true,
  "userId": "你的微信ID或Telegram chatId",
  "accountId": "你的账号ID（可选）"
}
```

### 3. 创建提醒

```bash
node scripts/create-reminder.mjs "喝水" "该喝水了" "+30m"
```

时间格式：
- `+5m` - 5分钟后
- `+1h` - 1小时后  
- `2026-03-30T15:00:00+08:00` - ISO时间

## 双保险架构

### 主方案：OpenClaw Cron
- 依赖 Gateway，功能完整
- 支持复杂 cron 表达式
- 自动删除已执行任务

### 备用方案：系统级定时任务
- **不依赖 Gateway**
- 系统 crontab 每分钟检查
- 多层级 fallback：CLI → API → 文件记录
- 失败后自动重试（最多3次）

## 使用方式

### 方式1：命令行

```bash
# 创建提醒
node scripts/create-reminder.mjs "名称" "消息" "时间"

# 示例
node scripts/create-reminder.mjs "开会" "15分钟后开会" "+15m"
node scripts/create-reminder.mjs "提交报告" "今天截止" "2026-03-30T18:00:00+08:00"
```

### 方式2：对话中使用

当用户说：
- "提醒我5分钟后喝水"
- "明天下午3点开会"
- "帮我设个提醒"

自动调用 `create-reminder.mjs` 创建双保险提醒。

## 工作模式

### 模式 A：主动捕捉（对话中）

检测到用户提及**时间 + 事项**时，主动提议创建提醒：

```
用户: "明天下午3点要跟投资人开会"
助手: "收到。我注意到你明天下午3点有投资人会议，要我帮你设提醒吗？
  建议：明天 14:30 提前30分钟提醒
  直接说'好'我就帮你创建。"
```

### 模式 B：日程巡检

每日早间自动推送日程预览（需配置 cron）。

### 模式 C：显式请求

用户直接说"提醒我..."时立即创建。

## 配置选项

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| primaryChannel | string | openclaw-weixin | 主推送渠道 |
| backupEnabled | boolean | true | 启用备用方案 |
| userId | string | - | 用户ID（必填） |
| accountId | string | - | 账号ID（多账号时需要） |

**支持渠道：**
- `openclaw-weixin` - 微信
- `telegram` - Telegram
- `discord` - Discord

## 文件结构

```
schedule-reminder/
├── SKILL.md              # 本文件
├── package.json          # 包配置
├── config/
│   └── default.json      # 默认配置
└── scripts/
    ├── install.mjs       # 安装脚本
    ├── create-reminder.mjs   # 创建提醒
    └── reminder-backup.mjs   # 备用检查
```

## 数据存储

- **主存储**: OpenClaw cron 系统
- **备用存储**: `~/.openclaw/data/reminders.json`
- **配置**: `~/.openclaw/data/schedule-reminder-config.json`
- **日志**: `~/.openclaw/data/reminder-backup.log`

## 注意事项

1. 安装后必须配置 `userId`，否则无法发送提醒
2. 备用方案依赖系统 crontab，确保有权限
3. 时区默认使用 `Asia/Shanghai`
4. 一次性提醒执行后自动清理

## 故障排查

**提醒没收到？**
1. 检查配置：`cat ~/.openclaw/data/schedule-reminder-config.json`
2. 查看日志：`tail ~/.openclaw/data/reminder-backup.log`
3. 检查 crontab：`crontab -l | grep reminder`
4. 手动测试：`node scripts/reminder-backup.mjs`
