---
slug: "slack-hub-skill-free"
name: "slack-hub-skill-free"
version: "1.0.0"
displayName: "Slack消息中枢LITE"
summary: "提供包含Slack基础消息发送与公共频道列表,Bot Token直连Web API.面向团队协作场景的Slack基础消息集成技能（免费版）.通过Slack Bot Token直连Web API, 提"
summary_zh: "Slack基础消息发送与公共频道列表，Bot Token直连Web API。面向团队协作场景的Slack基础消息集成技能（免费版）。通过Slack Bot Token直连Web API"
license: "MIT"
description: "|-. 适用于需要slack hub skill相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  面向团队协作场景的Slack基础消息集成技能（免费版）。通过Slack Bot Token直连Web API，
  提供频道消息发送与公共频道列表两大基础能力.
  支持频道ID寻址、基础消息格式化（粗体/斜体/代码块）、emoji语法.
  适用于发布通知、频道发现等基础场景.
tags:
  - Communication
  - slack
  - hub
  - skill
  - automation
  - 消息API
  - 社交
  - 通信
  - token
  - bot
tools:
  - read
  - exec
  - write
homepage: ""
category: "Communication"
pricing_tier: free
---
# Slack消息中枢 LITE（Slack Hub Skill Free）

面向团队协作场景的Slack基础消息集成（免费版）。提供频道消息发送与公共频道列表两大能力.
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Slack消息中枢LITE处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
需要配置对应API Key，详见上文环境配置章节

### 可用性分类
- **分类**: MD+EXEC（）

**API Key配置方式**:
```bash
export API_KEY=${API_KEY:?请设置环境变量}
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 核心能力

### 1. 频道消息发送
向指定公共频道发送文本消息。频道参数接受频道ID（`C0123456789`）或频道名（`#general`）。支持基础Slack消息格式化：`*bold*`、`_italic_`、`` `code` ``、emoji语法 `:name:`.
### 2. 公共频道列表
列出工作区内所有公共频道，返回频道ID、名称、成员数、话题。可用于频道发现与ID解析.
> **升级提示**：线程回复、工作区内容搜索、用户DM发送、频道名自动解析、速率限制感知重试等高级功能仅在 slack-hub-skill 付费版中提供。- 验证返回数据的完整性和格式正确性
- 参考`公共频道列表`的配置文档进行参数调优
#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 适用场景

| 场景 | 典型输入 | 输出内容 | 涉及能力 |
|---:|---:|---:|---:|
| 通知发布 | 向#general发送会议提醒 | 消息投递确认+时间戳 | 消息发送 |
| 频道发现 | 列出所有公共频道 | 频道列表（ID、名称、成员数） | 频道列表 |

**不适用于**：线程回复、工作区搜索、DM发送、文件上传（需升级付费版）

## 使用流程

### 检查 Bot Token（永不打印值）
```bash
[ -n "${SLACK_BOT_TOKEN:-}" ] && echo ok || echo missing
```

### 缺失时引导配置
> 需要先配置 Slack Bot Token：
> 1. 访问 https://api.slack.com/apps 创建新App
> 2. 配置 Bot Token Scopes：`chat:write`、`channels:read`
> 3. 安装App到工作区，获取 `xoxb-` 开头的Bot Token
> 4. 终端环境变量：`export SLACK_BOT_TOKEN="${SLACK_BOT_TOKEN:?请设置环境变量}"`
> 5. 将Bot邀请到目标频道（`/invite @botname`）

**安全红线**：永不接受/回显/存储来自聊天输入的Token；Token仅作为 `Authorization: Bearer` 请求头使用.
### 发送消息或列出频道
1. 发送消息：`POST chat.postMessage`，传 `channel`、`text`
2. 列出频道：`GET conversations.list`，传 `types=public_channel`

### 透传结果
3. 发送成功返回 `{ok: true, channel, ts, message}`
4. 频道列表返回 `{ok: true, channels: [{id, name, num_members, ...}]}`

#
## 案例展示

### 案例1：通知发布
**场景**：团队需要在 `#general` 频道发布会议提醒

**执行**：
```bash
# 发送会议提醒
curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C0GENERAL01",
    "text": ":bell: *明日会议提醒*\n时间：周三 10:00\n地点：3号会议室\n议题：Q3路线图评审"
  }'
```

**输出**：
```json
{
  "ok": true,
  "channel": "C0GENERAL01",
  "ts": "1721452800.123456",
  "message": {
    "text": ":bell: *明日会议提醒*\n时间：周三 10:00\n地点：3号会议室\n议题：Q3路线图评审",
    "type": "message"
  }
}
```

**分析**：消息成功投递到 `#general` 频道，时间戳 `1721452800.123456` 可用于后续引用。`:bell:` 会被渲染为bell emoji，`*明日会议提醒*` 渲染为粗体.
## 错误处理

| 错误码 | 错误信息 | 原因分析 | 处理方式 |
|:---:|:---:|:---:|:---:|
| `invalid_auth` | `{ok:false, error:"invalid_auth"}` | Token无效/过期/格式错误 | 检查网络连接和配置后重试，引导用户检查 `SLACK_BOT_TOKEN` 是否以 `xoxb-` 开头 |
| `channel_not_found` | `{ok:false, error:"channel_not_found"}` | 频道ID不存在或Bot不是成员 | 引导用户用 `/invite @botname` 将Bot加入频道 |
| `rate_limited` | HTTP 429 + `Retry-After` 头 | 触发速率限制 | 等待 `Retry-After` 秒数后检查网络连接和配置后重试 |
| `missing_scope` | `{ok:false, error:"missing_scope"}` | Token缺少所需权限 | 引导用户添加 `chat:write` 或 `channels:read` Scope |
| `no_text` | `{ok:false, error:"no_text"}` | 消息内容为空或仅含空格 | 检查 `text` 参数非空 |

## 常见问题

### Q1：如何获取Slack Bot Token？
A：访问 https://api.slack.com/apps 创建新App，在 **OAuth & Permissions** 页面配置 Bot Token Scopes（至少 `chat:write`、`channels:read`），安装App到工作区后复制 `xoxb-` 开头的Token。注意将Bot邀请到目标频道后才能发送消息.
### Q2：Bot为什么发不出消息？
A：常见原因：1) Token缺少 `chat:write` 权限；2) Bot未加入目标频道（用 `/invite @botname` 邀请）；3) 频道ID错误。建议先用 `conversations.list` 确认频道ID，再检查返回的 `error` 字段.
### Q3：免费版和付费版有什么区别？
A：免费版（LITE）包含频道消息发送和公共频道列表两大基础功能。付费版（Slack消息中枢）额外提供：
- 线程回复（thread_ts 参数）
- 工作区内容搜索（消息检索+搜索修饰符）
- 用户DM发送
- 频道名自动解析为频道ID
- 速率限制感知与指数退避重试（最多3次）
- 3 个完整案例（vs 免费版 1 个）
- 8 种错误处理（vs 免费版 5 种）

### Q4：如何格式化消息内容？
A：Slack支持 `*bold*`（粗体）、`_italic_`（斜体）、`` `code` ``（行内代码）。emoji使用 `:name:` 语法，如 `:bell:`、`:rocket:`。换行使用 `\n`.
## 已知限制

1. **基础功能**：仅支持频道消息发送和公共频道列表，不支持线程回复、工作区搜索、DM发送（需升级付费版）
2. **无速率限制重试**：遇到429错误仅提示等待，不自动重试（付费版支持指数退避重试）
3. **无频道名解析**：需手动提供频道ID，不支持 `#general` 自动解析（付费版支持）
4. **仅公共频道**：频道列表仅返回公共频道，不包含私有频道
5. **无文件上传**：不支持文件上传，需使用 slack-workspace 技能

---
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> **需要更多能力？** 升级到 slack-hub-skill 付费版获取线程回复、工作区搜索、DM发送、频道名解析、速率限制重试等高级功能.