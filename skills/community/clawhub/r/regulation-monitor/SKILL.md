---
name: regulation-monitor
description: "监控中国金融监管机构网站（国家金融监管总局NFRA、证监会CSRC、央行PBOC等），抓取最新监管政策、行政处罚、通知公告、风险提示等内容，并以标题+摘要格式输出，支持Word和纯文本。当用户说\"帮我看看最新的监管动态\"、\"查一下最新监管政策\"、\"有没有新的处罚案例\"、\"监管有什么新动态\"、\"看看NFRA/证监会/央行最新发布了什么\"时，必须使用此Skill。即使用户只是问\"最近有什么监管新闻\"，也应优先触发此Skill。"
---

# 监管动态追踪 Skill

帮助用户追踪中国主要金融监管机构的最新动态，包括政策法规、行政处罚、通知公告和风险提示，并整理输出结构化摘要。

---

## 前置依赖

`scripts/crawler.py` 依赖以下第三方 Python 包，首次使用前需安装：

```bash
pip install requests beautifulsoup4
```

| 包名 | 用途 |
|------|------|
| `requests` | 发送 HTTP 请求，抓取监管机构网页 |
| `beautifulsoup4` | 解析 HTML 页面，提取标题、日期、正文等字段 |

---

## 执行流程

### Step 1：抓取网页内容

使用 `scripts/crawler.py` 获取目标页面内容。脚本支持指定监管机构（`--regulator`）和回溯天数（`--days`）。

**监管机构参数说明：**
- `nfra`: 国家金融监督管理总局
- `csrc`: 证监会
- `pboc`: 央行
- `all`: 所有机构（默认值）

**执行示例：**
```bash
# 抓取所有机构最近 14 天的动态
python scripts/crawler.py --days 14

# 抓取所有机构最近 14 天的动态（明确指定 all）
python scripts/crawler.py --regulator all --days 14

# 仅抓取监管总局最近 14 天的动态
python scripts/crawler.py --regulator nfra --days 14

# 仅抓取证监会最近 14 天的动态
python scripts/crawler.py --regulator csrc --days 14

# 仅抓取央行最近 14 天的动态
python scripts/crawler.py --regulator pboc --days 14
```


### Step 2：处理正文内容

对 Step 1 输出的每条动态：
- 如果包含「📖 正文内容」字段，对该正文进行总结，提炼核心要点（3~5条要点，每条不超过50字）
- 如果只有「📝 摘要」字段，直接使用摘要

### Step 3：结构化输出

用 **Markdown 格式**输出，确保链接可点击。按以下格式输出每条动态：

```markdown
## [📌 标题文字](原文链接)

📅 **日期：** YYYY-MM-DD

📝 **要点：**
- 要点1
- 要点2
- 要点3

📎 **附件：** [PDF 下载](pdf链接) | [DOC 下载](doc链接)

---
```

所有动态输出完毕后，最后用 2~3 句话给出整体趋势判断。

