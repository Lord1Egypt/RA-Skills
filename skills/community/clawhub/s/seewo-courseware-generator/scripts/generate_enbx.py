#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_enbx.py - 生成可在「希沃白板」客户端打开的多页课件 (.enbx)

ENBX 是希沃白板的私有课件格式，本质是一个 ZIP 压缩包，内部采用类 XAML/XML
的描述文件（注意：它不是标准 OOXML，没有 ppt/ 目录）。本脚本依据对真实
.enbx 样本（courseware.enbx）逆向得到的结构，生成合规的课件。

内部文件结构（必须完全一致）：
    [Content_Types].xml        # 内容类型声明（含 UTF-8 BOM）
    Document.xml               # 课件元信息
    Reference.xml              # 资源关系表（Id/Hash -> Resources\\<hash>.<ext>
    Board.xml                  # 幻灯片顺序（Item = 各 Slide 的 <Id>）
    SaveInfoMetadataFile.xml   # 静态元素类型契约列表（内容无关，原样复制）
    Slides/Slide_0.xml ...     # 每页内容
    Resources/<hash>.<ext>     # 图片/音频等媒体
    thumbnail.png              # 预览缩略图

关键要点：
    * 所有 XML 文件必须以 UTF-8 BOM 开头，且声明 encoding="utf-8"
    * Slide 元素的 <Id> 必须与 Board.xml 中 <Item> 一一对应且顺序一致
    * 元素引用的资源 id://<hash> 必须在 Reference.xml 与 Resources/ 中真实存在
    * 颜色使用 ARGB 十六进制，如 #FFFFFFFF（不透明白）/ #FF000000（不透明黑）
"""

import os
import sys
import json
import uuid
import random
import datetime
import zipfile
import struct
import zlib

# ---------------------------------------------------------------------------
# 基础工具
# ---------------------------------------------------------------------------

def xml_escape(s):
    """转义 XML 纯文本中的特殊字符。"""
    if s is None:
        return ""
    s = str(s)
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;"))


def hex_id(n=32):
    """生成 n 位十六进制资源/幻灯片 id（与样本一致的长度）。"""
    return "".join(random.choice("0123456789abcdef") for _ in range(n))


def guid():
    """生成 GUID 形态的元素 id（如 Picture/Table 所用）。"""
    return str(uuid.uuid4())


def now_str():
    """样本使用 M/D/YYYY H:MM:SS 格式的时间戳。"""
    return datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")


def argb(hex6, alpha="FF"):
    """#RRGGBB -> #AARRGGBB。alpha 默认不透明。"""
    h = hex6.lstrip("#")
    if len(h) == 6:
        return "#" + alpha + h.upper()
    return hex6.upper()


def wrap_text(text, font_size, box_width, pad=16):
    """对文本做按宽度折行（中文按字宽≈font_size 估算）。返回行列表。"""
    if text is None:
        return [""]
    text = str(text)
    # 显式换行优先
    paragraphs = text.split("\n")
    cpl = max(1, int((box_width - 2 * pad) / max(1.0, font_size)))
    lines = []
    for para in paragraphs:
        if para == "":
            lines.append("")
            continue
        # 以 cpl 为步长按字符切分（中文逐字；混合也近似成立）
        i = 0
        while i < len(para):
            lines.append(para[i:i + cpl])
            i += cpl
    return lines


# ---------------------------------------------------------------------------
# 纯 Python PNG 生成（用于背景、色块、缩略图，无需第三方库）
# ---------------------------------------------------------------------------

def _png_chunk(tag, data):
    chunk = tag + data
    return struct.pack(">I", len(data)) + chunk + struct.pack(">I", zlib.crc32(chunk) & 0xFFFFFFFF)


def make_png(width, height, color, grad_color=None):
    """
    生成一张 RGBA PNG（字节）。
    color / grad_color: (r,g,b) 或 (r,g,b,a)
    若提供 grad_color，则生成从上到下的线性渐变。
    """
    if len(color) == 3:
        color = color + (255,)
    if grad_color is None:
        grad_color = color
    if len(grad_color) == 3:
        grad_color = grad_color + (255,)

    raw = bytearray()
    for y in range(height):
        t = y / max(1, height - 1)
        r = int(color[0] * (1 - t) + grad_color[0] * t)
        g = int(color[1] * (1 - t) + grad_color[1] * t)
        b = int(color[2] * (1 - t) + grad_color[2] * t)
        a = int(color[3] * (1 - t) + grad_color[3] * t)
        raw.append(0)  # filter type 0
        for _ in range(width):
            raw += bytes((r, g, b, a))
    comp = zlib.compress(bytes(raw), 9)

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)  # 8-bit RGBA
    png = sig + _png_chunk(b"IHDR", ihdr) + _png_chunk(b"IDAT", comp) + _png_chunk(b"IEND", b"")
    return png


def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 8:  # #AARRGGBB
        return (int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16))
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


# ---------------------------------------------------------------------------
# 图片尺寸探测（PNG / JPEG），用于 Picture 的 MetaData
# ---------------------------------------------------------------------------

def image_dimensions(path):
    """返回 (w, h)，不支持时返回 (0, 0)。"""
    try:
        with open(path, "rb") as f:
            head = f.read(32)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            w, h = struct.unpack(">II", head[16:24])
            return w, h
        if head[:2] in (b"\xff\xd8",):
            with open(path, "rb") as f:
                f.read(2)
                while True:
                    b = f.read(1)
                    if not b or b != b"\xff":
                        break
                    marker = f.read(1)
                    if marker in (b"\xc0", b"\xc1", b"\xc2", b"\xc3",
                                  b"\xc5", b"\xc6", b"\xc7", b"\xc9", b"\xca",
                                  b"\xcb", b"\xcd", b"\xce", b"\xcf"):
                        f.read(3)
                        h, w = struct.unpack(">HH", f.read(4))
                        return w, h
                    else:
                        ln = struct.unpack(">H", f.read(2))[0]
                        f.read(ln - 2)
    except Exception:
        pass
    return (0, 0)


def ext_of(path):
    _, e = os.path.splitext(path)
    return (e.lstrip(".").lower()) or "png"


# ---------------------------------------------------------------------------
# XML 片段构建
# ---------------------------------------------------------------------------

BOM = "\ufeff"


def xml_decl():
    return '<?xml version="1.0" encoding="utf-8"?>'


def rich_text_xml(lines, fmt):
    """
    构建 <RichText>...</RichText>。
    lines: 可见文本行列表（不含换行符）
    fmt: dict(font_size, color(#RRGGBB 或 #AARRGGBB), bold(bool), font_family, align)
    """
    font_size = fmt.get("font_size", 30)
    color = argb(fmt.get("color", "#000000"), "FF")
    bold = "Bold" if fmt.get("bold") else "Normal"
    family = fmt.get("font_family", "微软雅黑")
    align = fmt.get("align", "Left")
    line_spacing = fmt.get("line_spacing", 1)

    runs = []
    for ln in lines:
        runs.append(
            '            <TextRun>\n'
            '              <Text>{text}&#xD;\n</Text>\n'
            '              <FontSize>{fs}</FontSize>\n'
            '              <FontVariants>Normal</FontVariants>\n'
            '              <FontStyle>Normal</FontStyle>\n'
            '              <FontWeight>{w}</FontWeight>\n'
            '              <FontFamily>\n'
            '                <Source>{fam}</Source>\n'
            '              </FontFamily>\n'
            '              <Background>\n'
            '                <ColorBrush>#00FFFFFF</ColorBrush>\n'
            '              </Background>\n'
            '              <Foreground>\n'
            '                <ColorBrush>{c}</ColorBrush>\n'
            '              </Foreground>\n'
            '              <Opacity>1</Opacity>\n'
            '              <DashStyle>\n'
            '                <Offset>0</Offset>\n'
            '                <Dashes></Dashes>\n'
            '              </DashStyle>\n'
            '            </TextRun>'.format(
                text=xml_escape(ln), fs=repr(font_size), w=bold, fam=xml_escape(family), c=color)
        )
    runs_xml = "\n".join("            <TextRuns>\n" + r + "\n            </TextRuns>" for r in runs)

    default_run = (
        '            <TextRun>\n'
        '              <Text></Text>\n'
        '              <FontSize>{fs}</FontSize>\n'
        '              <FontVariants>Normal</FontVariants>\n'
        '              <FontStyle>Normal</FontStyle>\n'
        '              <FontWeight>{w}</FontWeight>\n'
        '              <FontFamily>\n'
        '                <Source>{fam}</Source>\n'
        '              </FontFamily>\n'
        '              <Background>\n'
        '                <ColorBrush>#00FFFFFF</ColorBrush>\n'
        '              </Background>\n'
        '              <Foreground>\n'
        '                <ColorBrush>{c}</ColorBrush>\n'
        '              </Foreground>\n'
        '              <Opacity>1</Opacity>\n'
        '              <DashStyle>\n'
        '                <Offset>0</Offset>\n'
        '                <Dashes></Dashes>\n'
        '              </DashStyle>\n'
        '            </TextRun>'.format(fs=repr(font_size), w=bold, fam=xml_escape(family), c=color)
    )

    textlines = []
    for ln in lines:
        textlines.append(
            '          <TextLine>\n'
            '            <LineSpacing>{ls}</LineSpacing>\n'
            '            <TextAlignment>{al}</TextAlignment>\n'
            '{runs}'
            '            <DefaultRunProperty>\n{dr}\n            </DefaultRunProperty>\n'
            '            <MarginLeft>0</MarginLeft>\n'
            '            <Indent>0</Indent>\n'
            '            <SpaceBefore>0</SpaceBefore>\n'
            '            <SpaceAfter>0</SpaceAfter>\n'
            '            <Lines>\n'
            '              <LineProperty>\n'
            '                <StartOffset>0</StartOffset>\n'
            '                <Length>{lnlen}</Length>\n'
            '              </LineProperty>\n'
            '            </Lines>\n'
            '            <Direction>LeftToRight</Direction>\n'
            '            <IndentLevel>0</IndentLevel>\n'
            '            <TextMarker>None</TextMarker>\n'
            '            <IndentType>FirstLine</IndentType>\n'
            '          </TextLine>'.format(
                ls=repr(line_spacing), al=align, runs=runs_xml, dr=default_run, lnlen=len(ln))
        )
    textlines_xml = "\n".join(textlines)

    plain = "&#xD;\n".join(xml_escape(ln) for ln in lines)

    return (
        '      <RichText>\n'
        '        <SizeToContent>Height</SizeToContent>\n'
        '        <ArrangingType>Horizontal</ArrangingType>\n'
        '        <VerticalTextAlignment>Top</VerticalTextAlignment>\n'
        '        <TextLines>\n'
        '{tl}'
        '        </TextLines>\n'
        '        <Text>{plain}</Text>\n'
        '      </RichText>'.format(tl=textlines_xml, plain=plain)
    )


def text_element_xml(elem, canvas_w):
    """构建 <Text> 元素。elem: {text,x,y,w,h,color,size,bold,align,font_family,line_spacing}"""
    text = elem.get("text", "")
    x = elem.get("x", 100)
    y = elem.get("y", 100)
    w = elem.get("w", canvas_w - 200)
    fs = elem.get("size", 30)
    lines = wrap_text(text, fs, w)
    h = elem.get("h")
    if h is None:
        lh = fs * (1 + max(0, elem.get("line_spacing", 1)) * 0.3) + fs * 0.4
        h = max(fs * 1.2, len(lines) * lh + 10)

    fmt = {
        "font_size": fs,
        "color": elem.get("color", "#000000"),
        "bold": elem.get("bold", False),
        "font_family": elem.get("font_family", "微软雅黑"),
        "align": elem.get("align", "Left"),
        "line_spacing": elem.get("line_spacing", 1),
    }
    rt = rich_text_xml(lines, fmt)
    eid = elem.get("id") or hex_id()
    return (
        '    <Text>\n'
        '{rt}\n'
        '      <BorderThickness>0</BorderThickness>\n'
        '      <BorderType>None</BorderType>\n'
        '      <Id>{eid}</Id>\n'
        '      <X>{x}</X>\n'
        '      <Y>{y}</Y>\n'
        '      <Width>{w}</Width>\n'
        '      <Height>{h}</Height>\n'
        '      <Rotation>0</Rotation>\n'
        '      <IsLocked>False</IsLocked>\n'
        '      <CanClone>False</CanClone>\n'
        '      <Hyperlink></Hyperlink>\n'
        '      <HasMask>False</HasMask>\n'
        '      <RotateOrigin>0.5,0.5</RotateOrigin>\n'
        '      <TextMask></TextMask>\n'
        '    </Text>'.format(rt=rt, eid=eid, x=repr(x), y=repr(y), w=repr(w), h=repr(h))
    )


def title_element_xml(elem, canvas_w):
    """标题：居中、WidthAndHeight、加粗。"""
    text = elem.get("text", "")
    x = elem.get("x", 100)
    y = elem.get("y", 80)
    w = elem.get("w", canvas_w - 200)
    fs = elem.get("size", 56)
    lines = wrap_text(text, fs, w)
    h = elem.get("h", max(fs * 1.4, len(lines) * fs * 1.3))
    fmt = {
        "font_size": fs,
        "color": elem.get("color", "#FFFFFF"),
        "bold": True,
        "font_family": elem.get("font_family", "微软雅黑"),
        "align": elem.get("align", "Center"),
        "line_spacing": 1,
    }
    rt = rich_text_xml(lines, fmt)
    eid = elem.get("id") or hex_id()
    return (
        '    <Text>\n'
        '{rt}\n'
        '      <BorderThickness>0</BorderThickness>\n'
        '      <BorderType>None</BorderType>\n'
        '      <Id>{eid}</Id>\n'
        '      <X>{x}</X>\n'
        '      <Y>{y}</Y>\n'
        '      <Width>{w}</Width>\n'
        '      <Height>{h}</Height>\n'
        '      <Rotation>0</Rotation>\n'
        '      <IsLocked>False</IsLocked>\n'
        '      <CanClone>False</CanClone>\n'
        '      <Hyperlink></Hyperlink>\n'
        '      <HasMask>False</HasMask>\n'
        '      <RotateOrigin>0.5,0.5</RotateOrigin>\n'
        '      <TextMask></TextMask>\n'
        '    </Text>'.format(rt=rt, eid=eid, x=repr(x), y=repr(y), w=repr(w), h=repr(h))
    )


def bullets_element_xml(elem, canvas_w):
    """无序列表：每行加 • 前缀。"""
    items = elem.get("items", [])
    text = "\n".join("• " + str(it) for it in items)
    elem = dict(elem)
    elem["text"] = text
    elem["align"] = elem.get("align", "Left")
    return text_element_xml(elem, canvas_w)


def picture_element_xml(elem, res_id, pic_path, canvas_w):
    """构建 <Picture>。res_id 为资源 hash；pic_path 用于取尺寸/体积。"""
    x = elem.get("x", 100)
    y = elem.get("y", 100)
    w = elem.get("w", 300)
    h = elem.get("h", 200)
    disp_w, disp_h = image_dimensions(pic_path)
    if disp_w == 0:
        disp_w, disp_h = int(w), int(h)
    file_size = os.path.getsize(pic_path)
    ext = ext_of(pic_path)
    eid = elem.get("id") or guid()
    return (
        '    <Picture>\n'
        '      <Source>id://{rid}</Source>\n'
        '      <PictureName>file0.{ext}</PictureName>\n'
        '      <Alpha>1</Alpha>\n'
        '      <DisplayRegion>\n'
        '        <Rectangle>0,0,{dw},{dh}</Rectangle>\n'
        '      </DisplayRegion>\n'
        '      <Style>\n'
        '        <StyleType>None</StyleType>\n'
        '        <PicturePresetStyle>None</PicturePresetStyle>\n'
        '      </Style>\n'
        '      <MetaData>\n'
        '        <PictureSize>{dh},{dw}</PictureSize>\n'
        '        <FileSize>{fs}</FileSize>\n'
        '      </MetaData>\n'
        '      <Id>{eid}</Id>\n'
        '      <X>{x}</X>\n'
        '      <Y>{y}</Y>\n'
        '      <Width>{w}</Width>\n'
        '      <Height>{h}</Height>\n'
        '      <Rotation>0</Rotation>\n'
        '      <IsLocked>False</IsLocked>\n'
        '      <CanClone>False</CanClone>\n'
        '      <Hyperlink></Hyperlink>\n'
        '      <HasMask>False</HasMask>\n'
        '      <RotateOrigin>0.5,0.5</RotateOrigin>\n'
        '    </Picture>'.format(
            rid=res_id, ext=ext, dw=disp_w, dh=disp_h, fs=file_size,
            eid=eid, x=repr(x), y=repr(y), w=repr(w), h=repr(h))
    )


def box_element_xml(elem, res_id):
    """色块：以生成的纯色 PNG 作为 Picture 实现。"""
    x = elem.get("x", 100)
    y = elem.get("y", 100)
    w = elem.get("w", 300)
    h = elem.get("h", 100)
    eid = elem.get("id") or guid()
    return (
        '    <Picture>\n'
        '      <Source>id://{rid}</Source>\n'
        '      <PictureName>box.png</PictureName>\n'
        '      <Alpha>1</Alpha>\n'
        '      <DisplayRegion>\n'
        '        <Rectangle>0,0,{w},{h}</Rectangle>\n'
        '      </DisplayRegion>\n'
        '      <Style>\n'
        '        <StyleType>None</StyleType>\n'
        '        <PicturePresetStyle>None</PicturePresetStyle>\n'
        '      </Style>\n'
        '      <MetaData>\n'
        '        <PictureSize>{h},{w}</PictureSize>\n'
        '        <FileSize>0</FileSize>\n'
        '      </MetaData>\n'
        '      <Id>{eid}</Id>\n'
        '      <X>{x}</X>\n'
        '      <Y>{y}</Y>\n'
        '      <Width>{w}</Width>\n'
        '      <Height>{h}</Height>\n'
        '      <Rotation>0</Rotation>\n'
        '      <IsLocked>False</IsLocked>\n'
        '      <CanClone>False</CanClone>\n'
        '      <Hyperlink></Hyperlink>\n'
        '      <HasMask>False</HasMask>\n'
        '      <RotateOrigin>0.5,0.5</RotateOrigin>\n'
        '    </Picture>'.format(rid=res_id, w=int(w), h=int(h), eid=eid,
                                x=repr(x), y=repr(y), w_=repr(w), h_=repr(h))
    )


def _cell_text_xml(cell_text, font_size=24, bold=False, color="#FF464646"):
    """表格单元格内的 <Text>...<Text>（注意：与顶层 Text 不同，内部用 X/Y=0）。"""
    lines = wrap_text(cell_text, font_size, 400)
    fmt = {"font_size": font_size, "color": color, "bold": bold,
           "font_family": "微软雅黑", "align": "Left", "line_spacing": 1}
    rt = rich_text_xml(lines, fmt)
    eid = hex_id()
    return (
        '              <Text>\n'
        '{rt}\n'
        '                <BorderThickness>0</BorderThickness>\n'
        '                <BorderType>None</BorderType>\n'
        '                <Id>{eid}</Id>\n'
        '                <X>0</X>\n'
        '                <Y>0</Y>\n'
        '                <Width>0</Width>\n'
        '                <Height>0</Height>\n'
        '                <Rotation>0</Rotation>\n'
        '                <IsLocked>False</IsLocked>\n'
        '                <CanClone>False</CanClone>\n'
        '                <HasMask>False</HasMask>\n'
        '              </Text>'.format(rt=rt, eid=eid)
    )


def table_element_xml(elem, canvas_w):
    """构建 <Table>。rows: 二维字符串列表；第一行为表头（若 header=true）。"""
    rows = elem.get("rows", [])
    if not rows:
        return ""
    header = elem.get("header", True)
    x = elem.get("x", 100)
    y = elem.get("y", 100)
    w = elem.get("w", canvas_w - 200)
    h = elem.get("h")
    ncols = max(len(r) for r in rows)
    col_w = int(w / ncols)
    if h is None:
        h = 60 + (len(rows)) * 56
    font_size = elem.get("size", 24)

    # 列宽
    col_widths = "\n".join("          <Item>{cw}</Item>".format(cw=col_w) for _ in range(ncols))

    # 行
    row_xmls = []
    for ri, row in enumerate(rows):
        is_header = header and ri == 0
        cells = []
        for ci in range(ncols):
            val = row[ci] if ci < len(row) else ""
            ct = _cell_text_xml(val, font_size=font_size,
                                bold=is_header,
                                color="#FF464646" if is_header else "#FF000000")
            cells.append(
                '            <Cell>\n'
                '{ct}\n'
                '              <HMerged>False</HMerged>\n'
                '              <VMerged>False</VMerged>\n'
                '              <RowSpan>1</RowSpan>\n'
                '              <ColumnSpan>1</ColumnSpan>\n'
                '              <IsErasable>False</IsErasable>\n'
                '            </Cell>'.format(ct=ct)
            )
        row_xmls.append(
            '          <Row>\n'
            '            <Height>{rh}</Height>\n'
            '            <Cells>\n'
            '{cells}\n'
            '            </Cells>\n'
            '          </Row>'.format(rh=62 if is_header else 56, cells="\n".join(cells))
        )

    eid = elem.get("id") or hex_id()
    return (
        '    <Table>\n'
        '      <Skin>\n'
        '        <TableSkin>Gray</TableSkin>\n'
        '        <HeaderFill>\n'
        '          <ColorBrush>#FFE6E6E6</ColorBrush>\n'
        '        </HeaderFill>\n'
        '        <RowSkins>\n'
        '          <RowSkinDetail>\n'
        '            <Fill>\n'
        '              <ColorBrush>#FFFFFFFF</ColorBrush>\n'
        '            </Fill>\n'
        '          </RowSkinDetail>\n'
        '          <RowSkinDetail>\n'
        '            <Fill>\n'
        '              <ColorBrush>#FFF5F5F5</ColorBrush>\n'
        '            </Fill>\n'
        '          </RowSkinDetail>\n'
        '        </RowSkins>\n'
        '        <StrokeThickness>1</StrokeThickness>\n'
        '        <Stroke>\n'
        '          <ColorBrush>#FFADADAD</ColorBrush>\n'
        '        </Stroke>\n'
        '        <HeaderForeground>\n'
        '          <ColorBrush>#FF464646</ColorBrush>\n'
        '        </HeaderForeground>\n'
        '        <HeaderFontSize>28</HeaderFontSize>\n'
        '      </Skin>\n'
        '      <ColumnWidths>\n'
        '{cw}\n'
        '      </ColumnWidths>\n'
        '      <Rows>\n'
        '{rows}\n'
        '      </Rows>\n'
        '      <CellHPadding>24</CellHPadding>\n'
        '      <CellVPadding>24</CellVPadding>\n'
        '      <Id>{eid}</Id>\n'
        '      <X>{x}</X>\n'
        '      <Y>{y}</Y>\n'
        '      <Width>{w}</Width>\n'
        '      <Height>{h}</Height>\n'
        '      <Rotation>0</Rotation>\n'
        '      <IsLocked>False</IsLocked>\n'
        '      <CanClone>False</CanClone>\n'
        '      <Hyperlink></Hyperlink>\n'
        '      <HasMask>False</HasMask>\n'
        '      <RotateOrigin>0.5,0.5</RotateOrigin>\n'
        '    </Table>'.format(cw=col_widths, rows="\n".join(row_xmls), eid=eid,
                              x=repr(x), y=repr(y), w=repr(w), h=repr(h))
    )


# ---------------------------------------------------------------------------
# 文件级 XML
# ---------------------------------------------------------------------------

def slide_xml(slide_id, canvas_w, canvas_h, bg_res_id, elements_xml, duration=5000000):
    return (
        '<Slide>\n'
        '  <Id>{sid}</Id>\n'
        '  <Width>{cw}</Width>\n'
        '  <Height>{ch}</Height>\n'
        '  <Background>\n'
        '    <ImageBrush>\n'
        '      <Source>id://{bg}</Source>\n'
        '      <Stretch>Fill</Stretch>\n'
        '      <TileMode>None</TileMode>\n'
        '      <Opacity>1</Opacity>\n'
        '      <ViewboxUnits>RelativeToBoundingBox</ViewboxUnits>\n'
        '      <ViewportUnits>RelativeToBoundingBox</ViewportUnits>\n'
        '      <Viewbox>0,0,1,1</Viewbox>\n'
        '      <Viewport>0,0,1,1</Viewport>\n'
        '      <RelativeMatrixTransform>1,0,0,1,0,0</RelativeMatrixTransform>\n'
        '    </ImageBrush>\n'
        '  </Background>\n'
        '  <Elements>\n'
        '{els}\n'
        '  </Elements>\n'
        '  <Duration>{dur}</Duration>\n'
        '  <ThemeForSlide>\n'
        '    <ThemeId>-12</ThemeId>\n'
        '  </ThemeForSlide>\n'
        '</Slide>'.format(sid=slide_id, cw=canvas_w, ch=canvas_h, bg=bg_res_id,
                          els=elements_xml, dur=duration)
    )


def board_xml(slide_ids, board_bg_res_id):
    items = "\n".join("    <Item>{i}</Item>".format(i=i) for i in slide_ids)
    return (
        '<Board>\n'
        '  <Slides>\n'
        '{items}\n'
        '  </Slides>\n'
        '  <ThemeForBoard>\n'
        '    <ThemeId>-12</ThemeId>\n'
        '    <ThemeBrush>\n'
        '      <ImageBrush>\n'
        '        <Source>id://{bg}</Source>\n'
        '        <Stretch>Fill</Stretch>\n'
        '        <TileMode>None</TileMode>\n'
        '        <Opacity>1</Opacity>\n'
        '        <ViewboxUnits>RelativeToBoundingBox</ViewboxUnits>\n'
        '        <ViewportUnits>RelativeToBoundingBox</ViewportUnits>\n'
        '        <Viewbox>0,0,1,1</Viewbox>\n'
        '        <Viewport>0,0,1,1</Viewport>\n'
        '        <RelativeMatrixTransform>1,0,0,1,0,0</RelativeMatrixTransform>\n'
        '      </ImageBrush>\n'
        '    </ThemeBrush>\n'
        '  </ThemeForBoard>\n'
        '</Board>'.format(items=items, bg=board_bg_res_id)
    )


def document_xml(name):
    return (
        '<Document>\n'
        '  <Name>{name}</Name>\n'
        '  <Creator>workbuddy-generator</Creator>\n'
        '  <LastModifiedBy>workbuddy-generator</LastModifiedBy>\n'
        '  <CreatedDateTime>{ts}</CreatedDateTime>\n'
        '  <ModifiedDateTime>{ts}</ModifiedDateTime>\n'
        '  <CreatedDocumentVersion>1.0</CreatedDocumentVersion>\n'
        '  <DocumentVersion>1.0</DocumentVersion>\n'
        '  <CreatedAppVersion>5.1.17.73189</CreatedAppVersion>\n'
        '  <AppVersion>5.1.17.73189</AppVersion>\n'
        '  <DocumentExtraInfo>\n'
        '    <CoursewareSourceTrace>\n'
        '      <UpstreamAuthor>workbuddy-generator</UpstreamAuthor>\n'
        '      <UpstreamId>{uid}</UpstreamId>\n'
        '      <UpstreamVersion>1</UpstreamVersion>\n'
        '    </CoursewareSourceTrace>\n'
        '  </DocumentExtraInfo>\n'
        '</Document>'.format(name=xml_escape(name), ts=now_str(),
                             uid=str(uuid.uuid4()))
    )


def reference_xml(relationships):
    """
    relationships: list of (res_id, target_path_no_slash)
    例如 ("abc123", "Resources/abc123.png")
    """
    rels = []
    for rid, target in relationships:
        t = target.replace("/", "\\")
        rels.append(
            '    <Relationship>\n'
            '      <Id>{rid}</Id>\n'
            '      <Target>{tgt}</Target>\n'
            '      <Hash>{rid}</Hash>\n'
            '    </Relationship>'.format(rid=rid, tgt=xml_escape(t))
        )
    return (
        '<Reference>\n'
        '  <Relationships>\n'
        '{rels}\n'
        '  </Relationships>\n'
        '</Reference>'.format(rels="\n".join(rels))
    )


def content_types_xml(extensionless):
    defaults = [
        '<Default Extension="xml" ContentType="" />',
        '<Default Extension="png" ContentType="" />',
    ]
    overrides = []
    for tgt in extensionless:
        # 无扩展名的资源需要 Override
        overrides.append(
            '<Override PartName="/{tgt}" ContentType="" />'.format(tgt=tgt.replace("\\", "/"))
        )
    parts = defaults + overrides
    return (
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '{parts}'
        '</Types>'.format(parts="".join(parts))
    )


SAVEINFO = (
    '<SaveInfoMetadataFile>\n'
    '  <MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>Board</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>ThemeForBoard</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>Slide</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>Text</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>RichText</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>TextLine</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>TextRun</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>LineProperty</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>TextMask</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>Picture</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>PictureStyle</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>PictureMetaData</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>ThemeForSlide</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>Table</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>TableSkin</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>RowSkinDetail</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>Row</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>Cell</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>Audio</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>ElementBehavior</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>Document</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>DocumentExtraInfo</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>CoursewareSourceTraceInfo</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>Reference</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '    <MetadataContract><SaveInfoName>Relationship</SaveInfoName><SaveInfoFriendlyName></SaveInfoFriendlyName><SaveInfoType>Unset</SaveInfoType><FallbackSaveInfo></FallbackSaveInfo></MetadataContract>\n'
    '  </MetadataContract>\n'
    '</SaveInfoMetadataFile>'
)


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

# 内置几种常用布局（自动生成 elements）
def apply_layout(page, canvas_w, canvas_h):
    """若 page 只给了 title/content/bullets/subtitle，则自动生成 elements。"""
    if page.get("elements"):
        return page["elements"]
    els = []
    layout = page.get("layout", "content")
    bg = page.get("background", "#FFFFFF")
    dark = is_dark(bg)

    if layout == "title_slide":
        els.append({"type": "title", "text": page.get("title", ""),
                    "x": 140, "y": canvas_h / 2 - 120, "w": canvas_w - 280,
                    "h": 140, "size": 64, "color": "#FFFFFF" if dark else "#222222"})
        if page.get("subtitle"):
            els.append({"type": "text", "text": page["subtitle"],
                        "x": 140, "y": canvas_h / 2 + 40, "w": canvas_w - 280,
                        "h": 60, "size": 32, "align": "Center",
                        "color": "#FFFFFF" if dark else "#555555"})
    else:
        # content / two_col / section 都有标题条
        els.append({"type": "title", "text": page.get("title", ""),
                    "x": 80, "y": 60, "w": canvas_w - 160, "h": 90,
                    "size": 48, "color": "#FFFFFF" if dark else "#1A237E",
                    "align": "Left"})
        if page.get("subtitle"):
            els.append({"type": "text", "text": page["subtitle"],
                        "x": 80, "y": 170, "w": canvas_w - 160, "h": 50,
                        "size": 28, "color": "#FFFFFF" if dark else "#555555"})
        body_y = 240
        if page.get("bullets"):
            els.append({"type": "bullets", "items": page["bullets"],
                        "x": 100, "y": body_y, "w": canvas_w - 200,
                        "size": 30, "color": "#FFFFFF" if dark else "#222222"})
        elif page.get("content"):
            els.append({"type": "text", "text": page["content"],
                        "x": 100, "y": body_y, "w": canvas_w - 200,
                        "size": 30, "color": "#FFFFFF" if dark else "#222222",
                        "line_spacing": 4})
        if page.get("table"):
            t = dict(page["table"])
            t["type"] = "table"
            t.setdefault("x", 100)
            t.setdefault("y", body_y)
            t.setdefault("w", canvas_w - 200)
            els.append(t)
    return els


def is_dark(hex6):
    try:
        r, g, b = hex_to_rgb(hex6)
        return (0.299 * r + 0.587 * g + 0.114 * b) < 128
    except Exception:
        return False


def build_element(elem, canvas_w, canvas_h, resources, tmp_files):
    """根据元素定义生成 XML 片段，并登记所需资源。
    返回 (xml_fragment, extra_relationships)
    resources: dict res_id -> (target_path, bytes)  （供打包与关系表使用）
    """
    etype = elem.get("type", "text")
    rels = []

    if etype in ("title",):
        return title_element_xml(elem, canvas_w), rels
    if etype in ("text",):
        return text_element_xml(elem, canvas_w), rels
    if etype in ("bullets",):
        return bullets_element_xml(elem, canvas_w), rels
    if etype in ("table",):
        return table_element_xml(elem, canvas_w), rels
    if etype in ("box",):
        rid = hex_id()
        color = hex_to_rgb(elem.get("color", "#FFD54F"))
        png = make_png(int(elem.get("w", 300)), int(elem.get("h", 100)), color)
        resources[rid] = ("Resources/{rid}.png".format(rid=rid), png)
        rels.append((rid, "Resources/{rid}.png".format(rid=rid)))
        return box_element_xml(elem, rid), rels
    if etype in ("picture",):
        src = elem.get("src")
        if not src or not os.path.exists(src):
            # 资源缺失：跳过，避免生成损坏文件
            sys.stderr.write("[warn] picture src not found: {0}\n".format(src))
            return "", rels
        rid = hex_id()
        with open(src, "rb") as f:
            data = f.read()
        ext = ext_of(src)
        target = "Resources/{rid}.{ext}".format(rid=rid, ext=ext)
        resources[rid] = (target, data)
        rels.append((rid, target))
        return picture_element_xml(elem, rid, src, canvas_w), rels

    sys.stderr.write("[warn] unknown element type: {0}\n".format(etype))
    return "", rels


def generate(spec, out_path):
    canvas_w = int(spec.get("canvas", {}).get("width", 1280))
    canvas_h = int(spec.get("canvas", {}).get("height", 720))
    name = spec.get("courseware_name", "未命名课件")

    resources = {}  # res_id -> (target_path, bytes)
    relationships = []  # (res_id, target_path)

    slide_ids = []
    slide_files = {}  # index -> (slide_id, xml)
    page_bg_rids = []  # 每页背景资源 id（顺序与 page 对应）

    pages = spec.get("pages", [])
    for idx, page in enumerate(pages):
        # 背景
        bg = page.get("background", "#FFFFFF")
        bg2 = page.get("background2")
        bg_rgb = hex_to_rgb(bg)
        bg2_rgb = hex_to_rgb(bg2) if bg2 else None
        bg_png = make_png(canvas_w, canvas_h, bg_rgb, bg2_rgb)
        bg_rid = hex_id()
        bg_target = "Resources/{rid}.png".format(rid=bg_rid)
        resources[bg_rid] = (bg_target, bg_png)
        relationships.append((bg_rid, bg_target))
        page_bg_rids.append(bg_rid)

        # 元素
        elements = apply_layout(page, canvas_w, canvas_h)
        frags = []
        for el in elements:
            frag, rels = build_element(el, canvas_w, canvas_h, resources, None)
            if frag:
                frags.append(frag)
            relationships.extend(rels)

        sid = hex_id()
        slide_ids.append(sid)
        sxml = slide_xml(sid, canvas_w, canvas_h, bg_rid, "\n".join(frags))
        slide_files[idx] = (sid, sxml)

    # 缩略图（用第一页背景色）
    first_bg = hex_to_rgb(pages[0].get("background", "#FFFFFF")) if pages else (255, 255, 255)
    thumb = make_png(160, 90, first_bg)
    resources["__thumb__"] = ("thumbnail.png", thumb)

    # 组装文件级 XML
    # Board 主题背景复用首张背景资源
    board_bg_rid = page_bg_rids[0] if page_bg_rids else ""

    board = board_xml(slide_ids, board_bg_rid)
    document = document_xml(name)
    reference = reference_xml(relationships)
    content = content_types_xml([])  # 所有资源均带扩展名，无需 Override

    # 写入 ZIP
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        # 必须在最外层（与样本一致，[Content_Types].xml 在根）
        z.writestr("[Content_Types].xml", BOM + xml_decl() + content)
        z.writestr("Document.xml", BOM + xml_decl() + document)
        z.writestr("Reference.xml", BOM + xml_decl() + reference)
        z.writestr("Board.xml", BOM + xml_decl() + board)
        z.writestr("SaveInfoMetadataFile.xml", BOM + xml_decl() + SAVEINFO)
        for idx in sorted(slide_files.keys()):
            sid, sxml = slide_files[idx]
            z.writestr("Slides/Slide_{0}.xml".format(idx), BOM + xml_decl() + sxml)
        for rid, (tgt, data) in resources.items():
            z.writestr(tgt, data)

    return {
        "out": out_path,
        "pages": len(pages),
        "resources": len(resources),
        "size_bytes": os.path.getsize(out_path),
    }


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: generate_enbx.py <spec.json> [output.enbx]\n")
        sys.exit(1)
    spec_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else "courseware.enbx"
    with open(spec_path, "r", encoding="utf-8") as f:
        spec = json.load(f)
    result = generate(spec, out_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
