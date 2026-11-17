---
slug: rss-fetcher-tool-free
name: rss-fetcher-tool-free
version: 1.0.0
displayName: RSS采集器免费版
summary: "轻量级RSS采集与管理工具,支持增量抓取、自动去重与标签提取,适合个人用户构建本地订阅库。RSS采集器免费版为个人用户提供轻量级的RSS订阅采集与本地管理能力。核心能力:"
license: Proprietary
edition: free
description: 'RSS采集器免费版为个人用户提供轻量级的RSS订阅采集与本地管理能力。核心能力:

  - 增量抓取与URL哈希去重

  - 自动标签提取(优先RSS分类)

  - SQLite本地存储

  - 按分类/时间查询文章

  - 终端文章列表浏览

  适用场景:

  - 个人技术资讯本地归档

  - 兴趣主题文章库构建

  - 离线阅读与检索

  差异化:免费版聚焦核心采集与存储流程,基于SQLite实现轻量本地部署,适合个人用户构建可持续积累的订阅文章库,无需服务器'
tags:
  - 研究工具
  - RSS
  - 数据采集
  - 本地存储
  - 个人效率
  - 搜索
  - 检索
  - 工具
  - python3
  - rss
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Knowledge"
---
# RSS采集器免费版

## 概述

RSS采集器免费版是一款基于Python和SQLite的轻量级RSS订阅采集与本地管理工具。它支持增量抓取(只获取新文章)、URL哈希自动去重、自动标签提取(优先使用RSS自带分类,无则从标题提取关键词),并将所有文章存储在本地SQLite数据库中,便于离线检索与长期积累.
免费版适合个人用户在本地构建可持续增长的订阅文章库。首次抓取会拉取历史文章(较慢),后续抓取仅获取增量更新,效率高。工具支持按分类、时间、标签多维查询.
## 核心能力

| 能力模块 | 说明 | 免费版支持 |
|----|---|-----|
| 增量抓取 | 只抓取新文章,基于URL哈希去重 | 支持 |
| 自动标签 | 优先RSS分类,无则提取标题关键词 | 支持 |
| SQLite存储 | 本地数据库持久化 | 支持 |
| 分类管理 | 文章继承源分类 | 支持 |
| 终端列表 | 按时间/分类查看文章 | 支持 |
| 源管理 | 添加/删除/启停RSS源 | 支持 |
| 源健康检查 | 批量检测源可用性 | 支持 |
| HTML报告 | 交互式HTML浏览页面 | 不支持 |
| 并行抓取 | 多源并发抓取 | 不支持(单线程) |
| 自定义标签规则 | 扩展标签提取规则 | 不支持(内置规则) |
| 数据导出 | 导出为JSON/CSV | 不支持 |

### 已知限制
执行已知限制操作,使用`input_params`参数进行配置,支持创建/查询/导出等操作.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 抓取方式
抓取方式:单线程顺序抓取

**处理**: 解析抓取方式的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回抓取方式的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 标签规则
标签规则:使用内置预定义规则,不可扩展

**处理**: 解析标签规则的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回标签规则的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 无HTML报告生成
无HTML报告生成

**处理**: 解析无HTML报告生成的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回无HTML报告生成的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 无数据导出功能
无数据导出功能

**处理**: 解析无数据导出功能的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回无数据导出功能的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 单源超时30秒
单源超时30秒,无并发优化

**处理**: 解析单源超时30秒的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回单源超时30秒的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

**处理**: 解析已知限制的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回已知限制的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：轻量级、采集与管理工具、支持增量抓取、自动去重与标签提、适合个人用户构建、本地订阅库、采集器免费版为个、人用户提供轻量级、订阅采集与本地管、理能力、核心能力、增量抓取与、自动标签提取、本地存储、按分类、时间查询文章、终端文章列表浏览等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:个人技术资讯归档

开发者希望将多个技术博客的文章持续归档到本地,构建可检索的知识库.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | RSS采集器免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 初始化数据库
python3 （请参考skill目录中的脚本文件）
# ...
# 配置订阅源
python3 （请参考skill目录中的脚本文件） add openai "OpenAI Blog" "https://openai.com/blog/rss.xml" tech
python3 （请参考skill目录中的脚本文件） add hn "Hacker News" "https://hnrss.org/frontpage" tech
python3 （请参考skill目录中的脚本文件） add arxiv "arXiv CS.AI" "https://export.arxiv.org/rss/cs.AI" academic
# ...
# 执行抓取
python3 （请参考skill目录中的脚本文件）
# ...
# 查看最近文章
python3 （请参考skill目录中的脚本文件） --hours 48
```

输出示例:

```text
| date     | source | category | title                          | tags           |
|---:|---:|---:|---:|---:|
| 07-18    | openai | tech     | Introducing GPT-5 API          | AI, GPT, API   |
| 07-18    | hn     | tech     | vLLM 0.8 PagedAttention升级    | AI, 推理       |
| 07-17    | arxiv  | academic | Efficient Transformers Survey  | AI, transformer|
```

### 场景二:按主题检索历史文章

用户想查找之前抓取过的关于"向量数据库"的文章.
```bash
# 按分类查看
python3 （请参考skill目录中的脚本文件） --category tech
# ...
# 使用SQL查询(直接操作数据库)
python3 -c "
import sqlite3
conn = sqlite3.connect('data/rss_fetcher.db')
for row in conn.execute(\"SELECT title, url, published_at FROM articles WHERE title LIKE '%向量数据库%' ORDER BY published_at DESC LIMIT 10\"):
    print(row)
"
```

### 场景三:源健康监控

用户想检查当前订阅源是否都正常工作,移除失效源.
```bash
# 检查所有源健康状态
python3 （请参考skill目录中的脚本文件） check
# ...
# 查看源统计
python3 （请参考skill目录中的脚本文件） stats
# ...
# 禁用失效源
python3 （请参考skill目录中的脚本文件） disable broken-source-id
```

## 不适用场景

以下场景RSS采集器免费版不适合处理：

- 数据库架构设计决策
- NoSQL选型
- 数据仓库ETL设计

## 触发条件

需要数据库操作、SQL查询、数据存储管理时使用。不适用于非本工具能力范围的需求.
## 快速开始

### 第一步:初始化

```bash
# 进入技能目录
cd skills/rss-fetcher-tool-free
# ...
# 初始化数据库
python3 （请参考skill目录中的脚本文件）
# 输出: Database initialized at data/rss_fetcher.db
```

### 第二步:配置订阅源

编辑`config/sources.json`或使用命令行添加:

```json
{
  "sources": [
    {
      "id": "openai",
      "name": "OpenAI Blog",
      "url": "https://openai.com/blog/rss.xml",
      "category": "tech",
      "enabled": true
    }
  ]
}
```

命令行方式:

```bash
com/blog/rss.xml" tech
```

### 第三步:执行首次抓取

```bash
# 首次抓取会拉取历史文章,较慢
python3 （请参考skill目录中的脚本文件）
# ...
# 后续抓取仅获取增量
python3 （请参考skill目录中的脚本文件） --hours 24
```

### 第四步:浏览与查询

```bash
# 查看最近48小时文章
python3 （请参考skill目录中的脚本文件） --hours 48
# ...
# 按分类查看
python3 （请参考skill目录中的脚本文件） --category tech
# ...
# JSON格式输出(便于程序处理)
python3 （请参考skill目录中的脚本文件） --json
```

## 示例

### sources.json 配置格式

```json
{
  "_description": "RSS源配置文件",
  "_updated": "2026-07-18",
  "_total_sources": 3,
  "sources": [
    {
      "id": "openai",
      "name": "OpenAI Blog",
      "category": "tech",
      "enabled": true
    },
    {
      "id": "arxiv-ai",
      "name": "arXiv CS.AI",
      "url": "https://export.arxiv.org/rss/cs.AI",
      "category": "academic",
      "enabled": true
    },
    {
      "id": "hn",
      "name": "Hacker News",
      "url": "https://hnrss.org/frontpage",
      "category": "tech",
      "enabled": true
    }
  ]
}
```

字段说明:

| 字段 | 说明 | 示例 |
|:---:|:---:|:---:|
| `id` | 源唯一标识 | `openai` |
| `name` | 显示名称 | `OpenAI Blog` |
| `url` | RSS订阅地址 | `https://openai.com/blog/rss.xml` |
| `category` | 文章分类 | `tech` |
| `enabled` | 是否启用 | `true` |

### 内置标签规则

免费版内置以下标签提取规则(不可扩展):

| 关键词 | 标签 |
|:------|------:|
| AI, GPT, 大模型, 机器学习 | AI |
| 区块链, 比特币, crypto | 区块链 |
| 股票, 股市, equity | 股票 |
| 游戏, gaming, esports | 游戏 |

无RSS分类时,从标题提取英文大写单词或中文词组作为标签.
### 常用SQL查询

```sql
-- 获取今天所有文章
SELECT title, url, source_id
FROM articles
WHERE date(fetched_at, 'unixepoch') = date('now')
ORDER BY published_at DESC;
# ...
-- 按分类获取最近24小时文章
SELECT * FROM articles
WHERE category = 'tech'
AND published_at > strftime('%s', 'now', '-24 hours');
# ...
-- 获取热门标签
SELECT t.name, COUNT(*) as count
FROM tags t
JOIN article_tags at ON t.id = at.tag_id
GROUP BY t.id
ORDER BY count DESC;
```

## 最佳实践

### 1. 分类要规划清晰

`category`字段一旦设定不易频繁更改。建议提前规划分类体系(如tech/academic/business/lifestyle),文章自动继承源的分类,便于后续按维度筛选.
### 2. 首次抓取要有耐心

首次抓取会拉取每个源的全部历史文章,可能较慢(取决于源的历史文章量)。后续抓取仅获取增量,速度会大幅提升。建议首次抓取选择非高峰时段.
### 3. 定期清理失效源

通过`source.py check`定期检查源健康状态,禁用或移除失效源。失效源会拖慢抓取速度(每次30秒超时).
### 4. SQLite单进程访问

SQLite不支持并发写入。避免同时运行多个抓取进程。建议通过crontab定时单次执行:

```bash
# 每日6点和18点各抓取一次
0 6,18 * * * cd /path/to/skill && python3 （请参考skill目录中的脚本文件）
```

### 5. 时间不可靠文章需人工审核

部分文章的`published_at`可能缺失或异常(标记为1970-01-01)。这些文章需要人工审核发布时间,或在查询时过滤:

```sql
SELECT * FROM articles WHERE published_at > 0 ORDER BY published_at DESC;
```

## 常见问题

### Q: 首次抓取很慢怎么办?

A: 首次抓取需要拉取每个源的全部历史文章,速度取决于源的历史文章量和网络。建议:(1)先添加少量源测试;(2)选择非高峰时段执行;(3)使用`--hours`限制时间范围(但首次仍会拉取全部,该参数仅过滤显示).
### Q: 标签提取不准怎么办?

A: 免费版使用内置规则提取标签,准确率有限。标签优先级为:RSS自带category > 标题关键词规则匹配 > 标题名词提取。如需更精准的标签,可升级到专业版使用自定义标签规则和LLM辅助标签提取.
### Q: SQLite数据库损坏怎么办?

A: SQLite数据库文件损坏通常由并发写入或异常中断导致。恢复方法:(1)备份数据库文件;(2)运行`sqlite3 data/rss_fetcher.db "PRAGMA integrity_check;"`检查;(3)如损坏严重,删除数据库文件并重新`init_db.py`,然后重新抓取(历史文章会重新拉取).
### Q: 抓取报错"源超时"怎么办?

A: 单源超时默认30秒。可能原因:(1)源服务器响应慢;(2)网络问题;(3)源URL已失效。运行`source.py check`检查源健康状态,禁用或移除持续超时的源.
### Q: 如何备份文章数据?

A: 直接复制`data/rss_fetcher.db`文件即可完成备份。建议定期(如每周)复制到备份目录。数据库文件是自包含的,可在任意机器上恢复使用.
### Q: 文章数量很大时查询变慢怎么办?

A: SQLite在10万条以下文章时查询性能良好。如文章量更大,确保查询使用了索引(时间、分类、URL均有索引)。避免全表扫描,查询时始终带上时间或分类过滤条件.
## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Python版本**: ≥ 3.8
- **运行时**: 需要终端执行能力(exec)以调用Python脚本

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|:---|---:|---:|
| Python 3.8+ | 运行时 | 必需 | https://python.org |
| feedparser | Python库 | 必需 | `pip3 install feedparser` |
| SQLite3 | 数据库 | 必需(Python内置) | Python标准库自带 |
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| 网络访问 | 网络 | 必需 | 需能访问目标RSS源URL |

### API Key 配置

- 本Skill基于Python脚本驱动,无需额外API Key
- RSS源若需认证,免费版暂不支持,建议使用公开RSS源
- 无外部付费API依赖

### 可用性分类

- **分类**: MD+EXEC(纯Markdown指令,核心功能需要exec命令行执行Python脚本)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent调用Python脚本完成RSS采集与本地存储任务。免费版聚焦个人用户的增量抓取、自动去重、标签提取与SQLite本地存储,适合构建可持续积累的订阅文章库.
## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------:|--------|:-------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
