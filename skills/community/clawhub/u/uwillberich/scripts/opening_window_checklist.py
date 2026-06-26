#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

from capital_flow import (
    attach_flow_tags,
    build_flow_lookup,
    build_group_flow_scoreboard,
    fetch_market_flow_snapshot,
    fetch_top_main_flows,
    render_flow_snapshot,
)
from industry_chain import enrich_event_payload_with_chain_focus
from market_data import fetch_tencent_quotes, format_markdown_table
from market_sentiment import build_sentiment_snapshot


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WATCHLIST = ROOT / "assets" / "default_watchlists.json"
DEFAULT_EVENT_WATCHLIST = Path.home() / ".uwillberich" / "news-iterator" / "event_watchlists.json"
EVENT_CATEGORY_ORDER = ["huge_conflict", "huge_future", "huge_name_release"]
CATEGORY_LABELS = {
    "huge_conflict": "巨大冲突",
    "huge_future": "巨大前景",
    "huge_name_release": "巨头名人",
}
SIGNAL_LABELS = {"high": "高", "medium": "中", "low": "低"}
KEYWORD_LABELS = {
    "war": "战争",
    "oil": "原油",
    "energy": "能源",
    "chips": "芯片",
    "chip": "芯片",
    "robots": "机器人",
    "robot": "机器人",
    "launch": "发布",
    "launches": "发布",
    "announces": "宣布",
    "announce": "宣布",
    "unveils": "亮相",
    "unveil": "亮相",
    "data center": "数据中心",
}

TIME_GATES = [
    {
        "time": "09:00",
        "watch": "LPR and policy timing",
        "bullish": "5Y LPR cut or clearly supportive policy tone",
        "bearish": "No support and policy-sensitive names stay weak",
    },
    {
        "time": "09:20-09:25",
        "watch": "Auction leadership",
        "bullish": "Tech repair groups lead the bid",
        "bearish": "Only oil, coal, banks, or telecom lead",
    },
    {
        "time": "09:30-10:00",
        "watch": "Prior-close reclaim and index support",
        "bullish": "Core leaders reclaim prior close and broad indices stabilize",
        "bearish": "Leaders stay under prior close and defensives dominate",
    },
    {
        "time": "10:00-10:30",
        "watch": "Breadth expansion",
        "bullish": "Repair broadens beyond 2-3 names",
        "bearish": "Bounce stays narrow and fades",
    },
]


def category_display_name(category: str) -> str:
    return CATEGORY_LABELS.get(category, category)


def signal_display_name(signal: str) -> str:
    return SIGNAL_LABELS.get(signal, signal)


def format_keyword_list(keywords: list[str]) -> str:
    if not keywords:
        return "n/a"
    return ", ".join(KEYWORD_LABELS.get(keyword, keyword) for keyword in keywords)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a first-30-minute A-share opening checklist.")
    parser.add_argument(
        "--watchlist",
        default=str(DEFAULT_WATCHLIST),
        help="Path to watchlist JSON. Defaults to the bundled watchlist.",
    )
    parser.add_argument(
        "--groups",
        nargs="+",
        default=["tech_repair", "policy_beta", "defensive_gauge"],
        help="Watchlist groups to score during the opening window.",
    )
    parser.add_argument(
        "--event-watchlist",
        default=str(DEFAULT_EVENT_WATCHLIST),
        help="Path to dynamic event-driven watchlists JSON.",
    )
    parser.add_argument(
        "--skip-event-pools",
        action="store_true",
        help="Do not append event-driven watchlists from the news iterator state.",
    )
    parser.add_argument(
        "--skip-capital-flow",
        action="store_true",
        help="Do not append capital-flow overlays.",
    )
    parser.add_argument(
        "--skip-sentiment",
        action="store_true",
        help="Do not append the market-sentiment overlay.",
    )
    parser.add_argument(
        "--skip-industry-chain",
        action="store_true",
        help="Do not enrich event pools with chain-focus groups.",
    )
    return parser


def load_watchlist(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_event_payload(path: str) -> dict:
    event_path = Path(path)
    if not event_path.exists():
        return {}
    return json.loads(event_path.read_text(encoding="utf-8"))


def build_signal_lookup(watchlist: dict) -> dict[str, dict]:
    lookup: dict[str, dict] = {}
    for items in watchlist.values():
        for item in items:
            symbol = item["symbol"]
            strong_signal = item.get("strong_signal")
            weak_signal = item.get("weak_signal")
            if not strong_signal and not weak_signal:
                continue
            lookup[symbol] = {
                "strong_signal": strong_signal or "",
                "weak_signal": weak_signal or "",
            }
    return lookup


def summarize_group(items: list[dict], quotes: list[dict]) -> dict:
    quote_map = {quote["code"]: quote for quote in quotes}
    above = 0
    below = 0
    flat = 0
    changes = []

    for item in items:
        code = item["symbol"][2:]
        quote = quote_map.get(code)
        if not quote or quote.get("change_pct") is None:
            continue
        changes.append(quote["change_pct"])
        if (quote.get("price") or 0) > (quote.get("prev_close") or 0):
            above += 1
        elif (quote.get("price") or 0) < (quote.get("prev_close") or 0):
            below += 1
        else:
            flat += 1

    avg_change = round(sum(changes) / len(changes), 2) if changes else None
    return {
        "group": "",
        "count": len(items),
        "above_prev_close": above,
        "below_prev_close": below,
        "flat": flat,
        "avg_change_pct": avg_change,
    }


def classify_state(scoreboard: list[dict]) -> str:
    by_name = {row["group"]: row for row in scoreboard}
    tech = by_name.get("tech_repair", {})
    policy = by_name.get("policy_beta", {})
    defensive = by_name.get("defensive_gauge", {})

    tech_above = tech.get("above_prev_close", 0)
    defensive_above = defensive.get("above_prev_close", 0)
    policy_above = policy.get("above_prev_close", 0)

    if tech_above >= 3 and defensive_above <= 2:
        return "State: likely true repair"
    if policy_above >= 2 and tech_above >= 2:
        return "State: likely policy-backed repair"
    if defensive_above >= 3 and tech_above <= 2:
        return "State: likely defensive concentration"
    return "State: mixed or unresolved opening tape"


def build_detail_rows(items: list[dict], quotes: list[dict], signal_lookup: dict[str, dict], flow_lookup: dict[str, dict]) -> list[dict]:
    quote_map = {quote["code"]: quote for quote in quotes}
    rows = []
    for item in items:
        code = item["symbol"][2:]
        quote = quote_map.get(code)
        if not quote:
            continue
        fallback = signal_lookup.get(item["symbol"], {})
        rows.append(
            {
                "name": quote["name"],
                "code": quote["code"],
                "role": item["role"],
                "price": quote["price"],
                "chg%": quote["change_pct"],
                "event_score": item.get("event_score"),
                "trigger_count": item.get("trigger_count"),
                "event_driver": item.get("event_driver", ""),
                "strong_signal": item.get("strong_signal") or fallback.get("strong_signal", ""),
                "weak_signal": item.get("weak_signal") or fallback.get("weak_signal", ""),
            }
        )
    return attach_flow_tags(rows, flow_lookup)


def render_detail_table(rows: list[dict], is_event: bool) -> str:
    columns = [
        ("Name", "name"),
        ("Code", "code"),
        ("Role", "role"),
        ("Price", "price"),
        ("Chg%", "chg%"),
        ("FlowTag", "flow_tag"),
        ("Flow(亿)", "flow_yi"),
    ]
    if is_event:
        columns.extend(
            [
                ("EventScore", "event_score"),
                ("Triggers", "trigger_count"),
                ("Driver", "event_driver"),
            ]
        )
    columns.extend(
        [
            ("Strong Signal", "strong_signal"),
            ("Weak Signal", "weak_signal"),
        ]
    )
    return format_markdown_table(rows, columns)


def render_event_summary(payload: dict) -> None:
    summary = payload.get("summary", [])
    if not summary:
        return
    rows = [
        {
            "category": category_display_name(item["category"]),
            "alert_count": item["alert_count"],
            "total_score": item["total_score"],
            "top_keywords": format_keyword_list(item.get("top_keywords", [])),
        }
        for item in summary
    ]
    print("\n## 事件驱动层总结")
    print(
        format_markdown_table(
            rows,
            [
                ("类别", "category"),
                ("条数", "alert_count"),
                ("总分", "total_score"),
                ("高频关键词", "top_keywords"),
            ],
        )
    )


def render_event_top_alerts(payload: dict) -> None:
    top_alerts = payload.get("top_alerts", {})
    if not top_alerts:
        return
    print("\n## 事件信息源链接")
    for category in EVENT_CATEGORY_ORDER:
        items = top_alerts.get(category, [])
        if not items:
            continue
        print(f"\n### {category_display_name(category)} Top 10 信息源")
        for index, item in enumerate(items, start=1):
            print(f"{index}. [{item['title']}]({item['link']})")
            print(
                f"   - 来源: {item['source']} | 信号: `{signal_display_name(item['signal'])}` | 分值: `{item['score']}`"
            )
            print(f"   - 实体: {', '.join(item.get('entities', [])) or 'n/a'}")
            print(f"   - 关键词: {format_keyword_list(item.get('keywords', []))}")


def render_chain_summary(payload: dict) -> None:
    summary = payload.get("chain_summary", [])
    if not summary:
        return
    rows = [
        {
            "theme": item["theme"],
            "score": item["score"],
            "group": item["group"],
            "reasons": " / ".join(item.get("reasons", [])[:3]) or "n/a",
        }
        for item in summary
    ]
    print("\n## Industry Chain Focus")
    print(
        format_markdown_table(
            rows,
            [
                ("Theme", "theme"),
                ("Score", "score"),
                ("Group", "group"),
                ("Reasons", "reasons"),
            ],
        )
    )


def classify_event_overlay(scoreboard: list[dict]) -> str:
    by_name = {row["group"]: row for row in scoreboard}
    conflict_benefit = by_name.get("event_focus_huge_conflict_benefit", by_name.get("event_focus_huge_conflict", {}))
    conflict_headwind = by_name.get("event_focus_huge_conflict_headwind", {})
    future = by_name.get("event_focus_huge_future", {})
    name_release = by_name.get("event_focus_huge_name_release", {})

    conflict_benefit_above = conflict_benefit.get("above_prev_close", 0)
    conflict_headwind_below = conflict_headwind.get("below_prev_close", 0)
    future_above = future.get("above_prev_close", 0)
    release_above = name_release.get("above_prev_close", 0)

    if conflict_benefit_above >= 4 and conflict_headwind_below >= 3:
        return "Event Overlay: conflict beneficiaries are confirming while compute-power names stay under pressure."
    if future_above >= 4 or release_above >= 4:
        return "Event Overlay: future/big-name news is translating into tradeable technology leadership."
    return "Event Overlay: messages are present, but translation into price action is still mixed."


def classify_opening_bias(scoreboard: list[dict], group_flow_rows: list[dict], sentiment: dict | None) -> str:
    base_read = classify_state(scoreboard)
    if not sentiment:
        return base_read
    by_name = {row["group"]: row for row in group_flow_rows}
    tech_flow = float((by_name.get("tech_repair") or {}).get("net_flow_yi") or 0)
    defensive_flow = float((by_name.get("defensive_gauge") or {}).get("net_flow_yi") or 0)
    if "defensive concentration" in base_read.lower() and sentiment.get("label") == "抱团行情":
        return "Open Read: 抱团行情延续，优先把油气、煤炭、红利当环境锚。"
    if "true repair" in base_read.lower() and tech_flow > 0:
        return "Open Read: 价格与资金共振，科技修复可信度提升。"
    if tech_flow > defensive_flow and sentiment.get("label") in {"科技修复", "修复扩散"}:
        return "Open Read: 资金更偏向成长，优先跟修复扩散而不是防御抱团。"
    return f"Open Read: {sentiment.get('read', base_read)}"


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    watchlist = load_watchlist(args.watchlist)
    event_payload = {} if args.skip_event_pools else load_event_payload(args.event_watchlist)
    if event_payload and not args.skip_industry_chain:
        event_payload = enrich_event_payload_with_chain_focus(
            event_payload,
            watchlist,
            selected_groups=args.groups,
        )
    event_groups = event_payload.get("groups", {})
    signal_lookup = build_signal_lookup(watchlist)
    selected_groups = [group for group in args.groups if group in watchlist]
    selected_event_groups = [group for group in args.groups if group in event_groups]
    if not selected_event_groups and event_groups:
        selected_event_groups = event_payload.get("default_report_groups", [])
    selected_event_groups = list(dict.fromkeys(selected_event_groups))

    all_symbols = []
    for group in selected_groups:
        all_symbols.extend(item["symbol"] for item in watchlist[group])
    for group in selected_event_groups:
        all_symbols.extend(item["symbol"] for item in event_groups.get(group, []))
    quotes = fetch_tencent_quotes(dict.fromkeys(all_symbols))
    flow_lookup: dict[str, dict] = {}
    group_flow_rows: list[dict] = []
    market_flow_rows: list[dict] = []
    if not args.skip_capital_flow:
        market_flow = fetch_market_flow_snapshot()
        inflow_items = fetch_top_main_flows("inflow", limit=8)
        outflow_items = fetch_top_main_flows("outflow", limit=8)
        flow_lookup = build_flow_lookup(inflow_items, outflow_items)
        group_flow_rows = build_group_flow_scoreboard(watchlist, selected_groups, flow_lookup)
        market_flow_rows = render_flow_snapshot(market_flow)
    sentiment = None if args.skip_sentiment else build_sentiment_snapshot(group_flow_rows=group_flow_rows)

    print("# Opening Window Checklist")
    print()
    print("## Time Gates")
    print(
        format_markdown_table(
            TIME_GATES,
            [
                ("Time", "time"),
                ("Watch", "watch"),
                ("Bullish Read", "bullish"),
                ("Bearish Read", "bearish"),
            ],
        )
    )

    scoreboard = []
    for group in selected_groups:
        summary = summarize_group(watchlist[group], quotes)
        summary["group"] = group
        scoreboard.append(summary)

    print("\n## Group Scoreboard")
    print(
        format_markdown_table(
            scoreboard,
            [
                ("Group", "group"),
                ("Count", "count"),
                ("Above Prev Close", "above_prev_close"),
                ("Below Prev Close", "below_prev_close"),
                ("Flat", "flat"),
                ("Avg Chg%", "avg_change_pct"),
            ],
        )
    )

    print("\n## Quick Read")
    print(classify_state(scoreboard))

    if market_flow_rows:
        print("\n## Capital Flow Snapshot")
        print(
            format_markdown_table(
                market_flow_rows,
                [
                    ("State", "label"),
                    ("MainNet(亿)", "main_net_yi"),
                    ("BigInflow(亿)", "big_order_inflow_yi"),
                    ("MediumInflow(亿)", "medium_order_inflow_yi"),
                    ("SmallInflow(亿)", "small_order_inflow_yi"),
                    ("As Of", "as_of"),
                ],
            )
        )

    if group_flow_rows:
        print("\n## Capital Flow Scoreboard")
        print(
            format_markdown_table(
                group_flow_rows,
                [
                    ("Group", "group"),
                    ("InflowHits", "inflow_hits"),
                    ("OutflowHits", "outflow_hits"),
                    ("NetFlow(亿)", "net_flow_yi"),
                    ("Bias", "bias"),
                    ("Leaders", "leaders"),
                ],
            )
        )

    if sentiment:
        print("\n## Sentiment Read")
        print(f"- state: {sentiment['label']}")
        print(f"- read: {sentiment['read']}")
        print(f"- opening_bias: {classify_opening_bias(scoreboard, group_flow_rows, sentiment)}")

    for group in selected_groups:
        rows = build_detail_rows(watchlist[group], quotes, signal_lookup, flow_lookup)
        print(f"\n## Watchlist: {group}")
        print(render_detail_table(rows, is_event=False))

    if event_groups and selected_event_groups:
        render_event_summary(event_payload)
        render_event_top_alerts(event_payload)
        render_chain_summary(event_payload)
        event_scoreboard = []
        for group in selected_event_groups:
            summary = summarize_group(event_groups[group], quotes)
            summary["group"] = group
            event_scoreboard.append(summary)

        print("\n## Event Overlay Scoreboard")
        print(
            format_markdown_table(
                event_scoreboard,
                [
                    ("Group", "group"),
                    ("Count", "count"),
                    ("Above Prev Close", "above_prev_close"),
                    ("Below Prev Close", "below_prev_close"),
                    ("Flat", "flat"),
                    ("Avg Chg%", "avg_change_pct"),
                ],
            )
        )

        print("\n## Event Overlay Read")
        print(classify_event_overlay(event_scoreboard))

        for group in selected_event_groups:
            rows = build_detail_rows(event_groups[group], quotes, signal_lookup, flow_lookup)
            print(f"\n## Event Watchlist: {group}")
            print(render_detail_table(rows, is_event=True))


if __name__ == "__main__":
    main()
