# -*- coding: utf-8 -*-
"""
Report-gama — Telegram 公开信息监控模块
支持：公开频道搜索、TGStat数据、Google site:t.me 搜索
"""

import random
import time
import logging
import re
import json
from datetime import datetime, timedelta
from urllib.parse import quote_plus
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"[ERROR] 缺少必需依赖: {e}")
    print("请运行: pip install requests beautifulsoup4 lxml")
    raise SystemExit(1)

# fake_useragent 初始化（可能联网失败，沙箱环境下使用硬编码UA池）
_UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
]
_has_fake_ua = False
try:
    from fake_useragent import UserAgent
    ua = UserAgent()
    ua.random  # 立即测试一次是否可用
    _has_fake_ua = True
except Exception:
    _has_fake_ua = False

def get_ua():
    if _has_fake_ua:
        try:
            return ua.random
        except Exception:
            return random.choice(_UA_POOL)
    return random.choice(_UA_POOL)

logging.basicConfig(level="INFO", format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 15
REQUEST_RETRIES = 2


# ============================================================
# 俄罗斯医疗器械行业 Telegram 公开频道数据库
# ============================================================
MEDICAL_TG_CHANNELS = {
    "俄罗斯": [
        # 医疗器械行业
        {"name": "Медвестник", "handle": "medvestnik", "url": "https://t.me/s/medvestnik", "category": "行业媒体"},
        {"name": "Vademecum", "handle": "vademecumru", "url": "https://t.me/s/vademecumru", "category": "行业媒体"},
        {"name": "Pharmvestnik", "handle": "pharmvestnik", "url": "https://t.me/s/pharmvestnik", "category": "制药/器械"},
        {"name": "Медицинская Россия", "handle": "medrf", "url": "https://t.me/s/medrf", "category": "行业媒体"},
        {"name": "Про Медицину", "handle": "promedinfo", "url": "https://t.me/s/promedinfo", "category": "医学新闻"},
        {"name": "Доктор на работе", "handle": "doctorwork", "url": "https://t.me/s/doctorwork", "category": "医生社区"},
        {"name": "Медтехника и инновации", "handle": "medtehru", "url": "https://t.me/s/medtehru", "category": "医疗器械"},
        {"name": "Росздравнадзор", "handle": "roszdravnadzor_news", "url": "https://t.me/s/roszdravnadzor_news", "category": "政府监管"},
        {"name": "Закупки МЗ РФ", "handle": "zakupkimz_rf", "url": "https://t.me/s/zakupkimz_rf", "category": "政府采购"},
        {"name": "Госзакупки.Медицина", "handle": "gosmedtender", "url": "https://t.me/s/gosmedtender", "category": "招标公告"},
        {"name": "Рынок медизделий", "handle": "medmarketru", "url": "https://t.me/s/medmarketru", "category": "市场分析"},
        {"name": "Фарм и Медицина", "handle": "farmmedicine", "url": "https://t.me/s/farmmedicine", "category": "制药/器械"},
        {"name": "Маркет WB - Медицина", "handle": "market_wb", "url": "https://t.me/s/market_wb", "category": "电商数据"},
        {"name": "Ozon/WB продавцы", "handle": "ecom_sellers_ru", "url": "https://t.me/s/ecom_sellers_ru", "category": "电商运营"},
        {"name": "Регистрация медизделий", "handle": "medreghelp", "url": "https://t.me/s/medreghelp", "category": "注册认证"},
        {"name": "Медизделия и тендеры", "handle": "medtendery", "url": "https://t.me/s/medtendery", "category": "招标"},
        {"name": "ЭКГ, УЗИ, анализаторы", "handle": "diagnostic_tech", "url": "https://t.me/s/diagnostic_tech", "category": "诊断设备"},
        {"name": "Лабораторная диагностика", "handle": "labdiagnostic", "url": "https://t.me/s/labdiagnostic", "category": "检验设备"},
        {"name": "Санитарное оборудование", "handle": "sanobor", "url": "https://t.me/s/sanobor", "category": "设备"},
        {"name": "Фармсклад. Опт", "handle": "pharmsklad", "url": "https://t.me/s/pharmsklad", "category": "批发渠道"},
    ],
    "哈萨克斯坦": [
        {"name": "Медицина Казахстана", "handle": "medkz", "url": "https://t.me/s/medkz", "category": "行业媒体"},
        {"name": "Минздрав РК", "handle": "mz_rk", "url": "https://t.me/s/mz_rk", "category": "政府"},
        {"name": "Закупки Казахстана", "handle": "zakupkikz", "url": "https://t.me/s/zakupkikz", "category": "招标"},
    ],
    "白俄罗斯": [
        {"name": "Медицина Беларуси", "handle": "medbelarus", "url": "https://t.me/s/medbelarus", "category": "行业媒体"},
        {"name": "Минздрав РБ", "handle": "mz_rb", "url": "https://t.me/s/mz_rb", "category": "政府"},
    ],
}

# 通配品类频道（用于泛搜索）
GENERIC_TG_CHANNELS = [
    {"name": "Telegram Search Archive", "handle": "search", "url": "https://t.me/s/", "category": "搜索存档"},
]


class TelegramMonitor:
    """Telegram 公开信息监控器"""

    def __init__(self, country="俄罗斯", lang="ru"):
        self.country = country
        self.lang = lang
        self.session = self._create_session()
        self.results = []

    def _create_session(self):
        session = requests.Session()
        session.headers.update({
            "User-Agent": get_ua(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ru,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
        })
        return session

    def _make_request(self, url, max_retries=REQUEST_RETRIES):
        for attempt in range(max_retries + 1):
            try:
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:
                    wait = (attempt + 1) * 5
                    logger.warning(f"[TG] 请求频繁，等待 {wait}s: {url[:60]}")
                    time.sleep(wait)
                else:
                    logger.warning(f"[TG] HTTP {response.status_code}: {url[:60]}")
            except requests.RequestException as e:
                logger.warning(f"[TG] 请求失败: {e}")
                time.sleep(3)
        return None

    # --------------------------------------------------------
    # 方法1: Google site:t.me 搜索（覆盖所有公开频道）
    # --------------------------------------------------------
    def search_via_google(self, keywords, max_results=30):
        """
        使用 Google site:t.me 搜索公开 Telegram 信息

        Args:
            keywords: list, 关键词列表（俄语优先）
            max_results: 最大结果数

        Returns:
            list: 搜索结果列表
        """
        if isinstance(keywords, str):
            keywords = [keywords]

        all_results = []
        seen = set()

        for keyword in keywords:
            query = f"site:t.me {keyword}"
            encoded = quote_plus(query)
            url = f"https://www.google.com/search?q={encoded}&hl=ru&lr=lang_ru&num=20"

            logger.info(f"[TG/Google] 搜索: {keyword[:40]}...")
            response = self._make_request(url)

            if not response:
                continue

            soup = BeautifulSoup(response.text, "lxml")
            for item in soup.select("div.g")[:15]:
                try:
                    title_elem = item.select_one("h3")
                    link_elem = item.select_one("a")
                    snippet_elem = item.select_one("div[data-sncf]")
                    if not (title_elem and link_elem):
                        continue
                    link = link_elem.get("href", "")
                    if "t.me" not in link:
                        continue
                    if link.startswith("/url?q="):
                        link = link.split("/url?q=")[1].split("&")[0]
                    if link in seen:
                        continue
                    seen.add(link)
                    all_results.append({
                        "title": title_elem.get_text(strip=True),
                        "url": link,
                        "snippet": snippet_elem.get_text(strip=True)[:300] if snippet_elem else "",
                        "source": "Google/site:t.me",
                        "keyword": keyword,
                        "search_time": datetime.now().isoformat(),
                    })
                except Exception:
                    continue

            time.sleep(random.uniform(2, 4))

        all_results.sort(key=lambda r: len(r["snippet"]), reverse=True)
        logger.info(f"[TG/Google] 共采集 {len(all_results)} 条 Telegram 搜索结果")
        self.results = all_results[:max_results]
        return self.results

    # --------------------------------------------------------
    # 方法2: TGStat.ru 搜索（专业 Telegram 统计平台）
    # --------------------------------------------------------
    def search_tgstat(self, keywords, max_results=30):
        """
        通过 TGStat.ru 搜索公开频道和帖子

        TGStat 是 Telegram 官方推荐的分析平台，支持：
        - 按关键词搜索帖子内容
        - 查找相关频道
        - 查看频道统计数据

        Args:
            keywords: list, 关键词列表
            max_results: 最大结果数

        Returns:
            list: 频道/帖子结果
        """
        if isinstance(keywords, str):
            keywords = [keywords]

        all_results = []
        seen = set()

        for keyword in keywords:
            # TGStat 搜索页面（网页版）
            encoded = quote_plus(keyword)
            url = f"https://tgstat.ru/search?query={encoded}&lang=ru"

            logger.info(f"[TG/TGStat] 搜索: {keyword[:40]}...")
            response = self._make_request(url)

            if not response:
                continue

            soup = BeautifulSoup(response.text, "lxml")

            # 搜索结果中的帖子
            for item in soup.select("div.search-item, div.media-body")[:15]:
                try:
                    title_elem = item.select_one("a[href*='/channel/'], a.title")
                    snippet_elem = item.select_one("div.text, p")
                    if not title_elem:
                        continue
                    link = title_elem.get("href", "")
                    if link.startswith("/"):
                        link = "https://tgstat.ru" + link
                    if link in seen:
                        continue
                    seen.add(link)
                    all_results.append({
                        "title": title_elem.get_text(strip=True),
                        "url": link,
                        "snippet": snippet_elem.get_text(strip=True)[:300] if snippet_elem else "",
                        "source": "TGStat.ru",
                        "keyword": keyword,
                        "search_time": datetime.now().isoformat(),
                    })
                except Exception:
                    continue

            time.sleep(random.uniform(1.5, 3))

        # 如果TGStat直接搜索失败，fallback到Google TGStat搜索
        if not all_results:
            logger.info("[TGStat] 直接访问失败，尝试 Google 搜索 TGStat...")
            for keyword in keywords[:5]:
                query = f"site:tgstat.ru {keyword} telegram channel"
                encoded = quote_plus(query)
                url = f"https://www.google.com/search?q={encoded}&hl=ru&num=10"
                response = self._make_request(url)
                if response:
                    soup = BeautifulSoup(response.text, "lxml")
                    for item in soup.select("div.g")[:5]:
                        title_elem = item.select_one("h3")
                        link_elem = item.select_one("a")
                        if title_elem and link_elem:
                            link = link_elem.get("href", "")
                            if "tgstat" in link:
                                all_results.append({
                                    "title": title_elem.get_text(strip=True),
                                    "url": link,
                                    "snippet": "",
                                    "source": "Google/TGStat",
                                    "keyword": keyword,
                                })

        logger.info(f"[TG/TGStat] 共采集 {len(all_results)} 条结果")
        return all_results[:max_results]

    # --------------------------------------------------------
    # 方法3: 抓取已知行业频道最新消息
    # --------------------------------------------------------
    def fetch_known_channels(self, keywords, channels=None, max_per_channel=10):
        """
        抓取已知行业公开频道中包含关键词的最新帖子

        Args:
            keywords: list, 关键词列表
            channels: list, 指定频道列表（默认使用行业频道库）
            max_per_channel: 每个频道最多抓取多少条

        Returns:
            list: 匹配关键词的帖子列表
        """
        if isinstance(keywords, str):
            keywords = [keywords]
        keywords_lower = [kw.lower() for kw in keywords]

        if channels is None:
            channels = MEDICAL_TG_CHANNELS.get(self.country, [])

        matched_posts = []
        seen_urls = set()

        def keyword_matches(text):
            text_lower = text.lower()
            return any(kw.lower() in text_lower for kw in keywords_lower)

        for channel in channels:
            url = channel["url"]
            logger.info(f"[TG/频道] 抓取: {channel['name']} ({channel['handle']})")

            try:
                response = self._make_request(url)
                if not response:
                    logger.warning(f"[TG/频道] 无法访问: {channel['name']}")
                    continue

                soup = BeautifulSoup(response.text, "lxml")

                # 解析 Telegram 频道消息列表
                # Telegram 频道的 HTML 结构
                for post in soup.select("div.message")[:max_per_channel * 2]:
                    try:
                        # 提取时间戳
                        time_elem = post.select_one("div.date a, .time")
                        post_time = time_elem.get_text(strip=True) if time_elem else ""

                        # 提取正文内容
                        text_elem = post.select_one("div.text, .message-text")
                        if not text_elem:
                            continue
                        text = text_elem.get_text(separator=" | ", strip=True)

                        if not keyword_matches(text):
                            continue

                        # 提取链接
                        links = [a.get("href", "") for a in post.select("a")]
                        link = next((l for l in links if "t.me" in l and "join" not in l), "")

                        post_id = post.get("data-post-id", text[:50])
                        if post_id in seen_urls:
                            continue
                        seen_urls.add(post_id)

                        matched_posts.append({
                            "title": text[:100],
                            "url": link or url,
                            "snippet": text[:400],
                            "source": f"TG: @{channel['handle']}",
                            "channel": channel["name"],
                            "category": channel["category"],
                            "post_time": post_time,
                            "keyword_matched": next((k for k in keywords_lower if k in text.lower()), ""),
                            "fetch_time": datetime.now().isoformat(),
                        })
                    except Exception:
                        continue

                # 频道间延迟
                time.sleep(random.uniform(0.8, 2.0))

            except Exception as e:
                logger.warning(f"[TG/频道] {channel['name']} 异常: {e}")
                continue

        # 按相关度排序
        def score(p):
            s = 0
            for kw in keywords_lower:
                if kw in p["title"].lower():
                    s += 5
                if kw in p["snippet"].lower():
                    s += 2
            return s

        matched_posts.sort(key=score, reverse=True)
        logger.info(f"[TG/频道] 匹配到 {len(matched_posts)} 条相关帖子")
        return matched_posts[:max_per_channel * len(channels) // 2]

    # --------------------------------------------------------
    # 方法4: 发现相关频道（通过TGStat或Google）
    # --------------------------------------------------------
    def discover_channels(self, keywords, max_results=15):
        """
        发现与关键词相关的 Telegram 频道

        Args:
            keywords: 关键词列表
            max_results: 最大发现数量

        Returns:
            list: 发现的相关频道信息
        """
        if isinstance(keywords, str):
            keywords = [keywords]

        channels = []

        for keyword in keywords:
            query = f"site:tgstat.ru/channel медицинск telegram {keyword}"
            encoded = quote_plus(query)
            url = f"https://www.google.com/search?q={encoded}&hl=ru&num=15"

            logger.info(f"[TG/发现] 搜索相关频道: {keyword[:40]}...")
            response = self._make_request(url)

            if not response:
                continue

            soup = BeautifulSoup(response.text, "lxml")
            for item in soup.select("div.g")[:8]:
                try:
                    title_elem = item.select_one("h3")
                    link_elem = item.select_one("a")
                    snippet_elem = item.select_one("div[data-sncf]")
                    if not title_elem:
                        continue
                    link = link_elem.get("href", "") if link_elem else ""
                    channels.append({
                        "name": title_elem.get_text(strip=True),
                        "url": link,
                        "snippet": snippet_elem.get_text(strip=True)[:200] if snippet_elem else "",
                        "source": "TGStat Channel Discovery",
                        "keyword": keyword,
                    })
                except Exception:
                    continue

            time.sleep(random.uniform(2, 4))

        # 去重
        seen_urls = set()
        unique = []
        for ch in channels:
            if ch["url"] not in seen_urls:
                seen_urls.add(ch["url"])
                unique.append(ch)

        logger.info(f"[TG/发现] 共发现 {len(unique)} 个相关频道")
        return unique[:max_results]

    # --------------------------------------------------------
    # 方法5: 关键词频率趋势分析（跨频道统计）
    # --------------------------------------------------------
    def keyword_frequency_analysis(self, keywords, channels=None):
        """
        分析关键词在多个频道中的出现频率

        Args:
            keywords: 关键词列表
            channels: 频道列表

        Returns:
            dict: {keyword: {"count": N, "channels": [...], "trend": "rising/stable/declining"}}
        """
        if channels is None:
            channels = MEDICAL_TG_CHANNELS.get(self.country, [])

        analysis = {}
        seen_posts = set()

        for kw in (keywords if isinstance(keywords, list) else [keywords]):
            analysis[kw] = {
                "keyword": kw,
                "count": 0,
                "channels_found_in": [],
                "posts": [],
                "fetch_time": datetime.now().isoformat(),
            }

        for channel in channels:
            url = channel["url"]
            logger.info(f"[TG/词频] 扫描频道: {channel['name']} - {channel['handle']}")

            try:
                response = self._make_request(url)
                if not response:
                    continue

                soup = BeautifulSoup(response.text, "lxml")
                posts = soup.select("div.message")[:50]

                for post in posts:
                    text_elem = post.select_one("div.text, .message-text")
                    if not text_elem:
                        continue
                    text = text_elem.get_text(strip=True)
                    post_id = text[:60]

                    if post_id in seen_posts:
                        continue

                    for kw in (keywords if isinstance(keywords, list) else [keywords]):
                        if kw.lower() in text.lower():
                            seen_posts.add(post_id)
                            analysis[kw]["count"] += 1
                            ch_name = channel["name"]
                            if ch_name not in analysis[kw]["channels_found_in"]:
                                analysis[kw]["channels_found_in"].append(ch_name)
                            analysis[kw]["posts"].append({
                                "channel": ch_name,
                                "snippet": text[:200],
                                "category": channel["category"],
                            })

                time.sleep(random.uniform(0.5, 1.5))

            except Exception as e:
                logger.warning(f"[TG/词频] {channel['name']} 异常: {e}")
                continue

        # 简单趋势判断（基于出现频率和跨频道分布）
        for kw, data in analysis.items():
            if data["count"] > 20 and len(data["channels_found_in"]) >= 5:
                data["trend"] = "高频"
            elif data["count"] > 5:
                data["trend"] = "中频"
            elif data["count"] > 0:
                data["trend"] = "低频"
            else:
                data["trend"] = "未发现"
            data["unique_channels_count"] = len(data["channels_found_in"])
            # 保留最多3个代表性帖子
            data["posts"] = data["posts"][:3]

        return analysis

    # --------------------------------------------------------
    # 整合：运行完整 Telegram 监控
    # --------------------------------------------------------
    def full_monitor(self, keywords, max_results=50):
        """
        完整 Telegram 监控流程

        1. Google site:t.me 搜索
        2. TGStat.ru 搜索
        3. 已知行业频道关键词匹配
        4. 关键词频率分析

        Args:
            keywords: 关键词列表
            max_results: 最大总结果数

        Returns:
            dict: 完整的监控结果
        """
        if isinstance(keywords, str):
            keywords = [keywords]

        logger.info(f"[TG Monitor] 启动完整监控，共 {len(keywords)} 个关键词...")

        results = {
            "monitor_time": datetime.now().isoformat(),
            "country": self.country,
            "keywords": keywords,
            "google_site_results": [],
            "tgstat_results": [],
            "channel_posts": [],
            "discovered_channels": [],
            "keyword_frequency": {},
            "total_results": 0,
        }

        # Step 1: Google site:t.me
        logger.info("[Step 1/5] Google site:t.me 搜索...")
        google_results = self.search_via_google(keywords, max_results=20)
        results["google_site_results"] = google_results

        # Step 2: TGStat
        logger.info("[Step 2/5] TGStat.ru 搜索...")
        tgstat_results = self.search_tgstat(keywords, max_results=15)
        results["tgstat_results"] = tgstat_results

        # Step 3: 已知频道关键词匹配
        logger.info("[Step 3/5] 扫描已知行业公开频道...")
        channel_posts = self.fetch_known_channels(keywords)
        results["channel_posts"] = channel_posts

        # Step 4: 频道发现
        logger.info("[Step 4/5] 发现相关频道...")
        discovered = self.discover_channels(keywords[:5])
        results["discovered_channels"] = discovered

        # Step 5: 关键词频率分析
        logger.info("[Step 5/5] 关键词频率分析...")
        freq_analysis = self.keyword_frequency_analysis(keywords)
        results["keyword_frequency"] = freq_analysis

        # 汇总
        all_items = (
            results["google_site_results"]
            + results["tgstat_results"]
            + [
                {**p, "type": "channel_post"}
                for p in results["channel_posts"]
            ]
        )
        results["total_results"] = len(all_items)

        # 排序：channel_post 优先（更精准），其次按来源
        all_items.sort(key=lambda x: (
            0 if x.get("type") == "channel_post" else 1,
            -len(x.get("snippet", ""))
        ), reverse=True)

        results["all_items"] = all_items[:max_results]

        logger.info(f"[TG Monitor] 完整完成，共 {results['total_results']} 条结果")
        return results

    def export_results(self, results, output_path=None):
        """导出监控结果为JSON"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"telegram_monitor_{timestamp}.json"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        logger.info(f"[TG] 结果已保存: {output_path}")
        return output_path


# ============================================================
# 独立运行入口
# ============================================================
def run_telegram_monitor(country, keywords, modules=None):
    """
    Telegram 监控独立运行函数

    Args:
        country: 国家名
        keywords: 品类关键词 dict{ru:[], en:[], zh:[]}
        modules: 需要执行的方法列表，默认全部

    Returns:
        dict: 监控结果
    """
    modules = modules or ["search", "tgstat", "channels", "discover", "frequency"]
    lang = "ru"

    # 取俄语关键词（最优先）
    kw_list = keywords.get("ru", []) + keywords.get("en", [])
    kw_list = list(set(kw_list))[:20]

    monitor = TelegramMonitor(country=country, lang=lang)

    if "search" in modules or "all" in modules:
        return monitor.full_monitor(kw_list)

    results = {}
    if "search" in modules:
        results["google_site"] = monitor.search_via_google(kw_list)
    if "tgstat" in modules:
        results["tgstat"] = monitor.search_tgstat(kw_list)
    if "channels" in modules:
        results["channel_posts"] = monitor.fetch_known_channels(kw_list)
    if "discover" in modules:
        results["discovered"] = monitor.discover_channels(kw_list[:5])
    if "frequency" in modules:
        results["frequency"] = monitor.keyword_frequency_analysis(kw_list)

    return results


if __name__ == "__main__":
    # 测试示例
    keywords = {
        "ru": ["глюкометр", "тонометр", "медицинское оборудование", "тендер медицина"],
        "en": ["glucometer", "blood pressure monitor"],
    }
    results = run_telegram_monitor("俄罗斯", keywords)
    print(f"\n总计 Telegram 相关信息: {results.get('total_results', 0)} 条")
    for item in results.get("all_items", [])[:5]:
        print(f"\n[{item.get('source', '?')}] {item.get('title', '')[:80]}")
        print(f"  {item.get('snippet', '')[:150]}...")
