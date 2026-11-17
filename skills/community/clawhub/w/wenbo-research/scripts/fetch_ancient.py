#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开源古籍全文拉取 + 关键词抽取（wenbo-research Step 2）

数据源：GitHub 开源古籍库（殆知阁 v20，raw.githubusercontent.com 可达）。
本脚本只拉取"免费公开"白名单数据，绝不抓取 ctext 等禁止源。

用法:
    python3 fetch_ancient.py 汉书 --keywords 上郡 肤施 奢延
    python3 fetch_ancient.py 水经注 --keywords 无定河 奢延水 --json
    python3 fetch_ancient.py --list                 # 列出可拉取的书目

说明:
    - 结果缓存到 ../data/cache/<书名>.txt，重复运行不重复下载。
    - 输出：关键词命中次数 + 上下文样例（段落级索引）。
    - 开源本为整理文本，非点校本；学术结论须回影印本/点校本（见 SKILL.md Step 5）。
"""
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(HERE, "..", "data", "cache")
RAW_BASE = "https://raw.githubusercontent.com/garychowcmu/daizhigev20/master/"

# 殆知阁 v20 关键书目 → 相对路径（史藏）
BOOKS = {
    "史记": "史藏/正史/史记.txt",
    "汉书": "史藏/正史/汉书.txt",
    "前汉书": "史藏/正史/前汉书.txt",
    "后汉书": "史藏/正史/后汉书.txt",
    "明史": "史藏/正史/明史.txt",
    "清史稿": "史藏/正史/清史稿.txt",
    "水经": "史藏/地理/水经.txt",
    "水经注": "史藏/地理/水经注.txt",
    "水经注疏": "史藏/地理/水经注疏.txt",
    "三辅黄图": "史藏/地理/三辅黄图.txt",
    "陕西通志": "史藏/地理/陕西通志.txt",
    "元和郡县图志": "史藏/地理/元和郡县图志.txt",
    "元和郡县志": "史藏/地理/元和郡县志.txt",
    "关中胜迹图志": "史藏/地理/关中胜迹图志.txt",
    "读史方舆纪要": "史藏/地理/读史方舆纪要.txt",
}

CTX = 60  # 上下文窗口（字）


def cache_path(book):
    os.makedirs(CACHE_DIR, exist_ok=True)
    return os.path.join(CACHE_DIR, book + ".txt")


def fetch(book, max_bytes=None):
    p = cache_path(book)
    if os.path.exists(p) and os.path.getsize(p) > 0:
        data = open(p, encoding="utf-8", errors="ignore").read()
        return (data[:max_bytes] if max_bytes else data), True
    rel = BOOKS[book]
    url = RAW_BASE + urllib.parse.quote(rel)
    # 优先 curl（对慢速/不稳定连接更稳健），失败 fallback 到 urllib
    try:
        subprocess.run(
            ["curl", "-sL", "--max-time", "180", "--retry", "2",
             "-A", "Mozilla/5.0 wenbo-research", url, "-o", p],
            check=True, timeout=200)
        if os.path.exists(p) and os.path.getsize(p) > 0:
            data = open(p, encoding="utf-8", errors="ignore").read()
            return (data[:max_bytes] if max_bytes else data), False
    except Exception as e:
        print(f"  [curl 失败，回退 urllib：{type(e).__name__}]")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 wenbo-research"})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = r.read().decode("utf-8", errors="ignore")
    with open(p, "w", encoding="utf-8") as f:
        f.write(data)
    return (data[:max_bytes] if max_bytes else data), False


def extract(text, keywords):
    result = {}
    for kw in keywords:
        hits = []
        start = 0
        while True:
            i = text.find(kw, start)
            if i == -1:
                break
            lo = max(0, i - CTX)
            hi = min(len(text), i + len(kw) + CTX)
            hits.append(text[lo:hi].replace("\n", " ").strip())
            start = i + len(kw)
        result[kw] = hits
    return result


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    list_only = "--list" in sys.argv

    if list_only:
        print("可拉取书目：")
        for b, rel in BOOKS.items():
            print(f"  {b}  ->  {rel}")
        return

    if not args:
        print(__doc__)
        return

    book = args[0]
    if book not in BOOKS:
        print(f"❌ 未收录书目「{book}」。可用 --list 查看清单。")
        sys.exit(1)

    keywords = args[1:] or ["上郡"]
    max_bytes = None
    if "--preview" in sys.argv:
        max_bytes = 300000
    text, cached = fetch(book, max_bytes=max_bytes)
    tag = "（预览前 30 万字）" if max_bytes else ""
    print(f"已加载《{book}》（{len(text)} 字{tag}，{'缓存' if cached else '新下载'}）\n")
    for kw in keywords:
        hits = extract(text, [kw])[kw]
        print(f"■ 「{kw}」命中 {len(hits)} 处")
        for h in hits[:3]:
            print(f"  …{h}…")
        print()


if __name__ == "__main__":
    main()
