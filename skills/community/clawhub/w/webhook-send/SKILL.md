---
name: webhook-send
description: |
  向指定 webhook 地址发送消息。URL 从环境变量 WEBHOOK_SEND_URL 读取。
  仅支持 text、markdown 两种类型，支持 Markdown 富文本。
triggers:
  - webhook
  - 群组
  - 机器人
  - 通知
  - 消息推送
  - webhook-send
  - 群组消息
  - markdown消息
  - 文本消息
---

# Webhook 发送消息

向指定 webhook 地址发起 **HTTP POST**，发送文本或 Markdown 消息。仅支持 **text**、**markdown** 两种类型。

## 何时使用

- 需要向 webhook 地址发送消息
- 需构造 text / markdown 请求体（URL 从 **WEBHOOK_SEND_URL** 读取）
- 询问群组通知、webhook 格式时

## 约定与限制

| 项 | 说明 |
|----|------|
| URL | 环境变量 **WEBHOOK_SEND_URL**（示例：`https://xxx.com/api/v1/webhook/send?key=xxx`） |
| 方法 | `POST`，`Content-Type: application/json` |
| 频率 | ≤ 20 条/分钟 |
| 长度 | 单条 ≤ 5000 字符 |

## 消息类型

| msgtype | 说明 | 必填 |
|---------|------|------|
| `text` | 纯文本 | `text.content` |
| `markdown` | Markdown | `markdown.text`，支持标题/引用/加粗/颜色/列表/链接/图片等 |

## 请求体示例

**text**

```json
{ "msgtype": "text", "text": { "content": "消息内容" } }
```

**markdown**（换行：`\n\n` 或 `双空格+\n`）

```json
{ "msgtype": "markdown", "markdown": { "text": "## 标题\n\n内容" } }
```

更多示例见 [reference.md](reference.md)。组好 body 后对 webhook URL 发 POST 即可。
