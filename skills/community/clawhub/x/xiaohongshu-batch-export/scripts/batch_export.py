#!/usr/bin/env python3
"""Read a batch of links and save each one as its own Markdown file (LinkDigest API).

    python3 batch_export.py link1 link2 ...                 # into ./linkdigest-export/
    python3 batch_export.py --file links.txt --out notes/   # one link (or share text) per line
    python3 batch_export.py --file links.txt --depth script # speech only, the cheapest read

Writes <out>/NN-<title>.md per link that was read, and <out>/index.md: a table
of number, title, author, date, likes and file. Standard library only. Reads
LINKDIGEST_API_KEY; talks only to linkdigest.dev. Cached links are free; links
that could not be read are listed and not billed.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import linkdigest as ld  # noqa: E402

BATCH = "https://linkdigest.dev/api/v1/digest/batch"
DEPTHS = ("full", "transcript", "script")


def safe_name(text: str, limit: int = 40) -> str:
    """A title as a file name: no path separators or control characters."""
    text = re.sub(r"[\\/:*?\"<>|\r\n\t#]+", " ", text or "").strip()
    return (text[:limit].strip() or "untitled").replace(" ", "-")


def stat(d: dict, *names: str):
    stats = d.get("stats") or {}
    for n in names:
        if isinstance(stats.get(n), int):
            return stats[n]
    return ""


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="一批链接逐条读成文字，每条存一个 Markdown 文件 / Batch-export links to Markdown files")
    p.add_argument("links", nargs="*", help="链接或整段分享文案")
    p.add_argument("--file", help="每行一条链接的文本文件")
    p.add_argument("--out", default="linkdigest-export", help="输出目录（默认 ./linkdigest-export）")
    p.add_argument("--depth", choices=DEPTHS, default=None, help="script=只要口播文案（最省）；transcript=逐字稿+每分钟一帧；full=完整（默认）")
    p.add_argument("--label", default="", help="给这一批起个名字，方便以后在控制台找")
    p.add_argument("--timeout", type=int, default=1800, help="最多等多少秒（默认 1800）")
    args = p.parse_args(argv)

    key = os.environ.get("LINKDIGEST_API_KEY", "").strip()
    if not key:
        ld.log(f"需要 LINKDIGEST_API_KEY：在 {ld.KEYS_URL} 创建（注册送 10 积分，不用卡），然后 export LINKDIGEST_API_KEY=ld_live_...")
        return ld.EXIT_USAGE
    links = list(args.links)
    if args.file:
        with open(args.file, encoding="utf-8") as f:
            links += [line.strip() for line in f if line.strip()]
    if not links:
        ld.log("没有链接。把链接写在命令后面，或用 --file。")
        return ld.EXIT_USAGE

    body: dict = {"urls": links}
    if args.depth and args.depth != "full":
        body["depth"] = args.depth
    if args.label:
        body["label"] = args.label
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
        if ld.field(state, "status", "") == "done":
            break
        ld.log(f"读了 {ld.field(state, 'done', 0)}/{ld.field(state, 'total', len(links))} 条…")
        time.sleep(6)
    else:
        ld.log(f"还没读完。稍后用同一个批次接着取：GET {BATCH}/{batch_id}")
        return ld.EXIT_TIMEOUT

    _, _, full = ld.call("GET", f"{BATCH}/{batch_id}?include=digests", key, None, timeout=120)
    digests = ld.field(full, "digests", None)
    digests = digests if isinstance(digests, dict) else {}
    os.makedirs(args.out, exist_ok=True)

    rows, missed = [], []
    for n, item in enumerate(ld.field(full, "items", []) or ld.field(state, "items", []) or [], start=1):
        url = item.get("url", "")
        d = digests.get(url) or {}
        if item.get("status") not in ("done", "cached") or not d:
            missed.append(f"| {n} | 没读到（{item.get('error_code') or item.get('status')}，不扣费） | {url} |")
            continue
        title = d.get("title") or (d.get("caption") or "").split("\n")[0][:40] or "(无标题)"
        name = f"{n:02d}-{safe_name(title)}.md"
        with open(os.path.join(args.out, name), "w", encoding="utf-8") as f:
            f.write(d.get("raw_markdown") or json.dumps(d, ensure_ascii=False, indent=2))
        likes = stat(d, "likes", "like")
        rows.append(f"| {n} | {title} | {d.get('author') or ''} | {d.get('posted_at') or ''} | {likes} | [{name}]({name}) |")

    with open(os.path.join(args.out, "index.md"), "w", encoding="utf-8") as f:
        f.write(f"# {args.label or '批量导出'}（批次 {batch_id}）\n\n")
        f.write("| # | 标题 | 作者 | 发布 | 点赞 | 文件 |\n|---|---|---|---|---|---|\n")
        f.write("\n".join(rows) + "\n")
        if missed:
            f.write("\n## 没读到\n\n| # | 原因 | 链接 |\n|---|---|---|\n" + "\n".join(missed) + "\n")

    ld.log(f"完成：{len(rows)} 条存到 {args.out}/，{len(missed)} 条没读到；共 {ld.field(full, 'credits_total', ld.field(state, 'credits_total', 0))} 积分。")
    print(os.path.join(args.out, "index.md"))
    return ld.EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
