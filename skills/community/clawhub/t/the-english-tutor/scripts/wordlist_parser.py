#!/usr/bin/env python3
"""
英语助教 · 单词表解析器
支持 CSV 和纯文本格式，自动识别并输出标准 JSON 格式
用法:
  python3 scripts/wordlist_parser.py <file>          # 解析并打印 JSON
  python3 scripts/wordlist_parser.py <file> --dry-run # 仅验证，不保存
"""
import csv, json, pathlib, re, sys

COLUMNS = ["word", "pronunciation", "meaning", "example", "mastery", "next_review", "review_count"]

def parse_txt(text: str):
    """每行格式: word,中文释义  或  word 释义"""
    entries = []
    for lineno, line in enumerate(text.strip().splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # 尝试多种分隔符
        for sep in [",", "\t", "  "]:
            if sep in line:
                parts = line.split(sep, 1)
                word = parts[0].strip()
                meaning = parts[1].strip()
                break
        else:
            word, meaning = line, ""
        if not word:
            continue
        entries.append(_make_entry(word, meaning=meaning))
    return entries

def parse_csv(path: pathlib.Path):
    entries = []
    with path.open(newline="", encoding="utf-8") as f:
        # 尝试 sniffer 检测分隔符
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample)
        except Exception:
            dialect = csv.excel
        reader = csv.DictReader(f, dialect=dialect)
        headers = [h.lower().strip() for h in reader.fieldnames or []]
        # 匹配列名
        col_map = {}
        for i, h in enumerate(headers):
            for std in COLUMNS:
                if std in h or h in std:
                    col_map[std] = i
        for row in reader:
            vals = list(row.values())
            word = vals[headers.index(next((h for h in headers if 'word' in h.lower()), headers[0]))].strip()
            if not word:
                continue
            meaning = ""
            if "meaning" in col_map:
                m = vals[col_map["meaning"]].strip()
                if m:
                    meaning = m
            pronunciation = vals[col_map["pronunciation"]].strip() if "pronunciation" in col_map else ""
            example = vals[col_map["example"]].strip() if "example" in col_map else ""
            entries.append(_make_entry(word, pronunciation, meaning, example))
    return entries

def _make_entry(word="", pronunciation="", meaning="", example="", mastery=0,
                next_review="", review_count=0):
    import datetime
    return {
        "word": word.lower().strip(),
        "pronunciation": pronunciation.strip(),
        "meaning": meaning.strip(),
        "example": example.strip(),
        "mastery": mastery,
        "next_review": next_review or datetime.datetime.now().strftime("%Y-%m-%d"),
        "review_count": review_count,
        "last_review": "",
    }

def infer_pronunciation(word: str) -> str:
    """简单的音标推断（对常见词根词缀做替换），不精确但够用"""
    replacements = [
        ("tion", "ʃən"), ("sion", "ʃən"), ("ough", "ʌf"), ("ight", "aɪt"),
        ("ee", "iː"), ("ea", "iː"), ("ou", "aʊ"), ("ow", "əʊ"),
        ("ai", "eɪ"), ("ay", "eɪ"), ("ch", "tʃ"), ("sh", "ʃ"),
        ("th", "θ"), ("ng", "ŋ"), ("qu", "kw"),
    ]
    result = word.lower()
    for k, v in replacements:
        result = result.replace(k, v)
    return f"/{result}/"

def main():
    import argparse
    parser = argparse.ArgumentParser(description="解析单词表")
    parser.add_argument("file", type=pathlib.Path)
    parser.add_argument("--dry-run", action="store_true", help="仅验证，不保存")
    parser.add_argument("--output", type=pathlib.Path, help="输出 JSON 路径")
    args = parser.parse_args()

    if not args.file.exists():
        print(f"❌ 文件不存在: {args.file}", file=sys.stderr)
        sys.exit(1)

    text = args.file.read_text()
    suffix = args.file.suffix.lower()

    if suffix == ".csv":
        entries = parse_csv(args.file)
    else:
        entries = parse_txt(text)

    # 补充缺失音标
    for e in entries:
        if not e["pronunciation"]:
            e["pronunciation"] = infer_pronunciation(e["word"])

    result = {
        "total": len(entries),
        "words": entries,
        "source": str(args.file),
    }

    out_path = args.output or args.file.with_suffix(".json")
    if not args.dry_run:
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2))
        print(f"✅ 解析完成: {len(entries)} 个单词 → {out_path}")
    else:
        print(f"📋 预览（共 {len(entries)} 词）:")
        for e in entries[:5]:
            print(f"  {e['word']} {e['pronunciation']} — {e['meaning']}")
        if len(entries) > 5:
            print(f"  ... 还有 {len(entries)-5} 个")

if __name__ == "__main__":
    main()
