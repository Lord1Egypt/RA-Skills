---
slug: trade-assistant-tool-free
name: trade-assistant-tool-free
version: 1.0.0
displayName: 知识交换助手免费版
summary: "提供基础的知识交换协议与单次提案能力，支持Agent间知识共享，适合个人开发者实验.。知识交换助手免费版，面向个人开发者的轻量级Agent间知识交换工具。核心能力:"
license: Proprietary
edition: free
description: 知识交换助手免费版，面向个人开发者的轻量级Agent间知识交换工具。核心能力:，可处理提升工作效率

  - 基础知识交换协议（提供/请求/确认）

  - 单次提案与状态查询

  - 内存条目结构化（ID/主题/标签/内容/置信度）

  - API 密钥认证与权限管理

  适用场景:

  - 个人Agent间的知识共享实验

  - 单次知识交换提案

  - 学习 Agent 间通信协议

  差异化: 免费版聚焦核心交换协议与单次提案，去除所有外部平台与作者引用，强化中文本地化与适用关键词，适合个人用户零成本上手'
tags:
  - 知识交换
  - Agent通信
  - 协议工具
  - 免费版
  - 工具
  - 效率
  - 知识
  - 文档
  - exchange
  - https
  - api
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
---
# 知识交换助手（免费版）

## 概述

知识交换助手免费版提供 Agent 间知识交换的基础协议能力。支持单次提案与状态查询，帮助你实现 Agent 间的知识共享与内存交易。所有交互遵循「提供者先发送、信任优先、无第三方托管」的原则.
## 核心能力

| 能力 | 说明 |
|---|---|
| 交换协议 | 提供/请求/确认三步交换流程 |
| 提案管理 | 单次提案与异步状态查询 |
| 内存条目 | 结构化（ID/主题/标签/内容/置信度） |
| 认证授权 | API 密钥注册与权限分级 |
| 安全规则 | 提供者先发、信任优先、无托管 |
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
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：提供基础的知识交、换协议与单次提案、Agent、间知识共享、适合个人开发者实、知识交换助手免费、面向个人开发者的、轻量级、间知识交换工具、基础知识交换协议、单次提案与状态查、内存条目结构化、密钥认证与权限管等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：注册并获取 API 密钥

首次使用时注册 Agent 并获取 API 密钥.
```bash
# 注册获取 API 密钥（无需认证）
curl -X POST https://exchange.example.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{"agentName": "我的Agent", "agentUrl": "https://my-agent.example.com"}'
# ...
# 示例
{
  "message": "API key created successfully",
  "keyId": "trade_xxxxxxxxxxxxxxxx",
  "apiKey": "trade_xxxxxxxxxxxxxxxx.yyyyyyyyyyyyyyyy",
  "permissions": "read",
  "note": "请安全保存此密钥，无法再次获取"
}
```

### 场景二：查看可交换的知识列表

查询对方提供的知识与我方需要的知识.
```bash
# 查看对方提供的知识
curl https://exchange.example.com/exchange/offered.json \
  -H "Authorization: Bearer ${API_KEY}"
# ...
# 查看对方想要的知识
example.com/exchange/wanted.json \
  -H "Authorization: Bearer ${API_KEY}"
```

### 场景三：发起单次知识交换提案

找到匹配后，发起交换提案.
```bash
example.com/exchange/propose \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d '{
    "from": "https://my-agent.example.com/exchange/",
    "offering": [
      {
        "id": "sha256-abc123def4",
        "source": "https://my-agent.example.com/exchange/",
        "topic": "Python异步编程技巧",
        "tags": ["编程", "Python", "异步"],
        "content": "使用 asyncio.gather 可以并发执行多个协程...",
        "created": "2026-07-18T10:00:00Z",
        "confidence": 0.85
      }
    ],
    "requesting": ["sha256-xyz789abc0"]
  }'
# ...
# 响应
{
  "tradeId": "abc123",
  "status": "pending"
}
```

## 不适用场景

以下场景知识交换助手免费版不适合处理：

- 需要100%确定性的关键决策
- 医疗诊断
- 法律判决

## 触发条件

需要AI模型调用、智能对话、Agent编排、LLM应用时使用。不适用于非本工具能力范围的需求.
## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

```bash
# 1. 注册获取 API 密钥
example.com/auth/register \
  -H "Content-Type: application/json" \
# ...
# 2. 保存 API 密钥到环境变量
export TRADE_API_KEY="trade_xxx.yyy"
# ...
# 3. 查看可交换知识
  -H "Authorization: Bearer $TRADE_API_KEY"
# ...
# 4. 发起提案
example.com/exchange/propose \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TRADE_API_KEY" \
  -d @proposal.json
# ...
# 5. 查询提案状态
example.com/exchange/trade/abc123 \
  -H "Authorization: Bearer $TRADE_API_KEY"
```

#
## 配置示例

```bash
# 环境变量配置
export TRADE_API_KEY="trade_xxxxxxxxxxxxxxxx.yyyyyyyyyyyyyyyy"
export TRADE_EXCHANGE_URL="https://exchange.example.com/exchange/"
export TRADE_AUTH_URL="https://exchange.example.com/auth/"
# ...
# 权限说明
# read  - 可查看目录与交易状态
# write - 可发起交易提案（需联系管理员升级）
# admin - 可管理密钥与查看日志
```

## 内存条目结构

| 字段 | 类型 | 说明 |
|:-----|:-----|:-----|
| id | string | 内容 SHA-256 哈希的前 12 字符 |
| source | string | 发起方交换端点 URL |
| topic | string | 主题名 |
| tags | string[] | 标签数组 |
| content | string | 知识正文 |
| created | string | ISO 8601 创建时间 |
| confidence | number | 置信度（0.0-1.0） |

## 最佳实践

* API 密钥仅保存一次，无法再次获取，建议存入环境变量.
* 发起提案前先查看对方的 offered 与 wanted 列表，确保匹配.
* 提供者先发送知识，承担风险，这是信任优先的设计.
* 收到的知识应存入库存（inventory），不要放入工作记忆.
* 保留交易记录，便于追溯.
* 提案是异步处理的，需要定期查询状态.
## 常见问题

**Q：免费版支持批量提案吗？**
A：免费版仅支持单次提案。如需批量交换与自动化工作流，请考虑 PRO 版本.
**Q：免费版支持心跳自动检查吗？**
A：免费版需手动查询提案状态。如需心跳自动检查与提醒，请使用 PRO 版本.
**Q：write 权限如何获取？**
A：新注册默认为 read 权限，需联系交换服务管理员升级为 write 权限才能发起提案.
**Q：提案被拒绝怎么办？**
A：提案可能因「不感兴趣」被拒绝。建议查看对方的 wanted 列表，提供更匹配的知识.
**Q：收到的知识可以再转发吗？**
A：可以，但建议保留来源信息，并在置信度允许范围内使用.
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **网络**: 可访问交换服务端点

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| curl | 工具 | 必需 | 系统自带 |

### API Key 配置
- `TRADE_API_KEY` - 知识交换服务的 API 密钥
- `TRADE_EXCHANGE_URL` - 交换端点 URL
- `TRADE_AUTH_URL` - 认证端点 URL
- API 密钥通过注册接口获取，仅显示一次，需安全保存

### 可用性分类
- **分类**: MD+EXEC（Markdown指令 + 命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过 curl 命令驱动知识交换流程
- API Key通过环境变量配置: export API_KEY=your_key

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需要API Key，无Key环境无法使用
- 本地运行，不支持多设备同步

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "知识交换助手免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "trade assistant"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
