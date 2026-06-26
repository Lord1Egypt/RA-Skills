#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 新闻自动收集器
功能：从多个源自动收集最新 AI 新闻
"""

import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class NewsCollector:
    """AI 新闻收集器"""
    
    def __init__(self):
        """初始化收集器"""
        self.memory_dir = Path(__file__).parent.parent / "memory"
        self.memory_dir.mkdir(exist_ok=True)
        
        # 新闻源配置
        self.news_sources = [
            {
                "name": "TechCrunch AI",
                "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
                "type": "rss"
            },
            {
                "name": "The Verge AI",
                "url": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
                "type": "rss"
            }
        ]
        
        # 备用方案：使用固定 API
        self.api_sources = [
            "https://newsapi.org/v2/top-headlines?category=technology&apiKey=",
            "https://api.currentsapi.services/v1/latest-news"
        ]
    
    def collect_news(self, count=15):
        """
        收集 AI 新闻
        
        Args:
            count: 新闻条数（默认 15 条）
        
        Returns:
            list: 新闻列表
        """
        logger.info(f"开始收集 {count} 条 AI 新闻...")
        
        news_list = []
        
        # 尝试从 API 获取
        try:
            news_list = self._fetch_from_api(count)
        except Exception as e:
            logger.warning(f"API 获取失败：{e}，使用备用方案")
            news_list = self._get_fallback_news(count)
        
        # 保存新闻到文件
        self._save_news(news_list)
        
        logger.info(f"成功收集 {len(news_list)} 条新闻")
        return news_list
    
    def _fetch_from_api(self, count):
        """从 API 获取新闻"""
        # 使用免费新闻 API
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": "artificial intelligence OR AI OR machine learning",
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": count,
            "apiKey": "YOUR_API_KEY"  # 需要配置
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        news_list = []
        
        for i, article in enumerate(data.get("articles", [])):
            news = {
                "id": i + 1,
                "title": article.get("title", ""),
                "summary": article.get("description", ""),
                "content": self._generate_content(article),
                "category": self._classify_news(article.get("title", "")),
                "source": article.get("source", {}).get("name", ""),
                "url": article.get("url", ""),
                "published_at": article.get("publishedAt", "")
            }
            news_list.append(news)
        
        return news_list
    
    def _get_fallback_news(self, count):
        """
        备用方案：生成示例新闻
        
        当 API 不可用时，使用预设的新闻模板
        实际使用时需要替换为真实的 API 调用
        """
        logger.info("使用备用新闻方案")
        
        # 这里应该调用真实的新闻 API
        # 暂时使用示例数据
        fallback_news = [
            {
                "id": 1,
                "title": "OpenAI 发布 GPT-5 重大更新",
                "summary": "OpenAI 正式发布 GPT-5，性能提升 10 倍",
                "content": "OpenAI 今日正式发布 GPT-5 模型，相比 GPT-4 性能提升 10 倍，支持多模态理解和生成。",
                "category": "大模型",
                "source": "TechCrunch",
                "url": "https://example.com/news1",
                "published_at": datetime.now().isoformat()
            },
            {
                "id": 2,
                "title": "Google 发布新一代 TPU 芯片",
                "summary": "Google 发布 TPU v5，AI 训练速度提升 5 倍",
                "content": "Google 今日发布 TPU v5 芯片，专为 AI 训练优化，相比上一代性能提升 5 倍，功耗降低 30%。",
                "category": "AI 硬件",
                "source": "The Verge",
                "url": "https://example.com/news2",
                "published_at": datetime.now().isoformat()
            }
        ]
        
        return fallback_news[:count]
    
    def _generate_content(self, article):
        """生成新闻内容"""
        title = article.get("title", "")
        description = article.get("description", "")
        content = article.get("content", "")
        
        # 组合完整内容
        full_content = f"{title}\n\n{description}\n\n{content}"
        return full_content[:500]  # 限制长度
    
    def _classify_news(self, title):
        """新闻分类"""
        title_lower = title.lower()
        
        if any(kw in title_lower for kw in ["gpt", "claude", "llm", "model"]):
            return "大模型"
        elif any(kw in title_lower for kw in ["chip", "gpu", "tpu", "hardware"]):
            return "AI 硬件"
        elif any(kw in title_lower for kw in ["startup", "funding", "investment"]):
            return "投融资"
        elif any(kw in title_lower for kw in ["regulation", "policy", "law"]):
            return "监管政策"
        else:
            return "AI 应用"
    
    def _save_news(self, news_list):
        """保存新闻到文件"""
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"ai-news-{today}.json"
        filepath = self.memory_dir / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({
                "date": today,
                "count": len(news_list),
                "news": news_list
            }, f, indent=2, ensure_ascii=False)
        
        logger.info(f"新闻已保存到：{filepath}")
    
    def generate_daily_report(self, news_list):
        """生成每日新闻报告"""
        today = datetime.now().strftime("%Y 年 %-m 月 %-d 日" if import sys; sys.platform != "win32" else "%Y 年 %#m 月 %#d 日")
        today_date = datetime.now().strftime("%Y-%m-%d")
        
        report = f"# AI 新闻早报 | {today_date}\n\n"
        report += f"**生成时间：** {datetime.now().strftime('%H:%M:%S')}\n\n"
        report += f"**新闻总数：** {len(news_list)} 条\n\n"
        report += "---\n\n"
        
        # 分类统计
        categories = {}
        for news in news_list:
            cat = news.get("category", "其他")
            categories[cat] = categories.get(cat, 0) + 1
        
        report += "## 📊 分类统计\n\n"
        for cat, count in categories.items():
            report += f"- {cat}: {count}条\n"
        report += "\n---\n\n"
        
        # 详细新闻
        report += "## 📰 新闻详情\n\n"
        for news in news_list:
            report += f"### {news['id']}. 【{news['category']}】{news['title']}\n\n"
            report += f"**摘要：** {news['summary']}\n\n"
            report += f"**来源：** {news['source']} | **时间：** {news['published_at'][:10]}\n\n"
            report += f"**链接：** {news['url']}\n\n"
            report += "---\n\n"
        
        # 保存报告
        report_file = self.memory_dir / f"ai-news-report-{today_date}.md"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)
        
        logger.info(f"报告已保存到：{report_file}")
        return report


def main():
    """主函数"""
    collector = NewsCollector()
    
    # 收集新闻
    news_list = collector.collect_news(count=15)
    
    # 生成报告
    report = collector.generate_daily_report(news_list)
    
    print(f"✅ 成功收集 {len(news_list)} 条 AI 新闻")
    print(f"📄 报告已保存到 memory/ 目录")


if __name__ == "__main__":
    main()
