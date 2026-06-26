# RSS News Aggregator

RSS 新闻聚合器 — 多源订阅抓取、过滤、摘要一站式工具。

## Features

| 功能 | 说明 |
|------|------|
| 多源订阅 | 支持 RSS/Atom 多种格式，同时管理多个订阅源 |
| 文章抓取 | 自动抓取标题、链接、发布时间、摘要、作者 |
| 关键词过滤 | 按关键词白名单/黑名单过滤文章 |
| 自动摘要 | 提取文章正文前 N 字符作为摘要 |
| 去重排序 | 按发布时间排序，去除重复链接 |
| 导出报告 | 生成 Markdown/HTML 格式聚合报告 |
| 内置源 | 预置科技、AI、开发等热门中文/英文 RSS 源 |

## Quick Start

```python
from scripts.rss_engine import RSSAggregator

agg = RSSAggregator()

# 1. 添加订阅源
agg.add_feed("https://news.ycombinator.com/rss", name="Hacker News")
agg.add_feed("https://rsshub.app/github/trending/daily/python", name="GitHub Trending Python")

# 2. 抓取文章
articles = agg.fetch_all(limit=10)
print(f"抓取到 {len(articles)} 篇文章")

# 3. 按关键词过滤
filtered = agg.filter_by_keyword(articles, ["AI", "LLM", "Python"])
print(f"过滤后 {len(filtered)} 篇相关文章")

# 4. 生成摘要报告
report = agg.generate_markdown_report(filtered, title="今日科技要闻")
print(report)

# 5. 使用内置热门源
popular = agg.get_builtin_feeds("tech")
for name, url in popular.items():
    agg.add_feed(url, name=name)
```

## Built-in Feeds

按分类预置的热门订阅源：

| 分类 | 包含源 |
|------|--------|
| `tech` | Hacker News, Ars Technica, TechCrunch, The Verge |
| `ai` | AI News, Paper Digest, HuggingFace Blog |
| `dev` | GitHub Trending, Dev.to, StackOverflow Blog |
| `cn` | 36氪, 少数派, 阮一峰博客 |

```python
# 获取分类下的源列表
tech_feeds = agg.get_builtin_feeds("tech")
ai_feeds = agg.get_builtin_feeds("ai")
cn_feeds = agg.get_builtin_feeds("cn")
```

## Installation

```bash
pip install -r requirements.txt
```

依赖:
- `feedparser>=6.0` — RSS/Atom 解析
- `requests>=2.31` — HTTP 请求
- `html2text>=2024.1` — HTML 转纯文本

## License
MIT