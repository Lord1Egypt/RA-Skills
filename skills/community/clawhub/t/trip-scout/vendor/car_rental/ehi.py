"""
一嗨租车网点查询

一嗨租车无公开 JSON API，通过 Playwright 解析 SSR 页面获取网点列表。

URL 规律:
  - 城市列表页: https://www.1hai.cn/Premises/Index
  - 网点列表页: https://www.1hai.cn/yyd_{城市拼音}/

页面结构: 每个网点是一个 <ul>，含 .store-name / .store-address / .store-phone 子元素。
"""

from __future__ import annotations

import re
from typing import Any

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    raise ImportError("请先安装 playwright: pip install playwright && playwright install chromium")

from .models import StoreInfo


_PREMISES_URL = "https://www.1hai.cn/Premises/Index"

# Premises/Index 页面是"精选页"，缺很多有网点的城市（实测连哈密/喀什/阿勒泰都没有）。
# 补充映射：已通过 yyd_<拼音>/ 页面标题含"<城市>租车"验证真实存在（2026-08-11 实测）。
_CITY_PINYIN_SUPPLEMENT = {
    "阿勒泰": "aletai", "博乐": "bole", "伊宁": "yining", "克拉玛依": "kelamayi",
    "哈密": "hami", "吐鲁番": "tulufan", "库尔勒": "kuerle", "喀什": "kashi",
    "和田": "hetian", "阿克苏": "akesu",
}

# 模块级缓存: {城市名: 拼音}
_city_map_cache: dict[str, str] | None = None


def _get_city_map() -> dict[str, str]:
    """获取一嗨租车城市映射，返回 {城市名: 拼音}

    数据源: Premises/Index 页面抓取 + 补充映射表（页面缺漏的城市）。
    """
    global _city_map_cache
    if _city_map_cache is not None:
        return _city_map_cache

    mapping: dict[str, str] = dict(_CITY_PINYIN_SUPPLEMENT)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        page.goto(_PREMISES_URL, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(2000)

        for link in page.query_selector_all("a"):
            href = link.get_attribute("href") or ""
            text = link.inner_text().strip()
            # 匹配 /yyd_xxx/ 格式
            m = re.search(r"/yyd_([a-z]+)/?", href)
            if m and text:
                pinyin = m.group(1)
                # 城市名去掉"租车"后缀
                city = text.replace("租车", "").strip()
                if city and city not in mapping:
                    mapping[city] = pinyin

        browser.close()

    _city_map_cache = mapping
    return mapping


def _resolve_city_pinyin(city_name: str) -> str:
    """城市名 -> 拼音，支持精确匹配和包含匹配"""
    cities = _get_city_map()

    if city_name in cities:
        return cities[city_name]

    for name, py in cities.items():
        if city_name in name or name in city_name:
            return py

    raise ValueError(f"一嗨租车未找到城市: {city_name}")


_TIME_RANGE_RE = re.compile(r"\d{1,2}:\d{2}\s*[-–—~至]\s*\d{1,2}:\d{2}")


def _parse_store(ul_element: Any) -> StoreInfo | None:
    """解析一个 <ul> 网点块，返回 StoreInfo 或 None"""
    name_el = ul_element.query_selector(".store-name")
    if not name_el:
        return None

    # name 只取 li 直接文本节点，排除 <em> 徽标（机场/高铁站/自助等）
    name = name_el.evaluate(
        "el => Array.from(el.childNodes)"
        ".filter(n => n.nodeType === 3)"
        ".map(n => n.textContent).join('').trim()"
    )
    if not name:
        name = name_el.inner_text().strip()

    addr_el = ul_element.query_selector(".store-address")
    address = addr_el.inner_text().strip() if addr_el else ""

    phone_el = ul_element.query_selector(".store-phone span")
    phone = phone_el.inner_text().strip() if phone_el else ""

    # 营业时间: 优先 .store-time 的首个 span（干净时间），
    # 兜底从块全文正则提取时间段（避免混入 time-tips 提示文本）
    work_time = ""
    time_el = ul_element.query_selector(".store-time span")
    if time_el:
        work_time = time_el.inner_text().strip()
    if not work_time:
        m = re.search(r"营业时间[：:]\s*(.+)", ul_element.inner_text())
        if m:
            line = m.group(1).strip().split("\n")[0].strip()
            tm = _TIME_RANGE_RE.search(line)
            work_time = tm.group(0).replace(" ", "") if tm else line

    # em 徽标文本（机场/高铁站/自助等）
    em_texts = []
    for em in name_el.query_selector_all("em"):
        em_text = em.inner_text().strip()
        if em_text:
            em_texts.append(em_text)

    # 机场/火车站/自助推断: name + em 徽标一起做关键词匹配
    full_name = name + "".join(em_texts)
    is_airport = "机场" in full_name
    is_train = any(k in full_name for k in ("高铁", "火车站", "动车"))
    is_self = "自助" in full_name

    return StoreInfo(
        name=name,
        address=address,
        phone=phone,
        work_time=work_time,
        source="ehi",
        is_self_service=is_self,
        is_airport=is_airport,
        is_train_station=is_train,
    )


def _fallback_parse(html: str) -> list[StoreInfo]:
    """页面结构变更时的全文提取兜底: 宽松匹配含 store*name 类名的 li 块"""
    stores: list[StoreInfo] = []
    for m in re.finditer(
        r'<li[^>]*class="[^"]*store-?name[^"]*"[^>]*>(.*?)</li>',
        html,
        re.S | re.I,
    ):
        raw = re.sub(r"<em[^>]*>.*?</em>", " ", m.group(1), flags=re.S)
        raw = re.sub(r"<[^>]+>", " ", raw)
        name = re.sub(r"\s+", " ", raw).strip()
        if name:
            stores.append(
                StoreInfo(name=name, address="", phone="", work_time="", source="ehi")
            )
    return stores


def get_stores(city_name: str) -> list[StoreInfo]:
    """查询一嗨租车某城市的全部网点

    降级链: 结构化解析 -> 全文正则兜底 -> 仍失败抛 RuntimeError
    （上层 get_stores 捕获后跳过一嗨只返回神州）
    """
    city_name = (city_name or "").strip()
    if not city_name:
        raise ValueError("城市名不能为空")

    pinyin = _resolve_city_pinyin(city_name)
    url = f"https://www.1hai.cn/yyd_{pinyin}/"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(2000)

        stores: list[StoreInfo] = []
        for ul in page.query_selector_all("ul"):
            store = _parse_store(ul)
            if store:
                stores.append(store)

        # 兜底: 页面结构变更时尝试全文正则提取
        if not stores:
            stores = _fallback_parse(page.content())

        browser.close()

    if not stores:
        raise RuntimeError(f"一嗨租车页面解析失败（结构可能已变更）: {url}")

    return stores
