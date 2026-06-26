---
name: sina-daily-news
description: "抓取新浪财经 7×24 实时新闻流，自动分类生成结构化日报。每类新闻按时间线排列，标注来源和阅读量。适合每日早间财经/政治/科技新闻速览。"
metadata:
  version: 1.0.0
  author: paudy
  license: MIT-0
---

# 新浪每日新闻抓取

从新浪财经 7×24 实时新闻流自动抓取、分类、生成每日新闻报告。

## 功能

- 抓取 `https://finance.sina.com.cn/7x24/?tag=0` 的 7×24 实时新闻
- 自动分类：国际政治军事 / 中国政治外交 / 中国财经股市 / 科技与AI / 产业与制造 / 社会热点
- 提取每条新闻的时间、标题、正文、来源、阅读量
- 生成结构化 Markdown 报告

## 使用方法

### 快速抓取

使用 OpenClaw 的 `web_fetch` 工具抓取页面，然后将内容传入解析脚本：

```bash
# 1. 用 web_fetch 抓取 https://finance.sina.com.cn/7x24/?tag=0 (maxChars: 15000)
# 2. 将抓取内容传入脚本
python scripts/sina_daily_news.py
```

### Cron 定时任务

建议配置 OpenClaw Cron 任务，每天早晨 8:00 自动执行：

```json
{
  "name": "新浪每日新闻日报",
  "schedule": { "kind": "cron", "expr": "0 8 * * *", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "1. web_fetch 抓取 https://finance.sina.com.cn/7x24/?tag=0 (maxChars: 15000)\n2. 将内容传入 scripts/sina_daily_news.py\n3. 输出报告到聊天 + 保存到 memory/sina_news_YYYY-MM-DD.md",
    "timeoutSeconds": 300
  },
  "delivery": { "mode": "announce", "channel": "last" }
}
```

## 脚本参数

| 参数 | 说明 |
|------|------|
| stdin | 传入抓取到的新闻文本（推荐方式） |
| argv[1] | 直接传入新闻文本字符串 |

## 输出格式

```markdown
# 📰 新浪每日新闻日报 — YYYY-MM-DD
> 数据源：新浪财经 7×24 实时新闻

## 一、国际政治军事（N条）
- **[HH:MM:SS] 标题** | 来源 | 阅读 X万
  正文摘要...

## 二、中国财经股市（N条）
...
```

## 分类规则

| 类别 | 关键词示例 |
|------|-----------|
| 国际政治军事 | 伊朗、美国、以色列、北约、俄罗斯、外交、总统 |
| 中国政治外交 | 中国、国务院、外交部、新华社、香港、台湾 |
| 中国财经股市 | A股、沪指、央行、利率、美联储、IPO、房地产 |
| 科技与AI | AI、大模型、芯片、华为、京东方、字节跳动 |
| 产业与制造 | 汽车、飞机、船舶、轨道交通、电站 |
| 社会热点 | 交通事故、食品安全、天气预警、邮轮 |

## 文件结构

```
sina-daily-news/
├── SKILL.md                    # 本文件
├── scripts/
│   └── sina_daily_news.py      # 新闻解析脚本
└── package.json                # ClawHub 元数据
```

## 故障排除

| 问题 | 解决 |
|------|------|
| web_fetch 403 | 改用 browser 工具打开页面并截图 |
| 解析脚本无输出 | 检查抓取内容是否包含有效新闻格式 |
| 分类不准确 | 编辑脚本中的 CATEGORIES 关键词列表 |

## 与其他新闻源互补

本脚本抓取新浪财经一手新闻流，建议与 web_search 多引擎搜索的新闻日报配合使用，形成双源交叉验证。
