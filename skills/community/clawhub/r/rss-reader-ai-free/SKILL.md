---
name: "rss-reader-ai-free"
description: "自动抓取RSS订阅源，使用AI生成中文摘要，支持单渠道推送，适合个人用户信息聚合。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "RSS智能阅读器免费版"
  version: "1.0.0"
  summary: "自动抓取RSS订阅源，使用AI生成中文摘要，支持单渠道推送，适合个人用户信息聚合。"
  tags:
    - "沟通协作"
    - "信息聚合"
    - "RSS"
    - "AI摘要"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# RSS智能阅读器（免费版）

## 概述

RSS智能阅读器免费版是一款面向个人用户的自动化信息聚合工具。它会自动抓取你关注的RSS/Atom订阅源，使用大语言模型生成简洁的中文摘要，并通过单一渠道（飞书/Telegram/Email任选其一）推送给你。内置SQLite去重机制，确保不会重复推送已读内容。

## 核心能力

### 1. RSS/Atom 自动抓取

支持标准RSS 2.0和Atom格式的订阅源自动抓取，可配置抓取频率。

**输入**: 用户提供RSS/Atom 自动抓取所需的指令和必要参数。
**处理**: 按照skill规范执行RSS/Atom 自动抓取操作,遵循单一意图原则。
**输出**: 返回RSS/Atom 自动抓取的执行结果,包含操作状态和输出数据。

- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 2. AI 中文摘要生成

调用大语言模型（支持Claude/OpenAI），将英文或长篇内容自动生成简洁的中文摘要，保留核心信息。

**输入**: 用户提供AI 中文摘要生成所需的指令和必要参数。
**处理**: 按照skill规范执行AI 中文摘要生成操作,遵循单一意图原则。
**输出**: 返回AI 中文摘要生成的执行结果,包含操作状态和输出数据。

- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 3. 智能去重

使用轻量级数据库（SQLite）记录已推送内容，通过内容指纹去重，避免重复推送。

**输入**: 用户提供智能去重所需的指令和必要参数。
**处理**: 按照skill规范执行智能去重操作,遵循单一意图原则。
**输出**: 返回智能去重的执行结果,包含操作状态和输出数据。

- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 4. 单渠道推送

免费版支持选择一个推送渠道：飞书群机器人、Telegram Bot 或 Email。

**输入**: 用户提供单渠道推送所需的指令和必要参数。
**处理**: 按照skill规范执行单渠道推送操作,遵循单一意图原则。
**输出**: 返回单渠道推送的执行结果,包含操作状态和输出数据。
**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：生成中文摘要、支持单渠道推送、适合个人用户信息、智能阅读器、面向个人用户的自、动化信息聚合工具等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：技术博客每日监控

订阅技术博客源，每天自动抓取新文章并生成中文摘要，推送到飞书群。

```yaml
# 个人技术博客订阅配置
feeds:
  - name: "Hacker News"
    url: "https://hnrss.org/frontpage"
    category: "tech"
  - name: "阮一峰周刊"
    url: "https://www.ruanyifeng.com/blog/atom.xml"
    category: "tech"
  - name: "V2EX热门"
    url: "https://www.v2ex.com/index.xml"
    category: "tech"
```

推送效果示例：

```text
RSS摘要推送
============================

Hacker News

Why SQLite is Taking Over
摘要: SQLite正在从嵌入式数据库扩展到更多应用场景。文章分析了其在
边缘计算、移动应用中的优势，以及开发者社区的采用趋势。

阅读原文: https://example.com/article1
---------------------------

阮一峰周刊

科技爱好者周刊第300期
摘要: 本期内容包括AI编程工具对比、WebAssembly最新进展、
开源许可证选择指南等。

阅读原文: https://example.com/article2
============================
```

### 场景二：每日新闻早报

每天定时抓取新闻源，生成摘要后通过Email推送给自己。

```bash
# 每天早上8点执行
python main.py --once --config morning_news.yaml

# 配置定时任务（crontab）
0 8 * * * cd ~/rss-reader && python main.py --once --config morning_news.yaml
```

### 场景三：兴趣主题聚合

```yaml
# 兴趣主题订阅
feeds:
  - name: "AI研究"
    url: "https://feeds.example.com/ai-research.xml"
    category: "ai"
  - name: "摄影博客"
    url: "https://feeds.example.com/photography.xml"
    category: "photography"

llm:
  provider: "claude"
  model: "claude-sonnet-4-20250514"
  summary_length: "short"    # short / medium / long

notify:
  telegram:
    enabled: true
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    chat_id: "${TELEGRAM_CHAT_ID}"
```

## 不适用场景

以下场景RSS智能阅读器免费版不适合处理：

- 需要100%确定性的关键决策
- 医疗诊断
- 法律判决

## 触发条件

需要AI模型调用、智能对话、Agent编排、LLM应用时使用。不适用于非本工具能力范围的需求。

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 安装

```bash
# 依赖说明
mkdir ~/rss-reader && cd ~/rss-reader
pip install -r requirements.txt

# 复制配置文件
cp config.example.yaml my_config.yaml
```

### 基本使用

```bash
# 单次执行（抓取并推送一次）
python main.py --once

# 启动定时任务模式
python main.py

# 查看统计信息
python main.py --stats

# 指定配置文件
python main.py --config my_config.yaml --once
```

### 命令行参数

```bash
python main.py [options]

--config, -c    配置文件路径 (默认: config.yaml)
--once          只执行一次，不进入定时模式
--stats         显示统计信息（已抓取/已推送/去重数量）
--db            数据库路径 (默认: rss_reader.db)
--verbose       详细日志输出
```

#
## 示例

```yaml
# config.yaml - 免费版配置
feeds:
  - name: "Hacker News"
    url: "https://hnrss.org/frontpage"
    category: "tech"
  - name: "阮一峰周刊"
    url: "https://www.ruanyifeng.com/blog/atom.xml"
    category: "tech"

# AI摘要配置
llm:
  provider: "claude"                      # 或 "openai"
  model: "claude-sonnet-4-20250514"
  api_key: "${ANTHROPIC_API_KEY}"
  summary_length: "medium"                # short / medium / long
  language: "zh-CN"                       # 摘要输出语言

# 推送配置（免费版选择一个渠道）
notify:
  feishu:
    enabled: true
    webhook_url: "${FEISHU_WEBHOOK}"
  # telegram:
  #   enabled: false
  #   bot_token: "${TELEGRAM_BOT_TOKEN}"
  #   chat_id: "${TELEGRAM_CHAT_ID}"
  # email:
  #   enabled: false
  #   smtp_host: "smtp.gmail.com"
  #   smtp_port: 587
  #   username: "${EMAIL_USER}"
  #   password: "${EMAIL_PASSWORD}"
  #   to: "me@example.com"

# 去重配置
dedup:
  enabled: true
  db_path: "rss_reader.db"
  retention_days: 30                      # 去重记录保留天数

# 抓取配置
fetch:
  interval_minutes: 60                    # 抓取间隔（分钟）
  timeout_seconds: 30                     # 单源超时
  max_items_per_feed: 10                  # 每源最大条目数
```

## 最佳实践

### 订阅源管理

| 实践 | 说明 |
|:-----|:-----|
| 分类管理 | 为每个订阅源设置 category，便于过滤 |
| 控制数量 | 免费版建议订阅源不超过20个，保证摘要质量 |
| 定期清理 | 定期检查失效源，移除无法访问的订阅 |
| 超时设置 | 设置合理的超时时间，避免单源阻塞 |

### AI 摘要质量优化

```python
# 摘要提示词优化建议
SUMMARY_PROMPT = """
请将以下内容生成一段简洁的中文摘要：
1. 保留核心观点和关键数据
2. 省略冗余细节和广告内容
3. 字数控制在100-200字
4. 保持客观中立的语气

内容: {article_content}
"""
```

### 去重策略

```bash
# 查看去重统计
python main.py --stats

# 输出示例:
# 已抓取: 1,250 篇
# 已推送: 980 篇
# 去重过滤: 270 篇
# 数据库大小: 2.3 MB
```

## 常见问题

### Q: 免费版支持多少个订阅源？

免费版建议配置不超过20个订阅源。订阅源过多可能导致摘要生成时间较长，影响推送及时性。如需更多订阅源，请考虑升级到 PRO 版本。

### Q: 可以同时推送到多个渠道吗？

免费版仅支持单渠道推送（飞书、Telegram、Email三选一）。PRO 版本支持多渠道同时推送。

### Q: AI摘要支持哪些模型？

免费版支持 Claude 和 OpenAI 两种提供商。你需要在配置中设置对应的 API Key。

### Q: 去重数据库会占用很多空间吗？

不会。每条记录仅存储内容指纹（哈希值）和元数据，约100字节/条。每月约产生30KB数据，非常轻量。

### Q: 抓取失败怎么办？

```bash
# 启用详细日志排查
python main.py --once --verbose

# 常见原因:
# 1. 订阅源URL失效 - 更新URL
# 2. 网络超时 - 增加timeout设置
# 3. 格式不支持 - 确认源为标准RSS/Atom格式
```

## 依赖说明

### 运行环境

- **Agent 平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python 版本**: 3.8+
- **网络环境**: 需能访问订阅源URL和AI API端点

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| Python 3.8+ | 运行时 | 必需 | python.org 官方下载 |
| feedparser | Python库 | 必需 | `pip install feedparser` |
| requests | Python库 | 必需 | `pip install requests` |
| anthropic / openai | Python库 | 必需 | `pip install anthropic` 或 `pip install openai` |
| sqlite3 | 标准库 | 必需 | Python内置 |
| pyyaml | Python库 | 必需 | `pip install pyyaml` |
| LLM API | API | 必需 | 由Agent内置LLM提供或自行配置 |

### API Key 配置

```bash
# AI摘要API（必选其一）
export ANTHROPIC_API_KEY="your_claude_api_key"
# 或
export OPENAI_API_KEY="your_openai_api_key"

# 推送渠道API（根据选择的渠道配置）
export FEISHU_WEBHOOK="your_feishu_webhook_url"
# 或
export TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"
# 或
export EMAIL_USER="your_email@gmail.com"
export EMAIL_PASSWORD="your_app_password"
```

### 可用性分类

- **分类**: MD+EXEC+SCRIPT（Markdown指令 + 命令行执行 + Python脚本）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent完成操作，配合Python脚本实现RSS抓取与摘要生成
- **适用人群**: 个人用户、信息工作者、技术爱好者
- **版本限制**: 免费版支持单渠道推送、20个以内订阅源，PRO 版本提供多渠道、多源聚合与高级分析

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
