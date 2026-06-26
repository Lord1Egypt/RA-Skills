# weixin-cron-push

OpenClaw Skill — 通过 Cron 定时任务向微信用户主动推送消息。

## 功能

- 一次性提醒（`at`）、每日定时推送（`cron`）、固定间隔循环（`every`）
- 精准路由：通过 `--session-key` 定位到具体微信用户
- 支持多微信账号隔离
- 可通过 CLI 或 AI 对话创建任务

## 原理

```
Cron agentTurn → 独立会话 → --announce + --channel openclaw-weixin → 微信投递到用户手机
```

- `--session-key` 指定用户的微信会话桶
- `--announce --channel openclaw-weixin` 确保回复通过微信投递
- `--message`（agentTurn）而非 `--system-event`

## 前提

- 已安装并启用 `openclaw-weixin` 插件
- 至少一个微信账号已扫码登录
- Gateway 正在运行
- 目标用户通过微信给机器人发过至少一条消息（建立 sessionKey）

## 安装

将本仓库作为 skill 添加到 OpenClaw：

```bash
openclaw skill add https://github.com/gausshj/openclaw-weixin-cron-push
```

## 使用示例

```bash
# 一次性提醒
openclaw cron add \
  --name "开会提醒" \
  --at "2026-04-30T09:00:00+08:00" \
  --message "请告诉用户：10点有产品评审会议" \
  --session-key "agent:main:openclaw-weixin:direct:<userId>@im.wechat" \
  --announce \
  --channel openclaw-weixin \
  --delete-after-run

# 每日天气推送
openclaw cron add \
  --name "每日天气" \
  --cron "0 8 * * *" \
  --tz "Asia/Shanghai" \
  --message "请查询今天天气并发送给用户。" \
  --session-key "agent:main:openclaw-weixin:direct:<userId>@im.wechat" \
  --announce \
  --channel openclaw-weixin
```

也可以直接对 AI 说"明天早上8点提醒我开会"，自动创建任务。

## 获取 sessionKey

```bash
# 从会话列表查找
openclaw sessions --json --all-agents | grep openclaw-weixin

# 或从微信账号配置获取 userId，拼接为：
# agent:main:openclaw-weixin:direct:<userId>@im.wechat
# userId 在 ~/.openclaw/openclaw-weixin/accounts/*.json 中
```

## ⚠️ 重要

必须用 `--message` + `--session-key` + `--announce` 方式，**不要用 `--system-event`**。
`--system-event` 走 main 桶，没有 deliveryContext，回复无法投递到微信。

## 文件说明

| 文件 | 说明 |
|------|------|
| `SKILL.md` | Skill 定义文件，包含触发条件和使用文档 |
| `references/weixin-api.md` | 微信 API 协议细节 |
| `LICENSE` | MIT License |

## License

MIT
