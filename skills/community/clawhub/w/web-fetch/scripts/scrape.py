#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通用网页采集脚本。

静态页: requests + BeautifulSoup
JS 页:   Playwright (--js)
支持: 自定义字段(CSS选择器)、链接提取、robots.txt 检查、结构化 JSON/CSV 输出。

用法示例:
  python scrape.py "https://news.ycombinator.com/" --select "span.titleline>a" --attr href --text
  python scrape.py "URL" --field "title:.product-card h2" --field "price:.price" --out out.json
  python scrape.py "URL" --js --wait ".product-card"
"""
import argparse
import csv
import json
import os
import random
import sys
import time

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("❌ 需要 requests 与 beautifulsoup4：pip install requests beautifulsoup4 lxml", file=sys.stderr)
    sys.exit(1)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
]


def can_fetch(url, check=True):
    if not check:
        return True
    try:
        from urllib.parse import urlparse
        from urllib.robotparser import RobotFileParser
        p = urlparse(url)
        base = f"{p.scheme}://{p.netloc}"
        rp = RobotFileParser()
        rp.set_url(base + "/robots.txt")
        rp.read()
        return rp.can_fetch("*", url)
    except Exception:
        return True  # 读取失败则放行（保守默认）


def fetch(url, use_js=False, wait=None, timeout=20):
    if use_js:
        return fetch_playwright(url, wait, timeout)
    headers = {"User-Agent": random.choice(USER_AGENTS), "Referer": "https://www.google.com/"}
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def fetch_playwright(url, wait, timeout):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ 需要 playwright：pip install playwright && playwright install chromium", file=sys.stderr)
        sys.exit(1)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=timeout * 1000)
        if wait:
            page.wait_for_selector(wait, timeout=timeout * 1000)
        html = page.content()
        browser.close()
        return html


def extract(html, args):
    soup = BeautifulSoup(html, "lxml")
    records = []
    if args.select:
        nodes = soup.select(args.select)
        for n in nodes:
            rec = {}
            if args.attr:
                rec["attr"] = n.get(args.attr, "")
            if args.text:
                rec["text"] = n.get_text(strip=True)
            if rec:
                records.append(rec)
        return records
    if args.field:
        fields = {}
        for f in args.field:
            if ":" not in f:
                continue
            name, sel = f.split(":", 1)
            nodes = soup.select(sel)
            fields[name.strip()] = [n.get_text(strip=True) for n in nodes]
        # 对齐为记录列表
        maxlen = max((len(v) for v in fields.values()), default=0)
        for i in range(maxlen):
            rec = {k: (v[i] if i < len(v) else "") for k, v in fields.items()}
            records.append(rec)
        return records
    # 默认：提取所有链接
    for a in soup.find_all("a", href=True):
        records.append({"text": a.get_text(strip=True), "href": a["href"]})
    return records


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--select", help="CSS 选择器（提取匹配节点）")
    ap.add_argument("--attr", help="从匹配节点取属性")
    ap.add_argument("--text", action="store_true", help="取匹配节点文本")
    ap.add_argument("--field", action="append", default=[], help="字段:选择器，可多次")
    ap.add_argument("--js", action="store_true", help="用 Playwright 渲染 JS")
    ap.add_argument("--wait", help="Playwright 等待选择器")
    ap.add_argument("--out", help="输出文件(.json/.csv)")
    ap.add_argument("--no-robots", action="store_true", help="跳过 robots.txt 检查")
    ap.add_argument("--timeout", type=int, default=20)
    args = ap.parse_args()

    if not can_fetch(args.url, not args.no_robots):
        print("⛔ robots.txt 禁止抓取该 URL：", args.url, file=sys.stderr)
        sys.exit(1)

    try:
        html = fetch(args.url, args.js, args.wait, args.timeout)
    except Exception as e:
        print(f"❌ 抓取失败: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)

    records = extract(html, args)
    print(f"✅ 抓取到 {len(records)} 条记录")
    print("__JSON__" + json.dumps(records[:20], ensure_ascii=False))

    if args.out:
        if args.out.endswith(".csv") and records:
            with open(args.out, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.DictWriter(f, fieldnames=records[0].keys())
                w.writeheader()
                w.writerows(records)
        else:
            with open(args.out, "w", encoding="utf-8") as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
        print(f"💾 已写入 {args.out}")


if __name__ == "__main__":
    main()
