---
name: weixin-cron-push
description: "通过 OpenClaw Cron 定时任务向微信用户主动推送消息（天气、提醒、新闻摘要等）。当用户需要：设置定时提醒、每日推送、定时通知、微信主动发消息、cron 推送到微信时触发。支持一次性（at）和循环（cron/every）任务，通过 sessionKey 路由到指定微信用户，AI 对话模式下自动获取 sessionKey。"
---

# 微信 Cron 推送

通过 Cron 定时任务实现微信主动推送。

## 原理

```
Cron agentTurn → 独立会话 → --announce + --channel openclaw-weixin → 微信投递到用户手机
```

关键：
- `--session-key` 指定用户的微信会话桶（格式：`agent:main:openclaw-weixin:direct:<userId>@im.wechat`）
- `--announce --channel openclaw-weixin` 确保回复通过微信投递
- `--message`（agentTurn）而非 `--system-event`（systemEvent 走 main 桶，无法投递）

## 前提

- 微信插件 `openclaw-weixin` 已安装启用
- 至少一个微信账号已扫码登录
- Gateway 正在运行
- 用户通过微信给机器人发过至少一条消息（建立 sessionKey）

## 创建任务

### 一次性提醒（at）

```bash
openclaw cron add \
  --name "提醒标题" \
  --at "2026-04-29T10:00:00Z" \
  --message "请告诉用户：这是提醒内容" \
  --session-key "agent:main:openclaw-weixin:direct:<userId>@im.wechat" \
  --announce \
  --channel openclaw-weixin \
  --delete-after-run
```

### 每日定时推送（cron 表达式）

```bash
openclaw cron add \
  --name "每日天气" \
  --cron "0 8 * * *" \
  --tz "Asia/Shanghai" \
  --message "请查询今天天气并发送给用户。" \
  --session-key "agent:main:openclaw-weixin:direct:<userId>@im.wechat" \
  --announce \
  --channel openclaw-weixin
```

### 循环间隔（every）

```bash
openclaw cron add \
  --name "每小时间隔" \
  --every "1h" \
  --message "请执行 XXX 检查并告知用户结果。" \
  --session-key "agent:main:openclaw-weixin:direct:<userId>@im.wechat" \
  --announce \
  --channel openclaw-weixin
```

### AI 对话方式

用户直接说"明天早上8点提醒我开会"，AI 自动创建任务。AI 需从当前会话获取 sessionKey 并使用上述参数。

## 获取 sessionKey

```bash
# 方法1：从会话列表查找（找含 openclaw-weixin 的 key）
openclaw sessions --json --all-agents | grep openclaw-weixin

# 方法2：从会话文件查找（自动适配 macOS / Linux）
python3 -c "
import json, pathlib
sessions_file = pathlib.Path.home() / '.openclaw' / 'agents' / 'main' / 'sessions' / 'sessions.json'
with open(sessions_file) as f:
    for k in json.load(f):
        if 'openclaw-weixin' in k and 'direct' in k:
            print(k)
"

# 方法3：从微信账号配置获取 userId，拼接为：
# agent:main:openclaw-weixin:direct:<userId>@im.wechat
# userId 在 ~/.openclaw/openclaw-weixin/accounts/*.json 中
```

## 关键 CLI 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--message <文本>` | ✅ | agentTurn 消息内容，AI 处理后回复用户 |
| `--session-key <key>` | ✅ | 微信会话桶 key（决定路由到哪个用户） |
| `--announce` | ✅ | 启用投递（否则回复不发送） |
| `--channel openclaw-weixin` | ✅ | 指定通过微信渠道投递 |
| `--at <ISO时间>` | 调度 | 一次性触发 |
| `--cron <表达式>` | 调度 | Cron 表达式循环 |
| `--every <间隔>` | 调度 | 固定间隔循环（如 10m, 1h） |
| `--tz <时区>` | 否 | 时区（如 Asia/Shanghai） |
| `--delete-after-run` | 否 | 触发后自动删除 |
| `--name <名称>` | 否 | 任务名称 |
| `--account <id>` | 否 | 多账号时指定微信账号 |

## ⚠️ 重要：system-event vs message

| 方式 | 投递 | 说明 |
|------|------|------|
| `--system-event` + `--session main` | ❌ 不可靠 | 注入 main 桶，没有 deliveryContext，回复无法投递 |
| `--message` + `--session-key` + `--announce` | ✅ 可靠 | 独立会话 + 明确投递渠道，消息必定到达微信 |

**必须用 `--message` 方式，不要用 `--system-event`。**

## 管理命令

```bash
openclaw cron list                    # 查看活跃任务
openclaw cron list --all              # 含已禁用/残留任务
openclaw cron delete <ID>             # 删除任务
openclaw cron run <ID>                # 立即触发
```

## 多账号场景

每个微信用户有独立 sessionKey：

1. 扫码登录：`openclaw channels login --channel openclaw-weixin`
2. 该微信号给机器人发一条消息（建立会话桶）
3. 查找该用户的 sessionKey
4. 创建 cron 任务时用对应 sessionKey

多账号时用 `--account` 指定微信账号：

```bash
openclaw cron add \
  --name "每日天气" \
  --cron "0 8 * * *" \
  --tz "Asia/Shanghai" \
  --message "请查询今天天气并发送给用户。" \
  --session-key "agent:main:openclaw-weixin:direct:<userId>@im.wechat" \
  --announce \
  --channel openclaw-weixin \
  --account <account-id>
```

多账号隔离建议：
```bash
openclaw config set session.dmScope per-account-channel-peer
```

## 常见问题

- **延迟**：正常几秒到1分钟，超过5分钟检查 gateway 状态
- **只发一条**：不需要重复发送
- **图片/文件**：在 message 中指示 AI 调用图片工具，AI 自动处理
- **sessionKey 找不到**：说明目标用户还没通过微信给机器人发过消息，需要先发一条建立绑定
- **sessionKey 错误**：任务会创建成功但消息无法投递，不会报错。请确认 `userId` 正确
- **创建任务后没收到消息**：检查 gateway 是否运行、微信是否在线、sessionKey 是否匹配该微信用户
