# -*- coding: utf-8 -*-
"""
Report-gama — VKontakte (ВКонтакте) 公开信息监控模块
支持：公开群组/公开页面搜索、Google site:vk.com 搜索、VK 帖子分析
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

# fake_useragent 初始化（可能联网失败，使用硬编码UA池）
_UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
]
_has_fake_ua = False
try:
    from fake_useragent import UserAgent
    ua = UserAgent()
    ua.random  # 立即测试一次
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
# 俄罗斯医疗器械/电商行业 VK 群组与公开页面数据库
# ============================================================
VK_INDUSTRY_GROUPS = {
    "俄罗斯": [
        # 电商卖家群 — Wildberries / Ozon
        {"name": "Продавцы Wildberries", "screen_name": "wildberries_sellers", "url": "https://vk.com/wall-197779475", "category": "电商-WB"},
        {"name": "Wildberries Официальное сообщество", "screen_name": "wildberries", "url": "https://vk.com/wildberries", "category": "电商-WB"},
        {"name": "Бизнес на Wildberries", "screen_name": "wb_business", "url": "https://vk.com/wb_business", "category": "电商-WB"},
        {"name": "Ozon Продавцы", "screen_name": "ozon_sellers", "url": "https://vk.com/ozon_sellers", "category": "电商-Ozon"},
        {"name": "Ozon Официальная группа", "screen_name": "ozonru", "url": "https://vk.com/ozonru", "category": "电商-Ozon"},
        {"name": "Маркетплейсы Россия", "screen_name": "marketplaces_ru", "url": "https://vk.com/marketplaces_ru", "category": "电商综合"},
        {"name": "Селлерский клуб", "screen_name": "seller_club", "url": "https://vk.com/seller_club", "category": "电商综合"},
        # 医疗器械行业
        {"name": "Медицинское оборудование", "screen_name": "med_equip", "url": "https://vk.com/med_equip", "category": "医疗器械"},
        {"name": "Медтехника. Продажа", "screen_name": "medtech_sale", "url": "https://vk.com/medtech_sale", "category": "医疗器械"},
        {"name": "Медицина и технологии", "screen_name": "med_tech_ru", "url": "https://vk.com/med_tech_ru", "category": "医疗器械"},
        {"name": "Регистрация медизделий", "screen_name": "medreg_ru", "url": "https://vk.com/medreg_ru", "category": "注册认证"},
        {"name": "Медицинские приборы", "screen_name": "medical_devices_ru", "url": "https://vk.com/medical_devices_ru", "category": "医疗器械"},
        {"name": "Лабораторное оборудование", "screen_name": "lab_equip_ru", "url": "https://vk.com/lab_equip_ru", "category": "检验设备"},
        {"name": "Здравоохранение РФ", "screen_name": "healthcare_rf", "url": "https://vk.com/healthcare_rf", "category": "医疗卫生"},
        {"name": "Росздравнадзор", "screen_name": "roszdravnadzor", "url": "https://vk.com/roszdravnadzor", "category": "政府监管"},
        # B2B / 采购
        {"name": "Медзакупки", "screen_name": "medzakupki", "url": "https://vk.com/medzakupki", "category": "政府采购"},
        {"name": "Тендеры медицина", "screen_name": "med_tenders", "url": "https://vk.com/med_tenders", "category": "招标"},
        {"name": "Госзакупки РФ", "screen_name": "goszakupki_rf", "url": "https://vk.com/goszakupki_rf", "category": "政府采购"},
        # 行业媒体
        {"name": "Медвестник", "screen_name": "medvestnik", "url": "https://vk.com/medvestnik", "category": "行业媒体"},
        {"name": "Vademecum", "screen_name": "vademecum_ru", "url": "https://vk.com/vademecum_ru", "category": "行业媒体"},
    ],
    "哈萨克斯坦": [
        {"name": "Медицина Казахстан", "screen_name": "med_kz", "url": "https://vk.com/med_kz", "category": "医疗卫生"},
        {"name": "Медтехника KZ", "screen_name": "medtech_kz", "url": "https://vk.com/medtech_kz", "category": "医疗器械"},
        {"name": "Здравоохранение KZ", "screen_name": "health_kz", "url": "https://vk.com/health_kz", "category": "医疗卫生"},
    ],
    "白俄罗斯": [
        {"name": "Медицина Беларуси", "screen_name": "med_by", "url": "https://vk.com/med_by", "category": "医疗卫生"},
        {"name": "Медтехника Беларусь", "screen_name": "medtech_by", "url": "https://vk.com/medtech_by", "category": "医疗器械"},
    ],
}

# 泛行业 VK 页面（用于补充搜索）
GENERIC_VK_PAGES = [
    {"name": "VK Здоровье", "screen_name": "health", "url": "https://vk.com/health", "category": "健康"},
    {"name": "Аптека.ру", "screen_name": "apteka_ru", "url": "https://vk.com/apteka_ru", "category": "药房"},
]


class VKMonitor:
    """VKontakte 公开信息监控器"""

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
                # 每次请求随机更换 UA
                self.session.headers.update({"User-Agent": get_ua()})
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:
                    wait = (attempt + 1) * 5
                    logger.warning(f"[VK] 请求频繁，等待 {wait}s: {url[:60]}")
                    time.sleep(wait)
                else:
                    logger.warning(f"[VK] HTTP {response.status_code}: {url[:60]}")
            except requests.RequestException as e:
                logger.warning(f"[VK] 请求失败: {e}")
                time.sleep(3)
        return None

    # --------------------------------------------------------
    # 方法1: Google site:vk.com 搜索（覆盖所有公开内容）
    # --------------------------------------------------------
    def search_vk_public(self, keyword, group_type="all", max_results=30):
        """
        搜索 VK 公开群组/页面

        Args:
            keyword: str, 搜索关键词（俄语优先）
            group_type: str, 类型筛选 — "group"(群组), "page"(公开页面), "all"(全部)
            max_results: int, 最大结果数

        Returns:
            list: 搜索结果列表
        """
        results = []
        seen = set()

        # 构建搜索查询
        if group_type == "group":
            query = f"site:vk.com {keyword}"
        elif group_type == "page":
            query = f"site:vk.com {keyword}"
        else:
            query = f"site:vk.com {keyword}"

        encoded = quote_plus(query)
        url = f"https://www.google.com/search?q={encoded}&hl=ru&lr=lang_ru&num=20"

        logger.info(f"[VK/Google] 搜索公开群组/页面: {keyword[:40]}... (type={group_type})")
        response = self._make_request(url)

        if not response:
            logger.warning(f"[VK/Google] 搜索失败，尝试备用策略")
            return self._search_vk_google_fallback(keyword, group_type, max_results)

        soup = BeautifulSoup(response.text, "lxml")
        for item in soup.select("div.g")[:15]:
            try:
                title_elem = item.select_one("h3")
                link_elem = item.select_one("a")
                snippet_elem = item.select_one("div[data-sncf]")
                if not (title_elem and link_elem):
                    continue
                link = link_elem.get("href", "")
                if "vk.com" not in link:
                    continue
                if link.startswith("/url?q="):
                    link = link.split("/url?q=")[1].split("&")[0]
                if link in seen:
                    continue
                seen.add(link)

                # 判断群组类型
                is_group = bool(re.search(r'vk\.com/(club|public|wall-|group)', link))
                detected_type = "group" if is_group else "page"

                if group_type != "all" and detected_type != group_type:
                    continue

                results.append({
                    "post_id": link,
                    "author": title_elem.get_text(strip=True),
                    "group_name": title_elem.get_text(strip=True),
                    "text": snippet_elem.get_text(strip=True)[:500] if snippet_elem else "",
                    "likes": 0,
                    "comments": 0,
                    "reposts": 0,
                    "publish_date": "",
                    "source_url": link,
                    "keywords": [keyword],
                    "source": "Google/site:vk.com",
                    "group_type": detected_type,
                    "search_time": datetime.now().isoformat(),
                })
            except Exception:
                continue

        time.sleep(random.uniform(2, 4))
        logger.info(f"[VK/Google] 共采集 {len(results)} 条 VK 搜索结果")
        return results[:max_results]

    def _search_vk_google_fallback(self, keyword, group_type, max_results):
        """Google site:vk.com 备用搜索：尝试 wall 搜索"""
        results = []
        query = f"site:vk.com/wall {keyword}"
        encoded = quote_plus(query)
        url = f"https://www.google.com/search?q={encoded}&hl=ru&lr=lang_ru&num=20"

        logger.info(f"[VK/Google/Fallback] 备用搜索: {keyword[:40]}...")
        response = self._make_request(url)

        if not response:
            return results

        soup = BeautifulSoup(response.text, "lxml")
        for item in soup.select("div.g")[:10]:
            try:
                title_elem = item.select_one("h3")
                link_elem = item.select_one("a")
                snippet_elem = item.select_one("div[data-sncf]")
                if not (title_elem and link_elem):
                    continue
                link = link_elem.get("href", "")
                if "vk.com" not in link:
                    continue
                if link.startswith("/url?q="):
                    link = link.split("/url?q=")[1].split("&")[0]

                results.append({
                    "post_id": link,
                    "author": title_elem.get_text(strip=True),
                    "group_name": title_elem.get_text(strip=True),
                    "text": snippet_elem.get_text(strip=True)[:500] if snippet_elem else "",
                    "likes": 0,
                    "comments": 0,
                    "reposts": 0,
                    "publish_date": "",
                    "source_url": link,
                    "keywords": [keyword],
                    "source": "Google/site:vk.com/fallback",
                    "group_type": "group",
                    "search_time": datetime.now().isoformat(),
                })
            except Exception:
                continue

        logger.info(f"[VK/Google/Fallback] 备用搜索采集 {len(results)} 条结果")
        return results[:max_results]

    # --------------------------------------------------------
    # 方法2: 获取 VK 帖子（通过 Google 索引的 wall 帖子）
    # --------------------------------------------------------
    def get_vk_wall_posts(self, keyword, limit=30):
        """
        获取包含关键词的 VK 帖子

        通过 Google site:vk.com/wall 搜索获取已被索引的公开帖子，
        并尝试直接抓取 VK wall 页面获取帖子详情。

        Args:
            keyword: str, 搜索关键词
            limit: int, 最大结果数

        Returns:
            list: 帖子数据列表
        """
        all_posts = []

        # 策略1: Google site:vk.com/wall 搜索
        google_posts = self._get_posts_via_google(keyword, limit)
        all_posts.extend(google_posts)

        # 策略2: 尝试 VK 搜索页面
        vk_posts = self._get_posts_via_vk_search(keyword, limit)
        all_posts.extend(vk_posts)

        # 去重
        seen_urls = set()
        unique_posts = []
        for post in all_posts:
            if post["source_url"] not in seen_urls:
                seen_urls.add(post["source_url"])
                unique_posts.append(post)

        # 尝试抓取帖子详情（互动数据）
        enriched_posts = self._enrich_posts_with_details(unique_posts[:limit])

        logger.info(f"[VK] 关键词 '{keyword[:30]}' 共获取 {len(enriched_posts)} 条帖子")
        self.results = enriched_posts
        return self.results

    def _get_posts_via_google(self, keyword, limit):
        """通过 Google site:vk.com/wall 搜索帖子"""
        posts = []
        seen = set()

        query = f"site:vk.com/wall {keyword}"
        encoded = quote_plus(query)
        url = f"https://www.google.com/search?q={encoded}&hl=ru&lr=lang_ru&num=20"

        logger.info(f"[VK/Posts/Google] 搜索帖子: {keyword[:40]}...")
        response = self._make_request(url)

        if not response:
            return posts

        soup = BeautifulSoup(response.text, "lxml")
        for item in soup.select("div.g")[:15]:
            try:
                title_elem = item.select_one("h3")
                link_elem = item.select_one("a")
                snippet_elem = item.select_one("div[data-sncf]")
                if not (title_elem and link_elem):
                    continue
                link = link_elem.get("href", "")
                if "vk.com" not in link or link in seen:
                    continue
                if link.startswith("/url?q="):
                    link = link.split("/url?q=")[1].split("&")[0]
                seen.add(link)

                # 尝试从 URL 提取 wall ID
                wall_match = re.search(r'wall(-?\d+_\d+)', link)
                post_id = wall_match.group(1) if wall_match else link

                # 尝试提取发布日期
                publish_date = self._extract_date_from_snippet(snippet_elem)

                posts.append({
                    "post_id": post_id,
                    "author": title_elem.get_text(strip=True),
                    "group_name": title_elem.get_text(strip=True),
                    "text": snippet_elem.get_text(strip=True)[:500] if snippet_elem else "",
                    "likes": 0,
                    "comments": 0,
                    "reposts": 0,
                    "publish_date": publish_date,
                    "source_url": link,
                    "keywords": [keyword],
                    "source": "Google/site:vk.com/wall",
                    "search_time": datetime.now().isoformat(),
                })
            except Exception:
                continue

        time.sleep(random.uniform(3, 5))
        logger.info(f"[VK/Posts/Google] Google 搜索获取 {len(posts)} 条帖子")
        return posts

    def _get_posts_via_vk_search(self, keyword, limit):
        """尝试通过 VK 搜索页面获取帖子"""
        posts = []
        try:
            # VK 搜索 URL 格式
            encoded_keyword = quote_plus(keyword)
            search_url = f"https://vk.com/search?c[section]=posts&c[q]={encoded_keyword}"

            logger.info(f"[VK/Posts/VKSearch] VK 搜索: {keyword[:40]}...")
            response = self._make_request(search_url)

            if not response:
                return posts

            soup = BeautifulSoup(response.text, "lxml")

            # 尝试解析 VK 搜索结果页面
            post_blocks = soup.select("div.post")
            if not post_blocks:
                post_blocks = soup.select("div._post_content")

            for block in post_blocks[:10]:
                try:
                    # 提取帖子文本
                    text_elem = block.select_one("div.wall_text")
                    text = text_elem.get_text(strip=True)[:500] if text_elem else ""

                    # 提取来源
                    author_elem = block.select_one("a.author")
                    author = author_elem.get_text(strip=True) if author_elem else ""

                    # 提取互动数据
                    likes = self._extract_count(block, "like", "likes")
                    comments = self._extract_count(block, "reply", "comments")
                    reposts = self._extract_count(block, "share", "reposts")

                    # 提取日期
                    date_elem = block.select_one("span.rel_date") or block.select_one("a.wall_post_more")
                    publish_date = date_elem.get_text(strip=True) if date_elem else ""

                    # 提取 post_id
                    post_elem = block.get("data-post-id", "")
                    wall_link_elem = block.select_one("a.wall_post_more")
                    wall_link = wall_link_elem.get("href", "") if wall_link_elem else ""
                    source_url = f"https://vk.com{wall_link}" if wall_link else ""
                    post_id = post_elem or source_url

                    if not text and not author:
                        continue

                    posts.append({
                        "post_id": post_id,
                        "author": author,
                        "group_name": author,
                        "text": text,
                        "likes": likes,
                        "comments": comments,
                        "reposts": reposts,
                        "publish_date": publish_date,
                        "source_url": source_url,
                        "keywords": [keyword],
                        "source": "VK Search",
                        "search_time": datetime.now().isoformat(),
                    })
                except Exception:
                    continue

            time.sleep(random.uniform(3, 5))
            logger.info(f"[VK/Posts/VKSearch] VK 搜索获取 {len(posts)} 条帖子")
        except Exception as e:
            logger.warning(f"[VK/Posts/VKSearch] VK 搜索失败: {e}")

        return posts

    def _enrich_posts_with_details(self, posts):
        """补充帖子的互动数据"""
        enriched = []
        for post in posts:
            try:
                url = post.get("source_url", "")
                if not url or "vk.com" not in url:
                    enriched.append(post)
                    continue

                # 如果还没有互动数据，尝试获取
                if post.get("likes", 0) == 0 and post.get("comments", 0) == 0:
                    detail = self._fetch_post_detail(url)
                    if detail:
                        post.update(detail)

                enriched.append(post)
                time.sleep(random.uniform(2, 4))
            except Exception:
                enriched.append(post)

        return enriched

    def _fetch_post_detail(self, url):
        """获取单个 VK 帖子的详情"""
        try:
            response = self._make_request(url)
            if not response:
                return None

            soup = BeautifulSoup(response.text, "lxml")

            # 尝试提取点赞/评论/转发
            likes = self._extract_count_from_page(soup, "like")
            comments = self._extract_count_from_page(soup, "reply")
            reposts = self._extract_count_from_page(soup, "share")

            # 提取完整文本
            text_elem = soup.select_one("div.wall_text")
            full_text = text_elem.get_text(strip=True)[:1000] if text_elem else ""

            # 提取发布日期
            date_elem = soup.select_one("span.rel_date")
            publish_date = date_elem.get_text(strip=True) if date_elem else ""

            return {
                "text": full_text or None,  # 不覆盖已有文本
                "likes": likes,
                "comments": comments,
                "reposts": reposts,
                "publish_date": publish_date or None,
            }
        except Exception as e:
            logger.debug(f"[VK] 获取帖子详情失败: {e}")
            return None

    # --------------------------------------------------------
    # 方法3: 分析产品在 VK 上的讨论
    # --------------------------------------------------------
    def analyze_vk_mentions(self, product_name, limit=50):
        """
        分析某产品在 VK 上的讨论情况

        Args:
            product_name: str, 产品名称（俄语/英语）
            limit: int, 最大结果数

        Returns:
            dict: 分析结果
        """
        logger.info(f"[VK/Analyze] 分析产品讨论: {product_name}")

        # 构建多语言搜索关键词
        keywords = [
            product_name,
            f'"{product_name}" отзывы',           # 评论
            f'"{product_name}" обзор',             # 测评
            f'"{product_name}" купить',            # 购买
            f'"{product_name}" цена',              # 价格
            f'"{product_name}" медтехника',        # 医疗设备
        ]

        all_posts = []
        seen_urls = set()

        for kw in keywords:
            try:
                posts = self.get_vk_wall_posts(kw, limit=10)
                for p in posts:
                    if p["source_url"] not in seen_urls:
                        seen_urls.add(p["source_url"])
                        all_posts.append(p)
                time.sleep(random.uniform(3, 5))
            except Exception as e:
                logger.warning(f"[VK/Analyze] 关键词 '{kw}' 搜索失败: {e}")

        # 统计分析
        total_likes = sum(p.get("likes", 0) for p in all_posts)
        total_comments = sum(p.get("comments", 0) for p in all_posts)
        total_reposts = sum(p.get("reposts", 0) for p in all_posts)

        # 按来源分组
        sources = {}
        for p in all_posts:
            src = p.get("source", "unknown")
            sources[src] = sources.get(src, 0) + 1

        # 提取讨论主题
        topics = self._extract_topics(all_posts, product_name)

        result = {
            "product_name": product_name,
            "total_mentions": len(all_posts),
            "total_likes": total_likes,
            "total_comments": total_comments,
            "total_reposts": total_reposts,
            "avg_engagement": round((total_likes + total_comments + total_reposts) / max(len(all_posts), 1), 2),
            "sources_breakdown": sources,
            "topics": topics,
            "posts": all_posts[:limit],
            "analysis_time": datetime.now().isoformat(),
        }

        logger.info(f"[VK/Analyze] 产品 '{product_name}' 共发现 {len(all_posts)} 条提及")
        self.results = all_posts[:limit]
        return result

    # --------------------------------------------------------
    # 方法4: 分析竞品在 VK 的提及情况
    # --------------------------------------------------------
    def get_competitor_vk_presence(self, company_name, limit=30):
        """
        分析竞品公司在 VK 上的提及和活跃度

        Args:
            company_name: str, 竞品公司名称
            limit: int, 最大结果数

        Returns:
            dict: 竞品 VK 分析结果
        """
        logger.info(f"[VK/Competitor] 分析竞品: {company_name}")

        results = {
            "company_name": company_name,
            "official_pages": [],
            "mentions": [],
            "groups": [],
            "statistics": {
                "total_mentions": 0,
                "total_likes": 0,
                "total_comments": 0,
                "estimated_reach": 0,
            },
            "search_time": datetime.now().isoformat(),
        }

        # 搜索官方页面
        try:
            official = self.search_vk_public(company_name, group_type="page", max_results=10)
            results["official_pages"] = official
        except Exception as e:
            logger.warning(f"[VK/Competitor] 官方页面搜索失败: {e}")

        time.sleep(random.uniform(2, 4))

        # 搜索群组讨论
        try:
            groups = self.search_vk_public(company_name, group_type="group", max_results=10)
            results["groups"] = groups
        except Exception as e:
            logger.warning(f"[VK/Competitor] 群组搜索失败: {e}")

        time.sleep(random.uniform(2, 4))

        # 搜索提及
        try:
            mentions = self.get_vk_wall_posts(company_name, limit=limit)
            results["mentions"] = mentions
        except Exception as e:
            logger.warning(f"[VK/Competitor] 提及搜索失败: {e}")

        # 汇总统计
        all_items = results["official_pages"] + results["groups"] + results["mentions"]
        results["statistics"]["total_mentions"] = len(all_items)
        results["statistics"]["total_likes"] = sum(i.get("likes", 0) for i in all_items)
        results["statistics"]["total_comments"] = sum(i.get("comments", 0) for i in all_items)
        results["statistics"]["estimated_reach"] = results["statistics"]["total_likes"] * 10  # 粗略估算

        logger.info(f"[VK/Competitor] 竞品 '{company_name}' 共发现 {len(all_items)} 条相关结果")
        return results

    # --------------------------------------------------------
    # 方法5: 监控 Wildberries 卖家 VK 群
    # --------------------------------------------------------
    def monitor_wb_seller_groups(self, category="医疗设备", limit=30):
        """
        监控 Wildberries 卖家 VK 群的讨论

        Args:
            category: str, 关注品类（用于过滤帖子）
            limit: int, 最大结果数

        Returns:
            list: 相关帖子列表
        """
        logger.info(f"[VK/WB] 监控 WB 卖家群, 品类: {category}")

        # WB 卖家群搜索关键词
        wb_keywords = [
            f"Wildberries {category}",
            f"WB {category}",
            f"Wildberries продавец {category}",
            f"маркетплейс {category} Wildberries",
            f"Wildberries медтехника" if "医疗" in category or "мед" in category.lower() else f"Wildberries {category}",
        ]

        # 获取已知 WB 群组的帖子
        all_posts = []
        wb_groups = VK_INDUSTRY_GROUPS.get(self.country, [])
        wb_relevant_groups = [g for g in wb_groups if "电商" in g["category"] or "WB" in g["category"]]

        # 尝试从已知群组抓取
        for group in wb_relevant_groups[:5]:
            try:
                group_posts = self._fetch_group_wall(group["url"], category, max_posts=10)
                all_posts.extend(group_posts)
                time.sleep(random.uniform(3, 5))
            except Exception as e:
                logger.warning(f"[VK/WB] 群组 '{group['name']}' 抓取失败: {e}")

        # 补充 Google 搜索
        for kw in wb_keywords[:3]:
            try:
                posts = self._get_posts_via_google(kw, limit=10)
                # 过滤包含品类关键词的帖子
                cat_lower = category.lower()
                filtered = [p for p in posts if cat_lower in p["text"].lower() or cat_lower in p["group_name"].lower()]
                all_posts.extend(filtered if filtered else posts[:5])
                time.sleep(random.uniform(3, 5))
            except Exception as e:
                logger.warning(f"[VK/WB] 关键词 '{kw}' 搜索失败: {e}")

        # 去重
        seen = set()
        unique = []
        for p in all_posts:
            if p["source_url"] not in seen:
                seen.add(p["source_url"])
                unique.append(p)

        # 标记数据来源
        for p in unique:
            p["monitor_type"] = "wb_seller_group"
            p["category"] = category

        logger.info(f"[VK/WB] WB 卖家群共获取 {len(unique)} 条相关帖子")
        self.results = unique[:limit]
        return self.results

    def _fetch_group_wall(self, group_url, keyword=None, max_posts=10):
        """从 VK 群组 wall 获取帖子"""
        posts = []
        try:
            response = self._make_request(group_url)
            if not response:
                return posts

            soup = BeautifulSoup(response.text, "lxml")

            # 尝试多种选择器
            post_blocks = (
                soup.select("div.post")
                or soup.select("div._post_content")
                or soup.select("div.wall_item")
            )

            for block in post_blocks[:max_posts]:
                try:
                    text_elem = block.select_one("div.wall_text")
                    text = text_elem.get_text(strip=True) if text_elem else ""

                    # 关键词过滤
                    if keyword and keyword.lower() not in text.lower() and keyword.lower() not in group_url.lower():
                        continue

                    author_elem = block.select_one("a.author") or block.select_one("a.post_author")
                    author = author_elem.get_text(strip=True) if author_elem else ""

                    date_elem = block.select_one("span.rel_date")
                    publish_date = date_elem.get_text(strip=True) if date_elem else ""

                    # 提取互动数据
                    likes = self._extract_count_from_page(block, "like")
                    comments = self._extract_count_from_page(block, "reply")
                    reposts = self._extract_count_from_page(block, "share")

                    post_id_elem = block.get("data-post-id", "")
                    wall_link_elem = block.select_one("a.wall_post_more")
                    wall_link = wall_link_elem.get("href", "") if wall_link_elem else ""
                    source_url = f"https://vk.com{wall_link}" if wall_link else group_url

                    posts.append({
                        "post_id": post_id_elem or source_url,
                        "author": author,
                        "group_name": group_url.split("vk.com/")[-1] if "vk.com" in group_url else "",
                        "text": text[:500],
                        "likes": likes,
                        "comments": comments,
                        "reposts": reposts,
                        "publish_date": publish_date,
                        "source_url": source_url,
                        "keywords": [keyword] if keyword else [],
                        "source": "VK Group Wall",
                        "search_time": datetime.now().isoformat(),
                    })
                except Exception:
                    continue

            logger.debug(f"[VK] 群组 {group_url[:50]} 获取 {len(posts)} 条帖子")
        except Exception as e:
            logger.debug(f"[VK] 群组 wall 抓取失败: {e}")

        return posts

    # --------------------------------------------------------
    # 辅助方法
    # --------------------------------------------------------
    def _extract_count(self, block, class_prefix, data_type):
        """从帖子区块提取互动计数"""
        try:
            like_elem = block.select_one(f"div.{class_prefix}_count") or block.select_one(f"span.{class_prefix}_count")
            if like_elem:
                text = like_elem.get_text(strip=True)
                return self._parse_count(text)
        except Exception:
            pass
        return 0

    def _extract_count_from_page(self, soup, class_prefix):
        """从页面元素提取计数"""
        try:
            selectors = [
                f"div.{class_prefix}_count",
                f"span.{class_prefix}_count",
                f"div.{class_prefix}_button span",
            ]
            for sel in selectors:
                elem = soup.select_one(sel)
                if elem:
                    text = elem.get_text(strip=True)
                    count = self._parse_count(text)
                    if count > 0:
                        return count
        except Exception:
            pass
        return 0

    @staticmethod
    def _parse_count(text):
        """解析 VK 计数文本（支持 K/M 格式）"""
        if not text:
            return 0
        text = text.strip().replace("\xa0", "").replace(" ", "")
        try:
            if "K" in text.upper():
                return int(float(text.upper().replace("K", "")) * 1000)
            elif "M" in text.upper():
                return int(float(text.upper().replace("M", "")) * 1000000)
            return int(re.sub(r'[^\d]', '', text))
        except (ValueError, TypeError):
            return 0

    @staticmethod
    def _extract_date_from_snippet(snippet_elem):
        """从 Google 搜索片段中提取日期"""
        if not snippet_elem:
            return ""
        text = snippet_elem.get_text(strip=True)
        # 常见日期格式：2024年1月15日、15.01.2024、Jan 15, 2024 等
        date_patterns = [
            r'(\d{1,2}\.\d{1,2}\.\d{4})',
            r'(\d{1,2}\s+(?:янв|фев|мар|апр|мая|июн|июл|авг|сен|окт|ноя|дек)\s+\d{4})',
            r'(\d{4}-\d{2}-\d{2})',
        ]
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return ""

    def _extract_topics(self, posts, product_name):
        """从帖子中提取讨论主题"""
        topic_keywords = {
            "отзывы": "用户评价",
            "обзор": "产品测评",
            "цена": "价格讨论",
            "купить": "购买意向",
            "проблема": "问题反馈",
            "не работает": "故障/质量问题",
            "рекомендую": "推荐",
            "лучший": "最佳推荐",
            "хуже": "负面评价",
            "аналог": "替代品讨论",
            "медтехника": "医疗设备讨论",
            "тендер": "招标采购",
            "завод": "生产/制造商",
            "импорт": "进口相关",
        }

        topics = {}
        for post in posts:
            text_lower = post.get("text", "").lower()
            for kw, topic_name in topic_keywords.items():
                if kw in text_lower:
                    topics[topic_name] = topics.get(topic_name, 0) + 1

        # 按频率排序
        sorted_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)
        return [{"topic": t, "count": c} for t, c in sorted_topics[:10]]

    # --------------------------------------------------------
    # 综合搜索方法
    # --------------------------------------------------------
    def comprehensive_search(self, keyword, limit=50):
        """
        综合搜索：同时使用多种数据源

        Args:
            keyword: str, 搜索关键词
            limit: int, 最大结果数

        Returns:
            list: 综合搜索结果
        """
        logger.info(f"[VK/Comprehensive] 综合搜索: {keyword}")

        all_results = []
        seen_urls = set()

        # 1. Google site:vk.com 搜索
        try:
            google_results = self.search_vk_public(keyword, max_results=limit)
            for r in google_results:
                if r["source_url"] not in seen_urls:
                    seen_urls.add(r["source_url"])
                    all_results.append(r)
        except Exception as e:
            logger.warning(f"[VK/Comprehensive] Google 搜索失败: {e}")

        time.sleep(random.uniform(2, 4))

        # 2. VK 帖子搜索
        try:
            wall_results = self.get_vk_wall_posts(keyword, limit=limit)
            for r in wall_results:
                if r["source_url"] not in seen_urls:
                    seen_urls.add(r["source_url"])
                    all_results.append(r)
        except Exception as e:
            logger.warning(f"[VK/Comprehensive] VK 帖子搜索失败: {e}")

        time.sleep(random.uniform(2, 4))

        # 3. 从已知行业群组搜索
        try:
            groups = VK_INDUSTRY_GROUPS.get(self.country, [])
            for group in groups[:5]:
                group_posts = self._fetch_group_wall(group["url"], keyword, max_posts=5)
                for p in group_posts:
                    if p["source_url"] not in seen_urls:
                        seen_urls.add(p["source_url"])
                        all_results.append(p)
                time.sleep(random.uniform(3, 5))
        except Exception as e:
            logger.warning(f"[VK/Comprehensive] 行业群组搜索失败: {e}")

        # 按互动量排序
        all_results.sort(key=lambda x: x.get("likes", 0) + x.get("comments", 0), reverse=True)

        logger.info(f"[VK/Comprehensive] 综合搜索共获取 {len(all_results)} 条结果")
        self.results = all_results[:limit]
        return self.results

    # --------------------------------------------------------
    # 结果保存
    # --------------------------------------------------------
    def save_results(self, output_dir=None, filename=None):
        """
        保存搜索结果到 JSON 文件

        Args:
            output_dir: str, 输出目录（默认 outputs/vk/）
            filename: str, 文件名（默认 vk_results_YYYYMMDD_HHMMSS.json）

        Returns:
            str: 保存的文件路径
        """
        import os

        if not output_dir:
            SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
            PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
            output_dir = os.path.join(PROJECT_ROOT, "outputs", "vk")

        os.makedirs(output_dir, exist_ok=True)

        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"vk_results_{timestamp}.json"

        filepath = os.path.join(output_dir, filename)

        output = {
            "search_time": datetime.now().isoformat(),
            "country": self.country,
            "total_results": len(self.results),
            "results": self.results,
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        logger.info(f"[VK] 结果已保存到: {filepath}")
        return filepath

    def save_analysis(self, analysis_data, output_dir=None, filename=None):
        """
        保存分析结果到 JSON 文件

        Args:
            analysis_data: dict, 分析数据
            output_dir: str, 输出目录
            filename: str, 文件名

        Returns:
            str: 保存的文件路径
        """
        import os

        if not output_dir:
            SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
            PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
            output_dir = os.path.join(PROJECT_ROOT, "outputs", "vk")

        os.makedirs(output_dir, exist_ok=True)

        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"vk_analysis_{timestamp}.json"

        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(analysis_data, f, ensure_ascii=False, indent=2)

        logger.info(f"[VK] 分析结果已保存到: {filepath}")
        return filepath


# ============================================================
# CLI 入口
# ============================================================
if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="VKontakte 行业监控工具")
    parser.add_argument("--keyword", "-k", type=str, help="搜索关键词")
    parser.add_argument("--product", "-p", type=str, help="分析产品讨论")
    parser.add_argument("--competitor", "-c", type=str, help="分析竞品 VK 活跃度")
    parser.add_argument("--wb-groups", action="store_true", help="监控 WB 卖家群")
    parser.add_argument("--category", type=str, default="医疗设备", help="品类（配合 --wb-groups）")
    parser.add_argument("--country", type=str, default="俄罗斯", help="目标国家")
    parser.add_argument("--limit", "-l", type=int, default=30, help="最大结果数")
    parser.add_argument("--output", "-o", type=str, help="输出文件路径")
    args = parser.parse_args()

    monitor = VKMonitor(country=args.country)

    if args.keyword:
        results = monitor.comprehensive_search(args.keyword, limit=args.limit)
        monitor.save_results(output_dir=args.output)
        print(json.dumps(results[:5], ensure_ascii=False, indent=2))
    elif args.product:
        analysis = monitor.analyze_vk_mentions(args.product, limit=args.limit)
        monitor.save_analysis(analysis, output_dir=args.output)
        print(f"产品 '{args.product}' 分析: {analysis['total_mentions']} 条提及")
        print(json.dumps(analysis["topics"], ensure_ascii=False, indent=2))
    elif args.competitor:
        analysis = monitor.get_competitor_vk_presence(args.competitor, limit=args.limit)
        monitor.save_analysis(analysis, output_dir=args.output)
        print(f"竞品 '{args.competitor}' VK 活跃度分析完成")
    elif args.wb_groups:
        results = monitor.monitor_wb_seller_groups(category=args.category, limit=args.limit)
        monitor.save_results(output_dir=args.output)
        print(f"WB 卖家群监控: {len(results)} 条相关帖子")
    else:
        parser.print_help()
