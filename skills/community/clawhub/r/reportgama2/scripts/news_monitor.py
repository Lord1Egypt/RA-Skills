# -*- coding: utf-8 -*-
"""
Report-gama — 新闻与行业动态监控模块
抓取目标国家近30天行业新闻、政府公告、社交媒体动态
"""

import random
import time
import logging
import re
import json
from datetime import datetime, timedelta
from urllib.parse import quote_plus

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"[ERROR] 缺少必需依赖: {e}")
    print("请运行: pip install requests beautifulsoup4 lxml")
    raise SystemExit(1)

from config import NEWS_SOURCES, REQUEST_TIMEOUT, REQUEST_RETRIES, USER_AGENTS, PROXY, HTTPS_PROXY, LOG_LEVEL, LOG_FORMAT

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


class NewsMonitor:
    """行业新闻与动态监控"""

    def __init__(self, country="俄罗斯", lang="ru"):
        self.country = country
        self.lang = lang
        self.country_code = self._country_to_code(country)
        self.session = self._create_session()
        self.articles = []

    def _country_to_code(self, country):
        codes = {"俄罗斯": "RU", "哈萨克斯坦": "KZ", "乌兹别克斯坦": "UZ", "白俄罗斯": "BY", "中国": "CN", "美国": "US"}
        return codes.get(country, "RU")

    def _create_session(self):
        session = requests.Session()
        session.headers.update({
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": f"{self.lang},en;q=0.5",
        })
        if PROXY:
            session.proxies = {"http": PROXY, "https": HTTPS_PROXY or PROXY}
        return session

    def _fetch_page(self, url, source_name="", max_retries=1):
        """快速抓取：超时5秒，最多重试1次，防止卡在慢网站"""
        for attempt in range(max_retries + 1):
            try:
                resp = self.session.get(url, timeout=5)  # 5秒超时，快速失败
                if resp.status_code == 200:
                    return resp.text
                elif resp.status_code == 429:
                    wait = (attempt + 1) * 3
                    logger.warning(f"[{source_name}] 429限速，等待{wait}s...")
                    time.sleep(wait)
            except Exception as e:
                logger.warning(f"[{source_name}] 请求失败: {e}")
                if attempt < max_retries:
                    time.sleep(1)
        return None

    def _parse_date(self, date_str):
        """解析各种格式的日期字符串"""
        if not date_str:
            return None
        date_str = date_str.strip()
        ru_months = {
            "января": "01", "февраля": "02", "марта": "03", "апреля": "04",
            "мая": "05", "июня": "06", "июля": "07", "августа": "08",
            "сентября": "09", "октября": "10", "ноября": "11", "декабря": "12",
        }
        for month, num in ru_months.items():
            if month in date_str:
                date_str = re.sub(r'\D', ' ', date_str).strip()
                parts = date_str.split()
                if len(parts) >= 2:
                    return f"2026-{num}-{parts[1].zfill(2)}"
        match = re.search(r'(\d{1,2})[./](\d{1,2})[./](\d{2,4})', date_str)
        if match:
            d, m, y = match.groups()
            y = y if len(y) == 4 else f"20{y}"
            return f"{y}-{m.zfill(2)}-{d.zfill(2)}"
        return None

    def _extract_article_info(self, item, source_name, source_lang):
        """从搜索结果项中提取文章信息"""
        article = {"source": source_name, "lang": source_lang}
        title_elem = (
            item.select_one("h2") or item.select_one("h3") or
            item.select_one("a") or item.select_one(".title") or
            item.select_one("[class*='title']")
        )
        if title_elem:
            article["title"] = title_elem.get_text(strip=True)
            if title_elem.name == "a" and title_elem.get("href"):
                article["url"] = title_elem.get("href")
            else:
                link = item.select_one("a[href]")
                if link:
                    article["url"] = link.get("href")
        snippet = (
            item.select_one(".snippet") or item.select_one(".abstract") or
            item.select_one("[class*='snippet']") or item.select_one("[class*='desc']") or
            item.select_one("p")
        )
        if snippet:
            article["snippet"] = snippet.get_text(strip=True)[:300]
        date_elem = (
            item.select_one(".date") or item.select_one("[class*='date']") or
            item.select_one("time") or item.select_one("[class*='time']")
        )
        if date_elem:
            date_str = date_elem.get("datetime") or date_elem.get_text(strip=True)
            article["date"] = self._parse_date(date_str)
        else:
            article["date"] = datetime.now().strftime("%Y-%m-%d")
        return article

    def monitor_industry_news(self, category_keywords, days=30):
        """监控行业新闻"""
        logger.info(f"[新闻监控] 开始抓取近{days}天行业新闻...")
        all_articles = []
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        ru_keywords = category_keywords.get("ru", [])
        en_keywords = category_keywords.get("en", [])

        sources_config = NEWS_SOURCES.get(self.country_code, {})

        for category_name, sources in sources_config.items():
            # 限制每个类别最多2个来源，防止请求过多
            for source in sources[:2]:
                source_name = source["name"]
                source_url = source["url"]
                source_lang = source["lang"]
                # 每个来源最多搜2个关键词
                for kw in (ru_keywords[:2] + en_keywords[:1]):
                    try:
                        search_url = self._build_news_url(source_url, kw, source_lang)
                        logger.info(f"[{source_name}] 抓取: {kw[:30]}...")
                        html = self._fetch_page(search_url, source_name)
                        if not html:
                            continue
                        soup = BeautifulSoup(html, "lxml")
                        articles_found = self._extract_from_soup(soup, source_name, source_lang)
                        all_articles.extend(articles_found)
                        time.sleep(random.uniform(0.3, 0.8))
                    except Exception as e:
                        logger.error(f"[{source_name}] 抓取失败: {e}")

        news_results = self._search_news_via_engine(ru_keywords + en_keywords[:3], days)
        all_articles.extend(news_results)

        seen_urls = set()
        unique_articles = []
        for art in all_articles:
            url = art.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_articles.append(art)

        unique_articles.sort(key=lambda x: x.get("date", "1900-01-01"), reverse=True)
        recent = [a for a in unique_articles if a.get("date", "") >= cutoff_date]

        logger.info(f"[新闻监控] 共采集 {len(unique_articles)} 条（近{days}天 {len(recent)} 条）")
        self.articles = recent if recent else unique_articles[:50]
        return self.articles

    def _build_news_url(self, source_url, keyword, lang="ru"):
        keyword_enc = quote_plus(keyword)
        if "yandex" in source_url.lower():
            return f"https://news.search.yandex.ru/news?q={keyword_enc}&lr={self.country_code}"
        elif "google" in source_url.lower():
            return f"https://news.google.com/search?q={keyword_enc}&hl={lang}&gl={self.country_code}"
        elif "rbc" in source_url.lower():
            return f"https://www.rbc.ru/search/?query={keyword_enc}"
        elif "medvestnik" in source_url.lower():
            return f"https://medvestnik.ru/search?q={keyword_enc}"
        elif "vademecum" in source_url.lower():
            return f"https://vademec.ru/search/?q={keyword_enc}"
        else:
            return f"{source_url}/search?q={keyword_enc}"

    def _extract_from_soup(self, soup, source_name, source_lang):
        articles = []
        selectors = [
            "article", ".article", ".news-item", ".news-article",
            "[class*='article']", "[class*='news-item']",
            ".b-media-news__item", ".list-news__item"
        ]
        for selector in selectors:
            items = soup.select(selector)
            if items:
                for item in items[:10]:
                    art = self._extract_article_info(item, source_name, source_lang)
                    if art.get("title") and len(art.get("title", "")) > 10:
                        articles.append(art)
                if articles:
                    break
        return articles

    def _search_news_via_engine(self, keywords, days=30):
        articles = []
        # 最多搜3个关键词，每个最多8条
        for kw in keywords[:3]:
            url = f"https://news.google.com/search?q={quote_plus(kw)}&hl={self.lang}&gl={self.country_code}&tbs=qdr:m"
            logger.info(f"[Google News] {kw[:30]}...")
            html = self._fetch_page(url, "Google News")
            if html:
                soup = BeautifulSoup(html, "lxml")
                for item in soup.select("article")[:8]:
                    try:
                        title = item.get_text(strip=True)
                        link = item.select_one("a[href]")
                        href = link.get("href", "") if link else ""
                        if "/articles/" in href or href.startswith("."):
                            href = "https://news.google.com" + href if href.startswith("/") else href
                        articles.append({
                            "title": title[:200],
                            "url": href,
                            "source": "Google News",
                            "lang": self.lang,
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "keyword": kw,
                        })
                    except Exception:
                        continue
            time.sleep(random.uniform(0.3, 0.8))
        return articles

    def monitor_government_announcements(self, category_keywords):
        """监控政府部门公告（快速版：最多抓2个来源，防止超时）"""
        articles = []
        gov_sources = [
            ("Росздравнадзор", "https://roszdravnadzor.gov.ru/news"),
            ("Минздрав России", "https://minzdrav.gov.ru/news"),
            ("ФАС России", "https://fas.gov.ru/news"),
        ]
        # 只抓第一个（最快的），其余跳过避免超时
        for name, url in gov_sources[:1]:
            try:
                logger.info(f"[政府公告] 抓取 {name}...")
                html = self._fetch_page(url, name)
                if html:
                    soup = BeautifulSoup(html, "lxml")
                    for item in soup.select("article, .news-item, .announcement")[:5]:
                        title_elem = item.select_one("h3, h2, a")
                        if title_elem:
                            articles.append({
                                "title": title_elem.get_text(strip=True)[:200],
                                "url": item.select_one("a").get("href", "") if item.select_one("a") else "",
                                "source": name,
                                "lang": "ru",
                                "date": datetime.now().strftime("%Y-%m-%d"),
                                "type": "government",
                            })
            except Exception as e:
                logger.warning(f"[{name}] 失败: {e}")
        return articles

    def generate_news_brief(self, articles=None):
        """生成新闻简报（Markdown格式）"""
        articles = articles or self.articles
        if not articles:
            return "## 📰 新闻动态\n\n（暂无数据，建议稍后重试）"
        by_source = {}
        for art in articles:
            src = art.get("source", "Unknown")
            if src not in by_source:
                by_source[src] = []
            by_source[src].append(art)
        brief = "## 📰 新闻动态\n\n"
        brief += f"_统计时间：{datetime.now().strftime('%Y-%m-%d')} | 共采集 {len(articles)} 条_\n\n"
        for source, arts in by_source.items():
            brief += f"### 📌 {source}（{len(arts)} 条）\n\n"
            for i, art in enumerate(arts[:10], 1):
                date = art.get("date", "未知日期")
                title = art.get("title", "无标题")
                snippet = art.get("snippet", "")
                url = art.get("url", "")
                brief += f"**{i}. {title}**\n"
                brief += f"- 📅 {date} | 📎 来源: {source}\n"
                if snippet:
                    brief += f"- 📝 {snippet[:150]}...\n"
                if url:
                    brief += f"- 🔗 [查看原文]({url})\n"
                brief += "\n"
        return brief


if __name__ == "__main__":
    monitor = NewsMonitor(country="俄罗斯", lang="ru")
    keywords = {"ru": ["глюкометр", "медицинское оборудование"], "en": ["blood glucose meter Russia"]}
    articles = monitor.monitor_industry_news(keywords, days=30)
    print(f"采集到 {len(articles)} 条新闻")
    for a in articles[:3]:
        print(f"  [{a.get('date')}] {a.get('title')}")
