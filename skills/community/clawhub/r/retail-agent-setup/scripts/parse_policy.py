#!/usr/bin/env python3
"""
parse_policy.py — Parse policy documents into structured rule entries
Supports: PDF, DOCX, plain text

Usage:
    python3 parse_policy.py <input_file> [--output <output.json>] [--type <return|warranty|promotion|faq|general>]

Output: JSON array of structured policy/FAQ entries
"""

import sys
import json
import re
import argparse
import hashlib
from pathlib import Path
from datetime import datetime

# Optional dep detection
try:
    import pdfplumber
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

try:
    from docx import Document as DocxDocument
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

# ─── Policy type detection ──────────────────────────────────────────────────

POLICY_PATTERNS = {
    "return": ["退货", "退款", "退换", "无理由退", "七天", "7天", "return", "refund"],
    "warranty": ["保修", "质保", "三包", "维修", "warranty", "guarantee"],
    "promotion": ["活动", "优惠", "促销", "折扣", "满减", "赠品", "promo", "discount"],
    "faq": ["常见问题", "FAQ", "问答", "Q&A", "怎么", "如何", "能否", "是否"],
    "membership": ["会员", "积分", "等级", "vip", "VIP", "points", "member"],
    "hours": ["营业时间", "开门", "关门", "几点", "hours", "schedule"],
    "delivery": ["发货", "快递", "配送", "物流", "shipping", "delivery"],
}

def detect_policy_type(text: str) -> str:
    """Detect the most likely policy type from text content."""
    counts = {ptype: 0 for ptype in POLICY_PATTERNS}
    text_lower = text.lower()
    for ptype, keywords in POLICY_PATTERNS.items():
        for kw in keywords:
            counts[ptype] += text_lower.count(kw.lower())
    best = max(counts, key=counts.get)
    return best if counts[best] > 0 else "general"


# ─── Text extraction ─────────────────────────────────────────────────────────

def extract_text_from_pdf(filepath: str) -> str:
    if not HAS_PDF:
        raise ImportError("pdfplumber is required: pip install pdfplumber")
    with pdfplumber.open(filepath) as pdf:
        pages = [page.extract_text() or "" for page in pdf.pages]
    return "\n\n".join(pages)


def extract_text_from_docx(filepath: str) -> str:
    if not HAS_DOCX:
        raise ImportError("python-docx is required: pip install python-docx")
    doc = DocxDocument(filepath)
    return "\n".join(para.para for para in doc.paragraphs if para.text.strip())


def extract_text_from_txt(filepath: str) -> str:
    return Path(filepath).read_text(encoding="utf-8", errors="replace")


def extract_text(filepath: str) -> str:
    ext = Path(filepath).suffix.lower()
    if ext == ".pdf":
        return extract_text_from_pdf(filepath)
    elif ext in (".docx", ".doc"):
        return extract_text_from_docx(filepath)
    elif ext in (".txt", ".md"):
        return extract_text_from_txt(filepath)
    else:
        raise ValueError(f"Unsupported format: {ext}")


# ─── Policy parsing ───────────────────────────────────────────────────────────

def split_into_sections(text: str) -> list[dict]:
    """Split a document into sections based on headings or numbered items."""
    sections = []
    lines = text.split("\n")
    current_title = None
    current_body = []

    heading_pattern = re.compile(
        r"^(\d+[.、]|[一二三四五六七八九十]+[、.。]|#+\s|【.{1,20}】|第[一二三四五六七八九十\d]+条)"
    )

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if heading_pattern.match(line) or (len(line) < 30 and line.endswith(("：", ":", "。")) is False and len(line) > 2):
            if current_title or current_body:
                sections.append({"title": current_title or "", "body": "\n".join(current_body).strip()})
            current_title = line
            current_body = []
        else:
            current_body.append(line)

    if current_title or current_body:
        sections.append({"title": current_title or "", "body": "\n".join(current_body).strip()})

    return [s for s in sections if s["body"]]


def extract_conditions(text: str) -> list[str]:
    """Extract condition clauses from policy text."""
    patterns = [
        r"(?:购买|使用|发货|收货|签收)?后?(\d+)(?:天|日|个工作日)内",
        r"[需须]?(?:凭|持有?)(.*?)(?:方可|才能|才可|可以)",
        r"(?:商品|产品)须?(?:保持|保留|保证)(.*?)(?:状态|完好|完整)",
        r"以下情况(?:不|不予|不适用|除外)",
    ]
    found = []
    for pat in patterns:
        matches = re.findall(pat, text)
        found.extend([m.strip() for m in matches if m.strip()])
    return list(dict.fromkeys(found))  # deduplicate preserving order


def extract_process_steps(text: str) -> list[str]:
    """Extract numbered or arrow-separated process steps."""
    steps = []
    # Arrow / arrow-like separators
    arrow_match = re.findall(r"[→➡](.{3,50}?)(?=[→➡]|$)", text)
    if arrow_match:
        return [s.strip() for s in arrow_match if s.strip()]
    # Numbered steps
    numbered = re.findall(r"(?:^|\n)\s*\d+[.、)]\s*(.+)", text)
    if numbered:
        return [s.strip() for s in numbered]
    # Chinese enumeration
    chinese_nums = re.findall(r"[①②③④⑤⑥⑦⑧⑨⑩]\s*(.+)", text)
    if chinese_nums:
        return [s.strip() for s in chinese_nums]
    return steps


def make_policy_id(title: str, source: str) -> str:
    raw = f"{source}:{title}"
    return hashlib.md5(raw.encode()).hexdigest()[:8]


def build_policy_entry(section: dict, policy_type: str, source_doc: str) -> dict:
    title = section["title"]
    body = section["body"]
    detected_type = detect_policy_type(body) if policy_type == "general" else policy_type

    # Extract keywords from title + body
    keywords = []
    for ptype, kws in POLICY_PATTERNS.items():
        for kw in kws:
            if kw in body or kw in title:
                keywords.append(kw)
    keywords = list(dict.fromkeys(keywords))[:10]

    return {
        "policy_id": make_policy_id(title, source_doc),
        "title": title,
        "type": detected_type,
        "keywords": keywords,
        "conditions": extract_conditions(body),
        "process": extract_process_steps(body),
        "full_text": body,
        "exceptions": [],
        "effective_date": None,
        "source_doc": source_doc,
        "_flags": [] if (title and body) else ["incomplete_section"],
    }


def build_faq_entries(text: str, source_doc: str) -> list[dict]:
    """Parse Q&A style text into FAQ entries."""
    entries = []
    # Pattern: Q: ... A: ...
    qa_pairs = re.findall(r"(?:Q:|问：?|【问】)\s*(.+?)\n+(?:A:|答：?|【答】)\s*(.+?)(?=\n+(?:Q:|问：?|【问】)|$)", text, re.DOTALL)
    for i, (q, a) in enumerate(qa_pairs):
        q, a = q.strip(), a.strip()
        if not q or not a:
            continue
        keywords = [w for kws in POLICY_PATTERNS.values() for w in kws if w in q or w in a]
        entries.append({
            "faq_id": f"faq_{i+1:03d}",
            "question": q,
            "answer": a,
            "category": detect_policy_type(q + a),
            "keywords": list(dict.fromkeys(keywords))[:8],
            "source_doc": source_doc,
            "_flags": [],
        })
    return entries


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Parse policy documents into structured JSON")
    parser.add_argument("input_file", help="Path to PDF, DOCX, or TXT file")
    parser.add_argument("--output", default=None, help="Output JSON path (default: stdout)")
    parser.add_argument("--type", default="general",
                        choices=["return", "warranty", "promotion", "faq", "membership", "general"],
                        help="Policy type hint")
    args = parser.parse_args()

    filepath = Path(args.input_file)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    print(f"Extracting text from {filepath.name}...", file=sys.stderr)
    raw_text = extract_text(str(filepath))

    if not raw_text.strip():
        print("Error: No text could be extracted from the file.", file=sys.stderr)
        sys.exit(1)

    source_doc = filepath.name
    entries = []

    # If FAQ type, try Q&A extraction first
    if args.type == "faq" or detect_policy_type(raw_text) == "faq":
        faq_entries = build_faq_entries(raw_text, source_doc)
        if faq_entries:
            entries.extend(faq_entries)

    # Section-based parsing for policy docs
    if not entries:
        sections = split_into_sections(raw_text)
        for section in sections:
            entries.append(build_policy_entry(section, args.type, source_doc))

    # Fallback: treat whole doc as one entry
    if not entries:
        entries.append({
            "policy_id": make_policy_id(filepath.stem, source_doc),
            "title": filepath.stem,
            "type": detect_policy_type(raw_text),
            "keywords": [],
            "conditions": extract_conditions(raw_text),
            "process": extract_process_steps(raw_text),
            "full_text": raw_text[:3000],
            "exceptions": [],
            "effective_date": None,
            "source_doc": source_doc,
            "_flags": ["single_block_extraction"],
        })

    result = {
        "entries": entries,
        "meta": {
            "source_file": source_doc,
            "policy_type": args.type,
            "entry_count": len(entries),
            "parsed_at": datetime.utcnow().isoformat() + "Z",
        }
    }

    output_json = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output_json, encoding="utf-8")
        print(f"✅ Parsed {len(entries)} policy entries → {args.output}", file=sys.stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
