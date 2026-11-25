#!/usr/bin/env python3
"""Read several Xiaohongshu / Douyin / TikTok / YouTube links and get one comparison page (LinkDigest API).

    python3 compare.py link1 link2 link3                # read all, then one comparison
    python3 compare.py --file links.txt                 # one link (or share text) per line
    python3 compare.py link1 link2 --format json        # the batch JSON instead of Markdown

Standard library only. Reads LINKDIGEST_API_KEY; talks only to linkdigest.dev.
Cached links are free; each new link is billed like a single read; the comparison
is billed once per started ten links.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import linkdigest as ld  # noqa: E402

BATCH = "https://linkdigest.dev/api/v1/digest/batch"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="多条小红书/抖音链接读完后出一页对比 / Read several links, get one comparison")
    p.add_argument("links", nargs="*", help="链接或整段分享文案，2 条起")
    p.add_argument("--file", help="每行一条链接的文本文件")
    p.add_argument("--label", default="", help="给这一批起个名字，方便以后在控制台找")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--timeout", type=int, default=900, help="最多等多少秒（默认 900）")
    args = p.parse_args(argv)

    key = os.environ.get("LINKDIGEST_API_KEY", "").strip()
    if not key:
        ld.log(f"需要 LINKDIGEST_API_KEY：在 {ld.KEYS_URL} 创建（注册送 10 积分，不用卡），然后 export LINKDIGEST_API_KEY=ld_live_...")
        return ld.EXIT_USAGE
    links = list(args.links)
    if args.file:
        with open(args.file, encoding="utf-8") as f:
            links += [line.strip() for line in f if line.strip()]
    if len(links) < 2:
        ld.log("至少给 2 条链接才能对比。")
        return ld.EXIT_USAGE

    body = {"urls": links, "synthesis": True, **({"label": args.label} if args.label else {})}
    try:
        status, _, payload = ld.call("POST", BATCH, key, body, timeout=120)
    except (urllib.error.URLError, OSError) as err:
        ld.log(f"连不上 linkdigest.dev: {err}{ld.net_hint(err)}")
        return ld.EXIT_ERROR
    if status == 401:
        ld.log(f"Key 无效（401）。在 {ld.KEYS_URL} 重新创建。")
        return ld.EXIT_AUTH
    if status == 402:
        ld.log(f"积分不够（402，未扣费）：{ld.field(payload, 'error', '')} 付款链接：{ld.field(payload, 'starter_url', '') or ld.field(payload, 'buy_url', '')}")
        return ld.EXIT_PAYMENT
    if status not in (200, 202):
        ld.log(f"提交失败（HTTP {status}）：{ld.field(payload, 'error', payload)}")
        return ld.EXIT_ERROR

    batch_id = ld.field(payload, "batch_id", "")
    ld.log(f"已提交 {len(links)} 条，批次 {batch_id}，正在读取…")
    deadline = time.time() + args.timeout
    state = payload
    while time.time() < deadline:
        status, _, state = ld.call("GET", f"{BATCH}/{batch_id}", key, None, timeout=60)
        synth = ld.field(state, "synthesis", None) or {}
        if ld.field(state, "status", "") == "done" and (not synth or synth.get("status") not in ("running", "pending")):
            break
        ld.log(f"读了 {ld.field(state, 'done', 0)}/{ld.field(state, 'total', len(links))} 条…")
        time.sleep(6)
    else:
        ld.log(f"还没读完。稍后用同一个批次接着取：GET {BATCH}/{batch_id}")
        return ld.EXIT_TIMEOUT

    # The full digests come back keyed by link when asked for; the plain poll only lists items.
    try:
        _, _, full = ld.call("GET", f"{BATCH}/{batch_id}?include=digests", key, None, timeout=60)
        if isinstance(full, dict) and isinstance(full.get("digests"), dict):
            state = full
    except (urllib.error.URLError, OSError):
        pass

    if args.format == "json":
        print(json.dumps(state, ensure_ascii=False, indent=2))
    else:
        synth = ld.field(state, "synthesis", None) or {}
        text = synth.get("raw_markdown") or synth.get("summary") or ""
        print(f"# 对比：{args.label or batch_id}\n")
        if text:
            print(text)
        else:
            err = ld.field(state, "synthesis_error", "")
            print(f"（没有生成对比{'：' + str(err) if err else ''}。至少要 2 条读到才会对比。）")
        digests = ld.field(state, "digests", None)
        digests = digests if isinstance(digests, dict) else {}
        print("\n## 每条链接\n")
        for item in ld.field(state, "items", []) or []:
            url = item.get("url", "")
            d = digests.get(url) or {}
            title = d.get("title") or (d.get("caption") or "").split("\n")[0][:40] or "(无标题)"
            if item.get("status") in ("done", "cached"):
                print(f"- {title} — {d.get('author') or ''} — {url}")
            else:
                print(f"- 没读到（{item.get('error_code') or item.get('status')}，不扣费）— {url}")
    failed = ld.field(state, "failed", 0)
    ld.log(f"完成：{ld.field(state, 'done', 0)} 条读到，{failed} 条没读到；共 {ld.field(state, 'credits_total', 0)} 积分。")
    return ld.EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
