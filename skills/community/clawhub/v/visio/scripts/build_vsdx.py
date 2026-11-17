#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_vsdx.py — 由 JSON 规格生成基础 .vsx 图（矩形图元 + 直线连线）。

用法:
    python build_vsdx.py <spec.json> <output.vsdx>

spec.json 格式（坐标单位：英寸，页面原点为左下角）:
{
  "page": { "width": 11.69, "height": 8.27, "name": "Page-1" },
  "font": "Microsoft YaHei",
  "nodes": [
    { "id": "A", "x": 1.0, "y": 6.0, "w": 2.0, "h": 0.8,
      "text": "智能筹划", "fill": "#185FA5", "text_color": "#FFFFFF",
      "font_size": 12, "corner": "round" }
  ],
  "edges": [
    { "from": "A", "to": "B", "color": "#5F5E5A", "weight": 1.0,
      "arrow": true, "dash": true, "label": "命令流" }
  ]
}

说明:
    - 不依赖 Visio 安装；产物可用 Visio 2016+ 打开后继续编辑。
    - 节点 id 可重复引用；连线自动取两节点边缘交点连线（简化为中心到中心）。
    - 仅支持基础矩形/圆角矩形与直线连线；复杂图形请生成 SVG 后导入 Visio。
"""
import json
import sys
import zipfile

XML_HEAD = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'

CONTENT_TYPES = XML_HEAD + (
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/visio/document.xml" ContentType="application/vnd.ms-visio.drawing.main+xml"/>'
    '<Override PartName="/visio/pages/pages.xml" ContentType="application/vnd.ms-visio.pages+xml"/>'
    '<Override PartName="/visio/pages/page1.xml" ContentType="application/vnd.ms-visio.page+xml"/>'
    '<Override PartName="/visio/windows.xml" ContentType="application/vnd.ms-visio.windows+xml"/>'
    '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
    '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
    "</Types>"
)

ROOT_RELS = XML_HEAD + (
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/document" Target="visio/document.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
    '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
    "</Relationships>"
)

CORE_PROPS = XML_HEAD + (
    '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
    'xmlns:dc="http://purl.org/dc/elements/1.1/" '
    'xmlns:dcterms="http://purl.org/dc/terms/" '
    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
    '<dc:creator>visio skill</dc:creator>'
    '<cp:lastModifiedBy>visio skill</cp:lastModifiedBy>'
    "</cp:coreProperties>"
)

APP_PROPS = XML_HEAD + (
    '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
    "<Application>visio skill</Application>"
    "</Properties>"
)


def document_xml(font_name):
    return XML_HEAD + (
        '<VisioDocument xmlns="http://schemas.microsoft.com/office/visio/2012/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xml:space="preserve">'
        '<DocumentSettings TopPage="0" DefaultTextStyle="0" DefaultLineStyle="0" DefaultFillStyle="0" DefaultGuideStyle="0"/>'
        '<FaceNames><FaceName ID="1" Name="%s" UnicodeRanges="-1 -1 -1 -1"/></FaceNames>'
        "</VisioDocument>"
    ) % font_name


DOC_RELS = XML_HEAD + (
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/pages" Target="pages/pages.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.microsoft.com/visio/2010/relationships/windows" Target="windows.xml"/>'
    "</Relationships>"
)

WINDOWS = XML_HEAD + (
    '<Windows ClientWidth="1" ClientHeight="1" xmlns="http://schemas.microsoft.com/office/visio/2012/main">'
    '<Window ID="0" WindowType="Drawing" StencilGroup="-1" StencilParentID="-1"/>'
    "</Windows>"
)

PAGES_RELS = XML_HEAD + (
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/page" Target="page1.xml"/>'
    "</Relationships>"
)


def pages_xml(page_w, page_h, page_name):
    return XML_HEAD + (
        '<Pages xmlns="http://schemas.microsoft.com/office/visio/2012/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xml:space="preserve">'
        '<Page ID="0" NameU="{name}" Name="{name}" Background="0" BackPage="-1" ViewScale="-1" ViewCenterX="{cx}" ViewCenterY="{cy}">'
        '<PageSheet LineStyle="0" FillStyle="0" TextStyle="0">'
        '<Cell N="PageWidth" V="{w}"/><Cell N="PageHeight" V="{h}"/>'
        '<Cell N="ShdwOffsetX" V="0.125"/><Cell N="ShdwOffsetY" V="-0.125"/>'
        "</PageSheet>"
        '<Rel r:id="rId1"/>'
        "</Page>"
        "</Pages>"
    ).format(name=page_name or "Page-1", w=page_w, h=page_h, cx=page_w / 2.0, cy=page_h / 2.0)


def rgb(hex_color):
    hex_color = (hex_color or "#5F5E5A").lstrip("#")
    return "RGB(%d,%d,%d)" % tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def esc(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def node_shape(idx, node, font_id=1):
    sid = idx + 1
    pin_x = node["x"] + node["w"] / 2.0
    pin_y = node["y"] + node["h"] / 2.0
    fill = rgb(node.get("fill", "#185FA5"))
    line = rgb(node.get("line_color", "#5F5E5A"))
    text_color = rgb(node.get("text_color", "#FFFFFF"))
    font_size = float(node.get("font_size", 12)) / 72.0
    text = esc(node.get("text", node.get("id", "")))
    shape_name = "RoundRect" if node.get("corner") == "round" else "Rect"
    return (
        '<Shape ID="{sid}" Type="Shape" NameU="{name}" Name="{name}" Master="-1">'
        '<Cell N="PinX" V="{px}"/><Cell N="PinY" V="{py}"/>'
        '<Cell N="Width" V="{w}"/><Cell N="Height" V="{h}"/>'
        '<Cell N="LocPinX" V="{lpx}" VUnit="IN_F"/><Cell N="LocPinY" V="{lpy}" VUnit="IN_F"/>'
        '<Cell N="Angle" V="0"/>'
        '<Cell N="FillBkgnd" V="{fill}"/><Cell N="FillForegnd" V="{fill}"/>'
        '<Cell N="FillPattern" V="1"/>'
        '<Cell N="LineColor" V="{line}"/><Cell N="LineWeight" V="0.01"/>'
        '<Cell N="Char.Color" V="{tcolor}"/>'
        '<Section N="Character"><Row IX="0"><Cell N="Font" V="{fid}"/><Cell N="Size" V="{fs}"/>'
        '<Cell N="Color" V="{tcolor}"/><Cell N="Case" V="0"/></Row></Section>'
        '<Section N="Paragraph"><Row IX="0"><Cell N="HorzAlign" V="1"/></Row></Section>'
        '<Section N="Geometry" IX="0">'
        + round_rect_geom(node["w"], node["h"], node.get("corner") == "round")
        + "</Section>"
        '<Text>{text}</Text>'
        "</Shape>"
    ).format(
        sid=sid, name=shape_name, px=pin_x, py=pin_y, w=node["w"], h=node["h"],
        lpx=node["w"] / 2.0, lpy=node["h"] / 2.0, fill=fill, line=line,
        tcolor=text_color, fid=font_id, fs=round(font_size, 5), text=text,
    )


def round_rect_geom(w, h, is_round):
    if not is_round:
        return (
            '<Row T="RelMoveTo" IX="1"><Cell N="X" V="0"/><Cell N="Y" V="0"/></Row>'
            '<Row T="RelLineTo" IX="2"><Cell N="X" V="1"/><Cell N="Y" V="0"/></Row>'
            '<Row T="RelLineTo" IX="3"><Cell N="X" V="1"/><Cell N="Y" V="1"/></Row>'
            '<Row T="RelLineTo" IX="4"><Cell N="X" V="0"/><Cell N="Y" V="1"/></Row>'
            '<Row T="RelLineTo" IX="5"><Cell N="X" V="0"/><Cell N="Y" V="0"/></Row>'
        )
    r = min(w, h) * 0.12
    rr = min(r / w, 0.5)
    rh = min(r / h, 0.5)
    return (
        '<Row T="RelMoveTo" IX="1"><Cell N="X" V="{rr}"/><Cell N="Y" V="0"/></Row>'
        '<Row T="RelLineTo" IX="2"><Cell N="X" V="{r2}"/><Cell N="Y" V="0"/></Row>'
        '<Row T="RelEllipticalArcTo" IX="3"><Cell N="X" V="1"/><Cell N="Y" V="0"/>'
        '<Cell N="A" V="{aw}"/><Cell N="B" V="{bh}"/><Cell N="C" V="0"/><Cell N="D" V="1"/></Row>'
        '<Row T="RelLineTo" IX="4"><Cell N="X" V="1"/><Cell N="Y" V="1"/></Row>'
        '<Row T="RelEllipticalArcTo" IX="5"><Cell N="X" V="0"/><Cell N="Y" V="1"/>'
        '<Cell N="A" V="{aw}"/><Cell N="B" V="{bh}"/><Cell N="C" V="1"/><Cell N="D" V="2"/></Row>'
        '<Row T="RelLineTo" IX="6"><Cell N="X" V="0"/><Cell N="Y" V="0"/></Row>'
        '<Row T="RelEllipticalArcTo" IX="7"><Cell N="X" V="{rr}"/><Cell N="Y" V="0"/>'
        '<Cell N="A" V="{aw}"/><Cell N="B" V="{bh}"/><Cell N="C" V="2"/><Cell N="D" V="3"/></Row>'
    ).format(rr=rr, r2=1 - rr, aw=w - 2 * r, bh=h - 2 * r)


def edge_shape_xml(sid, x1, y1, x2, y2, edge):
    w = abs(x2 - x1) or 0.001
    h = abs(y2 - y1) or 0.001
    parts = [
        '<Shape ID="%d" Type="Shape" NameU="Connector" Name="Connector" Master="-1"' % sid,
        ' BeginX="%f" BeginY="%f" EndX="%f" EndY="%f">' % (x1, y1, x2, y2),
        '<Cell N="PinX" V="%f"/><Cell N="PinY" V="%f"/>' % ((x1 + x2) / 2.0, (y1 + y2) / 2.0),
        '<Cell N="Width" V="%f"/><Cell N="Height" V="%f"/>' % (w, h),
        '<Cell N="LocPinX" V="%f" VUnit="IN_F"/><Cell N="LocPinY" V="%f" VUnit="IN_F"/>' % (w / 2.0, h / 2.0),
        '<Cell N="Angle" V="0"/>',
        '<Cell N="LineColor" V="%s"/>' % rgb(edge.get("color", "#5F5E5A")),
        '<Cell N="LineWeight" V="%f"/>' % round(edge.get("weight", 1.0) * 0.01, 4),
    ]
    if edge.get("arrow"):
        parts.append('<Cell N="EndArrow" V="4"/>')
    if edge.get("dash"):
        parts.append('<Cell N="LinePattern" V="2"/>')
    parts.append(
        '<Section N="Geometry" IX="0">'
        '<Row T="MoveTo" IX="1"><Cell N="X" V="0"/><Cell N="Y" V="0"/></Row>'
        '<Row T="LineTo" IX="2"><Cell N="X" V="%f"/><Cell N="Y" V="%f"/></Row>'
        "</Section>" % (w, h)
    )
    if edge.get("label"):
        parts.append(
            '<Section N="Character"><Row IX="0"><Cell N="Font" V="1"/>'
            '<Cell N="Size" V="%f"/><Cell N="Color" V="RGB(95,94,90)"/></Row></Section>'
            "<Text>%s</Text>" % (round(10 / 72.0, 5), esc(edge["label"]))
        )
    parts.append("</Shape>")
    return "".join(parts)


def page_xml(nodes, edges, id_map):
    shapes_xml = []
    for i, node in enumerate(nodes):
        shapes_xml.append(node_shape(i, node))
    next_id = len(nodes) + 1
    for edge in edges:
        a = id_map[edge["from"]]
        b = id_map[edge["to"]]
        ax = a["x"] + a["w"] / 2.0
        ay = a["y"] + a["h"] / 2.0
        bx = b["x"] + b["w"] / 2.0
        by = b["y"] + b["h"] / 2.0
        shapes_xml.append(edge_shape_xml(next_id, ax, ay, bx, by, edge))
        next_id += 1
    return XML_HEAD + (
        '<PageContents xmlns="http://schemas.microsoft.com/office/visio/2012/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xml:space="preserve">'
        "<Shapes>%s</Shapes><Connects/>"
        "</PageContents>"
    ) % "".join(shapes_xml)


def build(spec, out_path):
    page = spec.get("page", {})
    page_w = float(page.get("width", 11.69))
    page_h = float(page.get("height", 8.27))
    font = spec.get("font", "Microsoft YaHei")
    nodes = spec.get("nodes", [])
    edges = spec.get("edges", [])
    id_map = {}
    for i, node in enumerate(nodes):
        nid = node.get("id", str(i + 1))
        if nid in id_map:
            raise SystemExit("重复的节点 id: %s" % nid)
        id_map[nid] = node
    for edge in edges:
        for key in ("from", "to"):
            if edge.get(key) not in id_map:
                raise SystemExit("连线引用了不存在的节点: %s" % edge.get(key))
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", CONTENT_TYPES)
        zf.writestr("_rels/.rels", ROOT_RELS)
        zf.writestr("docProps/core.xml", CORE_PROPS)
        zf.writestr("docProps/app.xml", APP_PROPS)
        zf.writestr("visio/document.xml", document_xml(font))
        zf.writestr("visio/_rels/document.xml.rels", DOC_RELS)
        zf.writestr("visio/windows.xml", WINDOWS)
        zf.writestr("visio/pages/pages.xml", pages_xml(page_w, page_h, page.get("name", "Page-1")))
        zf.writestr("visio/pages/_rels/pages.xml.rels", PAGES_RELS)
        zf.writestr("visio/pages/page1.xml", page_xml(nodes, edges, id_map))


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        spec = json.load(f)
    build(spec, sys.argv[2])
    print("已生成: %s" % sys.argv[2])


if __name__ == "__main__":
    main()
