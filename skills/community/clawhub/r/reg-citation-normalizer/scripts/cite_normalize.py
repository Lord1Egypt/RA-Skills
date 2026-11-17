#!/usr/bin/env python3
"""reg-citation-normalizer: 医疗器械法规引用编号识别与规范化.

用法:
  python cite_normalize.py normalize "21 CFR 820.30(a)(6)"     # 规范化书写
  python cite_normalize.py parse "ISO 13485:2016 clause 7.5.1" # 结构化 JSON
  python cite_normalize.py check report.md                     # 批量检查文件中的引用
  python cite_normalize.py normalize --json "YY/T 0287-2017 7.5.1"

零第三方依赖，纯标准库。MIT License.
"""
import argparse
import json
import re
import sys

# ---------------------------------------------------------------------------
# 机构别名表（NMPA 历史沿革）
# 官方口径: 部令写法 = 发布机关全称 + 令 + 第N号
# 出处: 国务院公报 / NMPA 官网公告
# ---------------------------------------------------------------------------
AGENCY_ALIASES = {
    "国家食品药品监督管理局": "国家食品药品监督管理局",
    "国家食品药品监督管理总局": "国家食品药品监督管理总局",
    "国家市场监督管理总局": "国家市场监督管理总局",
    "国家药品监督管理局": "国家药品监督管理局",
    "国务院": "国务院",
    "sfda": "国家食品药品监督管理局",
    "cfda": "国家食品药品监督管理总局",
    "nmpa": "国家药品监督管理局",
}

# ---------------------------------------------------------------------------
# 条款路径: 7.5.1 / (a)(6) / Annex B.5
# ---------------------------------------------------------------------------
_CLAUSE = r"(?:clause\s+|section\s+|第)?\s*(\d+(?:\.\d+)*|[A-Z](?:\.\d+)*)\s*(?:(?:条|款)?\s*([（(][a-zA-Z0-9０-９]+[)）](?:\s*[（(]\d+[)）])*))?"

# ---------------------------------------------------------------------------
# 文法 1: 美国 21 CFR — 官方格式 "title CFR part.section"
# 出处: govinfo.gov / ecfr.gov
# ---------------------------------------------------------------------------
CFR_RE = re.compile(
    r"\b(?P<title>\d{1,2})\s*CFR\s*(?:§\s*|Part\s+|part\s+|part\.?\s*)?"
    r"(?P<part>\d{1,4})(?:\.(?P<section>\d{1,4}))?"
    r"(?P<paras>(?:\s*[（(][a-zA-Z0-9]+[)）])*)",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# 文法 2: ISO/IEC — 注日期引用 "ISO 12345:2018, 4.3.9"
# 出处: ISO/IEC Directives Part 2, clauses 10.4-10.5
# ---------------------------------------------------------------------------
ISO_RE = re.compile(
    r"\b(?P<body>ISO(?:/IEC(?:\s*/?)?)?|IEC|ISO/IEC\s*IEEE|ISO/TR|ISO/TS)\s*"
    r"(?P<num>\d{3,6})(?:[-/](?P<part>\d{1,3}))?\s*"
    r"(?:[:：]\s*(?P<year>\d{4}))?"
    r"(?:\s*(?:,|，)?\s*(?:clause\s+|section\s+|第)?\s*(?P<clause>\d+(?:\.\d+)+|\d+)\s*"
    r"(?P<paras>(?:\s*[（(][a-zA-Z0-9]+[)）])*)"
    r")?"
    r"(?P<amd>\s*(?:/Amd(?:1|2)?:?\s*\d{4}|/Amd\s*\d+:\s*\d{4}))?",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# 文法 3: 中国国标/行标 — "代号 顺序号-年份"
# 出处: GB/T 1.1-2020（引用规则）
# ---------------------------------------------------------------------------
CN_STD_RE = re.compile(
    r"\b(?P<code>GB/T|GB/Z|YY/T|YY/Z|YZB|GB|YY|QB|JB|WS/T|WS)\s*"
    r"(?P<num>\d{1,6})(?:\.(?P<part>\d{1,3}))?\s*"
    r"[-—–]\s*(?P<year>\d{4})"
    r"(?:\s*(?:,|，)?\s*(?:第)?\s*(?P<clause>\d+(?:\.\d+)*)\s*条?)?",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# 文法 4: 中国部令/公告 — "机关全称令第N号" / "公告 20XX年第N号"
# ---------------------------------------------------------------------------
DECREE_RE = re.compile(
    r"(?P<agency>[^\s，,。;；()（）《》]{2,25}?)(?:令|署令)\s*(?:第\s*)?(?P<num>\d{1,4})\s*号"
    r"|(?P<agency2>国家药监局|国家市场监督管理总局|国务院)\s*公告\s*"
    r"(?P<year2>20\d{2})\s*年\s*第\s*(?P<num2>\d{1,4})\s*号",
)

# 常见书写勘误规则
TYPO_RULES = [
    (re.compile(r"\bISO(?=\d)", re.IGNORECASE), "代号与编号之间缺空格（且代号应大写）: 'ISO13485'/'iso13485' → 'ISO 13485'"),
    (re.compile(r"\biso\s*(?=\d)"), "标准代号应全大写: 'iso 13485' → 'ISO 13485'"),
    (re.compile(r"\bIEC(?=\d)"), "标准号与编号之间缺空格: 'IEC62304' → 'IEC 62304'"),
    (re.compile(r"\b(?:YY|GB)/(?:T|Z)?(?=\d)"), "代号与编号之间缺空格: 'YY/T0287' → 'YY/T 0287'"),
    (re.compile(r"\bCFR\s*§", re.IGNORECASE), "CFR 官方写法无需 § 号: '21 CFR § 820.30' → '21 CFR 820.30'"),
    (re.compile(r"\b\d{1,2}\s*CFR\s*Part\s+\d+\.\d+", re.IGNORECASE), "'Part' 后不应跟节号: '21 CFR Part 820.30' → '21 CFR 820.30'"),
    (re.compile(r"\b\d{1,2}\s*CFR(?=\d)", re.IGNORECASE), "CFR 与编号之间缺空格: '21CFR820' → '21 CFR 820'"),
    (re.compile(r"[（(]\d{4}[）)]\s*版"), "年份建议用一字线连接: 'YY/T 0287（2017）版' → 'YY/T 0287-2017'"),
    (re.compile(r"\bGB(?:/T|/Z)?\s*\d+(?:\.\d+)?\s*:\s*\d{4}", re.IGNORECASE), "中国标准年份用一字线不用冒号: 'GB 9706.1:2020' → 'GB 9706.1-2020'"),
]


def _clean_paras(paras: str):
    if not paras:
        return []
    return re.findall(r"[（(]([a-zA-Z0-9]+)[)）]", paras)


def parse_citation(text: str):
    """返回第一个命中的引用结构（dict），未命中返回 None。"""
    m = CFR_RE.search(text)
    if m:
        return {
            "domain": "us-fda",
            "type": "cfr",
            "title": int(m.group("title")),
            "part": m.group("part"),
            "section": m.group("section"),
            "paragraphs": _clean_paras(m.group("paras")),
            "canonical": canonical_cfr(m),
            "source_text": m.group(0).strip(),
        }
    m = ISO_RE.search(text)
    if m:
        clause = m.group("clause")
        year = m.group("year")
        return {
            "domain": "international",
            "type": "iso-iec",
            "body": m.group("body").upper().replace("  ", " "),
            "number": m.group("num"),
            "part": m.group("part"),
            "year": year,
            "clause": clause,
            "paragraphs": _clean_paras(m.group("paras")),
            "amd": (m.group("amd") or "").strip(),
            "canonical": canonical_iso(m),
            "warnings": iso_warnings(m),
            "source_text": m.group(0).strip(),
        }
    m = CN_STD_RE.search(text)
    if m:
        code = m.group("code").upper()
        if m.group("code").lower().endswith("/t") or "/T" in m.group("code"):
            pass
        # 归一代码: GB/T / YY/T 补齐斜杠
        raw = m.group(0)
        return {
            "domain": "china",
            "type": "cn-standard",
            "code": code,
            "number": m.group("num"),
            "part": m.group("part"),
            "year": m.group("year"),
            "clause": m.group("clause"),
            "canonical": f"{code} {m.group('num')}{('.' + m.group('part')) if m.group('part') else ''}-{m.group('year')}"
                         + (f"，第{m.group('clause')}条" if m.group("clause") else ""),
            "source_text": raw.strip(),
        }
    m = DECREE_RE.search(text)
    if m:
        agency = (m.group("agency") or m.group("agency2") or "").strip()
        for lead in ("依据", "按照", "根据", "符合", "见", "参照"):
            if agency.startswith(lead):
                agency = agency[len(lead):]
        agency_std = AGENCY_ALIASES.get(agency.lower(), AGENCY_ALIASES.get(agency, agency))
        if m.group("num2"):
            canon = f"{agency_std}公告 {m.group('year2')}年第{m.group('num2')}号"
        else:
            canon = f"{agency_std}令第{m.group('num')}号"
        return {
            "domain": "china",
            "type": "decree-notice",
            "agency": agency_std,
            "number": m.group("num") or m.group("num2"),
            "canonical": canon,
            "source_text": m.group(0).strip(),
        }
    return None


def canonical_cfr(m):
    canon = f"{m.group('title')} CFR {m.group('part')}"
    if m.group("section"):
        canon += f".{m.group('section')}"
    for p in _clean_paras(m.group("paras")):
        canon += f"({p})"
    return canon


def canonical_iso(m):
    body = m.group("body").upper()
    canon = f"{body} {m.group('num')}"
    if m.group("part"):
        canon += f"-{m.group('part')}"
    clause = m.group("clause")
    if clause:
        # ISO 规则: 引用具体条款必须注日期，逗号+空格
        canon += f":{m.group('year') or 'YYYY'}, {clause}"
        for p in _clean_paras(m.group("paras")):
            canon += f"({p})"
    elif m.group("year"):
        canon += f":{m.group('year')}"
    if m.group("amd"):
        canon += m.group("amd").strip()
    return canon


def iso_warnings(m):
    warns = []
    if m.group("clause") and not m.group("year"):
        warns.append("引用具体条款须注日期（ISO/IEC Directives Part 2 §10.5）")
    return warns


def check_text(text: str):
    """扫描文本中的引用与书写问题，返回问题列表。"""
    issues = []
    for line_no, line in enumerate(text.splitlines(), 1):
        for rx, msg in TYPO_RULES:
            if rx.search(line):
                issues.append({"line": line_no, "issue": msg, "context": line.strip()[:80]})
        # ISO 条款引用缺年份
        for m in ISO_RE.finditer(line):
            if m.group("clause") and not m.group("year"):
                issues.append({
                    "line": line_no,
                    "issue": f"注日期建议: '{m.group(0).strip()}' 引用条款须注日期 → '{canonical_iso(m)}'",
                    "context": line.strip()[:80],
                })
    return issues


def normalize(text: str, as_json: bool = False):
    hits = []
    s = text
    # 找出全部命中（逐文法扫描，取不重叠命中）
    for rx in (CFR_RE, ISO_RE, CN_STD_RE, DECREE_RE):
        for m in rx.finditer(text):
            span = m.span()
            if any(not (span[1] <= h["start"] or span[0] >= h["end"]) for h in hits):
                continue
            one = parse_citation(m.group(0))
            if one:
                one["start"], one["end"] = span
                hits.append(one)
    hits.sort(key=lambda h: h["start"])
    if as_json:
        return json.dumps(hits, ensure_ascii=False, indent=2)
    if not hits:
        return "（未识别到法规引用）"
    out = []
    for h in hits:
        warn = h.get("warnings")
        out.append(f"{h['source_text']}  →  {h['canonical']}" + (f"   ⚠ {'；'.join(warn)}" if warn else ""))
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="医疗器械法规引用编号识别与规范化")
    ap.add_argument("mode", choices=["normalize", "parse", "check"])
    ap.add_argument("input", help="文本（normalize/parse）或文件路径（check）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    if args.mode == "normalize":
        print(normalize(args.input, args.json))
    elif args.mode == "parse":
        r = parse_citation(args.input)
        print(json.dumps(r, ensure_ascii=False, indent=2) if r else json.dumps(None))
    elif args.mode == "check":
        with open(args.input, encoding="utf-8-sig") as f:
            text = f.read()
        issues = check_text(text)
        if args.json:
            print(json.dumps(issues, ensure_ascii=False, indent=2))
        else:
            if not issues:
                print("PASS: 未发现引用书写问题")
            for i in issues:
                print(f"第{i['line']}行: {i['issue']}\n    上下文: {i['context']}")
            sys.exit(1 if issues else 0)


if __name__ == "__main__":
    main()
