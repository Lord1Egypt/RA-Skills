#!/usr/bin/env python3
"""Web Content Monitor — 网页内容监控"""
import argparse, hashlib, os, sys, re
from datetime import datetime

MONITOR_DIR = os.path.expanduser("~/.web_monitor")

def load_hashes(path: str) -> dict:
    f = os.path.join(MONITOR_DIR, "hashes.json")
    if os.path.exists(f):
        import json; return json.load(open(f))
    return {}

def save_hashes(hashes: dict):
    os.makedirs(MONITOR_DIR, exist_ok=True)
    import json
    with open(os.path.join(MONITOR_DIR, "hashes.json"), "w") as f:
        json.dump(hashes, f)

def fetch_page(url: str) -> str:
    try:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return f"[ERROR fetching page: {e}]"

def monitor(url: str, keywords: list) -> dict:
    content = fetch_page(url)
    url_hash = hashlib.md5(url.encode()).hexdigest()
    old_hashes = load_hashes()
    old_content = old_hashes.get(url_hash, {}).get("content", "")
    old_hash = hashlib.md5(old_content.encode()).hexdigest()
    new_hash = hashlib.md5(content.encode()).hexdigest()
    result = {"changed": new_hash != old_hash, "url": url}
    if keywords:
        kws_found = [k for k in keywords if k in content]
        kws_old = [k for k in keywords if k in old_content]
        result["keywords_new"] = [k for k in kws_found if k not in kws_old]
        result["keywords_disappeared"] = [k for k in kws_old if k not in kws_found]
    old_hashes[url_hash] = {"content": content, "ts": datetime.now().isoformat()}
    save_hashes(old_hashes)
    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--url", required=True)
    p.add_argument("--keywords", default="", help="逗号分隔关键词")
    p.add_argument("--hash-file", default="")
    args = p.parse_args()
    kw_list = [k.strip() for k in args.keywords.split(",") if k.strip()] if args.keywords else []
    result = monitor(args.url, kw_list)
    print(f"URL: {result['url']}")
    print(f"内容变化: {'是' if result['changed'] else '否'}")
    if kw_list:
        print(f"新增关键词: {result.get('keywords_new', [])}")
        print(f"消失关键词: {result.get('keywords_disappeared', [])}")
    sys.exit(1 if result["changed"] else 0)
