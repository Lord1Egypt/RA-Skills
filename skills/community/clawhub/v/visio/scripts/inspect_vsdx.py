#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inspect_vsdx.py — 解析 .vsdx 文件，输出页/形状/文本/连线的结构化摘要。

用法:
    python inspect_vsdx.py <file.vsdx> [--json]

说明:
    - 不依赖 Visio 安装，直接按 OPC 包解包解析 XML。
    - 默认输出 Markdown 摘要；--json 输出 JSON。
"""
import argparse
import json
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = {
    "v": "http://schemas.microsoft.com/office/visio/2012/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def q(ns, tag):
    return "{%s}%s" % (NS[ns], tag)


def parse_rels(zf, part):
    """解析 *_rels/*.rels，返回 {Id: Target}"""
    try:
        data = zf.read(part)
    except KeyError:
        return {}
    root = ET.fromstring(data)
    return {rel.get("Id"): rel.get("Target") for rel in root.findall(q("rel", "Relationship"))}


def cell(shape, name):
    for c in shape.findall(q("v", "Cell")):
        if c.get("N") == name:
            return c.get("V")
    return None


def sec_rows(shape, sec_name):
    for s in shape.findall(q("v", "Section")):
        if s.get("N") == sec_name:
            return s.findall(q("v", "Row"))
    return []


def parse_page(zf, page_part):
    root = ET.fromstring(zf.read(page_part))
    shapes = []
    for sh in root.iter(q("v", "Shape")):
        texts = [t for t in sh.findall(q("v", "Text"))]
        text = "".join(texts[0].itertext()).strip() if texts else ""
        shapes.append(
            {
                "id": sh.get("ID"),
                "type": sh.get("Type", "Shape"),
                "name": sh.get("NameU") or sh.get("Name") or "",
                "master": sh.get("Master"),
                "text": text[:80],
                "pin_x": cell(sh, "PinX"),
                "pin_y": cell(sh, "PinY"),
                "width": cell(sh, "Width"),
                "height": cell(sh, "Height"),
                "is_connector": sh.get("BeginX") is not None,
            }
        )
    connects = []
    for c in root.iter(q("v", "Connect")):
        connects.append(
            {
                "from_sheet": c.get("FromSheet"),
                "to_sheet": c.get("ToSheet"),
                "from_cell": c.get("FromCell"),
                "to_cell": c.get("ToCell"),
            }
        )
    return {"shapes": shapes, "connects": connects}


def inspect(path):
    result = {"file": path, "pages": []}
    with zipfile.ZipFile(path) as zf:
        # 找到主文档部件
        root_rels = parse_rels(zf, "_rels/.rels")
        doc_part = next((t for t in root_rels.values() if t.endswith("document.xml")), None)
        if not doc_part:
            raise SystemExit("未找到 visio/document.xml，不是有效的 .vsdx 文件")
        doc_rels = parse_rels(zf, "visio/_rels/document.xml.rels")
        pages_part = next((t for t in doc_rels.values() if t.endswith("pages.xml")), None)
        if not pages_part:
            raise SystemExit("未找到 pages.xml")
        pages_rels = parse_rels(zf, "visio/pages/_rels/pages.xml.rels")
        pages_root = ET.fromstring(zf.read("visio/" + pages_part if not pages_part.startswith("visio/") else pages_part))
        for page in pages_root.findall(q("v", "Page")):
            rel_elem = page.find(q("v", "Rel"))
            rid = rel_elem.get(q("r", "id")) if rel_elem is not None else None
            target = pages_rels.get(rid, "")
            page_info = {
                "id": page.get("ID"),
                "name": page.get("NameU") or page.get("Name") or "",
                "part": target,
            }
            if target:
                part = "visio/pages/" + target if not target.startswith("visio/") else target
                try:
                    parsed = parse_page(zf, part)
                    page_info.update(parsed)
                except KeyError:
                    page_info["error"] = "页面部件缺失: " + part
            result["pages"].append(page_info)
    return result


def to_markdown(info):
    lines = ["# %s 结构摘要" % info["file"], ""]
    for p in info["pages"]:
        shapes = p.get("shapes", [])
        connects = p.get("connects", [])
        connectors = [s for s in shapes if s["is_connector"]]
        blocks = [s for s in shapes if not s["is_connector"]]
        lines.append("## 页 %s%s" % (p.get("id", "?"), ("（%s）" % p["name"]) if p.get("name") else ""))
        lines.append("- 形状总数: %d（图元 %d / 连线 %d）" % (len(shapes), len(blocks), len(connectors)))
        lines.append("- 连接关系数: %d" % len(connects))
        if blocks:
            lines.append("")
            lines.append("| ID | 名称 | 文本 | 中心X | 中心Y | 宽 | 高 |")
            lines.append("|---|---|---|---|---|---|---|")
            for s in blocks[:60]:
                lines.append(
                    "| %s | %s | %s | %s | %s | %s | %s |"
                    % (s["id"], s["name"], s["text"], s["pin_x"], s["pin_y"], s["width"], s["height"])
                )
            if len(blocks) > 60:
                lines.append("\n> 其余 %d 个图元略" % (len(blocks) - 60))
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", help="待解析的 .vsdx 文件")
    ap.add_argument("--json", action="store_true", help="输出 JSON 而非 Markdown")
    args = ap.parse_args()
    info = inspect(args.file)
    if args.json:
        print(json.dumps(info, ensure_ascii=False, indent=2))
    else:
        print(to_markdown(info))


if __name__ == "__main__":
    main()
