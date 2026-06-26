#!/usr/bin/env python3
"""
Ticket Price Search Script v6.2
Searches and compares flight and train ticket prices across major platforms.
Uses web scraping (Ctrip/Qunar) for real-time flight prices - NO API KEY NEEDED.
Uses 12306 public API for real-time train availability AND prices.
Optionally supports Firecrawl (JS rendering) for detailed flight data, Tequila/Amadeus API for users who already have keys.

Data Sources (no registration required):
  1. Ctrip/Qunar Web Scraping (primary, no API key needed):
     - Scrapes public flight search pages for price data
     - Works out of the box, no setup required

  2. 12306 Train Tickets (no API key needed):
     - Uses 12306 public leftTicket/query endpoint for availability
     - Uses 12306 public queryTicketPrice endpoint for prices
     - No login required for either endpoint

Optional API (for users who already have keys):
  3. Firecrawl API (if FIRECRAWL_API_KEY is set)
     - Renders JavaScript pages, gets detailed flight info from Ctrip PC page
     - PC page: individual flight numbers, times, aircraft types, prices
     - Mobile page: price calendar with daily lowest prices (fallback)
     - Register at https://firecrawl.dev
  4. Kiwi.com Tequila API (if TEQUILA_API_KEY is set)
     - Note: Registration may no longer be available
  5. Amadeus API (if AMADEUS_CLIENT_ID + AMADEUS_CLIENT_SECRET are set)
     - Note: Self-service registration is NO LONGER available

Usage:
  python ticket_search.py <departure> <arrival> <date> [flight|train|all]
  python ticket_search.py Beijing Shanghai 2026-05-01 flight
  python ticket_search.py Shanghai Tokyo 2026-06-15 all
"""

import json
import os
import re
import ssl
import urllib.parse
import urllib.request
import urllib.error
import sys
import time
from datetime import datetime, timedelta

# Fix Windows console encoding for CNY symbol (¥) and Chinese characters
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Try to import amadeus-python SDK (optional, for existing key holders)
try:
    from amadeus import Client as AmadeusClientSDK, ResponseError as AmadeusResponseError
    HAS_AMADEUS_SDK = True
except ImportError:
    HAS_AMADEUS_SDK = False

# SSL context for 12306: full verification always.
# 12306.cn may have certificate chain issues on some networks/systems,
# but we never bypass SSL verification — doing so exposes connections to
# MITM attacks. If SSL verification fails, the script returns an empty
# result with a helpful message. 12306 queries are public data (no
# credentials transmitted), so the impact is limited to unavailable
# train data; all other features (flight search, platform links) still work.
_ssl_ctx = ssl.create_default_context()  # Full TLS verification


def _urlopen_12306(req, timeout=15):
    """Open a URL to 12306 with full SSL verification.

    If SSL verification fails, raises the error with a helpful message.
    The caller should catch the exception and return empty results gracefully.
    """
    try:
        return urllib.request.urlopen(req, timeout=timeout, context=_ssl_ctx)
    except (ssl.SSLError, urllib.error.URLError) as e:
        is_ssl_error = isinstance(e, ssl.SSLError) or "CERTIFICATE" in str(e).upper() or "SSL" in str(e).upper()
        if is_ssl_error:
            print(f"[12306] SSL certificate verification failed: {e}", file=sys.stderr)
            print("[12306] Train data unavailable due to SSL error. "
                  "Try updating system CA certificates or using a different network. "
                  "Other features (flight search, platform links) still work.", file=sys.stderr)
        raise


# ============================================================
# IATA / Station Code Mappings
# ============================================================

CITY_IATA = {
    # Chinese cities
    "北京": "PEK", "上海": "PVG", "广州": "CAN", "深圳": "SZX", "成都": "CTU",
    "杭州": "HGH", "武汉": "WUH", "西安": "SIA", "重庆": "CKG", "南京": "NKG",
    "长沙": "CSX", "青岛": "TAO", "大连": "DLC", "厦门": "XMN", "昆明": "KMG",
    "哈尔滨": "HRB", "沈阳": "SHE", "天津": "TSN", "苏州": "SZV", "郑州": "CGO",
    "济南": "TNA", "福州": "FOC", "贵阳": "KWE", "兰州": "LHW", "太原": "TYN",
    "合肥": "HFE", "南宁": "NNG", "乌鲁木齐": "URC", "拉萨": "LXA", "海口": "HAK",
    "三亚": "SYX", "宁波": "NGB", "温州": "WNZ", "珠海": "ZUH", "东莞": "DGM",
    "佛山": "FUO", "无锡": "WUX", "常州": "CZX", "烟台": "YNT", "泉州": "JJN",
    # Common international (English)
    "Tokyo": "TYO", "Osaka": "OSA", "Seoul": "ICN", "Bangkok": "BKK",
    "Singapore": "SIN", "Kuala Lumpur": "KUL", "Taipei": "TPE", "Hong Kong": "HKG",
    "London": "LON", "Paris": "PAR", "Frankfurt": "FRA", "Amsterdam": "AMS",
    "New York": "NYC", "Los Angeles": "LAX", "San Francisco": "SFO",
    "Chicago": "ORD", "Sydney": "SYD", "Melbourne": "MEL", "Dubai": "DXB",
    "Delhi": "DEL", "Mumbai": "BOM",
    # Common international (Chinese)
    "纽约": "NYC", "洛杉矶": "LAX", "旧金山": "SFO", "芝加哥": "ORD",
    "悉尼": "SYD", "墨尔本": "MEL", "迪拜": "DXB",
    "东京": "TYO", "大阪": "OSA", "首尔": "ICN", "曼谷": "BKK",
    "新加坡": "SIN", "吉隆坡": "KUL", "台北": "TPE", "香港": "HKG",
    "伦敦": "LON", "巴黎": "PAR", "法兰克福": "FRA", "阿姆斯特丹": "AMS",
    "新德里": "DEL", "孟买": "BOM",
    # Airport codes as-is
    "PEK": "PEK", "PVG": "PVG", "CAN": "CAN", "SZX": "SZX", "CTU": "CTU",
    "HGH": "HGH", "NRT": "NRT", "HND": "HND", "ICN": "ICN", "GMP": "GMP",
    "JFK": "JFK", "LAX": "LAX", "SFO": "SFO", "LHR": "LHR", "CDG": "CDG",
    "BJS": "BJS", "SHA": "SHA",
}

# 12306 station telegraph codes (major cities)
STATION_CODES = {
    "北京": "BJP", "北京南": "VNP", "北京西": "BXP", "北京北": "VAP",
    "上海": "SHH", "上海虹桥": "AOH", "上海南": "SNH",
    "广州": "GZQ", "广州南": "IZQ", "广州东": "GGQ",
    "深圳": "SZQ", "深圳北": "CSQ",
    "成都": "CDW", "成都东": "ICW",
    "杭州": "HZH", "杭州东": "HGH",
    "武汉": "WHN", "汉口": "HKN",
    "西安": "XAY", "西安北": "EAY",
    "重庆": "CQW", "重庆北": "CUW",
    "南京": "NJH", "南京南": "NKH",
    "长沙": "CSQ", "长沙南": "CWQ",
    "青岛": "QDK",
    "大连": "DLT",
    "厦门": "XMS",
    "昆明": "KMM",
    "哈尔滨": "HBB", "哈尔滨西": "VAB",
    "沈阳": "SYT", "沈阳北": "SBT",
    "天津": "TJP", "天津西": "TXP",
    "郑州": "ZZF", "郑州东": "ZAF",
    "济南": "JNK", "济南西": "JGK",
    "福州": "FZS", "福州南": "FYS",
    "贵阳": "GIW",
    "兰州": "LZJ",
    "太原": "TYV",
    "合肥": "HFH", "合肥南": "ENH",
    "南宁": "NNZ", "南宁东": "NDZ",
    "拉萨": "LSO",
    "海口": "VUQ",
    "三亚": "SJQ",
    "宁波": "NGH",
    "石家庄": "SJP",
    "南昌": "NXG", "南昌西": "NXG",
    "长春": "CRT", "长春西": "CLT",
    "呼和浩特": "HHC",
    "乌鲁木齐": "WAR",
    "苏州": "SZH", "苏州北": "SZH",
    "无锡": "WXH", "无锡东": "WXH",
    "常州": "CZH",
    "烟台": "YTK",
    "温州": "RZH",
}


# ============================================================
# Platform Configuration
# ============================================================

FLIGHT_PLATFORMS = {
    "携程旅行": {
        "type": "domestic",
        "search_url": "https://flights.ctrip.com/online/list/oneway-{dep}-{arr}?depdate={date}",
        "intl_search_url": "https://flights.ctrip.com/online/list/international/oneway-{dep}-{arr}?depdate={date}",
        "note": "国内最大OTA，APP内可用AI助手TripGenie查票"
    },
    "去哪儿旅行": {
        "type": "domestic",
        "search_url": "https://flight.qunar.com/site/oneway_list.htm?searchDepartureAirport={dep}&searchArrivalAirport={arr}&searchDepartureTime={date}",
        "intl_search_url": "https://flight.qunar.com/site/international/oneway_list.htm?searchDepartureAirport={dep}&searchArrivalAirport={arr}&searchDepartureTime={date}",
        "note": "比价聚合平台，APP内可用AI助手小驼查票"
    },
    "飞猪旅行": {
        "type": "domestic",
        "search_url": "https://www.fliggy.com/flight/domestic-search?depCity={dep}&arrCity={arr}&depDate={date}",
        "intl_search_url": "https://www.fliggy.com/flight/international-search?depCity={dep}&arrCity={arr}&depDate={date}",
        "note": "阿里旗下"
    },
    "同程旅行": {
        "type": "domestic",
        "search_url": "https://www.ly.com/flights/itinerary/oneway/{dep}-{arr}?startdate={date}",
        "intl_search_url": "https://www.ly.com/flights/international/oneway/{dep}-{arr}?startdate={date}",
        "note": "微信小程序可查"
    },
    "途牛旅游": {
        "type": "domestic",
        "search_url": "https://flight.tuniu.com/{dep}-{arr}/{date}",
        "intl_search_url": "https://flight.tuniu.com/international/{dep}-{arr}/{date}",
        "note": "旅游套餐搭配"
    },
    "12306机票": {
        "type": "domestic",
        "search_url": "https://www.12306.cn/index/otn/ticketController?depCity={dep}&arrCity={arr}&depDate={date}",
        "note": "铁路官方APP内可购机票，退改有保障"
    },
    "Skyscanner天巡": {
        "type": "international",
        "search_url": "https://www.skyscanner.net/transport/flights/{dep}/{arr}/{date_nodash}",
        "note": "全球最大比价平台"
    },
    "Google Flights": {
        "type": "international",
        "search_url": "https://www.google.com/travel/flights?q=flights+from+{dep}+to+{arr}+on+{date}",
        "note": "日历视图看整月低价"
    },
    "Kayak客涯": {
        "type": "international",
        "search_url": "https://www.kayak.com/flights/{dep}-{arr}/{date_nodash}",
        "note": "价格预测功能"
    },
    "Momondo": {
        "type": "international",
        "search_url": "https://www.momondo.com/flight-search/{dep}-{arr}/{date_nodash}",
        "note": "常发现隐藏低价"
    },
    "Expedia": {
        "type": "international",
        "search_url": "https://www.expedia.com/Flights-search/{dep}-{arr}/{date_nodash}",
        "note": "套餐优惠力度大"
    },
    "Booking.com": {
        "type": "international",
        "search_url": "https://booking.com/flights/results/{dep}-{arr}/{date_nodash}",
        "note": "酒店+机票套餐"
    },
}

AIRLINE_OFFICIAL_SITES = {
    "中国国航": "https://www.airchina.com.cn",
    "东方航空": "https://www.ceair.com",
    "南方航空": "https://www.csair.com",
    "海南航空": "https://www.hnair.com",
    "春秋航空": "https://www.ch.com",
    "吉祥航空": "https://www.juneyaoair.com",
    "深圳航空": "https://www.shenzhenair.com",
    "厦门航空": "https://www.xiamenair.com",
    "四川航空": "https://www.sichuanair.com",
    "山东航空": "https://www.shandongair.com.cn",
    "新加坡航空": "https://www.singaporeair.com",
    "国泰航空": "https://www.cathaypacific.com",
    "大韩航空": "https://www.koreanair.com",
    "全日空ANA": "https://www.ana.co.jp",
    "日本航空JAL": "https://www.jal.com",
    "阿联酋航空": "https://www.emirates.com",
    "卡塔尔航空": "https://www.qatarairways.com",
    "土耳其航空": "https://www.turkishairlines.com",
    "汉莎航空": "https://www.lufthansa.com",
    "英国航空": "https://www.britishairways.com",
    "达美航空": "https://www.delta.com",
    "美联航": "https://www.united.com",
    "美国航空": "https://www.aa.com",
}

# ============================================================
# WeChat Mini Program Quick Links (微信小程序快捷入口)
# These generate URL Schemes that open the mini program directly in WeChat.
# Users can click the link on their phone (or scan QR) to search flights instantly.
# ============================================================
WECHAT_MINI_PROGRAMS = {
    "携程旅行机票": {
        "app_id": "wx5e73d1afdb3e3b0e",
        "page": "pages/flight/search/search",
        "note": "微信搜索「携程旅行」小程序 → 机票",
        "h5_url": "https://m.ctrip.com/html5/flight/swift/domestic/{dep}-{arr}?date={date}",
    },
    "飞猪旅行机票": {
        "app_id": "wx23d7bb5e6c0a7c3e",
        "page": "pages/flight/search/search",
        "note": "微信搜索「飞猪旅行」小程序 → 机票",
        "h5_url": "https://www.fliggy.com/flight/domestic-search?depCity={dep}&arrCity={arr}&depDate={date}",
    },
    "同程旅行机票": {
        "app_id": "wxe5f52902cf4de874",
        "page": "pages/flight/search/search",
        "note": "微信搜索「同程旅行」小程序 → 机票，支持微信支付",
        "h5_url": "https://www.ly.com/flights/itinerary/oneway/{dep}-{arr}?startdate={date}",
    },
    "去哪儿机票": {
        "app_id": "wx25231f9f6e8f5793",
        "page": "pages/flight/search/search",
        "note": "微信搜索「去哪儿旅行」小程序 → 机票",
        "h5_url": "https://flight.qunar.com/site/oneway_list.htm?searchDepartureAirport={dep}&searchArrivalAirport={arr}&searchDepartureTime={date}",
    },
    "航司官方小程序": {
        "app_id": "",
        "page": "",
        "note": "国航/东航/南航/春秋等均有微信小程序，支持在线值机",
        "h5_url": "",
        "airlines": [
            {"name": "中国国航", "search_tip": "微信搜索「中国国航」"},
            {"name": "东方航空", "search_tip": "微信搜索「东方航空」"},
            {"name": "南方航空", "search_tip": "微信搜索「南方航空」"},
            {"name": "海南航空", "search_tip": "微信搜索「海南航空」"},
            {"name": "春秋航空", "search_tip": "微信搜索「春秋航空」"},
            {"name": "吉祥航空", "search_tip": "微信搜索「吉祥航空」"},
        ],
    },
    "铁路12306机票": {
        "app_id": "wx8c0c6db73a1d94ad",
        "page": "",
        "note": "微信搜索「铁路12306」小程序 → 机票，官方渠道退改有保障",
        "h5_url": "https://www.12306.cn/index/",
    },
    "AI助手查票": {
        "app_id": "",
        "page": "",
        "note": "携程APP TripGenie / 去哪儿APP 小驼 — 用AI对话查航班价格",
        "h5_url": "",
        "ai_tips": [
            {"name": "携程 TripGenie", "search_tip": "打开携程APP → 点击AI助手 → 说「查北京到上海4月16日机票」"},
            {"name": "去哪儿 小驼", "search_tip": "打开去哪儿APP → 点击小驼 → 说「查北京到上海最便宜机票」"},
        ],
    },
}

TRAIN_PLATFORMS = {
    "12306官网": {
        "search_url": "https://www.12306.cn/index/otn/leftTicketDto/query?leftTicketDTO.train_date={date}&leftTicketDTO.from_station={dep}&leftTicketDTO.to_station={arr}&purpose_codes=ADULT",
        "note": "中国铁路官方售票平台"
    },
    "携程火车票": {
        "search_url": "https://trains.ctrip.com/webapp/train/list?ticketType=0&dStation={dep}&aStation={arr}&dDate={date}",
        "note": "可抢票"
    },
    "去哪儿火车票": {
        "search_url": "https://train.qunar.com/stationToStation.htm?fromStation={dep}&toStation={arr}&date={date}",
        "note": "智能中转推荐"
    },
    "飞猪火车票": {
        "search_url": "https://www.fliggy.com/train?depCityName={dep}&arrCityName={arr}&depDate={date}",
        "note": "有红包优惠"
    },
    "同程火车票": {
        "search_url": "https://www.ly.com/trains/{dep}-{arr}?date={date}",
        "note": "微信便捷"
    },
}

# Airline code to name mapping (major carriers)
CARRIER_NAMES = {
    "CA": "中国国航", "MU": "东方航空", "CZ": "南方航空", "HU": "海南航空",
    "9C": "春秋航空", "HO": "吉祥航空", "ZH": "深圳航空", "MF": "厦门航空",
    "3U": "四川航空", "SC": "山东航空", "FM": "上海航空", "GS": "天津航空",
    "PN": "西部航空", "G5": "华夏航空", "EU": "成都航空",
    "SQ": "新加坡航空", "CX": "国泰航空", "KE": "大韩航空", "NH": "全日空",
    "JL": "日本航空", "EK": "阿联酋航空", "QR": "卡塔尔航空", "TK": "土耳其航空",
    "LH": "汉莎航空", "BA": "英国航空", "DL": "达美航空", "UA": "美联航",
    "AA": "美国航空", "AF": "法国航空", "KL": "荷兰皇家", "QF": "澳洲航空",
    "NZ": "新西兰航空", "TG": "泰国航空", "MH": "马来西亚航空", "CI": "中华航空",
    "BR": "长荣航空", "OZ": "韩亚航空", "HX": "香港航空", "UO": "香港快运",
    "KA": "港龙航空", "5J": "宿务太平洋", "TR": "酷航", "3K": "捷星亚洲",
    "GK": "捷星日本", "BC": "Skymark", "MM": "Peach航空",
}


# ============================================================
# Ctrip Web Scraper (Primary Flight Price Source, NO API KEY)
# ============================================================

class CtripScraper:
    """Scrapes Ctrip (携程) public flight search pages for price data.
    No API key needed — works out of the box.
    """

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "https://flights.ctrip.com/",
        }

    def search_flights(self, dep_city: str, arr_city: str, date: str, is_international: bool = False) -> list:
        """Search flight prices from Ctrip public pages.

        Args:
            dep_city: Departure city name in Chinese (e.g., "北京") or IATA code
            arr_city: Arrival city name in Chinese or IATA code
            date: Departure date YYYY-MM-DD
            is_international: Whether this is an international route

        Returns:
            List of flight offer dicts
        """
        # Build search URL
        dep_iata = _get_iata(dep_city)
        arr_iata = _get_iata(arr_city)

        if is_international:
            url = f"https://flights.ctrip.com/online/list/international/oneway-{dep_iata}-{arr_iata}?depdate={date}"
        else:
            url = f"https://flights.ctrip.com/online/list/oneway-{dep_iata}-{arr_iata}?depdate={date}"

        req = urllib.request.Request(url)
        for k, v in self.headers.items():
            req.add_header(k, v)

        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
                return self._parse_html(html, dep_iata, arr_iata)
        except Exception as e:
            print(f"[携程] 网页请求失败: {e}", file=sys.stderr)
            return []

    def _parse_html(self, html: str, dep_iata: str, arr_iata: str) -> list:
        """Parse Ctrip HTML response for flight price data.

        Ctrip renders flight data via JavaScript (React/Next.js), so we look for
        the JSON data embedded in the page's script tags or window.__INITIAL_STATE__.
        """
        offers = []

        # Method 1: Try to extract from __NEXT_DATA__ or window.__INITIAL_STATE__
        json_data = None

        # Look for __NEXT_DATA__
        match = re.search(r'<script\s+id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
        if match:
            try:
                next_data = json.loads(match.group(1))
                # Navigate the structure to find flight data
                props = next_data.get("props", {}).get("pageProps", {})
                json_data = props.get("flightList") or props.get("data") or props.get("flightData")
            except (json.JSONDecodeError, KeyError):
                pass

        # Look for window.__INITIAL_STATE__
        if not json_data:
            match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', html, re.DOTALL)
            if match:
                try:
                    init_state = json.loads(match.group(1))
                    json_data = init_state.get("flightList") or init_state.get("data")
                except (json.JSONDecodeError, KeyError):
                    pass

        # Method 2: If JSON data found, parse it
        if json_data and isinstance(json_data, list):
            for item in json_data[:20]:
                try:
                    price = item.get("price", item.get("adultPrice", 0))
                    carrier = item.get("carrier", item.get("airlineName", ""))
                    flight_no = item.get("flightNo", item.get("flightNumber", ""))
                    dep_time = item.get("departTime", item.get("departureTime", ""))
                    arr_time = item.get("arriveTime", item.get("arrivalTime", ""))
                    duration = item.get("duration", item.get("flyTime", ""))
                    stops = item.get("stopCount", 0)
                    cabin = item.get("cabinClass", "")

                    if price:
                        offers.append({
                            "price": f"{price} CNY",
                            "price_float": float(price),
                            "currency": "CNY",
                            "carrier": carrier,
                            "flight_number": flight_no,
                            "departure_time": dep_time,
                            "arrival_time": arr_time,
                            "duration": duration,
                            "stops": stops,
                            "cabin": cabin,
                            "source": "携程网页",
                        })
                except (ValueError, TypeError):
                    continue

        # Method 3: Fallback - extract prices from HTML using regex
        if not offers:
            offers = self._extract_from_html_regex(html, dep_iata, arr_iata)

        offers.sort(key=lambda x: x.get("price_float", 99999))
        return offers

    def _extract_from_html_regex(self, html: str, dep_iata: str, arr_iata: str) -> list:
        """Fallback: Extract flight prices from HTML using regex patterns.

        This handles the case where Ctrip renders data server-side or in
        a format we can parse with regex.
        """
        offers = []

        # Common Ctrip price patterns
        # Pattern: "price":1234 or "price":"1234" or ¥1234
        price_patterns = [
            r'"price"\s*:\s*"?(\\d+)"?',
            r'"adultPrice"\s*:\s*"?(\\d+)"?',
            r'class="price"[^>]*>\\s*[¥￥]?\\s*(\\d+)',
            r'[¥￥]\\s*(\\d{2,6})\\s*</?(?:em|span|div)',
            r'"totalPrice"\s*:\s*(\\d+)',
        ]

        found_prices = set()
        for pattern in price_patterns:
            for m in re.finditer(pattern, html):
                try:
                    p = int(m.group(1))
                    if 50 < p < 50000:  # Reasonable flight price range in CNY
                        found_prices.add(p)
                except (ValueError, IndexError):
                    continue

        # Extract airline/flight info
        airline_pattern = r'"airlineName"\s*:\s*"([^"]+)"'
        flight_no_pattern = r'"flightNo"\s*:\s*"([^"]+)"'
        dep_time_pattern = r'"departTime"\s*:\s*"([^"]+)"'
        arr_time_pattern = r'"arriveTime"\s*:\s*"([^"]+)"'

        airlines = [m.group(1) for m in re.finditer(airline_pattern, html)]
        flight_nos = [m.group(1) for m in re.finditer(flight_no_pattern, html)]
        dep_times = [m.group(1) for m in re.finditer(dep_time_pattern, html)]
        arr_times = [m.group(1) for m in re.finditer(arr_time_pattern, html)]

        # Build offers from found data
        if found_prices:
            sorted_prices = sorted(found_prices)[:20]
            max_len = max(len(airlines), len(flight_nos), len(dep_times), len(arr_times), len(sorted_prices))

            for i, price in enumerate(sorted_prices):
                airline = airlines[i] if i < len(airlines) else ""
                fn = flight_nos[i] if i < len(flight_nos) else ""
                dt = dep_times[i] if i < len(dep_times) else ""
                at = arr_times[i] if i < len(arr_times) else ""

                offers.append({
                    "price": f"{price} CNY",
                    "price_float": float(price),
                    "currency": "CNY",
                    "carrier": airline,
                    "flight_number": fn,
                    "departure_time": dt,
                    "arrival_time": at,
                    "duration": "",
                    "stops": -1,  # Unknown
                    "cabin": "",
                    "source": "携程网页(解析)",
                })
        elif airlines or flight_nos:
            # We found flight info but no prices — still useful
            max_len = max(len(airlines), len(flight_nos), len(dep_times), len(arr_times))
            for i in range(min(max_len, 20)):
                offers.append({
                    "price": "查看详情",
                    "price_float": 99999,
                    "currency": "CNY",
                    "carrier": airlines[i] if i < len(airlines) else "",
                    "flight_number": flight_nos[i] if i < len(flight_nos) else "",
                    "departure_time": dep_times[i] if i < len(dep_times) else "",
                    "arrival_time": arr_times[i] if i < len(arr_times) else "",
                    "duration": "",
                    "stops": -1,
                    "cabin": "",
                    "source": "携程网页(部分数据)",
                })

        return offers


# ============================================================
# Firecrawl Scraper (JS-rendered page support, optional)
# ============================================================

class FirecrawlScraper:
    """Scrapes Ctrip flight pages via Firecrawl API (renders JavaScript).

    Supports two modes:
    1. PC flight list page (PRIMARY): Returns detailed flight info with flight numbers,
       times, aircraft types, and individual prices for each flight.
    2. Mobile H5 price calendar (FALLBACK): Returns daily lowest prices across dates.

    Requires FIRECRAWL_API_KEY environment variable.
    Falls back gracefully if not configured.
    """

    API_URL = "https://api.firecrawl.dev/v2/scrape"

    def __init__(self):
        self.api_key = os.environ.get("FIRECRAWL_API_KEY", "")
        self.is_configured = bool(self.api_key)

    def _call_api(self, url, mobile=True, wait_ms=15000):
        """Make a Firecrawl scrape API call and return markdown content."""
        payload = json.dumps({
            "url": url,
            "formats": ["markdown"],
            "onlyMainContent": True,
            "waitFor": wait_ms,
            "timeout": 30000,
            "mobile": mobile,
            "proxy": "basic",
            "blockAds": True,
            "storeInCache": True,
        }).encode("utf-8")

        req = urllib.request.Request(
            self.API_URL,
            data=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read().decode("utf-8"))

            if not result.get("success"):
                print(f"[Firecrawl] API returned unsuccessful response", file=sys.stderr)
                return ""

            data = result.get("data", {})
            return data.get("markdown", "")

        except urllib.error.HTTPError as e:
            body = ""
            try:
                body = e.read().decode("utf-8", errors="ignore")
            except Exception:
                pass
            print(f"[Firecrawl] HTTP error {e.code}: {body[:200]}", file=sys.stderr)
            return ""
        except Exception as e:
            print(f"[Firecrawl] Request failed: {e}", file=sys.stderr)
            return ""

    def search_flights(self, dep_city: str, arr_city: str, date: str, is_international: bool = False) -> list:
        """Search flight prices via Firecrawl.

        Tries PC flight list page first (detailed flight info), then falls back
        to mobile price calendar (daily lowest prices only).

        Args:
            dep_city: Departure city name or IATA code
            arr_city: Arrival city name or IATA code
            date: Departure date YYYY-MM-DD
            is_international: Whether this is an international route

        Returns:
            List of flight offer dicts
        """
        if not self.is_configured:
            return []

        dep_iata = _get_iata(dep_city)
        arr_iata = _get_iata(arr_city)

        # Primary: Try PC flight list page for detailed flight data
        offers = self.search_flights_detailed(dep_iata, arr_iata, date, is_international)
        if offers:
            return offers

        # Fallback: Try mobile H5 price calendar
        return self.search_price_calendar(dep_iata, arr_iata, date)

    def search_flights_detailed(self, dep_iata: str, arr_iata: str, date: str, is_international: bool = False) -> list:
        """Search detailed flight info via Ctrip PC page (Firecrawl renders JS).

        The PC page returns individual flight entries with:
        - Flight number (e.g., CA8357, MU5100)
        - Departure/arrival times
        - Airport and terminal info
        - Aircraft type
        - Individual price per flight
        - Cabin class and discount

        Args:
            dep_iata: Departure IATA code
            arr_iata: Arrival IATA code
            date: Departure date YYYY-MM-DD
            is_international: Whether this is an international route

        Returns:
            List of flight offer dicts with detailed info
        """
        # Ctrip PC flight search URL
        url = f"https://flights.ctrip.com/online/list/oneway-{dep_iata}-{arr_iata}?depdate={date}&cabin=y"

        print(f"[Firecrawl-PC] Scraping Ctrip PC flight list: {url}", file=sys.stderr)
        markdown = self._call_api(url, mobile=False, wait_ms=15000)

        if not markdown:
            return []

        offers = self._parse_flight_list(markdown, dep_iata, arr_iata, date)
        if offers:
            print(f"[Firecrawl-PC] Parsed {len(offers)} flights from Ctrip PC page", file=sys.stderr)
        else:
            print(f"[Firecrawl-PC] No flight data parsed from Ctrip PC page", file=sys.stderr)

        return offers

    def search_price_calendar(self, dep_iata: str, arr_iata: str, date: str) -> list:
        """Search via Ctrip mobile H5 price calendar (daily lowest prices only).

        The mobile page includes a price calendar showing daily lowest
        prices for 2+ months. Less detailed than PC but works as fallback.

        Args:
            dep_iata: Departure IATA code
            arr_iata: Arrival IATA code
            date: Departure date YYYY-MM-DD

        Returns:
            List of flight offer dicts (price calendar data)
        """
        url = f"https://m.ctrip.com/html5/flight/swift/domestic/{dep_iata}-{arr_iata}?date={date}"

        print(f"[Firecrawl-Mobile] Scraping Ctrip mobile price calendar: {url}", file=sys.stderr)
        markdown = self._call_api(url, mobile=True, wait_ms=10000)

        if not markdown:
            return []

        offers = self._parse_price_calendar(markdown, dep_iata, arr_iata, date)
        if offers:
            print(f"[Firecrawl-Mobile] Parsed price calendar data", file=sys.stderr)

        return offers

    def _parse_flight_list(self, markdown: str, dep_iata: str, arr_iata: str, target_date: str) -> list:
        """Parse Ctrip PC flight list page markdown into structured flight offers.

        The PC page markdown contains flight entries in this pattern:
            [airline logo image]
            Airline Name
            FLIGHT_NUMBER Aircraft_Type
            DEPARTURE_TIME
            Airport Terminal
            ARRIVAL_TIME
            Airport Terminal
            [promotions]
            ¥PRICE起
            Cabin_Class
            订票

        Returns:
            List of flight offer dicts with detailed information.
        """
        offers = []

        # Split markdown by airline logo markers (each flight starts with an airline logo)
        # The logo pattern: ![AirlineName](https://...airline/XX.png)
        # Split by this to get individual flight blocks
        flight_blocks = re.split(r'!\[.*?\]\(https://static\.tripcdn\.com/packages/flight/airline-logo/', markdown)

        for block in flight_blocks[1:]:  # Skip the first block (before any airline logo)
            try:
                offer = self._parse_single_flight(block)
                if offer and offer.get("price_float"):
                    offers.append(offer)
            except Exception:
                continue

        # If logo-based split didn't work well, try alternative parsing
        if len(offers) < 2:
            offers = self._parse_flight_list_alt(markdown, dep_iata, arr_iata, target_date)

        # Deduplicate by flight number
        seen = set()
        unique_offers = []
        for o in offers:
            fn = o.get("flight_number", "")
            key = f"{fn}_{o.get('departure_time', '')}_{o.get('price', '')}"
            if key not in seen and fn:
                seen.add(key)
                unique_offers.append(o)

        # Sort by price
        unique_offers.sort(key=lambda x: x.get("price_float", 99999))

        return unique_offers

    def _parse_single_flight(self, block: str) -> dict:
        """Parse a single flight block from Ctrip PC markdown.

        Block format (after airline logo split):
            XX.png)\n\nAirline Name\n\nFLIGHT_NUMBER Aircraft_Type\n\n...
        """
        # Extract airline name - first line after the logo
        lines = [l.strip() for l in block.split("\n") if l.strip()]

        if len(lines) < 5:
            return None

        # Airline name is typically the first meaningful line
        airline_name = ""
        flight_number = ""
        aircraft_type = ""
        dep_time = ""
        arr_time = ""
        dep_terminal = ""
        arr_terminal = ""
        price = 0
        cabin = ""
        stops = 0

        # Find flight number pattern: XX1234 or XX123 at start of line
        fn_pattern = re.compile(r'^([A-Z]{2}\d{3,4})\s*(.*)$')

        i = 0
        # Skip the logo line (XX.png))
        if lines[0].endswith('.png)'):
            i = 1

        # Airline name
        if i < len(lines) and not fn_pattern.match(lines[i]):
            airline_name = lines[i]
            i += 1

        # Flight number + aircraft type
        if i < len(lines):
            fn_match = fn_pattern.match(lines[i])
            if fn_match:
                flight_number = fn_match.group(1)
                aircraft_type = fn_match.group(2).strip()
                i += 1

        # Scan remaining lines for times, terminals, price
        time_pattern = re.compile(r'^(\d{1,2}:\d{2})$')
        terminal_pattern = re.compile(r'(国际机场|机场)(T\d)')
        price_pattern = re.compile(r'[¥￥]\s*(\d{2,6})')
        cabin_pattern = re.compile(r'(经济舱|公务舱|头等舱)')

        times_found = []
        terminals_found = []

        while i < len(lines):
            line = lines[i]

            # Time pattern
            t_match = time_pattern.match(line)
            if t_match:
                times_found.append(t_match.group(1))
                i += 1
                continue

            # Terminal pattern
            t2_match = terminal_pattern.search(line)
            if t2_match:
                terminals_found.append(t2_match.group(2))
                i += 1
                continue

            # Price pattern
            p_match = price_pattern.search(line)
            if p_match:
                try:
                    price = int(p_match.group(1))
                except ValueError:
                    pass
                i += 1
                continue

            # Cabin pattern
            c_match = cabin_pattern.search(line)
            if c_match:
                cabin = c_match.group(1)
                i += 1
                continue

            # Detect stops (中转)
            if '中转' in line or '转1次' in line:
                stops = 1
            elif '转2次' in line:
                stops = 2

            # "+1天" or "+2天" means next day arrival
            if '+1天' in line or '+2天' in line:
                arr_time = line.strip()  # Will be overridden if there's a time

            i += 1

        if len(times_found) >= 2:
            dep_time = times_found[0]
            arr_time = times_found[1]
        elif len(times_found) == 1:
            dep_time = times_found[0]

        # Must have at least flight number and price
        if not flight_number or not price:
            return None

        return {
            "price": f"{price} CNY",
            "price_float": float(price),
            "currency": "CNY",
            "carrier": airline_name,
            "flight_number": flight_number,
            "departure_time": dep_time,
            "arrival_time": arr_time,
            "duration": "",
            "stops": stops,
            "cabin": cabin,
            "aircraft": aircraft_type,
            "dep_terminal": terminals_found[0] if len(terminals_found) > 0 else "",
            "arr_terminal": terminals_found[1] if len(terminals_found) > 1 else "",
            "source": "Ctrip(Firecrawl-PC)",
        }

    def _parse_flight_list_alt(self, markdown: str, dep_iata: str, arr_iata: str, target_date: str) -> list:
        """Alternative parser for Ctrip PC flight list using regex on full markdown.

        Used when the logo-based split doesn't produce good results.
        Searches for flight_number + time + price patterns.
        """
        offers = []

        # Find all flight numbers
        flight_matches = list(re.finditer(
            r'([A-Z]{2}\d{3,4})\s*([^\n]*)',
            markdown
        ))

        for fm in flight_matches:
            flight_number = fm.group(1)
            aircraft_info = fm.group(2).strip()

            # Skip common false positives (like image URLs)
            if flight_number in ("MP4", "MP3", "JPEG", "GIF2", "PNG2"):
                continue

            # Look for surrounding context (200 chars before and after)
            start = max(0, fm.start() - 50)
            end = min(len(markdown), fm.end() + 300)
            context = markdown[start:end]

            # Extract times in context
            times = re.findall(r'\b(\d{1,2}:\d{2})\b', context)
            dep_time = times[0] if len(times) >= 1 else ""
            arr_time = times[1] if len(times) >= 2 else ""

            # Extract price in context (after flight number)
            after_fn = markdown[fm.end():fm.end() + 300]
            price_match = re.search(r'[¥￥]\s*(\d{2,6})', after_fn)
            price = 0
            if price_match:
                try:
                    price = int(price_match.group(1))
                except ValueError:
                    pass

            # Extract airline name - look backwards from flight number
            before_fn = markdown[max(0, fm.start() - 100):fm.start()]
            # Airline name is usually the last line before flight number
            airline_lines = [l.strip() for l in before_fn.split("\n") if l.strip()]
            airline_name = airline_lines[-1] if airline_lines else ""

            # Clean up airline name (remove markdown artifacts)
            airline_name = re.sub(r'[!\[\]()]', '', airline_name).strip()
            if len(airline_name) > 20 or len(airline_name) < 2:
                airline_name = ""

            # Extract cabin class
            cabin = ""
            cabin_match = re.search(r'(经济舱|公务舱|头等舱)', after_fn)
            if cabin_match:
                cabin = cabin_match.group(1)

            # Detect stops
            stops = 0
            if '中转' in after_fn or '转1次' in after_fn:
                stops = 1
            elif '转2次' in after_fn:
                stops = 2

            # Only add if we have at least a price
            if price >= 50:
                offers.append({
                    "price": f"{price} CNY",
                    "price_float": float(price),
                    "currency": "CNY",
                    "carrier": airline_name,
                    "flight_number": flight_number,
                    "departure_time": dep_time,
                    "arrival_time": arr_time,
                    "duration": "",
                    "stops": stops,
                    "cabin": cabin,
                    "aircraft": aircraft_info,
                    "source": "Ctrip(Firecrawl-PC)",
                })

        return offers

    def _parse_price_calendar(self, markdown: str, dep_iata: str, arr_iata: str, target_date: str) -> list:
        """Parse Ctrip mobile page price calendar from Firecrawl markdown output.

        The mobile H5 page includes a date selector with daily lowest prices.
        In markdown the pattern looks like:
            24\n¥500\n25\n¥380\n26\n¥360

        We extract prices for all visible dates and match against the target date.

        Returns:
            List with a single offer dict for the target date,
            plus optional nearby-date comparison data.
        """
        offers = []

        # Extract year-month headers and date-price pairs
        # Pattern: "2026年4月" or "2026年5月" followed by date-price data
        year_month_pattern = r'(\d{4})\u5e74(\d{1,2})\u6708'

        # Split markdown by year-month headers to know which month each price belongs to
        parts = re.split(year_month_pattern, markdown)
        # parts: [pre, year1, month1, content1, year2, month2, content2, ...]

        date_prices = {}  # "YYYY-MM-DD" -> price

        for i in range(1, len(parts) - 2, 3):
            year = parts[i]
            month = parts[i + 1].zfill(2)
            content = parts[i + 2]

            # Find day-price pairs: standalone number followed by ¥price
            # Handles various markdown spacing: "24\n¥500" or "24\n\n¥500"
            day_price_pairs = re.findall(
                r'(?:^|\n)\s*(\d{1,2})\s*\n\s*[¥￥]\s*(\d{2,6})',
                content
            )
            for day_str, price_str in day_price_pairs:
                day = day_str.zfill(2)
                date_key = f"{year}-{month}-{day}"
                try:
                    price = int(price_str)
                    if 50 < price < 50000:
                        date_prices[date_key] = price
                except (ValueError, IndexError):
                    continue

        # If no structured parsing worked, try a relaxed scan across the whole markdown
        if not date_prices:
            # Find all ¥price patterns and their preceding day number
            relaxed_pairs = re.findall(
                r'(\d{1,2})\s*\n+[¥￥]\s*(\d{2,6})',
                markdown
            )
            if relaxed_pairs:
                # Determine year/month from target_date
                target_year = target_date[:4]
                target_month = target_date[5:7]
                target_year_int = int(target_year)
                target_month_int = int(target_month)

                for day_str, price_str in relaxed_pairs:
                    day_int = int(day_str)
                    if 1 <= day_int <= 31:
                        try:
                            price = int(price_str)
                            if 50 < price < 50000:
                                day = day_str.zfill(2)
                                # Assume same month as target, or next month if day > 28 and target is end of month
                                date_key = f"{target_year}-{target_month}-{day}"
                                date_prices[date_key] = price
                                # Also add next month variant for small day numbers
                                if day_int <= 12:
                                    next_month_dt = datetime(target_year_int, target_month_int, 1) + timedelta(days=32)
                                    next_month_str = next_month_dt.strftime("%Y-%m")
                                    date_key2 = f"{next_month_str}-{day}"
                                    date_prices[date_key2] = price
                        except (ValueError, IndexError):
                            continue

        # Build offer for the target date
        target_price = date_prices.get(target_date)
        if target_price:
            offers.append({
                "price": f"{target_price} CNY",
                "price_float": float(target_price),
                "currency": "CNY",
                "carrier": "Ctrip lowest price",
                "flight_number": "",
                "departure_time": "",
                "arrival_time": "",
                "duration": "",
                "stops": -1,
                "cabin": "economy",
                "source": "Ctrip(Firecrawl price calendar)",
            })

        # Add nearby dates for price comparison (±3 days)
        if target_price:
            try:
                target_dt = datetime.strptime(target_date, "%Y-%m-%d")
                nearby = []
                for delta in range(-3, 4):
                    if delta == 0:
                        continue
                    nearby_dt = target_dt + timedelta(days=delta)
                    nearby_date = nearby_dt.strftime("%Y-%m-%d")
                    nearby_price = date_prices.get(nearby_date)
                    if nearby_price:
                        nearby.append({
                            "date": nearby_date,
                            "price": nearby_price,
                            "label": "cheaper" if nearby_price < target_price else "more expensive" if nearby_price > target_price else "same",
                        })
                # Sort by price and add top 3 cheapest as comparison info
                if nearby:
                    nearby.sort(key=lambda x: x["price"])
                    offers[0]["nearby_dates"] = nearby[:3]
                    cheaper = [n for n in nearby if n['label'] == 'cheaper']
                    if cheaper:
                        offers[0]["price_calendar_note"] = (
                            f"Price calendar from Ctrip mobile page. "
                            f"Nearby cheaper dates: " +
                            ", ".join(f"{n['date']} ¥{n['price']}" for n in cheaper[:3])
                        )
                    else:
                        offers[0]["price_calendar_note"] = (
                            f"Price calendar from Ctrip mobile page. {target_date} is already among the cheapest nearby dates."
                        )
            except (ValueError, IndexError):
                pass

        return offers


# ============================================================
# Kiwi.com Tequila API (Optional, for existing key holders)
# ============================================================

class TequilaClient:
    """Kiwi.com Tequila API client for flight search (optional).

    Note: Registration may no longer be available for new users.
    Only use this if you already have a TEQUILA_API_KEY.
    """

    BASE_URL = "https://api.tequila.kiwi.com"

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("TEQUILA_API_KEY", "")

    @property
    def is_configured(self):
        return bool(self.api_key)

    def search_flights(self, origin: str, destination: str, date: str, adults: int = 1) -> list:
        """Search for flight offers using Tequila Search API.

        Args:
            origin: IATA code (e.g., "PEK", "PVG")
            destination: IATA code (e.g., "SHA", "NRT")
            date: Departure date YYYY-MM-DD
            adults: Number of adult passengers

        Returns:
            List of flight offer dicts
        """
        params = urllib.parse.urlencode({
            "fly_from": origin,
            "fly_to": destination,
            "date_from": date,
            "date_to": date,
            "adults": adults,
            "curr": "CNY",
            "max_stopovers": 2,
            "limit": 30,
            "sort": "price",
        })
        url = f"{self.BASE_URL}/v2/search?{params}"

        req = urllib.request.Request(url)
        req.add_header("apikey", self.api_key)
        req.add_header("Accept", "application/json")

        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return self._parse_response(data)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore") if e.fp else ""
            if e.code == 429:
                print("[Tequila] API请求频率超限，请稍后重试", file=sys.stderr)
            elif e.code == 401:
                print("[Tequila] API Key无效或已过期，请检查 TEQUILA_API_KEY", file=sys.stderr)
            else:
                print(f"[Tequila] API请求失败 (HTTP {e.code}): {err_body}", file=sys.stderr)
            return []
        except Exception as e:
            print(f"[Tequila] 请求异常: {e}", file=sys.stderr)
            return []

    def _parse_response(self, data: dict) -> list:
        """Parse Tequila API response into structured flight offers."""
        offers = []
        for item in data.get("data", []):
            # Price info
            price = item.get("price", 0)
            currency = item.get("currency", "CNY")
            conversion_rate = item.get("conversion", {}).get("CNY", 1) if item.get("conversion") else 1

            # Route info
            city_from = item.get("cityFrom", "")
            city_to = item.get("cityTo", "")
            country_from = item.get("countryFrom", {}).get("code", "")
            country_to = item.get("countryTo", {}).get("code", "")

            # Build route segments
            route = item.get("route", [])
            segments = []
            for seg in route:
                carrier_code = seg.get("airline", "")
                carrier_name = CARRIER_NAMES.get(carrier_code, carrier_code)
                flight_no = seg.get("flight_no", "")
                dep_time = seg.get("local_departure", "")
                arr_time = seg.get("local_arrival", "")
                dep_airport = seg.get("flyFrom", "")
                arr_airport = seg.get("flyTo", "")
                segments.append({
                    "carrier": carrier_name,
                    "carrier_code": carrier_code,
                    "flight_number": f"{carrier_code}{flight_no}",
                    "departure": dep_time,
                    "arrival": arr_time,
                    "departure_airport": dep_airport,
                    "arrival_airport": arr_airport,
                    "aircraft": seg.get("equipment", ""),
                })

            # Duration
            duration_total = item.get("fly_duration", "")
            duration_minutes = item.get("duration", {}).get("total", 0)
            if duration_minutes and not duration_total:
                hours = duration_minutes // 60
                mins = duration_minutes % 60
                duration_total = f"{hours}h{mins:02d}m"

            # Stops
            stops = item.get("routes", [])
            num_stops = len(route) - 1 if route else 0

            # Deep link for booking
            deep_link = item.get("deep_link", "")

            # Parsed offer
            price_cny = price * conversion_rate if currency != "CNY" and conversion_rate else price
            offers.append({
                "price": f"{price_cny:.0f} CNY" if isinstance(price_cny, (int, float)) else f"{price} {currency}",
                "price_float": float(price_cny) if isinstance(price_cny, (int, float)) else float(price),
                "currency": "CNY",
                "city_from": city_from,
                "city_to": city_to,
                "country_from": country_from,
                "country_to": country_to,
                "duration": duration_total,
                "stops": num_stops,
                "segments": segments,
                "deep_link": deep_link,
                "booking_token": item.get("booking_token", ""),
                "source": "Kiwi Tequila",
            })

        offers.sort(key=lambda x: x["price_float"])
        return offers


# ============================================================
# Amadeus API Integration (Optional, for existing key holders)
# ============================================================

class AmadeusClient:
    """Amadeus for Developers API client (optional).

    Note: Self-service registration is NO LONGER available for new users.
    Only use this if you already have API keys.
    """

    BASE_URL = "https://test.api.amadeus.com"

    def __init__(self, client_id=None, client_secret=None):
        self.client_id = client_id or os.environ.get("AMADEUS_CLIENT_ID", "")
        self.client_secret = client_secret or os.environ.get("AMADEUS_CLIENT_SECRET", "")
        self._token = None
        self._token_expires = 0

    @property
    def is_configured(self):
        return bool(self.client_id and self.client_secret)

    def search_flights(self, origin: str, destination: str, date: str, adults: int = 1) -> list:
        """Search for flight offers using Amadeus Flight Offers Search API."""
        # Try SDK first
        if HAS_AMADEUS_SDK and self.is_configured:
            try:
                client = AmadeusClientSDK(
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                )
                response = client.shopping.flight_offers_search.get(
                    originLocationCode=origin,
                    destinationLocationCode=destination,
                    departureDate=date,
                    adults=adults,
                    currencyCode="CNY",
                    max=20,
                )
                return self._parse_sdk_response(response)
            except Exception as e:
                print(f"[Amadeus] SDK请求失败: {e}", file=sys.stderr)
                # Fall through to HTTP

        # HTTP fallback
        token = self._get_access_token()
        if not token:
            return []

        params = urllib.parse.urlencode({
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": date,
            "adults": adults,
            "currencyCode": "CNY",
            "max": 20,
        })
        url = f"{self.BASE_URL}/v2/shopping/flight-offers?{params}"

        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {token}")

        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return self._parse_http_response(data)
        except urllib.error.HTTPError as e:
            print(f"[Amadeus] API请求失败 (HTTP {e.code})", file=sys.stderr)
            return []
        except Exception as e:
            print(f"[Amadeus] 请求异常: {e}", file=sys.stderr)
            return []

    def _get_access_token(self):
        """Obtain OAuth2 access token from Amadeus."""
        if self._token and time.time() < self._token_expires:
            return self._token

        url = f"{self.BASE_URL}/v1/security/oauth2/token"
        data = urllib.parse.urlencode({
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }).encode("utf-8")

        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                self._token = result["access_token"]
                self._token_expires = time.time() + result.get("expires_in", 1800) - 60
                return self._token
        except Exception as e:
            print(f"[Amadeus] 获取token失败: {e}", file=sys.stderr)
            return None

    def _parse_sdk_response(self, response):
        """Parse amadeus-python SDK response."""
        offers = []
        for offer in response.data:
            price_info = offer.get("price", {})
            total = price_info.get("total", "N/A")
            currency = price_info.get("currency", "CNY")

            itineraries = []
            for itinerary in offer.get("itineraries", []):
                segments = []
                for seg in itinerary.get("segments", []):
                    cc = seg.get("carrierCode", "")
                    segments.append({
                        "carrier": CARRIER_NAMES.get(cc, cc),
                        "carrier_code": cc,
                        "flight_number": f"{cc}{seg.get('number', '')}",
                        "departure": seg.get("departure", {}).get("at", ""),
                        "arrival": seg.get("arrival", {}).get("at", ""),
                        "departure_airport": seg.get("departure", {}).get("iataCode", ""),
                        "arrival_airport": seg.get("arrival", {}).get("iataCode", ""),
                        "duration": seg.get("duration", ""),
                    })
                itineraries.append({"segments": segments, "duration": itinerary.get("duration", "")})

            fare_details = []
            for tp in offer.get("travelerPricings", []):
                for fd in tp.get("fareDetailsBySegment", []):
                    fare_details.append(fd.get("cabin", ""))
            cabin = fare_details[0] if fare_details else ""

            offers.append({
                "price": f"{total} {currency}",
                "price_float": float(total) if total != "N/A" else 99999,
                "currency": currency,
                "cabin": cabin,
                "itineraries": itineraries,
                "seats_available": offer.get("numberOfBookableSeats", ""),
                "source": "Amadeus SDK",
            })
        offers.sort(key=lambda x: x["price_float"])
        return offers

    def _parse_http_response(self, data):
        """Parse raw Amadeus HTTP response."""
        offers = []
        for offer in data.get("data", []):
            price_info = offer.get("price", {})
            total = price_info.get("total", "N/A")
            currency = price_info.get("currency", "CNY")

            itineraries = []
            for itinerary in offer.get("itineraries", []):
                segments = []
                for seg in itinerary.get("segments", []):
                    cc = seg.get("carrierCode", "")
                    segments.append({
                        "carrier": CARRIER_NAMES.get(cc, cc),
                        "carrier_code": cc,
                        "flight_number": f"{cc}{seg.get('number', '')}",
                        "departure": seg.get("departure", {}).get("at", ""),
                        "arrival": seg.get("arrival", {}).get("at", ""),
                        "departure_airport": seg.get("departure", {}).get("iataCode", ""),
                        "arrival_airport": seg.get("arrival", {}).get("iataCode", ""),
                        "duration": seg.get("duration", ""),
                    })
                itineraries.append({"segments": segments, "duration": itinerary.get("duration", "")})

            fare_details = []
            for tp in offer.get("travelerPricings", []):
                for fd in tp.get("fareDetailsBySegment", []):
                    fare_details.append(fd.get("cabin", ""))
            cabin = fare_details[0] if fare_details else ""

            offers.append({
                "price": f"{total} {currency}",
                "price_float": float(total) if total != "N/A" else 99999,
                "currency": currency,
                "cabin": cabin,
                "itineraries": itineraries,
                "seats_available": offer.get("numberOfBookableSeats", ""),
                "source": "Amadeus HTTP",
            })
        offers.sort(key=lambda x: x["price_float"])
        return offers


# ============================================================
# 12306 Train Ticket Query
# ============================================================

def query_12306_trains(dep_city: str, arr_city: str, date: str) -> list:
    """Query 12306 for real-time train ticket availability."""
    dep_code = STATION_CODES.get(dep_city)
    arr_code = STATION_CODES.get(arr_city)

    if not dep_code or not arr_code:
        print(f"[12306] 未找到站点代码: {dep_city}={dep_code}, {arr_city}={arr_code}", file=sys.stderr)
        return []

    url = (
        f"https://kyfw.12306.cn/otn/leftTicket/queryA?"
        f"leftTicketDTO.train_date={date}&"
        f"leftTicketDTO.from_station={dep_code}&"
        f"leftTicketDTO.to_station={arr_code}&"
        f"purpose_codes=ADULT"
    )

    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    req.add_header("Cookie", "_jc_save_fromStation=" + urllib.parse.quote(dep_city))
    req.add_header("Referer", "https://kyfw.12306.cn/otn/leftTicket/init")

    try:
        with _urlopen_12306(req, timeout=15) as resp:
            raw = resp.read()
            # 12306 sometimes returns UTF-8 BOM, html error pages, or normal JSON
            text = raw.decode("utf-8-sig").strip()
            if not text.startswith("{"):
                print(f"[12306] 非JSON响应（可能被反爬拦截）", file=sys.stderr)
                return []
            data = json.loads(text)
            if data.get("httpstatus") != 200:
                print(f"[12306] 查询失败: {data.get('messages', '未知错误')}", file=sys.stderr)
                return []
            trains = _parse_12306_data(data)
            # Fetch prices for each train
            if trains:
                _fetch_12306_prices(trains, dep_code, date)
            return trains
    except Exception as e:
        print(f"[12306] 查询异常: {e}", file=sys.stderr)
        return []


def _parse_12306_data(data: dict) -> list:
    """Parse 12306 API response into structured train info."""
    trains = []
    result = data.get("data", {}).get("result", [])
    station_map = data.get("data", {}).get("map", {})

    for item in result:
        parts = item.split("|")
        if len(parts) < 20:
            continue

        train_code = parts[3] if len(parts) > 3 else ""
        from_code = parts[6] if len(parts) > 6 else ""
        to_code = parts[7] if len(parts) > 7 else ""
        start_time = parts[8] if len(parts) > 8 else ""
        end_time = parts[9] if len(parts) > 9 else ""
        duration = parts[10] if len(parts) > 10 else ""

        from_station = station_map.get(from_code, from_code)
        to_station = station_map.get(to_code, to_code)

        seat_info = {}
        seat_mapping = [
            (17, "商务座/特等座"), (18, "动卧"), (19, "一等座/软座"),
            (20, "二等座/硬座"), (21, "软卧"), (22, "硬卧"),
            (23, "无座"), (24, "二等座"), (25, "一等座"),
        ]
        for idx, label in seat_mapping:
            if idx < len(parts):
                val = parts[idx].strip()
                if val and val != "--" and val != "无" and val != "*":
                    seat_info[label] = val

        if train_code.startswith("G"):
            train_type = "高铁"
        elif train_code.startswith("D"):
            train_type = "动车"
        elif train_code.startswith("C"):
            train_type = "城际"
        elif train_code.startswith("Z"):
            train_type = "直达"
        elif train_code.startswith("T"):
            train_type = "特快"
        elif train_code.startswith("K"):
            train_type = "快速"

            train_type = "其他"

        trains.append({
            "train_code": train_code,
            "train_type": train_type,
            "from_station": from_station,
            "to_station": to_station,
            "departure_time": start_time,
            "arrival_time": end_time,
            "duration": duration,
            "seats": seat_info,
            "prices": {},  # to be filled by _fetch_12306_prices
            # Internal fields for price query
            "_train_no": parts[2] if len(parts) > 2 else "",
            "_from_station_no": parts[16] if len(parts) > 16 else "",
            "_to_station_no": parts[17] if len(parts) > 17 else "",
            "_seat_types": parts[35] if len(parts) > 35 else (parts[11] if len(parts) > 11 else ""),
            "source": "12306",
        })

    return trains


def _fetch_12306_prices(trains: list, dep_code: str, date: str):
    """Fetch ticket prices for each train via 12306 queryTicketPrice API.

    The price API is publicly accessible (no login required) but needs
    train_no, from_station_no, to_station_no, and seat_types from the
    leftTicket query response.
    """
    if not trains:
        return

    # Price label mapping: API key -> display name
    price_key_map = {
        "A9": "商务座", "P": "特等座", "M": "一等座", "O": "二等座",
        "A6": "高级软卧", "A4": "软卧", "A3": "动卧", "A1": "硬卧",
        "A2": "软座", "A0": "硬座", "WZ": "无座",
    }

    print(f"[12306] 正在查询 {len(trains)} 趟列车的票价...", file=sys.stderr)

    for train in trains:
        train_no = train.get("_train_no", "")
        from_no = train.get("_from_station_no", "")
        to_no = train.get("_to_station_no", "")
        seat_types = train.get("_seat_types", "")

        if not train_no or not from_no or not to_no:
            continue

        url = (
            f"https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?"
            f"train_no={train_no}&from_station_no={from_no}"
            f"&to_station_no={to_no}&seat_types={seat_types}"
            f"&train_date={date}"
        )

        req = urllib.request.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        req.add_header("Cookie", "_jc_save_fromStation=" + urllib.parse.quote(dep_code))
        req.add_header("Referer", "https://kyfw.12306.cn/otn/leftTicket/init")

        try:
            with _urlopen_12306(req, timeout=10) as resp:
                raw = resp.read().decode("utf-8-sig").strip()
                if not raw.startswith("{"):
                    continue
                pdata = json.loads(raw)
                price_data = pdata.get("data", {})

                prices = {}
                for key, val in price_data.items():
                    if key in ("OT", "train_no") or not val or val == "--":
                        continue
                    label = price_key_map.get(key)
                    if not label:
                        # Skip unknown seat type codes (like "9" which is internal)
                        continue
                    try:
                        val_str = str(val).replace("¥", "").replace("￥", "").strip()
                        num = float(val_str)
                        # API returns prices in yuan (e.g., "¥662.0")
                        prices[label] = f"¥{num:.0f}"
                    except (ValueError, TypeError):
                        prices[label] = str(val)

                train["prices"] = prices
        except Exception:
            # Price query failed for this train, skip silently
            continue

    # Clean up internal fields
    for train in trains:
        train.pop("_train_no", None)
        train.pop("_from_station_no", None)
        train.pop("_to_station_no", None)
        train.pop("_seat_types", None)

    fetched = sum(1 for t in trains if t.get("prices"))
    print(f"[12306] 成功获取 {fetched}/{len(trains)} 趟列车的票价", file=sys.stderr)


# ============================================================
# Helper Functions
# ============================================================

def _detect_international(departure: str, arrival: str) -> bool:
    """Detect if the route is international."""
    domestic = [
        "北京", "上海", "广州", "深圳", "成都", "杭州", "武汉", "西安", "重庆", "南京",
        "长沙", "青岛", "大连", "厦门", "昆明", "哈尔滨", "沈阳", "天津", "苏州", "郑州",
        "济南", "福州", "贵阳", "兰州", "太原", "合肥", "南宁", "乌鲁木齐", "拉萨", "海口",
        "三亚", "宁波", "温州", "珠海", "东莞", "佛山", "无锡", "常州", "烟台", "泉州",
        "Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Chengdu", "Hangzhou", "Wuhan",
        "Xi'an", "Chongqing", "Nanjing", "PEK", "PVG", "CAN", "SZX", "CTU", "HGH"
    ]
    dep_d = any(kw.lower() in departure.lower() for kw in domestic)
    arr_d = any(kw.lower() in arrival.lower() for kw in domestic)
    return dep_d != arr_d or (not dep_d and not arr_d)


def _get_iata(city: str) -> str:
    """Get IATA code for a city name."""
    code = CITY_IATA.get(city)
    if code:
        return code
    # Fallback: if city is all ASCII (e.g., "NYC"), use upper()[:3]
    try:
        city.encode("ascii")
        return city.upper()[:3] if len(city) >= 3 else city.upper()
    except UnicodeEncodeError:
        # Non-ASCII city name (Chinese etc.) with no mapping —
        # URL-encode it so it can be used in URLs safely
        return urllib.parse.quote(city)


def generate_flight_links(departure, arrival, date, is_international):
    results = []
    date_nodash = date.replace("-", "")
    dep_iata = _get_iata(departure)
    arr_iata = _get_iata(arrival)

    for name, config in FLIGHT_PLATFORMS.items():
        is_intl = config["type"] == "international"
        if is_international and not is_intl and "intl_search_url" in config:
            tpl = config["intl_search_url"]
        else:
            tpl = config["search_url"]

        # Use IATA codes for international platforms, Chinese names for domestic
        dep_for_url = dep_iata if is_intl else urllib.parse.quote(departure)
        arr_for_url = arr_iata if is_intl else urllib.parse.quote(arrival)

        url = tpl.format(
            dep=dep_for_url,
            arr=arr_for_url,
            date=date, date_nodash=date_nodash
        )
        results.append({"platform": name, "url": url, "note": config["note"],
                         "category": "international" if is_intl else "domestic"})
    return results


def generate_wechat_links(departure, arrival, date, is_international):
    """Generate WeChat mini program quick links and mobile H5 links.

    Since we cannot directly invoke mini programs or AI chatbots from a desktop script,
    we provide:
    1. Mobile H5 links that work in phone browsers
    2. Instructions to search in WeChat mini programs
    3. Airline mini program search tips
    4. AI assistant usage tips (TripGenie, 小驼)
    """
    results = []
    for name, config in WECHAT_MINI_PROGRAMS.items():
        entry = {"name": name, "note": config["note"]}

        if config.get("h5_url") and "{" in config["h5_url"]:
            h5_url = config["h5_url"].format(
                dep=urllib.parse.quote(departure),
                arr=urllib.parse.quote(arrival),
                date=date,
            )
            entry["h5_url"] = h5_url
            entry["tip"] = f"手机浏览器打开，或微信内搜索小程序「{name.replace('机票', '')}」"
        elif config.get("h5_url"):
            entry["h5_url"] = config["h5_url"]
            entry["tip"] = f"微信搜索小程序「{name.replace('机票', '')}」"

        if config.get("airlines"):
            entry["airlines"] = config["airlines"]
            entry["tip"] = "打开微信 → 搜索对应航司小程序 → 查询航班"

        if config.get("ai_tips"):
            entry["ai_tips"] = config["ai_tips"]
            entry["tip"] = "打开对应APP → 使用AI助手对话查票"

        results.append(entry)
    return results


def generate_airline_links(departure, arrival, is_international):
    chinese = list(AIRLINE_OFFICIAL_SITES.items())[:10]
    items = AIRLINE_OFFICIAL_SITES.items() if is_international else chinese
    return [{"airline": n, "official_site": u,
             "search_tip": f"在官网搜索 {departure} → {arrival}"} for n, u in items]


def generate_train_links(departure, arrival, date):
    results = []
    for name, config in TRAIN_PLATFORMS.items():
        url = config["search_url"].format(
            dep=urllib.parse.quote(departure),
            arr=urllib.parse.quote(arrival), date=date
        )
        results.append({"platform": name, "url": url, "note": config["note"]})
    return results


# ============================================================
# Main Search & Formatting
# ============================================================

def search_tickets(departure, arrival, date, ticket_type="all"):
    is_international = _detect_international(departure, arrival)
    output = {
        "query": {"departure": departure, "arrival": arrival, "date": date, "is_international": is_international},
        "flight_offers": [],
        "train_offers": [],
        "flight_platforms": [],
        "airline_official_sites": [],
        "train_platforms": [],
        "search_tips": [],
        "api_status": {},
    }

    # --- Flights ---
    if ticket_type in ("flight", "all"):
        origin_iata = _get_iata(departure)
        dest_iata = _get_iata(arrival)
        flight_data_found = False

        # Primary: Ctrip web scraping (no API key needed)
        print(f"[携程] 正在查询 {departure}({origin_iata}) → {arrival}({dest_iata}) 的航班价格...", file=sys.stderr)
        ctrip = CtripScraper()
        ctrip_offers = ctrip.search_flights(departure, arrival, date, is_international)
        if ctrip_offers:
            output["flight_offers"] = ctrip_offers
            output["api_status"]["ctrip_scrape"] = "ok"
            flight_data_found = True
        else:
            output["api_status"]["ctrip_scrape"] = "no_results"

        # Fallback 1: Try Firecrawl (JS rendering, detailed PC flight list first)
        if not flight_data_found:
            firecrawl = FirecrawlScraper()
            if firecrawl.is_configured:
                print(f"[Firecrawl] 正在通过Firecrawl渲染查询 {origin_iata} → {dest_iata} 的航班详情...", file=sys.stderr)
                fc_offers = firecrawl.search_flights(departure, arrival, date, is_international)
                if fc_offers:
                    output["flight_offers"] = fc_offers
                    # Distinguish between PC detailed results and mobile price calendar
                    source = fc_offers[0].get("source", "")
                    if "PC" in source:
                        output["api_status"]["firecrawl_pc"] = "ok"
                    else:
                        output["api_status"]["firecrawl_mobile"] = "ok"
                    flight_data_found = True
                else:
                    output["api_status"]["firecrawl"] = "no_results"
            else:
                output["api_status"]["firecrawl"] = "not_configured"

        # Fallback 2: Try Tequila API (for existing key holders)
        if not flight_data_found:
            tequila = TequilaClient()
            if tequila.is_configured:
                print(f"[Tequila] 正在查询 {origin_iata} → {dest_iata} 的航班价格...", file=sys.stderr)
                offers = tequila.search_flights(origin_iata, dest_iata, date)
                if offers:
                    output["flight_offers"] = offers
                    output["api_status"]["tequila"] = "ok"
                    flight_data_found = True
                else:
                    output["api_status"]["tequila"] = "no_results"
            else:
                output["api_status"]["tequila"] = "not_configured"

        # Fallback 3: Try Amadeus API (for existing key holders)
        if not flight_data_found:
            amadeus = AmadeusClient()
            if amadeus.is_configured:
                print(f"[Amadeus] 正在查询 {origin_iata} → {dest_iata} 的航班价格...", file=sys.stderr)
                offers = amadeus.search_flights(origin_iata, dest_iata, date)
                if offers:
                    output["flight_offers"] = offers
                    output["api_status"]["amadeus"] = "ok"
                    flight_data_found = True
                else:
                    output["api_status"]["amadeus"] = "no_results"
            else:
                output["api_status"]["amadeus"] = "not_configured"

        # Tips for users without API keys
        if not flight_data_found:
            output["search_tips"].append(
                "提示: 实时航班价格暂无法获取，请点击下方平台链接手动查询最新价格"
            )

        output["flight_platforms"] = generate_flight_links(departure, arrival, date, is_international)
        output["airline_official_sites"] = generate_airline_links(departure, arrival, is_international)
        output["wechat_mini_programs"] = generate_wechat_links(departure, arrival, date, is_international)

    # --- Trains ---
    if ticket_type in ("train", "all"):
        if not is_international:
            print(f"[12306] 正在查询 {departure} → {arrival} 的火车票...", file=sys.stderr)
            trains = query_12306_trains(departure, arrival, date)
            output["train_offers"] = trains
            output["api_status"]["12306"] = "ok" if trains else "no_results"
            output["train_platforms"] = generate_train_links(departure, arrival, date)
        else:
            output["api_status"]["12306"] = "skipped_international"
            output["search_tips"].append("国际路线无火车票选项，如需欧洲铁路请查看 Eurail/Trainline")

    # Tips
    output["search_tips"].extend(_get_search_tips(is_international, ticket_type))
    return output


def _get_search_tips(is_international, ticket_type):
    tips = []
    if is_international:
        tips.extend([
            "国际机票建议：提前2-3个月购买通常更便宜",
            "建议使用 Skyscanner/Google Flights 比价后到航司官网购买，退改更方便",
            "注意：部分特价票可能需要中转，飞行时间较长",
            "转机签证：部分中转城市需要过境签证，请提前确认",
        ])
    else:
        tips.extend([
            "国内机票建议：提前1-2周购买通常较便宜",
            "周二/周三/周六出发通常比周末便宜",
            "廉航（春秋/吉祥）注意行李额，托运需额外付费",
        ])
    if ticket_type in ("train", "all") and not is_international:
        tips.extend([
            "火车票建议：12306为唯一官方渠道，开售时间通常为出发前15天",
            "候补购票：热门车票售罄后可使用12306候补功能",
        ])
    return tips


def format_output(data):
    lines = []
    q = data["query"]
    route_type = "国际" if q["is_international"] else "国内"

    lines.append(f"# {route_type}票价比价查询结果")
    lines.append(f"")
    lines.append(f"| 项目 | 信息 |")
    lines.append(f"|------|------|")
    lines.append(f"| 出发地 | {q['departure']} |")
    lines.append(f"| 目的地 | {q['arrival']} |")
    lines.append(f"| 出发日期 | {q['date']} |")
    lines.append(f"| 路线类型 | {route_type} |")
    lines.append(f"")

    # API Status
    api_status = data.get("api_status", {})
    if api_status:
        lines.append(f"## 数据源状态")
        lines.append(f"")
        for source, status in api_status.items():
            if status == "ok":
                lines.append(f"- **{source}**: 已获取实时数据")
            elif status == "no_results":
                lines.append(f"- **{source}**: 已查询，暂无结果")
            elif status == "not_configured":
                if source == "ctrip_scrape":
                    lines.append(f"- **{source}**: 网页爬取未获取数据")
                elif source in ("tequila", "amadeus"):
                    lines.append(f"- **{source}**: 未配置API密钥（该API已停止新用户注册）")
                elif source == "skyscanner":
                    lines.append(f"- **{source}**: 未配置")
                else:
                    lines.append(f"- **{source}**: 未配置")
            elif status == "skipped_international":
                lines.append(f"- **{source}**: 国际路线跳过")
            else:
                lines.append(f"- **{source}**: {status}")
        lines.append(f"")

    # Real-time flight offers
    if data.get("flight_offers"):
        source_name = data["flight_offers"][0].get("source", "API") if data["flight_offers"] else "API"
        lines.append(f"## 实时航班价格（来自{source_name}）")
        lines.append(f"")

        if source_name.startswith("携程网页"):
            # Ctrip scraping format
            lines.append(f"| 序号 | 航空公司 | 航班号 | 出发时间 | 到达时间 | 飞行时长 | 价格 |")
            lines.append(f"|------|----------|--------|----------|----------|----------|------|")
            for i, offer in enumerate(data["flight_offers"], 1):
                carrier = offer.get("carrier", "")
                fn = offer.get("flight_number", "")
                dep_time = offer.get("departure_time", "")
                arr_time = offer.get("arrival_time", "")
                dur = offer.get("duration", "")
                price = offer["price"]
                lines.append(f"| {i} | {carrier} | {fn} | {dep_time} | {arr_time} | {dur} | {price} |")
            lines.append(f"")

        elif source_name.startswith("Ctrip(Firecrawl-PC)"):
            # Firecrawl PC detailed flight list format
            lines.append(f"| 序号 | 航空公司 | 航班号 | 机型 | 出发时间 | 到达时间 | 舱位 | 中转 | 价格 |")
            lines.append(f"|------|----------|--------|------|----------|----------|------|------|------|")
            for i, offer in enumerate(data["flight_offers"], 1):
                carrier = offer.get("carrier", "")
                fn = offer.get("flight_number", "")
                aircraft = offer.get("aircraft", "")
                dep_time = offer.get("departure_time", "")
                arr_time = offer.get("arrival_time", "")
                cabin = offer.get("cabin", "")
                stops = "直飞" if offer.get("stops", 0) == 0 else f"{offer['stops']}次中转"
                price = offer["price"]
                lines.append(f"| {i} | {carrier} | {fn} | {aircraft} | {dep_time} | {arr_time} | {cabin} | {stops} | {price} |")
            lines.append(f"")
            lines.append(f"> 数据来源: 携程PC网页 (Firecrawl渲染)，包含航班号、起降时间、机型等详细信息")
            lines.append(f"")

        elif source_name.startswith("Ctrip(Firecrawl"):
            # Firecrawl mobile price calendar format (less detailed)
            lines.append(f"| 序号 | 描述 | 价格 |")
            lines.append(f"|------|------|------|")
            for i, offer in enumerate(data["flight_offers"], 1):
                carrier = offer.get("carrier", "")
                price = offer["price"]
                note = offer.get("price_calendar_note", "")
                lines.append(f"| {i} | {carrier} | {price} |")
                if note:
                    lines.append(f"| | {note} | |")
            if data["flight_offers"] and data["flight_offers"][0].get("nearby_dates"):
                lines.append(f"")
                lines.append(f"### 附近日期低价")
                lines.append(f"")
                lines.append(f"| 日期 | 价格 | 对比 |")
                lines.append(f"|------|------|------|")
                for nd in data["flight_offers"][0]["nearby_dates"]:
                    lines.append(f"| {nd['date']} | ¥{nd['price']} | {nd['label']} |")
            lines.append(f"")
            lines.append(f"> 数据来源: 携程移动端价格日历 (Firecrawl渲染)，仅显示每日最低价")
            lines.append(f"")

        elif source_name == "Kiwi Tequila":
            # Tequila format
            lines.append(f"| 序号 | 航空公司 | 航班号 | 出发 | 到达 | 飞行时长 | 中转 | 价格 | 预订 |")
            lines.append(f"|------|----------|--------|------|------|----------|------|------|------|")
            for i, offer in enumerate(data["flight_offers"], 1):
                seg = offer["segments"][0] if offer.get("segments") else {}
                carrier = seg.get("carrier", "")
                fn = seg.get("flight_number", "")
                dep_time = seg.get("departure", "")[11:16] if seg.get("departure") else ""
                arr_time = offer["segments"][-1].get("arrival", "")[11:16] if offer.get("segments") else ""
                dur = offer.get("duration", "")
                stops = offer.get("stops", 0)
                price = offer["price"]
                link = f"[预订]({offer['deep_link']})" if offer.get("deep_link") else ""
                lines.append(f"| {i} | {carrier} | {fn} | {dep_time} | {arr_time} | {dur} | {stops}次中转 | {price} | {link} |")
            lines.append(f"")

            # Multi-segment detail
            multi_seg = [o for o in data["flight_offers"] if o.get("stops", 0) > 0]
            if multi_seg:
                lines.append(f"### 中转航班详情")
                lines.append(f"")
                for i, offer in enumerate(multi_seg[:5], 1):
                    segs = offer.get("segments", [])
                    seg_details = " → ".join(
                        f"{s.get('departure_airport','')}({s.get('departure','')[11:16] if s.get('departure') else ''})"
                        for s in segs
                    )
                    lines.append(f"{i}. **{offer['price']}** {seg_details} ({offer.get('duration','')})")
                lines.append(f"")


        else:
            # Amadeus format
            lines.append(f"| 序号 | 航空公司 | 航班号 | 出发 | 到达 | 飞行时长 | 中转 | 舱位 | 价格 | 余座 |")
            lines.append(f"|------|----------|--------|------|------|----------|------|------|------|------|")
            for i, offer in enumerate(data["flight_offers"], 1):
                if offer.get("itineraries"):
                    itin = offer["itineraries"][0]
                    seg = itin["segments"][0] if itin["segments"] else {}
                    dep_time = seg.get("departure", "")[11:16] if seg.get("departure") else ""
                    arr_time = seg.get("arrival", "")[11:16] if seg.get("arrival") else ""
                    dur = itin.get("duration", "").replace("PT", "").replace("H", "h").replace("M", "m")
                    stops = len(itin["segments"]) - 1 if itin["segments"] else 0
                    carrier = seg.get("carrier", "")
                    fn = seg.get("flight_number", "")
                else:
                    dep_time = arr_time = dur = carrier = fn = ""
                    stops = 0
                cabin = offer.get("cabin", "")
                price = offer["price"]
                seats = offer.get("seats_available", "")
                lines.append(f"| {i} | {carrier} | {fn} | {dep_time} | {arr_time} | {dur} | {stops}次中转 | {cabin} | {price} | {seats} |")
            lines.append(f"")

        # Discount conditions for flight offers
        lines.append(f"## 航班优惠条件/限制")
        lines.append(f"")
        lines.append(f"| 条件类型 | 说明 |")
        lines.append(f"|----------|------|")
        lines.append(f"| 退改规则 | 特价票通常不可退改，具体以航司政策为准 |")
        lines.append(f"| 行李额度 | 经济舱通常含23kg托运行李；廉航可能仅含手提行李 |")
        lines.append(f"| 座位选择 | 特价舱位座位选择受限，可能需额外付费 |")
        lines.append(f"| 舱位限制 | 最低舱位票数量有限，售完即恢复原价 |")
        lines.append(f"| 中转风险 | 中转航班如遇延误，后续航班可能不保障 |")
        lines.append(f"| 支付方式 | 部分航司官网支持支付宝/微信，OTA支持更多方式 |")
        lines.append(f"")

    # Real-time train offers from 12306
    if data.get("train_offers"):
        # Check if any train has price data
        has_prices = any(t.get("prices") for t in data["train_offers"])

        lines.append(f"## 实时火车票信息（来自12306）")
        lines.append(f"")

        # Unified table with all info: schedule + price + seat availability
        lines.append(f"| 车次 | 类型 | 出发站→到达站 | 时间 | 历时 | 票价（余票） |")
        lines.append(f"|------|------|--------------|------|------|-------------|")
        for train in data["train_offers"]:
            route = f"{train['from_station']}→{train['to_station']}"
            time_range = f"{train['departure_time']}-{train['arrival_time']}"
            # Combine price and seat count into one column: "商务座¥830(12) / 一等座¥488(有)"
            if train.get("prices") and train.get("seats"):
                parts = []
                for seat_label, price in train["prices"].items():
                    seat_count = train["seats"].get(seat_label, "")
                    if seat_count:
                        parts.append(f"{seat_label}{price}({seat_count})")
                    else:
                        parts.append(f"{seat_label}{price}")
                price_seat_str = " / ".join(parts)
            elif train.get("prices"):
                price_seat_str = " / ".join(f"{k}{v}" for k, v in train["prices"].items())
            elif train.get("seats"):
                price_seat_str = " / ".join(f"{k}:{v}" for k, v in train["seats"].items()) + "（票价查询失败）"
            else:
                price_seat_str = "暂无"
            lines.append(f"| {train['train_code']} | {train['train_type']} | {route} | "
                         f"{time_range} | {train['duration']} | {price_seat_str} |")
        lines.append(f"")

        lines.append(f"## 火车票优惠条件")
        lines.append(f"")
        lines.append(f"| 条件类型 | 说明 |")
        lines.append(f"|----------|------|")
        lines.append(f"| 学生票 | 普通硬座5折，动车二等座7.5折（需在优惠区间内，每年4次） |")
        lines.append(f"| 儿童票 | 身高1.2-1.5m半价（需成人陪同） |")
        lines.append(f"| 改签规则 | 开车前可改签一次，开车后不可退票 |")
        lines.append(f"| 候补购票 | 售罄车次可候补，不保证成功 |")
        lines.append(f"")

    # Platform links (always shown)
    if data["flight_platforms"]:
        lines.append(f"## 机票比价平台链接")
        lines.append(f"")
        lines.append(f"| 平台 | 类型 | 链接 | 备注 |")
        lines.append(f"|------|------|------|------|")
        for p in data["flight_platforms"]:
            cat = "国内" if p["category"] == "domestic" else "国际"
            lines.append(f"| {p['platform']} | {cat} | [点击搜索]({p['url']}) | {p['note']} |")
        lines.append(f"")

    if data["airline_official_sites"]:
        lines.append(f"## 航空公司官网")
        lines.append(f"")
        lines.append(f"| 航空公司 | 官网 |")
        lines.append(f"|----------|------|")
        for a in data["airline_official_sites"]:
            lines.append(f"| {a['airline']} | [官网]({a['official_site']}) |")
        lines.append(f"")

    # WeChat Mini Program Quick Links
    if data.get("wechat_mini_programs"):
        lines.append(f"## 微信小程序 & AI助手快捷查询")
        lines.append(f"")
        lines.append(f"> 手机微信搜索小程序或使用AI助手，可快速查询和购买机票，支持微信支付")
        lines.append(f"")
        for wp in data["wechat_mini_programs"]:
            if wp.get("ai_tips"):
                lines.append(f"**{wp['name']}**")
                for ai in wp["ai_tips"]:
                    lines.append(f"- {ai['name']}: {ai['search_tip']}")
                lines.append(f"")
            elif wp.get("h5_url"):
                lines.append(f"**{wp['name']}**")
                lines.append(f"- 手机浏览器: [点击打开]({wp['h5_url']})")
                lines.append(f"- 微信小程序: {wp['note']}")
                lines.append(f"")
            elif wp.get("airlines"):
                lines.append(f"**{wp['name']}**")
                for airline in wp["airlines"]:
                    lines.append(f"- {airline['name']}: {airline['search_tip']}")
                lines.append(f"")
        lines.append(f"")

    if data["train_platforms"]:
        lines.append(f"## 火车票查询平台链接")
        lines.append(f"")
        lines.append(f"| 平台 | 链接 | 备注 |")
        lines.append(f"|------|------|------|")
        for t in data["train_platforms"]:
            lines.append(f"| {t['platform']} | [点击查询]({t['url']}) | {t['note']} |")
        lines.append(f"")

    # Tips
    if data["search_tips"]:
        lines.append(f"## 查询建议")
        lines.append(f"")
        for i, tip in enumerate(data["search_tips"], 1):
            lines.append(f"{i}. {tip}")
        lines.append(f"")

    return "\n".join(lines)


# ============================================================
# CLI Entry Point
# ============================================================

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python ticket_search.py <departure> <arrival> <date> [flight|train|all]")
        print("Examples:")
        print("  python ticket_search.py 北京 上海 2026-05-01 flight")
        print("  python ticket_search.py Shanghai Tokyo 2026-06-15 all")
        print("  python ticket_search.py 北京 广州 2026-05-10 train")
        print("")
        print("Environment Variables (optional, for existing API key holders):")
        print("  TEQUILA_API_KEY       - Kiwi Tequila API key (registration may be closed)")
        print("  AMADEUS_CLIENT_ID     - Amadeus API client ID (registration closed)")
        print("  AMADEUS_CLIENT_SECRET - Amadeus API client secret")
        print("")
        print("Note: Flight prices are primarily fetched via web scraping (no API key needed).")
        print("      API keys are optional fallbacks for users who already have them.")
        sys.exit(1)

    dep = sys.argv[1]
    arr = sys.argv[2]
    date = sys.argv[3]
    ticket_type = sys.argv[4] if len(sys.argv) > 4 else "all"

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print(f"Error: Invalid date format '{date}'. Please use YYYY-MM-DD format.")
        sys.exit(1)

    result = search_tickets(dep, arr, date, ticket_type)
    print(format_output(result))
