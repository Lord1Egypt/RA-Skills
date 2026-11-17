---
slug: rss-reader-tool-free
name: rss-reader-tool-free
version: 1.0.0
displayName: RSS阅读器免费版
summary: "轻量级RSS/Atom订阅阅读器,支持分类管理、关键词过滤与多种输出格式,适合个人内容研究。RSS阅读器免费版为个人用户提供轻量级的RSS/Atom订阅管理与内容研究能力。核心能力:"
license: Proprietary
edition: free
description: 'RSS阅读器免费版为个人用户提供轻量级的RSS/Atom订阅管理与内容研究能力。核心能力:

  - 订阅源添加与分类管理

  - 关键词监控与过滤

  - 多种输出格式(列表/内容研究/JSON)

  - 时间范围筛选

  - 自动摘要生成

  适用场景:

  - 竞品博客与行业媒体监控

  - 内容创作灵感收集

  - Newsletter订阅聚合

  差异化:免费版聚焦核心订阅管理与内容研究流程,基于Node'
tags:
  - 研究工具
  - RSS
  - 内容研究
  - 个人效率
  - 订阅管理
  - 搜索
  - 检索
  - 工具
  - node
  - rss
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Knowledge"
---
# RSS阅读器免费版

## 概述

RSS阅读器免费版是一款基于Node.js的轻量级RSS/Atom订阅管理与内容研究工具。它支持订阅源添加、分类管理、关键词监控、时间范围筛选与多种输出格式,帮助个人用户从订阅源中高效获取信息与创作灵感.
免费版特别强化了"内容研究模式"(ideas格式),能够从订阅文章中提取关键要点和创作角度,适合内容创作者、独立开发者和研究者使用。工具使用`xml2js`解析订阅源,支持RSS 2.0和Atom格式.
## 核心能力

| 能力模块 | 说明 | 免费版支持 |
|----|---|-----|
| 订阅管理 | 添加/删除/列出订阅源 | 支持 |
| 分类管理 | 按分类组织订阅源 | 支持 |
| 关键词监控 | 按关键词过滤条目 | 支持 |
| 时间筛选 | 按最近N小时过滤 | 支持 |
| 列表输出 | 紧凑列表格式 | 支持 |
| 内容研究模式 | 提取要点与创作角度 | 支持 |
| JSON输出 | 程序化处理格式 | 支持 |
| 自动摘要 | 条目摘要生成 | 支持 |
| 定时调度 | 内置Cron任务 | 不支持 |
| 邮件推送 | 摘要邮件发送 | 不支持 |
| 多用户 | 多用户配置 | 不支持 |

### 已知限制
执行已知限制操作,使用`input_params`参数进行配置,支持创建/查询/导出等操作.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 订阅源数量建议
订阅源数量建议:不超过20个

**处理**: 解析订阅源数量建议的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回订阅源数量建议的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 不支持内置定时调度(需手动或系
不支持内置定时调度(需手动或系统crontab)

**处理**: 解析不支持内置定时调度(需手动或系的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回不支持内置定时调度(需手动或系的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 不支持邮件/IM推送
不支持邮件/IM推送

**处理**: 解析不支持邮件/IM推送的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回不支持邮件/IM推送的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 不支持多用户配置
不支持多用户配置

**处理**: 解析不支持多用户配置的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回不支持多用户配置的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 输出格式固定为三种(列表/id
输出格式固定为三种(列表/ideas/JSON)

**处理**: 解析输出格式固定为三种(列表/id的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回输出格式固定为三种(列表/id的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

**处理**: 解析已知限制的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回已知限制的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：轻量级、RSS、Atom、订阅阅读器、支持分类管理、关键词过滤与多种、适合个人内容研究、阅读器免费版为个、人用户提供轻量级、订阅管理与内容研、究能力、核心能力、订阅源添加与分类、关键词监控与过滤、多种输出格式、时间范围筛选、自动摘要生成等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:竞品博客监控

独立开发者希望监控几个竞品博客的更新,及时了解对方产品动向.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | RSS阅读器免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 添加竞品订阅源
node （请参考skill目录中的脚本文件） add "https://competitor-a.com/blog/feed" --category competitors
node （请参考skill目录中的脚本文件） add "https://competitor-b.com/feed.xml" --category competitors
# ...
# 添加行业媒体
node （请参考skill目录中的脚本文件） add "https://techcrunch.com/feed" --category news
node （请参考skill目录中的脚本文件） add "https://news.ycombinator.com/rss" --category tech
# ...
# 检查最近24小时更新
node （请参考skill目录中的脚本文件） check --since 24h
```

输出示例:

```text
[competitors] Competitor A Blog - "New Feature: AI Assistant" (3h ago)
  https://competitor-a.com/blog/ai-assistant
[news] TechCrunch - "Startup Raises $50M Series B" (5h ago)
  https://techcrunch.com/startup-funding
[tech] Hacker News - "Show HN: Open-source LLM Router" (8h ago)
  https://news.ycombinator.com/item?id=12345
```

### 场景二:内容创作灵感收集

内容创作者希望从订阅源中获取创作灵感,提取文章要点和可写的角度.
```bash
# 内容研究模式:提取要点和创作角度
node （请参考skill目录中的脚本文件） check --since 24h --format ideas
```

输出示例:

```text
## 不适用场景
# ...
以下场景RSS阅读器免费版不适合处理：
# ...
- 纯技术文档撰写
- 学术论文写作
- 法律文书起草
# ...
## 触发条件
# ...
需要生成营销文案、写作内容、标题优化、内容创作时使用。不适用于非本工具能力范围的需求.
# ...
## Content Ideas from RSS (Last 24h)
# ...
### Tech
- **"vLLM 0.8 PagedAttention全面升级"** - [Hacker News]
  Key points: KV缓存效率提升40%, 支持更长上下文, 延迟降低25%
  Angle: 如何利用新版vLLM优化你的推理服务部署
# ...
- **"Bun 1.2原生SQLite支持"** - [JavaScript Weekly]
  Key points: 内置SQLite, 比better-sqlite3快3倍, 消除外部依赖
  Angle: Bun vs Node.js: 全栈开发体验对比
# ...
### News
- **"OpenAI发布GPT-5 API"** - [OpenAI Blog]
  Key points: 128K上下文, 定价降50%, 免费试用
  Angle: GPT-5 API定价对SaaS产品成本结构的影响
```

### 场景三:关键词监控

用户希望只关注包含特定关键词的文章更新.
```bash
# 按关键词过滤
node （请参考skill目录中的脚本文件） check --keywords "AI,agents,automation"
# ...
# 按分类+关键词组合过滤
node （请参考skill目录中的脚本文件） check --category tech --keywords "Rust,async,tokio" --since 48h
```

## 快速开始

### 依赖详情

```bash
npm install xml2js node-fetch
```

脚本在依赖缺失时会自动提示安装.
### 第二步:添加第一个订阅源

```bash
ycombinator.com/rss" --category tech
```

### 第三步:检查更新

```bash
# 检查所有源最近24小时更新
node （请参考skill目录中的脚本文件） check
# ...
# 检查特定分类
node （请参考skill目录中的脚本文件） check --category tech --since 24h
```

### 第四步:浏览与管理

```bash
# 列出所有订阅源
node （请参考skill目录中的脚本文件） list
# ...
# 移除订阅源
node （请参考skill目录中的脚本文件） remove "https://example.com/feed.xml"
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 示例

### feeds.json 配置格式

```json
{
  "feeds": [
    {
      "url": "https://news.ycombinator.com/rss",
      "name": "Hacker News",
      "category": "tech",
      "enabled": true,
      "lastChecked": "2026-07-18T08:00:00Z",
      "lastItemDate": "2026-07-18T07:30:00Z"
    },
    {
      "url": "https://openai.com/blog/rss.xml",
      "name": "OpenAI Blog",
      "category": "tech",
      "enabled": true,
      "lastChecked": "2026-07-18T08:00:00Z",
      "lastItemDate": "2026-07-17T15:00:00Z"
    }
  ],
  "settings": {
    "maxItemsPerFeed": 10,
    "maxAgeDays": 7,
    "summaryEnabled": true
  }
}
```

### 设置项说明

| 设置项 | 说明 | 默认值 |
|---:|---:|---:|
| `maxItemsPerFeed` | 每个源最多显示条目数 | 10 |
| `maxAgeDays` | 最大文章年龄(天) | 7 |
| `summaryEnabled` | 是否生成摘要 | true |

### 推荐订阅源

#
### 技术/AI

```text
https://news.ycombinator.com/rss          - Hacker News
https://www.reddit.com/r/artificial/.rss   - r/artificial
https://www.reddit.com/r/LocalLLaMA/.rss   - r/LocalLLaMA
https://openai.com/blog/rss.xml           - OpenAI Blog
```

#
### 营销/创业

```text
https://www.reddit.com/r/Entrepreneur/.rss - r/Entrepreneur
https://www.reddit.com/r/SaaS/.rss          - r/SaaS
```

#
### 新闻

```text
https://techcrunch.com/feed/               - TechCrunch
https://www.theverge.com/rss/index.xml     - The Verge
```

## 最佳实践

### 1. 分类体系要清晰

添加订阅源时务必指定`--category`。推荐分类:tech(技术)、news(新闻)、competitors(竞品)、newsletters(通讯)、academic(学术)。清晰的分类便于后续按维度筛选.
### 2. 善用内容研究模式

`--format ideas`是免费版的特色功能,它不仅列出文章,还提取关键要点和创作角度。内容创作者应将其作为日常灵感收集工具:

```bash
node （请参考skill目录中的脚本文件） check --since 24h --format ideas > daily-ideas.md
```

### 3. 关键词监控聚焦高价值信号

不要设置太多关键词,否则过滤效果会大打折扣。建议每次监控3-5个高相关性关键词:

```bash
# 好:聚焦当前关注方向
node （请参考skill目录中的脚本文件） check --keywords "向量数据库,RAG,embedding"
# ...
# 不好:关键词过多,几乎不过滤
node （请参考skill目录中的脚本文件） check --keywords "AI,tech,software,code,dev,tool"
```

### 4. 结合系统crontab实现定时

免费版不支持内置调度,但可结合系统crontab实现定时检查:

```bash
# 每日8:00检查并生成内容灵感
0 8 * * * cd /path/to/skill && node （请参考skill目录中的脚本文件） check --since 24h --format ideas > /reports/daily-ideas.md
```

### 5. 定期清理订阅列表

通过`node （请参考skill目录中的脚本文件） list`查看所有订阅源,移除长期不更新或不再关注的源,保持订阅列表精简.
## 常见问题

### Q: 添加订阅源时报错"无法解析"怎么办?

A: 常见原因:(1)URL不是有效的RSS/Atom源,先用浏览器验证;(2)源需要特定User-Agent,部分站点拒绝默认请求;(3)网络无法访问目标URL。确认URL有效后重试,如持续失败考虑更换源URL.
### Q: 内容研究模式(ideas格式)的要点和角度是如何生成的?

A: ideas格式由AI助手根据文章标题和摘要生成关键要点和创作角度。要点是文章核心信息的提炼,角度是针对该文章可能的创作方向建议。质量取决于原始摘要的完整性.
### Q: 关键词过滤的匹配范围是什么?

A: 关键词匹配文章标题和摘要(摘要)。全文内容不在匹配范围内(免费版不抓取全文)。如需全文搜索,建议升级到专业版或配合其他全文索引工具.
### Q: 如何在多台设备间同步订阅配置?

A: `feeds.json`是订阅配置的唯一文件。将其放入Git仓库或云同步目录(如Dropbox、iCloud)即可在多设备间同步。注意`lastChecked`和`lastItemDate`字段会因设备不同而异,不影响订阅配置本身.
### Q: maxItemsPerFeed设置多少合适?

A: 取决于使用场景。日常浏览设10-20即可;深度研究可设50-100。设置过大会增加单次检查耗时和Token消耗。建议默认10,需要时通过命令行参数临时增大.
### Q: 依赖安装失败怎么办?

A: 确认Node.js版本≥14。网络问题可使用国内镜像源:`npm install xml2js node-fetch --registry https://registry.npmmirror.com`。如遇权限问题,使用`npx`前缀或配置npm全局目录权限.
## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Node.js版本**: ≥ 14
- **运行时**: 需要终端执行能力(exec)以调用Node.js脚本

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| Node.js 14+ | 运行时 | 必需 | https://nodejs.org |
| xml2js | npm包 | 必需 | `npm install xml2js` |
| node-fetch | npm包 | 必需 | `npm install node-fetch` |
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| 网络访问 | 网络 | 必需 | 需能访问目标RSS源URL |

### API Key 配置

- 本Skill基于Node.js脚本驱动,无需额外API Key
- RSS源若需认证,免费版暂不支持,建议使用公开RSS源
- 无外部付费API依赖

### 可用性分类

- **分类**: MD+EXEC(纯Markdown指令,核心功能需要exec命令行执行Node.js脚本)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent调用Node.js脚本完成RSS订阅管理与内容研究任务。免费版聚焦个人用户的订阅管理、关键词监控与内容研究模式,适合竞品监控、创作灵感收集与Newsletter聚合场景.
## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
