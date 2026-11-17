#!/usr/bin/env python3
"""Search Xiaohongshu by topic, then read the notes you pick (LinkDigest API).

    python3 xhs_search.py "成都 咖啡店"                # list the notes (4 credits when found)
    python3 xhs_search.py "成都 咖啡店" --read 3       # also read the first 3 (text, every image OCR'd, top comments)
    python3 xhs_search.py "skincare routine" --limit 8 --format json

Standard library only. Reads LINKDIGEST_API_KEY; talks only to linkdigest.dev.
The reads go through the bundled linkdigest.py (202 queue + polling handled).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import linkdigest as ld  # noqa: E402

SEARCH = "https://linkdigest.dev/api/v1/search"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="小红书按话题搜笔记，再读成文字 / Search Xiaohongshu, then read the notes")
    p.add_argument("query", help="话题，中文或英文，如 成都 咖啡店、通勤穿搭、skincare routine")
    p.add_argument("--limit", type=int, default=5, help="最多返回几条（1–10，默认 5）")
    p.add_argument("--read", type=int, default=0, help="接着读前 N 条（按条计费：图文 6 张图以内 1 积分，视频按分钟）")
    p.add_argument("--max-credits", type=int, help="每条最多花多少积分，超过的不读、不扣费")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = p.parse_args(argv)

    key = os.environ.get("LINKDIGEST_API_KEY", "").strip()
    if not key:
        ld.log(f"搜索需要 LINKDIGEST_API_KEY：在 {ld.KEYS_URL} 创建（注册送 10 积分，不用卡），然后 export LINKDIGEST_API_KEY=ld_live_...")
        return ld.EXIT_USAGE
    if not 1 <= args.limit <= 10 or args.read < 0:
        ld.log("--limit 是 1 到 10；--read 不能是负数")
        return ld.EXIT_USAGE

    try:
        status, headers, payload = ld.call(
            "POST", SEARCH, key, {"query": args.query, "platform": "xiaohongshu", "limit": args.limit}, timeout=120
        )
    except (urllib.error.URLError, OSError) as err:
        ld.log(f"连不上 linkdigest.dev: {err}{ld.net_hint(err)}")
        return ld.EXIT_ERROR
    if status == 401:
        ld.log(f"Key 无效（401）。在 {ld.KEYS_URL} 重新创建。")
        return ld.EXIT_AUTH
    if status == 402:
        ld.log(f"积分不够这次搜索（402，未扣费）：{ld.field(payload, 'error', '')} 付款链接：{ld.field(payload, 'starter_url', '') or ld.field(payload, 'buy_url', '')}")
        return ld.EXIT_PAYMENT
    if status == 429:
        ld.log(f"搜索太频繁或今天的免费搜索额度用完了（429）：{ld.field(payload, 'error', '')}")
        return ld.EXIT_RATE_LIMITED
    if status != 200:
        ld.log(f"搜索失败（HTTP {status}）：{ld.field(payload, 'error', payload)}")
        return ld.EXIT_ERROR

    results = ld.field(payload, "results", []) or []
    if args.format == "json" and not args.read:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"## 小红书搜索：{args.query}（{len(results)} 条，搜索 {ld.field(payload, 'credits', 0)} 积分）\n")
        for i, r in enumerate(results, 1):
            print(f"{i}. {r.get('title') or '(无标题)'}\n   {r.get('url')}")
    if not results:
        ld.log("没有找到网页已收录的小红书笔记。换一个更具体的中文说法试试，或在自己的浏览器里用 LinkDigest 扩展读自己的信息流。")
        return ld.EXIT_OK

    code = ld.EXIT_OK
    for i, r in enumerate(results[: args.read], 1):
        print(f"\n---\n\n# {i}. {r.get('title') or r.get('url')}\n", flush=True)
        extra = ["--format", args.format] + (["--max-credits", str(args.max_credits)] if args.max_credits else [])
        code = ld.main([r["url"], *extra])
        if code == ld.EXIT_PAYMENT:
            ld.log("积分不够，后面的不读了。付款链接在上面；买完重跑同一条命令，读过的走缓存不再扣费。")
            return code
    return code


if __name__ == "__main__":
    sys.exit(main())
