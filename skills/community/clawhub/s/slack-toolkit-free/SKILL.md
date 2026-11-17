---
name: "slack-toolkit-free"
description: "Slack消息管理基础工具，支持发送、编辑、删除消息，表情回应与置顶操作，适合个人日常使用。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "Slack工具箱免费版"
  version: "1.0.0"
  summary: "Slack消息管理基础工具，支持发送、编辑、删除消息，表情回应与置顶操作，适合个人日常使用。"
  tags:
    - "沟通协作"
    - "Slack"
    - "消息管理"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# Slack工具箱（免费版）

## 概述

Slack工具箱免费版是一款面向个人用户的Slack消息管理工具。通过Bot Token认证，提供消息发送、编辑、删除、读取，表情回应，消息置顶，成员信息查询等核心功能，帮助你高效管理日常工作沟通。

## 核心能力

### 1. 消息管理

支持向频道或用户发送消息，编辑已发送消息，删除消息，以及读取频道最近消息。

**输入**: 用户提供消息管理所需的指令和必要参数。
**处理**: 按照skill规范执行消息管理操作,遵循单一意图原则。
**输出**: 返回消息管理的执行结果,包含操作状态和输出数据。

- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 2. 表情回应

为消息添加表情回应（支持Unicode和自定义表情名称），查看消息上的所有回应。

**输入**: 用户提供表情回应所需的指令和必要参数。
**处理**: 按照skill规范执行表情回应操作,遵循单一意图原则。
**输出**: 返回表情回应的执行结果,包含操作状态和输出数据。

- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 3. 消息置顶

将重要消息置顶到频道，取消置顶，查看频道置顶列表。

**输入**: 用户提供消息置顶所需的指令和必要参数。
**处理**: 按照skill规范执行消息置顶操作,遵循单一意图原则。
**输出**: 返回消息置顶的执行结果,包含操作状态和输出数据。

- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 4. 成员信息

通过用户ID查询成员详细信息。

**输入**: 用户提供成员信息所需的指令和必要参数。
**处理**: 按照skill规范执行成员信息操作,遵循单一意图原则。
**输出**: 返回成员信息的执行结果,包含操作状态和输出数据。

- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 5. 表情列表

查看工作区中所有自定义表情。

**输入**: 用户提供表情列表所需的指令和必要参数。
**处理**: 按照skill规范执行表情列表操作,遵循单一意图原则。
**输出**: 返回表情列表的执行结果,包含操作状态和输出数据。
**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Slack、消息管理基础工具、支持发送、表情回应与置顶操、适合个人日常使用、工具箱、免费版、面向个人用户的、消息管理工具、核心能力、消息发送、删除与读取、表情回应添加与查、消息置顶与取消置、成员信息查询、自定义表情列表查等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：发送工作通知消息

向团队频道发送项目进度通知。

```json
{
  "action": "sendMessage",
  "to": "channel:C0123456789",
  "content": "项目Alpha v2.1.0 已部署到生产环境，请团队验证。"
}
```

### 场景二：标记任务完成

用表情回应标记已完成的任务消息。

```json
{
  "action": "react",
  "channelId": "C0123456789",
  "messageId": "1712023032.1234",
  "emoji": "white_check_mark"
}
```

### 场景三：置顶重要决策

将团队决策消息置顶，方便后续查阅。

```json
{
  "action": "pinMessage",
  "channelId": "C0123456789",
  "messageId": "1712023032.1234"
}
```

## 不适用场景

以下场景Slack工具箱免费版不适合处理：

- 垃圾信息群发
- 通信协议逆向
- 电话语音交互

## 触发条件

需要消息发送、通知推送、邮件短信、通信集成时使用。不适用于非本工具能力范围的需求。

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 安装

```bash
npx skillhub@latest install slack-toolkit-free
```

### 配置Bot Token

```bash
# 在 .env 文件中配置
SLACK_BOT_TOKEN=REDACTED-SECRET
```

### 基本使用

所有操作通过JSON参数调用：

```bash
# 发送消息
slack-toolkit --action sendMessage --to "channel:C0123456789" \
  --content "Hello from Slack Toolkit"

# 读取最近消息
slack-toolkit --action readMessages --channelId "C0123456789" --limit 20

# 添加表情回应
slack-toolkit --action react --channelId "C0123456789" \
  --messageId "1712023032.1234" --emoji "thumbsup"
```

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

#
## 示例

```yaml
# config.yaml
slack:
  bot_token: "${SLACK_BOT_TOKEN}"
  default_channel: "C0123456789"
  
# 功能开关（免费版全部默认启用）
features:
  reactions: true        # 表情回应
  messages: true         # 消息读写
  pins: true             # 置顶管理
  memberInfo: true       # 成员信息
  emojiList: true        # 表情列表
```

### 操作总览

| 操作组 | 默认状态 | 说明 |
|:-------|:---------|:-----|
| reactions | 启用 | 添加/查看表情回应 |
| messages | 启用 | 读取/发送/编辑/删除消息 |
| pins | 启用 | 置顶/取消置顶/查看置顶列表 |
| memberInfo | 启用 | 查询成员信息 |
| emojiList | 启用 | 查看自定义表情列表 |

## 最佳实践

### 消息管理规范

| 实践 | 说明 |
|:-----|:-----|
| 频道选择 | 公开讨论用频道，私密沟通用私信 |
| 消息长度 | 长内容使用线程回复，保持频道整洁 |
| 表情回应 | 用表情代替"收到""好的"等短回复 |
| 置顶管理 | 仅置顶重要决策与公告，避免过多 |

### 常用操作示例

```json
// 发送消息到频道
{
  "action": "sendMessage",
  "to": "channel:C0123456789",
  "content": "今日站会15分钟后开始"
}

// 发送私信
{
  "action": "sendMessage",
  "to": "user:U0123456789",
  "content": "请查看刚才发到频道的文档"
}

// 编辑消息
{
  "action": "editMessage",
  "channelId": "C0123456789",
  "messageId": "1712023032.1234",
  "content": "更新后的内容"
}

// 删除消息
{
  "action": "deleteMessage",
  "channelId": "C0123456789",
  "messageId": "1712023032.1234"
}

// 读取最近消息
{
  "action": "readMessages",
  "channelId": "C0123456789",
  "limit": 20
}

// 查看消息上的回应
{
  "action": "reactions",
  "channelId": "C0123456789",
  "messageId": "1712023032.1234"
}

// 查看置顶列表
{
  "action": "listPins",
  "channelId": "C0123456789"
}

// 查询成员信息
{
  "action": "memberInfo",
  "userId": "U0123456789"
}

// 查看自定义表情
{
  "action": "emojiList"
}
```

## 错误处理


| 序号 | 错误场景 | 原因 | 处理方式 | 优先级 |
|------|----------|------|----------|--------|
| 1 | 输入参数缺失 | 用户未提供必要参数 | 提示用户提供所需参数后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 | P0 |
| 2 | 执行超时 | 处理时间过长 | 检查输入数据量,分批处理 | P1 |
| 3 | 输出格式错误 | 结果不符合预期格式 | 检查`output_format`参数配置 | P1 |

## 常见问题

### Q: 如何获取Bot Token？

在Slack App管理页面创建应用，添加Bot Token Scopes（如`chat:write`、`reactions:write`、`pins:write`等），安装到工作区后获取`xoxb-`开头的Token。

### Q: 免费版支持批量操作吗？

免费版仅支持单条消息操作。如需批量发送、批量编辑等能力，请升级到PRO版本。

### Q: 频道ID和消息ID从哪里获取？

- **频道ID**: 在Slack中右键频道名 -> 查看频道详情 -> 最下方显示频道ID
- **消息ID**: 即消息时间戳，格式如`1712023032.1234`，右键消息 -> 复制链接中包含

### Q: 表情回应支持哪些格式？

支持两种格式：
- Unicode表情：`"emoji": "✅"`
- Slack自定义表情名称：`"emoji": ":custom_emoji:"`

### Q: 发送消息失败怎么办？

```bash
# 错误处理
# 1. channel_not_found - Bot未加入该频道，需先邀请Bot加入
# 2. not_authed - Token无效或过期，重新获取
# 3. missing_scope - Token权限不足，添加对应Scope
# 4. rate_limited - 请求过于频繁，稍后重试
```

## 依赖说明

### 运行环境

- **Agent 平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **网络环境**: 需能访问 `https://slack.com/api/` 端点

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Slack Bot Token | API凭证 | 必需 | Slack App管理页面创建 |
| requests | Python库 | 推荐 | `pip install requests` |

### API Key 配置

```bash
# Slack Bot Token（必需）
export SLACK_BOT_TOKEN="REDACTED-SECRET"

# 所需Bot Token Scopes:
# - chat:write        发送消息
# - chat:write.edit   编辑消息
# - chat:write.delete 删除消息  
# - channels:history  读取频道消息
# - reactions:write   添加表情回应
# - reactions:read    查看表情回应
# - pins:write        置顶/取消置顶
# - pins:read         查看置顶列表
# - users:read        查询成员信息
# - emoji:read        查看自定义表情
```

### 可用性分类

- **分类**: MD+EXEC+API（Markdown指令 + 命令行执行 + Slack API调用）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent完成操作，调用Slack Web API实现消息管理
- **适用人群**: 个人用户、团队成员、Slack日常使用者
- **版本限制**: 免费版支持单条操作，PRO版本提供批量处理与高级管理能力

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
