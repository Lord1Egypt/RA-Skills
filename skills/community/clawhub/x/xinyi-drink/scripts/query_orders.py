#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from typing import Any

from build_response import render_orders_section
from recommendation_logic import COFFEE_NAME_KEYWORDS
from response_rendering import render_text_section
from skill_config import load_config
from skill_http import SkillHttpError, build_url, fetch_json, make_debug_logger
from user_state import load_mobile


debug_log = make_debug_logger("query_orders")


def is_coffee_name(name: str) -> bool:
    normalized_name = name.lower()
    return any(keyword.lower() in normalized_name for keyword in COFFEE_NAME_KEYWORDS)


def unique_names(names: list[str]) -> list[str]:
    return list(dict.fromkeys(name for name in names if name.strip()))


def collect_order_goods_names(orders: list[dict[str, Any]]) -> list[str]:
    return [
        str(good.get("name"))
        for order in orders
        for good in order.get("goods", [])
        if good.get("name")
    ]


def get_orders_list(orders_data: dict[str, Any]) -> list[dict[str, Any]]:
    orders = orders_data.get("orders", [])
    return orders if isinstance(orders, list) else []


def read_goods_num(order: dict[str, Any]) -> int:
    goods_num = order.get("goodsNum")
    if isinstance(goods_num, int):
        return goods_num
    if isinstance(goods_num, str) and goods_num.isdigit():
        return int(goods_num)
    return 0


def read_good_num(good: dict[str, Any]) -> int:
    num = good.get("num")
    if isinstance(num, int):
        return num
    if isinstance(num, str) and num.isdigit():
        return int(num)
    # Order summaries only count cups explicitly returned by the orders endpoint.
    return 0


def get_visible_drink_count(orders: list[dict[str, Any]]) -> int:
    return sum(read_goods_num(order) for order in orders)


def build_order_rating_lines(cup_count: int) -> list[str]:
    if cup_count <= 0:
        return []
    if cup_count <= 2:
        return [
            f"你已经在新一咖啡点单{cup_count}杯，欢迎开启美味体验！",
        ]
    if cup_count <= 5:
        return [
            f"你已经在新一咖啡点单{cup_count}杯，我们越来越有默契了！",
        ]
    if cup_count <= 10:
        return [
            f"你已经在新一咖啡点单{cup_count}杯，你一定是新一咖啡的忠实铁粉吧！",
        ]
    if cup_count < 15:
        return [
            f"你已经在新一咖啡点单{cup_count}杯，简直是我们的超级品鉴官！",
        ]
    return [
        f"你已经在新一咖啡点单{cup_count}杯，你不仅懂咖啡，有品位，更是新一不可或缺的灵魂伴侣，殿堂级知音！",
    ]


def summarize_coffee_cups(orders: list[dict[str, Any]]) -> tuple[int, list[str]]:
    cup_count = 0
    ambiguous_names: list[str] = []

    for order in orders:
        goods = order.get("goods", [])
        if not isinstance(goods, list) or not goods:
            continue

        coffee_goods = [
            good
            for good in goods
            if good.get("name") and is_coffee_name(str(good.get("name")))
        ]
        if not coffee_goods:
            continue

        if len(coffee_goods) == len(goods):
            good_level_count = sum(read_good_num(good) for good in coffee_goods)
            cup_count += good_level_count or read_goods_num(order)
            continue

        for good in coffee_goods:
            good_count = read_good_num(good)
            if good_count:
                cup_count += good_count
            elif good.get("name"):
                ambiguous_names.append(str(good.get("name")))

    return cup_count, unique_names(ambiguous_names)


def build_order_summary_lines(orders_data: dict[str, Any]) -> list[str]:
    orders = get_orders_list(orders_data)
    completed_orders = [order for order in orders if order.get("state") == 6]
    drink_count = get_visible_drink_count(orders)
    goods_names = unique_names(collect_order_goods_names(orders))
    coffee_names = [name for name in goods_names if is_coffee_name(name)]
    coffee_cup_count, ambiguous_coffee_names = summarize_coffee_cups(orders)

    lines = [
        f"当前可见订单数：{len(orders)}单。",
        f"已完成订单数：{len(completed_orders)}单。",
        f"可见饮品杯数：{drink_count}杯。",
    ]

    if goods_names:
        lines.append(f"买过的饮品：{'、'.join(goods_names[:10])}。")
    else:
        lines.append("当前没拿到具体饮品名称。")

    if coffee_names:
        lines.append(f"可确认咖啡相关杯数：{coffee_cup_count}杯。")
        if ambiguous_coffee_names:
            lines.append(
                f"混合订单里还有无法精确计杯的咖啡相关饮品：{'、'.join(ambiguous_coffee_names[:10])}。"
            )
        lines.append(
            f"咖啡相关饮品：{len(coffee_names)}项（按商品名初步识别）：{'、'.join(coffee_names[:10])}。"
        )
    else:
        lines.append("当前没识别到咖啡相关饮品；不要据此断言用户一定没喝过咖啡。")

    lines.append("订单信息只能基于本次查询到的订单字段，不能预估、估算或模糊处理。")
    lines.append("回答用户时不要补全本次结果里没有的订单、杯数或商品。")
    return lines


def render_order_query_unavailable(error: Any) -> str:
    return render_text_section(
        "实时数据状态",
        [
            f"订单历史暂时没拿到：{error}",
            "不要猜用户下过几单、买过什么或喝了多少咖啡。",
            "可以请用户稍后重试，或提供小程序绑定手机号后重新查询。",
        ],
    )


def render_missing_mobile() -> str:
    return render_text_section(
        "订单查询",
        [
            "未提供手机号，不能查询订单历史。",
            "请提供微信小程序【新一咖啡】绑定手机号，或在已保存手机号的个性化场景使用缓存手机号。",
        ],
    )


def render_orders_result(orders_data: dict[str, Any]) -> str:
    orders = get_orders_list(orders_data)
    rating_lines = build_order_rating_lines(get_visible_drink_count(orders))
    sections = [
        render_orders_section(orders_data),
        render_text_section("订单摘要", build_order_summary_lines(orders_data)),
    ]
    if rating_lines:
        sections.append(render_text_section("给用户的订单等级", rating_lines))
    return "\n\n".join(sections)


def main() -> int:
    parser = argparse.ArgumentParser(description="按手机号查询新一好喝用户订单")
    parser.add_argument("--mobile", help="用户在【新一咖啡】微信小程序绑定的手机号")
    parser.add_argument(
        "--use-saved-mobile",
        action="store_true",
        help="内部参数：仅订单摘要或口味偏好等明确个性化场景复用本地手机号",
    )
    parser.add_argument(
        "--status",
        type=int,
        choices=(2, 4),
        help="可选订单状态分组；不传查询全部订单，2=正在进行中订单，4=历史订单/已完成订单",
    )
    parser.add_argument("--query", help="用户原始订单问题")
    parser.add_argument("--debug", action="store_true", help="输出调试信息到 stderr")
    args = parser.parse_args()

    resolved_mobile = args.mobile
    if not resolved_mobile and args.use_saved_mobile:
        resolved_mobile = load_mobile()

    if args.mobile:
        debug_log(args.debug, "resolved mobile from cli argument")
    elif args.use_saved_mobile and resolved_mobile:
        debug_log(args.debug, "resolved mobile from local state")
    elif args.use_saved_mobile:
        debug_log(args.debug, "saved mobile requested but not found")
    else:
        debug_log(args.debug, "no mobile resolved; saved mobile not used")

    if not resolved_mobile:
        sys.stdout.write(render_missing_mobile())
        return 0

    config = load_config()
    query = {
        "mobile": resolved_mobile,
        "status": args.status,
    }
    orders_url = build_url(
        config["apiBaseUrl"].rstrip("/"),
        "/skill/xinyi/orders",
        query,
    )
    debug_log(args.debug, f"fetching orders from {orders_url}")

    try:
        orders_response = fetch_json(orders_url, config["timeoutSeconds"])
    except SkillHttpError as exc:
        sys.stdout.write(render_order_query_unavailable(exc))
        return 0

    orders_data = orders_response.get("data", {})
    safe_orders_data = orders_data if isinstance(orders_data, dict) else {}
    sys.stdout.write(render_orders_result(safe_orders_data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
