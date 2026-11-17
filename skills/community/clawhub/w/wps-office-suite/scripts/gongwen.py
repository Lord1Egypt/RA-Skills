# -*- coding: utf-8 -*-
"""
公文一键排版引擎 v5.2
依据 references/gongwen_rules.yaml（GB/T 9704-2012 党政机关公文格式）对文档逐段识别结构
（标题/主送/正文/落款/附注）并套版。
支持：
  - 红头预留位（--redhead）
  - 联合行文（--joint）
  - 处理前自动备份原文件
零外部 API；仅依赖 python-docx（与全家桶既有模块一致）。

死规则合规：规则9（基础功能自研）规则10（不拖累设备）规则13（不生成禁止文件）
"""
import sys
import os
import re
import json
import shutil
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

try:
    import yaml
except ImportError:
    yaml = None

try:
    from docx import Document
    from docx.shared import Pt, RGBColor, Mm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.text import WD_LINE_SPACING
    from docx.oxml.ns import qn
except ImportError:
    Document = None

SCRIPT_DIR = Path(__file__).parent
RULES_PATH = SCRIPT_DIR.parent / "references" / "gongwen_rules.yaml"

# 字号 → 磅值 映射
SIZE_PT = {
    "初号": 42, "小初": 36, "一号": 26, "小一": 24, "二号": 22, "小二": 18,
    "三号": 16, "小三": 15, "四号": 14, "小四": 12, "五号": 10.5, "小五": 9,
}

DATE_RE = re.compile(r"(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)|(\d{4}[-/]\d{1,2}[-/]\d{1,2})")


def load_rules() -> Dict[str, Any]:
    if yaml is None:
        raise RuntimeError("需要 pyyaml：pip install pyyaml")
    if not RULES_PATH.exists():
        raise RuntimeError(f"规则库缺失：{RULES_PATH}")
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def size_to_pt(size: str) -> int:
    return SIZE_PT.get(size, 16)


def set_run_font(run, name: str, fallback: str, size_pt: int,
                 bold: bool = False, color_hex: str = "000000"):
    """设置 run 字体（含东亚字体属性，避免中文回退为西文字体）"""
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run._element.rPr.rFonts.set(qn("w:ascii"), name)
    run._element.rPr.rFonts.set(qn("w:hAnsi"), name)
    # 兜底字体记录
    run._element.rPr.rFonts.set(qn("w:cs"), fallback)
    try:
        run.font.color.rgb = RGBColor.from_string(color_hex)
    except Exception:
        pass


def apply_para_style(p, spec: Dict[str, Any], text: str = ""):
    """按规则库 spec 应用段落样式"""
    name = spec.get("name", "仿宋")
    fallback = spec.get("fallback", "仿宋")
    size_pt = size_to_pt(spec.get("size", "三号"))
    bold = spec.get("bold", False)
    color = spec.get("color", "000000")
    align = spec.get("align", "left")

    align_map = {
        "center": WD_ALIGN_PARAGRAPH.CENTER,
        "left": WD_ALIGN_PARAGRAPH.LEFT,
        "right": WD_ALIGN_PARAGRAPH.RIGHT,
        "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
    }
    p.alignment = align_map.get(align, WD_ALIGN_PARAGRAPH.LEFT)

    # 首行缩进
    indent = spec.get("first_line_indent")
    if indent == "2字符":
        p.paragraph_format.first_line_indent = Pt(size_pt * 2)
    elif indent == "0":
        p.paragraph_format.first_line_indent = Pt(0)

    # 行距
    if spec.get("line_spacing_rule") == "fixed" and spec.get("line_spacing"):
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        try:
            val = float(str(spec["line_spacing"]).replace("pt", ""))
            p.paragraph_format.line_spacing = val
        except Exception:
            pass

    # 段后间距
    if spec.get("spacing_after"):
        p.paragraph_format.space_after = Pt(size_pt)

    # 清空并重建 runs（保证整段统一字体）
    for r in list(p.runs):
        r._element.getparent().remove(r._element)
    run = p.add_run(text if text else (p.text or ""))
    set_run_font(run, name, fallback, size_pt, bold, color)


def detect_structure(paras: List[str], rules: Dict[str, Any]) -> Dict[int, str]:
    """逐段识别结构类型，返回 {段落索引: 类型}"""
    doc_types = rules.get("doc_types", [])
    main_markers = rules.get("main_send_markers", ["：", ":"])
    result: Dict[int, str] = {}
    n = len(paras)

    # 标题：首个非空段
    title_idx = None
    for i, t in enumerate(paras):
        if t.strip():
            title_idx = i
            break

    for i, t in enumerate(paras):
        s = t.strip()
        if not s:
            result[i] = "empty"
            continue
        if i == title_idx:
            result[i] = "title"
            continue

        # 落款：含日期且靠近文末
        if DATE_RE.search(s) and i >= n - 4:
            result[i] = "signature"
            continue

        # 附注：文末圆括号段
        if s.startswith("（") or s.startswith("("):
            if i >= n - 3:
                result[i] = "annotation"
                continue

        # 主送：以全角/半角冒号结尾且含顿号或逗号（机构列表）
        if any(s.endswith(m) for m in main_markers) and ("、" in s or "，" in s or "," in s):
            result[i] = "main_send"
            continue

        result[i] = "body"

    return result


def detect_level(text: str, rules: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """检测正文段首的结构层次序数，返回对应字体 spec 或 None"""
    levels = rules.get("structure_levels", [])
    for lv in levels:
        marker = lv.get("marker", "")
        if text.strip().startswith(marker):
            return lv
    return None


def layout(filepath: str, output: str = "", redhead: bool = False,
           joint: bool = False, rules: Dict[str, Any] = None) -> Dict[str, Any]:
    """对文档套用公文格式，返回结果字典"""
    if Document is None:
        return {"success": False, "error": "需要 python-docx：pip install python-docx"}
    if rules is None:
        rules = load_rules()

    src = Path(filepath).resolve()
    if not src.exists():
        return {"success": False, "error": f"文件不存在：{filepath}"}

    # 备份原文件
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = src.parent / f"{src.stem}_gongwen_backup_{ts}{src.suffix}"
    shutil.copy2(src, backup)

    # 读取段落文本
    ext = src.suffix.lower()
    if ext == ".docx":
        doc = Document(str(src))
        paras = [p.text for p in doc.paragraphs]
    elif ext in (".txt", ".md"):
        with open(src, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        # 按行保留空行以识别结构
        paras = content.split("\n")
        doc = Document()
        # 为 txt/md 重建段落，使 doc.paragraphs 与 paras 一一对应
        for line in paras:
            doc.add_paragraph(line)
    else:
        return {"success": False, "error": f"不支持的文件类型：{ext}（支持 .docx/.txt/.md）"}

    struct = detect_structure(paras, rules)
    fonts = rules.get("fonts", {})

    # 逐段套版
    changed = 0
    for i, p in enumerate(doc.paragraphs):
        if i >= len(paras):
            break
        text = paras[i]
        stype = struct.get(i, "body")

        if stype == "empty":
            continue
        elif stype == "title":
            apply_para_style(p, fonts.get("title", {}), text)
        elif stype == "main_send":
            apply_para_style(p, fonts.get("main_send", {}), text)
        elif stype == "signature":
            apply_para_style(p, fonts.get("signature", {}), text)
        elif stype == "annotation":
            apply_para_style(p, fonts.get("annotation", {}), text)
        else:  # body
            lv = detect_level(text, rules)
            if lv:
                lv_spec = {
                    "name": lv.get("font", "仿宋_GB2312"),
                    "fallback": lv.get("fallback", "仿宋"),
                    "size": lv.get("size", "三号"),
                    "bold": lv.get("bold", False),
                    "align": "justify",
                    "first_line_indent": "2字符",
                    "line_spacing_rule": "fixed",
                    "line_spacing": "28pt",
                }
                apply_para_style(p, lv_spec, text)
            else:
                apply_para_style(p, fonts.get("body", {}), text)
        changed += 1

    # 红头预留位（套版后插入文档最前，避免干扰段落索引）
    if redhead:
        gap = rules.get("redhead_line_gap", 2)
        ph = rules.get("redhead_placeholder", "[红头：发文机关标志预留位]")
        redhead_spec = fonts.get("redhead", fonts.get("title", {}))
        body = doc.element.body
        first_p = body.find(qn("w:p"))
        rp = doc.add_paragraph()
        apply_para_style(rp, redhead_spec, ph)
        if first_p is not None:
            first_p.addprevious(rp._element)
        else:
            body.append(rp._element)
        # 空行间隔
        for _ in range(gap):
            gp = doc.add_paragraph()
            rp._element.addnext(gp._element)

    # 联合行文：落款段追加提示（多机关并排由用户在红头/署名处填写，引擎保证署名右对齐）
    if joint:
        # 在文档属性或末段注释中记录，便于审阅
        core = doc.core_properties
        core.comments = (core.comments or "") + " [联合行文模式]"

    out_path = output or str(src.parent / f"{src.stem}_公文版{src.suffix}")
    doc.save(out_path)

    return {
        "success": True,
        "output": out_path,
        "backup": str(backup),
        "processed_paragraphs": changed,
        "redhead": redhead,
        "joint": joint,
    }


def cmd_layout(args):
    rules = load_rules()
    result = layout(args.file, args.output, args.redhead, args.joint, rules)
    if result.get("success"):
        print(f"✅ 排版完成：{result['output']}")
        print(f"📋 备份原文件：{result['backup']}")
        print(f"📊 处理段落数：{result['processed_paragraphs']}")
    else:
        print(f"❌ {result.get('error', '未知错误')}")
    return 0 if result.get("success") else 1


def main():
    parser = argparse.ArgumentParser(description="公文一键排版引擎 v5.2（GB/T 9704）")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("layout", help="对文档套用公文格式")
    p.add_argument("--file", required=True, help="输入文档路径（.docx/.txt/.md）")
    p.add_argument("--output", default="", help="输出路径（默认 <名>_公文版.docx）")
    p.add_argument("--redhead", action="store_true", help="插入红头预留位")
    p.add_argument("--joint", action="store_true", help="联合行文模式")
    p.set_defaults(func=cmd_layout)

    args = parser.parse_args()
    if not getattr(args, "command", None):
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
