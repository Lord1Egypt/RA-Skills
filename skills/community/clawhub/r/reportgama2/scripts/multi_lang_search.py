# -*- coding: utf-8 -*-
"""
Report-gama — 多语种搜索引擎模块
支持：俄语/英语/中文/哈萨克语/乌兹别克语等多语种搜索
"""

import random
import time
import logging
import re
import json
from datetime import datetime, timedelta
from urllib.parse import quote_plus, urlencode, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"[ERROR] 缺少必需依赖: {e}")
    print("请运行: pip install requests beautifulsoup4 lxml")
    raise SystemExit(1)

from config import (
    SEARCH_ENGINES, USER_AGENTS, REQUEST_TIMEOUT, REQUEST_RETRIES,
    PROXY, HTTPS_PROXY, LOG_LEVEL, LOG_FORMAT
)

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


class MultiLangSearch:
    """多语种搜索引擎"""

    def __init__(self, country="俄罗斯", lang="ru"):
        self.country = country
        self.lang = lang
        self.country_code = self._get_country_code(country)
        self.session = self._create_session()
        self.results = []
        self.all_sources = []

    def _get_country_code(self, country):
        codes = {
            "俄罗斯": "RU", "哈萨克斯坦": "KZ", "乌兹别克斯坦": "UZ",
            "白俄罗斯": "BY", "中国": "CN", "美国": "US",
            "德国": "DE", "法国": "FR", "英国": "GB",
        }
        return codes.get(country, "US")

    def _create_session(self):
        session = requests.Session()
        session.headers.update({
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": f"{self.lang},en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        })
        if PROXY:
            session.proxies = {"http": PROXY, "https": HTTPS_PROXY or PROXY}
        return session

    def _get_headers_for_engine(self, engine_name):
        headers = self.session.headers.copy()
        if engine_name == "yandex":
            headers["Accept-Language"] = "ru,en;q=0.9"
        elif engine_name == "baidu":
            headers["Accept-Language"] = "zh-CN,zh;q=0.9"
        elif engine_name == "google":
            headers["Accept-Language"] = f"{self.lang}-{self.country_code};q=0.9,en;q=0.8"
        return headers

    def _make_request(self, url, engine_name="generic", max_retries=REQUEST_RETRIES):
        """带重试的HTTP请求"""
        for attempt in range(max_retries + 1):
            try:
                headers = self._get_headers_for_engine(engine_name)
                response = self.session.get(
                    url, headers=headers,
                    timeout=REQUEST_TIMEOUT
                )
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:
                    wait_time = (attempt + 1) * 5
                    logger.warning(f"[{engine_name}] 请求过于频繁，等待 {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.warning(f"[{engine_name}] HTTP {response.status_code}: {url}")
            except requests.RequestException as e:
                logger.warning(f"[{engine_name}] 请求失败 (尝试 {attempt+1}/{max_retries+1}): {e}")
                time.sleep(3)
        return None

    def _parse_google_results(self, html):
        """解析Google搜索结果"""
        soup = BeautifulSoup(html, "lxml")
        results = []
        for item in soup.select("div.g")[:15]:
            try:
                title_elem = item.select_one("h3")
                link_elem = item.select_one("a")
                snippet_elem = item.select_one("div[data-sncf]")
                if title_elem and link_elem:
                    link = link_elem.get("href", "")
                    if link.startswith("/url?q="):
                        link = link.split("/url?q=")[1].split("&")[0]
                    if not link.startswith("http"):
                        continue
                    results.append({
                        "title": title_elem.get_text(strip=True),
                        "url": link,
                        "snippet": snippet_elem.get_text(strip=True) if snippet_elem else "",
                        "source": "Google",
                    })
            except Exception:
                continue
        return results

    def _parse_yandex_results(self, html):
        """解析Yandex搜索结果"""
        soup = BeautifulSoup(html, "lxml")
        results = []
        for item in soup.select("li.serp-item")[:15]:
            try:
                title_elem = item.select_one("h2 a") or item.select_one(".OrganicTitle-Chemist a")
                link_elem = item.select_one("a.Link")
                snippet_elem = item.select_one(".OrganicTextContentSpan")
                if title_elem:
                    link = link_elem.get("href", "") if link_elem else ""
                    results.append({
                        "title": title_elem.get_text(strip=True),
                        "url": link,
                        "snippet": snippet_elem.get_text(strip=True) if snippet_elem else "",
                        "source": "Yandex",
                    })
            except Exception:
                continue
        return results

    def _parse_baidu_results(self, html):
        """解析百度搜索结果"""
        soup = BeautifulSoup(html, "lxml")
        results = []
        for item in soup.select("div.result")[:15]:
            try:
                title_elem = item.select_one("h3 a")
                link_elem = item.select_one("h3 a")
                snippet_elem = item.select_one("div.c-abstract") or item.select_one("span")
                if title_elem:
                    link = link_elem.get("href", "") if link_elem else ""
                    results.append({
                        "title": title_elem.get_text(strip=True),
                        "url": link,
                        "snippet": snippet_elem.get_text(strip=True)[:200] if snippet_elem else "",
                        "source": "百度",
                    })
            except Exception:
                continue
        return results

    def _parse_generic_results(self, html, engine_name="generic"):
        """通用解析器（fallback）"""
        soup = BeautifulSoup(html, "lxml")
        results = []
        for item in soup.select("h2, h3")[:15]:
            try:
                parent = item.find_parent()
                if parent:
                    link = parent.get("href", "") if parent.name == "a" else ""
                    if not link:
                        link_elem = item.find_next("a")
                        if link_elem:
                            link = link_elem.get("href", "")
                    if link and link.startswith("http"):
                        results.append({
                            "title": item.get_text(strip=True),
                            "url": link,
                            "snippet": "",
                            "source": engine_name,
                        })
            except Exception:
                continue
        return results

    def _build_search_url(self, engine_name, keyword, news_mode=False):
        """构建搜索引擎URL"""
        keyword_encoded = quote_plus(keyword)

        if engine_name == "yandex":
            lr_code = SEARCH_ENGINES["yandex"]["lr_codes"].get(self.country_code, 213)
            base = SEARCH_ENGINES["yandex"]["news_url"] if news_mode else SEARCH_ENGINES["yandex"]["base_url"]
            return base.format(keyword=keyword_encoded, lr=lr_code)

        elif engine_name == "google":
            hl_map = {"ru": "ru", "en": "en-US", "zh": "zh-CN", "kk": "kk", "uz": "uz"}
            gl_map = {"ru": "RU", "en": "US", "zh": "CN", "kk": "KZ", "uz": "UZ"}
            base = "https://news.google.com/search?q={keyword}&hl={hl}&gl={gl}" if news_mode else SEARCH_ENGINES["google"]["base_url"]
            return base.format(keyword=keyword_encoded, hl=hl_map.get(self.lang, "en"), gl=gl_map.get(self.country_code, "US"))

        elif engine_name == "baidu":
            base = SEARCH_ENGINES["baidu"]["news_url"] if news_mode else SEARCH_ENGINES["baidu"]["base_url"]
            return base.format(keyword=keyword_encoded)

        elif engine_name == "ddg":
            base = SEARCH_ENGINES["ddg"]["news_url"] if news_mode else SEARCH_ENGINES["ddg"]["base_url"]
            return base.format(keyword=keyword_encoded)

        elif engine_name == "bing":
            base = SEARCH_ENGINES["bing"]["news_url"] if news_mode else SEARCH_ENGINES["bing"]["base_url"]
            return base.format(keyword=keyword_encoded)

        return f"https://duckduckgo.com/html/?q={keyword_encoded}"

    def search(self, keywords, engines=None, news_mode=False, max_results=20):
        """
        多引擎并发搜索

        Args:
            keywords: str or list, 搜索关键词（支持多语种）
            engines: list, 搜索引擎列表，默认["yandex", "google", "ddg"]
            news_mode: bool, 是否仅搜索新闻
            max_results: int, 每个引擎最多返回结果数

        Returns:
            list: 搜索结果列表
        """
        if isinstance(keywords, str):
            keywords = [keywords]

        if engines is None:
            engines = ["yandex", "google", "ddg"]

        all_results = []
        seen_urls = set()

        for keyword in keywords:
            for engine in engines:
                url = self._build_search_url(engine, keyword, news_mode)
                logger.info(f"[{engine}] 搜索: {keyword[:50]}...")

                response = self._make_request(url, engine)
                if not response:
                    logger.warning(f"[{engine}] 搜索失败: {keyword}")
                    continue

                try:
                    if engine == "google":
                        results = self._parse_google_results(response.text)
                    elif engine == "yandex":
                        results = self._parse_yandex_results(response.text)
                    elif engine == "baidu":
                        results = self._parse_baidu_results(response.text)
                    else:
                        results = self._parse_generic_results(response.text, engine)

                    for r in results:
                        if r["url"] not in seen_urls:
                            r["keyword"] = keyword
                            r["engine"] = engine
                            r["search_time"] = datetime.now().isoformat()
                            all_results.append(r)
                            seen_urls.add(r["url"])

                    logger.info(f"[{engine}] 找到 {len(results)} 条结果")

                except Exception as e:
                    logger.error(f"[{engine}] 解析失败: {e}")

                # 礼貌性延迟，避免被限速
                time.sleep(random.uniform(1.5, 3.5))

        # 按关键词相关性排序（标题含关键词的优先）
        def score(result):
            s = 0
            for kw in keywords:
                if kw.lower() in result["title"].lower():
                    s += 3
                if kw.lower() in result["snippet"].lower():
                    s += 1
            return s

        all_results.sort(key=score, reverse=True)
        self.results = all_results[:max_results]
        self.all_sources = list(seen_urls)

        logger.info(f"总计采集 {len(self.results)} 条独立搜索结果（去重后）")
        return self.results

    def search_concurrent(self, keywords, engines=None, news_mode=False, max_results=20, max_workers=3):
        """
        并发多引擎搜索（加速版）

        Args:
            keywords: str or list, 搜索关键词
            engines: list, 引擎列表，默认 ["yandex", "google", "ddg"]
            news_mode: bool, 是否仅搜索新闻
            max_results: int, 最大结果数
            max_workers: int, 并发线程数

        Returns:
            list: 搜索结果列表
        """
        if isinstance(keywords, str):
            keywords = [keywords]
        if engines is None:
            engines = ["yandex", "google", "ddg"]

        all_results = []
        seen_urls = set()
        lock = threading.Lock()

        def _search_one_engine(keyword, engine):
            url = self._build_search_url(engine, keyword, news_mode)
            logger.info(f"[{engine}] 搜索: {keyword[:50]}...")

            response = self._make_request(url, engine)
            if not response:
                logger.warning(f"[{engine}] 搜索失败: {keyword}")
                return []

            try:
                if engine == "google":
                    results = self._parse_google_results(response.text)
                elif engine == "yandex":
                    results = self._parse_yandex_results(response.text)
                elif engine == "baidu":
                    results = self._parse_baidu_results(response.text)
                else:
                    results = self._parse_generic_results(response.text, engine)

                for r in results:
                    r["keyword"] = keyword
                    r["engine"] = engine
                    r["search_time"] = datetime.now().isoformat()

                logger.info(f"[{engine}] 找到 {len(results)} 条结果")
                return results
            except Exception as e:
                logger.error(f"[{engine}] 解析失败: {e}")
                return []

        # 构建所有 (keyword, engine) 组合
        tasks = [(kw, eng) for kw in keywords for eng in engines]

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(_search_one_engine, kw, eng): (kw, eng) for kw, eng in tasks}
            for future in as_completed(futures):
                try:
                    results = future.result()
                    with lock:
                        for r in results:
                            if r["url"] not in seen_urls:
                                all_results.append(r)
                                seen_urls.add(r["url"])
                except Exception as e:
                    kw, eng = futures[future]
                    logger.warning(f"[{eng}] {kw} 异常: {e}")

        # 排序
        def score(result):
            s = 0
            for kw in keywords:
                if kw.lower() in result["title"].lower():
                    s += 3
                if kw.lower() in result["snippet"].lower():
                    s += 1
            return s

        all_results.sort(key=score, reverse=True)
        self.results = all_results[:max_results]
        self.all_sources = list(seen_urls)
        logger.info(f"[并发搜索] 总计采集 {len(self.results)} 条独立结果（去重后）")
        return self.results

    def search_with_time_filter(self, keywords, time_range="m"):
        """
        按时间范围搜索（仅Google/Bing支持精确时间过滤）

        time_range: "h"=1小时, "d"=1天, "w"=1周, "m"=1月, "y"=1年
        """
        if isinstance(keywords, str):
            keywords = [keywords]

        tbs_map = {
            "h": "qdr:h", "d": "qdr:d", "w": "qdr:w", "m": "qdr:m", "y": "qdr:y"
        }
        tbs = tbs_map.get(time_range, "qdr:m")

        all_results = []
        for keyword in keywords:
            url = f"https://www.google.com/search?q={quote_plus(keyword)}&tbs={tbs}&hl={self.lang}"
            logger.info(f"[Google/时控] 搜索: {keyword[:50]}... [{time_range}]")

            response = self._make_request(url, "google")
            if response:
                results = self._parse_google_results(response.text)
                for r in results:
                    r["keyword"] = keyword
                    r["time_filter"] = time_range
                all_results.extend(results)

            time.sleep(random.uniform(2, 4))

        return all_results[:50]

    def get_related_keywords(self, keyword, lang=None):
        """获取相关关键词建议"""
        lang = lang or self.lang
        url = self._build_search_url("google", keyword)

        response = self._make_request(url, "google")
        if not response:
            return []

        soup = BeautifulSoup(response.text, "lxml")
        related = []

        # Google 相关搜索（多种可能的选择器）
        for selector in ["div.oSokLb", "div.KV lunar-fade", ".wMPar"]:
            for elem in soup.select(selector)[:10]:
                text = elem.get_text(strip=True)
                if text:
                    related.append(text)

        # Yandex 相关关键词选择器
        for selector in [".SuggestItem-Link", ".mini-suggest__item"]:
            for elem in soup.select(selector)[:10]:
                text = elem.get_text(strip=True)
                if text and len(text) > 2:
                    related.append(text)

        return list(set(related))[:20]

    def export_results(self, output_path=None):
        """导出搜索结果为JSON"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"search_results_{timestamp}.json"

        data = {
            "search_time": datetime.now().isoformat(),
            "country": self.country,
            "lang": self.lang,
            "total_results": len(self.results),
            "results": self.results,
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"结果已保存: {output_path}")
        return output_path

    def fetch_page_content(self, url, max_chars=3000, timeout=None):
        """
        抓取搜索结果页面的正文内容（用于深度分析）

        Args:
            url: 目标URL
            max_chars: 最大返回字符数
            timeout: 超时（秒），默认使用 REQUEST_TIMEOUT

        Returns:
            dict: {title, text, domain, lang_detected} 或 None（失败时）
        """
        timeout = timeout or REQUEST_TIMEOUT
        domain = urlparse(url).netloc

        try:
            response = self._make_request(url, engine_name=f"content:{domain}")
            if not response:
                return None

            content_type = response.headers.get("Content-Type", "")
            if "text/html" not in content_type and "application/xhtml" not in content_type:
                return {"title": "", "text": response.text[:max_chars], "domain": domain, "lang_detected": "unknown"}

            soup = BeautifulSoup(response.text, "lxml")

            # 移除干扰元素
            for tag in soup.find_all(["script", "style", "nav", "footer", "header", "aside", "noscript", "iframe"]):
                tag.decompose()

            # 提取标题
            title = (
                soup.select_one("h1")
                or soup.select_one("article h1")
                or soup.select_one("title")
            )
            title = title.get_text(strip=True)[:200] if title else ""

            # 提取正文（多策略）
            text = ""
            for selector in [
                "article", ".article-body", ".article__body", ".content",
                "main", "[role=main]", ".post-content", ".entry-content",
                ".story-body", "#articleBody", ".news-text"
            ]:
                elem = soup.select_one(selector)
                if elem:
                    text = elem.get_text(separator=" ", strip=True)
                    break

            if not text:
                # fallback: 提取所有段落
                paragraphs = soup.select("p")
                text = " ".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

            text = text[:max_chars]

            # 语言检测（简单启发式）
            cyrillic = len(re.findall(r"[\u0400-\u04FF]", text))
            chinese = len(re.findall(r"[\u4e00-\u9fff]", text))
            if cyrillic > 50:
                lang_detected = "ru"
            elif chinese > 50:
                lang_detected = "zh"
            else:
                lang_detected = "en"

            logger.info(f"[内容抓取] {domain}: {len(text)} 字符, lang={lang_detected}")
            return {
                "title": title,
                "text": text,
                "domain": domain,
                "url": url,
                "lang_detected": lang_detected,
                "fetch_time": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.warning(f"[内容抓取] 失败 {url}: {e}")
            return None

    def fetch_contents_parallel(self, urls, max_workers=5, max_chars=3000):
        """
        并发抓取多个URL的页面内容

        Args:
            urls: URL列表
            max_workers: 并发线程数
            max_chars: 每个页面最大字符数

        Returns:
            list: 成功抓取的内容字典列表
        """
        results = []
        lock = threading.Lock()

        def _fetch_one(url):
            content = self.fetch_page_content(url, max_chars=max_chars)
            if content:
                with lock:
                    results.append(content)
            return url

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(_fetch_one, url): url for url in urls[:20]}
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    url = futures[future]
                    logger.warning(f"[并发抓取] {url} 异常: {e}")

        logger.info(f"[并发抓取] 成功 {len(results)}/{len(urls[:20])} 个页面")
        return results


def translate_keywords(keywords, from_lang="zh", to_lang="ru"):
    """
    关键词翻译辅助函数
    使用Google Translate（非官方，礼貌性使用）
    """
    try:
        from googletrans import Translator
        translator = Translator()
        if isinstance(keywords, str):
            keywords = [keywords]
        results = {}
        for kw in keywords:
            try:
                translated = translator.translate(kw, src=from_lang, dest=to_lang)
                results[kw] = translated.text
                time.sleep(0.5)
            except Exception:
                results[kw] = kw
        return results
    except ImportError:
        logger.warning("googletrans 未安装，将返回原始关键词")
        return {kw: kw for kw in (keywords if isinstance(keywords, list) else [keywords])}


# ============================================================
# 行业预设关键词翻译映射
# ============================================================
KEYWORD_TRANSLATIONS = {
    # 血糖检测
    "血糖检测设备": {
        "ru": ["глюкометр", "измеритель глюкозы", "тест-полоски", "сахар в крови прибор"],
        "en": ["blood glucose meter", "glucometer", "glucose strips"],
    },
    # 医疗器械
    "医疗器械": {
        "ru": ["медицинское оборудование", "медицинская техника", "медицинские изделия"],
        "en": ["medical equipment", "medical devices", "medical tech"],
    },
    # 市场/行业
    "市场规模": {
        "ru": ["объём рынка", "размер рынка", "ёмкость рынка"],
        "en": ["market size", "market volume", "market capacity"],
    },
    "市场趋势": {
        "ru": ["тренды рынка", "динамика рынка", "рыночные тенденции"],
        "en": ["market trends", "industry trends"],
    },
    "竞争格局": {
        "ru": ["конкуренция", "конкурентный анализ", "игроки рынка"],
        "en": ["competitive landscape", "competitor analysis"],
    },
    "进出口": {
        "ru": ["импорт", "экспорт", "таможенная статистика"],
        "en": ["import", "export", "customs data"],
    },
    "电商": {
        "ru": ["интернет-магазин", "Wildberries", "Ozon", "электронная коммерция"],
        "en": ["e-commerce", "online shopping", "Amazon", "e-commerce platform"],
    },
    "价格": {
        "ru": ["цена", "стоимость", "прайс", "сколько стоит"],
        "en": ["price", "cost", "how much"],
    },
    "注册证": {
        "ru": ["регистрация медицинских изделий", "Росздравнадзор регистрация"],
        "en": ["medical device registration", "FDA clearance", "CE marking"],
    },
    "新闻": {
        "ru": ["новости", "события", "обновления"],
        "en": ["news", "updates", "recent developments"],
    },
    "法规": {
        "ru": ["регулирование", "законодательство", "стандарты"],
        "en": ["regulation", "legislation", "standards"],
    },
}


def expand_keywords(base_keywords, dimensions=None):
    """
    扩展关键词列表（基础词 × 维度词）

    Args:
        base_keywords: 品类基础关键词 dict{lang: [keywords]}，例如 {"ru": ["глюкометр"], "en": ["glucometer"], "zh": ["血糖仪"]}
        dimensions: 需要叠加的维度列表，如["市场规模","竞争格局","新闻","法规","价格","电商","进出口","注册证"]

    Returns:
        dict: {lang: [expanded keywords]}
    """
    if dimensions is None:
        dimensions = ["市场规模", "竞争格局", "新闻", "法规", "价格", "电商"]

    expanded = {"ru": [], "en": [], "zh": []}

    # 第一层：直接加入基础品类词
    for lang in ["ru", "en", "zh"]:
        expanded[lang].extend(base_keywords.get(lang, base_keywords.get("en", [])))

    # 第二层：维度词 × 基础品类词 = 组合关键词
    for dim in dimensions:
        dim_translations = KEYWORD_TRANSLATIONS.get(dim, {})
        for lang in ["ru", "en"]:
            # 基础品类词（该语言有则用，无则fallback英语）
            base_list = base_keywords.get(lang, base_keywords.get("en", []))
            dim_words = dim_translations.get(lang, [])
            for b in base_list:
                for d in dim_words:
                    # 组合词：品类词在前，维度词在后
                    combined = f"{b} {d}".strip()
                    if combined not in expanded[lang]:
                        expanded[lang].append(combined)

    # 去重并清理
    for lang in expanded:
        expanded[lang] = sorted(set([kw.strip() for kw in expanded[lang] if kw.strip()]))

    return expanded


def run_search(country, category_keywords, modules=None, lang=None):
    """
    执行完整的多语种搜索流程

    Args:
        country: 国家名
        category_keywords: 品类关键词 dict{ru:[], en:[], zh:[]}
        modules: 需要搜索的模块列表
        lang: 主语言

    Returns:
        dict: 各类别搜索结果
    """
    modules = modules or ["news", "market", "competitor", "ecommerce", "ads", "customs"]
    lang = lang or "ru"

    searcher = MultiLangSearch(country=country, lang=lang)

    results = {}

    dimension_map = {
        "news": ["新闻"],
        "market": ["市场规模", "市场趋势"],
        "competitor": ["竞争格局"],
        "ecommerce": ["电商", "价格"],
        "ads": ["广告", "营销"],
        "customs": ["进出口"],
    }

    for module in modules:
        dims = dimension_map.get(module, ["新闻"])
        keywords_to_search = []

        # 维度词扩展：品类词 × 各维度词
        expanded = expand_keywords(category_keywords, dimensions=dims)
        keywords_to_search.extend(expanded.get(lang, []))
        keywords_to_search.extend(expanded.get("en", []))

        keywords_to_search = list(set(keywords_to_search))[:30]
        logger.info(f"[{module.upper()}] 并发搜索 {len(keywords_to_search)} 个关键词...")

        module_results = searcher.search_concurrent(
            keywords_to_search,
            news_mode=(module == "news"),
            max_workers=3
        )
        results[module] = module_results

        # 模块间延迟
        time.sleep(random.uniform(2, 4))

    return results


if __name__ == "__main__":
    import sys

    # 测试示例
    keywords = {
        "ru": ["глюкометр", "рынок медицинского оборудования"],
        "en": ["blood glucose meter Russia market"],
        "zh": ["血糖仪", "俄罗斯医疗器械市场"],
    }

    searcher = MultiLangSearch(country="俄罗斯", lang="ru")
    results = searcher.search(keywords["ru"], engines=["yandex", "google"], news_mode=False)

    print(f"\n搜索到 {len(results)} 条结果:")
    for r in results[:5]:
        print(f"  [{r['source']}] {r['title']}")
        print(f"    {r.get('snippet', '')[:100]}...")
