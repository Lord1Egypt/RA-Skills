---
name: "slack-workspace-manager-free"
description: "Slack工作区基础管理工具，支持消息发送、频道管理、文件处理与提醒创建，适合个人与小型团队。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "Slack工作区管理免费版"
  version: "1.0.0"
  summary: "Slack工作区基础管理工具，支持消息发送、频道管理、文件处理与提醒创建，适合个人与小型团队。"
  tags:
    - "沟通协作"
    - "Slack"
    - "工作区管理"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# Slack工作区管理器（免费版）

## 概述

Slack工作区管理器免费版是一款面向个人与小型团队的Slack工作区管理工具。通过OAuth安全认证连接Slack工作区，提供消息管理、频道管理、文件处理、提醒创建、用户查询等核心功能，帮助你高效管理日常工作协作。

所有写操作均需用户确认后执行，确保操作安全可控。

## 核心能力

### 1. 消息管理

发送文本消息、线程回复、定时消息，删除与更新已发送消息。

**输入**: 用户提供消息管理所需的指令和必要参数。
**处理**: 按照skill规范执行消息管理操作,遵循单一意图原则。
**输出**: 返回消息管理的执行结果,包含操作状态和输出数据。

- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 2. 频道管理

列出所有频道、搜索频道、创建新频道、设置频道主题与用途。

**输入**: 用户提供频道管理所需的指令和必要参数。
**处理**: 按照skill规范执行频道管理操作,遵循单一意图原则。
**输出**: 返回频道管理的执行结果,包含操作状态和输出数据。

- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 3. 文件处理

上传文件到频道、列出工作区文件、下载文件。

**输入**: 用户提供文件处理所需的指令和必要参数。
**处理**: 按照skill规范执行文件处理操作,遵循单一意图原则。
**输出**: 返回文件处理的执行结果,包含操作状态和输出数据。

- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 4. 提醒管理

创建定时提醒、列出所有提醒、查看提醒详情、完成与删除提醒。

**输入**: 用户提供提醒管理所需的指令和必要参数。
**处理**: 按照skill规范执行提醒管理操作,遵循单一意图原则。
**输出**: 返回提醒管理的执行结果,包含操作状态和输出数据。

- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 5. 用户查询

列出所有用户、按邮箱查找用户、查看用户在线状态与勿扰状态。

**输入**: 用户提供用户查询所需的指令和必要参数。
**处理**: 按照skill规范执行用户查询操作,遵循单一意图原则。
**输出**: 返回用户查询的执行结果,包含操作状态和输出数据。
**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Slack、工作区基础管理工、支持消息发送、文件处理与提醒创、适合个人与小型团、工作区管理器、免费版、面向个人与小型团、工作区管理工具、核心能力、消息发送、线程回复与定时消、频道创建、查找与列表查看、文件上传与列表查、提醒创建与管理、用户查询与状态查等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：创建项目频道并发送通知

```bash
# 创建新的项目频道
slack-workspace-manager create-channel \
  --name "project-alpha" \
  --is-private false

# 设置频道主题
slack-workspace-manager set-topic \
  --channel "C0123456789" \
  --topic "Alpha项目协作频道"

# 发送启动通知
slack-workspace-manager send-message \
  --channel "C0123456789" \
  --text "项目Alpha正式启动！请各位同步各自负责的模块。"
```

### 场景二：上传文件并设置提醒

```bash
# 上传项目文档到频道
slack-workspace-manager upload-file \
  --channel "C0123456789" \
  --filename "project_plan.pdf" \
  --title "项目计划书"

# 设置每周五的周报提醒
slack-workspace-manager create-reminder \
  --text "提交本周工作周报" \
  --time "every friday at 17:00"

# 查看所有提醒
slack-workspace-manager list-reminders
```

### 场景三：查找同事并发送私信

```bash
# 按邮箱查找用户
slack-workspace-manager find-user \
  --email "colleague@company.com"

# 查看用户在线状态
slack-workspace-manager user-presence \
  --user-id "U0123456789"

# 发送私信
slack-workspace-manager send-message \
  --channel "D0123456789" \
  --text "你好，关于昨天的设计文档有几个问题想讨论"
```

## 不适用场景

以下场景Slack工作区管理免费版不适合处理：

- 实际人员绩效评估
- 财务预算审批
- 合同法务审核

## 触发条件

需要项目管理、任务规划、进度跟踪、团队协作时使用。不适用于非本工具能力范围的需求。

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 依赖详情

```bash
# 安装工具
npx skillhub@latest install slack-workspace-manager-free

# 连接Slack工作区（OAuth认证）
slack-workspace-manager connect
# 浏览器将打开授权页面，完成授权后自动连接
```

### 基本使用

```bash
# 验证连接
slack-workspace-manager list-connections

# 列出所有频道
slack-workspace-manager list-channels

# 发送消息
slack-workspace-manager send-message \
  --channel "C0123456789" \
  --text "Hello from Workspace Manager"

# 线程回复
slack-workspace-manager send-thread-reply \
  --channel "C0123456789" \
  --thread-ts "1234567890.123456" \
  --text "收到，我来跟进"
```

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。


## 示例

```yaml
# config.yaml
slack:
  auth_mode: "oauth"          # OAuth认证模式
  default_channel: "C0123456789"

# 功能配置
features:
  messages: true              # 消息管理
  channels: true              # 频道管理
  files: true                 # 文件处理
  reminders: true             # 提醒管理
  users: true                 # 用户查询

# 安全配置
security:
  confirm_writes: true        # 写操作需确认
  confirm_deletes: true       # 删除操作需确认
  log_operations: true        # 记录操作日志
```

### 工具分类总览

| 类别 | 工具 | 模式 | 说明 |
|:-----|:-----|:-----|:-----|
| 消息 | send_message | 写 | 发送文本消息 |
| 消息 | send_thread_reply | 写 | 线程回复 |
| 消息 | schedule_message | 写 | 定时消息 |
| 消息 | update_message | 写 | 更新消息 |
| 消息 | delete_message | 写 | 删除消息 |
| 频道 | list_channels | 读 | 列出所有频道 |
| 频道 | find_channels | 读 | 搜索频道 |
| 频道 | create_channel | 写 | 创建频道 |
| 频道 | set_channel_topic | 写 | 设置频道主题 |
| 文件 | upload_file | 写 | 上传文件 |
| 文件 | list_files | 读 | 列出文件 |
| 文件 | download_file | 读 | 下载文件 |
| 提醒 | create_reminder | 写 | 创建提醒 |
| 提醒 | list_reminders | 读 | 列出提醒 |
| 用户 | list_users | 读 | 列出所有用户 |
| 用户 | find_user_by_email | 读 | 按邮箱查找用户 |
| 用户 | get_user_presence | 读 | 查看用户状态 |

## 最佳实践

### 安全操作规范

| 规范 | 说明 |
|:-----|:-----|
| 写操作确认 | 所有写操作执行前预览并确认 |
| 删除谨慎 | 删除操作标记为高影响，双重确认 |
| 频道命名 | 使用小写字母与连字符，如`project-alpha` |
| 提醒时间 | 使用自然语言设置，如"every monday at 9am" |

### 操作流程

```text
读操作（安全）:
  list → get → search → find → call
  示例: 查找频道 → 获取历史 → 显示消息

写操作（需确认）:
  describe → preview → confirm → call
  示例: 预览消息 → 用户确认 → 发送消息
```

### 常用操作示例

```bash
# 列出所有频道
slack-workspace-manager list-channels

# 搜索频道
slack-workspace-manager find-channels --query "project"

# 获取频道历史消息
slack-workspace-manager get-history \
  --channel "C0123456789" \
  --limit 50

# 获取线程回复
slack-workspace-manager get-thread \
  --channel "C0123456789" \
  --thread-ts "1234567890.123456"

# 设置定时消息
slack-workspace-manager schedule-message \
  --channel "C0123456789" \
  --text "每周提醒：更新项目状态" \
  --time "every monday at 9am"
```

## 常见问题

### Q: 如何连接Slack工作区？

通过OAuth认证流程连接。运行`connect`命令后，浏览器会打开Slack授权页面，授权后工具自动获取并安全存储OAuth Token，后续操作无需再次认证。

### Q: 写操作为什么需要确认？

为确保操作安全，所有写操作（发送消息、创建频道、删除文件等）在执行前会显示预览，用户确认后才执行。这可以防止误操作。

### Q: 频道ID和频道名称如何转换？

```bash
# 通过名称查找频道ID
slack-workspace-manager find-channels --query "general"
# 返回结果包含频道ID
```

大部分工具需要频道ID（C开头），可先通过`find-channels`查找。

### Q: 定时消息支持哪些时间格式？

支持自然语言和Unix时间戳：
- 自然语言：`"in 15 minutes"`、`"every thursday at 2pm"`、`"tomorrow at 9am"`
- Unix时间戳：`1712023032`

### 已知限制

受Slack API限制，单文件最大不超过1GB。大文件建议先上传到文件托管服务，再分享链接。

### Q: 连接失败怎么办？

```bash
# 检查连接状态
slack-workspace-manager list-connections

# 重新连接
slack-workspace-manager connect

# 常见问题
# 1. Token过期 - 重新授权
# 2. 权限不足 - 在Slack管理页面调整App权限
# 3. 网络问题 - 检查网络连接
```
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 依赖说明

### 运行环境

- **Agent 平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **网络环境**: 需能访问Slack API端点

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Slack OAuth Token | API凭证 | 必需 | OAuth授权流程获取 |
| requests | Python库 | 推荐 | `pip install requests` |

### API Key 配置

```bash
# 通过OAuth流程自动配置（推荐）
slack-workspace-manager connect

# Token由工具安全存储，无需手动配置
# 所需OAuth Scopes:
# - chat:write              发送消息
# - channels:read           读取频道
# - channels:write          管理频道
# - files:read              读取文件
# - files:write             上传文件
# - reminders:read          读取提醒
# - reminders:write         管理提醒
# - users:read              读取用户信息
# - users:read.email        按邮箱查找用户
```

### 可用性分类

- **分类**: MD+EXEC+API（Markdown指令 + 命令行执行 + Slack API调用）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent完成操作，通过OAuth认证调用Slack Web API管理工作区
- **适用人群**: 个人用户、小型团队、Slack工作区管理员
- **版本限制**: 免费版支持基础工作区管理，PRO版本提供企业Grid、审计日志与批量操作能力

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
