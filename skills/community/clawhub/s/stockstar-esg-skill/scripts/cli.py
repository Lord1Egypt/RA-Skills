#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI 入口模块：命令解析 + 5 个命令处理函数 + main 入口。

本模块负责：
- 定义 argparse 参数解析器，支持 search/query/detail/compare/list 五个子命令（list 为辅助功能）
- 每个 cmd_* 函数对应一个子命令，负责：调用 API → 解析数据 → 格式化输出
- main() 函数是脚本起点，路由命令到对应的处理函数

命令概览：
    search <keyword>    模糊搜索股票（名称/代码/拼音）
    query <stock_code>  查询个股 ESG 综合评级（三家机构）
    detail <stock_code> 查询个股 ESG 详细评分（含 E/S/G 三维度）
    compare <code...>   对比多只股票的 ESG 评级
    list --provider <p> 浏览评级列表（辅助功能）
"""

import argparse
import json
import re
import sys

from config import PROVIDERS, PROVIDER_ALIAS, PROVIDER_NAME_MAP
from utils import output_json, output_error, output_text, normalize_name
from api import fetch_detail, fetch_list, search_by_suggest, search_in_list, search_heuristic
from parser import parse_detail_html


def cmd_search(args):
    """
    模糊搜索股票命令。

    搜索策略（三级降级）：
        1. 纯 5~6 位数字 → 直接请求详情页验证
        2. 非纯数字 → suggest API（支持代码/全称/拼音）
        3. suggest 无结果 → 列表扫描（遍历华证+妙盈列表 API 逐页匹配）
        4. 列表也无结果 → 试探式搜索（提取数字当作代码尝试）

    参数：
        args: argparse 命名空间，包含 keyword, json 等字段

    输出：
        JSON（--json 时）或 文本表格
    """
    keyword = args.keyword.strip()
    candidates = []

    # 策略 1：输入是纯 5~6 位数字时优先当作股票代码验证
    if re.match(r'^\d{5,6}$', keyword):
        html = fetch_detail(keyword)
        data = parse_detail_html(html)
        name = data.get("stock_name", "")
        code = data.get("stock_code", "")
        if name and code:
            # 详情页验证通过，直接返回该股票
            candidates.append({
                "name": name,
                "code": code,
                "source": "exact_code"
            })
        else:
            # 详情页查不到，回退到 suggest API
            candidates = search_by_suggest(keyword)
    else:
        # 策略 2：通过 suggest API 搜索
        candidates = search_by_suggest(keyword)
        # 策略 3：suggest 无结果，通过列表扫描
        if not candidates:
            candidates = search_in_list(keyword)
        # 策略 4：列表也找不到，试探式提取数字
        if not candidates:
            candidates = search_heuristic(keyword)

    if not candidates:
        output_json({
            "keyword": keyword,
            "candidates": [],
            "hint": f"未找到 \"{keyword}\"。建议：① 使用完整名称如\"贵州茅台\" ② 使用股票代码如\"600519\" ③ 使用拼音首字母"
        })
        return

    if args.json:
        output_json({"keyword": keyword, "candidates": candidates[:15]})
    else:
        # 文本模式下展示候选列表，供用户选择
        print(f"🔍 搜索 \"{keyword}\" 的结果：")
        for i, c in enumerate(candidates[:10], 1):
            code = c.get("code", "")
            name = c.get("name", "")
            print(f"  {i}. {name} ({code})")
        if len(candidates) > 10:
            print(f"  ... 及 {len(candidates) - 10} 条更多结果")
        print("可使用股票代码继续查询 ESG 评级。")


def _validate_code(code):
    """检查输入是否为有效的股票代码（5-6 位数字）"""
    if not re.match(r'^\d{5,6}$', code):
        output_error(f"\"{code}\" 不是有效的股票代码。请使用 search 命令先搜索名称，或用 5-6 位数字代码。")
        return False
    return True


def _strip_json(data):
    """JSON 输出时剥离 ranks/rates，只保留 rate+date+E/S/G 评分"""
    result = {
        "stock_name": data.get("stock_name", ""),
        "stock_code": data.get("stock_code", ""),
    }
    for name in PROVIDER_NAME_MAP.values():
        prov = data.get(name, {})
        result[name] = {
            k: prov.get(k, "") for k in ("rate", "date", "e_score", "s_score", "g_score")
        }
    return result


def cmd_query(args):
    """
    查询个股 ESG 综合评级命令。

    从详情页提取三家机构的综合评级等级和日期，
    快速呈现 ESG 概览。

    参数：
        args: argparse 命名空间，包含 stock_code, json 等字段

    输出：
        JSON（--json 时）或 Markdown 表格
    """
    code = args.stock_code
    if not _validate_code(code):
        return
    html = fetch_detail(code)
    data = parse_detail_html(html)
    # 如果妙盈和华证都没有数据，认为该股票无 ESG 覆盖
    prov_names = list(PROVIDER_NAME_MAP.values())
    if not data.get(prov_names[0], {}).get("rate") and not data.get(prov_names[1], {}).get("rate"):
        output_error(f"未找到股票 {code} 的 ESG 评级数据。")
        return

    if args.json:
        output_json(_strip_json(data))
    else:
        lines = []
        name = data.get("stock_name", "")
        code = data.get("stock_code", "")
        lines.append(f"📊 {name} ({code}) — ESG 评级")
        lines.append("")
        lines.append("| 评级机构 | 综合评级 | 评级日期 |")
        lines.append("|---------|---------|---------|")
        for name_key in PROVIDER_NAME_MAP.values():
            d = data.get(name_key, {})
            rate = d.get("rate", "")
            date = d.get("date", "")
            if rate:
                lines.append(f"| {name_key} | {rate} | {date} |")
        if len(lines) <= 3:
            output_error(f"未找到股票 {code} 的 ESG 评级数据。")
            return
        lines.append("")
        lines.append("> 数据来源：证券之星 ESG")
        output_text("\n".join(lines))


def cmd_detail(args):
    """
    查询个股 ESG 详细评分命令。

    在 query 的基础上，进一步展示每家机构的 E(环境)/S(社会)/G(治理)
    三维度的评分、评级和行业排名。

    各机构的数据详细程度不同：
        - 妙盈：有 E/S/G 评分（百分制数值）
        - 华证：有评分 + 评级字母 + 行业排名（如 5/29）
        - 商道融绿：仅有综合评级，无 E/S/G 维度数据

    参数：
        args: argparse 命名空间，包含 stock_code, json 等字段

    输出：
        JSON（--json 时）或 Markdown 按机构分组的详细报告
    """
    code = args.stock_code
    if not _validate_code(code):
        return
    html = fetch_detail(code)
    data = parse_detail_html(html)
    prov_names = list(PROVIDER_NAME_MAP.values())
    if not data.get(prov_names[0], {}).get("rate") and not data.get(prov_names[1], {}).get("rate"):
        output_error(f"未找到股票 {code} 的 ESG 评级数据。")
        return

    if args.json:
        output_json(_strip_json(data))
    else:
        parts = []
        name = data.get("stock_name", "")
        code = data.get("stock_code", "")
        parts.append(f"📊 {name} ({code}) — ESG 详细评分")
        parts.append("")
        # 先展示综合评级摘要
        parts.append("| 评级机构 | 综合评级 | 评级日期 |")
        parts.append("|---------|---------|---------|")
        for name_key in PROVIDER_NAME_MAP.values():
            d = data.get(name_key, {})
            rate = d.get("rate", "")
            date = d.get("date", "")
            if rate:
                parts.append(f"| {name_key} | {rate} | {date} |")
        parts.append("")

        # 再按机构展示 E/S/G 三维度详情
        for name_key in PROVIDER_NAME_MAP.values():
            d = data.get(name_key, {})
            rate = d.get("rate", "")
            date = d.get("date", "")
            if not rate:
                continue

            parts.append(f"### {name_key} — {rate}（{date}）")
            if name_key == PROVIDER_NAME_MAP["chindices"]:
                # 华证最详细：评分 + 评级 + 排名
                parts.append("| 维度 | 评分 | 评级 | 行业排名 |")
                parts.append("|------|------|------|---------|")
                parts.append(f"| 环境(E) | {d.get('e_score', '')} | {d.get('e_rate', '')} | {d.get('e_rank', '')} |")
                parts.append(f"| 社会(S) | {d.get('s_score', '')} | {d.get('s_rate', '')} | {d.get('s_rank', '')} |")
                parts.append(f"| 治理(G) | {d.get('g_score', '')} | {d.get('g_rate', '')} | {d.get('g_rank', '')} |")
            elif name_key == PROVIDER_NAME_MAP["syntaogf"]:
                # 商道融绿只有综合评级
                parts.append("> 商道融绿仅提供综合评级，不提供 E/S/G 维度评分。")
            else:
                # 妙盈有评分但没有评级字母和排名
                parts.append("| 维度 | 评分 |")
                parts.append("|------|------|")
                parts.append(f"| 环境(E) | {d.get('e_score', '')} |")
                parts.append(f"| 社会(S) | {d.get('s_score', '')} |")
                parts.append(f"| 治理(G) | {d.get('g_score', '')} |")
            parts.append("")

        output_text("\n".join(parts))


def cmd_compare(args):
    """
    多股 ESG 评级对比命令。

    同时查询多只股票的 ESG 评级，以对比表格形式展示。
    限制每次最多对比 5 只，超出时自动截断并警告。

    参数：
        args: argparse 命名空间，包含 stock_codes, json 等字段

    输出：
        JSON（--json 时）或 Markdown 对比表格
    """
    codes = list(dict.fromkeys(args.stock_codes))[:5]
    if len(args.stock_codes) > 5:
        print(f"⚠️ 最多支持 5 只股票对比，已截取前 5 只：{', '.join(codes)}", file=sys.stderr)

    invalid = [c for c in codes if not re.match(r'^\d{5,6}$', c)]
    if invalid:
        output_error(f"无效的股票代码：{', '.join(invalid)}。请使用 5-6 位数字代码。")
        return

    data_list = []
    for code in codes:
        html = fetch_detail(code)
        data = parse_detail_html(html)
        prov_names = list(PROVIDER_NAME_MAP.values())
        if data.get(prov_names[0], {}).get("rate") or data.get(prov_names[1], {}).get("rate"):
            data_list.append(data)

    if not data_list:
        output_error("无有效的股票 ESG 数据。")
        return

    if args.json:
        output_json({"stocks": [_strip_json(d) for d in data_list]})
    else:
        lines = ["📊 ESG 评级对比", ""]
        headers = ["股票"] + list(PROVIDER_NAME_MAP.values())
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("|" + "|".join(["---"] * len(headers)) + "|")

        for data in data_list:
            name = data.get("stock_name", "")
            code = data.get("stock_code", "")
            row = [f"{name}({code})"]
            for name_key in PROVIDER_NAME_MAP.values():
                d = data.get(name_key, {})
                rate = d.get("rate", "-")
                date = d.get("date", "")
                row.append(f"{rate} ({date})" if date else rate)
            lines.append("| " + " | ".join(row) + " |")

        lines.append("")
        lines.append("> 数据来源：证券之星 ESG")
        output_text("\n".join(lines))


def cmd_list(args):
    """
    辅助功能：浏览 ESG 评级列表命令。

    按评级机构分类展示股票列表，支持翻页。
    每页固定 20 条记录。仅当用户明确要求时使用。

    参数：
        args: argparse 命名空间，包含 provider, page, json 等字段
              provider 支持英文名（miotech/chindices/syntaogf）和中文别名（妙盈/华证/商道融绿）

    输出：
        JSON（--json 时）或 Markdown 列表
    """
    provider = PROVIDER_ALIAS.get(args.provider.lower())
    if not provider or provider not in PROVIDERS:
        output_error(f"无效的评级机构。可用选项：{'、'.join(PROVIDERS.keys())}（妙盈、华证、商道融绿）")
        return

    prov = PROVIDERS[provider]
    resp_text = fetch_list(prov["api"], args.page, 20)
    try:
        resp = json.loads(resp_text)
    except json.JSONDecodeError:
        output_error("API 返回数据格式错误。")
        return

    if resp.get("ret") != 0:
        output_error(f"API 返回错误: {resp.get('msg', '未知错误')}")
        return

    items = resp.get("data", [])
    if not items:
        output_error("暂无数据。")
        return

    if args.json:
        output_json({"provider": prov["name"], "page": args.page, "items": items})
    else:
        lines = [f"📋 {prov['name']} ESG 评级列表（第{args.page}页）", ""]
        lines.append("| 股票名称 | 股票代码 | ESG 评级 | 评级日期 |")
        lines.append("|---------|---------|---------|---------|")
        for item in items:
            name = normalize_name(item.get("STOCKNAME", ""))
            code = item.get("STOCKCODE", "")
            rate = item.get("ESG_RATE", "")
            raw_date = str(item.get("ESG_RATING_DATE", ""))
            date_fmt = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:]}" if len(raw_date) == 8 else raw_date
            lines.append(f"| {name} | {code} | {rate} | {date_fmt} |")
        lines.append("")
        footer = f"> 共 {len(items)} 条记录"
        if len(items) == 20:
            footer += f"。提示: 使用 --page {args.page + 1} 查看下一页"
        lines.append(footer)
        output_text("\n".join(lines))


def main():
    """
    CLI 主入口：构建参数解析器、解析参数、路由到对应命令处理函数。

    支持 5 个子命令：
        search    — 模糊搜索股票
        query     — 个股综合 ESG 评级
        detail    — 个股 ESG 详细评分
        compare   — 多股 ESG 对比
        list      — 评级列表浏览（辅助功能）

    每个子命令都支持 --json 参数控制输出格式。
    """
    parser = argparse.ArgumentParser(
        description="证券之星 ESG 评级查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python cli.py search 茅台                # 搜索股票
  python cli.py query 600519               # 查询贵州茅台ESG评级
  python cli.py detail 000858 --json       # 查看五粮液ESG详细评分（JSON输出）
  python cli.py compare 600519 000858      # 对比茅台和五粮液
  python cli.py list --provider chindices    # 查看华证评级列表（辅助功能）
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # search 子命令：模糊搜索
    p_search = subparsers.add_parser("search", help="模糊搜索股票（按名称或代码）")
    p_search.add_argument("keyword", help="股票名称或代码关键词")
    p_search.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    # query 子命令：个股综合评级
    p_query = subparsers.add_parser("query", help="查询个股综合 ESG 评级")
    p_query.add_argument("stock_code", help="股票代码（如 600519、00001）")
    p_query.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    # detail 子命令：个股详细评分
    p_detail = subparsers.add_parser("detail", help="查询个股 ESG 详细评分")
    p_detail.add_argument("stock_code", help="股票代码（如 600519、00001）")
    p_detail.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    # compare 子命令：多股对比
    p_compare = subparsers.add_parser("compare", help="对比多只股票 ESG 评级（最多 5 只）")
    p_compare.add_argument("stock_codes", nargs="+", help="股票代码列表")
    p_compare.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    # list 子命令：评级列表
    p_list = subparsers.add_parser("list", help="浏览 ESG 评级列表（辅助功能）")
    p_list.add_argument("--provider", "-p", required=True,
                        help="评级机构（miotech/chindices/syntaogf 或 妙盈/华证/商道融绿）")
    p_list.add_argument("--page", type=int, default=1, help="页码（默认 1）")
    p_list.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    commands = {
        "search": cmd_search,
        "query": cmd_query,
        "detail": cmd_detail,
        "compare": cmd_compare,
        "list": cmd_list,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
