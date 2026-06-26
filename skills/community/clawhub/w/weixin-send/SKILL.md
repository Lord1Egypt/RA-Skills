---
name: weixin-send
version: 1.1.0
description: |
  主动向微信 ClawBot 用户推送文本消息。作为 openclaw-weixin 插件 message 工具的兜底方案，仅在其不可用时使用。
author: 小老弟
category: messaging
tags:
  - weixin
  - wechat
  - message
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# weixin-send - 主动向微信 ClawBot 发送消息（兜底方案）

> ⚠️ **本 skill 是兜底方案，仅在 openclaw-weixin 插件原生能力不足时使用。**

## 使用优先级

| 优先级 | 方式 | 前提条件 | 适用场景 |
|--------|------|----------|----------|
| ✅ 首选 | `message(action=send, ...)` | tools.profile = `full`（含 `group:messaging`） | 当前会话 / 跨 agent 发消息/图片/文件 |
| ⚠️ 兜底 | `weixin-send` (本 skill) | 无限制 | message 工具不可用时（profile 不满足 / 非 agent 环境） |

### 什么时候用 weixin-send

只有当 openclaw-weixin 插件**确实无法完成**时才用本 skill：

- **后台脚本触发** — 从非 OpenClaw agent 的脚本/定时任务中推送（无 message 工具可用时）

> ✅ 已验证：跨 agent session（如飞书 session）中可以用 `message(action=send, channel=openclaw-weixin, target=用户ID@im.wechat, message="内容")` 直接发微信。
>
> ⚠️ 前提：tools.profile 需为 `full`（或包含 `group:messaging`），否则 message 工具不可用，此时回退到 weixin-send。

### 什么时候不该用

- ❌ 当前正在微信会话中对话 → 直接用 `message` 工具
- ❌ 能通过插件原生通道完成的操作 → 不要绕道走外部 API

## 背景

OpenClaw 的 `openclaw-weixin` 插件支持微信消息收发，但只在**用户主动发消息时才能回复**。无法从 cron 定时任务、其他 agent session、或后台脚本中主动向用户推送消息。

本 skill 通过直接调用微信 ilink API 绕过这一限制，实现**从任意 session/脚本主动向微信用户发消息**。

## 前置条件

| 条件 | 说明 |
|------|------|
| openclaw-weixin 通道 | 已通过 `openclaw channels login --channel openclaw-weixin` 登录 |
| Python | 3.8+（纯标准库，无第三方依赖） |
| context_token | 用户近期与 bot 有过对话（否则消息可能无法送达） |

## 快速开始

```bash
# 1. 列出可用账号
python3 send.py list

# 2. 发送消息
python3 send.py send "TARGET_USER_ID@im.wechat" "你好！这是一条主动推送的消息 🐾"
```

## 命令行用法

### 发送文本消息

```bash
# 自动选择账号
python3 send.py send "TARGET_USER_ID@im.wechat" "消息内容"

# 指定 bot 账号（多账号场景）
python3 send.py send "TARGET_USER_ID@im.wechat" "消息内容" --account "your-account-id"
```

### 列出已登录账号

```bash
python3 send.py list
# 输出示例：
#   your-account-id -> oXxx@im.wechat
```

## Python API

```python
from send import send_text, list_accounts

# 列出账号
accounts = list_accounts()
for a in accounts:
    print(f"{a['accountId']}: {a['userId']}")

# 发送消息
result = send_text(
    to_user="TARGET_USER_ID@im.wechat",
    text="你好！"
)

if result["ok"]:
    print(f"发送成功 (HTTP {result['status']})")
else:
    print(f"发送失败: {result.get('error')}")
```

## 在 OpenClaw Agent 中使用

### Cron 定时推送

```json
{
  "name": "daily-reminder",
  "schedule": { "kind": "cron", "expr": "0 9 * * *", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "运行命令发送提醒：python3 ~/.openclaw/workspace/skills/weixin-send/send.py send 'TARGET_USER_ID@im.wechat' '早安！新的一天开始了 🐾'"
  }
}
```

### 从 Agent Session 调用

Agent 在对话中可以直接 exec 调用：

```bash
python3 ~/.openclaw/workspace/skills/weixin-send/send.py send \
  "TARGET_USER_ID@im.wechat" "任务已完成 ✅"
```

## 返回值说明

```json
{
  "ok": true,
  "status": 200
}
```

| 字段 | 说明 |
|------|------|
| `ok` | 是否成功（HTTP 2xx） |
| `status` | HTTP 状态码 |
| `error` | 失败时的错误信息 |

## 工作原理

```
┌─────────────────┐     ┌──────────────────────┐     ┌──────────┐
│  Agent / Cron   │────▶│  send.py             │────▶│  用户微信 │
│  (任意 session)  │     │  ilink/bot/sendmessage│     │          │
└─────────────────┘     └──────────┬───────────┘     └──────────┘
                                   │
                          读取本地 token
                                   │
                    ┌──────────────▼──────────────┐
                    │  ~/.openclaw/openclaw-weixin │
                    │  /accounts/*.json            │
                    └─────────────────────────────┘
```

- 直接调用 `ilinkai.weixin.qq.com/ilink/bot/sendmessage` 接口
- token 从本地 `~/.openclaw/openclaw-weixin/accounts/` 自动读取
- 不经过 OpenClaw 通道框架，不触发 session 日志

## 能力边界

### ✅ 支持

- 文本消息（任意长度，UTF-8）

### ❌ 不支持

- **文件/图片/音频/视频** — 微信 ilink bot 平台限制，第三方 bot 无法通过 API 发送可下载的文件。消息能显示但客户端无法下载（显示"接收中断"或"不支持的消息"）。这是平台层面的限制，非代码问题。

## 注意事项

- **context_token 是关键** — 用户必须近期与 bot 对话过，否则服务端可能静默丢弃消息
- **返回 200 ≠ 确认送达** — 微信 ilink API 是 fire-and-forget 模式
- **token 存储在本地** — 隐私安全，不会被打包到 skill 中
- **单向推送** — 只发送文本，不接收回复（接收仍通过 openclaw-weixin 插件）

## 常见问题

### Q: 发送返回 200 但用户没收到？

检查 context_token：
```bash
cat ~/.openclaw/openclaw-weixin/accounts/*.context-tokens.json
```
如果目标用户没有 token 记录，需要该用户先在微信里给 bot 发一条消息。

### Q: 多个 bot 账号怎么选？

```bash
python3 send.py list  # 查看所有账号
python3 send.py send "TARGET@im.wechat" "msg" --account "specific-account-id"
```

### Q: 能发图片/文件吗？

**不能。** 微信 ilink bot 平台对第三方 bot 不开放文件下载能力。消息能发出但客户端无法下载。如需发送文件，可通过其他通道（如元宝）实现。
