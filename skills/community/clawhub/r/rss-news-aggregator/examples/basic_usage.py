"""
RSS News Aggregator - 基础使用示例
"""
from scripts.rss_engine import RSSAggregator


def main():
    agg = RSSAggregator()

    print("=" * 50)
    print("示例 1: 添加自定义 RSS 源并抓取")
    print("=" * 50)
    agg.add_feed("https://news.ycombinator.com/rss", name="Hacker News")
    articles = agg.fetch_all(limit_per_feed=5, total_limit=10)
    print(f"抓取到 {len(articles)} 篇文章")
    for a in articles[:3]:
        print(f"  - [{a['source']}] {a['title'][:60]}...")

    print("\n" + "=" * 50)
    print("示例 2: 使用内置热门源")
    print("=" * 50)
    agg2 = RSSAggregator()
    feeds = agg2.get_builtin_feeds("tech")
    print(f"内置 tech 分类源: {list(feeds.keys())}")

    print("\n" + "=" * 50)
    print("示例 3: 关键词过滤")
    print("=" * 50)
    demo_articles = [
        {"title": "New AI model released by OpenAI", "summary": "GPT-5 is here", "source": "AI News", "link": "#", "published": "2026-04-27"},
        {"title": "Python 4.0 roadmap announced", "summary": "Major changes coming", "source": "Dev.to", "link": "#", "published": "2026-04-26"},
        {"title": "Cloud costs optimization guide", "summary": "Save money on AWS", "source": "TechCrunch", "link": "#", "published": "2026-04-25"},
    ]
    filtered = agg2.filter_by_keyword(demo_articles, ["AI", "Python"])
    print(f"关键词 'AI' 或 'Python' 匹配到 {len(filtered)} 篇文章:")
    for a in filtered:
        print(f"  - {a['title']}")

    print("\n" + "=" * 50)
    print("示例 4: 生成 Markdown 报告")
    print("=" * 50)
    report = agg2.generate_markdown_report(demo_articles, title="今日精选")
    print(report[:800] + "\n...")

    print("\n" + "=" * 50)
    print("示例 5: 按来源筛选")
    print("=" * 50)
    from_dev = agg2.search_by_source(demo_articles, "Dev")
    print(f"来自 Dev 源的文章: {[a['title'] for a in from_dev]}")


if __name__ == "__main__":
    main()
