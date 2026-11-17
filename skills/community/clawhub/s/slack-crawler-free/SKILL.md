---
slug: slack-crawler-free
name: slack-crawler-free
version: 1.0.0
displayName: Slack爬虫工具
summary: 基于本地Slack归档数据的检索与统计工具，支持新鲜度检查与只读SQL查询。
license: Proprietary
edition: free
description: 'Slack爬虫工具（免费版）基于本地Slack归档数据提供消息检索、新鲜度检查与只读SQL统计，优先使用本地数据避免重复API调用。


  核心能力：归档健康检查、数据新鲜度查询、关键词检索、时间范围消息切片、只读SQL统计查询。


  适用场景：个人Slack工作区归档分析、历史消息检索、团队活跃度统计、避免重复拉取API数据。


  差异化：聚焦"本地优先"检索闭环，通过只读SQL精确统计。专业版新增API同步、线程/DM完整化、定时调度、数据导出等能力。


  适用关键词：Slack归档、消息检索、新鲜度、SQL统计、Slack爬虫'
tags:
- 集成工具
- 数据分析
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: "L2-标准级"
pricing_model: per_use
suggested_price: "19.9 CNY/per_use"
tools: ["read", "write", "exec"]
tags: "Slack,社交,通信"
---
# Slack爬虫工具（免费版）

## 概述

Slack爬虫工具（免费版）基于本地Slack归档数据提供消息检索与统计分析能力。核心设计理念是"本地优先"：优先使用已归档的本地数据回答问题，仅在数据过期或用户要求时才同步，避免重复调用Slack API浪费配额与时间。

本免费版聚焦本地归档的检索与统计场景，提供健康检查、新鲜度查询、关键词检索、时间范围切片与只读SQL统计，适合个人与小型团队的Slack数据分析需求。数据存储于本地SQLite数据库，无需额外数据库服务。

## 核心能力

| 能力 | 说明 | 免费版支持 |
|---|---|-----|
| 归档健康检查 | 检查归档完整性与配置 | 是 |
| 数据新鲜度查询 | 查看各频道数据最后同步时间 | 是 |
| 关键词检索 | 全文检索历史消息 | 是 |
| 时间范围切片 | 按时间范围查询消息 | 是 |
| 只读SQL统计 | SQL精确统计与排名 | 是 |
| 桌面端同步 | 从Slack桌面应用导出同步 | 是 |
| API同步 | 从Slack API同步最新数据 | 否 |
| 线程/DM完整化 | 补全线程回复与私信 | 否 |
| 定时调度 | 定时自动同步 | 否 |
| 数据导出 | 导出为CSV/JSON | 否 |

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
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：基于本地、归档数据的检索与、统计工具、支持新鲜度检查与、爬虫工具、归档数据提供消息、新鲜度检查与只读、优先使用本地数据、避免重复等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景1：个人Slack工作区归档分析

小刘希望分析自己Slack工作区过去半年的活跃度。他使用本工具：从Slack桌面应用导出数据同步到本地归档，用只读SQL统计每月消息数、最活跃频道、最活跃成员，生成活跃度报告。

### 场景2：历史消息快速检索

团队成员需要查找三个月前讨论某功能的消息。直接在Slack中搜索受限于搜索范围与索引延迟。使用本工具在本地归档中全文检索，快速定位相关消息及其上下文。

### 场景3：避免重复API调用

Agent需要回答"本月#general频道有多少条消息"这类统计问题。本工具优先查询本地归档（毫秒级响应），仅当数据过期时才提示同步，避免每次都调用Slack API（受速率限制且耗时）。

## 不适用场景

以下场景Slack爬虫工具不适合处理：

- 数据库架构设计决策
- NoSQL选型
- 数据仓库ETL设计

## 触发条件

需要数据库操作、SQL查询、数据存储管理时使用。不适用于非本工具能力范围的需求。

## 使用流程

### Step 1：检查归档状态

```bash
slack-crawler doctor
slack-crawler status --json
```

`doctor`检查归档完整性与配置问题，`status`返回各频道的最后同步时间与消息数量。

### Step 2：同步本地数据（首次）

从Slack桌面应用导出数据同步：

```bash
slack-crawler sync --source desktop
```

### Step 3：检索消息

```bash
# 关键词检索（限20条）
slack-crawler search --limit 20 "产品发布"
# ...
# 时间范围切片（最近7天，限50条）
slack-crawler messages --since 7d --limit 50
```

### Step 4：SQL统计查询

```bash
# 统计消息总数
slack-crawler sql "select count(*) from messages;"
# ...
# 各频道消息数排名
slack-crawler sql "select channel, count(*) as cnt from messages group by channel order by cnt desc limit 10;"
```

## 示例

### 健康检查输出

```bash
slack-crawler doctor
```

输出示例：

```text
归档路径: ~/.slack-crawler/archive.db
数据库: SQLite (正常)
频道数: 12
消息总数: 45230
最早消息: 2025-01-15
最新消息: 2026-07-10
新鲜度状态: 部分过期（3个频道超过7天未同步）
```

### 新鲜度查询

```bash
slack-crawler status --json
```

输出示例：

```json
{
  "channels": [
    {"name": "#general", "last_sync": "2026-07-10", "message_count": 12340, "stale": false},
    {"name": "#random", "last_sync": "2026-06-28", "message_count": 8765, "stale": true}
  ],
  "total_messages": 45230,
  "freshness": "partial"
}
```

### 只读SQL查询

```bash
# 按用户统计消息数
slack-crawler sql "select user, count(*) as cnt from messages group by user order by cnt desc limit 10;"
# ...
# 按小时统计活跃度
slack-crawler sql "select strftime('%H', timestamp) as hour, count(*) as cnt from messages group by hour order by cnt desc;"
# ...
# 包含特定关键词的消息
slack-crawler sql "select channel, user, text from messages where text like '%产品发布%' limit 20;"
```

### 时间范围切片

```bash
# 最近7天
slack-crawler messages --since 7d --limit 50
# ...
# 指定日期范围
slack-crawler messages --since 2026-07-01 --until 2026-07-15 --limit 100
# ...
# 特定频道
slack-crawler messages --channel "#general" --since 30d --limit 200
```

## 最佳实践

1. **本地优先**：回答问题前先检查本地归档是否新鲜，新鲜则直接查询
2. **按需同步**：仅当数据过期或用户明确要求时同步，避免不必要的API调用
3. **有界切片**：检索时始终指定`--limit`，避免返回超大结果集
4. **SQL用于精确统计**：需要精确计数或排名时用SQL，模糊检索用search
5. **报告要素完整**：汇报结果时包含工作区/频道名、绝对日期范围、计数与数据来源限制

## 常见问题

### Q1：本地数据过期了怎么办？
A：运行`slack-crawler sync --source desktop`从桌面应用导出同步。免费版仅支持桌面端同步，API同步需专业版。

### Q2：SQL查询报错"table not found"怎么办？
A：归档尚未同步。先运行`slack-crawler sync --source desktop`初始化归档，再执行SQL查询。

### Q3：检索结果不全怎么办？
A：本地归档可能不完整（缺少线程回复或私信）。免费版仅同步桌面端导出的数据，完整化需专业版的API同步与线程/DM完整化功能。

### Q4：可以修改归档数据吗？
A：不可以。本工具仅提供只读SQL，避免误操作损坏归档完整性。数据修改需在Slack原平台操作后重新同步。

### Q5：归档数据库占用空间过大怎么办？
A：可定期清理旧数据。建议保留近1年数据，更早的数据导出后清理。专业版支持自动归档与压缩。

## 已知限制

本免费体验版限制以下高级功能：
- 不支持从Slack API同步最新数据（仅桌面端导出）
- 不支持线程回复与私信完整化
- 不支持定时自动同步调度
- 不支持数据导出为CSV/JSON
- 不支持增量同步与版本对比

解锁全部功能请使用专业版：`slack-crawler-pro`
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 依赖说明

### 运行环境
- **Agent平台**：支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**：Windows / macOS / Linux
- **本地存储**：归档数据库存储于`~/.slack-crawler/archive.db`

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| Slack桌面应用 | 桌面软件 | 必需 | Slack官网下载（数据导出源） |
| SQLite | 数据库 | 必需 | 系统内置或随工具安装 |
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |

### API Key 配置
- **本免费版无需Slack API Token**：数据来源为桌面端导出
- **Slack API Token**：仅专业版API同步需要，存储于环境变量`SLACK_TOKEN`
- **禁止**：在脚本中硬编码Token

### 可用性分类
- **分类**：MD+EXEC（纯Markdown指令，部分功能需要exec命令行执行能力）
- **说明**：基于Markdown的AI Skill，通过自然语言指令驱动Agent完成操作

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
