---
name: wukong-invite-monitor
description: 钉钉悟空邀请码监控，零 token 消耗。自动监控邀请码图片版本变化，支持本地 Tesseract OCR 识别和心跳推送通知。
---

# 悟空邀请码监控 - 轻量版

## 🚀 快速开始

```bash
cd ~/.openclaw/workspace/skills/wukong-invite-monitor/scripts

# 1. 安装依赖
./install-dependencies.sh

# 2. 初始化
python3 monitor_lite.py init

# 3. 测试
python3 monitor_lite.py check

# 4. 设置定时监控（可选）
./setup-cron.sh 5
```

## 📋 命令参考

| 命令 | 说明 |
|------|------|
| `init` | 初始化状态 |
| `check` | 执行一次检查 |
| `status` | 显示当前状态 |
| `scan` | 扫描所有可用版本 |
| `help` | 显示帮助 |

## 🔔 心跳推送通知

配置心跳检查，自动推送新邀请码通知：

```bash
# 添加心跳检查任务
*/5 * * * * python3 heartbeat-check.py >> /tmp/wukong-heartbeat.log 2>&1
```

**特点：**
- ✅ 每 5 分钟检查一次
- ✅ 只在官方时间段工作（9-12 点、14-18 点）
- ✅ 发现新内容才推送
- ✅ 避免重复通知

## 📖 完整文档

- [README.md](README.md) - 完整使用指南
- [QUICKSTART.md](QUICKSTART.md) - 60 秒快速开始
- [LOCAL-OCR.md](LOCAL-OCR.md) - OCR 配置详解
- [HEARTBEAT.md](HEARTBEAT.md) - 心跳推送配置
