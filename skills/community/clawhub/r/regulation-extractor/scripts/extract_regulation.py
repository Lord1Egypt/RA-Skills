# -*- coding: utf-8 -*-
"""
法规PDF结构化提取脚本
从建筑工程规范PDF中提取条文，处理双文字层（原文+OCR），输出结构化JSON。

用法: python extract_regulation.py <pdf_path> [--output <output.json>] [--chapters <chapters.json>]
"""

import fitz, re, json, sys, argparse
from difflib import SequenceMatcher
from pathlib import Path

# OCR错误特征字符集
OCR_ERROR_CHARS = set("秭瀑癌编髟勉举伞攀秂")

# 页眉/页脚/水印关键词
SKIP_KEYWORDS = {"住房城乡建设部", "浏览专用", "息公"}

# 非正文关键词
NON_BODY_PREFIX = re.compile(r'^(附录|说明|用词|条文|引用|List|Appendix|Explanation|for Design|本规范用词|引用标准)')

# 章节标题模式
CHAPTER_TITLE_RE = re.compile(r'^\d{1,2}\s+[\u4e00-\u9fff].{1,20}$')

# 纯数字行（页码）
PAGE_NUM_RE = re.compile(r'^\d{1,3}$')

# 带圈数字映射
CIRCLE_NUM = {
    '①':'1','②':'2','③':'3','④':'4','⑤':'5',
    '⑥':'6','⑦':'7','⑧':'8','⑨':'9',
    '\u2460':'1','\u2461':'2','\u2462':'3','\u2463':'4',
    '\u2464':'5','\u2465':'6','\u2466':'7','\u2467':'8',
    '\u2468':'9','\u2469':'10',
}

# 默认章节映射（JGJ 80-2016）
DEFAULT_CHAPTERS = {
    "1": "总则", "2": "术语和符号", "3": "基本规定",
    "4": "临边与洞口作业", "5": "攀登与悬空作业",
    "6": "操作平台", "7": "交叉作业", "8": "建筑施工安全网",
}


def has_ocr_errors(text):
    return any(c in text for c in OCR_ERROR_CHARS)


def similarity(a, b, threshold=0.75):
    if not a or not b or len(a) < 5 or len(b) < 5:
        return False
    id_a = re.match(r'^\d+\.\d+\.\d+', a)
    id_b = re.match(r'^\d+\.\d+\.\d+', b)
    if id_a and id_b and id_a.group() != id_b.group():
        return False
    if (id_a is None) != (id_b is None):
        return False
    return SequenceMatcher(None, a, b).ratio() >= threshold


def extract_lines(doc, chapters=None):
    """提取文本行，双文字层去重"""
    all_lines = []
    for page_idx in range(len(doc)):
        page = doc[page_idx]
        blocks = page.get_text("dict")["blocks"]
        page_lines = []
        for block in blocks:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                text = "".join(span["text"] for span in line["spans"]).strip()
                if not text or len(text) < 2:
                    continue
                if any(kw in text for kw in SKIP_KEYWORDS):
                    continue
                page_lines.append(text)
        
        # 相邻相似行去重（保留更干净的）
        deduped, skip = [], set()
        for i, la in enumerate(page_lines):
            if i in skip:
                continue
            best = la
            for j in range(i + 1, min(i + 4, len(page_lines))):
                if j in skip:
                    continue
                if similarity(la, page_lines[j]):
                    if has_ocr_errors(best) and not has_ocr_errors(page_lines[j]):
                        best = page_lines[j]
                    skip.add(j)
            deduped.append({"page": page_idx + 1, "text": best})
        all_lines.extend(deduped)
    return all_lines


def parse_articles(lines, chapters=None):
    """切分条文"""
    if chapters is None:
        chapters = DEFAULT_CHAPTERS
    articles = {}
    current_id, current_lines, current_page = None, [], 1
    
    for item in lines:
        text, page = item["text"], item["page"]
        if CHAPTER_TITLE_RE.match(text) and len(text) < 25:
            continue
        if PAGE_NUM_RE.match(text):
            continue
        if NON_BODY_PREFIX.match(text):
            continue
        
        # 子条目检测（如 6.4.④ → 6.4.4）
        sub_m = re.match(r'^(\d+\.\d+)\.\s*([' + ''.join(CIRCLE_NUM.keys()) + r']|(\d+))\s*(.*)', text)
        if sub_m and current_id:
            if current_id and current_lines:
                _save(articles, current_id, current_page, current_lines, chapters)
            num = CIRCLE_NUM.get(sub_m.group(2), sub_m.group(3) or sub_m.group(2))
            current_id = f"{sub_m.group(1)}.{num}"
            current_lines = [sub_m.group(4)] if sub_m.group(4) else []
            current_page = page
            continue
        
        # 正式条文编号 (支持 3.1.2 和 3. 1. 2 两种格式，也支持4级)
        m = re.match(r'^(\d+\.\s*\d+\.\s*\d+(?:\.\s*\d+)*)[\s]*(.*)', text)
        if m:
            if current_id and current_lines:
                _save(articles, current_id, current_page, current_lines, chapters)
            current_id = re.sub(r'\s+', '', m.group(1))  # 去掉编号中的空格
            current_lines = [m.group(2)] if m.group(2) else []
            current_page = page
        elif current_id:
            current_lines.append(text)
    
    if current_id and current_lines:
        _save(articles, current_id, current_page, current_lines, chapters)
    return articles


def _save(articles, aid, page, lines, chapters):
    full = '\n'.join(lines).strip()
    full = re.sub(r'(\d+\.\d+)\.\s*[' + ''.join(CIRCLE_NUM.keys()) + r']', r'\1.', full)
    q = "clean" if not has_ocr_errors(full) else "ocr_error"
    if aid not in articles:
        articles[aid] = {"id": aid, "chapter": chapters.get(aid.split('.')[0], ""), "page": page, "text": full, "quality": q}
    elif q == "clean" and articles[aid]["quality"] == "ocr_error":
        articles[aid].update({"text": full, "quality": "clean", "page": page})


def postprocess(articles):
    """后处理：清理格式残留"""
    for aid, info in articles.items():
        t = info["text"]
        t = re.sub(r'^\s*\d+\.\d+\.\d+\s*[' + ''.join(CIRCLE_NUM.keys()) + r']\s*[《<]', '', t)
        t = re.sub(r'(\d+\.\d+\.\d+)\s*[' + ''.join(CIRCLE_NUM.keys()) + r']\s*[《<]?', r'\1 ', t)
        # 行内去重
        lines = t.split('\n')
        cleaned, skip = [], set()
        for i, line in enumerate(lines):
            if i in skip:
                continue
            for j in range(i + 1, min(i + 3, len(lines))):
                if similarity(line, lines[j], 0.8):
                    skip.add(j)
            cleaned.append(line)
        info["text"] = '\n'.join(cleaned)
        info["quality"] = "clean" if not has_ocr_errors(info["text"]) else "ocr_error"
    return articles


def validate(articles):
    report = {"total": len(articles), "clean": 0, "ocr_error": 0, "by_chapter": {}, "warnings": [], "missing": []}
    for aid, info in sorted(articles.items()):
        report["clean"] += info["quality"] == "clean"
        report["ocr_error"] += info["quality"] == "ocr_error"
        ch = info["chapter"]
        report["by_chapter"][ch] = report["by_chapter"].get(ch, 0) + 1
        tlen = len(info["text"])
        if tlen < 5:
            report["warnings"].append(f"{aid}: 过短({tlen}字)")
        elif tlen > 500:
            report["warnings"].append(f"{aid}: 过长({tlen}字)")
    def _sort_key(x):
        parts = x.split('.')
        result = []
        for p in parts:
            if p.isdigit():
                result.append(int(p))
            else:
                # 如 "3.1.2.a" → [3, 1, 2, 0] (字母按0处理，不影响主排序)
                try:
                    result.append(int(p))
                except ValueError:
                    result.append(0)
        return result
    
    all_ids = sorted(articles.keys(), key=_sort_key)
    for i in range(len(all_ids) - 1):
        cp = all_ids[i].split('.')
        np_ = all_ids[i+1].split('.')
        # 只对纯数字ID检查缺失
        if all(p.isdigit() for p in cp) and all(p.isdigit() for p in np_):
            c = [int(p) for p in cp]
            n = [int(p) for p in np_]
            if c[0] == n[0] and c[1] == n[1] and n[2] - c[2] > 1:
                for j in range(c[2]+1, n[2]):
                    report["missing"].append(f"{c[0]}.{c[1]}.{j}")
    return report


def main():
    parser = argparse.ArgumentParser(description="法规PDF条文提取")
    parser.add_argument("pdf", help="PDF文件路径")
    parser.add_argument("--output", "-o", help="输出JSON路径", default=None)
    parser.add_argument("--chapters", help="章节映射JSON文件", default=None)
    args = parser.parse_args()

    chapters = DEFAULT_CHAPTERS
    if args.chapters:
        with open(args.chapters, 'r', encoding='utf-8') as f:
            chapters = json.load(f)
    
    output = args.output or str(Path(args.pdf).with_suffix('.json'))
    
    print(f"📄 打开: {args.pdf}")
    doc = fitz.open(args.pdf)
    print(f"   页数: {len(doc)}")
    
    lines = extract_lines(doc, chapters)
    print(f"   文本行: {len(lines)}")
    
    articles = parse_articles(lines, chapters)
    articles = postprocess(articles)
    
    report = validate(articles)
    print(f"\n📊 提取完成: {report['total']}条  ✅{report['clean']}  ⚠️{report['ocr_error']}")
    for ch, cnt in report['by_chapter'].items():
        print(f"   {ch}: {cnt}")
    if report['missing']:
        print(f"⚠️ 缺失: {', '.join(report['missing'])}")

    with open(output, 'w', encoding='utf-8') as f:
        json.dump({"articles": articles, "report": report}, f, ensure_ascii=False, indent=2)
    print(f"💾 输出: {output}")
    doc.close()


if __name__ == '__main__':
    main()
