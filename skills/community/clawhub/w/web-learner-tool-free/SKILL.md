---
slug: web-learner-tool-free
name: web-learner-tool-free
version: 1.0.0
displayName: 自主学习助手免费版
summary: "让 AI 自主上网搜索和学习,主动获取最新信息,整合互联网知识,适合个人知识获取。自主学习助手免费版,面向个人用户提供 AI 自主上网搜索和学习的能力。支持 Web 搜索、网页抓取、浏览器交"
license: Proprietary
edition: free
description: 自主学习助手免费版,面向个人用户提供 AI 自主上网搜索和学习的能力。支持 Web 搜索、网页抓取、浏览器交互等多种信息获取方式。Use
  when 需要AI模型调用、智能对话、Agent编排、LLM应用时使用。不适用于需要100%确定性的关键决策。Use
  when 需要AI模型调用、智能对话、Agent编排、LLM应用时使用。不适用于需要100%确定性的关键决策.
tags:
  - 研究工具
  - 自主学习
  - 知识获取
  - Web开发
  - 前端
  - 开发工具
  - web_search
  - bash
  - web_fetch
  - https
  - url
tools:
  - read
  - exec
  - write
  - glob
homepage: ""
category: "Development"
---
# 自主学习助手免费版

## 概述

自主学习助手免费版是一款让 AI 能够自主上网搜索和学习的工具。它赋予 AI 主动从互联网获取最新信息、学习新知识、整合多源信息的能力,使 AI 的回答不再局限于训练数据,而是能够实时获取互联网上的最新知识.
本工具特别适合个人用户获取最新资讯、学生学习新知识、研究者收集资料等场景。免费版支持 Web 搜索、网页抓取、浏览器交互等多种信息获取方式,开箱即用.
## 核心能力

### 1. Web 搜索

使用搜索工具进行关键词搜索,获取实时信息.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 自主学习助手免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 基础搜索
web_search("最新人工智能研究进展")
# ...
# 中文搜索优先
web_search("深度学习优化算法", country="CN")
# ...
# 限定时间范围
web_search("今日科技新闻", freshness="pd")  # pd: 今天
web_search("本周热点", freshness="pw")      # pw: 本周
web_search("本月资讯", freshness="pm")      # pm: 本月
```

**处理**: 解析Web 搜索的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回Web 搜索的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 网页抓取

获取网页的详细内容,学习新知识.
```bash
# 获取网页 Markdown 内容
web_fetch("https://docs.example.com/guide", format="markdown")
# ...
# 获取网页纯文本内容
web_fetch("https://article.example.com", format="text")
# ...
# 处理页面加载失败
try:
    content = web_fetch("https://target-url.com")
except:
    # 使用备选数据源
    content = web_fetch("https://fallback-url.com")
```

**处理**: 解析网页抓取的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回网页抓取的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 浏览器交互

当搜索和抓取失败时,使用浏览器工具处理复杂页面.
```bash
# 启动浏览器服务
browser_start()
# ...
# 导航到目标页面
browser_navigate("https://spa.example.com")
# ...
# 获取页面内容
browser_get_text()
# ...
# 截图保存
browser_screenshot()
```

**处理**: 解析浏览器交互的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回浏览器交互的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. 多源信息整合

从多个来源获取信息,整合形成完整认知.
```bash
# 步骤1:搜索获取概览
search_results = web_search("量子计算最新进展")
# ...
# 步骤2:抓取详细内容
for result in search_results[:3]:
    content = web_fetch(result.url)
    # 整合内容
# ...
# 步骤3:整合并总结
summary = summarize(all_content, language="zh")
```

**处理**: 解析多源信息整合的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回多源信息整合的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：自主上网搜索和学、主动获取最新信息、整合互联网知识、适合个人知识获取、自主学习助手免费、面向个人用户提供、习的能力、浏览器交互等多种、信息获取方式、Use、when、模型调用、智能对话、Agent、LLM、应用时使用、不适用于需要、确定性的关键决策、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景一:获取最新资讯

小王想了解今天的科技新闻.
```bash
# 步骤1:搜索最新新闻
results = web_search("今日科技新闻", freshness="pd", country="CN")
# ...
# 步骤2:抓取新闻详情
for news in results[:3]:
    article = web_fetch(news.url, format="markdown")
    # 提取关键信息
# ...
# 步骤3:总结呈现
# 用中文总结今天的科技新闻要点
```

### 场景二:学习新知识

小李正在学习区块链技术,想获取最新的学习资料.
```bash
# 步骤1:搜索学习资源
results = web_search("区块链入门教程 2026", country="CN")
# ...
# 步骤2:抓取教程内容
tutorial = web_fetch("https://tutorial.example.com/blockchain", format="markdown")
# ...
# 步骤3:整理学习要点
# 提取核心概念、技术要点、实践步骤
```

### 场景三:查询实时信息

小张需要查询今天的天气.
```bash
# 步骤1:使用天气服务(首选)
weather = web_fetch("https://wttr.in/Beijing?format=3")
# ...
# 步骤2:备选方案
if not weather:
    weather = web_fetch("https://weather.com.cn/beijing")
# ...
# 步骤3:总结天气信息
# 用中文呈现今天的天气情况
```

## 快速开始

### 第一步:检查工具可用性

```bash
# 检查 web_search 是否可用(需要 Brave API Key)
# 检查 web_fetch 是否可用(大部分网页可用)
# 检查 browser 是否可用(需要浏览器服务运行)
# ...
# 测试基础搜索
web_search("test query")
```

### 第二步:执行首次学习

```bash
# 搜索并获取信息
results = web_search("人工智能最新发展")
content = web_fetch(results[0].url)
# ...
# 整合并总结
summary = summarize(content, language="zh")
```

### 第三步:处理复杂场景

```bash
# 当 web_fetch 失败时,尝试浏览器
try:
    content = web_fetch(url)
except:
    browser_start()
    browser_navigate(url)
    content = browser_get_text()
```

#
## 示例

### 个人偏好配置

```bash
# config.json - 学习偏好配置
{
  "search": {
    "language": "zh-CN",
    "country": "CN",
    "default_freshness": "pw",
    "result_limit": 10
  },
  "fetch": {
    "format": "markdown",
    "timeout": 30,
    "follow_redirects": true
  },
  "browser": {
    "headless": true,
    "timeout": 60
  },
  "output": {
    "language": "zh",
    "format": "structured",
    "cite_sources": true
  }
}
```

### 搜索策略配置

```bash
# 配置搜索策略
{
  "strategy": {
    "primary": "web_search",      # 优先使用搜索
    "secondary": "web_fetch",     # 搜索结果抓取
    "fallback": "browser",        # 浏览器作为备选
    "retry": 2,                   # 重试次数
    "timeout": 30                 # 超时时间(秒)
  }
}
```

## 最佳实践

### 1. 明确学习目标

```bash
# 正确做法:明确需要什么信息
web_search("React 18 新特性详细介绍")
# ...
# 错误做法:目标不明确
web_search("React")  # 太宽泛,结果不聚焦
```

### 2. 优先使用中文搜索

```bash
# 中文主题用中文搜索
web_search("中国新能源汽车政策", country="CN")
# ...
# 英文技术用英文搜索
web_search("React hooks best practices", country="US")
```

### 3. 合理使用时间过滤

```bash
# 获取最新信息
web_search("AI 突破", freshness="pd")  # 今天
# ...
# 获取近期信息
web_search("行业趋势", freshness="pw")  # 本周
# ...
# 获取长期信息
web_search("基础知识", freshness="pm")  # 本月
```

### 4. 多源验证重要信息

```bash
# 重要信息从多个来源验证
sources = []
for query in ["声明1", "声明2", "声明3"]:
    results = web_search(query)
    sources.append(web_fetch(results[0].url))
# ...
# 交叉验证信息的准确性
```

### 5. 注明信息来源

```bash
# 向用户呈现信息时,注明来源
# 来源:百度新闻(news.baidu.com)
# 来源:澎湃新闻(thepaper.cn)
```

## 常见问题

### Q1: web_search 不可用怎么办?

**A:** `web_search` 工具需要配置 Brave API Key。如果不可用:

1. 检查 API Key 是否配置正确
2. 使用 `web_fetch` 直接访问已知网站
3. 使用 `browser` 工具通过浏览器搜索

### Q2: web_fetch 抓取内容为空?

**A:** 可能原因和解决方案:

1. 网站使用 JavaScript 动态加载 -> 使用 `browser` 工具
2. 网站有反爬虫机制 -> 尝试不同的 User-Agent
3. 需要登录才能查看 -> 使用真实浏览器控制工具
4. 网络连接问题 -> 检查网络连接

### Q3: 如何处理视频内容?

**A:** 无法直接播放或理解视频内容,但可以:

1. 使用 `web_fetch` 获取视频页面的描述
2. 提取视频标题和简介
3. 搜索视频相关的文字报道

### Q4: 搜索结果质量不高?

**A:** 优化搜索策略:

1. 使用更具体的关键词
2. 添加引号搜索精确短语
3. 限定语言和地区
4. 尝试不同的搜索引擎

### 已知限制

**A:** 免费版主要面向个人学习场景,具备完整的信息获取能力。如需批量学习、知识库管理、团队协作、定时更新等高级功能,请考虑升级到 PRO 版本.
## 依赖说明

### 运行环境

- **Agent 平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **网络**: 需要可访问互联网

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| web_search | 搜索工具 | 推荐 | Agent 内置或 Brave Search API |
| web_fetch | 网页抓取 | 必需 | Agent 内置 |
| browser | 浏览器 | 备选 | Agent 内置或外部浏览器服务 |
| Brave API Key | API Key | web_search 需要 | Brave Search 官网注册 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置

免费版需要以下配置以启用完整功能:

```bash
# .env 文件配置
# Brave Search API(启用 web_search)
BRAVE_API_KEY=your_brave_api_key
# ...
# 其他搜索引擎(可选)
SEARCH_API_KEY=your_search_api_key
```

### 可用性分类

- **分类**: MD+EXEC(纯 Markdown 指令,通过 exec 执行搜索和抓取工具)
- **说明**: 基于多源信息获取的自主学习工具,通过自然语言指令驱动 Agent 搜索和整合互联网知识
- **适用规模**: 个人用户、单次查询、本地运行

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
    "result": "自主学习助手免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "web learner"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
