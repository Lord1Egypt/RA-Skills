#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from typing import Any

COFFEE_NAME_KEYWORDS = (
    "咖啡",
    "拿铁",
    "美式",
    "摩卡",
    "冷萃",
    "浓缩",
    "dirty",
    "espresso",
    "latte",
    "americano",
    "mocha",
)

PREFERENCE_NAME_KEYWORDS = COFFEE_NAME_KEYWORDS + (
    "茶",
    "毛尖",
    "果茶",
    "奶茶",
    "轻咖",
    "燕麦",
    "椰",
    "桂花",
    "葡萄",
    "柚",
    "柠檬",
    "芒果",
    "西柚",
    "桃",
    "草莓",
    "乳",
    "奶",
    "低卡",
    "低糖",
)


def describe_weather_feel(weather: dict[str, Any] | None) -> str | None:
    temperature = weather.get("temperatureC") if weather else None
    if not isinstance(temperature, (int, float)):
        return None

    if temperature <= 10:
        return "有点冷"
    if temperature <= 18:
        return "偏凉"
    if temperature <= 26:
        return "挺舒服"
    return "有点热"


def read_order_good_count(order_good: dict[str, Any]) -> int:
    count = order_good.get("num") or order_good.get("quantity") or order_good.get("count")
    if isinstance(count, int) and count > 0:
        return count
    if isinstance(count, str) and count.isdigit():
        return int(count)
    # Deliberately differs from query_orders.read_good_num: scoring only needs
    # to know the named item appeared, while order summaries require exact cups.
    return 1


def collect_order_good_counts(orders: dict[str, Any] | None) -> Counter[str]:
    counts: Counter[str] = Counter()
    for order in (orders or {}).get("orders", []):
        goods = order.get("goods", [])
        if not isinstance(goods, list):
            continue
        for order_good in goods:
            if not isinstance(order_good, dict):
                continue
            name = str(order_good.get("name") or "").strip()
            if name:
                counts[name] += read_order_good_count(order_good)
    return counts


def names_match(left_name: str, right_name: str) -> bool:
    left = left_name.strip()
    right = right_name.strip()
    if not left or not right:
        return False
    return left == right or left in right or right in left


def get_order_count_for_good(good: dict[str, Any], order_good_counts: Counter[str]) -> int:
    good_name = str(good.get("name") or "").strip()
    if not good_name:
        return 0
    return sum(
        count
        for ordered_name, count in order_good_counts.items()
        if names_match(good_name, ordered_name)
    )


def normalize_text_items(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def extract_name_preference_tags(name: str) -> set[str]:
    lower_name = name.lower()
    return {
        keyword
        for keyword in PREFERENCE_NAME_KEYWORDS
        if keyword.lower() in lower_name
    }


def extract_good_preference_tags(good: dict[str, Any]) -> set[str]:
    tags = extract_name_preference_tags(str(good.get("name") or ""))
    for field in ("categories", "ingredients", "temperatures", "sugarLevels"):
        tags.update(normalize_text_items(good.get(field)))
    return {tag for tag in tags if tag}


def build_history_preference_tags(
    goods: list[dict[str, Any]],
    order_good_counts: Counter[str],
) -> set[str]:
    tags: set[str] = set()
    for ordered_name in order_good_counts:
        tags.update(extract_name_preference_tags(ordered_name))

    for good in goods:
        if get_order_count_for_good(good, order_good_counts) > 0:
            tags.update(extract_good_preference_tags(good))

    return tags


def score_weather_fit(good: dict[str, Any], weather: dict[str, Any] | None) -> int:
    feel = describe_weather_feel(weather)
    temperatures = good.get("temperatures") or []
    if feel in {"有点冷", "偏凉"} and any("热" in str(item) for item in temperatures):
        return 8
    if feel == "有点热" and any("冰" in str(item) for item in temperatures):
        return 8
    return 0


def choose_recommendation_good(
    goods: list[dict[str, Any]],
    orders: dict[str, Any] | None,
    weather: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if not goods:
        return None

    order_good_counts = collect_order_good_counts(orders)
    if order_good_counts:
        candidate_counts = [
            get_order_count_for_good(good, order_good_counts)
            for good in goods
        ]
        min_count = min(candidate_counts)
        max_count = max(candidate_counts)
        history_tags = build_history_preference_tags(goods, order_good_counts)

        scored_goods: list[tuple[float, dict[str, Any]]] = []
        for index, good in enumerate(goods):
            order_count = candidate_counts[index]
            preference_overlap = len(extract_good_preference_tags(good) & history_tags)
            score = preference_overlap * 10 + score_weather_fit(good, weather)

            if order_count == 0:
                score += 100
            elif order_count == min_count:
                score += 70

            if max_count > min_count and order_count == max_count:
                score -= 80

            score -= order_count * 4
            score -= index * 0.01
            scored_goods.append((score, good))

        return max(scored_goods, key=lambda item: item[0])[1]

    feel = describe_weather_feel(weather)
    if feel in {"有点冷", "偏凉"}:
        for good in goods:
            temperatures = good.get("temperatures") or []
            if any("热" in str(item) for item in temperatures):
                return good

    if feel == "有点热":
        for good in goods:
            temperatures = good.get("temperatures") or []
            if any("冰" in str(item) for item in temperatures):
                return good

    return goods[0]


def summarize_top_ordered_goods(order_good_counts: Counter[str], limit: int = 3) -> str | None:
    if not order_good_counts:
        return None
    items = [
        f"{name}（{count}次）"
        for name, count in order_good_counts.most_common(limit)
    ]
    return "、".join(items)


def build_recommendation_reason_signals(
    recommended_good: dict[str, Any],
    orders: dict[str, Any] | None,
    weather: dict[str, Any] | None,
) -> list[str]:
    signals: list[str] = []
    recommended_name = recommended_good.get("name")
    order_good_counts = collect_order_good_counts(orders)

    if recommended_name and order_good_counts:
        recommended_order_count = get_order_count_for_good(
            recommended_good,
            order_good_counts,
        )
        if recommended_order_count:
            signals.append(f"这杯在可见订单里出现过：{recommended_order_count}次")
        else:
            signals.append("这杯在可见订单里没有出现，适合做新尝试")

        top_ordered_goods = summarize_top_ordered_goods(order_good_counts)
        if top_ordered_goods:
            signals.append(f"常点参考：{top_ordered_goods}")

    weather_feel = describe_weather_feel(weather)
    if weather_feel:
        signals.append(f"当前天气体感：{weather_feel}")

    temperatures = recommended_good.get("temperatures") or []
    if temperatures:
        signals.append(f"可选温度：{'、'.join(str(item) for item in temperatures)}")

    sugar_levels = recommended_good.get("sugarLevels") or []
    if sugar_levels:
        signals.append(f"可选糖度：{'、'.join(str(item) for item in sugar_levels)}")

    calories = recommended_good.get("calories")
    if calories:
        signals.append(f"热量信息：{calories}")

    categories = recommended_good.get("categories") or []
    if categories:
        signals.append(f"商品分类：{'、'.join(str(item) for item in categories)}")

    ingredients = recommended_good.get("ingredients") or []
    if ingredients:
        signals.append(f"主要配料：{'、'.join(str(item) for item in ingredients)}")

    return signals


def build_recommendation_fallback_copy(
    goods: list[dict[str, Any]],
    orders: dict[str, Any] | None,
    weather: dict[str, Any] | None,
) -> str | None:
    recommended_good = choose_recommendation_good(goods, orders, weather)
    if not recommended_good:
        return None

    recommended_name = recommended_good.get("name")
    if not recommended_name:
        return None

    weather_feel = describe_weather_feel(weather)
    has_history = bool((orders or {}).get("orders"))

    if weather_feel:
        if has_history:
            return f"哇我们的老朋友，今天天气{weather_feel}，建议您喝{recommended_name}。"
        return f"今天天气{weather_feel}，建议您喝{recommended_name}。"

    if has_history:
        return f"哇我们的老朋友，今天建议您喝{recommended_name}。"
    return f"今天建议您喝{recommended_name}。"


def build_recommendation_material_lines(
    goods: list[dict[str, Any]],
    orders: dict[str, Any] | None,
    weather: dict[str, Any] | None,
) -> list[str]:
    recommended_good = choose_recommendation_good(goods, orders, weather)
    if not recommended_good:
        return []

    recommended_name = recommended_good.get("name")
    if not recommended_name:
        return []

    lines = [
        f"推荐候选饮品：{recommended_name}",
        f"推荐素材字段：candidateName={recommended_name}",
        "推荐尝试方向：优先推荐口味相邻但不常点或未点过的饮品；不要把用户最常点的饮品作为默认主推，除非菜单里没有合适替代。",
        "推荐素材字段：explorationMode=prefer_less_ordered_similar_goods",
        "主推荐文案由大模型根据下方素材自行生成；回答结构、语气和活动留资以“回答要求”区块为准。",
    ]
    reason_signals = build_recommendation_reason_signals(
        recommended_good,
        orders,
        weather,
    )
    if reason_signals:
        lines.append(f"推荐素材字段：reasonSignals={' | '.join(reason_signals)}")
        lines.append(f"可用推荐依据：{'；'.join(reason_signals)}。")

    return lines
