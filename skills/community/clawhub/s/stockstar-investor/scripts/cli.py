#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI 入口模块：命令解析 + 4 个命令处理函数 + main 入口。

本模块负责：
- 定义 argparse 参数解析器，支持 signals/qa/tags/search 四个子命令
- 每个 cmd_* 函数对应一个子命令，负责：调用 API → 解析数据 → 格式化输出
- main() 函数是脚本起点，路由命令到对应的处理函数

命令概览：
    signals <stock_code>             查看线索挖掘（结构化投资信号）
    qa <stock_code>                  查看投资者互动原始问答
    qa <stock_code> --domain --tag   按标签筛选问答
    tags <stock_code>                查看可用标签列表
    search <keyword>                 模糊搜索股票
"""

import argparse
import datetime
import json
import re
import sys

from config import DOMAIN_MAP, DOMAIN_NAME_MAP, IMPORTANCE_WEIGHT, SENTIMENT_MAP, REPLY_TYPE_MAP
from utils import output_json, output_error, output_text, normalize_stock_id
from api import fetch_qa, fetch_qa_by_tag, fetch_tag_stats, fetch_signal_page, search_stock
from parser import parse_signal_page


def cmd_signals(args):
    """
    查看线索挖掘命令。

    抓取信号页面 HTML 并解析为结构化信号列表，
    按重要性排序展示。

    参数：
        args: argparse 命名空间，包含 stock_code, json
    """
    code = args.stock_code
    stockid = normalize_stock_id(code)

    try:
        html = fetch_signal_page(code)
    except SystemExit:
        output_error(f"无法获取股票 {code} 的线索挖掘数据。")
        return

    data = parse_signal_page(html)

    if not data["signals"]:
        if args.json:
            output_json({
                "stock_name": data["stock_name"],
                "stock_code": data["stock_code"],
                "signals": [],
                "hint": f"该股票暂无结构化线索数据，建议使用 qa 命令查看原始问答。",
            })
        else:
            name = data["stock_name"] or code
            output_text(f"📡 {name} ({data['stock_code'] or code}) — 暂无线索数据\n")
            output_text("该股票暂无结构化线索。建议使用 qa 命令查看原始投资者互动问答。")
        return

    # 按重要性排序
    sorted_signals = sorted(
        data["signals"],
        key=lambda s: IMPORTANCE_WEIGHT.get(s.get("importance", ""), 0),
        reverse=True
    )

    if args.json:
        output_json({
            "stock_name": data["stock_name"],
            "stock_code": data["stock_code"],
            "signals": sorted_signals,
        })
    else:
        name = data["stock_name"] or code
        code_display = data["stock_code"] or code
        lines = [f"📡 {name} ({code_display}) — 线索挖掘", ""]

        current_importance = ""
        for sig in sorted_signals:
            imp = sig.get("importance", "")
            if imp != current_importance:
                current_importance = imp
                lines.append(f"【{imp}重要性】" if imp else "【未知】")

            sig_name = sig.get("name", "")
            category = sig.get("category", "")
            change_type = sig.get("change_type", "")
            summary = sig.get("summary", "")
            timeline = sig.get("timeline", [])

            lines.append(f"• {sig_name}（{category} / {change_type}）")
            if summary:
                lines.append(f"  {summary}")
            if timeline:
                latest = timeline[0]
                date_range = f"{timeline[-1].get('date', '')} → {timeline[0].get('date', '')}" if len(timeline) > 1 else latest.get("date", "")
                lines.append(f"  时间：{date_range}")
            lines.append("")

        output_text("\n".join(lines))


def cmd_qa(args):
    """
    查看投资者互动原始问答命令。

    支持四种模式：
    1. 默认：分页查看所有问答
    2. 按领域筛选：仅 --domain，客户端过滤（分页基于全量数据）
    3. 按标签筛选：仅 --tag，自动发现所属领域后服务端过滤（分页准确）
    4. 精确筛选：--domain + --tag 同时传入，服务端过滤（分页准确）

    参数：
        args: argparse 命名空间，包含 stock_code, page, domain, tag, json
    """
    code = args.stock_code
    page = args.page
    filter_info = {}

    if args.domain and args.tag:
        # 模式4：两者都有 → 服务端过滤
        domain = DOMAIN_MAP.get(args.domain)
        if not domain:
            output_error(f"无效的领域：{args.domain}。可用：热点题材/业务运营/公司治理/风险提示/财务能力")
            return
        filter_info = {"domain": DOMAIN_NAME_MAP.get(domain, domain), "tag": args.tag}
        try:
            result = fetch_qa_by_tag(code, domain, args.tag, page)
        except SystemExit:
            output_error(f"无法获取标签筛选数据。")
            return

    elif args.tag and not args.domain:
        # 模式3：仅 tag → 先发现 domain 再服务端过滤
        filter_info = {"tag": args.tag}
        try:
            tag_stats = fetch_tag_stats(code, "all")
        except SystemExit:
            output_error(f"无法获取股票 {code} 的标签数据。")
            return
        discovered_domain = None
        for t in tag_stats:
            if t.get("TAG_NAME") == args.tag:
                discovered_domain = t.get("TAG_DOMAIN")
                break
        if discovered_domain:
            filter_info["domain"] = DOMAIN_NAME_MAP.get(discovered_domain, discovered_domain)
            try:
                result = fetch_qa_by_tag(code, discovered_domain, args.tag, page)
            except SystemExit:
                output_error(f"无法获取标签筛选数据。")
                return
        else:
            # tag 不在 stats 中 → 客户端兜底过滤
            try:
                result = fetch_qa(code, page)
            except SystemExit:
                output_error(f"无法获取股票 {code} 的问答数据。")
                return
            result["items"] = [
                item for item in result["items"]
                if any(t.get("TAG_NAME") == args.tag for t in item.get("DOMAIN_TAGS", []))
            ]

    elif args.domain and not args.tag:
        # 模式2：仅 domain → 客户端过滤
        domain = DOMAIN_MAP.get(args.domain)
        if not domain:
            output_error(f"无效的领域：{args.domain}。可用：热点题材/业务运营/公司治理/风险提示/财务能力")
            return
        filter_info = {"domain": DOMAIN_NAME_MAP.get(domain, domain)}
        try:
            result = fetch_qa(code, page)
        except SystemExit:
            output_error(f"无法获取股票 {code} 的问答数据。")
            return
        result["items"] = [
            item for item in result["items"]
            if any(t.get("TAG_DOMAIN") == domain for t in item.get("DOMAIN_TAGS", []))
        ]

    else:
        # 模式1：全量
        try:
            result = fetch_qa(code, page)
        except SystemExit:
            output_error(f"无法获取股票 {code} 的问答数据。")
            return

    items = result["items"]
    stock_name = result["stock_name"]
    stock_code = result["stock_code"]
    has_more = result["has_more"]

    # 构建筛选标注文本
    if filter_info:
        parts = []
        if "domain" in filter_info:
            parts.append(filter_info["domain"])
        if "tag" in filter_info:
            parts.append(filter_info["tag"])
        filter_label = "筛选：" + "/".join(parts)
    else:
        filter_label = ""

    if not items:
        if args.json:
            output_data = {
                "stock_name": stock_name,
                "stock_code": stock_code,
                "page": page,
                "items": [],
                "has_more": False,
            }
            if filter_info:
                output_data["filter"] = filter_info
            output_json(output_data)
        else:
            name = stock_name or code
            hint = f"（{filter_label}）" if filter_label else ""
            output_text(f"📋 {name} ({stock_code or code}) — 暂无问答数据{hint}\n")
        return

    if args.json:
        json_items = []
        for item in items:
            tags = []
            for t in item.get("DOMAIN_TAGS", []):
                tags.append({
                    "name": t.get("TAG_NAME", ""),
                    "domain": t.get("TAG_DOMAIN", ""),
                    "snippet": t.get("REFERENCE_SNIPPET", ""),
                })

            json_items.append({
                "id": item.get("IRM_QUEST_ID"),
                "question": item.get("QUEST", ""),
                "answer": item.get("REPLY", ""),
                "source": item.get("SOURCE", ""),
                "ask_time": _format_date(item.get("QUEST_TIME", "")),
                "reply_time": _format_date(item.get("REPLY_TIME", "")),
                "tags": tags,
                "sentiment": item.get("SENTIMENT"),
                "reply_type": item.get("REPLY_TYPE"),
                "detail_url": f"https://stock.stockstar.com/dmhd/detail/{item.get('IRM_QUEST_ID', '')}",
            })

        output_data = {
            "stock_name": stock_name,
            "stock_code": stock_code,
            "page": page,
            "items": json_items,
            "has_more": has_more,
        }
        if filter_info:
            output_data["filter"] = filter_info
        output_json(output_data)
    else:
        name = stock_name or code
        header = f"📋 {name} ({stock_code or code}) — 投资者互动 (第{page}页)"
        if filter_label:
            header += f"（{filter_label}）"
        lines = [header, ""]

        for i, item in enumerate(items, 1):
            ask_time = _format_date(item.get("QUEST_TIME", ""))
            reply_time = _format_date(item.get("REPLY_TIME", ""))
            question = item.get("QUEST", "")
            answer = item.get("REPLY", "")
            source = item.get("SOURCE", "")
            sentiment = SENTIMENT_MAP.get(item.get("SENTIMENT"), "")
            reply_type = REPLY_TYPE_MAP.get(item.get("REPLY_TYPE"), "")

            # 截断过长内容
            q_display = question[:150] + "..." if len(question) > 150 else question
            a_display = answer[:200] + "..." if len(answer) > 200 else answer

            tags = []
            for t in item.get("DOMAIN_TAGS", []):
                tag_name = t.get("TAG_NAME", "")
                tag_domain = DOMAIN_NAME_MAP.get(t.get("TAG_DOMAIN", ""), "")
                if tag_name:
                    tags.append(f"{tag_name}" + (f"({tag_domain})" if tag_domain else ""))

            lines.append(f"{i}. [{ask_time}] 问：{q_display}")
            lines.append(f"   答：{a_display}")
            tag_str = " | ".join(tags[:5])
            attr_parts = []
            if sentiment:
                attr_parts.append(f"语义：{sentiment}")
            if reply_type:
                attr_parts.append(f"质量：{reply_type}")
            if source:
                attr_parts.append(f"来源：{source}")
            if tag_str:
                lines.append(f"   标签：{tag_str}")
            if attr_parts:
                lines.append(f"   {' | '.join(attr_parts)}")
            lines.append("")

        if has_more:
            footer = f"提示：使用 --page {page + 1} 查看下一页"
        else:
            footer = "已到最后一页"
        lines.append(footer)

        output_text("\n".join(lines))


def cmd_search(args):
    """
    模糊搜索股票命令。

    参数：
        args: argparse 命名空间，包含 keyword, json
    """
    keyword = args.keyword.strip()
    candidates = search_stock(keyword)

    if not candidates:
        output_json({
            "keyword": keyword,
            "candidates": [],
            "hint": f"未找到 \"{keyword}\"。建议：① 使用完整名称如\"贵州茅台\" ② 使用股票代码如\"600519\""
        })
        return

    if args.json:
        output_json({"keyword": keyword, "candidates": candidates[:15]})
    else:
        lines = [f'🔍 搜索 "{keyword}" 的结果：']
        for i, c in enumerate(candidates[:10], 1):
            code = c.get("code", "")
            name = c.get("name", "")
            lines.append(f"  {i}. {name} ({code})")
        if len(candidates) > 10:
            lines.append(f"  ... 及 {len(candidates) - 10} 条更多结果")
        lines.append("可使用股票代码继续查询。")
        output_text("\n".join(lines))


def cmd_tags(args):
    """
    查看可用标签列表命令。

    返回该股票在投资者互动中被标注的所有领域标签，按领域分组。
    用户可据此选择 --domain 和 --tag 值用于 qa 命令的标签筛选。

    参数：
        args: argparse 命名空间，包含 stock_code, domain, json
    """
    code = args.stock_code
    domain = args.domain or "all"

    try:
        tags = fetch_tag_stats(code, domain)
    except SystemExit:
        output_error(f"无法获取股票 {code} 的标签数据。")
        return

    if not tags:
        if args.json:
            output_json({
                "stock_code": code,
                "domain": domain,
                "tags": [],
            })
        else:
            output_text(f"🏷️ {code} — 暂无标签数据")
        return

    if args.json:
        json_tags = []
        for t in tags:
            tag_domain = t.get("TAG_DOMAIN", "")
            json_tags.append({
                "name": t.get("TAG_NAME", ""),
                "domain": tag_domain,
                "domain_name": DOMAIN_NAME_MAP.get(tag_domain, ""),
                "count": t.get("TAG_COUNT", 0),
            })
        output_json({
            "stock_code": code,
            "domain": domain,
            "tags": json_tags,
        })
    else:
        lines = [f"🏷️ {code} — 可用标签", ""]
        current_domain = ""
        for t in tags:
            tag_domain = t.get("TAG_DOMAIN", "")
            domain_name = DOMAIN_NAME_MAP.get(tag_domain, tag_domain)
            if domain_name != current_domain:
                current_domain = domain_name
                lines.append(f"【{domain_name}】")
            tag_name = t.get("TAG_NAME", "")
            count = t.get("TAG_COUNT", 0)
            lines.append(f"  • {tag_name} ({count}条)")
        lines.append("")
        lines.append("可用 qa --domain <领域> --tag <标签名> 筛选问答。")
        output_text("\n".join(lines))


def _format_date(date_str):
    """将 /Date(1779423720000)/ 格式转为 YYYY-MM-DD（固定 UTC+8 北京时间）"""
    if not date_str:
        return ""
    match = re.search(r'/Date\((\d+)\)/', date_str)
    if match:
        ts = int(match.group(1)) / 1000
        tz = datetime.timezone(datetime.timedelta(hours=8))
        try:
            dt = datetime.datetime.fromtimestamp(ts, tz=tz)
            return dt.strftime("%Y-%m-%d")
        except (OSError, ValueError):
            return ""
    return date_str


def main():
    """
    CLI 主入口：构建参数解析器、解析参数、路由到对应命令处理函数。

    支持 4 个子命令：
        signals    — 线索挖掘（结构化投资信号）
        qa         — 投资者互动原始问答
        tags       — 查看可用标签列表
        search     — 模糊搜索股票
    """
    parser = argparse.ArgumentParser(
        description="证券之星投资者互动查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python cli.py signals 600000              # 查看浦发银行线索挖掘
  python cli.py qa 600000                   # 查看浦发银行投资者互动问答
  python cli.py qa 600000 --domain govern --tag 市值管理  # 按标签筛选
  python cli.py tags 600000                 # 查看浦发银行可用标签
  python cli.py search 浦发                 # 搜索股票
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # signals 子命令：线索挖掘
    p_signals = subparsers.add_parser("signals", help="查看线索挖掘（结构化投资信号）")
    p_signals.add_argument("stock_code", help="股票代码（如 600000、000001）")
    p_signals.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    # qa 子命令：投资者互动问答
    p_qa = subparsers.add_parser("qa", help="查看投资者互动原始问答")
    p_qa.add_argument("stock_code", help="股票代码（如 600000、000001）")
    p_qa.add_argument("--page", type=int, default=1, help="页码（默认 1）")
    p_qa.add_argument("--domain", help="标签领域（热点题材/业务运营/公司治理/风险提示/财务能力）")
    p_qa.add_argument("--tag", help="标签名称（需与 --domain 同时使用）")
    p_qa.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    # search 子命令：模糊搜索
    p_search = subparsers.add_parser("search", help="模糊搜索股票")
    p_search.add_argument("keyword", help="股票名称或代码关键词")
    p_search.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    # tags 子命令：查看可用标签
    p_tags = subparsers.add_parser("tags", help="查看可用标签列表")
    p_tags.add_argument("stock_code", help="股票代码（如 600000、000001）")
    p_tags.add_argument("--domain", help="标签领域（热点题材/业务运营/公司治理/风险提示/财务能力）")
    p_tags.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    commands = {
        "signals": cmd_signals,
        "qa": cmd_qa,
        "tags": cmd_tags,
        "search": cmd_search,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
