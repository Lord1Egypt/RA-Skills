#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys

from build_response import (
    ACTIVITY_GIFT_SUMMARY,
    is_activity_query,
    is_order_query,
    render_recommendation_context,
    render_recommendation_unavailable,
)
from skill_config import load_config
from skill_http import SkillHttpError, build_url, fetch_json, make_debug_logger
from user_state import (
    clear_mobile,
    load_activity_joined,
    load_mobile,
    load_state,
)


debug_log = make_debug_logger("recommend_drink")

PERSONALIZED_RECOMMENDATION_KEYWORDS = (
    "我的口味",
    "我的偏好",
    "我常点",
    "我经常点",
    "我不常点",
    "没喝过",
    "未喝过",
    "没点过",
    "未点过",
    "根据我",
    "适合我",
    "个性化",
    "推荐尝试",
)

# 仅活动总览、订单或明确个性化推荐这类场景才允许复用本地缓存手机号。
# 普通推荐、菜单、热量查询不在此列；缺关键词时即使加了 --use-saved-mobile 也不发送手机号，
# 防止 Agent 误调时把缓存手机号扩散到普通菜单查询。


def matches_personalized_recommendation_query(args) -> bool:
    text = " ".join(
        str(value or "")
        for value in (args.query, args.scene, args.preference)
    )
    return any(keyword in text for keyword in PERSONALIZED_RECOMMENDATION_KEYWORDS)


def is_personalized_query(args) -> bool:
    context = {
        "query": args.query,
        "scene": args.scene,
        "preference": args.preference,
    }
    return (
        is_activity_query(context)
        or is_order_query(context)
        or matches_personalized_recommendation_query(args)
    )


def render_mobile_status(candidate_mobile: str | None = None) -> str:
    state = load_state()
    mobile = state.get("mobile")
    if not isinstance(mobile, str) or not mobile.strip():
        lines = ["本地未保存新一咖啡手机号。"]
        if candidate_mobile:
            lines.extend(
                [
                    f"候选手机号：{candidate_mobile}",
                    "本地没有可对比的参与状态；如需向后端查询或领取礼包，需要用户明确确认后再走领取流程。",
                ]
            )
        return "\n".join(lines) + "\n"

    activity_joined = state.get("activityJoined")
    if activity_joined is True:
        activity_label = "已领取过"
    elif activity_joined is False:
        activity_label = "未参与"
    else:
        activity_label = "未确认"

    lines = [
        f"本地已保存手机号：{mobile}",
        f"活动状态：{activity_label}",
    ]
    updated_at = state.get("updatedAt")
    if updated_at:
        lines.append(f"缓存更新时间：{updated_at}")
    if activity_joined is True:
        lines.append(f"已领取内容：{ACTIVITY_GIFT_SUMMARY}")

    if candidate_mobile:
        lines.append(f"候选手机号：{candidate_mobile}")
        if candidate_mobile == mobile:
            lines.append("候选手机号与本地保存手机号一致。")
        elif activity_joined is True:
            lines.append("本机缓存已确认当前手机号参与活动，不能更换手机号重复领取。")
        else:
            lines.append("候选手机号与本地保存手机号不同；本地未确认已参与。")
            lines.append("如需向后端同步或领取礼包，需要用户明确确认后再走领取流程。")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="获取聚合推荐上下文，并整理成可直接提供给大模型的文本/表格"
    )
    parser.add_argument("--mobile", help="可选手机号，用于个性化推荐")
    parser.add_argument(
        "--use-saved-mobile",
        action="store_true",
        help="内部参数：仅在活动总览或明确个性化推荐场景复用本地手机号",
    )
    parser.add_argument(
        "--clear-mobile",
        action="store_true",
        help="清空已保存的手机号，下次不再自动带出",
    )
    parser.add_argument(
        "--show-mobile-status",
        action="store_true",
        help="只读取本地缓存手机号和活动状态，不请求后端",
    )
    parser.add_argument("--candidate-mobile", help="只读换号预检候选手机号，不请求后端")
    parser.add_argument("--query", help="用户问题或饮品名称")
    parser.add_argument("--scene", help="场景，如提神、下午茶、轻负担")
    parser.add_argument("--preference", help="偏好，如咖啡、茶、低卡")
    parser.add_argument("--debug", action="store_true", help="输出调试信息到 stderr")
    args = parser.parse_args()

    if args.clear_mobile:
        clear_mobile()
        debug_log(args.debug, "cleared saved mobile")
        sys.stdout.write("已清空本地手机号缓存和活动状态。\n")
        return 0

    if args.show_mobile_status:
        debug_log(args.debug, "showing saved mobile status from local state")
        sys.stdout.write(render_mobile_status(args.candidate_mobile))
        return 0

    resolved_mobile = args.mobile
    saved_mobile_skipped_for_generic_query = False
    if not resolved_mobile and args.use_saved_mobile:
        if is_personalized_query(args):
            resolved_mobile = load_mobile()
        else:
            saved_mobile_skipped_for_generic_query = True

    if args.mobile:
        debug_log(args.debug, "resolved mobile from cli argument")
    elif saved_mobile_skipped_for_generic_query:
        debug_log(
            args.debug,
            "saved mobile not reused: query is not activity/order/personalized",
        )
    elif args.use_saved_mobile and resolved_mobile:
        debug_log(args.debug, "resolved mobile from local state")
    elif args.use_saved_mobile:
        debug_log(args.debug, "saved mobile requested but not found")
    else:
        debug_log(args.debug, "no mobile resolved; saved mobile not used")

    config = load_config()
    base_url = config["apiBaseUrl"].rstrip("/")
    timeout = config["timeoutSeconds"]

    context_url = build_url(
        base_url,
        "/skill/xinyi/context",
        {"mobile": resolved_mobile},
    )
    debug_log(args.debug, f"fetching context from {context_url}")
    try:
        context_response = fetch_json(context_url, timeout)
    except SkillHttpError as exc:
        sys.stdout.write(render_recommendation_unavailable(exc))
        return 0
    context_data = context_response.get("data", {})

    weather_data = context_data.get("weather")
    debug_log(
        args.debug,
        "context includes weather data" if weather_data is not None else "context missing weather; using generic recommendation copy",
    )

    mobile_from_store = bool(
        resolved_mobile and args.use_saved_mobile and not args.mobile
    )
    rendered_context = render_recommendation_context(
        context={
            "mobile": resolved_mobile,
            "mobileFromStore": mobile_from_store,
            "preference": args.preference,
            "query": args.query,
            "scene": args.scene,
            "activityJoined": load_activity_joined(resolved_mobile),
        },
        goods=context_data.get("goods", []),
        weather=weather_data,
        orders=context_data.get("orders"),
    )

    sys.stdout.write(rendered_context)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
