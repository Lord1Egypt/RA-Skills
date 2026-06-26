# weixin-send

> 🐾 OpenClaw Skill — 主动向微信 ClawBot 用户推送文本消息

[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.com)
[![Python](https://img.shields.io/badge/Python-3.8+-green)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

## 这是什么？

`weixin-send` 是一个 [OpenClaw](https://github.com/openclaw/openclaw) 技能，让你的 AI Agent 可以**主动**向微信用户发消息，而不是只能被动回复。

> ⚠️ **本 skill 是兜底方案。** 优先使用 `openclaw-weixin` 插件的 `message` 工具，仅在其不可用时才用本 skill。

### 使用优先级

| 优先级 | 方式 | 前提条件 | 适用场景 |
|--------|------|----------|----------|
| ✅ 首选 | `message(action=send, ...)` | tools.profile = `full` | 跨 agent 发消息/图片/文件到微信 |
| ⚠️ 兜底 | `weixin-send` (本 skill) | 无限制 | message 工具不可用时 |

### 适用场景

- 📜 **非 agent 脚本** — 外部脚本/定时任务没有 message 工具时，通过 send.py 推送微信消息
- ⚠️ **profile 不满足** — 当 tools.profile 非 `full` 且无 `group:messaging` 时的备选方案

### 为什么需要它？

大部分场景下，直接用 `message(action=send, channel=openclaw-weixin, ...)` 即可发微信（支持文本、图片、文件、视频）。

但当 `message` 工具不可用时（如非 agent 环境、profile 限制），`weixin-send` 提供一个纯 Python 的文本推送方案。

## 快速开始

### 1. 前置条件

确保已安装并登录 `openclaw-weixin` 通道：

```bash
openclaw channels login --channel openclaw-weixin
```

### 2. 安装技能

```bash
# 从 ClawHub 安装
openclaw skills install weixin-send

# 或手动克隆到 skills 目录
git clone <repo-url> ~/.openclaw/workspace/skills/weixin-send
```

### 3. 发送第一条消息

```bash
# 查看已登录的账号
python3 ~/.openclaw/workspace/skills/weixin-send/send.py list

# 发送测试消息（替换为实际的 user_id）
python3 ~/.openclaw/workspace/skills/weixin-send/send.py send \
  "YOUR_USER_ID@im.wechat" "你好！第一条主动推送 🐾"
```

## 使用方式

### 命令行

```bash
# 发送消息
python3 send.py send "TARGET_USER_ID@im.wechat" "消息内容"

# 指定 bot 账号
python3 send.py send "TARGET@im.wechat" "消息" --account "account-id"

# 列出账号
python3 send.py list
```

### Python API

```python
from send import send_text, list_accounts

result = send_text("TARGET@im.wechat", "你好！")
# result: {"ok": true, "status": 200}
```

### OpenClaw Agent / Cron

在 agent 对话中直接 exec：

```bash
python3 ~/.openclaw/workspace/skills/weixin-send/send.py send \
  "TARGET@im.wechat" "任务完成 ✅"
```

## 工作原理

```
Agent / Cron / 脚本
        │
        ▼
   send.py ──── 读取本地 bot token + context_token
        │
        ▼
   POST ilinkai.weixin.qq.com/ilink/bot/sendmessage
        │
        ▼
    用户微信收到文本消息
```

- 直接调用微信 ilink API，不经过 OpenClaw 通道框架
- token 自动从 `~/.openclaw/openclaw-weixin/accounts/` 读取
- 零配置，零依赖（Python 标准库即可）

## 前置要求

| 项目 | 要求 |
|------|------|
| OpenClaw | 已安装并运行 |
| openclaw-weixin | 已登录（`openclaw channels login --channel openclaw-weixin`） |
| Python | 3.8+（标准库） |
| context_token | 目标用户近期与 bot 对话过 |

## 能力边界

| 类型 | 支持 |
|------|------|
| 文本消息 | ✅ |
| 文件/图片/音频/视频 | ❌ 微信 ilink 平台限制，第三方 bot 无法发送可下载的文件 |

## 隐私安全

- ✅ token 存储在本地 `~/.openclaw/openclaw-weixin/accounts/`，不打包到 skill
- ✅ 无硬编码密钥或用户 ID
- ✅ `.gitignore` 排除所有 json/env/key 文件
- ✅ 纯本地调用，不经过第三方服务

## 许可证

[MIT](LICENSE)
