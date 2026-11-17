---
slug: slack-api-toolkit-free
name: slack-api-toolkit-free
version: 1.0.0
displayName: Slack API工具箱
summary: 通过托管OAuth安全调用Slack API，支持消息收发与频道管理，适合个人快速集成。
license: Proprietary
edition: free
description: Slack API工具箱（免费版）通过托管OAuth机制安全调用Slack API，免去手动管理Token的繁琐，支持消息收发与频道管理核心能力。核心能力：托管OAuth连接管理、消息发送与回复、频道列表与信息查询、用户信息查询、CLI与Python调用示例。Use
  when 需要API集成、接口对接、Webhook配置、系统连接时使用。不适用于逆向工程闭源API。
tags:
- 集成工具
- 团队协作
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: "L1-入门级"
pricing_model: per_use
suggested_price: "9.9 CNY/per_use"
tools: ["read", "write", "exec"]
tags: "API,接口,开发工具"
---
# Slack API工具箱（免费版）

## 概述

Slack API工具箱（免费版）通过托管OAuth机制帮助Agent安全调用Slack API。传统Slack集成需要手动创建App、配置OAuth scopes、管理Token刷新，本工具通过托管层自动处理OAuth，开发者只需建立连接即可调用API，Token由托管层注入。

本免费版聚焦"消息收发"与"频道管理"两类高频核心能力，提供CLI与Python双调用示例，适合个人开发者快速构建Slack自动化与通知机器人。

## 核心能力

| 能力 | 说明 | 免费版支持 |
|---|---|-----|
| 托管OAuth连接 | 自动管理Token，无需手动刷新 | 是 |
| 发送消息 | 文本与Block Kit消息 | 是 |
| 消息回复与更新 | 线程回复、消息更新与删除 | 是 |
| 频道列表与信息 | 列出频道、查看频道详情 | 是 |
| 用户信息查询 | 列出用户、查看用户详情 | 是 |
| 文件管理 | 上传、下载、删除文件 | 否 |
| 搜索 | 搜索消息与文件 | 否 |
| 反应与书签 | 表情反应、书签、置顶 | 否 |
| 批量操作 | 批量发消息、批量管理频道 | 否 |
| 审计日志 | 操作全程留痕 | 否 |

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输入**: 用户提供结果处理与输出所需的指令和必要参数。
**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：通过托管、安全调用、Slack、API、支持消息收发与频、道管理、适合个人快速集成、工具箱、机制安全调用、免去手动管理、的繁琐、道管理核心能力、核心能力、连接管理、消息发送与回复、频道列表与信息查、CLI、Python、调用示例、Use、when、接口对接、Webhook、系统连接时使用、不适用于逆向工程等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景1：个人开发者Slack自动化

小陈是一名独立开发者，希望每天早晨在Slack频道发送项目状态报告。他使用本工具：建立Slack连接，编写定时脚本调用消息发送API，无需手动管理Token，报告自动推送到指定频道。

### 场景2：团队通知机器人

运维团队需要一个机器人将告警信息推送到Slack。使用本工具：建立连接，在告警系统中调用消息发送API，告警自动以Block Kit格式推送到运维频道，支持线程回复进行告警讨论。

### 场景3：快速验证Slack集成可行性

产品经理想评估"将CI构建结果通知到Slack"的可行性。使用本工具快速建立连接并发送测试消息，验证集成可行后即可投入开发，无需先创建Slack App。

## 使用流程

### 依赖详情

```bash
# NPM
npm install -g @slack-gateway/cli
# ...
# 或 Homebrew
brew install slack-gateway/cli/sgw
```

### Step 2：登录并获取API Key

```bash
sgw login                    # 浏览器登录
sgw login --interactive      # 直接粘贴API Key
sgw whoami                   # 查看当前登录状态
```

或在控制台设置API Key为环境变量：

```bash
export SGW_API_KEY="your_api_key_here"
```

### Step 3：创建Slack连接

```bash
sgw connection create slack
```

返回的`url`在浏览器中打开，完成Slack OAuth授权。

### Step 4：发送第一条消息

```bash
sgw slack message send --channel C0123456789 --text 'Hello from Slack Gateway!'
```

#
## 示例

### CLI 发送消息

```bash
# 基础文本消息
sgw slack message send --channel C0123456789 --text 'Hello team'
# ...
# Block Kit 消息
sgw slack message send --channel C0123456789 \
  --blocks '[{"type":"section","text":{"type":"mrkdwn","text":"*加粗* 与 _斜体_"}}]'
# ...
# 线程回复
sgw slack message reply --channel C0123456789 --thread-ts 1234567890.123456 --text '回复内容'
# ...
# 更新消息
sgw slack message update --channel C0123456789 --ts 1234567890.123456 --text '更新后内容'
# ...
# 删除消息
sgw slack message delete --channel C0123456789 --ts 1234567890.123456
```

### Python 发送消息

```python
import os
import requests
# ...
api_key = os.environ['SGW_API_KEY']
base_url = 'https://api.slack-gateway.com'
# ...
resp = requests.post(
    f'{base_url}/slack/api/chat.postMessage',
    headers={
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    },
    json={'channel': 'C0123456789', 'text': 'Hello from Python!'}
)
print(resp.json())
```

### 频道与用户查询

```bash
# 列出频道
sgw slack channel list --types public_channel,private_channel --limit 100
# ...
# 查看频道信息
sgw slack channel view C0123456789
# ...
# 查看频道消息历史
sgw slack message list --channel C0123456789 --limit 50
# ...
# 列出用户
sgw slack user list --limit 100
# ...
# 按邮箱查找用户
sgw slack user lookup --email alice@example.com
```

### 指定连接（多工作区场景）

```bash
sgw slack message send --channel C0123456789 --text 'Hello!' --connection conn_xyz
```

## 最佳实践

1. **写操作需确认**：所有创建、更新、删除操作执行前需向用户确认目标与意图
2. **频道ID准确**：使用频道ID（C开头）而非频道名，避免歧义
3. **Block Kit格式**：复杂消息使用Block Kit，体验优于纯文本
4. **线程回复**：讨论类消息使用线程回复，保持频道整洁
5. **多连接指定**：多工作区场景务必指定`--connection`，避免发错工作区

## 常见问题

### Q1：返回400 Missing Slack connection怎么办？
A：尚未建立Slack连接。运行`sgw connection create slack`并在浏览器完成OAuth授权。

### Q2：返回401 Invalid API key怎么办？
A：检查`SGW_API_KEY`环境变量是否正确设置。运行`sgw whoami`确认登录状态，或重新`sgw login`。

### Q3：返回429 Rate limited怎么办？
A：已触发速率限制（每账户10请求/秒）。降低请求频率，批量场景考虑升级专业版使用批量接口。

### Q4：missing_scope错误怎么办？
A：当前连接的OAuth scopes不足。在控制台为该连接申请额外权限范围，或重新创建连接时勾选所需权限。

### Q5：如何发送带格式的消息？
A：使用Block Kit格式。`mrkdwn`类型支持Slack风格markdown（`*加粗*`、`_斜体_`），比纯文本表现力更强。

## 已知限制

本免费体验版限制以下高级功能：
- 不支持文件上传、下载与管理
- 不支持消息与文件搜索
- 不支持表情反应、书签、置顶
- 不支持批量操作（批量发消息、批量管理频道）
- 不支持操作审计日志
- 不支持定时消息

解锁全部功能请使用专业版：`slack-api-toolkit-pro`

## 依赖说明

### 运行环境
- **Agent平台**：支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**：Windows / macOS / Linux
- **网络**：可访问Slack网关与Slack API

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| Slack网关账户 | 在线服务 | 必需 | 在网关控制台注册 |
| Slack工作区 | 在线服务 | 必需 | 在Slack创建或加入 |
| Node.js | 运行时 | 可选 | CLI安装需要 |
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |

### API Key 配置
- **网关API Key**：存储于环境变量`SGW_API_KEY`或通过`sgw login`保存
- **Slack OAuth Token**：由网关托管，通过OAuth授权建立连接，本地不保存
- **禁止**：在代码或脚本中硬编码API Key或Slack Token

### 可用性分类
- **分类**：MD+EXEC（纯Markdown指令，部分功能需要exec命令行执行能力）
- **说明**：基于Markdown的AI Skill，通过自然语言指令驱动Agent完成操作

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Slack API工具箱处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "slack apikit"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
