#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_quote.py - 从图语录 tuyulu.com 获取每日语录 / 往期回顾 / 分类语录。

数据源为图语录公开 API（GET JSON）：
    https://www.tuyulu.com/ur/openApi/tuyulu/daily           今日/指定日期语录
    https://www.tuyulu.com/ur/openApi/tuyulu/daily/history   往期回顾列表
    https://www.tuyulu.com/ur/openApi/tuyulu/category/list   分类列表
    https://www.tuyulu.com/ur/openApi/tuyulu/phrase/list     分类语录分页

用法：
    python fetch_quote.py daily                          # 今日语录
    python fetch_quote.py daily --date 20260917          # 指定日期（YYYYMMDD）
    python fetch_quote.py daily --output out.json        # 写入文件
    python fetch_quote.py history [--output out.json]    # 往期回顾
    python fetch_quote.py categories [--output out.json] # 分类列表
    python fetch_quote.py phrase --category 3 [--page 1] [--pageSize 5] [--output out.json]

退出码：0 成功；1 网络/解析失败。失败时在 stderr 输出原因。
输出：JSON 直接打到 stdout（UTF-8，不转义中文），--output 时写入文件。
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse

BASE = "https://www.tuyulu.com/ur/openApi/tuyulu"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Referer": "https://www.tuyulu.com/",
    "Accept": "application/json, text/plain, */*",
}
TIMEOUT = 30


def get_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"响应不是合法 JSON（{url}）：{e}；返回前 200 字符：{raw[:200]}")
    if not data.get("success"):
        raise RuntimeError(f"接口返回失败（{url}）：{data}")
    return data


def main():
    parser = argparse.ArgumentParser(description="图语录数据获取")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_daily = sub.add_parser("daily", help="今日/指定日期每日语录")
    p_daily.add_argument("--date", help="日期 YYYYMMDD，缺省为今天")
    p_daily.add_argument("--output")

    p_hist = sub.add_parser("history", help="往期每日语录列表")
    p_hist.add_argument("--output")

    p_cat = sub.add_parser("categories", help="语录分类列表")
    p_cat.add_argument("--output")

    p_phrase = sub.add_parser("phrase", help="分类语录分页列表")
    p_phrase.add_argument("--category", type=int, required=True, help="分类 ID")
    p_phrase.add_argument("--page", type=int, default=1)
    p_phrase.add_argument("--pageSize", type=int, default=5)
    p_phrase.add_argument("--output")

    args = parser.parse_args()
    try:
        if args.cmd == "daily":
            url = f"{BASE}/daily"
            if args.date:
                url += "?" + urllib.parse.urlencode({"date": args.date})
            payload = get_json(url)
        elif args.cmd == "history":
            payload = get_json(f"{BASE}/daily/history")
        elif args.cmd == "categories":
            payload = get_json(f"{BASE}/category/list")
        else:  # phrase
            qs = urllib.parse.urlencode({
                "categoryId": args.category, "page": args.page, "pageSize": args.pageSize
            })
            payload = get_json(f"{BASE}/phrase/list?{qs}")
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)

    out = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"已写入 {args.output}", file=sys.stderr)
    else:
        print(out)


if __name__ == "__main__":
    main()
