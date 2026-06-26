#!/usr/bin/env python3
"""
Tavily Search & Extract — OpenClaw Skill
Modes: general | news | research
Presets: crypto | finance | spiritual
"""

import argparse
import json
import os
import pathlib
import re
import sys
import urllib.request

SEARCH_URL = "https://api.tavily.com/search"
EXTRACT_URL = "https://api.tavily.com/extract"

PRESETS = {
    "crypto": [
        "coindesk.com", "cointelegraph.com", "decrypt.co", "messari.io",
        "defillama.com", "theblock.co", "cryptobriefing.com", "bitcoin.com",
        "coinmarketcap.com", "coingecko.com", "binance.com", "delphi.digital",
    ],
    "finance": [
        "bloomberg.com", "reuters.com", "ft.com", "wsj.com", "cnbc.com",
        "marketwatch.com", "investing.com", "seekingalpha.com",
        "tradingview.com", "coinmarketcap.com",
    ],
    "spiritual": [
        "gaia.com", "mindvalley.com", "chopra.com", "spiritualityhealth.com",
        "lionsroar.com", "tricycle.org", "sounds-true.com",
    ],
}


def load_key():
    # 首先檢查環境變數
    key = os.environ.get("TAVILY_API_KEY")
    if key:
        return key.strip()
    
    # 如果沒有設定，提示用戶設定（英文 + 中文）
    print("")
    print("=" * 60)
    print("⚠️ TAVILY API Key Required / 需要設定 TAVILY API Key")
    print("=" * 60)
    print("")
    print("To use this skill, please set your Tavily API key:")
    print("使用此 skill，請設定您的 Tavily API key：")
    print("")
    print("Option 1 / 選項 1 - Set environment variable:")
    print("  export TAVILY_API_KEY='your_api_key_here'")
    print("")
    print("Option 2 / 選項 2 - Add to ~/.openclaw/.env:")
    print("  TAVILY_API_KEY=your_api_key_here")
    print("")
    print("Get your free API key at: https://tavily.com")
    print("獲取免費 API key：https://tavily.com")
    print("")
    print("=" * 60)
    sys.exit(1)


def post_json(url, payload):
    key = load_key()
    payload["api_key"] = key
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        sys.exit(f"Tavily API 錯誤 {e.code}: {body[:300]}")
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        sys.exit(f"Tavily 回傳非 JSON: {body[:300]}")


def build_query_with_lang(query, lang):
    """Append language hint to query if needed."""
    if lang == "zh-TW":
        return f"{query} 繁體中文"
    if lang == "en":
        return query
    # both: no modification, let Tavily return mixed
    return query


def do_search(args):
    mode = args.mode
    query = build_query_with_lang(args.query, args.lang)

    payload = {
        "query": query,
        "max_results": args.max_results,
        "include_images": False,
        "include_raw_content": False,
    }

    # Mode-specific settings
    if mode == "news":
        payload["topic"] = "news"
        payload["days"] = args.days if args.days is not None else 7
        payload["search_depth"] = "basic"
        payload["include_answer"] = False
    elif mode == "research":
        payload["topic"] = "general"
        payload["search_depth"] = "advanced"
        payload["include_answer"] = True
        if args.days is not None:
            payload["days"] = args.days
    else:  # general
        payload["topic"] = "general"
        payload["search_depth"] = "basic"
        payload["include_answer"] = args.include_answer
        if args.days is not None:
            payload["days"] = args.days

    # Domain preset
    if args.preset and args.preset in PRESETS:
        payload["include_domains"] = PRESETS[args.preset]

    obj = post_json(SEARCH_URL, payload)

    results = []
    for r in (obj.get("results") or [])[:args.max_results]:
        results.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": r.get("content", ""),
            "published_date": r.get("published_date"),
        })

    out = {
        "mode": mode,
        "query": args.query,
        "answer": obj.get("answer"),
        "results": results,
    }
    if not out["answer"]:
        out.pop("answer", None)

    return out


def do_extract(urls):
    payload = {"urls": urls}
    obj = post_json(EXTRACT_URL, payload)

    results = []
    for r in (obj.get("results") or []):
        results.append({
            "url": r.get("url", ""),
            "title": r.get("title", ""),
            "content": r.get("raw_content") or r.get("content", ""),
            "failed_results": None,
        })

    failed = obj.get("failed_results") or []

    return {"extracted": results, "failed": failed}


def fmt_md(out):
    lines = []

    if "extracted" in out:
        for r in out["extracted"]:
            lines.append(f"## {r['title'] or r['url']}")
            lines.append(f"URL: {r['url']}")
            lines.append("")
            content = (r.get("content") or "").strip()
            lines.append(content[:3000] + ("…" if len(content) > 3000 else ""))
            lines.append("")
        if out.get("failed"):
            lines.append("### 擷取失敗")
            for f in out["failed"]:
                lines.append(f"- {f.get('url', f)}: {f.get('error', '未知錯誤')}")
        return "\n".join(lines)

    if out.get("answer"):
        lines.append(f"**摘要：** {out['answer'].strip()}")
        lines.append("")

    for i, r in enumerate(out.get("results", []), 1):
        title = r.get("title", "").strip() or r.get("url", "")
        url = r.get("url", "")
        snippet = (r.get("snippet") or "").strip()
        date = r.get("published_date")
        lines.append(f"{i}. **{title}**")
        if url:
            lines.append(f"   {url}")
        if date:
            lines.append(f"   📅 {date}")
        if snippet:
            lines.append(f"   {snippet[:300]}")
        lines.append("")

    return "\n".join(lines).strip()


def fmt_brief(out):
    lines = []
    if out.get("answer"):
        lines.append(f"摘要：{out['answer'].strip()[:200]}")
        lines.append("")
    for i, r in enumerate(out.get("results", []), 1):
        title = r.get("title", "").strip() or "(無標題)"
        url = r.get("url", "")
        lines.append(f"{i}. {title}")
        if url:
            lines.append(f"   {url}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Tavily Search & Extract for OpenClaw")
    ap.add_argument("--query", help="搜索關鍵字")
    ap.add_argument("--mode", choices=["general", "news", "research"], default="general")
    ap.add_argument("--preset", choices=list(PRESETS.keys()), help="Domain 預設組合")
    ap.add_argument("--days", type=int, help="只搜最近 N 天（news 預設 7）")
    ap.add_argument("--max-results", type=int, default=5)
    ap.add_argument("--lang", choices=["zh-TW", "en", "both"], default="both")
    ap.add_argument("--include-answer", action="store_true")
    ap.add_argument("--format", choices=["md", "json", "brief"], default="md")
    ap.add_argument("--extract", nargs="+", metavar="URL", help="擷取完整頁面內容")
    args = ap.parse_args()

    # research mode bumps max-results default
    if args.mode == "research" and args.max_results == 5:
        args.max_results = 8

    if args.extract:
        out = do_extract(args.extract)
    elif args.query:
        out = do_search(args)
    else:
        ap.error("請提供 --query 或 --extract")

    if args.format == "json":
        json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    elif args.format == "brief":
        print(fmt_brief(out))
    else:
        print(fmt_md(out))


if __name__ == "__main__":
    main()
