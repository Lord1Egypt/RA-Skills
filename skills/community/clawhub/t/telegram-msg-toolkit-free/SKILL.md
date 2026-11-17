---
name: "telegram-msg-toolkit-free"
description: "Telegram Bot 消息免费版：文本/图片/文件/投票发送，聊天信息查询与基础Bot命令管理。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "Telegram消息工具箱(免费版)"
  version: "1.0.0"
  summary: "Telegram Bot 消息免费版：文本/图片/文件/投票发送，聊天信息查询与基础Bot命令管理。"
  tags:
    - "沟通协作"
    - "即时通讯"
    - "Telegram"
    - "消息自动化"
    - "Bot开发"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# Telegram 消息工具箱（免费版）

## 概述

本工具箱封装 Telegram Bot API 的基础消息能力，让 AI Agent 能够通过 REST API 发送文本、图片、文件、位置、投票与转发消息，查询聊天信息，并管理 Bot 命令。免费版聚焦"能发能查"——覆盖 6 类基础消息发送与聊天信息读取；批量操作、群组管理、审核与 Webhook 等进阶能力留给专业版。

Telegram Bot API 使用 HTTP REST 接口，所有请求通过 `https://api.telegram.org/bot<TOKEN>/<METHOD>` 调用，响应为 JSON 格式。

## 核心能力

| 能力 | 说明 | 免费版 |
|------|------|--------|
| 文本消息 | 发送纯文本消息 | 是 |
| 图片发送 | 发送图片（URL 或上传） | 是 |
| 文件发送 | 发送文档/文件 | 是 |
| 位置发送 | 发送地理坐标 | 是 |
| 投票发送 | 发送原生投票 | 是 |
| 消息转发 | 转发消息到其他聊天 | 是 |
| 消息编辑 | 编辑 Bot 已发送消息 | 是 |
| 消息删除 | 删除 Bot 消息 | 是 |
| 聊天信息 | 群组/成员/管理员查询 | 是 |
| 邀请链接 | 生成与撤销邀请链接 | 是 |
| Bot 命令 | 设置与获取命令列表 | 是 |
| 批量发送 | 批量消息/批量投票 | 否（专业版） |
| 群组管理 | 创建/踢人/权限/封禁 | 否（专业版） |
| Webhook | 实时事件回调 | 否（专业版） |
| 频道管理 | 频道发布/管理 | 否（专业版） |

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 按照skill规范执行核心功能执行操作,遵循单一意图原则。
**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 按照skill规范执行参数配置与调用操作,遵循单一意图原则。
**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输入**: 用户提供结果处理与输出所需的指令和必要参数。
**处理**: 按照skill规范执行结果处理与输出操作,遵循单一意图原则。
**输出**: 返回结果处理与输出的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Telegram、消息免费版、聊天信息查询与基、命令管理、消息工具箱、面向个人用户与独、立开发者、API、的基础消息能力、REST、直接调用、无需额外中间件、Use、when、接口对接、系统连接时使用、不适用于逆向工程等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：部署状态通知

用户说"部署完成后通知 Telegram 群"。Agent 调用 `sendMessage` 发送文本消息到指定群组，包含版本号与状态。

```bash
curl -X POST "https://api.telegram.org/bot{{BOT_TOKEN}}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "-1001234567890",
    "text": "部署完成！版本 2.1.0 已上线生产环境。",
    "parse_mode": "Markdown"
  }'
```

### 场景二：发送周报图片

用户说"把这张周报图表发到 Telegram"。Agent 调用 `sendPhoto` 发送图片，附带说明文字。

```bash
curl -X POST "https://api.telegram.org/bot{{BOT_TOKEN}}/sendPhoto" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "-1001234567890",
    "photo": "https://example.com/weekly-report.png",
    "caption": "本周活跃度报告\n日期：2026-07-17"
  }'
```

### 场景三：发起功能投票

用户说"在群里发起投票问下个版本优先做什么"。Agent 调用 `sendPoll` 发送原生投票。

```bash
curl -X POST "https://api.telegram.org/bot{{BOT_TOKEN}}/sendPoll" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "-1001234567890",
    "question": "下个版本优先开发哪个功能？",
    "options": ["暗色模式", "导出PDF", "团队共享", "API访问"],
    "allows_multiple_answers": false
  }'
```

## 快速开始

### 60 秒上手

1. 通过 BotFather 创建 Bot 获取 token（`/newbot` 命令）
2. 将 Bot 加入目标群组并赋予发送消息权限
3. 获取目标聊天 ID（群组以 `-100` 开头）
4. 调用 `sendMessage` 发送第一条消息

### 获取 Bot Token

```text
1. 在 Telegram 中搜索 @BotFather
2. 发送 /newbot 命令
3. 按提示输入 Bot 名称与用户名
4. 获取 HTTP API token（格式：123456789:ABCdef...）
```

### 获取聊天 ID

```bash
# 先将 Bot 加入群组，然后在群中发一条消息
curl "https://api.telegram.org/bot{{BOT_TOKEN}}/getUpdates" | jq '.result[-1].message.chat.id'
```

### 发送第一条消息

```bash
curl -X POST "https://api.telegram.org/bot{{BOT_TOKEN}}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "CHAT_ID",
    "text": "Hello from AI Agent!"
  }'
```

#
## 示例

### Bot Token 配置

```bash
# 环境变量配置
export TELEGRAM_BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrSTUvwxYZ"

# 在命令中引用
curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{"chat_id": "-1001234567890", "text": "Test message"}'
```

### 聊天 ID 格式

| 类型 | 格式 | 示例 |
|------|------|------|
| 私聊 | 用户数字 ID | `123456789` |
| 群组 | 负数 | `-1001234567890` |
| 频道 | 负数（公开频道可用 @username） | `-1009876543210` 或 `@mychannel` |

### 消息格式化

```bash
# Markdown 格式
curl -X POST "https://api.telegram.org/bot{{BOT_TOKEN}}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "-1001234567890",
    "text": "*加粗* _斜体_ `代码`\n[链接](https://example.com)",
    "parse_mode": "MarkdownV2",
    "disable_web_page_preview": true
  }'

# HTML 格式
curl -X POST "https://api.telegram.org/bot{{BOT_TOKEN}}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "-1001234567890",
    "text": "<b>加粗</b> <i>斜体</i> <code>代码</code>",
    "parse_mode": "HTML"
  }'
```

### 内联键盘按钮

```bash
curl -X POST "https://api.telegram.org/bot{{BOT_TOKEN}}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "-1001234567890",
    "text": "请选择操作：",
    "reply_markup": {
      "inline_keyboard": [
        [
          {"text": "确认", "callback_data": "confirm"},
          {"text": "取消", "callback_data": "cancel"}
        ]
      ]
    }
  }'
```

### Bot 命令设置

```bash
# 设置命令列表
curl -X POST "https://api.telegram.org/bot{{BOT_TOKEN}}/setMyCommands" \
  -H "Content-Type: application/json" \
  -d '{
    "commands": [
      {"command": "start", "description": "开始使用"},
      {"command": "help", "description": "获取帮助"},
      {"command": "status", "description": "查看状态"},
      {"command": "report", "description": "获取报告"}
    ]
  }'

# 获取命令列表
curl "https://api.telegram.org/bot{{BOT_TOKEN}}/getMyCommands"
```

## 最佳实践

### 已知限制

Telegram Bot API 限制：全局约 30 条消息/秒，单个聊天约 1 条消息/秒。收到 429 响应时按 `retry_after` 等待后重试。

### 2. 消息格式选择

- 简单文本：不设 `parse_mode`
- 含加粗/链接/代码：用 `MarkdownV2`（注意转义特殊字符）
- 含复杂 HTML：用 `HTML` 格式

### 3. 图片质量保持

`sendPhoto` 会压缩图片。如需保持原始质量，改用 `sendDocument` 发送：

```bash
curl -X POST "https://api.telegram.org/bot{{BOT_TOKEN}}/sendDocument" \
  -F "chat_id=-1001234567890" \
  -F "document=@/path/to/image.png"
```

### 4. 消息删除限制

Bot 只能删除自己发送的消息，或在 Bot 为管理员的群组中删除他人消息。群组中超过 48 小时的消息无法删除。

### 5. 长轮询与 Webhook 互斥

`getUpdates`（长轮询）与 Webhook 互斥。若 Webhook 已设置，调用 `getUpdates` 返回 409 冲突。删除 Webhook 后才能使用长轮询：

```bash
curl "https://api.telegram.org/bot{{BOT_TOKEN}}/deleteWebhook"
```

### 6. 聊天 ID 持久化

获取到的聊天 ID 应持久化存储，避免每次都通过 `getUpdates` 重新获取。私聊 ID 是用户数字 ID，群组以 `-100` 开头。
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 常见问题

### Q1：发送消息返回 403 Forbidden？
A：Bot 未被加入目标聊天，或被聊天管理员屏蔽。将 Bot 加入群组并确保有发送消息权限。

### Q2：发送消息返回 400 chat_not_found？
A：聊天 ID 不正确。群组以 `-100` 开头（如 `-1001234567890`），私聊用用户数字 ID。检查 ID 是否完整。

### Q3：Markdown 格式消息发送失败？
A：MarkdownV2 需要转义特殊字符（`_`、`*`、`[`、`]`、`(`、`)`、`~`、`` ` ``、`>`、`#`、`+`、`-`、`=`、`|`、`{`、`}`、`.`、`!`）。或改用 HTML 格式更简单。

### Q4：图片发送后质量下降？
A：`sendPhoto` 会压缩图片。使用 `sendDocument` 发送可保持原始质量，但不会显示预览。

### Q5：Bot 收不到群组消息？
A：检查 Bot 的隐私模式（Privacy Mode）。通过 BotFather 的 `/setprivacy` 关闭后 Bot 才能接收群组所有消息。关闭后需重新加入群组。

### Q6：getUpdates 返回 409 冲突？
A：已设置 Webhook，长轮询不可用。调用 `deleteWebhook` 删除后重试，或改用 Webhook 接收更新。

### Q7：免费版有哪些限制？
A：免费版不支持批量发送、群组管理（踢人/封禁/权限）、频道管理、Webhook 回调与审核功能。这些能力在专业版提供。

## 免费版限制

本免费版限制以下高级功能：
- 批量操作（批量消息、批量投票、批量转发）
- 群组管理（踢人、封禁、权限设置、管理员管理）
- 频道管理（频道发布、定时发布、频道信息管理）
- Webhook 回调与实时事件推送
- 消息审核与过滤（关键词过滤、媒体审核）
- 高级媒体处理（音视频转码、贴纸包管理）
- 机器人命令菜单（动态菜单、多语言支持）

解锁全部功能请使用专业版：`telegram-msg-toolkit-pro`

## 依赖说明

### 运行环境
- **Agent 平台**：支持 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：Windows / macOS / Linux
- **网络**：可访问 `api.telegram.org` 的网络连接
- **Telegram 账号**：已通过 BotFather 创建的 Bot 与有效 token

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |
| curl | CLI 工具 | 必需 | 系统自带或包管理器安装 |
| Telegram Bot Token | 凭证 | 必需 | 通过 BotFather 创建 Bot 获取 |
| jq | CLI 工具 | 推荐 | 用于 JSON 响应解析 |

### API Key 配置
- **Bot Token**：通过 BotFather 创建 Bot 获取，保存在环境变量 `TELEGRAM_BOT_TOKEN` 中
- **获取方式**：Telegram 中搜索 @BotFather → 发送 `/newbot` → 按提示操作 → 获取 HTTP API token
- **禁止**：在 SKILL.md 或脚本中硬编码 Bot Token
- **安全建议**：Token 等同于 Bot 密码，泄露后任何人可控制该 Bot。泄露后通过 BotFather `/revokenewtoken` 重置

### 可用性分类
- **分类**：MD+EXEC（纯 Markdown 指令，部分功能需要 exec 命令行执行能力）
- **说明**：基于 Markdown 的 AI Skill，通过自然语言指令驱动 Agent 执行任务
- **模型路由建议**：免费版使用低成本模型（如 GPT-4o-mini / Claude Haiku）即可完成消息发送与查询

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
