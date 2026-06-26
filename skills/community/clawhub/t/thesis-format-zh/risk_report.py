#!/usr/bin/env python3
"""
交付前风险检测报告

只读扫描 .docx，输出 Markdown 报告，列出所有需要人工检查的点。
不改动文件，不做自动修复。

用法：
  python3 risk_report.py 论文.docx -o 风险报告.md
  python3 risk_report.py 论文.docx --json -o 风险清单.json
"""
import argparse
import json
import os
import re
import tempfile
import zipfile
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
WPS = "http://schemas.microsoft.com/office/word/2010/wordprocessingShape"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def qw(tag):
    return f"{{{W}}}{tag}"


def qwp(tag):
    return f"{{{WP}}}{tag}"


TOC_RE = re.compile(r"TOC\s", re.I)
PAGE_RE = re.compile(r"PAGE", re.I)
NUMPAGES_RE = re.compile(r"NUMPAGES", re.I)


def find_all_footers(tmpdir):
    out = []
    word_dir = os.path.join(tmpdir, "word")
    if not os.path.isdir(word_dir):
        return out
    for fn in sorted(os.listdir(word_dir)):
        if fn.startswith("footer") and fn.endswith(".xml"):
            out.append(os.path.join(word_dir, fn))
    return out


def find_all_headers(tmpdir):
    out = []
    word_dir = os.path.join(tmpdir, "word")
    if not os.path.isdir(word_dir):
        return out
    for fn in sorted(os.listdir(word_dir)):
        if fn.startswith("header") and fn.endswith(".xml"):
            out.append(os.path.join(word_dir, fn))
    return out


def parse_document(tmpdir):
    doc_xml = os.path.join(tmpdir, "word", "document.xml")
    if not os.path.exists(doc_xml):
        return None, None
    tree = etree.parse(doc_xml)
    root = tree.getroot()
    body = root.find(qw("body"))
    return tree, body


def analyse_sections(body):
    """检测分节符、页码设置、页眉页脚链接。"""
    issues = []
    sections = []
    last_sect = body.find(qw("sectPr"))
    # also check sectPr inside body (usually last), and sectPr inside paragraphs (section breaks)
    for i, child in enumerate(body):
        if child.tag == qw("p"):
            ppr = child.find(qw("pPr"))
            if ppr is not None:
                sect = ppr.find(qw("sectPr"))
                if sect is not None:
                    sections.append(("分节符(段落)", i, sect))
                else:
                    section_break = False
                    for r in child.findall(qw("r")):
                        for br in r.findall(qw("br")):
                            if br.get(qw("type")) == "section":
                                section_break = True
                    if section_break:
                        sections.append(("分节符(换行)", i, ppr.find(qw("sectPr"))))

    # final section properties
    if last_sect is not None:
        sections.append(("文档末节", -1, last_sect))

    for sec_idx, (label, para_idx, sect) in enumerate(sections):
        sec_issues = []
        pgNumType = None
        titlePg = None
        for el in sect:
            if el.tag == qw("pgNumType"):
                pgNumType = el
            elif el.tag == qw("titlePg"):
                titlePg = el
        # header/footer references
        for el in sect.iter():
            if el.tag in (qw("headerReference"), qw("footerReference")):
                pass  # we check footer files separately

        if pgNumType is not None:
            fmt = pgNumType.get(qw("fmt"), "decimal")
            start = pgNumType.get(qw("start"))
            if start:
                sec_issues.append(f"起始页码设为 {start}")
        else:
            sec_issues.append("未设置页码格式(默认续前)")

        if titlePg is not None:
            sec_issues.append("首页不同(标题页模式)")
        if sec_issues:
            issues.append({
                "kind": "section",
                "section_index": sec_idx,
                "label": f"第 {sec_idx+1} 节 ({label})",
                "paragraph_index": para_idx,
                "details": sec_issues,
            })

    return issues, sections


def analyse_footers(tmpdir, sections):
    """检查页脚文件和页码格式一致性。"""
    issues = []
    footer_files = find_all_footers(tmpdir)
    if not footer_files:
        issues.append({"kind": "footer", "label": "全局", "details": ["无页脚文件(可能无页码)"]})
        return issues

    for fp in footer_files:
        tree = etree.parse(fp)
        root = tree.getroot()
        f_issues = []
        has_page_field = False
        has_page_run = False
        field_count = 0

        for el in root.iter():
            if el.tag == qw("instrText") and el.text and PAGE_RE.search(el.text):
                has_page_field = True
                field_count += 1
            if el.tag == qw("fldChar"):
                has_page_field = True

        # check font/size used in page number runs
        fonts = set()
        sizes = set()
        for rpr in root.findall(f".//{qw('rPr')}"):
            rf = rpr.find(qw("rFonts"))
            if rf is not None:
                for attr in ("ascii", "hAnsi", "eastAsia"):
                    v = rf.get(qw(attr))
                    if v:
                        fonts.add(v)
            sz = rpr.find(qw("sz"))
            if sz is not None:
                sizes.add(sz.get(qw("val")))

        if fonts:
            f_issues.append(f"页码字体: {', '.join(sorted(fonts))}")
        if sizes:
            f_issues.append(f"页码字号(半磅): {', '.join(sorted(sizes))}")

        basename = os.path.basename(fp)
        if has_page_field:
            f_issues.append(f"含 {field_count} 个 PAGE 域")
        else:
            f_issues.append("⚠️ 未检测到 PAGE 域(可能无页码)")

        if f_issues:
            issues.append({
                "kind": "footer",
                "label": f"页脚: {basename}",
                "details": f_issues,
            })

    return issues


def analyse_images(body):
    """检测文档中的图片及其定位方式。"""
    issues = []
    for i, child in enumerate(body):
        if child.tag != qw("p"):
            continue
        drawings = child.findall(f".//{qw('drawing')}")
        if not drawings:
            continue
        for d_idx, d in enumerate(drawings):
            d_issues = []
            # Check inline vs anchored
            inline = d.find(f".//{qwp('inline')}")
            anchor = d.find(f".//{qwp('anchor')}")
            if anchor is not None:
                d_issues.append("浮动定位(anchor)，可能在页面间漂移")
            # Check size
            extent = d.find(f".//{qwp('extent')}")
            if extent is not None:
                cx = int(extent.get("cx", "0"))
                cy = int(extent.get("cy", "0"))
                # ~11906 EMU per mm, A4 printable width ~160mm, height ~247mm
                w_mm = cx / 360000
                h_mm = cy / 360000
                if w_mm > 150:
                    d_issues.append(f"图片过宽({w_mm:.0f}mm)可能超出版心")
                if h_mm > 200:
                    d_issues.append(f"图片过高({h_mm:.0f}mm)可能跨页")
            if d_issues:
                issues.append({
                    "kind": "image",
                    "paragraph_index": i,
                    "image_index": d_idx,
                    "details": d_issues,
                })
    return issues


def analyse_tables(body):
    """检测表格跨页风险。"""
    issues = []
    for i, child in enumerate(body):
        if child.tag != qw("tbl"):
            continue
        t_issues = []
        # count rows, check header repeat
        rows = child.findall(qw("tr"))
        if len(rows) > 15:
            t_issues.append(f"表格 {len(rows)} 行，可能跨页")
        # check tblPr for header row repeat
        tblPr = child.find(qw("tblPr"))
        if tblPr is not None:
            header = tblPr.find(qw("tblHeader"))
            if header is None:
                t_issues.append("未设置标题行重复(跨页无表头)")
        # check for merged cells
        for row in rows:
            for tc in row.findall(qw("tc")):
                tcPr = tc.find(qw("tcPr"))
                if tcPr is not None:
                    gridSpan = tcPr.find(qw("gridSpan"))
                    vMerge = tcPr.find(qw("vMerge"))
                    if gridSpan is not None:
                        span = int(gridSpan.get(qw("val"), "1"))
                        if span > 1:
                            t_issues.append("含横向合并单元格")
        if t_issues:
            issues.append({
                "kind": "table",
                "paragraph_index": i,
                "row_count": len(rows),
                "details": list(dict.fromkeys(t_issues)),  # dedupe
            })
    return issues


def analyse_toc(body):
    """检测目录域是否过期。"""
    issues = []
    for i, child in enumerate(body):
        if child.tag != qw("p"):
            continue
        for instr in child.findall(f".//{qw('instrText')}"):
            if instr.text and TOC_RE.search(instr.text):
                issues.append({
                    "kind": "toc",
                    "paragraph_index": i,
                    "field_code": instr.text.strip(),
                    "details": ["目录域存在，交付前请右键 → 更新域 → 更新整个目录"],
                })
    return issues


def analyse_empty_paragraphs(body):
    """检测空段、纯空白段、可疑多余分页。"""
    issues = []
    empty_indices = []
    manual_breaks = []
    for i, child in enumerate(body):
        if child.tag != qw("p"):
            continue
        text = "".join(t.text or "" for t in child.findall(f".//{qw('t')}")).strip()
        if not text:
            empty_indices.append(i)
        # Manual page breaks
        for r in child.findall(qw("r")):
            for br in r.findall(qw("br")):
                if br.get(qw("type")) == "page":
                    manual_breaks.append(i)
    if empty_indices:
        issues.append({
            "kind": "empty_paragraphs",
            "count": len(empty_indices),
            "paragraph_indices": empty_indices if len(empty_indices) <= 20 else empty_indices[:20] + ["..."],
            "details": [f"共 {len(empty_indices)} 个空段落，可能造成多余空白。请检查排版效果。"],
        })
    if manual_breaks:
        issues.append({
            "kind": "manual_page_breaks",
            "count": len(manual_breaks),
            "paragraph_indices": manual_breaks,
            "details": [f"共 {len(manual_breaks)} 处手动分页，建议用分节符或段前分页替代。"],
        })
    return issues


def analyse_residual_ops(paper_path, template_path, module_regions=None):
    """检测 residual ops 并按模块分类。

    module_regions: list of (module_id, para_start, para_end) from module_orchestrator
    """
    from diff import diff as run_diff
    from reader import classify_and_dump

    rules, _ = classify_and_dump(str(template_path))
    fix_types = {'h1','h2','h3','body','abstract_title','abstract_body','abstract_keywords_cn',
                 'abstract_title_cn','abstract_title_en','abstract_body_en','abstract_keywords_en',
                 'refs_title','refs_body','ack_title','ack_body',
                 'fig_caption','table_caption','toc_title','toc_entry','conclusion_title'}
    all_ops = run_diff(str(paper_path), rules, fix_types=fix_types, enable_global_ops=False)
    para_ops = [op for op in all_ops if 'para' in op]

    if not module_regions:
        return [{'kind': 'residual_ops', 'label': '全文', 'total_ops': len(para_ops), 'modules': {}}]

    # 按模块归类
    by_module = {}
    for op in para_ops:
        idx = op['para']
        found = False
        for mod_id, start, end in module_regions:
            if start <= idx < end:
                by_module.setdefault(mod_id, []).append(idx)
                found = True
                break
        if not found:
            by_module.setdefault('_unmapped', []).append(idx)

    issues = []
    for mod_id, indices in sorted(by_module.items()):
        n = len(indices)
        label = {
            'cover': '封面', 'statement': '声明', 'abstract_cn': '中文摘要',
            'abstract_en': '英文摘要', 'toc': '目录', 'chapter': '章节',
            'refs': '参考文献', 'ack': '致谢', 'appendix': '附录',
        }.get(mod_id, mod_id)
        issues.append({
            'kind': 'residual_ops',
            'module_id': mod_id,
            'label': label,
            'count': n,
            'sample_paras': sorted(set(indices))[:5],
        })

    return issues


def analyse_cover_page(body):
    """检测封面/声明页风险。"""
    issues = []
    # Look for common patterns that suggest a cover page section
    first_paras = []
    for child in body:
        if child.tag != qw("p"):
            continue
        text = "".join(t.text or "" for t in child.findall(f".//{qw('t')}")).strip()
        if text:
            first_paras.append(text[:60])
            if len(first_paras) >= 5:
                break

    cover_keywords = ["论文", "大学", "学院", "指导老师", "指导教师", "专业", "学号", "班级", "声明", "原创", "学位"]
    found = [kw for kw in cover_keywords if any(kw in t for t in first_paras)]
    if found:
        issues.append({
            "kind": "cover_page",
            "details": [f"疑似封面/声明页(含关键词: {', '.join(found)})，请人工核实格式。"],
        })
    return issues


def generate_report(all_issues, filename, sections_count):
    """生成 Markdown 风险报告。"""
    by_kind = defaultdict(list)
    for item in all_issues:
        by_kind[item["kind"]].append(item)

    lines = []
    lines.append("# 📋 论文交付前风险检测报告")
    lines.append("")
    lines.append(f"- **文件**: `{Path(filename).name}`")
    lines.append(f"- **生成时间**: {datetime.now():%Y-%m-%d %H:%M:%S}")
    lines.append(f"- **风险项总计**: {len(all_issues)}")
    lines.append(f"- **分节数**: {sections_count}")
    lines.append("")

    # Summary
    lines.append("## 📊 总览")
    lines.append("")
    lines.append("| 类别 | 数量 |")
    lines.append("|------|-----:|")
    for kind in ["section", "footer", "image", "table", "toc", "empty_paragraphs", "manual_page_breaks", "cover_page", "residual_ops"]:
        count = len(by_kind.get(kind, []))
        if count == 0 and kind not in ("toc", "cover_page"):
            continue
        label = {
            "section": "分节与页码",
            "footer": "页脚页码",
            "image": "图片布局",
            "table": "表格布局",
            "toc": "目录域",
            "empty_paragraphs": "空段落",
            "manual_page_breaks": "手动分页",
            "cover_page": "封面/声明页",
            "residual_ops": "格式残留(ops)",
        }.get(kind, kind)
        lines.append(f"| {label} | {count} |")
    lines.append("")

    # Detail per kind
    kind_order = ["section", "footer", "image", "table", "toc", "empty_paragraphs", "manual_page_breaks", "cover_page", "residual_ops"]

    for kind in kind_order:
        items = by_kind.get(kind, [])
        if not items:
            continue
        kind_label = {
            "section": "## 📐 分节与页码",
            "footer": "## 📄 页脚页码",
            "image": "## 🖼️ 图片布局",
            "table": "## 📊 表格布局",
            "toc": "## 📑 目录域",
            "empty_paragraphs": "## ⬜ 空段落",
            "manual_page_breaks": "## ✂️ 手动分页",
            "cover_page": "## 🏷️ 封面/声明页",
            "residual_ops": "## 📝 格式残留 (residual ops)",
        }.get(kind, f"## {kind}")
        lines.append(kind_label)
        lines.append("")
        for item in items:
            label = item.get("label", "")
            if kind == "empty_paragraphs":
                indices = item.get("paragraph_indices", [])
                preview = ", ".join(str(x) for x in (indices[:10] if isinstance(indices, list) else indices))
                lines.append(f"- **{item['count']} 个空段落** (段: {preview})")
                for d in item["details"]:
                    lines.append(f"  - {d}")
            elif kind == "manual_page_breaks":
                lines.append(f"- **{item['count']} 处手动分页**")
                for d in item["details"]:
                    lines.append(f"  - {d}")
            elif kind == "residual_ops":
                n = item.get('count', 0)
                mod = item.get('label', '?')
                paras = item.get('sample_paras', [])
                pv = ','.join(str(p) for p in paras[:5])
                flag = '⚠️' if n > 20 else '✅'
                lines.append(f"- {flag} **{mod}**: {n} ops" + (f' (段: {pv})' if pv else ''))
            else:
                prefix = f"- {label}: " if label else "- "
                lines.append(f"{prefix}" + item["details"][0])
                for d in item["details"][1:]:
                    lines.append(f"  - {d}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 🛠️ 建议操作")
    lines.append("")
    lines.append("| 类别 | 操作 |")
    lines.append("|------|------|")
    lines.append("| 目录域 | WPS/Word 中右键目录 → 更新域 → 更新整个目录 |")
    lines.append("| 页眉域 | WPS/Word 中 Ctrl+A 全选 → F9 更新域 → 页眉章节名才会显示 |")
    lines.append("| 封面/声明页 | 人工核实字体、字号、对齐、换页 |")
    lines.append("| 分节页码 | 双击页脚检查每节起始页码、首页不同 |")
    lines.append("| 图片漂移 | 将图片设为嵌入型(非浮动)，避免打印偏移 |")
    lines.append("| 表格跨页 | 检查长表格，设置标题行重复 + 允许跨页断行 |")
    lines.append("| 空段落 | 逐个确认是否多余，建议用段前段后间距替代空段 |")
    lines.append("| 手动分页 | 用「段前分页」或分节符替代 Ctrl+Enter |")
    lines.append("")

    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="论文交付前风险检测报告")
    ap.add_argument("docx", help="目标论文 .docx")
    ap.add_argument("-o", "--output", help="输出 Markdown 报告")
    ap.add_argument("--json", help="输出 JSON 原始数据")
    ap.add_argument("--template", "-t", help="学校模板（用于 residual ops 分类）")
    ap.add_argument("--modules-json", help="模块边界 JSON（来自 module_orchestrator）")
    args = ap.parse_args()

    src = Path(args.docx).expanduser().resolve()
    if not src.exists():
        raise SystemExit(f"文件不存在: {src}")

    tmpdir = tempfile.mkdtemp(prefix="risk_")
    all_issues = []
    sections_count = 0
    try:
        with zipfile.ZipFile(src, "r") as z:
            z.extractall(tmpdir)
        _, body = parse_document(tmpdir)
        if body is None:
            raise SystemExit("无法解析 document.xml")

        # 1. Sections & page numbering
        sec_issues, sections = analyse_sections(body)
        all_issues.extend(sec_issues)
        sections_count = len([s for s in sections if s[2] is not None])

        # 2. Footer/header checks
        all_issues.extend(analyse_footers(tmpdir, sections))

        # 3. Images
        all_issues.extend(analyse_images(body))

        # 4. Tables
        all_issues.extend(analyse_tables(body))

        # 5. TOC
        all_issues.extend(analyse_toc(body))

        # 6. Empty paragraphs, manual breaks
        all_issues.extend(analyse_empty_paragraphs(body))

        # 7. Cover page guess
        all_issues.extend(analyse_cover_page(body))

    finally:
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)

    # 8. Residual ops by module (不依赖 tmpdir)
    if args.template:
        regions = None
        if args.modules_json and Path(args.modules_json).exists():
            import json as _json
            with open(args.modules_json) as f:
                regions = _json.load(f)
        all_issues.extend(analyse_residual_ops(str(src), args.template, regions))

    report = generate_report(all_issues, src.name, sections_count)

    out = Path(args.output).expanduser().resolve() if args.output else src.with_suffix(".risk.md")
    out.write_text(report, encoding="utf-8")
    print(f"✅ 风险报告: {out}")
    print(f"   共 {len(all_issues)} 项风险")

    if args.json:
        jout = Path(args.json).expanduser().resolve()
        jout.write_text(json.dumps(all_issues, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ JSON: {jout}")


if __name__ == "__main__":
    main()
