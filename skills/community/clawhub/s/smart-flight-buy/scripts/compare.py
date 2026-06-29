#!/usr/bin/env python3
"""
机票聪明买：多平台机票比价 + 低价日历 + 购票决策建议
通过SCF代理查询飞猪/途牛/RG实时机票价格

用法:
  python3 compare.py search --from "北京" --to "上海" --date 2026-07-01 [--trip-type one_way] [--cabin economy] [--adults 1]
  python3 compare.py compare --from "北京" --to "上海" --date 2026-07-01 --flight-no "CA1234" [--cabin economy]
  python3 compare.py calendar --from "北京" --to "上海" --start-date 2026-07-01 --days 14 [--cabin economy]
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta

# HTTP请求
try:
    from coze_workload_identity import requests as coze_requests
except ImportError:
    coze_requests = None

# ============================================================
# 配置
# ============================================================

PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")

# 代理地址
SCF_FLIGGY_URL = "https://1439498936-6sysdjjt99.ap-guangzhou.tencentscf.com"
SCF_TUNIU_URL = "https://1439498936-0junm3maxj.ap-guangzhou.tencentscf.com"
SCF_RG_URL = "https://1439498936-460a7b6oqn.ap-guangzhou.tencentscf.com"

HEADERS = {
    "Content-Type": "application/json",
    "X-Proxy-Token": PROXY_TOKEN,
}

# ============================================================
# 航线常识价格区间（经济舱单程，单位：元）
# 数据来源：行业公开数据 + 经验估算
# 格式：标准航线key → (低价, 均价, 高价)
# ============================================================

ROUTE_PRICE_REF = {
    # 北京出发
    "北京-上海": (350, 700, 1500),
    "北京-广州": (400, 800, 1800),
    "北京-深圳": (400, 850, 1800),
    "北京-成都": (350, 750, 1600),
    "北京-重庆": (350, 700, 1500),
    "北京-杭州": (300, 600, 1300),
    "北京-南京": (300, 550, 1200),
    "北京-武汉": (300, 600, 1300),
    "北京-长沙": (300, 600, 1300),
    "北京-西安": (300, 600, 1400),
    "北京-昆明": (400, 850, 1800),
    "北京-三亚": (500, 1100, 2500),
    "北京-厦门": (350, 700, 1600),
    "北京-大连": (250, 500, 1100),
    "北京-青岛": (250, 500, 1100),
    "北京-哈尔滨": (300, 650, 1400),
    # 上海出发
    "上海-广州": (350, 700, 1500),
    "上海-深圳": (350, 700, 1500),
    "上海-成都": (350, 750, 1600),
    "上海-重庆": (350, 700, 1500),
    "上海-武汉": (250, 500, 1100),
    "上海-长沙": (250, 550, 1200),
    "上海-西安": (300, 650, 1400),
    "上海-昆明": (400, 850, 1800),
    "上海-三亚": (450, 1000, 2200),
    "上海-厦门": (250, 500, 1100),
    "上海-青岛": (250, 500, 1100),
    "上海-大连": (250, 550, 1200),
    "上海-哈尔滨": (350, 750, 1600),
    # 广州/深圳出发
    "广州-成都": (300, 650, 1400),
    "广州-重庆": (300, 600, 1300),
    "广州-杭州": (250, 550, 1200),
    "广州-武汉": (250, 500, 1100),
    "广州-昆明": (300, 700, 1500),
    "深圳-成都": (300, 650, 1400),
    "深圳-杭州": (250, 550, 1200),
    "深圳-重庆": (300, 600, 1300),
    # 西南出发
    "成都-昆明": (200, 450, 1000),
    "成都-重庆": (150, 350, 800),
    "成都-西安": (250, 550, 1200),
    "成都-武汉": (250, 550, 1200),
    "重庆-昆明": (200, 450, 1000),
    "重庆-西安": (250, 550, 1200),
    # 其他热门
    "杭州-厦门": (200, 400, 900),
    "杭州-深圳": (250, 550, 1200),
    "武汉-三亚": (350, 750, 1600),
    "西安-昆明": (250, 550, 1200),
}

# 节假日/旺季日期（2026年）
PEAK_DATES = {
    "春运": ("2026-01-25", "2026-02-22"),
    "清明": ("2026-04-03", "2026-04-06"),
    "五一": ("2026-05-01", "2026-05-05"),
    "端午": ("2026-05-30", "2026-06-01"),
    "暑假": ("2026-07-01", "2026-08-31"),
    "中秋": ("2026-09-25", "2026-09-27"),
    "国庆": ("2026-10-01", "2026-10-07"),
    "寒假": ("2026-01-15", "2026-02-22"),
}

# 城市三字码映射（常见城市）
CITY_CODES = {
    "北京": "BJS", "上海": "SHA", "广州": "CAN", "深圳": "SZX",
    "成都": "CTU", "重庆": "CKG", "杭州": "HGH", "南京": "NKG",
    "武汉": "WUH", "长沙": "CSX", "西安": "SIA", "昆明": "KMG",
    "三亚": "SYX", "厦门": "XMN", "大连": "DLC", "青岛": "TAO",
    "哈尔滨": "HRB", "天津": "TSN", "郑州": "CGO", "福州": "FOC",
    "济南": "TNA", "沈阳": "SHE", "长春": "CGQ", "贵阳": "KWE",
    "兰州": "LHW", "乌鲁木齐": "URC", "拉萨": "LXA", "海口": "HAK",
    "宁波": "NGB", "合肥": "HFE", "南昌": "KHN", "太原": "TYN",
}


def get_route_key(from_city, to_city):
    """生成标准航线key"""
    return f"{from_city}-{to_city}"


def get_route_price_range(from_city, to_city):
    """获取航线常识价格区间"""
    key = get_route_key(from_city, to_city)
    if key in ROUTE_PRICE_REF:
        return ROUTE_PRICE_REF[key]
    # 反向查
    rev_key = get_route_key(to_city, from_city)
    if rev_key in ROUTE_PRICE_REF:
        return ROUTE_PRICE_REF[rev_key]
    return None


def is_peak_season(date_str):
    """判断是否旺季"""
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        for name, (start, end) in PEAK_DATES.items():
            if datetime.strptime(start, "%Y-%m-%d") <= d <= datetime.strptime(end, "%Y-%m-%d"):
                return True, name
    except ValueError:
        pass
    return False, None


def get_weekday_weight(date_str):
    """星期几权重：周二/三最便宜，周五/日最贵"""
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        wd = d.weekday()  # 0=Mon
        # 经验数据：周二周三比周末便宜15-18%
        weights = {0: 0.95, 1: 0.88, 2: 0.88, 3: 0.92, 4: 1.05, 5: 1.12, 6: 1.08}
        return weights.get(wd, 1.0)
    except ValueError:
        return 1.0


# ============================================================
# 购票决策引擎
# ============================================================

def buy_or_wait(price, from_city, to_city, dep_date, all_prices=None):
    """
    购票决策建议引擎
    返回: {signal, confidence, reasons[], tip}
    signal: "buy" / "wait" / "watch"
    """
    reasons = []
    signal_scores = []  # 正数=建议买，负数=建议等

    # 1. 航线常识价格分位
    price_range = get_route_price_range(from_city, to_city)
    if price_range:
        low, avg, high = price_range
        percentile = (price - low) / (high - low) if high > low else 0.5
        percentile = max(0, min(1, percentile))

        if percentile <= 0.25:
            reasons.append(f"当前价¥{price}处于该航线低价区间（约{int(percentile*100)}%分位），明显划算")
            signal_scores.append(3)
        elif percentile <= 0.5:
            reasons.append(f"当前价¥{price}低于该航线均价¥{avg}（约{int(percentile*100)}%分位），价格合理")
            signal_scores.append(2)
        elif percentile <= 0.75:
            reasons.append(f"当前价¥{price}接近该航线均价¥{avg}（约{int(percentile*100)}%分位），中等水平")
            signal_scores.append(0)
        else:
            reasons.append(f"当前价¥{price}高于该航线均价¥{avg}（约{int(percentile*100)}%分位），偏贵")
            signal_scores.append(-2)
    else:
        reasons.append(f"该航线暂无参考价格区间，无法判断价格高低")
        signal_scores.append(0)

    # 2. 距出发天数风险
    try:
        dep_dt = datetime.strptime(dep_date, "%Y-%m-%d")
        days_left = (dep_dt - datetime.now()).days

        if days_left < 3:
            reasons.append(f"距出发仅{days_left}天，国内航线临期价格通常暴涨，强烈建议立即购买")
            signal_scores.append(5)
        elif days_left < 7:
            reasons.append(f"距出发{days_left}天，已进入涨价期，越等越贵")
            signal_scores.append(3)
        elif days_left <= 14:
            reasons.append(f"距出发{days_left}天，处于国内航线黄金窗口(15-25天)，价格一般较优")
            signal_scores.append(1)
        elif days_left <= 30:
            reasons.append(f"距出发{days_left}天，处于提前购买优惠期，可以继续观望")
            signal_scores.append(-1)
        elif days_left <= 60:
            reasons.append(f"距出发{days_left}天，提前量大，价格波动空间大，建议设提醒观望")
            signal_scores.append(-2)
        else:
            reasons.append(f"距出发{days_left}天，时间尚早，航司尚未放出低价舱位，建议出发前30-45天再查")
            signal_scores.append(-1)
    except ValueError:
        pass

    # 3. 旺季特殊判断
    is_peak, peak_name = is_peak_season(dep_date)
    if is_peak:
        reasons.append(f"出发日处于{peak_name}旺季，越早买越便宜，不建议等")
        signal_scores.append(3)

    # 4. 多源价差分析
    if all_prices and len(all_prices) >= 2:
        valid_prices = [p for p in all_prices if p and p > 0]
        if len(valid_prices) >= 2:
            min_p = min(valid_prices)
            max_p = max(valid_prices)
            spread = (max_p - min_p) / min_p * 100 if min_p > 0 else 0

            if spread > 20:
                reasons.append(f"多平台价差{spread:.0f}%，最低¥{min_p} vs 最高¥{max_p}，价差较大，最低价可能不会持续太久")
                signal_scores.append(2)
            elif spread > 10:
                reasons.append(f"多平台价差{spread:.0f}%，最低¥{min_p} vs 最高¥{max_p}，有一定价差")
                signal_scores.append(1)
            else:
                reasons.append(f"多平台价差仅{spread:.0f}%，价格趋于一致")
                signal_scores.append(0)

    # 5. 星期效应
    wd_weight = get_weekday_weight(dep_date)
    try:
        dep_dt = datetime.strptime(dep_date, "%Y-%m-%d")
        weekdays_cn = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        wd_name = weekdays_cn[dep_dt.weekday()]
        if wd_weight <= 0.9:
            reasons.append(f"出发日{wd_name}，属于低价出行日，价格通常比周末便宜")
            signal_scores.append(1)
        elif wd_weight >= 1.05:
            reasons.append(f"出发日{wd_name}，属于高价出行日，价格通常比工作日贵")
            signal_scores.append(-1)
    except ValueError:
        pass

    # 综合判断
    total_score = sum(signal_scores)

    if total_score >= 3:
        signal = "buy"
        signal_emoji = "🟢"
        signal_text = "建议现在购买"
    elif total_score >= 1:
        signal = "buy"
        signal_emoji = "🟢"
        signal_text = "倾向于购买"
    elif total_score <= -3:
        signal = "wait"
        signal_emoji = "🔴"
        signal_text = "建议继续观望"
    elif total_score <= -1:
        signal = "watch"
        signal_emoji = "🟡"
        signal_text = "可以再等等"
    else:
        signal = "watch"
        signal_emoji = "🟡"
        signal_text = "观望为主，逢低入手"

    # 生成tip
    tips = []
    if is_peak:
        tips.append("旺季出行，提前购买是最佳策略")
    try:
        if days_left and days_left < 14:
            tips.append("国内航线提前15-25天通常最便宜，临近出发大概率涨价")
        elif days_left and days_left > 45:
            tips.append("距出发较远，建议出发前30-45天再查价格")
    except:
        pass

    if price_range and price > price_range[1]:
        tips.append("当前价格偏贵，如果不是刚需出行，考虑换日期或邻近机场")

    return {
        "signal": signal,
        "signal_emoji": signal_emoji,
        "signal_text": signal_text,
        "confidence": min(abs(total_score) / 8, 1.0),
        "reasons": reasons,
        "tips": tips,
        "price_percentile": int(percentile * 100) if price_range and price_range else None,
        "route_price_range": {"low": price_range[0], "avg": price_range[1], "high": price_range[2]} if price_range else None,
    }


# ============================================================
# HTTP请求
# ============================================================

def http_post(url, body, timeout=25):
    if coze_requests is not None:
        resp = coze_requests.post(url, json=body, headers=HEADERS, timeout=timeout, verify=True)
        return resp.json()
    else:
        import urllib.request
        import urllib.error
        import ssl
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
        ctx = ssl.create_default_context()
        ctx.check_hostname = True
        ctx.verify_mode = ssl.CERT_REQUIRED
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return json.loads(resp.read().decode("utf-8"))


# ============================================================
# 数据源查询
# ============================================================

def search_fliggy_flights(from_city, to_city, dep_date, journey_type=1, cabin_class=None, adult_count=1):
    """飞猪机票搜索"""
    try:
        params = {
            "origin": from_city,
            "destination": to_city,
            "depDate": dep_date,
            "journeyType": journey_type,
            "adultCount": adult_count,
        }
        if cabin_class:
            params["cabinClass"] = cabin_class

        resp = http_post(SCF_FLIGGY_URL, {
            "type": "search_flight",
            "params": params,
        })

        data = resp.get("data", {})
        items = data.get("itemList", [])

        flights = []
        for item in items:
            journeys = item.get("journeys", [])
            if not journeys:
                continue
            journey = journeys[0]
            segments = journey.get("segments", [])
            if not segments:
                continue

            seg = segments[0]
            price_str = item.get("ticketPrice", "0")
            try:
                price = float(price_str)
            except (ValueError, TypeError):
                price = 0

            airline_name = seg.get("marketingTransportName", "")
            # 航司名清洗：含"|"分隔符时取最后一段
            if "|" in airline_name:
                airline_name = airline_name.split("|")[-1]

            flight = {
                "source": "飞猪",
                "flight_no": seg.get("marketingTransportNo", ""),
                "airline": airline_name,
                "price": price,
                "dep_time": seg.get("depDateTime", "")[11:16] if seg.get("depDateTime") else "",
                "arr_time": seg.get("arrDateTime", "")[11:16] if seg.get("arrDateTime") else "",
                "dep_airport": seg.get("depStationShortName", seg.get("depStationName", "")),
                "arr_airport": seg.get("arrStationShortName", seg.get("arrStationName", "")),
                "duration": journey.get("totalDuration", ""),
                "journey_type": journey.get("journeyType", ""),
                "url": item.get("jumpUrl", ""),
                "cabin": seg.get("seatClassName", "经济舱"),
            }
            flights.append(flight)

        return {"source": "飞猪", "flights": flights, "error": None}
    except Exception as e:
        return {"source": "飞猪", "flights": [], "error": str(e)}


def search_tuniu_flights(from_city, to_city, dep_date):
    """途牛机票搜索"""
    try:
        resp = http_post(SCF_TUNIU_URL, {
            "type": "tuniu_flight_search",
            "params": {
                "departureCityName": from_city,
                "arrivalCityName": to_city,
                "departureDate": dep_date,
            },
        })

        data = resp.get("data", {})
        if isinstance(data, dict) and data.get("error"):
            return {"source": "途牛", "flights": [], "error": data["error"]}

        flight_list = data.get("data", []) if isinstance(data, dict) else data
        if not isinstance(flight_list, list):
            flight_list = []

        flights = []
        for f in flight_list:
            try:
                price = float(f.get("basePrice", 0))
            except (ValueError, TypeError):
                price = 0

            dep_time_full = f.get("departureTime", "")
            arr_time_full = f.get("arrivalTime", "")

            # 途牛时间格式 "2026-07-01 20:50" 或 "20:50"
            dep_time = ""
            arr_time = ""
            if dep_time_full:
                if " " in dep_time_full:
                    dep_time = dep_time_full.split(" ")[-1][:5]
                else:
                    dep_time = dep_time_full[:5]
            if arr_time_full:
                if " " in arr_time_full:
                    arr_time = arr_time_full.split(" ")[-1][:5]
                else:
                    arr_time = arr_time_full[:5]

            flight = {
                "source": "途牛",
                "flight_no": f.get("flightNumber", ""),
                "airline": f.get("airlineCompany", ""),
                "price": price,
                "dep_time": dep_time,
                "arr_time": arr_time,
                "dep_airport": f.get("departureAirport", ""),
                "arr_airport": f.get("arrivalAirport", ""),
                "duration": f.get("totalDuration", f.get("flyTime", "")),
                "journey_type": f.get("type", ""),
                "remaining_seats": f.get("remainingSeats", ""),
                "cabin": f.get("cabinClass", "经济舱"),
            }
            flights.append(flight)

        return {"source": "途牛", "flights": flights, "error": None}
    except Exception as e:
        return {"source": "途牛", "flights": [], "error": str(e)}


def search_rg_flights(from_city, to_city, dep_date):
    """RG机票搜索（备用，API可能不稳定）"""
    try:
        from_code = CITY_CODES.get(from_city, from_city)
        to_code = CITY_CODES.get(to_city, to_city)

        resp = http_post(SCF_RG_URL, {
            "type": "flight",
            "params": {
                "from_city": from_code,
                "to_city": to_code,
                "from_date": dep_date,
                "trip_type": "ONE_WAY",
                "adult_number": 1,
                "cabin_grade": "ECONOMY",
            },
        })

        data = resp.get("data", {})
        flight_list = data.get("flightInformationList", [])

        if not flight_list:
            return {"source": "RG", "flights": [], "error": "无结果（API可能暂时不可用）"}

        flights = []
        for f in flight_list:
            try:
                price = float(f.get("price", 0))
            except (ValueError, TypeError):
                price = 0

            flight = {
                "source": "RG",
                "flight_no": f.get("flightNo", ""),
                "airline": f.get("airline", ""),
                "price": price,
                "dep_time": f.get("departureTime", ""),
                "arr_time": f.get("arrivalTime", ""),
                "dep_airport": f.get("departureAirport", ""),
                "arr_airport": f.get("arrivalAirport", ""),
                "duration": f.get("duration", ""),
                "url": f.get("bookingUrl", ""),
                "cabin": "经济舱",
            }
            flights.append(flight)

        return {"source": "RG", "flights": flights, "error": None}
    except Exception as e:
        return {"source": "RG", "flights": [], "error": str(e)}


# ============================================================
# 航班跨平台匹配
# ============================================================

def match_flight_cross_platform(flight_no, candidates):
    """按航班号匹配跨平台航班"""
    if not flight_no:
        return []
    fn = flight_no.strip().upper()
    matched = []
    for c in candidates:
        c_fn = c.get("flight_no", "").strip().upper()
        if c_fn == fn:
            matched.append(c)
    return matched


# ============================================================
# 主命令
# ============================================================

def cmd_search(args):
    """搜索航班（多源合并+购票建议）"""
    from_city = args.from_city
    to_city = args.to_city
    dep_date = args.dep_date

    # 并行查询
    fliggy_result = search_fliggy_flights(from_city, to_city, dep_date)
    tuniu_result = search_tuniu_flights(from_city, to_city, dep_date)
    rg_result = search_rg_flights(from_city, to_city, dep_date)

    # 合并航班
    all_flights = []

    # 飞猪数据
    if fliggy_result.get("flights"):
        all_flights.extend(fliggy_result["flights"])

    # 途牛数据（去重：按航班号）
    if tuniu_result.get("flights"):
        existing_fns = {f["flight_no"].upper() for f in all_flights if f.get("flight_no")}
        for tf in tuniu_result["flights"]:
            fn = tf.get("flight_no", "").upper()
            if fn and fn in existing_fns:
                # 已存在，补充途牛价格
                for af in all_flights:
                    if af.get("flight_no", "").upper() == fn:
                        af["tuniu_price"] = tf.get("price", 0)
                        af["tuniu_url"] = ""
                        break
            else:
                all_flights.append(tf)
                existing_fns.add(fn)

    # 按价格排序
    all_flights.sort(key=lambda x: x.get("price", 99999) if x.get("price", 0) > 0 else 99999)

    # 取最低价生成购票建议
    lowest = None
    for f in all_flights:
        if f.get("price", 0) > 0:
            lowest = f
            break

    advice = None
    if lowest:
        all_prices = [f["price"] for f in all_flights if f.get("price", 0) > 0]
        advice = buy_or_wait(lowest["price"], from_city, to_city, dep_date, all_prices)

    output = {
        "success": True,
        "action": "search",
        "from": from_city,
        "to": to_city,
        "date": dep_date,
        "flights_count": len(all_flights),
        "flights": all_flights[:20],  # 最多返回20个
        "sources": {
            "飞猪": {"count": len(fliggy_result.get("flights", [])), "error": fliggy_result.get("error")},
            "途牛": {"count": len(tuniu_result.get("flights", [])), "error": tuniu_result.get("error")},
            "RG": {"count": len(rg_result.get("flights", [])), "error": rg_result.get("error")},
        },
        "lowest_price": lowest["price"] if lowest else None,
        "lowest_flight": lowest["flight_no"] if lowest else None,
        "advice": advice,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_calendar(args):
    """低价日历（扫描多日价格）"""
    from_city = args.from_city
    to_city = args.to_city
    start_date = args.start_date
    days = min(args.days, 30)  # 最多30天

    calendar = []

    for i in range(days):
        try:
            d = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
            date_str = d.strftime("%Y-%m-%d")
        except ValueError:
            continue

        # 查飞猪（速度快，数据全）
        result = search_fliggy_flights(from_city, to_city, date_str)
        flights = result.get("flights", [])

        if flights:
            prices = [f["price"] for f in flights if f.get("price", 0) > 0]
            lowest = min(prices) if prices else None
            calendar.append({
                "date": date_str,
                "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][d.weekday()],
                "lowest_price": lowest,
                "flight_count": len(flights),
                "cheapest_flight": flights[0]["flight_no"] if flights else None,
                "url": flights[0].get("url", "") if flights else "",
            })
        else:
            calendar.append({
                "date": date_str,
                "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][d.weekday()],
                "lowest_price": None,
                "flight_count": 0,
                "cheapest_flight": None,
                "url": "",
            })

        # 限速：避免请求过快
        time.sleep(0.3)

    # 找价格洼地
    priced_days = [d for d in calendar if d.get("lowest_price")]
    if priced_days:
        min_price = min(d["lowest_price"] for d in priced_days)
        avg_price = sum(d["lowest_price"] for d in priced_days) / len(priced_days)

        for d in calendar:
            p = d.get("lowest_price")
            if p:
                if p <= min_price * 1.05:
                    d["tag"] = "🟢 低价"
                elif p <= avg_price:
                    d["tag"] = "🟡 适中"
                else:
                    d["tag"] = "🔴 偏贵"
            else:
                d["tag"] = "— 无数据"

        # 最便宜日期的购票建议
        cheapest = min(priced_days, key=lambda x: x["lowest_price"])
        advice = buy_or_wait(cheapest["lowest_price"], from_city, to_city, cheapest["date"])
    else:
        advice = None
        min_price = None
        avg_price = None

    output = {
        "success": True,
        "action": "calendar",
        "from": from_city,
        "to": to_city,
        "start_date": start_date,
        "days": days,
        "calendar": calendar,
        "min_price": min_price,
        "avg_price": int(avg_price) if avg_price else None,
        "cheapest_date": cheapest["date"] if priced_days else None,
        "advice": advice,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_monitor(args):
    """生成监控任务JSON（供宿主Agent定时执行）"""
    monitor = {
        "action": "monitor",
        "from": args.from_city,
        "to": args.to_city,
        "date": args.dep_date,
        "threshold_percent": args.threshold or 10,
        "threshold_amount": args.amount or 200,
        "frequency": args.frequency or "daily",
        "duration_days": args.duration or 7,
        "created_at": datetime.now().isoformat(),
        "status": "active",
    }
    print(json.dumps(monitor, ensure_ascii=False, indent=2))


# ============================================================
# CLI入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="机票聪明买：多平台比价+低价日历+购票建议")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # search
    search_p = subparsers.add_parser("search", help="搜索航班（多源合并+购票建议）")
    search_p.add_argument("--from", dest="from_city", required=True, help="出发城市")
    search_p.add_argument("--to", dest="to_city", required=True, help="到达城市")
    search_p.add_argument("--date", dest="dep_date", required=True, help="出发日期 YYYY-MM-DD")
    search_p.add_argument("--trip-type", dest="trip_type", default="one_way", help="行程类型 one_way/round_trip")
    search_p.add_argument("--cabin", default="economy", help="舱位 economy/business/first")
    search_p.add_argument("--adults", type=int, default=1, help="成人数")

    # calendar
    cal_p = subparsers.add_parser("calendar", help="低价日历（扫描多日价格）")
    cal_p.add_argument("--from", dest="from_city", required=True, help="出发城市")
    cal_p.add_argument("--to", dest="to_city", required=True, help="到达城市")
    cal_p.add_argument("--start-date", dest="start_date", required=True, help="起始日期 YYYY-MM-DD")
    cal_p.add_argument("--days", type=int, default=14, help="扫描天数（最多30）")
    cal_p.add_argument("--cabin", default="economy", help="舱位 economy/business/first")

    # monitor
    mon_p = subparsers.add_parser("monitor", help="生成降价监控任务JSON")
    mon_p.add_argument("--from", dest="from_city", required=True, help="出发城市")
    mon_p.add_argument("--to", dest="to_city", required=True, help="到达城市")
    mon_p.add_argument("--date", dest="dep_date", required=True, help="出发日期 YYYY-MM-DD")
    mon_p.add_argument("--threshold", type=int, default=10, help="降价阈值百分比")
    mon_p.add_argument("--amount", type=int, default=200, help="降价阈值金额")
    mon_p.add_argument("--frequency", default="daily", help="检查频率 daily/twice_daily")
    mon_p.add_argument("--duration", type=int, default=7, help="监控天数")

    args = parser.parse_args()

    if args.command == "search":
        cmd_search(args)
    elif args.command == "calendar":
        cmd_calendar(args)
    elif args.command == "monitor":
        cmd_monitor(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
