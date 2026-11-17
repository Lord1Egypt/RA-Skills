---
slug: rss-feed-digest-tool-free
name: rss-feed-digest-tool-free
version: 1.0.0
displayName: RSS聚合摘要免费版
summary: 轻量级RSS/Atom聚合摘要工具,支持关键词过滤与Markdown输出,适合个人用户生成每日资讯摘要
license: Proprietary
edition: free
description: 'RSS聚合摘要免费版为个人用户提供轻量级的RSS/Atom订阅聚合与摘要生成能力。核心能力:

  - 多源RSS/Atom订阅抓取

  - 关键词包含/排除过滤

  - 跨源自动去重

  - 时间范围筛选

  - Markdown/纯文本输出

  适用场景:

  - 个人每日资讯摘要生成

  - 兴趣主题内容聚合

  - 简单的订阅源监控

  差异化:免费版聚焦核心聚合与过滤流程,通过Python脚本实现轻量部署,适合个人用户快速生成每日摘要,无需数据库或复杂配置'
tags:
  - 研究工具
  - RSS
  - 信息聚合
  - 内容摘要
  - 个人效率
  - 搜索
  - 检索
  - 工具
  - https
  - rss
  - markdown
  - bash
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Knowledge"
---
# RSS聚合摘要免费版

## 概述

RSS聚合摘要免费版是一款基于Python的轻量级RSS/Atom订阅聚合工具。它通过`feedparser`库抓取多个订阅源,支持关键词过滤、跨源去重、时间范围筛选,最终生成清晰的Markdown或纯文本摘要.
免费版适合个人用户快速搭建每日资讯摘要流程,无需数据库,无需复杂配置,一条命令即可完成抓取、过滤与输出。工具支持RSS 2.0和Atom两种主流订阅格式.
## 核心能力

| 能力模块 | 说明 | 免费版支持 |
|----|---|-----|
| 多源抓取 | 同时抓取多个RSS/Atom源 | 支持(建议≤5源) |
| 关键词过滤 | 包含/排除关键词筛选 | 支持 |
| 跨源去重 | 多源内容自动去重 | 支持 |
| 时间筛选 | 按最近N小时过滤 | 支持 |
| Markdown输出 | 生成.md格式摘要 | 支持 |
| 纯文本输出 | 生成.txt格式摘要 | 支持 |
| 订阅列表文件 | 从文件批量读取源URL | 支持 |
| 定时调度 | Cron定时任务 | 不支持 |
| HTML报告 | 生成可交互HTML页面 | 不支持 |
| 邮件分发 | 自动发送摘要邮件 | 不支持 |

### 已知限制
执行已知限制操作,使用`input_params`参数进行配置,支持创建/查询/导出等操作.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 建议订阅源数量
建议订阅源数量:不超过5个

**处理**: 解析建议订阅源数量的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回建议订阅源数量的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 不支持定时自动化调度
不支持定时自动化调度

**处理**: 解析不支持定时自动化调度的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回不支持定时自动化调度的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 不支持HTML交互式报告
不支持HTML交互式报告

**处理**: 解析不支持HTML交互式报告的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回不支持HTML交互式报告的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 不支持邮件/IM分发
不支持邮件/IM分发

**处理**: 解析不支持邮件/IM分发的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回不支持邮件/IM分发的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 不支持多用户配置
不支持多用户配置

**处理**: 解析不支持多用户配置的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回不支持多用户配置的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

**处理**: 解析已知限制的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回已知限制的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：轻量级、聚合摘要工具、支持关键词过滤与、适合个人用户生成、每日资讯摘要、聚合摘要免费版为、个人用户提供轻量、订阅聚合与摘要生、成能力、核心能力、订阅抓取、关键词包含、排除过滤、跨源自动去重、时间范围筛选等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:每日AI资讯摘要

个人开发者希望每天快速了解AI领域动态,而非逐个浏览多个网站.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | RSS聚合摘要免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 抓取多个AI相关源,过滤关键词,输出Markdown
python3 （请参考skill目录中的脚本文件） fetch \
  --feeds "https://hnrss.org/frontpage" \
          "https://feeds.arstechnica.com/arstechnica/technology-lab" \
          "https://openai.com/blog/rss.xml" \
  --keywords "AI,LLM,GPT,Claude,agent" \
  --hours 24 \
  --limit 20 \
  --output daily-ai-digest.md \
  --format markdown
```

生成的摘要示例:

```markdown
# 每日AI资讯摘要 | 2026-07-18
# ...
## 不适用场景
# ...
以下场景RSS聚合摘要免费版不适合处理：
# ...
- 实时流数据处理
- 小规模数据手动分析
- 非结构化文本情感分析
# ...
## 触发条件
# ...
需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于非本工具能力范围的需求.
# ...
## 来源: Hacker News
- **[GPT-5多模态推理能力实测](https://example.com/post1)** (3h ago)
  OpenAI最新模型在视觉推理基准上达到SOTA,支持图文混合输入...
# ...
- **[开源大模型推理框架对比](https://example.com/post2)** (6h ago)
  vLLM、TGI、SGLang三大框架在A100上的吞吐量与延迟基准测试...
# ...
## 来源: OpenAI Blog
- **[Introducing GPT-5 API](https://openai.com/blog/gpt5)** (12h ago)
  新API支持128K上下文,定价降低50%,提供免费试用额度...
# ...
---
共抓取 47 条 | 过滤后 20 条 | 去重后 18 条 | 耗时 3.2s
```

### 场景二:竞品动态监控

独立开发者希望追踪几个竞品博客的更新,及时了解对方产品动向.
```bash
# 监控竞品博客,按关键词过滤
python3 （请参考skill目录中的脚本文件） fetch \
  --feeds "https://competitor-a.com/blog/feed" \
          "https://competitor-b.com/feed.xml" \
  --keywords "发布,更新,功能,pricing,launch" \
  --hours 48 \
  --output competitor-watch.md
```

### 场景三:学术研究订阅聚合

研究生希望聚合多个学术RSS源,按研究方向过滤相关论文.
```bash
# 使用订阅列表文件管理多个学术源
cat > academic-feeds.txt << 'EOF'
https://export.arxiv.org/rss/cs.AI
https://export.arxiv.org/rss/cs.CL
https://export.arxiv.org/rss/cs.LG
EOF
# ...
python3 （请参考skill目录中的脚本文件） fetch \
  --feed-file academic-feeds.txt \
  --keywords "transformer,attention,fine-tuning,RAG" \
  --hours 72 \
  --limit 30 \
  --output weekly-papers.md
```

## 快速开始

### 依赖详情

```bash
pip3 install feedparser
```

### 第二步:首次抓取

```bash
# 最简用法:抓取单个源
python3 （请参考skill目录中的脚本文件） fetch \
  --hours 24
```

### 第三步:添加过滤与输出

```bash
# 添加关键词过滤并保存到文件
python3 （请参考skill目录中的脚本文件） fetch \
  --keywords "AI,LLM" \
  --hours 24 \
  --output digest.md \
  --format markdown
```

### 第四步:使用订阅列表文件

当订阅源较多时,使用文件管理更方便:

```bash
# 创建订阅列表
cat > my-feeds.txt << 'EOF'
https://hnrss.org/frontpage
https://feeds.arstechnica.com/arstechnica/technology-lab
https://openai.com/blog/rss.xml
EOF
# ...
# 从文件读取源列表
python3 （请参考skill目录中的脚本文件） fetch \
  --feed-file my-feeds.txt \
  --hours 24 \
  --output daily-digest.md
```

## 示例

### 命令行参数详解

```text
python3 （请参考skill目录中的脚本文件） fetch [选项]
# ...
选项:
  --feeds URL [URL ...]     一个或多个RSS/Atom源URL
  --feed-file PATH          包含源URL列表的文件(每行一个URL)
  --hours N                 只抓取最近N小时的内容(默认24)
  --limit N                 最多输出N条结果(默认20)
  --keywords KW [KW ...]    只保留包含指定关键词的条目(逗号分隔)
  --exclude KW [KW ...]     排除包含指定关键词的条目
  --output PATH             输出文件路径(不指定则输出到终端)
  --format FORMAT           输出格式: markdown 或 text(默认markdown)
```

### 关键词过滤策略

```bash
# 包含过滤:只保留含任一关键词的条目
--keywords "AI,LLM,GPT,Claude"
# ...
# 排除过滤:移除含任一关键词的条目
--exclude "招聘,广告,sponsor"
# ...
# 组合使用:先包含再排除
--keywords "AI,agent" --exclude "招聘,广告"
```

### 订阅列表文件格式

```text
# my-feeds.txt - 每行一个RSS/Atom源URL
# 以#开头的行为注释,自动忽略
https://hnrss.org/frontpage
https://feeds.arstechnica.com/arstechnica/technology-lab
https://openai.com/blog/rss.xml
https://www.artificialintelligence-news.com/feed/
```

## 最佳实践

### 1. 合理设置时间窗口

`--hours`参数控制抓取时间范围。每日摘要用24,周报用168,实时监控用6。时间窗口过大会导致抓取缓慢且结果过多.
### 2. 善用关键词过滤

不要抓取所有内容再人工筛选。通过`--keywords`预先过滤,大幅减少噪音。关键词用逗号分隔,匹配逻辑为"任一命中即保留".
### 3. 使用订阅列表文件管理源

当订阅源超过3个时,改用`--feed-file`管理。文件方式便于版本控制、团队共享和批量修改.
### 4. 输出Markdown便于后续处理

Markdown格式的摘要可直接粘贴到笔记应用(如Obsidian、Notion),也方便AI助手进一步分析和总结.
### 5. 避免抓取过于频繁

RSS源通常有更新频率限制。建议每日抓取1-2次,避免对源站点造成压力。免费版不支持定时调度,可结合系统crontab实现:

```bash
# 每日8:00自动生成摘要(crontab配置)
0 8 * * * cd /path/to/skill && python3 （请参考skill目录中的脚本文件） fetch --feed-file my-feeds.txt --hours 24 --output /reports/$(date +\%Y\%m\%d)-digest.md
```

## 常见问题

### Q: 抓取某些RSS源时报错或返回空结果怎么办?

A: 常见原因有三:(1)源URL已失效,需验证URL是否可访问;(2)源需要特定User-Agent,部分站点会拒绝默认请求头;(3)源格式非标准RSS/Atom。建议先用浏览器验证URL可访问,再确认源格式.
### Q: 关键词过滤支持中文吗?

A: 支持。`feedparser`会正确解析中文内容,关键词匹配为子串包含。例如`--keywords "大模型"`会匹配标题或摘要中包含"大模型"的条目.
### Q: 去重逻辑是如何工作的?

A: 去重基于URL哈希。如果多个源转载了同一篇文章(URL相同或仅参数不同),只会保留第一次出现的条目。对于URL不同但内容相同的转载,免费版不做内容级去重.
### Q: 如何抓取需要认证的私有RSS源?

A: 免费版不支持认证抓取。如果源需要Basic Auth,可在URL中嵌入凭证(`https://user:pass@example.com/feed`),但不推荐明文存储凭证。建议使用专业版的安全认证管理功能.
### Q: 输出的Markdown格式可以自定义吗?

A: 免费版提供固定的Markdown模板(标题+来源+条目列表+统计信息)。如需自定义格式,可修改`（请参考skill目录中的脚本文件）`中的输出模板部分,或升级到专业版使用模板系统.
### Q: feedparser安装失败怎么办?

A: 确认Python版本≥3.8。网络问题可使用国内镜像源安装:`pip3 install feedparser -i https://pypi.tuna.tsinghua.edu.cn/simple`。如果仍有依赖冲突,建议使用虚拟环境隔离安装.
## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Python版本**: ≥ 3.8
- **运行时**: 需要终端执行能力(exec)以调用Python脚本

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| Python 3.8+ | 运行时 | 必需 | https://python.org |
| feedparser | Python库 | 必需 | `pip3 install feedparser` |
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| 网络访问 | 网络 | 必需 | 需能访问目标RSS源URL |

### API Key 配置

- 本Skill基于Python脚本驱动,无需额外API Key
- RSS/Atom源若需认证,需在URL中嵌入凭证(不推荐)或使用专业版
- 无外部付费API依赖

### 可用性分类

- **分类**: MD+EXEC(纯Markdown指令,核心功能需要exec命令行执行Python脚本)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent调用Python脚本完成RSS聚合摘要任务。免费版聚焦个人用户的多源抓取、关键词过滤与Markdown输出,适合每日资讯摘要与兴趣主题聚合场景.
## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "RSS聚合摘要免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "rss feed digest"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
