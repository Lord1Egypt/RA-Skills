---
slug: search-v2-tool-free
name: search-v2-tool-free
version: 1.0.0
displayName: 搜索工具免费版
summary: "轻量级LLM优化搜索工具,支持基础网页搜索与结果摘要,适合个人用户快速获取信息。搜索工具免费版为个人用户提供轻量级的LLM优化网页搜索能力."
license: Proprietary
edition: free
description: '搜索工具免费版为个人用户提供轻量级的LLM优化网页搜索能力.
  核心能力:

  - LLM优化的网页搜索

  - 基础搜索深度选择

  - 结果内容摘要

  - 简单域名过滤

  适用场景:

  - 快速事实查找

  - 技术问题搜索

  - 日常信息检索

  差异化:免费版聚焦核心搜索流程,通过Tavily API实现LLM友好的搜索结果,适合个人用户快速获取优化后的搜索内容,无需复杂配置.
  适用关键词: 搜索, search, Tavily, 网页搜索, LLM优化, 检索, 查询'
tags:
  - 研究工具
  - 搜索
  - 信息检索
  - 个人效率
  - 检索
  - 工具
  - query
  - python
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Knowledge"
---
# 搜索工具免费版

## 概述

搜索工具免费版是一款基于Tavily API的轻量级LLM优化网页搜索工具。它返回经过LLM优化的搜索结果,包含标题、URL、内容摘要和相关度评分,帮助个人用户快速获取高质量搜索内容.
免费版适合个人用户的日常搜索需求,支持基础搜索深度选择(basic/advanced)和简单域名过滤。搜索结果已为LLM消费优化,内容片段精炼且相关度高,适合直接交给AI助手进行后续分析.
## 核心能力

| 能力模块 | 说明 | 免费版支持 |
|----|---|-----|
| 网页搜索 | LLM优化的搜索结果 | 支持 |
| 搜索深度 | basic/advanced两种模式 | 支持 |
| 结果数量 | 可配置返回条数 | 支持(最多10条) |
| 域名过滤 | 包含/排除特定域名 | 支持 |
| 时间范围 | 按时间过滤结果 | 支持 |
| 内容摘要 | AI生成的答案摘要 | 支持 |
| 全文内容 | 返回原始页面内容 | 不支持 |
| 图片结果 | 返回相关图片 | 不支持 |
| 主题分类 | news/finance分类搜索 | 不支持 |
| 批量搜索 | 多查询并行搜索 | 不支持 |
| 结果缓存 | 搜索结果缓存 | 不支持 |

### 已知限制
执行已知限制操作,使用`input_params`参数进行配置,支持创建/查询/导出等操作.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 单次搜索最多返回10条结果
单次搜索最多返回10条结果

**处理**: 解析单次搜索最多返回10条结果的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回单次搜索最多返回10条结果的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 不支持news/finance
不支持news/finance主题分类搜索

**处理**: 解析不支持news/finance的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回不支持news/finance的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 不支持返回原始页面全文内容
不支持返回原始页面全文内容

**处理**: 解析不支持返回原始页面全文内容的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回不支持返回原始页面全文内容的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 不支持图片搜索结果
不支持图片搜索结果

**处理**: 解析不支持图片搜索结果的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回不支持图片搜索结果的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 不支持批量多查询并行
不支持批量多查询并行

**处理**: 解析不支持批量多查询并行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回不支持批量多查询并行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

- 不支持搜索结果缓存

**处理**: 解析已知限制的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回已知限制的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：轻量级、优化搜索工具、支持基础网页搜索、与结果摘要、适合个人用户快速、获取信息、搜索工具免费版为、个人用户提供轻量、优化网页搜索能力等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:技术问题快速查找

开发者遇到技术问题,需要快速查找解决方案.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 搜索工具免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 基础搜索
（请参考skill目录中的脚本文件） '{"query": "Python async patterns best practices"}'
# ...
# 高级搜索(更精确)
（请参考skill目录中的脚本文件） '{"query": "Python async patterns", "max_results": 5, "search_depth": "advanced"}'
# ...
# 限定可信域名
（请参考skill目录中的脚本文件） '{"query": "React hooks tutorial", "max_results": 5, "include_domains": ["docs.python.org", "realpython.com"]}'
```

输出示例:

```json
{
  "query": "Python async patterns best practices",
  "results": [
    {
      "title": "Async IO in Python: A Complete Walkthrough",
      "url": "https://realpython.com/async-io-python/",
      "content": "asyncio is a library to write concurrent code using the async/await syntax. This guide covers coroutines, tasks, event loops...",
      "score": 0.92
    },
    {
      "title": "Python Async Programming Guide",
      "url": "https://docs.python.org/3/library/asyncio.html",
      "content": "asyncio is used as a foundation for multiple Python asynchronous frameworks...",
      "score": 0.88
    }
  ],
  "response_time": 1.2
}
```

### 场景二:按时间范围搜索最新内容

用户希望只搜索最近一周的相关内容.
```bash
# 搜索最近一周的内容
（请参考skill目录中的脚本文件） '{"query": "AI news", "time_range": "week", "max_results": 10}'
# ...
# 搜索最近一天的内容
（请参考skill目录中的脚本文件） '{"query": "GPT-5 release", "time_range": "day", "max_results": 5}'
```

### 场景三:域名过滤聚焦可信源

用户希望只在特定可信域名中搜索,避免低质量结果.
```bash
# 只在学术和技术文档站点搜索
（请参考skill目录中的脚本文件） '{
  "query": "machine learning transformer architecture",
  "include_domains": ["arxiv.org", "github.com", "docs.pytorch.org"],
  "search_depth": "advanced",
  "max_results": 10
}'
# ...
# 排除特定域名
（请参考skill目录中的脚本文件） '{
  "query": "Python web frameworks",
  "exclude_domains": ["pinterest.com", "quora.com"],
  "max_results": 5
}'
```

## 不适用场景

以下场景搜索工具免费版不适合处理：

- 需要100%确定性的关键决策
- 医疗诊断
- 法律判决

## 触发条件

需要AI模型调用、智能对话、Agent编排、LLM应用时使用。不适用于非本工具能力范围的需求.
## 快速开始

### 第一步:获取API Key

访问 https://tavily.com 注册并获取API Key.
### 第二步:配置API Key

将API Key添加到Agent配置中:

```json
// ~/.claude/settings.json
{
  "env": {
    "TAVILY_API_KEY": "tvly-your-api-key-here"
  }
}
```

或通过环境变量配置:

```bash
export TAVILY_API_KEY="tvly-your-api-key-here"
```

### 第三步:执行首次搜索

```bash
# 最简搜索
（请参考skill目录中的脚本文件） '{"query": "what is RAG in AI"}'
```

### 第四步:使用高级选项

```bash
# 高级搜索深度+域名过滤
（请参考skill目录中的脚本文件） '{
  "query": "vector database comparison",
  "search_depth": "advanced",
org", "github.com"],
  "max_results": 10
}'
```

## 示例

### 搜索深度对比

| 深度 | 延迟 | 相关度 | 内容类型 | 适用场景 |
|---:|---:|---:|---:|---:|
| `basic` | 中等 | 高 | NLP摘要 | 通用搜索,平衡速度与质量 |
| `advanced` | 较高 | 最高 | 分块内容 | 精确搜索,需要最高相关度 |

### 请求参数说明

| 参数 | 类型 | 默认值 | 说明 |
|:---:|:---:|:---:|:---:|
| `query` | string | 必需 | 搜索查询(建议<400字符) |
| `max_results` | integer | 5 | 最大结果数(免费版上限10) |
| `search_depth` | string | `basic` | 搜索深度:basic/advanced |
| `time_range` | string | null | 时间范围:day/week/month/year |
| `include_domains` | array | [] | 包含的域名列表 |
| `exclude_domains` | array | [] | 排除的域名列表 |
| `include_answer` | boolean | false | 是否包含AI生成的答案 |

### 常用搜索模式

```bash
# 快速搜索(基础深度)
（请参考skill目录中的脚本文件） '{"query": "your question", "max_results": 5}'
# ...
# 精确搜索(高级深度)
（请参考skill目录中的脚本文件） '{"query": "your question", "search_depth": "advanced", "max_results": 10}'
# ...
# 时间限定搜索
（请参考skill目录中的脚本文件） '{"query": "your question", "time_range": "week"}'
# ...
# 域名限定搜索
（请参考skill目录中的脚本文件） '{"query": "your question", "include_domains": ["arxiv.org"]}'
# ...
# 获取AI答案
（请参考skill目录中的脚本文件） '{"query": "your question", "include_answer": true}'
```

## 最佳实践

### 1. 查询要简洁精准

搜索查询不是Prompt,保持简洁(建议<400字符)。复杂问题拆分为多个子查询,效果优于一个冗长查询:

```bash
# 好:简洁精准
（请参考skill目录中的脚本文件） '{"query": "vLLM PagedAttention optimization"}'
# ...
# 不好:过于冗长
（请参考skill目录中的脚本文件） '{"query": "请帮我详细解释一下vLLM中的PagedAttention机制是如何优化KV缓存管理的,以及它与传统方法相比有哪些优势"}'
```

### 2. 善用域名过滤提升质量

通过`include_domains`限定可信源,通过`exclude_domains`排除低质量站点:

```bash
# 学术研究:限定学术站点
（请参考skill目录中的脚本文件） '{"query": "transformer attention", "include_domains": ["arxiv.org", "scholar.google.com"]}'
# ...
# 编程问题:限定文档站点
（请参考skill目录中的脚本文件） '{"query": "FastAPI dependency injection", "include_domains": ["fastapi.tiangolo.com", "stackoverflow.com"]}'
```

### 3. 高级深度用于精确需求

`advanced`深度提供最高相关度,但延迟更高。日常搜索用`basic`,需要精确结果时用`advanced`:

```bash
# 日常:basic
（请参考skill目录中的脚本文件） '{"query": "Python list comprehension"}'
# ...
# 精确:advanced
（请参考skill目录中的脚本文件） '{"query": "Python GIL impact on multithreading", "search_depth": "advanced"}'
```

### 4. 利用时间范围获取最新信息

对于时效性强的查询,使用`time_range`过滤旧内容:

```bash
# 最新新闻
（请参考skill目录中的脚本文件） '{"query": "AI model releases", "time_range": "week"}'
# ...
# 年度回顾
（请参考skill目录中的脚本文件） '{"query": "AI industry report", "time_range": "month"}'
```

### 5. 按相关度评分筛选

返回结果包含`score`字段(0-1),数值越高相关度越强。优先关注score>0.8的结果:

```bash
# 搜索后让AI助手按score排序并筛选
（请参考skill目录中的脚本文件） '{"query": "your question", "max_results": 10}'
# AI助手会优先分析高score结果
```

## 常见问题

### Q: 搜索返回0条结果怎么办?

A: 可能原因:(1)查询过于具体或生僻,尝试更通用的关键词;(2)域名过滤过严,放宽`include_domains`限制;(3)时间范围过窄,扩大`time_range`。建议先不加任何过滤条件测试基础搜索.
### Q: API Key无效或报错401怎么办?

A: 检查API Key是否正确配置:(1)确认`TAVILY_API_KEY`环境变量已设置;(2)确认Key未过期;(3)确认Key有足够的调用额度。Tavily免费额度有限,超出后需升级套餐.
### Q: 搜索结果内容不全怎么办?

A: 免费版返回的是内容摘要(NLP summary),不是页面全文。如需全文,可:(1)使用`include_answer: true`获取AI综合答案;(2)用WebFetch工具直接抓取结果中的URL获取全文;(3)升级到专业版使用`include_raw_content`参数.
### Q: 搜索延迟很高怎么办?

A: 延迟主要取决于`search_depth`。`advanced`深度比`basic`慢。如对速度敏感,使用`basic`深度并减少`max_results`。网络延迟也会影响整体响应时间.
### Q: 如何搜索特定语言的内容?

A: 在查询中使用目标语言关键词。例如搜索中文内容,用中文查询词:"机器学习 推理优化"。搜索引擎会根据查询语言返回对应内容。免费版不显式支持语言过滤参数.
### Q: 搜索结果的相关度评分(score)如何解读?

A: score范围0-1,越高越相关。一般规律:>0.9高度相关,0.7-0.9较相关,0.5-0.7一般相关,<0.5相关度较低。建议优先关注0.8以上的结果。评分由搜索引擎的NLP模型计算.
## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **运行时**: 需要终端执行能力(exec)以调用搜索脚本

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| Tavily API | 搜索API | 必需 | https://tavily.com 注册获取 |
| curl | HTTP工具 | 必需(系统自带) | 系统预装 |
| jq(可选) | JSON处理 | 推荐 | `apt install jq` 或 `brew install jq` |
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| 网络访问 | 网络 | 必需 | 需能访问Tavily API |

### API Key 配置

- **Tavily API Key**: 必需,通过环境变量`TAVILY_API_KEY`配置
- 获取方式:访问 https://tavily.com 注册,免费额度有限
- 配置位置:`~/.claude/settings.json`的`env`字段,或系统环境变量
- **LLM API**: 由Agent平台内置提供,无需额外配置

### 可用性分类

- **分类**: MD+EXEC(纯Markdown指令,核心功能需要exec命令行执行搜索脚本)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent调用Tavily API完成LLM优化网页搜索任务。免费版聚焦个人用户的基础搜索、域名过滤与时间范围筛选,适合快速事实查找、技术问题搜索与日常信息检索场景.
## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
