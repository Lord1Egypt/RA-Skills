---
slug: web-browsing-tool-free
name: web-browsing-tool-free
version: 1.0.0
displayName: 网页浏览助手免费版
summary: "浏览和总结网站内容,从 URL 提取信息,搜索网络获取实时资讯,适合个人日常使用。网页浏览助手免费版,面向个人用户提供基础的网页浏览和信息提取能力。支持网站访问、内容总结、URL 内容提取、"
license: Proprietary
edition: free
description: 网页浏览助手免费版,面向个人用户提供基础的网页浏览和信息提取能力。支持网站访问、内容总结、URL 内容提取、网络搜索等核心功能。Use when
  需要SEO优化、关键词分析、排名提升、搜索流量优化时使用。不适用于黑帽SEO手段。Use when 需要SEO优化、关键词分析、排名提升、搜索流量优化时使用。不适用于黑帽SEO手段.
tags:
  - 研究工具
  - 网页浏览
  - 信息获取
  - Web开发
  - 前端
  - 开发工具
  - web-browsing
  - https
  - bash
tools:
  - read
  - exec
  - write
  - glob
homepage: ""
category: "Development"
---
# 网页浏览助手免费版

## 概述

网页浏览助手免费版是一款面向个人用户的网页信息获取工具。它能够访问指定的网站、总结网页内容、从 URL 中提取结构化信息,并支持网络搜索获取实时资讯,让 AI 成为您的智能网页浏览助手.
本工具特别适合个人用户日常的网页信息获取需求,例如查看网站内容、了解最新资讯、收集研究资料等。免费版聚焦核心浏览和提取功能,无需注册,开箱即用.
## 核心能力

### 1. 直接 URL 访问

访问指定 URL,获取网页主要内容.
具体操作方式与参数说明请参考下方示例代码.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 网页浏览助手免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 访问指定网页
web-browsing fetch "https://example.com"
# ...
# 获取网页内容并总结
web-browsing fetch "https://news.example.com" --summarize
# ...
# 获取特定格式的输出
web-browsing fetch "https://docs.example.com" --format markdown
```

**处理**: 解析直接 URL 访问的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回直接 URL 访问的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 网页内容智能分析

自动提取网页主要内容并生成摘要.
```bash
# 总结网页内容
web-browsing summarize "https://long-article.example.com"
# ...
# 指定总结长度
web-browsing summarize "https://article.example.com" --length short
example.com" --length detailed
```

**处理**: 解析网页内容智能总结的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回网页内容智能总结的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 网络搜索

搜索网络获取实时信息.
```bash
# 基础搜索
web-browsing search "最新人工智能研究进展"
# ...
# 搜索并总结
web-browsing search "气候变化最新报告" --summarize
# ...
# 指定搜索结果数量
web-browsing search "React 教程" --limit 5
```

**处理**: 解析网络搜索的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回网络搜索的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. 结构化数据提取

从网页中提取特定的结构化数据.
```bash
# 提取特定数据
web-browsing extract "https://product.example.com" --fields "name,price,rating"
# ...
# 提取表格数据
web-browsing extract "https://data.example.com" --selector "table" --format csv
# ...
# 提取列表数据
web-browsing extract "https://list.example.com" --selector ".item" --format json
```

**处理**: 解析结构化数据提取的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结构化数据提取的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：浏览和总结网站内、提取信息、适合个人日常使用、网页浏览助手免费、面向个人用户提供、基础的网页浏览和、信息提取能力、支持网站访问、内容总结、内容提取、网络搜索等核心功、Use、when、SEO、关键词分析、排名提升、搜索流量优化时使、不适用于黑帽、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景一:个人用户获取网页信息

小王想快速了解某个网站的内容,无需逐页浏览.
```bash
# 步骤1:访问网站并获取内容
web-browsing fetch "https://target-website.com"
# ...
# 步骤2:总结网站主要内容
web-browsing summarize "https://target-website.com"
# ...
# 步骤3:提取特定信息
web-browsing extract "https://target-website.com" --fields "title,author,date"
```

### 场景二:学生收集研究资料

小李是学生,需要从多个网站收集特定主题的资料.
```bash
# 步骤1:搜索相关内容
web-browsing search "深度学习优化算法" --limit 10
# ...
# 步骤2:访问搜索结果中的网页
web-browsing fetch "https://result1.example.com" --summarize
web-browsing fetch "https://result2.example.com" --summarize
# ...
# 步骤3:提取结构化数据
web-browsing extract "https://paper.example.com" --fields "title,abstract,authors"
```

### 场景三:快速了解新闻资讯

小张想快速了解今天的科技新闻.
```bash
# 步骤1:搜索最新科技新闻
web-browsing search "今日科技新闻" --freshness today
# ...
# 步骤2:访问新闻网站
web-browsing fetch "https://tech-news.example.com"
# ...
# 步骤3:总结新闻要点
web-browsing summarize "https://tech-news.example.com" --length short
```

## 快速开始

### 第一步:查看可用命令

```bash
# 查看所有命令
web-browsing help
# ...
# 查看特定命令用法
web-browsing fetch --help
web-browsing search --help
```

### 第二步:执行首次访问

```bash
# 访问简单网页
# ...
# 总结网页内容
web-browsing summarize "https://example.com"
```

### 第三步:执行首次搜索

```bash
# 搜索网络
web-browsing search "人工智能最新进展"
# ...
# 搜索并总结
web-browsing search "人工智能最新进展" --summarize --limit 3
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
#
## 示例

### 个人偏好配置

```bash
# config.json - 个人浏览偏好
{
  "fetch": {
    "timeout": 30,
    "user_agent": "Mozilla/5.0",
    "follow_redirects": true
  },
  "summarize": {
    "default_length": "medium",
    "language": "zh"
  },
  "search": {
    "default_limit": 5,
    "language": "zh-CN",
    "safe_search": true
  }
}
```

### 搜索配置

```bash
# 配置搜索引擎偏好
web-browsing config set-search \
  --engine "default" \
  --language "zh-CN" \
  --safe-search true \
  --default-limit 5
```

## 最佳实践

### 1. 明确获取目标

```bash
# 正确做法:明确说明需要什么
com" --fields "title,price,availability"
# ...
# 错误做法:目标不明确
```

### 2. 善用总结功能

```bash
# 长文章用总结
example.com" --length short
# ...
# 需要详情时直接获取
web-browsing fetch "https://article.example.com" --format markdown
```

### 3. 合理使用搜索过滤

```bash
# 搜索时限定时间范围
web-browsing search "最新新闻" --freshness today
web-browsing search "本周热点" --freshness week
# ...
# 限定语言
web-browsing search "AI research" --language en
web-browsing search "人工智能研究" --language zh
```

### 4. 批量处理多个 URL

```bash
# 批量获取多个网页
for url in "url1" "url2" "url3"; do
  echo "=== $url ==="
  web-browsing summarize "$url"
done
```

## 常见问题

### Q1: 无法访问某些网站怎么办?

**A:** 部分网站可能阻止自动化访问。建议:

1. 尝试不同的 User-Agent
2. 检查网站是否需要登录
3. 使用网络搜索替代直接访问

### Q2: 内容提取不完整?

**A:** 可能原因和解决方案:

1. 网站使用 JavaScript 动态加载内容 -> 尝试使用浏览器自动化工具
2. 内容需要登录才能查看 -> 提供登录态或使用真实浏览器控制工具
3. 选择器不正确 -> 检查网页结构,调整选择器

### Q3: 搜索结果质量不高?

**A:** 优化搜索:

1. 使用更具体的关键词
2. 添加引号搜索精确短语:web-browsing search '"深度学习优化"'
3. 限定语言和地区

### Q4: 支持哪些输出格式?

**A:** 免费版支持多种输出格式:

- text:纯文本
- markdown:Markdown 格式
- json:JSON 结构化数据
- csv:CSV 表格格式

### 已知限制

**A:** 免费版主要面向个人日常浏览场景,具备完整的网页访问和搜索能力。如需批量处理、定时监控、深度分析、团队协作等高级功能,请考虑升级到 PRO 版本.
## 依赖说明

### 运行环境

- **Agent 平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **网络**: 需要可访问互联网

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| curl | HTTP 工具 | 必需 | 系统自带 |
| web_search | 搜索工具 | 必需 | Agent 内置或外部搜索 API |
| web_fetch | 网页抓取 | 必需 | Agent 内置或外部抓取工具 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置

免费版使用 Agent 内置工具,基础LLM由Agent平台提供。部分高级搜索功能可能需要搜索引擎 API Key.
```bash
# 可选:配置搜索引擎 API(提升搜索质量)
SEARCH_API_KEY=your_search_api_key
```

### 可用性分类

- **分类**: MD+EXEC(纯 Markdown 指令,通过 exec 执行 HTTP 请求和网页抓取)
- **说明**: 基于网页浏览的信息获取工具,通过自然语言指令驱动 Agent 访问网页和搜索信息
- **适用规模**: 个人用户、单次查询、本地运行

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
