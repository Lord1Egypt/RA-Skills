#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI 入口模块：命令解析 + 2 个命令处理函数 + main 入口。

命令概览：
    ranking [--period day|week|all]  查看大模型调用排行榜（默认日榜+周榜）
    search <keyword>                 在日榜/周榜中查找模型

所有命令支持 --json 参数输出 JSON（供 AI 解析），
不加 --json 时输出 Markdown 表格（供终端阅读）。
"""

import argparse

from config import BASE_URL, PERIODS, PERIOD_ALIAS, VENDOR_NAMES
from utils import http_get, output_error, output_json, output_text, output_stderr
from parser import parse_ranking_html

# 榜单条目在搜索输出中的展示顺序（日榜在前）
LIST_IDS_ORDER = ("day", "week")


def resolve_period(alias):
    """把用户输入的周期别名解析为内部 key（day/week/all），未知别名默认 all。"""
    return PERIOD_ALIAS.get((alias or "all").strip().lower(), "all")


def _load_rankings():
    """请求页面并解析排行榜，网络失败时返回 None。"""
    try:
        html = http_get(BASE_URL)
    except Exception as exc:
        output_stderr(f"⚠️ 请求 {BASE_URL} 失败：{exc}")
        return None
    return parse_ranking_html(html)


def _build_period(items):
    """组装单个周期的输出结构。"""
    return {"count": len(items), "items": items}


def _header(title, updated_at=""):
    """生成文本页头：有更新日期时追加（更新：<日期>）。"""
    return f"{title}（更新：{updated_at}）" if updated_at else title


def _change_display(item):
    """把趋势方向 + 百分比 + 新上榜标记转为展示文本。"""
    if item.get("is_new"):
        return "new"
    arrow = {"up": "↑", "down": "↓"}.get(item.get("trend", ""), "")
    return f"{arrow}{item.get('change', '')}" if arrow else item.get("change", "")


def _vendor_display(vendor):
    """把厂商 slug 转为展示名（中国厂商中文名/海外厂商英文品牌，未知回退原文）。"""
    return VENDOR_NAMES.get(vendor, vendor)


def _render_table(items):
    """把条目列表渲染为 Markdown 表格。"""
    lines = ["| 排名 | 模型 | 厂商 | Tokens | 变动 |",
             "|------|------|------|--------|------|"]
    for it in items:
        lines.append(f"| {it['rank']} | {it['model']} | {_vendor_display(it.get('vendor', ''))} | "
                     f"{it['tokens']} | {_change_display(it)} |")
    return "\n".join(lines)


def _footer(data_source=""):
    """统一数据来源说明：榜单归属证券之星，原始数据来自页面标注的 data_source。"""
    if not data_source:
        return "> 榜单由证券之星科技频道整理"
    src = data_source
    if src.startswith("数据来源："):
        src = src[len("数据来源："):]
    return f"> 榜单由证券之星科技频道整理，数据来源：{src}"


def cmd_ranking(args):
    """查看调用排行榜命令（主命令）。"""
    period = resolve_period(args.period)
    parsed = _load_rankings()
    if parsed is None:
        output_error("网络请求失败，请稍后重试。")
        return

    keys = list(PERIODS.keys()) if period == "all" else [period]
    periods = {PERIODS[k]["name"]: _build_period(parsed.get(k, [])) for k in keys}
    if not any(p["items"] for p in periods.values()):
        output_error("未获取到排行榜数据，请稍后重试。")
        return

    if args.json:
        output_json({
            "source": BASE_URL,
            "data_source": parsed.get("data_source", ""),
            "updated_at": parsed.get("updated_at", ""),
            "periods": periods,
            "status": "success",
        })
    else:
        parts = [_header("📊 大模型调用排行榜", parsed.get("updated_at", "")), ""]
        for name, p in periods.items():
            parts.append(f"### {name}（{p['count']} 条）")
            parts.append(_render_table(p["items"]))
            parts.append("")
        parts.append(_footer(parsed.get("data_source", "")))
        output_text("\n".join(parts))


def cmd_search(args):
    """在日榜/周榜中查找模型命令（辅助功能）。"""
    keyword = args.keyword.strip()
    if not keyword:
        output_error("请输入要查找的模型关键词。")
        return
    parsed = _load_rankings()
    if parsed is None:
        output_error("网络请求失败，请稍后重试。")
        return

    kw = keyword.lower()
    matches = []
    for k in LIST_IDS_ORDER:
        for it in parsed.get(k, []):
            vendor = it.get("vendor", "")
            vendor_cn = _vendor_display(vendor).lower()
            if kw in it["model"].lower() or kw in vendor.lower() or kw in vendor_cn:
                matches.append({"period": PERIODS[k]["name"], "rank": it["rank"],
                                "model": it["model"], "vendor": vendor,
                                "tokens": it["tokens"], "change": it["change"],
                                "trend": it["trend"], "is_new": it["is_new"]})
    if args.json:
        output_json({
            "source": BASE_URL,
            "data_source": parsed.get("data_source", ""),
            "updated_at": parsed.get("updated_at", ""),
            "keyword": keyword,
            "matches": matches,
            "status": "success",
        })
        return
    if not matches:
        output_text(f"未找到与 \"{keyword}\" 匹配的模型。")
        return
    parts = [_header(f"🔍 在调用排行榜中搜索 \"{keyword}\"：",
                     parsed.get("updated_at", "")), ""]
    for m in matches:
        mark = "（新上榜）" if m["is_new"] else ""
        vendor = f"，厂商 {_vendor_display(m['vendor'])}" if m["vendor"] else ""
        parts.append(f"- {m['period']} 第 {m['rank']} 名：{m['model']}{vendor}，"
                     f"Tokens {m['tokens']}，变动 {_change_display(m)}{mark}")
    parts.append("")
    parts.append(_footer(parsed.get("data_source", "")))
    output_text("\n".join(parts))


def main():
    """CLI 主入口：构建参数解析器、解析参数、路由到对应命令处理函数。"""
    parser = argparse.ArgumentParser(
        description="证券之星大模型调用排行榜查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python cli.py ranking --json                 # 查看日榜+周榜（JSON输出）
  python cli.py ranking --period week          # 只看周榜
  python cli.py ranking --period 日             # 支持中英文别名
  python cli.py search DeepSeek --json         # 在双榜中查找模型
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    p_ranking = subparsers.add_parser("ranking", help="查看大模型调用排行榜（日榜+周榜）")
    p_ranking.add_argument("--period", "-p", default="all",
                           help="周期筛选：day/week/all 或 日/周/全部（默认 all）")
    p_ranking.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    p_search = subparsers.add_parser("search", help="在日榜/周榜中查找模型（辅助功能）")
    p_search.add_argument("keyword", help="模型名或厂商关键词（支持中文厂商名，如\"小米\"）")
    p_search.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    commands = {
        "ranking": cmd_ranking,
        "search": cmd_search,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()