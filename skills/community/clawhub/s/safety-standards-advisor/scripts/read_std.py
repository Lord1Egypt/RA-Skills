# -*- coding: utf-8 -*-
"""读标准：给定相对路径/标准号/标题，抽取并输出该标准的全文文字，供顾问引用真实条款。
用法：
  python read_std.py "法律标准\\标准\\化学品\\GB 30871-2022 ...pdf"
  python read_std.py "GB 30871-2022 危险化学品企业特殊作业安全规范（2022.10.1实施）.pdf"
输出：标准全文（截断到 config 上限），扫描件/.doc 给出提示。
"""
import os, sys, argparse, csv, json

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STANDARDS_ROOT = os.environ.get("SAFETY_STANDARDS_ROOT", "standards")
CORPUS = os.environ.get("SAFETY_CORPUS", "safety-corpus")
CORPUS_IDX = os.path.join(CORPUS, "index.jsonl")
REF = os.path.join(SKILL_DIR, "references")
CATALOG = os.path.join(REF, "标准目录.csv")
sys.path.insert(0, os.path.join(SKILL_DIR, "scripts"))
from extract_text import read_standard

MAX_CHARS = int(os.environ.get("SAFETY_READ_MAX", "60000"))


def load_corpus_map():
    """src_rel -> (text_rel, chars, ocr_pages)。用于扫描件 OCR 文本回落。"""
    m = {}
    if not os.path.exists(CORPUS_IDX):
        return m
    with open(CORPUS_IDX, encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r.get("text_rel") and r.get("chars", 0) > 0:
                m[r["src_rel"]] = (r["text_rel"], r["chars"], r.get("ocr_pages"))
    return m


def resolve_rel(query):
    """把标准号/标题模糊匹配到目录里的相对路径。
    排除加密件 (.xdf)、扫描件等无法机读的格式，优先选可读版本。"""
    cols = {"标准号": "stdno", "标题": "title", "主题": "topic", "格式": "fmt", "相对路径": "rel"}
    rows = []
    for r in csv.DictReader(open(CATALOG, encoding="utf-8-sig")):
        rows.append({en: r.get(zh, "") for zh, en in cols.items()})
    q = os.path.splitext(query)[0].replace(" ", "").lower()
    # 不可读扩展名（加密/压缩包/图片）— 不作为首选
    BAD_EXT = ('.xdf', '.rar', '.zip', '.dwg')
    candidates = []
    for r in rows:
        s = r["stdno"].replace(" ", "").lower()
        t = r["title"].replace(" ", "").lower()
        sc = 0
        if t and q in t:
            sc = 95
        elif s and (q == s or q in s or s in q):
            sc = 90
        elif t and t in q and len(t) > 3:
            sc = 70
        if sc > 0:
            # 不可读格式扣分，可读格式加分
            rel_low = r["rel"].lower()
            if any(rel_low.endswith(ext) for ext in BAD_EXT):
                sc -= 50  # 大幅降权，但不完全排除（万一只有这一份）
            candidates.append((sc, r["rel"]))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    best = candidates[0][1]
    # .doc 若有同名 .docx 副本，改用副本（.doc 二进制读不出正文）
    if best.lower().endswith(".doc"):
        alt = best[:-4] + ".docx"
        if os.path.exists(os.path.join(STANDARDS_ROOT, alt)):
            has_docx = any(r["rel"] == alt for r in rows)
            if has_docx:
                return alt
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", help="相对路径 / 标准号 / 标题")
    ap.add_argument("--max", type=int, default=MAX_CHARS)
    a = ap.parse_args()

    rel = a.query
    if not os.path.exists(rel):
        rel = resolve_rel(a.query)
        if not rel:
            print("[未找到匹配的标准：%s]" % a.query)
            return
    txt, scanned, ext, found = read_standard(rel, STANDARDS_ROOT)
    if not found:
        print("[文件不存在：%s]" % rel)
        return
    if scanned or not txt.strip():
        # 源库读不出 → 回落到 corpus（可能已有 OCR 文本或 .docx 副本正文）
        cmap = load_corpus_map()
        hit = cmap.get(rel)
        if hit:
            text_rel, chars, ocr_pages = hit
            tp = os.path.join(CORPUS, text_rel)
            if os.path.exists(tp):
                with open(tp, encoding="utf-8", errors="ignore") as tf:
                    body = tf.read()
                print("源文件：%s" % os.path.join(STANDARDS_ROOT, rel))
                if ocr_pages:
                    print("[扫描件，正文来自 OCR 前 %d 页]" % ocr_pages)
                else:
                    print("[源格式无文字层，正文来自语料库抽取件]")
                print("字数：%d" % chars)
                print("=" * 70)
                print(body[:a.max])
                return
        if scanned:
            print("[扫描件/图片型PDF，无文字层，且语料库中尚无 OCR 文本。]")
        else:
            print("[无可用正文]")
        print("源文件：%s" % os.path.join(STANDARDS_ROOT, rel))
        return
    if not txt.strip():
        if ext == ".doc":
            print("[.doc 二进制格式，未抽正文。请用 Word 另存为 .docx 后重抽。]")
        else:
            print("[无可用正文]")
        print("源文件：%s" % os.path.join(STANDARDS_ROOT, rel))
        return
    print("源文件：%s" % os.path.join(STANDARDS_ROOT, rel))
    print("字数：%d" % len(txt))
    print("=" * 70)
    print(txt[:a.max])


if __name__ == "__main__":
    main()
