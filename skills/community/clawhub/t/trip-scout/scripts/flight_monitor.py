#!/usr/bin/env python3
"""
机票价格监控与买入时机分析

通过携程 API 抓取航班票价/余票/降价预测，积累价格历史，
分析合理入手区间，给出最佳下单时机建议。

用法:
  # 登录（首次使用，复用携程 Cookie）
  python scripts/flight_monitor.py login [--show]

  # 单次抓取
  python scripts/flight_monitor.py --route "成都->伊宁" --date 2026-09-25

  # 分析报告（含 flyai 交叉验证）
  python scripts/flight_monitor.py --route "成都->伊宁" --date 2026-09-25 --analyze

  # 配置文件模式（多航线批量）
  python scripts/flight_monitor.py --config ~/.trip-scout/flight-monitor/config.json

输出: JSON 到 stdout + Markdown 表格到 stderr
历史数据: ~/.trip-scout/flight-monitor/history.json
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# Windows GBK 终端兼容
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# vendored 模块路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "vendor"))

from ctrip.client import CtripClient
from ctrip.login import check_login, login, logout
from ctrip.flight import (
    FlightTicket,
    FlightResult,
    PricePrediction,
    fetch_flights,
    CITY_CODES,
    BUDGET_AIRLINES,
    is_budget_airline,
    MULTI_AIRPORT_CITIES,
    match_airport,
    classify_time_period,
)

# ── 路径 ──────────────────────────────────────────────────────────────────

DATA_DIR = Path(os.path.expanduser("~/.trip-scout/flight-monitor"))
HISTORY_FILE = DATA_DIR / "history.json"
CONFIG_FILE = DATA_DIR / "config.json"

# 假期日历（数据驱动，便于维护扩展）
# 参考 references/flight-search.md 假期影响表
HOLIDAY_CALENDAR: list[dict[str, Any]] = [
    {"name": "元旦",   "start": "2026-01-01", "end": "2026-01-03", "premium": 1.25},
    {"name": "春节",   "start": "2026-02-17", "end": "2026-02-23", "premium": 1.75},
    {"name": "清明",   "start": "2026-04-04", "end": "2026-04-06", "premium": 1.25},
    {"name": "劳动节", "start": "2026-05-01", "end": "2026-05-05", "premium": 1.40},
    {"name": "端午",   "start": "2026-05-31", "end": "2026-06-02", "premium": 1.25},
    {"name": "中秋",   "start": "2026-09-25", "end": "2026-09-27", "premium": 1.30},
    {"name": "国庆",   "start": "2026-10-01", "end": "2026-10-07", "premium": 1.75},
]


# ── 假期查询 ──────────────────────────────────────────────────────────────

def _lookup_holiday(date: str) -> tuple[str, float]:
    """查询日期对应的假期名称和溢价系数

    Returns:
        (假期名称, 溢价系数)  平日返回 ("平日", 1.0)
    """
    try:
        d = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return "平日", 1.0
    for h in HOLIDAY_CALENDAR:
        try:
            start = datetime.strptime(h["start"], "%Y-%m-%d")
            end = datetime.strptime(h["end"], "%Y-%m-%d")
        except ValueError:
            continue
        if start <= d <= end:
            return h["name"], float(h.get("premium", 1.0))
    return "平日", 1.0


# ── 廉航/中转过滤 ─────────────────────────────────────────────────────────

def _split_budget_tickets(tickets: list[dict[str, Any]]) -> tuple[list[dict], list[dict]]:
    """将航班列表分为 (非廉航, 廉航) 两组"""
    main, budget = [], []
    for t in tickets:
        airlines = t.get("airlines", "") or ""
        flight_numbers = t.get("flight_numbers", "") or ""
        if is_budget_airline(airlines, flight_numbers):
            budget.append(t)
        else:
            main.append(t)
    return main, budget


def _filter_direct_only(tickets: list[Any]) -> list[Any]:
    """过滤掉中转/经停航班，只保留直飞"""
    return [t for t in tickets
            if (t.get("flight_type", "") if isinstance(t, dict) else t.flight_type) == "直飞"]


# ── 价格历史 ──────────────────────────────────────────────────────────────

def load_history() -> dict[str, Any]:
    """加载价格历史"""
    if not HISTORY_FILE.exists():
        return {"routes": {}}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.setdefault("routes", {})
        return data
    except (json.JSONDecodeError, OSError):
        return {"routes": {}}


def save_history(history: dict[str, Any]) -> None:
    """保存价格历史"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def update_history(
    history: dict[str, Any],
    route: str,
    date: str,
    result: FlightResult,
    now: datetime | None = None,
) -> None:
    """将一次抓取结果存入历史"""
    if now is None:
        now = datetime.now()

    routes = history.setdefault("routes", {})
    route_data = routes.setdefault(route, {})
    date_data = route_data.setdefault(date, {"snapshots": []})

    snapshot = {
        "timestamp": now.strftime("%Y-%m-%dT%H:%M:%S"),
        "source": result.source,
        "tickets": [
            {
                "flight_numbers": t.flight_numbers,
                "airlines": t.airlines,
                "departure_time": t.departure_time,
                "arrival_time": t.arrival_time,
                "departure_airport": t.departure_airport,
                "arrival_airport": t.arrival_airport,
                "flight_type": t.flight_type,
                "total_duration": t.total_duration,
                "price": t.price,
                "discount": t.discount,
                "remaining_seats": t.remaining_seats,
                "labels": t.labels,
            }
            for t in result.tickets
        ],
        "lowest_price": min((t.price for t in result.tickets), default=0),
        "avg_price": (
            round(sum(t.price for t in result.tickets) / len(result.tickets))
            if result.tickets else 0
        ),
    }

    # 降价预测
    if result.prediction:
        snapshot["prediction"] = {
            "raw_text": result.prediction.raw_text,
            "predicted_price": result.prediction.predicted_price,
            "probability": result.prediction.probability,
            "time_range": result.prediction.time_range,
            "source": result.prediction.source,
        }

    date_data["snapshots"].append(snapshot)

    # 清理过期数据（默认保留 60 天）
    cutoff = (now - timedelta(days=60)).strftime("%Y-%m-%dT%H:%M:%S")
    for route_key, route_val in routes.items():
        for date_key, date_val in list(route_val.items()):
            snaps = date_val.get("snapshots", [])
            date_val["snapshots"] = [
                s for s in snaps if s.get("timestamp", "") >= cutoff
            ]
            if not date_val["snapshots"]:
                del route_val[date_key]


# ── 价格分析 ──────────────────────────────────────────────────────────────

def analyze_prices(
    history: dict[str, Any],
    route: str,
    date: str,
    include_budget: bool = False,
    passengers: int = 3,
    include_transfer: bool = False,
) -> dict[str, Any]:
    """价格分析: 历史 + 趋势 + 入手区间 + 建议

    Args:
        include_budget: 是否包含廉航航班在价格统计中（默认排除）
        passengers: 每组人数（用于计算含通勤的总成本）
        include_transfer: 是否包含中转/经停航班（默认仅直飞）
    """
    route_data = history.get("routes", {}).get(route, {})
    snapshots = route_data.get(date, {}).get("snapshots", [])

    if not snapshots:
        return {"error": "无历史数据，请先运行抓取"}

    # 对每个快照过滤廉航+中转，重新计算 lowest_price / avg_price
    filtered_snapshots = []
    budget_count = 0
    transfer_count = 0
    for s in snapshots:
        tickets = s.get("tickets", [])
        if not include_budget:
            tickets, budget_tickets = _split_budget_tickets(tickets)
            budget_count = max(budget_count, len(budget_tickets))
        if not include_transfer:
            before = len(tickets)
            tickets = _filter_direct_only(tickets)
            transfer_count = max(transfer_count, before - len(tickets))
        prices = [t.get("price", 0) for t in tickets if t.get("price")]
        if not prices:
            continue
        filtered_snapshots.append({
            **s,
            "lowest_price": min(prices),
            "avg_price": round(sum(prices) / len(prices)),
            "ticket_count": len(tickets),
        })

    if not filtered_snapshots:
        return {"error": "历史数据中无有效价格（廉航过滤后为空，尝试 --include-budget）"}

    # 价格序列
    prices = [s["lowest_price"] for s in filtered_snapshots]
    current_price = prices[-1]
    min_price = min(prices)
    max_price = max(prices)
    avg_price = round(sum(prices) / len(prices))

    # 百分位
    percentile = round(
        sum(1 for p in prices if p < current_price) / len(prices) * 100
    )

    # 距出发天数
    try:
        dep_date = datetime.strptime(date, "%Y-%m-%d")
        days_left = (dep_date - datetime.now()).days
    except ValueError:
        days_left = 0

    # 假期溢价
    holiday_name, holiday_premium = _lookup_holiday(date)

    # 趋势（最近3次）
    recent = prices[-3:]
    if len(recent) >= 3:
        if recent[-1] > recent[-2] > recent[-3]:
            trend = "上涨"
        elif recent[-1] < recent[-2] < recent[-3]:
            trend = "下跌"
        elif abs(recent[-1] - sum(recent[:-1]) / len(recent[:-1])) < 50:
            trend = "稳定"
        else:
            trend = "波动"
        trend_detail = f"¥{recent[-3]}->¥{recent[-2]}->¥{recent[-1]}"
    elif len(recent) == 2:
        diff = recent[-1] - recent[-2]
        trend = "上涨" if diff > 50 else ("下跌" if diff < -50 else "稳定")
        trend_detail = f"¥{recent[-2]}->¥{recent[-1]}"
    else:
        trend = "数据不足"
        trend_detail = f"¥{recent[-1]}"

    # 余票状态（最近快照，仅看非廉航）
    latest_snap = filtered_snapshots[-1]
    latest_tickets = latest_snap.get("tickets", [])
    if not include_budget:
        latest_tickets, _ = _split_budget_tickets(latest_tickets)
    if not include_transfer:
        latest_tickets = _filter_direct_only(latest_tickets)
    all_remaining = [
        t.get("remaining_seats") for t in latest_tickets
        if t.get("remaining_seats") is not None
    ]
    if all_remaining:
        min_remaining = min(all_remaining)
        if min_remaining <= 3:
            seat_status = "紧张"
        elif min_remaining <= 9:
            seat_status = "偏少"
        else:
            seat_status = "充足"
    else:
        # 用折扣率推断
        discounts = [t.get("discount", "") for t in latest_tickets]
        has_low_discount = any(d and ("折" in d) and float(
            d.replace("折", "").replace("起", "")
        ) <= 4 for d in discounts if d and "折" in d)
        seat_status = "充足" if has_low_discount else "未知"

    # 携程降价预测
    predictions = [s.get("prediction") for s in filtered_snapshots if s.get("prediction")]
    latest_prediction = predictions[-1] if predictions else None

    # 入手区间（假期溢价调整：假期期间合理价格上浮）
    buy_price = round(min_price * 1.1 * holiday_premium)
    watch_price = round(avg_price)
    must_buy_price = round(avg_price * 1.3 * holiday_premium)

    # 如果携程预测了更低价格，用预测价作为入手目标
    if latest_prediction and latest_prediction.get("predicted_price"):
        pred_price = latest_prediction["predicted_price"]
        if pred_price < buy_price:
            buy_price = pred_price

    # 综合建议
    prob = latest_prediction.get("probability") if latest_prediction else None

    if current_price <= buy_price or (days_left <= 14 and seat_status == "紧张"):
        recommendation = "立即下单"
        next_check = "尽快"
        reason = "价格已到建议入手价" if current_price <= buy_price else "距出发不足14天且余票紧张"
    elif (current_price < watch_price and days_left > 30 and trend != "上涨"):
        # 携程预测辅助：高概率降价倾向观望
        if prob and prob >= 70:
            recommendation = "继续观望"
            next_check = "3天后"
            reason = f"价格低于均价且携程预测降价概率{prob}%"
        else:
            recommendation = "继续观望"
            next_check = "3天后"
            reason = "价格低于均价，距出发尚早，可继续观望"
    else:
        if prob and prob >= 70:
            recommendation = "设置提醒"
            next_check = "1天后"
            reason = f"携程预测降价概率{prob}%，但当前价格偏高，建议密切关注"
        else:
            recommendation = "设置提醒"
            next_check = "1天后"
            reason = "价格处于观望区间，建议每日关注"

    # 预测辅助说明
    prediction_note = None
    if latest_prediction:
        parts = []
        if latest_prediction.get("time_range"):
            parts.append(latest_prediction["time_range"])
        if latest_prediction.get("predicted_price"):
            parts.append(f"可能降价至¥{latest_prediction['predicted_price']}")
        if prob:
            parts.append(f"概率{prob}%")
        prediction_note = "，".join(parts)
    elif predictions:
        prediction_note = "历史有预测数据，但最新快照未捕获"
    else:
        prediction_note = "携程未提供预测"

    # 时段+机场分析（基于最新快照的非廉航直飞航班）
    dep_city = route.split("->")[0].strip() if "->" in route else ""
    latest_tickets = latest_snap.get("tickets", [])
    if not include_budget:
        latest_tickets, _ = _split_budget_tickets(latest_tickets)
    if not include_transfer:
        latest_tickets = _filter_direct_only(latest_tickets)
    ta_analysis = analyze_by_time_and_airport(latest_tickets, dep_city, passengers)
    flight_recs = recommend_flights(latest_tickets, dep_city, passengers, include_budget)

    return {
        "route": route,
        "date": date,
        "days_left": days_left,
        "holiday": {
            "name": holiday_name,
            "premium": holiday_premium,
        },
        "budget_filter": {
            "enabled": not include_budget,
            "excluded_count": budget_count,
            "airlines": list(BUDGET_AIRLINES.keys()) if not include_budget else [],
        },
        "transfer_filter": {
            "direct_only": not include_transfer,
            "excluded_count": transfer_count,
        },
        "stats": {
            "min_price": min_price,
            "max_price": max_price,
            "avg_price": avg_price,
            "current_price": current_price,
            "percentile": percentile,
            "snapshot_count": len(filtered_snapshots),
        },
        "trend": {
            "direction": trend,
            "detail": trend_detail,
        },
        "seats": {
            "status": seat_status,
            "min_remaining": min(all_remaining) if all_remaining else None,
        },
        "prediction": {
            "latest": latest_prediction,
            "note": prediction_note,
        },
        "buy_zones": {
            "buy_price": buy_price,
            "watch_price": watch_price,
            "must_buy_price": must_buy_price,
        },
        "recommendation": {
            "action": recommendation,
            "next_check": next_check,
            "reason": reason,
        },
        "time_airport_analysis": ta_analysis,
        "flight_recommendations": flight_recs,
        "snapshots": [
            {
                "timestamp": s.get("timestamp", ""),
                "lowest_price": s.get("lowest_price", 0),
                "avg_price": s.get("avg_price", 0),
                "ticket_count": len(s.get("tickets", [])),
                "prediction": s.get("prediction"),
            }
            for s in filtered_snapshots
        ],
    }


# ── 时段+机场分析 ─────────────────────────────────────────────────────────

def analyze_by_time_and_airport(
    tickets: list[dict[str, Any]],
    dep_city: str,
    passengers: int = 3,
) -> dict[str, Any]:
    """按时段和机场分析航班价格分布

    Args:
        tickets: 非廉航航班列表（dict 格式，来自历史快照）
        dep_city: 出发城市名（用于匹配多机场信息）
        passengers: 每组人数（用于计算含通勤的总成本）
    """
    # 时段统计
    period_data: dict[str, list[int]] = {}
    for t in tickets:
        period = classify_time_period(t.get("departure_time", ""))
        period_data.setdefault(period, []).append(t.get("price", 0))

    time_analysis = []
    for period_name in ["早班", "上午", "下午", "晚班"]:
        prices = period_data.get(period_name, [])
        if not prices:
            continue
        time_analysis.append({
            "period": period_name,
            "count": len(prices),
            "lowest": min(prices),
            "avg": round(sum(prices) / len(prices)),
        })

    # 机场统计
    city_airports = MULTI_AIRPORT_CITIES.get(dep_city)
    airport_data: dict[str, list[dict[str, Any]]] = {}
    for t in tickets:
        airport_name = t.get("departure_airport", "")
        if city_airports:
            info = match_airport(airport_name, dep_city)
            key = info["key"] if info else "其他"
        else:
            key = "本场"
        airport_data.setdefault(key, []).append(t)

    airport_analysis = []
    for key, flights in airport_data.items():
        prices = [f.get("price", 0) for f in flights]
        if not prices:
            continue
        info = match_airport(flights[0].get("departure_airport", ""), dep_city) if city_airports else None
        commute_cost = info["commute_cost"] if info else 0
        commute_time = info["commute_time"] if info else ""
        preferred = info.get("preferred", False) if info else True
        lowest = min(prices)
        airport_analysis.append({
            "airport": key,
            "count": len(flights),
            "lowest": lowest,
            "avg": round(sum(prices) / len(prices)),
            "commute_cost": commute_cost,
            "commute_time": commute_time,
            "preferred": preferred,
            "total_per_family": lowest * passengers + commute_cost,
        })
    airport_analysis.sort(key=lambda a: a["total_per_family"])

    return {
        "time_analysis": time_analysis,
        "airport_analysis": airport_analysis,
        "passengers": passengers,
    }


def recommend_flights(
    tickets: list[dict[str, Any]],
    dep_city: str,
    passengers: int = 3,
    include_budget: bool = False,
) -> list[dict[str, Any]]:
    """推荐最优航班（综合考虑价格+机场通勤+时段+直飞偏好）

    评分逻辑:
    - 基础分 = 总成本（票价×人数 + 通勤费），越低越好
    - 直飞加分: -200（直飞优先）
    - 近郊机场加分: -100（双流等优先）
    - 时段加分: 上午(09-12) -50 / 早班(06-09) -30 / 下午 0 / 晚班 +50
    """
    city_airports = MULTI_AIRPORT_CITIES.get(dep_city)
    scored: list[dict[str, Any]] = []

    for t in tickets:
        price = t.get("price", 0)
        if not price:
            continue

        # 通勤成本
        airport_name = t.get("departure_airport", "")
        info = match_airport(airport_name, dep_city) if city_airports else None
        commute_cost = info["commute_cost"] if info else 0
        commute_time = info["commute_time"] if info else ""
        is_preferred_airport = info.get("preferred", False) if info else True
        total_cost = price * passengers + commute_cost

        # 评分（越低越好）
        score = total_cost

        # 直飞偏好
        flight_type = t.get("flight_type", "")
        is_direct = flight_type == "直飞"
        if is_direct:
            score -= 200

        # 近郊机场偏好
        if is_preferred_airport:
            score -= 100

        # 时段偏好（9:30出发习惯，上午最佳）
        period = classify_time_period(t.get("departure_time", ""))
        if period == "上午":
            score -= 50
        elif period == "早班":
            score -= 30
        elif period == "晚班":
            score += 50

        scored.append({
            "flight_numbers": t.get("flight_numbers", ""),
            "airlines": t.get("airlines", ""),
            "departure_time": t.get("departure_time", ""),
            "arrival_time": t.get("arrival_time", ""),
            "departure_airport": airport_name,
            "arrival_airport": t.get("arrival_airport", ""),
            "flight_type": flight_type,
            "total_duration": t.get("total_duration", ""),
            "price": price,
            "discount": t.get("discount", ""),
            "remaining_seats": t.get("remaining_seats"),
            "total_cost_per_family": total_cost,
            "commute_cost": commute_cost,
            "commute_time": commute_time,
            "score": score,
            "is_direct": is_direct,
            "airport_key": info["key"] if info else None,
            "is_preferred_airport": is_preferred_airport,
            "time_period": period,
        })

    scored.sort(key=lambda x: x["score"])
    return scored[:3]


# ── flyai 交叉验证 ────────────────────────────────────────────────────────

def flyai_cross_validate(
    dep_city: str, arr_city: str, date: str,
    include_budget: bool = False,
) -> dict[str, Any]:
    """调用 flyai search-flight 交叉验证价格"""
    try:
        result = subprocess.run(
            [
                "flyai", "search-flight",
                "--origin", dep_city,
                "--destination", arr_city,
                "--dep-date", date,
                "--sort-type", "3",  # 价格升序
            ],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            return {"available": False, "error": result.stderr.strip()[:200]}

        data = json.loads(result.stdout)
        # flyai 格式: data.itemList[].ticketPrice (string)
        items = data.get("data", {}).get("itemList", [])
        if not items:
            items = data.get("flights", data.get("result", []))

        if not items:
            return {"available": True, "lowest_price": None, "flight_count": 0}

        prices = []
        budget_count = 0
        for item in items:
            # 提取航司名和航班号用于廉航过滤
            journeys = item.get("journeys", [])
            airline_name = ""
            flight_no = ""
            for seg in journeys:
                for s in seg.get("segments", []):
                    airline_name += " " + (s.get("marketingTransportName") or "")
                    flight_no += " " + (s.get("marketingTransportNo") or "")

            if not include_budget and is_budget_airline(airline_name, flight_no):
                budget_count += 1
                continue

            p = item.get("ticketPrice") or item.get("price") or item.get("minPrice")
            if p:
                try:
                    prices.append(int(float(p)))
                except (TypeError, ValueError):
                    pass

        if not prices:
            return {
                "available": True,
                "lowest_price": None,
                "flight_count": 0,
                "budget_excluded": budget_count,
            }

        return {
            "available": True,
            "lowest_price": min(prices),
            "flight_count": len(items) - budget_count,
            "all_prices": sorted(prices)[:5],
            "budget_excluded": budget_count,
        }
    except FileNotFoundError:
        return {"available": False, "error": "flyai 命令未安装"}
    except subprocess.TimeoutExpired:
        return {"available": False, "error": "flyai 超时"}
    except (json.JSONDecodeError, OSError, ValueError) as e:
        return {"available": False, "error": str(e)[:200]}


# ── 输出格式化 ────────────────────────────────────────────────────────────

def format_fetch_output(result: FlightResult, route: str, date: str,
                        include_budget: bool = False,
                        include_transfer: bool = False) -> str:
    """格式化单次抓取结果为 Markdown"""
    dep, arr = route.split("->")
    holiday_name, _ = _lookup_holiday(date)
    holiday_suffix = f" ({holiday_name})" if holiday_name != "平日" else ""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"## ✈️ {dep.strip()} -> {arr.strip()} | {date}{holiday_suffix}",
        f"> 抓取时间: {now_str} | 数据源: 携程{result.source.upper()}",
        "",
    ]

    if not result.tickets:
        lines.append("未找到航班信息。")
        return "\n".join(lines)

    # 分离廉航
    all_tickets = result.tickets
    if include_budget:
        main_tickets = all_tickets
        budget_tickets = []
    else:
        main_tickets = [t for t in all_tickets
                        if not is_budget_airline(t.airlines, t.flight_numbers)]
        budget_tickets = [t for t in all_tickets
                          if is_budget_airline(t.airlines, t.flight_numbers)]

    # 过滤中转（默认只看直飞）
    if not include_transfer:
        transfer_tickets = [t for t in main_tickets if t.flight_type != "直飞"]
        main_tickets = [t for t in main_tickets if t.flight_type == "直飞"]
    else:
        transfer_tickets = []

    # 主航班表格
    lines.append("| 航班 | 航司 | 出发 | 到达 | 机场 | 时长 | 价格 | 折扣 | 余票 |")
    lines.append("|------|------|------|------|------|------|------|------|------|")
    for t in main_tickets:
        seat = f"仅剩{t.remaining_seats}张" if t.remaining_seats else "-"
        airport = f"{t.departure_airport}->{t.arrival_airport}"
        lines.append(
            f"| {t.flight_numbers} | {t.airlines} | {t.departure_time} | "
            f"{t.arrival_time} | {airport} | {t.total_duration} | "
            f"¥{t.price} | {t.discount} | {seat} |"
        )

    # 廉航单独展示
    if budget_tickets and not include_budget:
        lines.append("")
        lines.append(f"<details><summary>廉航航班 ({len(budget_tickets)}班，已排除出价格分析)</summary>")
        lines.append("")
        lines.append("| 航班 | 航司 | 出发 | 到达 | 机场 | 价格 | 折扣 |")
        lines.append("|------|------|------|------|------|------|------|")
        for t in budget_tickets:
            airport = f"{t.departure_airport}->{t.arrival_airport}"
            lines.append(
                f"| {t.flight_numbers} | {t.airlines} | {t.departure_time} | "
                f"{t.arrival_time} | {airport} | ¥{t.price} | {t.discount} |"
            )
        lines.append("")
        lines.append("</details>")

    # 中转航班单独展示
    if transfer_tickets and not include_transfer:
        lines.append("")
        lines.append(f"<details><summary>中转/经停航班 ({len(transfer_tickets)}班，已排除出价格分析)</summary>")
        lines.append("")
        lines.append("| 航班 | 航司 | 出发 | 到达 | 机场 | 时长 | 价格 |")
        lines.append("|------|------|------|------|------|------|------|")
        for t in transfer_tickets:
            airport = f"{t.departure_airport}->{t.arrival_airport}"
            lines.append(
                f"| {t.flight_numbers} | {t.airlines} | {t.departure_time} | "
                f"{t.arrival_time} | {airport} | {t.total_duration} | ¥{t.price} |"
            )
        lines.append("")
        lines.append("</details>")

    # 降价预测
    if result.prediction:
        lines.append("")
        lines.append("### 🔮 携程降价预测")
        lines.append(f"> {result.prediction.raw_text}")
        parts = []
        if result.prediction.time_range:
            parts.append(f"时间: {result.prediction.time_range}")
        if result.prediction.predicted_price:
            parts.append(f"预测低价: ¥{result.prediction.predicted_price}")
        if result.prediction.probability:
            parts.append(f"概率: {result.prediction.probability}%")
        if parts:
            lines.append(f"> {' | '.join(parts)}")
    else:
        lines.append("")
        lines.append("> ℹ️ 携程未提供降价预测")

    return "\n".join(lines)


def format_analyze_output(analysis: dict[str, Any], flyai_data: dict[str, Any] | None) -> str:
    """格式化分析报告为 Markdown"""
    route = analysis.get("route", "")
    date = analysis.get("date", "")
    dep, arr = route.split("->")
    holiday = analysis.get("holiday", {})
    budget_filter = analysis.get("budget_filter", {})
    stats = analysis.get("stats", {})
    trend = analysis.get("trend", {})
    seats = analysis.get("seats", {})
    prediction = analysis.get("prediction", {})
    buy_zones = analysis.get("buy_zones", {})
    rec = analysis.get("recommendation", {})
    snapshots = analysis.get("snapshots", [])
    days_left = analysis.get("days_left", 0)

    holiday_name = holiday.get("name", "平日")
    holiday_suffix = f" ({holiday_name})" if holiday_name != "平日" else ""

    lines = [
        f"## 📊 机票价格分析 | {dep.strip()} -> {arr.strip()} | {date}{holiday_suffix}",
        "",
    ]

    # 廉航过滤提示
    if budget_filter.get("enabled"):
        excluded = budget_filter.get("excluded_count", 0)
        airlines_list = budget_filter.get("airlines", [])
        if airlines_list:
            lines.append(f"> 已排除廉航: {', '.join(airlines_list)}"
                         + (f"（本次过滤{excluded}班）" if excluded else ""))

    # 中转过滤提示
    transfer_filter = analysis.get("transfer_filter", {})
    if transfer_filter.get("direct_only"):
        excluded = transfer_filter.get("excluded_count", 0)
        lines.append(f"> 仅显示直飞航班"
                     + (f"（已排除{excluded}班中转/经停）" if excluded else ""))
    if budget_filter.get("enabled") or transfer_filter.get("direct_only"):
        lines.append("")

    # 价格历史
    lines.append("### 价格历史")
    lines.append("| 时间 | 最低价 | 均价 | 航班数 | 预测 |")
    lines.append("|------|--------|------|--------|------|")
    for s in snapshots:
        ts = s.get("timestamp", "")
        # 简化时间显示
        try:
            dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")
            ts_display = dt.strftime("%m-%d %H:%M")
        except ValueError:
            ts_display = ts[:16]
        pred = "✅" if s.get("prediction") else "-"
        lines.append(
            f"| {ts_display} | ¥{s.get('lowest_price', 0)} | "
            f"¥{s.get('avg_price', 0)} | {s.get('ticket_count', 0)} | {pred} |"
        )

    # 统计
    lines.append("")
    lines.append("### 统计")
    lines.append(
        f"- 最低价: ¥{stats.get('min_price', 0)} | "
        f"最高价: ¥{stats.get('max_price', 0)} | "
        f"均价: ¥{stats.get('avg_price', 0)}"
    )
    lines.append(
        f"- 当前价格: ¥{stats.get('current_price', 0)} "
        f"(百分位: {stats.get('percentile', 0)}%)"
    )
    lines.append(f"- 距出发: {days_left}天 | 快照数: {stats.get('snapshot_count', 0)}")

    # 趋势
    lines.append("")
    lines.append("### 趋势")
    trend_emoji = {"上涨": "📈", "下跌": "📉", "稳定": "➡️", "波动": "🔄"}.get(
        trend.get("direction", ""), "❓"
    )
    lines.append(f"- 价格趋势: {trend_emoji} {trend.get('direction', '')} ({trend.get('detail', '')})")
    lines.append(f"- 余票状态: {seats.get('status', '未知')}")
    if seats.get("min_remaining"):
        lines.append(f"  (最少余票: {seats['min_remaining']}张)")

    # 携程预测
    pred_note = prediction.get("note", "携程未提供预测")
    lines.append(f"- 携程预测: {pred_note}")

    # 入手区间
    lines.append("")
    lines.append("### 💡 入手区间")
    lines.append("| 区间 | 价格 | 说明 |")
    lines.append("|------|------|------|")
    premium_note = f" ×{holiday.get('premium', 1.0)}假期溢价" if holiday_name != "平日" else ""
    pred_note = " / 携程预测价" if prediction.get("latest", {}) and prediction.get("latest", {}).get("predicted_price") else ""
    lines.append(f"| ✅ 建议入手价 | ¥{buy_zones.get('buy_price', 0)} | 历史最低价×1.1{premium_note}{pred_note} |")
    lines.append(f"| ⏳ 可观望价 | ¥{buy_zones.get('watch_price', 0)} | 历史均价 |")
    lines.append(f"| ⚠️ 必须下单价 | ¥{buy_zones.get('must_buy_price', 0)} | 均价×1.3{premium_note} |")

    # 建议
    lines.append("")
    rec_emoji = {"立即下单": "🔴", "继续观望": "🟢", "设置提醒": "🟡"}.get(
        rec.get("action", ""), "⚪"
    )
    lines.append(f"### 🎯 建议: {rec_emoji} {rec.get('action', '')}")
    lines.append(f"{rec.get('reason', '')}。建议{rec.get('next_check', '')}复查。")

    # 时段分析
    ta = analysis.get("time_airport_analysis", {})
    time_rows = ta.get("time_analysis", [])
    if time_rows:
        lines.append("")
        lines.append("### 📅 时段价格分布")
        lines.append("| 时段 | 班次 | 最低价 | 均价 |")
        lines.append("|------|------|--------|------|")
        for row in time_rows:
            lines.append(
                f"| {row['period']} | {row['count']} | "
                f"¥{row['lowest']} | ¥{row['avg']} |"
            )

    # 机场对比
    airport_rows = ta.get("airport_analysis", [])
    passengers = ta.get("passengers", 3)
    if len(airport_rows) > 1:
        lines.append("")
        lines.append(f"### 🏢 机场对比（含通勤成本，按{passengers}人/组计算）")
        lines.append("| 机场 | 班次 | 最低票价 | 通勤费 | 通勤时间 | 每组总成本 |")
        lines.append("|------|------|----------|--------|----------|-----------|")
        for row in airport_rows:
            star = "✅" if row.get("preferred") else "⚠️"
            lines.append(
                f"| {star} {row['airport']} | {row['count']} | "
                f"¥{row['lowest']} | ¥{row['commute_cost']} | "
                f"{row['commute_time']} | ¥{row['total_per_family']} |"
            )
        # 给出机场选择建议
        if len(airport_rows) >= 2:
            best = airport_rows[0]  # 总成本最低
            other = airport_rows[1]
            ticket_diff = other["lowest"] - best["lowest"]
            total_diff = other["total_per_family"] - best["total_per_family"]
            commute_diff = abs(other["commute_cost"] - best["commute_cost"])

            if total_diff > 0:
                # best 总成本更低
                if best.get("preferred"):
                    # 近郊机场既近又便宜 → 毫无疑问选近郊
                    lines.append(
                        f"\n> ✅ {best['airport']}总成本最低（¥{best['total_per_family']}），"
                        f"且通勤更近，毫无疑问选{best['airport']}。"
                    )
                else:
                    # 远郊机场虽然远但票价便宜到值得跑远路
                    lines.append(
                        f"\n> ⚠️ {best['airport']}总成本最低（¥{best['total_per_family']}），"
                        f"比{other['airport']}省¥{total_diff}/组。"
                        f" {best['airport']}票价低¥{ticket_diff}/人"
                        f"（>¥100/人阈值，值得跑远路）。"
                        f" 但{other['airport']}通勤仅{other['commute_time']}，"
                        f"图省事可选{other['airport']}（多花¥{total_diff}/组）。"
                    )
            else:
                # 近郊总成本更低
                lines.append(
                    f"\n> ✅ {best['airport']}总成本最低（¥{best['total_per_family']}）。"
                )

    # 推荐航班
    flight_recs = analysis.get("flight_recommendations", [])
    if flight_recs:
        lines.append("")
        lines.append("### ✈️ 推荐航班 Top3")
        lines.append("| 排名 | 航班 | 航司 | 出发->到达 | 机场 | 时段 | 票价 | 每组总成本 | 备注 |")
        lines.append("|------|------|------|-----------|------|------|------|-----------|------|")
        medals = ["🥇", "🥈", "🥉"]
        for i, f in enumerate(flight_recs):
            notes = []
            if f.get("is_direct"):
                notes.append("直飞")
            if f.get("airport_key"):
                notes.append(f.get("airport_key"))
            if f.get("remaining_seats") is not None and f["remaining_seats"] <= 9:
                notes.append(f"仅剩{f['remaining_seats']}张")
            if f.get("discount"):
                notes.append(f["discount"])
            lines.append(
                f"| {medals[i]} | {f['flight_numbers']} | {f['airlines']} | "
                f"{f['departure_time']}->{f['arrival_time']} | "
                f"{f['departure_airport']} | {f.get('time_period', '')} | "
                f"¥{f['price']} | ¥{f['total_cost_per_family']} | "
                f"{' '.join(notes)} |"
            )
        # 推荐理由
        best = flight_recs[0]
        reason_parts = [f"票价¥{best['price']}，含通勤每组¥{best['total_cost_per_family']}"]
        if best.get("is_direct"):
            reason_parts.append("直飞省时")
        if best.get("airport_key"):
            reason_parts.append(f"从{best['airport_key']}出发（通勤{best.get('commute_time', '未知')}）")
        if best.get("time_period"):
            reason_parts.append(f"{best['time_period']}起飞")
        lines.append(f"\n> **首选 {best['flight_numbers']}**：{best['airlines']} "
                     f"{best['departure_time']}->{best['arrival_time']}，"
                     f"{'，'.join(reason_parts)}。")

    # flyai 交叉验证
    if flyai_data:
        lines.append("")
        lines.append("### flyai 交叉验证")
        if not flyai_data.get("available"):
            lines.append(f"飞猪不可用: {flyai_data.get('error', '')}")
        elif flyai_data.get("lowest_price") is None:
            lines.append("飞猪无结果")
        else:
            ctrip_price = stats.get("current_price", 0)
            flyai_price = flyai_data["lowest_price"]
            diff = flyai_price - ctrip_price
            diff_str = f"{'+' if diff >= 0 else ''}¥{diff}" if diff != 0 else "持平"
            lines.append("| 平台 | 最低价 | 差异 |")
            lines.append("|------|--------|------|")
            lines.append(f"| 携程 | ¥{ctrip_price} | - |")
            lines.append(f"| 飞猪 | ¥{flyai_price} | {diff_str} |")
            budget_excluded = flyai_data.get("budget_excluded", 0)
            if budget_excluded:
                lines.append(f"_(飞猪已排除{budget_excluded}班廉航)_")
            if abs(diff) <= 20:
                lines.append("价格接近，差异可忽略。")
            elif diff < 0:
                lines.append(f"飞猪更便宜¥{abs(diff)}，建议对比下单。")
            else:
                lines.append(f"携程更便宜¥{diff}，建议选携程下单。")

    return "\n".join(lines)


# ── 命令处理 ──────────────────────────────────────────────────────────────

def cmd_login(args) -> int:
    """登录携程"""
    return login(show_browser=not args.headless)


def cmd_check_login(args) -> int:
    """检查登录状态"""
    ok, username = check_login()
    if ok:
        print(json.dumps({"logged_in": True, "username": username}, ensure_ascii=False))
    else:
        print(json.dumps({"logged_in": False}, ensure_ascii=False))
    return 0 if ok else 1


def cmd_logout(args) -> int:
    """登出"""
    logout()
    print(json.dumps({"logged_out": True}, ensure_ascii=False))
    return 0


def cmd_fetch(args) -> int:
    """单次抓取"""
    route = args.route
    date = args.date

    # 解析出发/到达
    if "->" not in route:
        print(json.dumps({"error": "route 格式应为 '出发->到达'，如 '成都->伊宁'"},
                         ensure_ascii=False))
        return 1

    dep, arr = [c.strip() for c in route.split("->", 1)]

    client = CtripClient(headless=not args.show)
    try:
        client.start()
        result = fetch_flights(client, dep, arr, date)
    finally:
        client.close()

    if not result.tickets:
        print(json.dumps({"error": "未找到航班信息", "route": route, "date": date},
                         ensure_ascii=False))
        return 1

    # 存入历史
    history = load_history()
    update_history(history, route, date, result)
    save_history(history)

    # 输出
    md = format_fetch_output(result, route, date,
                             include_budget=args.include_budget,
                             include_transfer=args.include_transfer)
    data = {
        "route": route,
        "date": date,
        "source": result.source,
        "ticket_count": len(result.tickets),
        "lowest_price": min(t.price for t in result.tickets),
        "budget_airlines_excluded": not args.include_budget,
        "tickets": [
            {
                "flight_numbers": t.flight_numbers,
                "airlines": t.airlines,
                "departure_time": t.departure_time,
                "arrival_time": t.arrival_time,
                "departure_airport": t.departure_airport,
                "arrival_airport": t.arrival_airport,
                "flight_type": t.flight_type,
                "total_duration": t.total_duration,
                "price": t.price,
                "discount": t.discount,
                "remaining_seats": t.remaining_seats,
                "labels": t.labels,
            }
            for t in result.tickets
        ],
        "prediction": (
            {
                "raw_text": result.prediction.raw_text,
                "predicted_price": result.prediction.predicted_price,
                "probability": result.prediction.probability,
                "time_range": result.prediction.time_range,
                "source": result.prediction.source,
            }
            if result.prediction else None
        ),
    }
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print("\n" + md, file=sys.stderr)
    return 0


def cmd_analyze(args) -> int:
    """分析报告"""
    route = args.route
    date = args.date

    if "->" not in route:
        print(json.dumps({"error": "route 格式应为 '出发->到达'"}, ensure_ascii=False))
        return 1

    # 先抓取最新数据
    dep, arr = [c.strip() for c in route.split("->", 1)]

    if not args.no_fetch:
        client = CtripClient(headless=not args.show)
        try:
            client.start()
            result = fetch_flights(client, dep, arr, date)
            if result.tickets:
                history = load_history()
                update_history(history, route, date, result)
                save_history(history)
        finally:
            client.close()

    # 分析
    history = load_history()
    analysis = analyze_prices(
        history, route, date,
        include_budget=args.include_budget,
        passengers=args.passengers,
        include_transfer=args.include_transfer,
    )

    if "error" in analysis:
        print(json.dumps(analysis, ensure_ascii=False))
        return 1

    # flyai 交叉验证
    flyai_data = None
    if not args.no_flyai:
        flyai_data = flyai_cross_validate(dep, arr, date, include_budget=args.include_budget)

    # 输出
    md = format_analyze_output(analysis, flyai_data)
    output = {**analysis}
    if flyai_data:
        output["flyai"] = flyai_data
    print(json.dumps(output, ensure_ascii=False, indent=2))
    print("\n" + md, file=sys.stderr)
    return 0


def cmd_config(args) -> int:
    """配置文件模式：多航线批量抓取"""
    config_path = Path(args.config)
    if not config_path.exists():
        print(json.dumps({"error": f"配置文件不存在: {config_path}"}, ensure_ascii=False))
        return 1

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    routes = config.get("routes", [])
    if not routes:
        print(json.dumps({"error": "配置文件中无航线"}, ensure_ascii=False))
        return 1

    results = []
    client = CtripClient(headless=not args.show)
    try:
        client.start()
        for r in routes:
            if not r.get("enabled", True):
                continue
            dep = r["departure_city"]
            arr = r["arrival_city"]
            date = r["departure_date"]
            route_key = f"{dep}->{arr}"

            try:
                result = fetch_flights(client, dep, arr, date)
                history = load_history()
                update_history(history, route_key, date, result)
                save_history(history)

                results.append({
                    "route": route_key,
                    "date": date,
                    "source": result.source,
                    "ticket_count": len(result.tickets),
                    "lowest_price": min((t.price for t in result.tickets), default=0),
                    "prediction": bool(result.prediction),
                })
                md = format_fetch_output(result, route_key, date,
                                         include_budget=args.include_budget,
                                         include_transfer=args.include_transfer)
                print(md, file=sys.stderr)
                print("", file=sys.stderr)
            except Exception as e:
                results.append({
                    "route": route_key,
                    "date": date,
                    "error": str(e)[:200],
                })
    finally:
        client.close()

    print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
    return 0


# ── CLI ───────────────────────────────────────────────────────────────────

def _parse_route_and_date(args) -> tuple[str, str] | None:
    """从 args 提取 route 和 date"""
    if not args.route or not args.date:
        return None
    return args.route, args.date


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="机票价格监控与买入时机分析",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/flight_monitor.py login --show          # 首次登录
  python scripts/flight_monitor.py --route "成都->伊宁" --date 2026-09-25
  python scripts/flight_monitor.py --route "成都->伊宁" --date 2026-09-25 --analyze
  python scripts/flight_monitor.py --config ~/.trip-scout/flight-monitor/config.json

支持城市: %s
""" % ", ".join(sorted(CITY_CODES.keys())),
    )
    sub = p.add_subparsers(dest="command")

    # login 子命令
    p_login = sub.add_parser("login", help="扫码登录携程")
    p_login.add_argument("--show", action="store_true", help="显示浏览器窗口")
    p_login.set_defaults(headless=False)

    # check-login 子命令
    sub.add_parser("check-login", help="检查登录状态")

    # logout 子命令
    sub.add_parser("logout", help="清除登录状态")

    # 主命令参数
    p.add_argument("--route", help='航线，格式 "出发->到达"，如 "成都->伊宁"')
    p.add_argument("--date", help="出发日期 YYYY-MM-DD")
    p.add_argument("--analyze", action="store_true", help="输出分析报告")
    p.add_argument("--config", help="配置文件路径（多航线批量）")
    p.add_argument("--show", action="store_true", help="显示浏览器窗口（调试）")
    p.add_argument("--no-fetch", action="store_true", help="分析模式跳过抓取，只用历史数据")
    p.add_argument("--no-flyai", action="store_true", help="跳过 flyai 交叉验证")
    p.add_argument("--include-budget", action="store_true",
                   help="包含廉航（春秋/西部/九元/联航/祥鹏）在价格分析中（默认排除）")
    p.add_argument("--include-transfer", action="store_true",
                   help="包含中转/经停航班（默认仅直飞）")
    p.add_argument("--passengers", type=int, default=3,
                   help="每组人数，用于计算含通勤的总成本（默认3）")

    args = p.parse_args(argv)

    # 子命令路由
    if args.command == "login":
        args.headless = not args.show
        return cmd_login(args)
    elif args.command == "check-login":
        return cmd_check_login(args)
    elif args.command == "logout":
        return cmd_logout(args)

    # 主命令
    if args.config:
        return cmd_config(args)
    elif args.route and args.date:
        if args.analyze:
            return cmd_analyze(args)
        else:
            return cmd_fetch(args)
    else:
        p.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
