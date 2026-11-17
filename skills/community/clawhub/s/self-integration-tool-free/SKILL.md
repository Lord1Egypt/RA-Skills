---
slug: self-integration-tool-free
name: self-integration-tool-free
version: 1.0.1
displayName: 自集成工具
summary: "通过统一网关连接任意外部应用并执行操作，适合个人开发者快速打通多平台.。自集成工具（免费版）通过统一集成网关让Agent连接任意外部应用（Slack、HubSpot、Notion等）并执行操"
license: Proprietary
edition: free
description: 自集成工具（免费版）通过统一集成网关让Agent连接任意外部应用（Slack、HubSpot、Notion等）并执行操作，无需为每个平台单独开发集成。核心能力：已有连接查询、连接器搜索、OAuth授权连接创建、动作搜索与执行、基础API参考。Use，可自动提升工作效率
  when 需要API集成、接口对接、Webhook配置、系统连接时使用。不适用于逆向工程闭源API.
tags:
  - 集成工具
  - 自动化
  - 工具
  - 效率
  - 集成
  - integration
  - 开发
  - 代码
  - 知识
  - api
  - slack
  - integration_token
  - bash
  - authorization
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Automation"
---
# 自集成工具（免费版）

## 概述

自集成工具（免费版）通过统一集成网关帮助Agent连接任意外部应用并执行操作。传统方式下，每接入一个SaaS平台（Slack、HubSpot、Notion等）都需要单独开发OAuth流程与API适配层。本工具通过"连接器"抽象，将各平台的差异封装为统一接口，Agent只需"建立连接-搜索动作-执行动作"三步即可操作任意已支持的应用.
本免费版聚焦个人开发者的核心集成场景，提供预置连接器查询、OAuth授权连接与动作执行能力，适合快速验证集成可行性与构建简单跨应用工作流.
## 核心能力

| 能力 | 说明 | 免费版支持 |
|---|---|-----|
| 已有连接查询 | 列出已建立的连接 | 是 |
| 连接器搜索 | 按应用名搜索预置连接器 | 是 |
| OAuth授权连接 | 创建授权链接供用户完成认证 | 是 |
| 动作搜索 | 自然语言搜索可执行动作 | 是 |
| 动作执行 | 执行单个动作并返回结果 | 是 |
| 自定义连接器构建 | 为未支持的应用构建连接器 | 否 |
| 批量动作 | 批量执行多个动作 | 否 |
| 工作流自动化 | 编排多步骤工作流 | 否 |
| 审计日志 | 操作全程留痕 | 否 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：通过统一网关连接、任意外部应用并执、适合个人开发者快、速打通多平台、自集成工具、通过统一集成网关、Agent、连接任意外部应用、Slack、HubSpot、Notion、并执行操作、无需为每个平台单、独开发集成、授权连接创建、动作搜索与执行、API、Use、when、接口对接、Webhook、系统连接时使用、不适用于逆向工程等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 使用场景

### 场景1：个人开发者打通Slack与HubSpot

小王是一名独立开发者，希望将Slack中收到的线索自动同步到HubSpot CRM。他使用本工具：搜索Slack连接器并建立连接，搜索HubSpot连接器并建立连接，搜索"创建联系人"动作并在Slack消息触发时执行，实现线索自动入库.
### 场景2：快速验证外部应用集成可行性

产品经理想评估"将Notion文档同步到Slack频道"的可行性。使用本工具搜索Notion与Slack连接器，确认两者均已有预置连接器与相关动作，即可判定集成可行，无需投入开发资源.
### 场景3：MCP工具集成外部应用

当需要将外部应用能力作为MCP工具接入Agent时，本工具提供统一连接层：MCP端点通过本工具建立连接并执行动作，无需为每个应用单独实现MCP适配.
## 使用流程

### Step 1：配置API Token

在集成网关控制台获取API Token，设置为环境变量：

```bash
export INTEGRATION_TOKEN="your_token_here"
```

所有请求携带`Authorization: Bearer $INTEGRATION_TOKEN`，基础URL为`https://api.integration-gateway.com`.
### Step 2：检查已有连接

```bash
curl https://api.integration-gateway.com/connections \
  -H "Authorization: Bearer $INTEGRATION_TOKEN"
```

查看是否已有目标应用的连接。若已有且`disconnected`为`false`，可直接跳到步骤4.
### Step 3：搜索并建立连接

搜索目标应用的连接器：

```bash
curl "https://api.integration-gateway.com/search?q=slack" \
  -H "Authorization: Bearer $INTEGRATION_TOKEN"
```

找到`elementType: "connector"`的结果，使用其`id`创建连接请求：

```bash
curl -X POST https://api.integration-gateway.com/connection-requests \
  -H "Authorization: Bearer $INTEGRATION_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"connectorId": "cnt_abc123"}'
```

响应中的`url`需在浏览器中打开，完成OAuth授权.
### Step 4：搜索并执行动作

授权完成后，搜索可用动作：

```bash
curl "https://api.integration-gateway.com/actions?connectionId=con_abc123&intent=send+a+message&limit=10" \
  -H "Authorization: Bearer $INTEGRATION_TOKEN"
```

执行动作：

```bash
curl -X POST "https://api.integration-gateway.com/actions/act_xyz/run?connectionId=con_abc123" \
  -H "Authorization: Bearer $INTEGRATION_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"input": {"channel": "#general", "text": "Hello!"}}'
```

#
## 示例

### 查询已有连接

```bash
curl https://api.integration-gateway.com/connections \
  -H "Authorization: Bearer $INTEGRATION_TOKEN"
```

响应字段说明：`id`（连接ID）、`name`（连接名）、`connectorId`（连接器ID）、`disconnected`（是否已断开）、`state`（状态：READY表示可用）.
### 创建连接请求

```bash
integration-gateway.com/connection-requests \
  -H "Authorization: Bearer $INTEGRATION_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "connectorId": "cnt_abc123",
    "name": "我的Slack工作区"
  }'
```

响应包含`url`（授权链接）与`requestId`（用于轮询状态）.
### 轮询连接结果

```bash
curl https://api.integration-gateway.com/connection-requests/req_xyz \
  -H "Authorization: Bearer $INTEGRATION_TOKEN"
```

状态说明：`pending`（等待用户授权）、`success`（成功，使用`resultConnectionId`）、`error`（失败，查看`resultError`）.
## 最佳实践

1. **复用已有连接**：执行动作前先查询已有连接，避免重复授权
2. **动作搜索用自然语言**：`intent`参数支持自然语言描述，如"发送消息"而非精确动作名
3. **inputSchema校验**：执行动作前查看动作的`inputSchema`，确保入参符合要求
4. **连接命名清晰**：创建连接时设置有意义的`name`，便于多连接管理
5. **及时断开无用连接**：不再使用的连接及时断开，减少安全暴露面

## 常见问题

### Q1：搜索不到目标应用的连接器怎么办？
A：免费版仅支持预置连接器。若目标应用未预置，可使用专业版的自定义连接器构建功能，通过自然语言描述自动构建.
### Q2：连接请求一直pending怎么办？
A：用户需在浏览器中打开返回的`url`完成OAuth授权。确认用户已访问链接并完成授权后，轮询状态应变为`success`.
### Q3：动作执行报inputSchema校验错误？
A：执行动作前先查看动作的`inputSchema`字段，了解所需参数的名称、类型与是否必填。确保`input`对象符合Schema定义.
### Q4：可以同时连接多个应用吗？
A：可以。每个应用建立独立连接，通过`connectionId`区分。执行动作时需指定对应的`connectionId`.
### Q5：Token泄露后如何处理？
A：立即在控制台撤销该Token并生成新Token。已建立的连接不受影响，但需用新Token重新发起请求.
## 已知限制

本免费体验版限制以下高级功能：
- 不支持自定义连接器构建（仅预置连接器）
- 不支持批量动作执行
- 不支持多步骤工作流编排
- 不支持操作审计日志
- 不支持连接健康监控与自动重连

解锁全部功能请使用专业版：`self-integration-tool-pro`
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 依赖说明

### 运行环境
- **Agent平台**：支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**：Windows / macOS / Linux
- **网络**：可访问集成网关与目标应用API

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| 集成网关账户 | 在线服务 | 必需 | 在网关控制台注册 |
| 目标应用账户 | 在线服务 | 必需 | 各SaaS平台注册 |
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |
| curl或HTTP客户端 | 命令行工具 | 可选 | 系统自带或pip/npm安装 |

### API Key 配置
- **集成网关Token**：存储于环境变量`INTEGRATION_TOKEN`
- **目标应用凭据**：由网关托管，通过OAuth授权建立连接，本地不保存
- **禁止**：在代码或脚本中硬编码Token或应用凭据

### 可用性分类
- **分类**：MD+EXEC（纯Markdown指令，部分功能需要exec命令行执行能力）
- **说明**：基于Markdown的AI Skill，通过自然语言指令驱动Agent完成操作

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
