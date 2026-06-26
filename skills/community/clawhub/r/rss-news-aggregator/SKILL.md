# rss-news-aggregator

## 技能概述
RSS 订阅聚合与新闻抓取工具。支持多源 RSS 订阅抓取、文章摘要提取、关键词过滤、去重排序，自动聚合多平台新闻源为统一的阅读流。

## 何时使用
- 需要自动抓取多个网站/博客的最新文章时
- 需要监控特定关键词在行业新闻中的出现时
- 需要对文章进行自动摘要和分类时
- 需要将多个信息源合并为统一输出时
- 需要定时获取新闻更新并做简单分析时

## 使用方法

### 基础用法
```python
from scripts.rss_engine import RSSAggregator

agg = RSSAggregator()

# 添加订阅源
agg.add_feed("https://news.ycombinator.com/rss", name="Hacker News")
agg.add_feed("https://feeds.arstechnica.com/arstechnica/index", name="Ars Technica")

# 抓取所有文章
articles = agg.fetch_all(limit=20)
# -> [{"title": "...", "link": "...", "summary": "...", "source": "Hacker News", "published": "..."}]

# 按关键词过滤
filtered = agg.filter_by_keyword(articles, ["AI", "Python", "cloud"])

# 生成摘要报告
report = agg.generate_summary(filtered)
```

## 文件结构
```
rss-news-aggregator/
├── SKILL.md
├── README.md
├── requirements.txt
├── scripts/
│   └── rss_engine.py          # 核心引擎
├── examples/
│   └── basic_usage.py           # 使用示例
└── tests/
    └── test_rss.py             # 单元测试
```

## 依赖
- `feedparser` — RSS/Atom 解析
- `requests` — HTTP 请求
- `html2text` — HTML 转纯文本摘要

## 标签
rss, news, aggregation, feed, monitoring, content