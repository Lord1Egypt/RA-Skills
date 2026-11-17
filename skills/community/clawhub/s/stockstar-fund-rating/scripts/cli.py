#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
证券之星基金评级 — CLI 入口模块。

使用方式：
  python scripts/cli.py query <基金代码>        # 文本输出
  python scripts/cli.py query <基金代码> --json  # JSON 输出（供 AI 解析）

数据流：
  1. _init_cache() 初始化缓存路径为脚本所在目录
  2. cache.load() 尝试加载本地缓存
  3. 无缓存 → cache.build_cache() 全量下载（并行）
  4. 有缓存 → cache.check_expiry() 检测过期 → 增量更新
  5. cache.find_fund() 在缓存中查找
   6. 未命中 → cache.append_fund() 并行补查
  7. 输出 JSON 或表格文本
"""

import argparse
import os
import re
import sys

from config import INSTITUTIONS
from utils import output_json, output_error, output_text
from parser import _rating_to_text, _rating_to_stars
import cache


def _init_cache():
    """设置缓存目录为脚本所在目录，确保缓存文件与脚本同路径。"""
    cache.CACHE_DIR = os.path.dirname(os.path.abspath(__file__))


def _resolve_code(c, raw):
    """
    将用户输入解析为基金代码。
    输入为 6 位数字 → 直接返回。
    输入为中文/字母 → 通过名称查找。
    返回 (code_or_none, error_or_none)。
    """
    if re.match(r'^\d{6}$', raw):
        return raw, None
    result = cache.search_by_name(c, raw)
    if result is None:
        return None, f"未找到与 \"{raw}\" 匹配的基金。"
    if "multiple" in result:
        names = "、".join([f"{m['name']}({m['code']})" for m in result["multiple"]])
        return None, f"找到多只匹配的基金：{names}，请使用基金代码查询。"
    return result["code"], None


def cmd_query(args):
    """
    查询基金评级主逻辑。

    步骤：
    1. 输入为 6 位数字 → 直接作为基金代码；否则按名称查找
    2. 加载/构建缓存
    3. 在缓存中查找基金
    4. 未命中时补查
    5. 组装输出结果

    JSON 输出包含：fund_name, fund_code, ratings.{机构名}.{rating/rating_text/rating_stars/rating_date/status}
    文本输出按 Markdown 表格排列，未评级机构显示 "-"。
    """
    _init_cache()
    c = cache.load()

    if c is None:
        # 首次查询：全量下载全部机构评级
        print("⏳ 正在初始化数据，请稍候...", file=sys.stderr)
        c = cache.build_cache()
        print("✅ 数据已就绪，可随时查询", file=sys.stderr)
    else:
        # 检测各机构评级日期是否变化
        expired = cache.check_expiry(c)
        if expired:
            names = [INSTITUTIONS[k]["name"] for k in expired]
            print(f"⏳ 检测到评级更新：{'、'.join(names)}，正在刷新...", file=sys.stderr)
            for key in expired:
                c = cache.update_institution(c, key)
            print("✅ 数据已更新", file=sys.stderr)

    # 解析输入：代码或名称
    code, err = _resolve_code(c, args.fund_code)
    if err:
        if args.json:
            output_error(err)
        else:
            output_text(err)
        return

    fund = cache.find_fund(c, code)
    if fund is None:
        # 缓存未命中：逐页搜索该基金
        print(f"⏳ 正在查找 {code} 的评级数据...", file=sys.stderr)
        fund = cache.append_fund(c, code)

    if fund is None:
        output_error(f"未找到基金 {code} 的评级数据。")
        return

    # 组装输出数据
    # rating_text（一星~五星）和 rating_stars（★★★☆☆）为 rating 的派生字段，
    # 缓存中不存储，在输出阶段由 parser._rating_to_text/stars 实时计算。
    # status 标记该机构对该基金是否已评级："rated" / "unrated"
    result = {
        "fund_name": fund["name"],
        "fund_code": code,
        "ratings": {},
    }
    for key, inst in INSTITUTIONS.items():
        rating_val = fund.get("ratings", {}).get(key, "")
        rating_date = c.get("institutions", {}).get(key, {}).get("rating_date", "")
        is_rated = rating_val != ""
        rating_str = str(rating_val) if is_rated else ""
        result["ratings"][inst["name"]] = {
            "rating": rating_str,
            "rating_text": _rating_to_text(rating_str) if is_rated else "",
            "rating_stars": _rating_to_stars(rating_str) if is_rated else "",
            "rating_date": rating_date,
            "status": "rated" if is_rated else "unrated",
        }

    if args.json:
        output_json(result)
    else:
        # 文本输出：Markdown 表格
        lines = [f"📊 {fund['name']} ({code}) — 基金评级", ""]
        lines.append("| 评级机构 | 评级 | 评级日期 |")
        lines.append("|---------|------|---------|")
        for name, inst in INSTITUTIONS.items():
            r = result["ratings"][inst["name"]]
            stars = r["rating_stars"] if r["status"] == "rated" else "未评级"
            date = r["rating_date"] or "-"
            lines.append(f"| {inst['name']} | {stars} | {date} |")
        lines.append("")
        lines.append("> 数据来源：证券之星基金评级")
        output_text("\n".join(lines))


def main():
    """CLI 入口：定义子命令和参数。"""
    parser = argparse.ArgumentParser(description="证券之星基金评级查询工具")
    subparsers = parser.add_subparsers(dest="command")

    p_query = subparsers.add_parser("query", help="查询基金评级")
    p_query.add_argument("fund_code", help="6 位基金代码")
    p_query.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    args = parser.parse_args()
    if args.command == "query":
        cmd_query(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
