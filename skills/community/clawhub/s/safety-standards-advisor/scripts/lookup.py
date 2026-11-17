# -*- coding: utf-8 -*-
"""查标准：根据关键词/标准号/主题/正文内容，在标准目录与语料库中检索适用标准。
用法：
  python lookup.py "有限空间" [--topic 有限空间] [--limit 20]
  python lookup.py "30871" --stdno
  python lookup.py "临时用电 电缆" --content
输出命中标准的 标准号/标题/主题/相对路径(fmt)，供顾问引用。
"""
import os, sys, json, csv, argparse

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STANDARDS_ROOT = os.environ.get("SAFETY_STANDARDS_ROOT", "standards")
CORPUS = os.environ.get("SAFETY_CORPUS", "safety-corpus")
REF = os.path.join(SKILL_DIR, "references")
CATALOG = os.path.join(REF, "标准目录.csv")
STDNO_IDX = os.path.join(REF, "stdno_index.json")
LAW_IDX = os.path.join(REF, "law_index.json")
CORPUS_IDX = os.path.join(CORPUS, "index.jsonl")

LEVEL_ORDER = ["法律", "行政法规", "部门规章", "规范性文件"]
LEVEL_BADGE = {"法律": "🔴法律", "行政法规": "🟠行政法规", "部门规章": "🟡部门规章", "规范性文件": "🟢规范性文件"}


def load_catalog():
    cols = {"标准号": "stdno", "标题": "title", "主题": "topic", "格式": "fmt", "相对路径": "rel"}
    out = []
    for r in csv.DictReader(open(CATALOG, encoding="utf-8-sig")):
        out.append({en: r.get(zh, "") for zh, en in cols.items()})
    return out


def search_law(q, limit=20):
    """在法律法规索引中检索（按法律层级排序输出）。
    国家法律法规作为上位法，永远优先于行业标准。"""
    if not os.path.exists(LAW_IDX):
        return []
    data = json.load(open(LAW_IDX, encoding="utf-8"))
    ql = q.lower()
    hits = []
    for L in data.get("all", []):
        hay = (L["title"] + " " + L.get("stdno", "")).lower()
        if ql in hay:
            hits.append(L)
    if not hits and len(q) >= 2:
        # 关键词拆分再搜
        for L in data.get("all", []):
            hay = L["title"].lower()
            if all(k in hay for k in q.lower().split()):
                hits.append(L)
    # 按 level 排序：法律 > 行政法规 > 部门规章 > 规范性文件
    hits.sort(key=lambda x: LEVEL_ORDER.index(x["level"]) if x["level"] in LEVEL_ORDER else 99)
    return hits[:limit]


def search_by_stdno(q):
    if not os.path.exists(STDNO_IDX):
        return []
    idx = json.load(open(STDNO_IDX, encoding="utf-8"))
    qn = q.replace(" ", "").upper()
    res = []
    if qn in idx:
        res += idx[qn]
    else:
        for k, v in idx.items():
            if qn in k.upper():
                res += v
    return res


def load_dup_set():
    """已由 .docx 副本承载正文的 .doc 记录，检索时让位，避免重复"""
    dups = set()
    if os.path.exists(CORPUS_IDX):
        with open(CORPUS_IDX, encoding="utf-8") as f:
            for line in f:
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                if rec.get("dup"):
                    dups.add(rec["src_rel"])
    return dups


def search_by_keyword(q, topic=None, limit=30):
    rows = load_catalog()
    dups = load_dup_set()
    ql = q.lower()
    out = []
    for r in rows:
        if r.get("rel") in dups:
            continue
        hay = (r["title"] + " " + r["stdno"] + " " + r["topic"]).lower()
        if ql in hay and (not topic or r["topic"] == topic):
            out.append(r)
    return out[:limit]


def search_content(q, limit=20):
    if not os.path.exists(CORPUS_IDX):
        return []
    ql = q.lower()
    out = []
    with open(CORPUS_IDX, encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            if rec.get("dup") or not rec.get("text_rel"):
                continue
            head = (rec.get("title", "") + rec.get("stdno", "")).lower()
            if ql in head:
                out.append(rec)
                if len(out) >= limit:
                    break
                continue
            tp = os.path.join(CORPUS, rec["text_rel"])
            if os.path.exists(tp):
                with open(tp, encoding="utf-8", errors="ignore") as tf:
                    chunk = tf.read(30000)
                if ql in chunk.lower():
                    out.append(rec)
            if len(out) >= limit:
                break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--topic", default=None)
    ap.add_argument("--stdno", action="store_true")
    ap.add_argument("--content", action="store_true")
    ap.add_argument("--law", action="store_true", help="只在法律法规索引中检索（上位法优先）")
    ap.add_argument("--limit", type=int, default=30)
    a = ap.parse_args()

    if a.law:
        res = search_law(a.query, a.limit)
        print("=== 法律法规命中（按法律层级排序，%d）===" % len(res))
        for L in res:
            badge = LEVEL_BADGE.get(L["level"], L["level"])
            print("  %s | %s | %s" % (badge, L["title"], L.get("rel", "")))
        return

    if a.stdno:
        res = search_by_stdno(a.query)
        print("=== 标准号匹配 (%d) ===" % len(res))
        for r in res:
            print("  %-12s | %s | %s | %s" % (r.get("stdno", ""), r["title"], r["topic"], r["rel"]))
    elif a.content:
        res = search_content(a.query, a.limit)
        print("=== 正文内容命中 (%d) ===" % len(res))
        for r in res:
            print("  %-12s | %s | %s | %s" % (r.get("stdno", ""), r.get("title",""), r.get("topic",""), r.get("src_rel", r.get("rel", ""))))
    else:
        # 默认：法律法规优先 + 行业标准补充
        laws = search_law(a.query, limit=10)
        stds = search_by_keyword(a.query, a.topic, a.limit)
        if laws:
            print("=== 一、适用法律法规（上位法义务，%d）===" % len(laws))
            for L in laws:
                badge = LEVEL_BADGE.get(L["level"], L["level"])
                print("  %s | %s | %s" % (badge, L["title"], L.get("rel", "")))
            print()
        else:
            print("（未在法律法规索引中命中，仅检索行业标准）\n")
        print("=== 二、相关行业标准（执行细则，%d）===" % len(stds))
        for r in stds:
            print("  %-12s | %s | %s | %s" % (r.get("stdno", ""), r["topic"], r["title"], r["rel"]))
        if len(laws) + len(stds) < 3:
            print("\n提示：命中少，可加 --content 在正文里搜，或 --stdno 按标准号查，或 --law 只查法律法规。")


if __name__ == "__main__":
    main()
