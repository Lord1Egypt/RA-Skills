---
slug: "rss-ai-reader-free"
name: "rss-ai-reader-free"
version: "1.0.0"
displayName: "RSS AI 摘要 LITE"
summary: "RSS抓取与LLM中文摘要生成,推送到飞书,SQLite去重,单次执行模式。RSS AI 阅读器(免费版)。自动抓取 RSS/Atom 订阅源,通过 ai-assistant 生成中文摘要,"
summary_zh: "RSS抓取与LLM中文摘要生成,推送到飞书,SQLite去重,单次执行模式。RSS AI 阅读器(免费版)。自动抓取 RSS/Atom 订阅源,通过 ai-assistant 生成中文摘要,"
license: "MIT"
description: "|-. 适用于需要rss ai reader相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  RSS AI 阅读器(免费版)。自动抓取 RSS/Atom 订阅源,通过 ai-assistant 生成中文摘要,
  推送到飞书群机器人 Webhook。基于 SQLite 存储实现条目去重,避免重复推送.
  覆盖三大基础能力:Feed 抓取(支持 RSS 2.0 与 Atom 1.0)、LLM 摘要生成(中文输出)、
  飞书 Webhook 推送。仅支持单次执行模式(--once),通过命令行参数控制执行行为.
  适用于技术博客监控、个人订阅摘要推送等基础场景.
  如需 Telegram 与 Email 推送、llm-provider 后端、定时任务循环、多渠道组合推送等高级能力,
  请升级至 rss-ai-reader 付费版.
tags:
  - 研发工具
  - rss
  - reader
  - automation
  - productivity
  - Research
  - 订阅
  - 信息
  - feed
  - llm
tools:
  - read
  - exec
homepage: ""
category: "Knowledge"
pricing_tier: free
---
# RSS AI 摘要 LITE

自动抓取 RSS/Atom 订阅源,通过 LLM 生成中文摘要,推送到飞书。基于 SQLite 去重,支持单次执行.
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | RSS AI 摘要 LITE处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 依赖说明

### 运行环境
- **Agent平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **Python 环境**: Python 3.9 及以上,需安装 feedparser、requests、PyYAML 等依赖

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供,或配置 ai-assistant 的 API Key |
| 飞书 Webhook | 凭证 | 必需 | 飞书群机器人配置后获取 Webhook URL |

### API Key 配置
- LLM API Key 通过环境变量注入(如 ANTHROPIC_API_KEY),在配置文件 llm 节点引用
- 飞书 Webhook URL 通过环境变量 FEISHU_WEBHOOK 注入

### 可用性分类
- **分类**: MD+EXEC模式纯 Markdown 指令,核心功能需要 exec 命令行执行能力)
- **说明**: 基于 Markdown 的 AI Skill,通过自然语言指令驱动 Agent 执行 Python 脚本完成任务

## 核心能力

### 1. RSS/Atom Feed 抓取
- **协议支持**: 兼容 RSS 2.0 与 Atom 1.0 两种主流订阅协议
- **多源管理**: 配置文件中以列表形式维护多个 feed,每个 feed 含 name、url、category 三个字段
- **分类标记**: 通过 category 字段对 feed 分组(如 tech、news),便于后续按类筛选
- **抓取容错**: 单个 feed 抓取失败不中断整体流程,记录失败源并继续抓取下一个
- **条目解析**: 从 feed 中提取标题、链接、发布时间、正文摘要等字段供 LLM 处理

### 2. LLM 中文摘要生成
- **Provider 支持**: 使用 ai-assistant 作为后端,在配置文件 llm.provider 字段固定为 ai-assistant
- **中文输出**: 无论原文语言,摘要统一输出为中文,降低阅读门槛
- **长度可控**: 通过 prompt 约束摘要长度(默认 3 到 5 句),避免过长影响推送体验
- **批量处理**: 对每批新条目逐条生成摘要,单条失败不影响其他条目
- **模型选择**: 通过 llm.model 字段指定具体模型(如 ai-assistant-sonnet-4-20250514)

### 3. SQLite 去重
- **去重维度**: 按 feed URL 与条目 ID(或 GUID)联合去重,确保同一篇文章不重复推送
- **持久存储**: 去重记录存储在 SQLite 数据库(默认 rss_reader.db),跨进程持久化
- **增量抓取**: 每次执行时只处理数据库中不存在的新条目,已推送的自动跳过
- **统计查询**: 通过 --stats 参数查看已处理条目数、各 feed 抓取量等统计信息

### 4. 飞书 Webhook 推送
- **推送渠道**: 通过飞书群机器人 Webhook 推送,消息含标题、摘要、原文链接
- **富文本格式**: 消息以卡片形式发送,标题加粗,摘要与原文链接分行展示
- **失败重试**: Webhook 调用失败时记录错误日志,不影响其他条目的推送

#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 适用场景

| 场景 | 输入 | 输出 |
|---:|---:|---:|
| 技术博客监控 | Hacker News、阮一峰等 feed 列表 | 新文章中文摘要推送到飞书群 |
| 个人订阅摘要 | 个人关注的技术博客 feed | 更新摘要推送到飞书 |

**不适用于**: 需要 Telegram 或 Email 推送的场景(需升级付费版);需要定时任务循环的场景(免费版仅支持单次执行);需要 llm-provider 后端的场景.
## 使用流程

1. **准备运行环境**: 确认 Python 3.9 已安装,获取项目代码并安装依赖(`pip install -r requirements.txt`)
2. **创建配置文件**: 复制 config.yaml 为 my_config.yaml,填入 feed 列表、llm 配置、飞书 Webhook 配置
3. **配置环境变量**: 将 LLM API Key 与飞书 Webhook URL 设为环境变量
4. **单次执行**: 运行 `python main.py --config my_config.yaml --once` 抓取并推送
5. **查看统计**: 运行 `python main.py --stats` 确认条目已入库与去重生效
6. **按需调整**: 根据推送效果调整 feed 列表与摘要长度

**结果验证**: 任务完成后,查看输出确认状态。成功时返回摘要和数据;失败时根据错误信息排查,参考恢复章节获取修复步骤.
## 配置文件结构

```yaml
feeds:
  - name: "Hacker News"
    url: "https://hnrss.org/frontpage"
    category: "tech"
  - name: "阮一峰周刊"
    url: "https://www.ruanyifeng.com/blog/atom.xml"
    category: "tech"
# ...
llm:
  provider: "ai-assistant"
  model: "ai-assistant-sonnet-4-20250514"
  api_key: "${ANTHROPIC_API_KEY}"
# ...
notify:
  feishu:
    enabled: true
    webhook_url: "${FEISHU_WEBHOOK}"
```

## 命令行参数

```bash
python main.py [options]
# ...
--config, -c  配置文件路径 (默认: config.yaml)
--once        只执行一次抓取与推送
--stats       显示数据库中的统计信息
--db          数据库路径 (默认: rss_reader.db)
```

## 案例展示

### 案例 1: 订阅 Hacker News 与阮一峰,推送到飞书群

**场景**: 个人希望每天手动执行一次,将技术博客更新摘要推送到飞书群

**配置文件 my_config.yaml**:

```yaml
feeds:
  - name: "Hacker News"
    category: "tech"
  - name: "阮一峰周刊"
ruanyifeng.com/blog/atom.xml"
    category: "tech"
# ...
llm:
  provider: "ai-assistant"
  model: "ai-assistant-sonnet-4-20250514"
  api_key: "${ANTHROPIC_API_KEY}"
# ...
notify:
  feishu:
    enabled: true
    webhook_url: "${FEISHU_WEBHOOK}"
```

**执行命令**:

```bash
python main.yaml --once
```

**飞书群收到的消息**:

```text
📰 Hacker News
# ...
**Why SQLite is Taking Over**
# ...
📝 SQLite 正在从嵌入式数据库扩展到更多应用场景。文章分析了其在边缘计算、移动应用中的优势,并对比了 PostgreSQL 在轻量级场景下的局限.
# ...
[🔗 阅读原文]
# ...
📰 阮一峰周刊
# ...
**科技爱好者周刊第 350 期**
# ...
📝 本期周刊介绍了 WebGPU 的最新进展、一个开源的 Markdown 编辑器项目,以及关于 AI Agent 架构的讨论.
# ...
[🔗 阅读原文]
```

**分析**: 单次执行抓取两个 feed 的新条目,ai-assistant 为每条生成中文摘要,飞书 Webhook 推送到群。SQLite 记录已推送的条目 ID,下次执行时自动跳过已推送的内容.
### 案例 2: 个人技术博客订阅摘要推送

**场景**: 开发者订阅 Hacker News、V2EX、阮一峰三个技术博客,每周手动执行一次获取更新摘要

**配置要点**: 在案例 1 的 feeds 列表中追加 V2EX 的 feed(`https://www.v2ex.com/index.xml`),三个 feed 均归入 tech 分类,llm 与 notify 配置不变.
**执行命令**:

```bash
python main.yaml --once
```

**分析**: ai-assistant 为三个 feed 的新条目生成中文摘要后通过飞书 Webhook 推送。SQLite 去重确保同一篇文章只推送一次,多次执行时只推送增量内容.
## 异常处理

| 错误场景 | 错误现象 | 原因分析 | 处理方式 |
|:---:|:---:|:---:|:---:|
| Feed URL 无法访问 | 抓取报 `ConnectionError` 或超时 | 网络不通或 feed URL 已失效 | 检查网络连接和配置后重试,在浏览器中打开 feed URL 确认是否可访问 |
| LLM API 调用失败 | 报 `401 Unauthorized` 或 `429 Too Many Requests` | API Key 无效或额度耗尽 | 核对环境变量中的 ANTHROPIC_API_KEY 是否正确;429 时降低执行频率 |
| 摘要内容为空 | LLM 返回空字符串或仅含标点 | feed 条目正文为空或 LLM 判断无有效内容 | 检查 feed 条目是否含 summary 或 content 字段;在 prompt 中加入兜底逻辑 |
| 飞书 Webhook 返回错误 | HTTP 状态码 400 或 `{"code": 19021}` | Webhook URL 失效或消息体格式不符飞书规范 | 在飞书群设置中重新获取 Webhook URL;检查消息体是否含必填字段(msg_type) |
| SQLite 数据库锁定 | 报 `database is locked` | 多个进程同时写入同一数据库文件 | 确保只有一个 main.py 进程在运行;通过 --db 参数指定独立数据库文件 |

## 常见问题

### Q1: 免费版支持哪些推送渠道?
A: 免费版仅支持飞书 Webhook 推送。如需 Telegram Bot、SMTP Email 推送或多渠道组合推送,需升级至 rss-ai-reader 付费版。飞书 Webhook 在飞书群设置中添加自定义机器人后即可获取.
### Q2: 免费版能定时自动执行吗?
A: 不能。免费版仅支持 --once 单次执行模式,需手动运行或配合外部 cron 调度。如需程序内置的定时循环任务(schedule.interval 配置),需升级至付费版。免费版用户可通过系统 计划任务配置 配合 --once 实现定时效果.
### Q3: SQLite 去重机制如何工作?
A: 去重基于 feed URL 与条目 ID(或 GUID)的联合唯一键。每次抓取新条目时,先查询数据库中是否已存在该条目 ID,存在则跳过,不存在则生成摘要、推送并写入数据库。如需清理历史数据,可直接删除 rss_reader.db 文件,下次执行会自动重建.
### Q4: 免费版与付费版有什么区别?
A: 免费版(LITE)包含 RSS 抓取、ai-assistant 摘要生成、飞书推送、SQLite 去重四大基础功能。付费版(RSS AI 摘要推送)额外提供:
- Telegram Bot 与 SMTP Email 推送渠道
- llm-provider 后端支持(OpenAI 兼容接口)
- 多渠道组合推送(飞书 + Telegram + Email 同时推送)
- 程序内置定时任务循环(schedule.interval 配置)
- 更多案例展示(3 个完整案例 vs 2 个基础案例)
- 更详细的异常处理(8 种场景 vs 5 种基础场景)
- 6 个领域专属 FAQ

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| LLM响应超时或无响应 | 网络延迟或模型负载过高 | 检查网络连接和配置后重试；确认Agent平台LLM服务正常 |
| 输入内容格式不正确 | 用户输入不符合skill预期格式 | 检查输入是否符合skill使用说明中的格式要求，参考示例章节 |
| 执行结果与预期不符 | 指令描述不够明确或上下文不足 | 提供更详细的指令描述，补充必要的上下文信息 |
| 命令执行失败 | 运行环境不满足要求或权限不足 | 确认运行环境符合依赖说明中的要求；检查命令权限设置 |

## 已知限制

- **功能限制**: 仅支持飞书推送,不支持 Telegram 与 Email(需升级付费版)
- **后端限制**: 仅支持 ai-assistant,不支持 llm-provider(需升级付费版)
- **执行模式限制**: 仅支持 --once 单次执行,不支持定时循环(需升级付费版)
- **依赖 LLM 能力**: 摘要质量取决于底层模型,弱模型上摘要可能出现事实偏差
- **仅生成摘要**: 不推送原文全文,如需全文需用户点击原文链接自行阅读
- **非实时推送**: 需手动执行或配合外部 cron,新文章不会在发布瞬间推送

---
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

## 升级提示

本免费版提供 RSS 抓取、ai-assistant 摘要生成、飞书推送、SQLite 去重四大基础功能。如需 Telegram 与 Email 推送、llm-provider 后端、定时任务循环、多渠道组合推送等高级能力,请升级至 **rss-ai-reader** 付费版,获取完整的多渠道推送与定时调度能力.
## 输出格式

```json
{
  "success": true,
  "data": {
    "result": "RSS AI 摘要 LITE处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "rss-ai-reader"
    }
  },
  "execution_log": [
    "解析输入参数",
    "执行核心处理",
    "格式化输出结果"
  ],
  "error": null
}
```
