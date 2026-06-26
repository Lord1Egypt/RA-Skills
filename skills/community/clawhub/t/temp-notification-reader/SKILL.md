---
name: macos-notification-reader
description: "读取 macOS 通知中心，导出到 memory/computer_io/notification/ 目录。让 OpenClaw 了解你的工作动态。"
---

# macOS Notification Reader

> 让 OpenClaw 读取你的 macOS 通知，自动生成每日工作摘要

> Read your macOS notifications and generate daily work summaries for OpenClaw

**这是一个为 OpenClaw 打造的技能（Skill），可以读取 macOS 通知中心的内容，帮助 AI 助手更好地了解你的工作动态。**

---

## 🎯 这是什么？ / What is this?

这个工具会把你的 macOS 通知导出到 OpenClaw 的 memory 目录，让 OpenClaw 能够：
- 📬 知道谁在找你（Teams、Outlook、WeChat...）
- 📅 了解你的日程提醒
- ✅ 提取待办事项（会议、审批、deadline...）
- 🧠 记住你最近在忙什么

---

## 📁 输出文件结构 / Output File Structure

```
memory/YYYY-MM-DD/
└── computer_io/
    └── notification/
        ├── YYYYMMDD-HHMMSS.md          # 原始通知导出
        └── work-summary-YYYYMMDD-HHMMSS.md  # 工作摘要（推荐）
```

---

## 🚀 安装 / Installation

### 前置要求
- macOS 系统
- Python 3.8+ (`python3 --version` 检查)
- OpenClaw 已安装并运行

### 步骤 1：放入 OpenClaw Skills 目录

```bash
# 克隆项目
git clone https://github.com/gift-is-coding/macos-notification-reader.git

# 复制到 OpenClaw skills 目录
cp -r macos-notification-reader ~/.openclaw/workspace/skills/

# 给脚本执行权限
chmod +x ~/.openclaw/workspace/skills/macos-notification-reader/scripts/*.sh
```

### 步骤 2：首次运行授权

```bash
~/.openclaw/workspace/skills/macos-notification-reader/scripts/export-notification.sh
```

首次运行时，macOS 会弹窗请求「通知访问权限」，点击**允许**。

---

## ⚙️ 配置定时任务 / Configure Cron Job

### 方法一：通过 OpenClaw 配置（推荐）

编辑 `~/.openclaw/cron/jobs.json`，添加：

```json
{
  "name": "Notification Reader",
  "schedule": "*/30 * * * *",
  "command": "~/.openclaw/workspace/skills/macos-notification-reader/scripts/export-notification.sh",
  "timezone": "Asia/Shanghai"
}
```

这会让 OpenClaw **每 30 分钟**自动抓取一次通知。

### 方法二：手动添加 crontab

```bash
crontab -e
```

添加：

```cron
*/30 * * * * ~/.openclaw/workspace/skills/macos-notification-reader/scripts/export-notification.sh >> ~/.openclaw/logs/notification.log 2>&1
```

---

## 💼 使用方式 / Usage

### 导出所有通知

```bash
~/.openclaw/workspace/skills/macos-notification-reader/scripts/export-notification.sh
```

### 工作摘要模式（推荐）

只提取工作相关通知（Teams/Outlook/WeChat）：

```bash
~/.openclaw/workspace/skills/macos-notification-reader/scripts/work-summary.sh
```

### 自定义时间范围

```bash
# 只看过去 1 小时的通知
NOTIF_LOOKBACK_MINUTES=60 ~/.openclaw/workspace/skills/macos-notification-reader/scripts/export-notification.sh

# 工作摘要只看过去 2 小时
WORK_LOOKBACK_MINUTES=120 ~/.openclaw/workspace/skills/macos-notification-reader/scripts/work-summary.sh
```

---

## 🔐 隐私 / Privacy

- ✅ 数据保存在本地（OpenClaw memory 目录），不上传任何服务器
- ✅ 只读取通知标题和内容，不读取附件
- ✅ 支持一键清理：`rm -rf ~/.openclaw/workspace/memory/*/computer_io/notification/`

---

## 🛠️ 故障排查 / Troubleshooting

### 显示 0 条通知？

1. 检查权限是否授权：
   ```bash
   # 打开系统设置 / System Settings
   open "x-apple.systempreferences:com.apple.preference.security?Privacy_Notifications"
   ```

2. 快速调试：
   ```bash
   python3 ~/.openclaw/workspace/skills/macos-notification-reader/scripts/read_notifications.py --minutes 5 --output /tmp/debug.txt
   cat /tmp/debug.txt
   ```

### 权限被拒绝？

```bash
chmod +x ~/.openclaw/workspace/skills/macos-notification-reader/scripts/*.sh
```

---

## 📞 支持 / Support

- 问题反馈：https://github.com/gift-is-coding/macos-notification-reader/issues
- 了解更多 OpenClaw：https://docs.openclaw.ai

---

**Made with ❤️ for OpenClaw**
