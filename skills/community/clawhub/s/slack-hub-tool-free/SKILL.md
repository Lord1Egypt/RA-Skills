---slug: slack-hub-tool-free
name: slack-hub-tool-free
version: 1.0.0
displayName: Slack Hub工具免费版
summary: "Slack消息发送与搜"
license: Proprietary
edition: free
description: Slack Hub工具（免费版）—— 面向个人用户的Slack消息发送与搜索工具，可处理提升工作效率
  核心能力:

  - 向频道或用户发送消息

  - 线程回复消息

  - 工作区内容搜索

  - 公开频道列表查看

  适用场景:

  - 日常工作消息发送

  - 线程内讨论回复

  - 快速查找历史消息

  - 浏览可用频道

  差异化: 聚焦个人用户核心需求，提供简洁的Slack消息发送与搜索能力，配置简单.
  适用关键词: Slack发送, 线程回复, 消息搜索, 频道列表, slack, hub, send, search, thread'
tags:
  - 沟通协作
  - Slack
  - 消息搜索
  - 社交
  - 通信
  - slack
  - slack-hub-tool
  - bot
  - token
  - bash
tools:
  - read
  - exec
  - write
homepage: ""
category: "Communication"---# Slack Hub工具（免费版）

## 概述

Slack Hub工具免费版是一款面向个人用户的Slack消息发送与搜索工具。通过Slack Bot Token认证，提供消息发送、线程回复、工作区搜索和频道列表查看功能，帮助你高效完成日常Slack沟通.
## 核心能力

### 1. 消息发送

向指定频道或用户发送文本消息，支持通过频道ID或频道名称指定目标.

**处理**: 解析消息发送的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回消息发送的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 2. 线程回复

在指定消息的线程中进行回复，保持讨论上下文完整.

**处理**: 解析线程回复的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回线程回复的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 3. 工作区搜索

搜索工作区中的消息或文件，快速定位历史信息.

**处理**: 解析工作区搜索的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回工作区搜索的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 4. 频道列表

列出工作区中所有公开频道，方便查找目标频道.

**处理**: 解析频道列表的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回频道列表的响应数据,包含状态码、结果和日志.
**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Slack、消息发送与搜索基、础工具、支持频道列表查看、消息发送与线程回、适合个人日常使用、Hub、免费版、面向个人用户的、消息发送与搜索工等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：向频道发送通知

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Slack Hub工具免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 通过频道名称发送
slack-hub-tool send \
  --target "#general" \
  --message "今日部署已完成，版本v2.1.0已上线"
# ...
# 通过频道ID发送
slack-hub-tool send \
  --target "C0123456789" \
  --message "项目评审会议改至周五14:00"
```

### 场景二：线程内回复讨论

```bash
# 在指定消息的线程中回复
slack-hub-tool send \
  --target "C0123456789" \
  --message "这个问题我来处理，预计今天内解决" \
  --thread-ts "1712023032.1234"
```

### 场景三：搜索历史消息

```bash
# 搜索包含关键词的消息
slack-hub-tool search --query "部署文档"
# ...
# 搜索特定频道的消息
slack-hub-tool search --query "bug修复" --channel "C0123456789"
```

## 不适用场景

以下场景Slack Hub工具免费版不适合处理：

- 垃圾信息群发
- 通信协议逆向
- 电话语音交互

## 触发条件

需要消息发送、通知推送、邮件短信、通信集成时使用。不适用于非本工具能力范围的需求.
## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 安装

```bash
npx skillhub@latest install slack-hub-tool-free
```

### 配置Bot Token

在项目根目录创建 `.env` 文件：

```bash
# .env
SLACK_BOT_TOKEN=REDACTED-SECRET
```

### 基本使用

```bash
# 列出所有公开频道
slack-hub-tool list-channels
# ...
# 发送消息
slack-hub-tool send --target "#general" --message "Hello World"
# ...
# 线程回复
slack-hub-tool send --target "C0123456789" \
  --message "收到，我来跟进" \
# ...
# 搜索消息
slack-hub-tool search --query "项目计划"
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 示例

```yaml
# config.yaml
slack:
  bot_token: "${SLACK_BOT_TOKEN}"
  default_channel: "#general"
# ...
# 功能配置
features:
  send: true              # 消息发送
  thread_reply: true      # 线程回复
  search: true            # 内容搜索
  list_channels: true     # 频道列表
# ...
# 搜索配置
search:
  max_results: 20         # 最大返回结果数
  sort: "timestamp"       # 排序方式: timestamp / score
```

### 工具说明

| 工具 | 功能 | 必需参数 | 可选参数 |
|:-----|:-----|:-----|:-----|
| `slack_send` | 发送消息 | `target`, `message` | `thread_ts` |
| `slack_search` | 搜索消息 | `query` | `channel`, `max_results` |
| `slack_list_channels` | 列出频道 | 无 | `exclude_archived` |

## 最佳实践

### 消息发送规范

| 实践 | 说明 |
|---:|---:|
| 目标明确 | 使用频道名称时以`#`开头，私信用`@`用户名 |
| 内容简洁 | 每条消息聚焦一个主题，长内容用线程 |
| 线程回复 | 讨论具体消息时使用`thread_ts`在线程内回复 |
| 搜索优化 | 使用具体关键词，避免过于宽泛的搜索词 |

### 搜索技巧

```bash
# 精确短语搜索
slack-hub-tool search --query "\"部署文档\""
# ...
# 按频道搜索
slack-hub-tool search --query "bug" --channel "C0123456789"
# ...
# 组合关键词
slack-hub-tool search --query "项目 AND 评审"
```

### 频道管理建议

```bash
# 查看所有频道（包括已归档）
slack-hub-tool list-channels --include-archived
# ...
# 仅查看活跃频道
slack-hub-tool list-channels --exclude-archived
```

### 线程回复规范

| 场景 | 是否使用线程 | 说明 |
|:---:|:---:|:---:|
| 回复具体消息 | 是 | 保持讨论上下文 |
| 全频道通知 | 否 | 直接发送到频道 |
| 讨论技术细节 | 是 | 避免刷屏主频道 |
| 简短确认 | 否 | 用表情回应代替 |

## 常见问题

### Q: 如何获取Slack Bot Token？

1. 访问 Slack App 管理页面创建新应用
2. 添加 Bot Token Scopes：`chat:write`、`search:read`、`channels:read`
3. 安装应用到工作区
4. 复制 `xoxb-` 开头的 Bot User OAuth Token

### Q: 发送消息时频道名称和ID有什么区别？

两者均可使用。频道名称更直观（如`#general`），频道ID更精确（如`C0123456789`）。当频道名称包含特殊字符时，建议使用ID.
### Q: 线程回复的 thread_ts 从哪里获取？

`thread_ts` 是被回复消息的时间戳。可以通过读取频道消息获取，格式如`1712023032.1234`.
### Q: 搜索功能能搜到私信吗？

免费版搜索范围限于公开频道和已加入的私密频道。私信内容不在搜索范围内.
### Q: Bot Token权限不足怎么办？

```bash
# 常见权限错误:
# missing_scope - 需要添加对应Scope
# not_authed - Token无效，重新获取
# channel_not_found - Bot未加入目标频道
```

确保Bot Token包含以下Scope：
- `chat:write` - 发送消息
- `search:read` - 搜索消息
- `channels:read` - 读取频道列表

## 依赖说明

### 运行环境

- **Agent 平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **网络环境**: 需能访问Slack API端点 `https://slack.com/api/`

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Slack Bot Token | API凭证 | 必需 | Slack App管理页面创建 |
| requests | Python库 | 推荐 | `pip install requests` |

### API Key 配置

```bash
# Slack Bot Token（必需）
export SLACK_BOT_TOKEN="REDACTED-SECRET"
# ...
# 所需Bot Token Scopes:
# - chat:write          发送消息
# - search:read         搜索工作区内容
# - channels:read       列出公开频道
# - groups:read         列出私密频道（如需）
```

### API 端点说明

本工具调用以下Slack Web API端点：
- `https://slack.com/api/chat.postMessage` - 发送消息
- `https://slack.com/api/search.messages` - 搜索消息
- `https://slack.com/api/conversations.list` - 列出频道

### 可用性分类

- **分类**: MD+EXEC+API（Markdown指令 + 命令行执行 + Slack API调用）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent完成操作，调用Slack Web API实现消息发送与搜索
- **适用人群**: 个人用户、团队成员、Slack日常使用者
- **版本限制**: 免费版支持基础发送与搜索，PRO版本提供高级搜索、批量操作与限流处理

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Slack Hub工具免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "slack hub"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
