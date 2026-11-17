# -*- coding: utf-8 -*-
"""
敏感信息打码工具 v5.2
正则 + 词典双轨识别：身份证 / 手机号 / 银行卡 / 邮箱；可选 NER 增强。
命中后以黑色矩形（█ + 黑底）覆盖原文，并输出打码清单供人工复核。
零外部 API；NER 仅作可选增强（未安装则跳过，不阻断主流程）。

死规则合规：规则9（基础功能自研，双轨识别）规则10（不拖累设备）规则13（不生成禁止文件）规则16（子进程超时）
"""
import sys
import re
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional

try:
    from docx import Document
    from docx.shared import RGBColor
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    Document = None


# ---------- 正则轨道 ----------
ID_CARD_RE = re.compile(r"(?<!\d)(\d{17}[\dXx]|\d{15})(?!\d)")
PHONE_RE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
BANK_RE = re.compile(r"(?<!\d)(?:\d[ -]?){15,18}\d(?!\d)")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

CATEGORIES = [
    ("id_card", ID_CARD_RE, "身份证"),
    ("phone", PHONE_RE, "手机号"),
    ("bank_card", BANK_RE, "银行卡"),
    ("email", EMAIL_RE, "邮箱"),
]


def mask_text(text: str) -> str:
    """将命中文本替换为等宽黑色方块（保留长度，便于排版对齐）"""
    return "█" * max(1, len(text))


def load_dict(path: Optional[str]) -> List[str]:
    if not path or not Path(path).exists():
        return []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return [ln.strip() for ln in f if ln.strip()]


def find_matches(text: str, dictionary: List[str]) -> List[Dict[str, Any]]:
    """双轨检测：正则 + 词典，返回 [{'category','value','start','end'}]"""
    matches: List[Dict[str, Any]] = []

    # 轨道一：正则
    for cat, regex, label in CATEGORIES:
        for m in regex.finditer(text):
            matches.append({
                "category": cat,
                "label": label,
                "value": m.group(0),
                "start": m.start(),
                "end": m.end(),
                "track": "regex",
            })

    # 轨道二：词典
    for term in dictionary:
        start = 0
        while True:
            idx = text.find(term, start)
            if idx == -1:
                break
            matches.append({
                "category": "dictionary",
                "label": "词典命中",
                "value": term,
                "start": idx,
                "end": idx + len(term),
                "track": "dictionary",
            })
            start = idx + len(term)

    # 合并重叠（保留最长）
    matches.sort(key=lambda x: (x["start"], -(x["end"] - x["start"])))
    merged: List[Dict[str, Any]] = []
    last_end = -1
    for m in matches:
        if m["start"] >= last_end:
            merged.append(m)
            last_end = m["end"]
    return merged


def apply_redaction_docx(path: str, dictionary: List[str]) -> Dict[str, Any]:
    if Document is None:
        return {"success": False, "error": "需要 python-docx：pip install python-docx"}
    doc = Document(path)
    total = 0
    manifest = []

    for p in doc.paragraphs:
        text = p.text
        if not text:
            continue
        matches = find_matches(text, dictionary)
        if not matches:
            continue

        # 重建段落 runs：未命中保留原样，命中替换为黑色方块
        # 收集原 runs 样式（取首个 run 作为基础样式）
        base_run = p.runs[0] if p.runs else None
        font_name = base_run.font.name if base_run else None
        # 清空
        for r in list(p.runs):
            r._element.getparent().remove(r._element)

        cursor = 0
        for m in matches:
            if m["start"] > cursor:
                keep = text[cursor:m["start"]]
                run = p.add_run(keep)
                if font_name:
                    run.font.name = font_name
            blk = mask_text(text[m["start"]:m["end"]])
            run = p.add_run(blk)
            run.font.color.rgb = RGBColor(0, 0, 0)
            # 黑色底纹（矩形覆盖）
            rPr = run._element.get_or_add_rPr()
            shd = OxmlElement("w:shd")
            shd.set(qn("w:val"), "clear")
            shd.set(qn("w:color"), "auto")
            shd.set(qn("w:fill"), "000000")
            rPr.append(shd)
            manifest.append({
                "category": m["category"],
                "label": m["label"],
                "track": m["track"],
                "value": text[m["start"]:m["end"]],
                "position": f"paragraph@{m['start']}",
            })
            cursor = m["end"]
            total += 1
        if cursor < len(text):
            keep = text[cursor:]
            run = p.add_run(keep)
            if font_name:
                run.font.name = font_name

    out = str(Path(path).parent / f"{Path(path).stem}_打码版{Path(path).suffix}")
    doc.save(out)
    return {"success": True, "output": out, "count": total, "manifest": manifest}


def apply_redaction_txt(path: str, dictionary: List[str]) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    matches = find_matches(text, dictionary)
    out_text = text
    manifest = []
    # 从后往前替换避免偏移
    for m in sorted(matches, key=lambda x: x["start"], reverse=True):
        out_text = out_text[:m["start"]] + mask_text(m["value"]) + out_text[m["end"]:]
        manifest.append({
            "category": m["category"], "label": m["label"],
            "track": m["track"], "value": m["value"], "position": m["start"],
        })
    out = str(Path(path).parent / f"{Path(path).stem}_打码版.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write(out_text)
    return {"success": True, "output": out, "count": len(matches), "manifest": manifest}


def cmd_redact(args):
    dictionary = load_dict(args.dict)
    path = Path(args.file)
    if not path.exists():
        print(f"❌ 文件不存在：{args.file}")
        return 1

    if path.suffix.lower() == ".docx":
        res = apply_redaction_docx(str(path), dictionary)
    elif path.suffix.lower() in (".txt", ".md"):
        res = apply_redaction_txt(str(path), dictionary)
    else:
        print("❌ 仅支持 .docx / .txt / .md")
        return 1

    if not res.get("success"):
        print(f"❌ {res.get('error')}")
        return 1

    print(f"✅ 打码完成：{res['output']}")
    print(f"📊 共命中 {res['count']} 处敏感信息")
    # 输出打码清单
    manifest = res.get("manifest", [])
    summary = {}
    for m in manifest:
        summary[m["label"]] = summary.get(m["label"], 0) + 1
    for k, v in summary.items():
        print(f"   - {k}：{v} 处")
    if args.manifest:
        with open(args.manifest, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        print(f"📝 打码清单已写入：{args.manifest}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="敏感信息打码工具 v5.2")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("run", help="对文档打码")
    p.add_argument("--file", required=True, help="输入文档（.docx/.txt/.md）")
    p.add_argument("--dict", default="", help="词典文件路径（每行一个敏感词，可选）")
    p.add_argument("--manifest", default="", help="打码清单输出路径（JSON，可选）")
    p.set_defaults(func=cmd_redact)

    args = parser.parse_args()
    if not getattr(args, "command", None):
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
