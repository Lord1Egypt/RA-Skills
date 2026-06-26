# -*- coding: utf-8 -*-
"""
Report-gama — 俄罗斯政府采购招标监控模块
抓取 zakupki.gov.ru、联邦主体平台、民间聚合平台的招标数据
"""

import os
import sys
import random
import time
import logging
import re
import json
from datetime import datetime, timedelta
from urllib.parse import quote_plus, urljoin

# ── 路径常量（与 report-gama 其他脚本保持一致）─────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
PROJECT_ROOT = os.path.dirname(SKILL_DIR)

sys.path.insert(0, SCRIPT_DIR)
from config import (
    REQUEST_TIMEOUT, REQUEST_RETRIES, USER_AGENTS,
    PROXY, HTTPS_PROXY, LOG_LEVEL, LOG_FORMAT, CATEGORY_KEYWORDS,
)

# ── 输出目录 ─────────────────────────────────────────────────────────────────
TENDER_OUTPUT_DIR = os.path.join(SKILL_DIR, "output", "tenders")
os.makedirs(TENDER_OUTPUT_DIR, exist_ok=True)

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# ── 全局请求超时常量 ───────────────────────────────────────────────────────────
REQUEST_TIMEOUT = REQUEST_TIMEOUT   # 来自 config


# ═══════════════════════════════════════════════════════════════════════════════
# 招标平台配置
# ═══════════════════════════════════════════════════════════════════════════════

TENDER_PLATFORMS = {
    "zakupki_gov": {
        "name": "ЕИС Закупки (zakupki.gov.ru)",
        "name_cn": "俄罗斯联邦政府采购网（ЕИС）",
        "base_url": "https://zakupki.gov.ru",
        "search_url": "https://zakupki.gov.ru/epz/order/extendedsearch/riscpec.html",
        "lang": "ru",
        "country": "RU",
    },
    "mos_ru": {
        "name": "Мос.ру (mos.ru)",
        "name_cn": "莫斯科政府采购平台",
        "base_url": "https://mos.ru",
        "search_url": "https://mos.ru/afisha/tenders/",
        "lang": "ru",
        "country": "RU",
    },
    "piter_ru": {
        "name": "СПб Закупки (piter.ru)",
        "name_cn": "圣彼得堡政府采购平台",
        "base_url": "https://piter.ru",
        "search_url": "https://piter.ru/procedure/",
        "lang": "ru",
        "country": "RU",
    },
    "tenderguru": {
        "name": "TenderGuru (tenderguru.ru)",
        "name_cn": "TenderGuru 民间聚合平台",
        "base_url": "https://tenderguru.ru",
        "search_url": "https://tenderguru.ru/tenders",
        "lang": "ru",
        "country": "RU",
    },
    "zakupki_online": {
        "name": "Zakupki-Online (zakupki-online.com)",
        "name_cn": "Zakupki-Online 民间聚合平台",
        "base_url": "https://zakupki-online.com",
        "search_url": "https://zakupki-online.com/tenders",
        "lang": "ru",
        "country": "RU",
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# 通用字段模板
# ═══════════════════════════════════════════════════════════════════════════════

def make_empty_tender():
    """返回空招标记录模板"""
    return {
        "id": "",
        "title": "",
        "customer": "",
        "winner": "",
        "price": 0.0,
        "currency": "RUB",
        "quantity": "",
        "specs": "",
        "publish_date": "",
        "deadline": "",
        "region": "",
        "source_url": "",
        "source_name": "",
        "status": "",
    }


# ═══════════════════════════════════════════════════════════════════════════════
# TenderMonitor 主类
# ═══════════════════════════════════════════════════════════════════════════════

class TenderMonitor:
    """俄罗斯政府采购招标监控系统"""

    def __init__(self, country="俄罗斯", lang="ru"):
        self.country = country
        self.lang = lang
        self.country_code = self._country_to_code(country)
        self.session = self._create_session()
        self.results = []

    # ── 工具方法 ──────────────────────────────────────────────────────────────

    def _country_to_code(self, country):
        codes = {
            "俄罗斯": "RU", "哈萨克斯坦": "KZ",
            "乌兹别克斯坦": "UZ", "白俄罗斯": "BY",
            "中国": "CN", "美国": "US",
        }
        return codes.get(country, "RU")

    def _create_session(self):
        """创建带随机 UA 和代理的会话"""
        session = requests.Session()
        session.headers.update({
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": f"{self.lang},en;q=0.5",
        })
        if PROXY:
            session.proxies = {"http": PROXY, "https": HTTPS_PROXY or PROXY}
        return session

    def _safe_request(self, url, params=None, method="GET", max_retries=None):
        """带重试的安全请求，每平台独立 try/except"""
        if max_retries is None:
            max_retries = REQUEST_RETRIES
        last_err = None
        for attempt in range(max_retries + 1):
            try:
                if method.upper() == "POST":
                    r = self.session.post(url, data=params, timeout=REQUEST_TIMEOUT)
                else:
                    r = self.session.get(url, params=params, timeout=REQUEST_TIMEOUT)
                r.raise_for_status()
                return r
            except Exception as e:
                last_err = e
                logger.warning(f"请求失败 [{url}] (attempt {attempt+1}): {e}")
                if attempt < max_retries:
                    time.sleep(random.uniform(2, 4))
        logger.error(f"请求最终失败 [{url}]: {last_err}")
        return None

    def _save_result(self, filename, data):
        """保存结果到 outputs/tenders/"""
        path = os.path.join(TENDER_OUTPUT_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"结果已保存: {path}")
        return path

    # ═══════════════════════════════════════════════════════════════════════════
    # 平台级搜索方法
    # ═══════════════════════════════════════════════════════════════════════════

    def _search_zakupki_gov(self, keywords, date_from, date_to, region=""):
        """
        搜索 zakupki.gov.ru（ЕИС 联邦政府采购网）
        API endpoint: https://zakupki.gov.ru/epz/order/extendedsearch/riscpec.html
        """
        tenders = []
        try:
            query = " ".join(keywords) if isinstance(keywords, list) else keywords
            params = {
                "searchString": query,
                "fz44": "on",
                "fz223": "on",
                "publishDateFrom": date_from,
                "publishDateTo": date_to,
                "sortBy": "PUBLISH_DATE",
                "pageNumber": 1,
            }
            if region:
                params["region"] = region
            r = self._safe_request(
                TENDER_PLATFORMS["zakupki_gov"]["search_url"], params=params
            )
            if not r:
                return tenders
            soup = BeautifulSoup(r.text, "html.parser")
            items = soup.select("div.search-registry-entry-block")
            logger.info(f"[ЕИС] 找到 {len(items)} 条记录")
            for item in items[:30]:
                t = make_empty_tender()
                try:
                    # 标题
                    title_el = item.select_one("div.registry-entry__body-hint")
                    if not title_el:
                        title_el = item.select_one("a.registry-entry__body-hint")
                    t["title"] = title_el.get_text(strip=True) if title_el else ""

                    # 编号
                    num_el = item.select_one("div.registry-entry__law-number")
                    t["id"] = num_el.get_text(strip=True) if num_el else ""

                    # 采购方
                    cust_el = item.select_one("div.customer-info__name")
                    t["customer"] = cust_el.get_text(strip=True) if cust_el else ""

                    # 价格
                    price_el = item.select_one("div.price-block__value")
                    if price_el:
                        price_text = re.sub(r"[^\d,.]", "", price_el.get_text(strip=True))
                        price_text = price_text.replace(",", ".")
                        try:
                            t["price"] = float(price_text)
                        except ValueError:
                            t["price"] = 0.0

                    # 截止日期
                    deadline_el = item.select_one("div.date-block")
                    t["deadline"] = deadline_el.get_text(strip=True) if deadline_el else ""

                    # 链接
                    link_el = item.select_one("a.registry-entry__body-hint")
                    if link_el:
                        href = link_el.get("href", "")
                        t["source_url"] = urljoin(
                            TENDER_PLATFORMS["zakupki_gov"]["base_url"], href
                        )

                    t["source_name"] = "ЕИС Закупки"
                    t["region"] = region or "РФ"
                    if t["title"] or t["id"]:
                        tenders.append(t)
                except Exception as e:
                    logger.warning(f"[ЕИС] 解析单条失败: {e}")
                    continue
        except Exception as e:
            logger.error(f"[ЕИС] 搜索异常: {e}")
        return tenders

    def _search_tenderguru(self, keywords, date_from, date_to, region=""):
        """搜索 tenderguru.ru"""
        tenders = []
        try:
            query = "+".join(keywords) if isinstance(keywords, list) else keywords.replace(" ", "+")
            url = f"{TENDER_PLATFORMS['tenderguru']['search_url']}?q={quote_plus(query)}"
            if date_from:
                url += f"&date_from={date_from}"
            if date_to:
                url += f"&date_to={date_to}"
            r = self._safe_request(url)
            if not r:
                return tenders
            soup = BeautifulSoup(r.text, "html.parser")
            cards = soup.select("div.tender-card, div.card, article.tender")
            logger.info(f"[TenderGuru] 找到 {len(cards)} 条记录")
            for card in cards[:30]:
                t = make_empty_tender()
                try:
                    title_el = card.select_one("h3, h4, .title, .tender-title")
                    t["title"] = title_el.get_text(strip=True) if title_el else ""

                    price_el = card.select_one(".price, .cost, .tender-price, .value")
                    if price_el:
                        price_text = re.sub(r"[^\d,.]", "", price_el.get_text(strip=True))
                        price_text = price_text.replace(",", ".")
                        try:
                            t["price"] = float(price_text)
                        except ValueError:
                            t["price"] = 0.0

                    customer_el = card.select_one(".customer, .customer-name, .customer-info")
                    t["customer"] = customer_el.get_text(strip=True) if customer_el else ""

                    date_el = card.select_one(".date, .deadline, time, .publish-date")
                    t["publish_date"] = date_el.get_text(strip=True) if date_el else ""

                    link_el = card.select_one("a[href]")
                    if link_el:
                        href = link_el.get("href", "")
                        t["source_url"] = urljoin(
                            TENDER_PLATFORMS["tenderguru"]["base_url"], href
                        )

                    t["source_name"] = "TenderGuru"
                    t["region"] = region or "РФ"
                    if t["title"]:
                        tenders.append(t)
                except Exception as e:
                    logger.warning(f"[TenderGuru] 解析单条失败: {e}")
                    continue
        except Exception as e:
            logger.error(f"[TenderGuru] 搜索异常: {e}")
        return tenders

    def _search_zakupki_online(self, keywords, date_from, date_to, region=""):
        """搜索 zakupki-online.com"""
        tenders = []
        try:
            query = "+".join(keywords) if isinstance(keywords, list) else keywords.replace(" ", "+")
            url = f"{TENDER_PLATFORMS['zakupki_online']['search_url']}?search={quote_plus(query)}"
            r = self._safe_request(url)
            if not r:
                return tenders
            soup = BeautifulSoup(r.text, "html.parser")
            rows = soup.select("table.tenders tr, div.tender-row, div.tender-item, tr[data-id]")
            logger.info(f"[Zakupki-Online] 找到 {len(rows)} 条记录")
            for row in rows[:30]:
                t = make_empty_tender()
                try:
                    title_el = row.select_one("a, .title, .name, h3, h4")
                    t["title"] = title_el.get_text(strip=True) if title_el else ""

                    price_el = row.select_one(".price, .cost, .value, td:nth-child(n)")
                    if price_el:
                        price_text = re.sub(r"[^\d,.]", "", price_el.get_text(strip=True))
                        price_text = price_text.replace(",", ".")
                        try:
                            t["price"] = float(price_text)
                        except ValueError:
                            t["price"] = 0.0

                    customer_el = row.select_one(".customer, .buyer, td:nth-child(2)")
                    t["customer"] = customer_el.get_text(strip=True) if customer_el else ""

                    date_el = row.select_one(".date, time, td:nth-child(n)")
                    t["publish_date"] = date_el.get_text(strip=True) if date_el else ""

                    link_el = row.select_one("a[href]")
                    if link_el:
                        href = link_el.get("href", "")
                        t["source_url"] = urljoin(
                            TENDER_PLATFORMS["zakupki_online"]["base_url"], href
                        )

                    t["source_name"] = "Zakupki-Online"
                    t["region"] = region or "РФ"
                    if t["title"]:
                        tenders.append(t)
                except Exception as e:
                    logger.warning(f"[Zakupki-Online] 解析单条失败: {e}")
                    continue
        except Exception as e:
            logger.error(f"[Zakupki-Online] 搜索异常: {e}")
        return tenders

    def _search_by_yandex(self, keywords, date_from, date_to, region=""):
        """
        通过 Yandex site: 搜索补充招标信息
        补充覆盖率较低的民间平台
        """
        tenders = []
        try:
            region_tag = f"site:{region}" if region and region != "РФ" else ""
            query_parts = keywords if isinstance(keywords, list) else [keywords]
            # 构建 site: 搜索词
            site_queries = [
                f"{q} закупка zakupki {region_tag}" for q in query_parts
            ]
            base = "https://yandex.ru/search/?text={q}&lr=213&nd=1"
            for sq in site_queries[:3]:
                url = base.format(q=quote_plus(sq))
                r = self._safe_request(url)
                if not r:
                    continue
                soup = BeautifulSoup(r.text, "html.parser")
                results = soup.select("li.serp-item, div.serp-item")
                logger.info(f"[Yandex site:] 找到 {len(results)} 条")
                for res in results[:10]:
                    t = make_empty_tender()
                    try:
                        title_el = res.select_one("h2 a, .OrganicTitle-Link")
                        t["title"] = title_el.get_text(strip=True) if title_el else ""

                        snippet_el = res.select_one(".OrganicTextContentSpan, .text-container")
                        snippet = snippet_el.get_text(strip=True) if snippet_el else ""

                        # 从 snippet 提取金额
                        price_m = re.search(r"([\d\s]+)\s*(руб|р\.|₽|RUB|USD|\$)", snippet, re.I)
                        if price_m:
                            price_text = re.sub(r"[^\d,.]", "", price_m.group(1))
                            price_text = price_text.replace(",", ".")
                            try:
                                t["price"] = float(price_text)
                            except ValueError:
                                pass

                        link_el = res.select_one("a")
                        if link_el:
                            href = link_el.get("href", "")
                            t["source_url"] = href

                        t["source_name"] = "Yandex"
                        t["region"] = region or "РФ"
                        if t["title"]:
                            tenders.append(t)
                    except Exception as e:
                        logger.warning(f"[Yandex] 解析失败: {e}")
                        continue
                time.sleep(random.uniform(2, 4))
        except Exception as e:
            logger.error(f"[Yandex site:] 搜索异常: {e}")
        return tenders

    # ═══════════════════════════════════════════════════════════════════════════
    # 公开 API
    # ═══════════════════════════════════════════════════════════════════════════

    def search_tenders(self, keywords, date_from="", date_to="", region="", max_pages=3):
        """
        综合搜索招标公告，覆盖所有平台

        Args:
            keywords: str 或 list，搜索关键词（支持俄语）
            date_from: str，起始日期 "YYYY-MM-DD"
            date_to: str，结束日期 "YYYY-MM-DD"
            region: str，区域（如 "Москва", "СПб", "РФ"）
            max_pages: int，最大页数（当前只取第一页）

        Returns:
            list[dict]: 招标列表，每条字段见 make_empty_tender()
        """
        if isinstance(keywords, str):
            keywords = [keywords]

        logger.info(f"=== 招标搜索开始 ===")
        logger.info(f"关键词: {keywords}, 日期: {date_from} ~ {date_to}, 区域: {region}")

        all_tenders = []

        # 各平台独立搜索，任一失败不影响其他
        logger.info("[1/4] 搜索 ЕИС (zakupki.gov.ru)...")
        eiis = self._search_zakupki_gov(keywords, date_from, date_to, region)
        all_tenders.extend(eiis)
        logger.info(f"  → ЕИС 返回 {len(eiis)} 条")
        time.sleep(random.uniform(2, 4))

        logger.info("[2/4] 搜索 TenderGuru...")
        tg = self._search_tenderguru(keywords, date_from, date_to, region)
        all_tenders.extend(tg)
        logger.info(f"  → TenderGuru 返回 {len(tg)} 条")
        time.sleep(random.uniform(2, 4))

        logger.info("[3/4] 搜索 Zakupki-Online...")
        zo = self._search_zakupki_online(keywords, date_from, date_to, region)
        all_tenders.extend(zo)
        logger.info(f"  → Zakupki-Online 返回 {len(zo)} 条")
        time.sleep(random.uniform(2, 4))

        logger.info("[4/4] 通过 Yandex site: 补充搜索...")
        yx = self._search_by_yandex(keywords, date_from, date_to, region)
        all_tenders.extend(yx)
        logger.info(f"  → Yandex 返回 {len(yx)} 条")

        # 去重（按标题+来源URL）
        seen = set()
        unique = []
        for t in all_tenders:
            key = (t.get("title", "")[:50], t.get("source_url", ""))
            if key not in seen:
                seen.add(key)
                unique.append(t)

        logger.info(f"=== 搜索完成: 共 {len(unique)} 条（去重后）===")
        self.results = unique
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._save_result(f"search_{ts}.json", unique)
        return unique

    def get_tender_detail(self, tender_url):
        """
        获取单个招标详细信息

        Args:
            tender_url: str，招标页面 URL

        Returns:
            dict: 招标详情
        """
        logger.info(f"获取招标详情: {tender_url}")
        t = make_empty_tender()
        t["source_url"] = tender_url

        try:
            r = self._safe_request(tender_url)
            if not r:
                return t
            soup = BeautifulSoup(r.text, "html.parser")

            # 尝试从 URL 判断来源
            if "zakupki.gov.ru" in tender_url:
                # 标题
                title_el = soup.select_one(
                    "div.page-info__title, h1, .registry-entry__body-hint, .padbottom h1"
                )
                t["title"] = title_el.get_text(strip=True) if title_el else ""

                # 编号
                num_el = soup.select_one("div[data-id=regNum], .registry-entry__number")
                t["id"] = num_el.get_text(strip=True) if num_el else ""

                # 采购方
                cust_el = soup.select_one(
                    "div[data-id=customerName], .customer-info, .customer-info__name"
                )
                t["customer"] = cust_el.get_text(strip=True) if cust_el else ""

                # 中标方
                winner_el = soup.select_one(
                    "div[data-id=supplierNameInfo], .supplier-info, .winner-info"
                )
                t["winner"] = winner_el.get_text(strip=True) if winner_el else ""

                # 价格（取最高）
                price_els = soup.select("div.price-block__value, .price, .cost, .tender-price")
                for pe in price_els:
                    try:
                        val = re.sub(r"[^\d,.]", "", pe.get_text(strip=True)).replace(",", ".")
                        v = float(val)
                        if v > t["price"]:
                            t["price"] = v
                    except ValueError:
                        continue

                # 数量 / 规格
                qty_el = soup.select_one("div[data-id=quantity], .quantity, .qty-info")
                t["quantity"] = qty_el.get_text(strip=True) if qty_el else ""

                specs_el = soup.select_one("div[data-id=okpdCode], .okpd, .specs")
                t["specs"] = specs_el.get_text(strip=True) if specs_el else ""

                # 日期
                pub_el = soup.select_one("div[data-id=publishDate], .publish-date, time")
                t["publish_date"] = pub_el.get_text(strip=True) if pub_el else ""

                deadline_el = soup.select_one(
                    "div[data-id=endDate], .deadline, .application-deadline"
                )
                t["deadline"] = deadline_el.get_text(strip=True) if deadline_el else ""

                t["source_name"] = "ЕИС Закупки"

            else:
                # 通用解析（民间平台）
                title_el = soup.select_one("h1, h2, .title, .tender-title")
                t["title"] = title_el.get_text(strip=True) if title_el else ""

                info_blocks = soup.select("div.info, .detail-row, .field, tr")
                for block in info_blocks:
                    label_el = block.select_one("th, .label, .field-name, strong")
                    value_el = block.select_one("td, .value, .field-value, span")
                    label = label_el.get_text(strip=True).lower() if label_el else ""
                    value = value_el.get_text(strip=True) if value_el else ""

                    if "заказчик" in label or "customer" in label:
                        t["customer"] = value
                    elif "поставщик" in label or "winner" in label or "подрядчик" in label:
                        t["winner"] = value
                    elif "цена" in label or "стоимость" in label or "price" in label:
                        price_text = re.sub(r"[^\d,.]", "", value).replace(",", ".")
                        try:
                            t["price"] = float(price_text)
                        except ValueError:
                            pass
                    elif "кол" in label or "qty" in label or "объём" in label:
                        t["quantity"] = value
                    elif "срок" in label or "deadline" in label:
                        t["deadline"] = value

                t["source_name"] = "Unknown"

            logger.info(f"详情获取成功: {t['title'] or tender_url}")
        except Exception as e:
            logger.error(f"详情获取失败 [{tender_url}]: {e}")

        return t

    def get_tender_history(self, company_name, date_from="", date_to=""):
        """
        获取某公司的历史中标记录

        Args:
            company_name: str，公司全称或简称
            date_from: str，起始日期
            date_to: str，结束日期

        Returns:
            list[dict]: 中标记录列表
        """
        logger.info(f"=== 查询公司中标历史: {company_name} ===")
        records = []

        # 方法1：直接在 ЕИС 搜索公司名
        try:
            params = {
                "searchString": company_name,
                "sortBy": "PUBLISH_DATE",
                "pageNumber": 1,
            }
            # ЕИС 有供应商搜索页面
            supplier_url = "https://zakupki.gov.ru/epz/order/extendedsearch/riscpec.html"
            r = self._safe_request(supplier_url, params=params)
            if r:
                soup = BeautifulSoup(r.text, "html.parser")
                items = soup.select("div.search-registry-entry-block")
                logger.info(f"[公司历史] ЕИС 找到 {len(items)} 条")
                for item in items[:50]:
                    t = make_empty_tender()
                    try:
                        title_el = item.select_one("div.registry-entry__body-hint")
                        t["title"] = title_el.get_text(strip=True) if title_el else ""
                        num_el = item.select_one("div.registry-entry__law-number")
                        t["id"] = num_el.get_text(strip=True) if num_el else ""
                        price_el = item.select_one("div.price-block__value")
                        if price_el:
                            price_text = re.sub(r"[^\d,.]", "",
                                                price_el.get_text(strip=True)).replace(",", ".")
                            try:
                                t["price"] = float(price_text)
                            except ValueError:
                                t["price"] = 0.0
                        t["winner"] = company_name
                        cust_el = item.select_one("div.customer-info__name")
                        t["customer"] = cust_el.get_text(strip=True) if cust_el else ""
                        deadline_el = item.select_one("div.date-block")
                        t["deadline"] = deadline_el.get_text(strip=True) if deadline_el else ""
                        link_el = item.select_one("a.registry-entry__body-hint")
                        if link_el:
                            href = link_el.get("href", "")
                            t["source_url"] = urljoin(
                                TENDER_PLATFORMS["zakupki_gov"]["base_url"], href
                            )
                        t["source_name"] = "ЕИС Закупки"
                        if t["title"]:
                            records.append(t)
                    except Exception as e:
                        logger.warning(f"[公司历史] 解析失败: {e}")
                        continue
                time.sleep(random.uniform(2, 4))
        except Exception as e:
            logger.error(f"[公司历史] ЕИС 搜索异常: {e}")

        # 方法2：Yandex site: 搜索 "компания" + "победитель"
        try:
            query = quote_plus(f'"{company_name}" победитель закупка')
            url = f"https://yandex.ru/search/?text={query}&lr=213"
            r = self._safe_request(url)
            if r:
                soup = BeautifulSoup(r.text, "html.parser")
                results = soup.select("li.serp-item")
                logger.info(f"[公司历史] Yandex 找到 {len(results)} 条")
                for res in results[:20]:
                    t = make_empty_tender()
                    title_el = res.select_one("h2 a")
                    t["title"] = title_el.get_text(strip=True) if title_el else ""
                    snippet_el = res.select_one(".OrganicTextContentSpan")
                    snippet = snippet_el.get_text(strip=True) if snippet_el else ""
                    price_m = re.search(r"([\d\s]+)\s*(руб|р\.|₽)", snippet, re.I)
                    if price_m:
                        price_text = re.sub(r"[^\d,.]", "", price_m.group(1)).replace(",", ".")
                        try:
                            t["price"] = float(price_text)
                        except ValueError:
                            pass
                    t["winner"] = company_name
                    link_el = res.select_one("a")
                    if link_el:
                        t["source_url"] = link_el.get("href", "")
                    t["source_name"] = "Yandex"
                    if t["title"]:
                        records.append(t)
                time.sleep(random.uniform(2, 4))
        except Exception as e:
            logger.error(f"[公司历史] Yandex 搜索异常: {e}")

        # 去重
        seen = set()
        unique = []
        for rec in records:
            key = (rec.get("title", "")[:50], rec.get("source_url", ""))
            if key not in seen:
                seen.add(key)
                unique.append(rec)

        logger.info(f"=== 公司历史完成: {len(unique)} 条 ===")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = re.sub(r"[^\w]", "_", company_name)
        self._save_result(f"history_{safe_name}_{ts}.json", unique)
        return unique

    def analyze_competitor_tenders(self, competitor_name, date_from="", date_to=""):
        """
        分析竞品公司中标历史，统计其中标区域、价格区间、频率

        Args:
            competitor_name: str，竞品公司名
            date_from: str
            date_to: str

        Returns:
            dict: 分析报告
        """
        logger.info(f"=== 分析竞品: {competitor_name} ===")
        records = self.get_tender_history(competitor_name, date_from, date_to)

        if not records:
            logger.warning(f"未找到竞品 {competitor_name} 的中标记录")
            return {
                "competitor": competitor_name,
                "total_contracts": 0,
                "report": "未找到中标记录",
                "records": [],
            }

        # 价格统计
        prices = [r["price"] for r in records if r["price"] > 0]
        price_stats = {}
        if prices:
            price_stats = {
                "min": min(prices),
                "max": max(prices),
                "avg": round(sum(prices) / len(prices), 2),
                "count": len(prices),
            }

        # 区域分布
        region_counts = {}
        for r in records:
            reg = r.get("region", "未知")
            region_counts[reg] = region_counts.get(reg, 0) + 1

        # 采购方分布
        customer_counts = {}
        for r in records:
            cust = r.get("customer", "未知")
            if cust:
                customer_counts[cust] = customer_counts.get(cust, 0) + 1

        top_customers = sorted(customer_counts.items(), key=lambda x: -x[1])[:10]

        report = {
            "competitor": competitor_name,
            "total_contracts": len(records),
            "price_stats": price_stats,
            "region_distribution": region_counts,
            "top_customers": top_customers,
            "records": records[:20],  # 保留最多20条原始记录
            "analyzed_at": datetime.now().isoformat(),
        }

        logger.info(f"竞品分析完成: {competitor_name}, {len(records)} 条记录")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = re.sub(r"[^\w]", "_", competitor_name)
        self._save_result(f"competitor_{safe_name}_{ts}.json", report)
        return report

    def get_market_price_from_tenders(self, category, date_from="", date_to="", region=""):
        """
        从历史招标中提取市场参考价

        Args:
            category: str，品类名（如 "глюкометр" / "тонометр"）
            date_from: str
            date_to: str
            region: str

        Returns:
            dict: 市场参考价分析
        """
        logger.info(f"=== 提取市场参考价: {category} ===")

        # 从 CATEGORY_KEYWORDS 获取对应关键词
        keywords_list = [category]
        for cat_name, cat_data in CATEGORY_KEYWORDS.items():
            if cat_name in category or category in cat_name:
                keywords_list = cat_data.get("ru", [category])
                break

        records = self.search_tenders(
            keywords=keywords_list,
            date_from=date_from,
            date_to=date_to,
            region=region,
        )

        if not records:
            logger.warning(f"未找到 {category} 相关招标")
            return {
                "category": category,
                "sample_count": 0,
                "market_prices": [],
                "reference_price": None,
            }

        prices = [r["price"] for r in records if r["price"] > 0]

        if not prices:
            logger.warning(f"{category} 招标中找到价格数据为0")
            return {
                "category": category,
                "sample_count": 0,
                "market_prices": [],
                "reference_price": None,
            }

        sorted_prices = sorted(prices)
        n = len(sorted_prices)
        reference_price = round(sum(prices) / len(prices), 2)
        p25 = sorted_prices[max(0, n // 4 - 1)]
        p50 = sorted_prices[n // 2]
        p75 = sorted_prices[min(n - 1, 3 * n // 4)]

        result = {
            "category": category,
            "sample_count": len(prices),
            "market_prices": prices[:50],   # 最多50条样本
            "reference_price": reference_price,
            "price_percentiles": {
                "p25": round(p25, 2),
                "p50": round(p50, 2),
                "p75": round(p75, 2),
                "min": round(min(prices), 2),
                "max": round(max(prices), 2),
            },
            "currency": "RUB",
            "unit": "招标含税总价",
            "records": records,
            "extracted_at": datetime.now().isoformat(),
        }

        logger.info(
            f"市场参考价完成: {category}, 参考价={reference_price} RUB, "
            f"样本={len(prices)}条"
        )
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_cat = re.sub(r"[^\w]", "_", category)
        self._save_result(f"market_price_{safe_cat}_{ts}.json", result)
        return result

    def get_regional_platforms(self):
        """返回俄罗斯各联邦主体主要招标平台 URL 列表"""
        return {
            "Москва": "https://mos.ru/afisha/tenders/",
            "Санкт-Петербург": "https://piter.ru/procedure/",
            "Московская обл.": "https://mosreg.ru/tenders",
            "Краснодарский край": "https://krd.ru/tenders",
            "Республика Татарстан": "https://tatarstan.ru/tenders",
            "Свердловская обл.": "https://midural.ru/tenders",
            "Новосибирская обл.": "https://nso.ru/tenders",
            "Красноярский край": "https://krasnoyarsk Krai.ru/tenders",
            "Ростовская обл.": "https://rostov.ru/tenders",
            "Челябинская обл.": "https://gov74.ru/tenders",
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 独立运行入口
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="俄罗斯政府采购招标监控")
    parser.add_argument("--keywords", nargs="+", default=["глюкометр"], help="搜索关键词（俄语）")
    parser.add_argument("--date-from", default="", help="起始日期 YYYY-MM-DD")
    parser.add_argument("--date-to", default="", help="结束日期 YYYY-MM-DD")
    parser.add_argument("--region", default="", help="区域（如 Москва）")
    parser.add_argument("--company", default="", help="查询公司中标历史")
    parser.add_argument("--competitor", default="", help="竞品分析")
    parser.add_argument("--market-price", default="", help="提取品类市场参考价")

    args = parser.parse_args()

    monitor = TenderMonitor()

    if args.competitor:
        result = monitor.analyze_competitor_tenders(
            args.competitor, args.date_from, args.date_to
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.company:
        result = monitor.get_tender_history(
            args.company, args.date_from, args.date_to
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.market_price:
        result = monitor.get_market_price_from_tenders(
            args.market_price, args.date_from, args.date_to, args.region
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        result = monitor.search_tenders(
            args.keywords, args.date_from, args.date_to, args.region
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
