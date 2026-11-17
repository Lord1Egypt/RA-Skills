"""
携程航班数据抓取模块

通过 Playwright 捕获携程航班列表页 API 响应，解析航班票价/余票/降价预测。
API 降级链: batchSearch 行程API -> DOM 解析 -> 最低价API

依赖: vendor/ctrip/client.py (CtripClient)
参考: /Users/tree/Develop/ctrip-flight-alter (Playwright + API 拦截方案)
"""
from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any
from urllib.parse import quote

import requests

from .client import CtripClient


# ── 常量 ──────────────────────────────────────────────────────────────────

CTRIP_FLIGHT_URL_TEMPLATE = (
    "https://flights.ctrip.com/online/list/oneway-{dep}-{arr}"
    "?depdate={date}&cabin=y_s_c_f&adult=1&child=0&infant=0"
)
CTRIP_BATCH_SEARCH_KEYWORD = "/search/api/search/batchSearch"
CTRIP_REPO_LOWEST_PRICE_URL = "https://flights.ctrip.com/itinerary/api/12808/lowestPrice"

# 常见城市三字码（携程 URL 用小写）
CITY_CODES: dict[str, str] = {
    "成都": "ctu", "伊宁": "yin", "乌鲁木齐": "urc",
    "北京": "bjs", "上海": "sha", "广州": "can",
    "深圳": "szx", "昆明": "kmg", "西安": "sia",
    "杭州": "hgh", "重庆": "ckg", "兰州": "lhw",
    "喀什": "khg", "阿勒泰": "aati", "克拉玛依": "kry",
    "库车": "kca", "吐鲁番": "tlq", "若羌": "rqa",
    "阿克苏": "aku", "和田": "htn", "石河子": "shf",
    "博乐": "bpl",
}

# 中国低成本/廉航航司（价格对比分析时默认排除）
# 匹配方式: 航司名称包含关键词 或 航班号前缀匹配
BUDGET_AIRLINES: dict[str, list[str]] = {
    "春秋航空": ["9C"],
    "西部航空": ["PN"],
    "九元航空": ["AQ"],
    "中国联合航空": ["KN"],
    "祥鹏航空": ["8L"],
}
# 扁平化: 航班号前缀集合
_BUDGET_FLIGHT_PREFIXES = {p for prefixes in BUDGET_AIRLINES.values() for p in prefixes}
# 扁平化: 航司名称关键词集合
_BUDGET_AIRLINE_NAMES = set(BUDGET_AIRLINES.keys())


def is_budget_airline(airlines: str, flight_numbers: str = "") -> bool:
    """判断是否为廉航航司

    Args:
        airlines: 航司名称，如 "春秋航空" 或 "中国国航 / 春秋航空"
        flight_numbers: 航班号，如 "9C7369" 或 "CA4101/MU5678"
    """
    # 按航司名称匹配
    for name in _BUDGET_AIRLINE_NAMES:
        if name in airlines:
            return True
    # 按航班号前缀匹配
    for num in flight_numbers.replace(" ", "").split("/"):
        num = num.strip()
        if len(num) >= 2 and num[:2] in _BUDGET_FLIGHT_PREFIXES:
            return True
        # 三字代码前缀（如 G52611 -> 取前2位不够，取字母部分）
        letters = "".join(c for c in num if c.isalpha())
        if letters and any(letters.startswith(p) for p in _BUDGET_FLIGHT_PREFIXES):
            return True
    return False


# 多机场城市信息（通勤成本影响航班选择）
# 参考 references/flight-search.md 机场信息输出规则
MULTI_AIRPORT_CITIES: dict[str, dict[str, Any]] = {
    "成都": {
        "双流": {"code": "CTU", "keywords": ["双流"], "commute_time": "30min", "commute_cost": 50,  "preferred": True},
        "天府": {"code": "TFU", "keywords": ["天府"], "commute_time": "1h",   "commute_cost": 150, "preferred": False},
    },
    "上海": {
        "虹桥": {"code": "SHA", "keywords": ["虹桥"], "commute_time": "40min", "commute_cost": 60,  "preferred": True},
        "浦东": {"code": "PVG", "keywords": ["浦东"], "commute_time": "1h",    "commute_cost": 120, "preferred": False},
    },
    "北京": {
        "首都": {"code": "PEK", "keywords": ["首都"], "commute_time": "40min", "commute_cost": 80,  "preferred": True},
        "大兴": {"code": "PKX", "keywords": ["大兴"], "commute_time": "1h",    "commute_cost": 150, "preferred": False},
    },
}

# 时段定义
TIME_PERIODS: list[tuple[str, str, str]] = [
    ("早班", "06:00", "08:59"),
    ("上午", "09:00", "11:59"),
    ("下午", "12:00", "17:59"),
    ("晚班", "18:00", "23:59"),
]


def match_airport(airport_name: str, city: str) -> dict[str, Any] | None:
    """匹配机场名称到 MULTI_AIRPORT_CITIES 中的机场信息"""
    city_airports = MULTI_AIRPORT_CITIES.get(city)
    if not city_airports:
        return None
    for key, info in city_airports.items():
        if any(kw in airport_name for kw in info["keywords"]):
            return {"key": key, **info}
    return None


def classify_time_period(time_str: str) -> str:
    """将时间字符串分类到时段"""
    if not time_str or ":" not in time_str:
        return "未知"
    try:
        h, m = int(time_str[:2]), int(time_str[3:5])
        minutes = h * 60 + m
    except (ValueError, IndexError):
        return "未知"
    for name, start, end in TIME_PERIODS:
        sh, sm = int(start[:2]), int(start[3:5])
        eh, em = int(end[:2]), int(end[3:5])
        if sh * 60 + sm <= minutes <= eh * 60 + em:
            return name
    return "未知"


# 注入 JS: 拦截 XHR/fetch，将响应存入 window.__flightCapture.requests[]
FLIGHT_CAPTURE_JS = """
(() => {
  const state = { requests: [] };
  window.__flightCapture = state;
  const capture = (meta, status, text) => {
    state.requests.push({
      url: meta.url || '', method: meta.method || '',
      status: status || 0, responseText: text || '', ts: Date.now()
    });
  };
  const origOpen = XMLHttpRequest.prototype.open;
  const origSend = XMLHttpRequest.prototype.send;
  XMLHttpRequest.prototype.open = function(method, url) {
    this.__fcMeta = { method, url };
    return origOpen.apply(this, arguments);
  };
  XMLHttpRequest.prototype.send = function(body) {
    this.addEventListener('loadend', function() {
      let text = '';
      try { text = this.responseText || ''; } catch(_) {}
      capture(this.__fcMeta || {}, this.status, text);
    });
    return origSend.apply(this, arguments);
  };
  const origFetch = window.fetch;
  window.fetch = async function(input, init) {
    const meta = {
      method: (init && init.method) || 'GET',
      url: typeof input === 'string' ? input : ((input && input.url) || '')
    };
    const resp = await origFetch.apply(this, arguments);
    try {
      const clone = resp.clone();
      clone.text().then(text => capture(meta, resp.status, text));
    } catch(_) {}
    return resp;
  };
})();
"""

# 预测关键词（用于扫描 API 响应和 DOM 文本）
_PREDICTION_KEYWORDS = [
    "降价", "可能降", "概率", "趋势", "预测", "低点",
    "priceTrend", "priceForecast", "priceTip", "priceAdvice",
    "lowPriceTip", "bookingTip", "flightTip", "priceStrategy",
    "建议购买", "购买建议", "降价提醒", "低价提醒",
]
# DOM 中可能包含预测的区域
_PREDICTION_SELECTORS = [
    ".low-price-remind", ".price-trend", ".price-tip",
    ".flight-tips", ".notice-box", ".alert-title",
    ".booking-advice", ".price-forecast", ".price-strategy",
    ".recommend-tip", ".low-price-tip", ".price-reminder",
]

# 余票正则
_REMAINING_SEAT_RE = re.compile(r"仅剩\s*(\d+)\s*张")
# 预测正则
_PREDICT_PRICE_RE = re.compile(r"(?:可能降价至|最低可能|低至|降至)\s*[￥¥]?\s*(\d{3,5})")
_PREDICT_PROB_RE = re.compile(r"概率\s*(\d{1,3})\s*%")
_PREDICT_TIME_RE = re.compile(r"(未来\d+天|近\d+天|一周内|两周内|一个月内)")


# ── 数据模型 ──────────────────────────────────────────────────────────────

@dataclass
class FlightTicket:
    """单张机票信息"""
    flight_numbers: str           # "CA4101" / "CA4101/MU5678"
    airlines: str                 # "中国国航"
    departure_time: str           # "07:15"
    arrival_time: str             # "10:45"
    departure_airport: str        # "双流T2"
    arrival_airport: str          # "伊宁"
    flight_type: str              # "直飞" / "中转" / "经停"
    total_duration: str           # "3h30m"
    price: int                    # 800
    discount: str                 # "4.5折"
    remaining_seats: int | None = None    # 5 (从"仅剩5张"解析, None=未知)
    labels: list[str] = field(default_factory=list)  # ["仅剩5张", "含餐", ...]
    source: str = "api"           # "api" / "dom" / "lowest_price"


@dataclass
class PricePrediction:
    """携程降价预测数据（非必现，有则记录）"""
    raw_text: str                          # 原始文本
    predicted_price: int | None = None     # 预测低价 ¥650
    probability: int | None = None         # 降价概率 70 (%)
    time_range: str | None = None          # 时间范围 "未来30天"
    source: str = "dom"                    # "api" / "dom"


@dataclass
class FlightResult:
    """抓取结果"""
    tickets: list[FlightTicket]
    prediction: PricePrediction | None
    source: str  # "api" / "dom" / "lowest_price"


# ── 工具函数 ──────────────────────────────────────────────────────────────

def _resolve_city_code(city: str) -> str:
    """城市名 -> 携程三字码(小写)"""
    code = CITY_CODES.get(city)
    if not code:
        raise ValueError(f"未找到城市三字码: {city}（请在 CITY_CODES 中添加）")
    return code


def _build_flight_url(dep_city: str, arr_city: str, date: str) -> str:
    """构建携程航班列表页 URL"""
    dep_code = _resolve_city_code(dep_city)
    arr_code = _resolve_city_code(arr_city)
    return CTRIP_FLIGHT_URL_TEMPLATE.format(dep=dep_code, arr=arr_code, date=date)


def _combine_airport(name: str | None, terminal: str | None) -> str:
    """合并机场名和航站楼"""
    parts = [p for p in [name, terminal] if p and str(p).strip()]
    return "".join(parts) if parts else ""


def _split_datetime(text: Any) -> tuple[str, str]:
    """从 '2026-09-25 07:15:00' 提取日期和时间"""
    if not text:
        return "", ""
    s = str(text).strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            dt = datetime.strptime(s, fmt)
            return dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M")
        except ValueError:
            pass
    return "", ""


def _humanize_minutes(minutes: int) -> str:
    """分钟 -> '3h30m'"""
    if minutes <= 0:
        return ""
    h, m = divmod(minutes, 60)
    if h and m:
        return f"{h}h{m}m"
    if h:
        return f"{h}h"
    return f"{m}m"


def _format_discount_rate(value: Any) -> str:
    """折扣率 -> '4.5折'"""
    try:
        rate = float(value)
    except (TypeError, ValueError):
        return ""
    if rate <= 0:
        return ""
    fold = rate * 10 if rate <= 1 else rate
    fold = round(fold, 1)
    if float(fold).is_integer():
        return f"{int(fold)}折"
    return f"{fold:.1f}折"


def _dedupe(items: list[str]) -> list[str]:
    """去重保序"""
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def merge_codeshares(tickets: list[FlightTicket]) -> list[FlightTicket]:
    """合并代码共享航班（同一架飞机挂多个航司号）

    判定条件: departure_time + arrival_time + departure_airport + arrival_airport
              + total_duration + flight_type 完全一致

    合并策略:
    - 航班号/航司名合并展示: "3U1834 / CZ6840 / MF2259"
    - 价格取最低（各航司报价不同）
    - 折扣取最低折扣
    - 标签取并集
    - 余票取最小值（最紧张航司的库存）
    - 添加 "代码共享" 标签
    """
    if len(tickets) <= 1:
        return tickets

    groups: dict[tuple, list[FlightTicket]] = {}
    order: list[tuple] = []
    for t in tickets:
        key = (
            t.departure_time, t.arrival_time,
            t.departure_airport, t.arrival_airport,
            t.total_duration, t.flight_type,
        )
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(t)

    merged: list[FlightTicket] = []
    for key in order:
        group = groups[key]
        if len(group) == 1:
            merged.append(group[0])
            continue

        # 合并航班号和航司
        all_numbers = _dedupe(
            n.strip() for t in group for n in t.flight_numbers.split("/")
        )
        all_airlines = _dedupe(
            a.strip() for t in group for a in t.airlines.split("/")
        )

        # 取最低价
        best = min(group, key=lambda t: t.price)

        # 合并标签
        all_labels = _dedupe(l for t in group for l in t.labels)
        if "代码共享" not in all_labels:
            all_labels.insert(0, "代码共享")

        # 余票取最小值
        seat_values = [t.remaining_seats for t in group if t.remaining_seats is not None]
        remaining = min(seat_values) if seat_values else None

        merged.append(FlightTicket(
            flight_numbers=" / ".join(all_numbers),
            airlines=" / ".join(all_airlines),
            departure_time=best.departure_time,
            arrival_time=best.arrival_time,
            departure_airport=best.departure_airport,
            arrival_airport=best.arrival_airport,
            flight_type=best.flight_type,
            total_duration=best.total_duration,
            price=best.price,
            discount=best.discount,
            remaining_seats=remaining,
            labels=all_labels,
            source=best.source,
        ))

    return merged


def _parse_ctrip_ms_date(value: Any) -> str:
    """解析 /Date(1695580800000+0800)/ 格式"""
    if not value:
        return ""
    s = str(value)
    m = re.match(r"/Date\((-?\d+)", s)
    if m:
        ts = int(m.group(1)) / 1000
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
    return s


def _parse_remaining_seats(labels: list[str], dom_text: str = "") -> int | None:
    """从标签和DOM文本解析"仅剩X张" """
    for label in labels:
        m = _REMAINING_SEAT_RE.search(label)
        if m:
            return int(m.group(1))
    if dom_text:
        m = _REMAINING_SEAT_RE.search(dom_text)
        if m:
            return int(m.group(1))
    return None


# ── batchSearch API 响应解析 ──────────────────────────────────────────────

def _extract_price_labels(price: dict[str, Any]) -> tuple[str, list[str]]:
    """从 priceList 条目提取折扣率和标签"""
    labels: list[str] = []

    # 行李标签
    baggage_tag = str((price.get("baggage") or {}).get("baggageTag") or "").strip()
    if baggage_tag:
        labels.append(baggage_tag)

    # priceTags
    for tag in price.get("priceTags") or []:
        if isinstance(tag, dict):
            label = str(tag.get("label") or tag.get("title") or "").strip()
            if label:
                labels.append(label)

    # priceUnitList -> flightSeatList
    discount = ""
    for unit in price.get("priceUnitList") or []:
        if not isinstance(unit, dict):
            continue
        for seat in unit.get("flightSeatList") or []:
            if not isinstance(seat, dict):
                continue
            special_name = str(seat.get("specialClassName") or "").strip()
            if special_name:
                labels.append(special_name)
            dr = seat.get("discountRate")
            if dr is not None and dr != "" and not discount:
                discount = _format_discount_rate(dr)

    if discount and discount not in labels:
        labels.insert(0, discount)
    # 过滤无效折扣标签（如"0折"）
    labels = [l for l in labels if l != "0折"]
    return discount, _dedupe(labels)


def _parse_segment(flight: dict[str, Any]) -> dict[str, str]:
    """解析单个航段"""
    dep_date, dep_time = _split_datetime(flight.get("departureDateTime"))
    arr_date, arr_time = _split_datetime(flight.get("arrivalDateTime"))
    airline = str(flight.get("marketAirlineName") or flight.get("operateAirlineName") or "").strip()
    return {
        "airline": airline,
        "flight_no": str(flight.get("flightNo") or "").strip(),
        "departure_date": dep_date,
        "departure_time": dep_time,
        "departure_airport": _combine_airport(
            flight.get("departureAirportName"), flight.get("departureTerminal")),
        "arrival_date": arr_date,
        "arrival_time": arr_time,
        "arrival_airport": _combine_airport(
            flight.get("arrivalAirportName"), flight.get("arrivalTerminal")),
        "flight_duration": _humanize_minutes(int(flight.get("duration") or 0))
            if flight.get("duration") else "",
    }


def _parse_itinerary(itinerary: dict[str, Any]) -> FlightTicket:
    """解析单个 flightItineraryList 条目 -> FlightTicket"""
    flight_segments = itinerary.get("flightSegments") or []
    flight_group = flight_segments[0] if flight_segments else {}
    flights = [f for f in flight_group.get("flightList") or [] if isinstance(f, dict)]
    if not flights:
        raise ValueError("未找到可解析的航班信息")

    segments = [_parse_segment(f) for f in flights]
    first = segments[0]
    last = segments[-1]

    # 最佳价格（取最低 adultPrice）
    price_items = [
        p for p in itinerary.get("priceList") or []
        if isinstance(p, dict) and p.get("adultPrice") not in (None, "")
    ]
    best_price = min(price_items or [{}], key=lambda p: float(p.get("adultPrice") or 1e9))
    discount, labels = _extract_price_labels(best_price)
    if discount == "0折":
        discount = ""

    # 航司
    airlines = " / ".join(_dedupe(
        [s["airline"] for s in segments if s["airline"]]
        or [str(flight_group.get("airlineName") or "").strip()]
    ))
    flight_numbers = " / ".join(s["flight_no"] for s in segments if s["flight_no"])

    # 飞行类型
    transfer_count = int(flight_group.get("transferCount") or 0)
    stop_count = int(flight_group.get("stopCount") or 0)
    if transfer_count > 0 or len(segments) > 1:
        flight_type = "中转"
    elif stop_count > 0:
        flight_type = "经停"
    else:
        flight_type = "直飞"

    # 总时长
    total_duration = (
        _humanize_minutes(int(flight_group.get("duration") or 0))
        if flight_group.get("duration") else ""
    )

    # 余票
    remaining = _parse_remaining_seats(labels)

    return FlightTicket(
        flight_numbers=flight_numbers,
        airlines=airlines,
        departure_time=first["departure_time"],
        arrival_time=last["arrival_time"],
        departure_airport=first["departure_airport"],
        arrival_airport=last["arrival_airport"],
        flight_type=flight_type,
        total_duration=total_duration,
        price=int(float(best_price.get("adultPrice") or 0)),
        discount=discount,
        remaining_seats=remaining,
        labels=labels,
        source="api",
    )


def _parse_itineraries(payload: dict[str, Any]) -> list[FlightTicket]:
    """解析 batchSearch API 响应 -> FlightTicket[]"""
    itineraries = payload.get("data", {}).get("flightItineraryList", [])
    tickets: list[FlightTicket] = []
    for item in itineraries:
        if not isinstance(item, dict):
            continue
        try:
            tickets.append(_parse_itinerary(item))
        except (ValueError, KeyError):
            continue
    tickets.sort(key=lambda t: (t.price, t.departure_time, t.flight_numbers))
    return tickets


# ── batchSearch API 等待 ──────────────────────────────────────────────────

def _wait_for_batch_search(page, timeout_ms: int = 60000) -> dict[str, Any] | None:
    """等待并返回 batchSearch API 响应 (同步版)

    轮询 window.__flightCapture.requests，找到 batchSearch 响应并解析。
    """
    deadline = time.time() + timeout_ms / 1000
    poll_interval = 0.5
    latest_payload: dict[str, Any] | None = None

    while time.time() < deadline:
        logs = page.evaluate(
            f"""() => ((window.__flightCapture && window.__flightCapture.requests) || [])
                .filter(item => (item.url || '').includes('{CTRIP_BATCH_SEARCH_KEYWORD}'))"""
        )
        for item in sorted(logs, key=lambda r: r.get("ts", 0), reverse=True):
            try:
                payload = json.loads(item["responseText"])
            except (json.JSONDecodeError, KeyError):
                continue
            latest_payload = payload
            if int(payload.get("status", -1)) == 0:
                return payload
        time.sleep(poll_interval)

    return latest_payload


def _get_all_api_responses(page) -> list[dict[str, Any]]:
    """获取全部捕获的 API 响应（用于预测数据扫描）"""
    return page.evaluate(
        """() => ((window.__flightCapture && window.__flightCapture.requests) || [])"""
    ) or []


# ── DOM 解析（降级） ──────────────────────────────────────────────────────

def _extract_dom_tickets(page) -> list[FlightTicket]:
    """从 DOM 解析航班卡片（降级方案）

    参考 ctrip-flight-alter 的 _extract_visible_prices，适配 sync API。
    """
    raw_rows = page.evaluate("""() => {
        const clean = v => (v || '').replace(/[\\t\\r\\n]+/g, ' ').replace(/\\s+/g, ' ').trim();
        const text = (root, sel) => {
            const el = root.querySelector(sel);
            return el ? clean(el.textContent || '') : '';
        };
        const texts = (root, sel) => Array.from(root.querySelectorAll(sel))
            .map(el => clean(el.textContent || '')).filter(Boolean);
        const airportText = container => {
            if (!container) return '';
            return clean(text(container, '.airport .name') + text(container, '.airport .terminal'));
        };
        return Array.from(document.querySelectorAll('.flight-item.domestic')).map(card => {
            const fullText = clean(card.innerText || '');
            const nums = Array.from(new Set(
                fullText.toUpperCase().match(/\\b[A-Z0-9]{2,3}\\d{3,4}\\b/g) || []
            ));
            const price = text(card, '.flight-price .price').replace(/\\D+/g, '');
            const transferText = text(card, '.arrow-box [id^="transfer-text-"]');
            const daycross = text(card, '.arrive-box .day');
            const labels = texts(card, '.flight-tags .tag');
            // 扫描卡片全部文本找"仅剩"
            const remainingMatch = fullText.match(/仅剩\\s*(\\d+)\\s*张/);
            return {
                price,
                airlines: text(card, '.airline-name span') || text(card, '.airline'),
                flight_numbers: nums.join('/'),
                departure_time: text(card, '.depart-box .time'),
                arrival_time: text(card, '.arrive-box .time'),
                departure_airport: airportText(card.querySelector('.depart-box')),
                arrival_airport: airportText(card.querySelector('.arrive-box')),
                arrival_day_note: daycross,
                discount: text(card, '.sub-price-item'),
                labels: labels,
                remaining_text: remainingMatch ? remainingMatch[0] : '',
                flight_type: fullText.includes('经停') ? '经停'
                    : ((nums.length > 1 || /中转|转机/.test(transferText)) ? '中转' : '直飞')
            };
        });
    }""")

    tickets: list[FlightTicket] = []
    for row in raw_rows:
        if not str(row.get("price") or "").isdigit():
            continue
        labels = row.get("labels") or []
        remaining_text = row.get("remaining_text") or ""
        remaining = _parse_remaining_seats([remaining_text] + labels)
        discount = str(row.get("discount") or "").strip()
        if discount and discount not in labels:
            labels.insert(0, discount)
        tickets.append(FlightTicket(
            flight_numbers=row.get("flight_numbers") or "",
            airlines=row.get("airlines") or "",
            departure_time=row.get("departure_time") or "",
            arrival_time=row.get("arrival_time") or "",
            departure_airport=row.get("departure_airport") or "",
            arrival_airport=row.get("arrival_airport") or "",
            flight_type=row.get("flight_type") or "直飞",
            total_duration="",
            price=int(row["price"]),
            discount=discount,
            remaining_seats=remaining,
            labels=labels,
            source="dom",
        ))
    tickets.sort(key=lambda t: (t.price, t.departure_time))
    return tickets


# ── 降价预测提取 ──────────────────────────────────────────────────────────

def _extract_price_prediction(
    all_api_responses: list[dict[str, Any]],
    page,
) -> PricePrediction | None:
    """从全部API响应和DOM中提取携程降价预测数据

    双路搜索:
    1. API: 遍历所有捕获的响应，搜索含预测关键词的 JSON 字段
    2. DOM: 扫描页面文本，正则匹配降价预测模式

    非必现: 携程不总会展示预测，无则返回 None
    """
    # ── 路1: API 响应扫描 ──
    for resp in all_api_responses:
        text = resp.get("responseText") or ""
        if not text or len(text) < 10:
            continue
        # 快速过滤：不含任何预测关键词的跳过
        if not any(kw.lower() in text.lower() for kw in _PREDICTION_KEYWORDS):
            continue
        try:
            data = json.loads(text)
        except (json.JSONDecodeError, TypeError):
            continue
        found = _scan_json_for_prediction(data)
        if found:
            found.source = "api"
            return found

    # ── 路2: DOM 文本扫描 ──
    # 先尝试特定 selector 区域
    for selector in _PREDICTION_SELECTORS:
        try:
            el_text = page.evaluate(
                f"""() => {{
                    const el = document.querySelector('{selector}');
                    return el ? el.innerText : '';
                }}"""
            )
            if el_text:
                pred = _parse_prediction_text(el_text)
                if pred:
                    pred.source = "dom"
                    return pred
        except Exception:
            pass

    # 兜底：扫描页面全部可见文本（限制范围避免太慢）
    try:
        body_text = page.evaluate(
            """() => {
                const els = document.querySelectorAll(
                    '.flight-list, .search-result, .price-info, .list-content, .main-content'
                );
                let text = '';
                els.forEach(el => text += (el.innerText || '') + '\\n');
                return text;
            }"""
        )
        if body_text:
            pred = _parse_prediction_text(body_text)
            if pred:
                pred.source = "dom"
                return pred
    except Exception:
        pass

    return None


def _scan_json_for_prediction(data: Any, depth: int = 0) -> PricePrediction | None:
    """递归扫描 JSON 结构，查找预测相关字段"""
    if depth > 10:
        return None
    if isinstance(data, dict):
        # 检查当前 dict 的值
        for key, val in data.items():
            key_lower = str(key).lower()
            val_str = str(val) if val is not None else ""
            # 如果 key 或 value 包含预测关键词
            if any(kw.lower() in key_lower or kw.lower() in val_str.lower()
                   for kw in _PREDICTION_KEYWORDS):
                # 尝试从值文本解析预测
                pred = _parse_prediction_text(val_str)
                if pred:
                    return pred
            # 递归
            result = _scan_json_for_prediction(val, depth + 1)
            if result:
                return result
    elif isinstance(data, list):
        for item in data:
            result = _scan_json_for_prediction(item, depth + 1)
            if result:
                return result
    elif isinstance(data, str):
        if any(kw.lower() in data.lower() for kw in _PREDICTION_KEYWORDS):
            return _parse_prediction_text(data)
    return None


def _parse_prediction_text(text: str) -> PricePrediction | None:
    """从文本解析降价预测信息"""
    if not text or len(text) < 5:
        return None
    text = str(text).strip()

    predicted_price = None
    probability = None
    time_range = None

    m = _PREDICT_PRICE_RE.search(text)
    if m:
        predicted_price = int(m.group(1))

    m = _PREDICT_PROB_RE.search(text)
    if m:
        probability = int(m.group(1))

    m = _PREDICT_TIME_RE.search(text)
    if m:
        time_range = m.group(1)

    # 至少要有一个有效字段才算预测
    if predicted_price is None and probability is None:
        return None

    # 限制 raw_text 长度
    raw = text[:200] if len(text) > 200 else text
    # 清理多余空白
    raw = re.sub(r"\s+", " ", raw).strip()

    return PricePrediction(
        raw_text=raw,
        predicted_price=predicted_price,
        probability=probability,
        time_range=time_range,
    )


# ── 最低价 API（降级） ────────────────────────────────────────────────────

def _fetch_lowest_price(
    dep_city: str, arr_city: str, date: str,
    source_url: str = "",
) -> FlightResult | None:
    """降级: 直接请求 12808/lowestPrice API"""
    dep_code = _resolve_city_code(dep_city).upper()
    arr_code = _resolve_city_code(arr_city).upper()
    params = {
        "depCity": dep_code,
        "arrCity": arr_code,
        "flightType": 1,
        "depDate": date,
        "channel": "online",
    }
    headers = {"Referer": source_url or "https://flights.ctrip.com/online/channel/domestic"}
    try:
        resp = requests.get(CTRIP_REPO_LOWEST_PRICE_URL, params=params,
                            headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return None

    price_rows = (data.get("data") or {}).get("oneWayPrice") or []
    if not price_rows or not isinstance(price_rows[0], dict):
        return None
    day_key = date.replace("-", "")
    raw_price = price_rows[0].get(day_key)
    if raw_price in (None, ""):
        # 尝试 YYYY-MM-DD 格式
        raw_price = price_rows[0].get(date)
    if raw_price in (None, ""):
        return None
    try:
        price = int(round(float(raw_price)))
    except (TypeError, ValueError):
        return None

    ticket = FlightTicket(
        flight_numbers="LOWEST-PRICE",
        airlines="携程日历价",
        departure_time="--:--",
        arrival_time="--:--",
        departure_airport=dep_city,
        arrival_airport=arr_city,
        flight_type="日历最低价",
        total_duration="",
        price=price,
        discount="",
        labels=["日历最低价", "仅含日期价格，不含具体航班"],
        source="lowest_price",
    )
    return FlightResult(tickets=[ticket], prediction=None, source="lowest_price")


# ── 主入口 ────────────────────────────────────────────────────────────────

def fetch_flights(
    client: CtripClient,
    dep_city: str,
    arr_city: str,
    date: str,
) -> FlightResult:
    """抓取航班列表 + 降价预测，API降级链: batchSearch -> DOM -> 最低价API

    Args:
        client: 已启动的 CtripClient 实例
        dep_city: 出发城市名（如"成都"）
        arr_city: 到达城市名（如"伊宁"）
        date: 出发日期 YYYY-MM-DD

    Returns:
        FlightResult: 含航班列表 + 预测数据
    """
    if not client.page:
        raise RuntimeError("CtripClient 未启动，请先调用 client.start()")

    # 注入 API 拦截脚本
    client.context.add_init_script(FLIGHT_CAPTURE_JS)

    url = _build_flight_url(dep_city, arr_city, date)
    client.navigate(url)

    # 等待 batchSearch 响应
    payload = _wait_for_batch_search(client.page, timeout_ms=60000)

    # 等待页面稳定
    time.sleep(2)
    try:
        client.page.wait_for_load_state("networkidle", timeout=8000)
    except Exception:
        pass

    tickets: list[FlightTicket] = []
    source = "api"

    # 路1: batchSearch API 解析
    if payload and int(payload.get("status", -1)) == 0:
        tickets = _parse_itineraries(payload)

    # 路2: DOM 降级解析
    if not tickets:
        tickets = _extract_dom_tickets(client.page)
        if tickets:
            source = "dom"

    # 路3: 最低价 API 降级
    if not tickets:
        result = _fetch_lowest_price(dep_city, arr_city, date, source_url=url)
        if result:
            return result
        return FlightResult(tickets=[], prediction=None, source="empty")

    # 用 DOM 文本补充余票信息（API 可能未返回"仅剩X张"）
    try:
        body_text = client.page.evaluate("() => document.body.innerText") or ""
        for ticket in tickets:
            if ticket.remaining_seats is None:
                # 在页面文本中搜索该航班号附近的"仅剩X张"
                idx = body_text.find(ticket.flight_numbers)
                if idx >= 0:
                    snippet = body_text[max(0, idx - 50):idx + 200]
                    remaining = _parse_remaining_seats([], snippet)
                    if remaining is not None:
                        ticket.remaining_seats = remaining
                        if "仅剩" not in " ".join(ticket.labels):
                            ticket.labels.append(f"仅剩{remaining}张")
    except Exception:
        pass

    # 提取降价预测（扫描全部 API 响应 + DOM）
    all_responses = _get_all_api_responses(client.page)
    prediction = _extract_price_prediction(all_responses, client.page)

    # 合并代码共享航班
    tickets = merge_codeshares(tickets)

    return FlightResult(tickets=tickets, prediction=prediction, source=source)
