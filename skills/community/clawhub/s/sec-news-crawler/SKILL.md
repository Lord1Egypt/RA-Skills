---
name: sec-news-crawler
description: |
  网络安全新闻爬虫，每小时自动从多个安全社区 RSS 抓取文章，存入 IMA 笔记。
  触发场景：用户说"抓取安全新闻"、"网络安全日报"、"定时爬取安全资讯"、"安全新闻源管理"
  或需要查看/管理安全新闻爬虫任务时使用此 skill。
---

# sec-news-crawler

每小时从多个安全社区 RSS 抓取最新文章，按日期合并为每日一篇笔记存入 IMA。

## 快速运行

```bash
# 立即执行一次抓取
bash ~/.openclaw/workspace/skills/sec-news-crawler/scripts/run.sh

# 查看运行日志
tail -f ~/.openclaw/workspace/logs/sec_news_cron.log
```

## 系统架构

- **爬虫脚本**：`scripts/crawler.py`
- **RSS 源配置**：`scripts/crawler.py` 内的 `RSS_FEEDS` 列表
- **去重库**：`data/sec_news_seen.json`
- **Cron**：每小时整点执行 `scripts/run.sh`

## 工作流程

1. 从各 RSS 源抓取最新文章
2. 仅保留今天/昨天的文章（按发布日期过滤）
3. 按 URL 去重（同篇文章不重复写入）
4. 同一天所有文章合并为**一篇**笔记，标题 `📰 网络安全新闻 YYYY-MM-DD`
5. 写入 IMA「Openclaw生成」笔记本

## 笔记格式

```
📰 网络安全新闻 2026-03-26（今日）
> 自动抓取 · 更新时间：2026-03-26 18:33 · 共 4 篇文章

1. 文章标题一
   - 来源：嘶吼 | 原文链接
   - 日期：2026-03-26
   - 摘要：...

2. 文章标题二
   - 来源：先知社区 | 原文链接
   ...
```

## 管理命令

| 操作 | 命令 |
|------|------|
| 手动执行一次 | `bash ~/.openclaw/workspace/skills/sec-news-crawler/scripts/run.sh` |
| 查看日志 | `cat ~/.openclaw/workspace/logs/sec_news_cron.log` |
| 查看上次运行状态 | `cat ~/.openclaw/workspace/data/sec_news_last_run.json` |
| 重置去重库（重新抓取所有文章） | `rm ~/.openclaw/workspace/data/sec_news_seen.json` |
| 查看 cron 配置 | `crontab -l \| grep sec_news` |
| 手动触发 cron | `run-parts /etc/cron.hourly`（系统级）|

## 添加/移除 RSS 源

编辑 `scripts/crawler.py`，修改 `RSS_FEEDS` 列表：

```python
RSS_FEEDS = [
    {"name": "嘶吼",     "url": "https://www.4hou.com/feed",     "type": "rss"},
    {"name": "先知社区", "url": "https://xz.aliyun.com/feed",    "type": "rss"},
    {"name": "Seebug",   "url": "https://paper.seebug.org/rss/", "type": "rss"},
]
```

## 当前可用 RSS 源

| 来源 | 状态 |
|------|------|
| 嘶吼 | ✅ 稳定 |
| 先知社区 | ✅ 稳定 |
| Seebug Paper | ✅ 偶尔 |

**失效源（已移除）：** FreeBuf（阿里云 WAF）、安全客、T00ls、安全脉搏、SecWiki、极速安全、补天、CNVD（521）、Seebug（空数据）

## 漏洞情报爬虫（vuln_crawler.py）

**功能：** 每日自动抓取全球漏洞情报（CVE），写入 IMA 每日漏洞集合系列。**英文描述自动翻译为中文。**

### 智能翻译规则

英文内容翻译为中文时，遵循以下规则：

| 类型 | 处理方式 | 示例 |
|------|----------|------|
| CVE 编号 | 保留英文，加粗显示 | **CVE-2024-1234** |
| 组件名 | 保留英文 | apache, nginx, MySQL, WordPress |
| 技术术语 | 保留英文 | RCE, SSRF, XSS, SQL Injection, zero-day |
| 协议名 | 保留英文 | HTTPS, TCP, DNS, OAuth, JWT |
| 产品/平台 | 保留英文 | Kubernetes, Docker, GitLab |
| 描述性文字 | 翻译为中文 | The vulnerability allows... → 该漏洞允许... |

### 数据源（2026-03 实测可用）

| 来源 | 类型 | 状态 | 说明 |
|------|------|------|------|
| NVD | REST API | ✅ 主力 | 每天 7 次查询，覆盖近 7 天所有 CVE |
| cxsecurity | RSS | ✅ 备用 | SSL 证书跳过，仍可抓取 |
| 安全客 | RSS | ✅ 备用 | 国内唯一稳定可用的安全 RSS |

**不可用来源：** CNVD（HTTP 521）、Seebug（空数据）、补天（空白内容）、工信部（DNS 失败）、CNNVD（无真实 RSS）

**运行命令：**
```bash
IMA_OPENAPI_CLIENTID=... IMA_OPENAPI_APIKEY=... \
MINIMAX_API_KEY=... MINIMAX_GROUP_ID=... \
python3 ~/.openclaw/workspace/skills/sec-news-crawler/scripts/vuln_crawler.py
```

**笔记系列：** IMA「漏洞情报」笔记本中，标题格式为 `🔐 漏洞情报 YYYY-MM-DD`，每天一篇。

**去重库：** `data/vuln_seen.json`（CVE ID 去重）
**运行日志：** `logs/vuln_cron.log`

### 环境变量

| 变量 | 必须 | 说明 |
|------|------|------|
| `IMA_OPENAPI_CLIENTID` | 是 | IMA 笔记凭证 |
| `IMA_OPENAPI_APIKEY` | 是 | IMA 笔记凭证 |
| `MINIMAX_API_KEY` | 是（翻译） | MiniMax API Key（复用 OpenClaw 配置的 key 即可） |

## IMA 凭证

需要环境变量（已在 `scripts/run.sh` 中硬编码，如需更新：

- `IMA_OPENAPI_CLIENTID`
- `IMA_OPENAPI_APIKEY`
