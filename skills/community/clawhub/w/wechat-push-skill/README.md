# 微信主动推送 Skill / WeChat Proactive Push Skill

> 让本地 Agent 主动推送消息到用户手机微信 —— 绕过 24 小时客服窗口限制
> Let your local Agent proactively push messages to a user's WeChat — bypass the 24h customer service window limit.

---

## 中文

### 这是什么

一个工程化的微信主动推送方案。装上后，从任何目录运行一行命令就能给用户发微信。

**核心承诺**：`wechat-push "消息"` → 用户手机微信收到。

### 解决什么问题

微信官方 API 的"24 小时客服窗口"限制：用户必须**先发消息**给公众号/bot，bot 才能在 24 小时内回复。**超过 24 小时不能主动推**——这对"每日早报""异常告警""任务完成通知"等场景是致命的。

这个 skill 通过调用 **OpenClaw 微信插件**的内部通道绕开这个限制。

### 安装先决条件

使用本 skill 前，需要先满足两个条件：

- 已经在使用 **OpenClaw**，并且本机可以正常运行 `openclaw` CLI。
- 已经有通畅的 **OpenClaw 微信渠道**：微信插件已完成扫码绑定，且能通过 OpenClaw 微信插件正常收发消息。

### 装上

```bash
# 1. 确认已满足上面的安装先决条件
#    参考: https://docs.openclaw.ai

# 2. 装本 skill
bash ~/.openclaw/skills/wechat-push-skill/install.sh

# 安装过程会引导你：
#   - 检查 openclaw CLI
#   - 探测活跃 bot 账号
#   - 配置你的微信 openid
#   - 跑一次 verify 验证
```

### 用法

```bash
# 推一条消息
wechat-push "你好"

# 推给指定 openid
wechat-push --to oXXXXXXXXXXXXXXXXX@im.wechat "你好"

# 静默推送（不响通知，用于探活）
wechat-push --silent "probe test"

# 预演：只打印将使用的 openid/account，不发送
wechat-push --dry-run "你好"

# 链路 5 跳自检
wechat-push-verify

# 故障排查
wechat-push-doctor
```

**成功标准**：安装成功不是脚本 exit 0，而是 `wechat-push "test"` 后用户手机微信实际收到消息。

### 账号选择策略

默认只需要配置 `openid`，不要写死 `account`。每次发送前，`wechat-push` 会按当前 `openid` 动态选择 bot account：

- 优先选择 `context_tokens` 里包含该 `openid` 的 bot。
- 如果多个 bot 匹配，选择最近仍在 sync 的 bot。
- 只有自动探测反复选错时，才在配置文件里手动写 `account=...`。

### 自动化

接 cron 让推送自动化：

```bash
# 每 15 分钟 silent 探活，链路断了主动告警
openclaw cron add ilink-probe-15min \
  --every "15m" --session main \
  --system-event "触发 ilink 探活"
```

### 故障排查

跑 `wechat-push-doctor` 看 6 种常见故障 + 修法。详见 [`references/troubleshooting.md`](references/troubleshooting.md)。

### 局限

- ✅ 推消息（单条文本）= 唯一核心能力
- ❌ 不支持多人 / 群发（每个用户单独 install）
- ❌ 不支持模板消息（卡片 / 图文）
- ❌ 不主动生成早报/晚报内容（用户自己写生成逻辑）

### 协议笔记

详见 [`references/protocol-notes.md`](references/protocol-notes.md)。

---

## English

### What is this

An engineering solution for **proactive WeChat push**. Once installed, push a message from anywhere with one command.

**Core promise**: `wechat-push "message"` → user receives it on their phone WeChat.

### What problem does it solve

WeChat's official "24-hour customer service window" rule: a user must **first send a message** to the bot, and the bot can only reply within 24 hours. **No proactive push beyond 24h** — fatal for use cases like daily briefings, anomaly alerts, and task completion notifications.

This skill bypasses the limit by going through the **OpenClaw WeChat plugin's internal channel**.

### Prerequisites

Before installing this skill, make sure both prerequisites are met:

- You are already using **OpenClaw**, and the `openclaw` CLI works on this machine.
- You already have a working **OpenClaw WeChat channel**: the WeChat plugin has completed QR-code binding and can send/receive messages through OpenClaw.

### Install

```bash
# 1. Make sure the prerequisites above are satisfied
#    See: https://docs.openclaw.ai

# 2. Install this skill
bash ~/.openclaw/skills/wechat-push-skill/install.sh

# Installer will:
#   - Check openclaw CLI
#   - Detect active bot account
#   - Configure your WeChat openid
#   - Run verify to validate
```

### Usage

```bash
# Push a message
wechat-push "Hello"

# Push to a specific openid
wechat-push --to oXXXXXXXXXXXXXXXXX@im.wechat "Hello"

# Silent push (no notification, for health probes)
wechat-push --silent "probe test"

# Dry run: print openid/account without sending
wechat-push --dry-run "Hello"

# 5-hop link self-check
wechat-push-verify

# Troubleshoot
wechat-push-doctor
```

**Success criterion**: installation is only truly verified when `wechat-push "test"` is received on the user's phone WeChat, not merely when the script exits 0.

### Account Selection

By default, only configure `openid`; do not pin `account`. Before each send, `wechat-push` dynamically selects the bot account for the current `openid`:

- Prefer a bot whose `context_tokens` contains the target `openid`.
- If multiple bots match, choose the one with the most recent sync.
- Only set `account=...` manually when automatic detection repeatedly selects the wrong bot.

### Automation

```bash
# Probe every 15 minutes, alert on link down
openclaw cron add ilink-probe-15min \
  --every "15m" --session main \
  --system-event "Trigger ilink probe"
```

### Troubleshooting

Run `wechat-push-doctor` to see 6 common failure modes + fixes. See [`references/troubleshooting.md`](references/troubleshooting.md).

### Limitations

- ✅ Push message (single text) = the only core capability
- ❌ No multi-user / broadcast (each user installs separately)
- ❌ No template messages (card / image-text)
- ❌ Doesn't generate daily/evening briefing content (you write that)

### Protocol Notes

See [`references/protocol-notes.md`](references/protocol-notes.md).

---

## License

MIT — use freely, attribution appreciated.

## Credits

Built on the OpenClaw WeChat plugin's internal `message send` channel. Inspired by real failure modes encountered in 2026-06.
