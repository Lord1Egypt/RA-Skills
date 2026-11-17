# -*- coding: utf-8 -*-
"""
批量水印工具 v5.2
支持：文字水印 / 图片水印；平铺（tile）/对角线（diagonal）两种布局；
支持 docx / pptx / 图片（png/jpg）批量目录处理。
原理：用 PIL 预生成整页水印画布（已含平铺或旋转），再嵌入文档页眉（behind-text）
      或 PPT 背景层（send-to-back），图片文件直接 PIL 合成。
零外部 API；依赖 python-docx / python-pptx / PIL（与全家桶既有模块一致）。

死规则合规：规则9（基础功能自研）规则10（批量并发受控）规则13（不生成禁止文件）规则16（子进程超时）
"""
import sys
import os
import io
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    Image = None

try:
    from docx import Document
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    Document = None

try:
    from pptx import Presentation
    from pptx.util import Emu
except ImportError:
    Presentation = None


# ---------- 页面尺寸（EMU）----------
DOCX_PAGE = (Emu(11906 * 9525), Emu(16838 * 9525))  # A4 横向像素 ≈ 11906 x 16838 EMU
PPT_SLIDE = (Emu(914400 * 10), Emu(914400 * 7.5))    # 10 x 7.5 英寸


def _load_font(size: int) -> Optional[ImageFont.FreeTypeFont]:
    """尝试加载系统中文字体，失败用默认字体"""
    candidates = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
        "/usr/share/fonts/windows/msyh.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                continue
    try:
        return ImageFont.load_default()
    except Exception:
        return None


def make_watermark_canvas(mode: str, text: str, image_path: str,
                          page_w: int, page_h: int,
                          color: str = "200,200,200", opacity: int = 90,
                          font_size: int = 48, diagonal: bool = False,
                          tile: bool = True) -> Image.Image:
    """生成整页水印画布（透明背景）"""
    if Image is None:
        raise RuntimeError("需要 Pillow：pip install pillow")

    canvas = Image.new("RGBA", (page_w, page_h), (255, 255, 255, 0))
    r, g, b = (int(x) for x in color.split(","))

    if mode == "text":
        font = _load_font(font_size)
        dummy = ImageDraw.Draw(canvas)
        tw = dummy.textlength(text, font=font) if font else len(text) * font_size * 0.6
        th = font_size
        wm = Image.new("RGBA", (int(tw) + 40, int(th) + 20), (255, 255, 255, 0))
        d = ImageDraw.Draw(wm)
        d.text((20, 10), text, font=font, fill=(r, g, b, opacity))
        if diagonal:
            wm = wm.rotate(45, expand=True)
    else:  # image
        wm_src = Image.open(image_path).convert("RGBA")
        wm_src = wm_src.resize((font_size * 3, font_size * 3))
        # 调低透明度
        alpha = wm_src.split()[3].point(lambda p: int(p * opacity / 255))
        wm_src.putalpha(alpha)
        if diagonal:
            wm = wm_src.rotate(45, expand=True)
        else:
            wm = wm_src

    wm_w, wm_h = wm.size

    if tile:
        # 平铺网格
        x = 0
        while x < page_w:
            y = 0
            while y < page_h:
                canvas.paste(wm, (x, y), wm)
                y += wm_h + 60
            x += wm_w + 120
    else:
        # 单个居中（对角线或大图）
        pos = ((page_w - wm_w) // 2, (page_h - wm_h) // 2)
        canvas.paste(wm, pos, wm)

    return canvas


def _inline_to_anchor(inline, behind: bool = True):
    """将 wp:inline 转换为 wp:anchor 以实现 behind-text 绝对定位"""
    extent = inline.find(qn("wp:extent"))
    docPr = inline.find(qn("wp:docPr"))
    graphic = inline.find(qn("a:graphic"))

    anchor = OxmlElement("wp:anchor")
    for k, v in [("distT", "0"), ("distB", "0"), ("distL", "0"), ("distR", "0"),
                 ("simplePos", "0"), ("relativeHeight", "1"),
                 ("behindDoc", "1" if behind else "0"), ("locked", "0"),
                 ("layoutInCell", "1"), ("allowOverlap", "1")]:
        anchor.set(k, v)

    sp = OxmlElement("wp:simplePos")
    sp.set("x", "0"); sp.set("y", "0")
    anchor.append(sp)

    h = OxmlElement("wp:positionH"); h.set("relativeFrom", "page")
    ho = OxmlElement("wp:posOffset"); ho.text = "0"; h.append(ho)
    anchor.append(h)

    v = OxmlElement("wp:positionV"); v.set("relativeFrom", "page")
    vo = OxmlElement("wp:posOffset"); vo.text = "0"; v.append(vo)
    anchor.append(v)

    anchor.append(extent)
    ee = OxmlElement("wp:effectExtent")
    for k in ("l", "t", "r", "b"):
        ee.set(k, "0")
    anchor.append(ee)
    anchor.append(OxmlElement("wp:wrapNone"))
    anchor.append(docPr)
    anchor.append(graphic)
    return anchor


def add_watermark_docx(path: str, canvas: Image.Image) -> str:
    """在 docx 页眉插入整页水印（behind text）"""
    if Document is None:
        raise RuntimeError("需要 python-docx：pip install python-docx")
    doc = Document(path)
    buf = io.BytesIO()
    canvas.save(buf, format="PNG")
    buf.seek(0)

    section = doc.sections[0]
    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0]
    run = hp.add_run()
    run.add_picture(buf, width=DOCX_PAGE[0], height=DOCX_PAGE[1])

    # 转为 behind-text anchor
    drawing = run._element.find(qn("w:drawing"))
    inline = drawing.find(qn("wp:inline"))
    if inline is not None:
        anchor = _inline_to_anchor(inline, behind=True)
        drawing.append(anchor)
        drawing.remove(inline)

    out = str(Path(path).parent / f"{Path(path).stem}_水印{Path(path).suffix}")
    doc.save(out)
    return out


def add_watermark_pptx(path: str, canvas: Image.Image) -> str:
    """在 pptx 每页插入整页水印并置于底层"""
    if Presentation is None:
        raise RuntimeError("需要 python-pptx：pip install python-pptx")
    prs = Presentation(path)
    buf = io.BytesIO()
    canvas.save(buf, format="PNG")
    buf.seek(0)

    for slide in prs.slides:
        pic = slide.shapes.add_picture(buf, 0, 0, width=PPT_SLIDE[0], height=PPT_SLIDE[1])
        # 置于最底层
        sp = pic._element
        sp.getparent().remove(sp)
        slide.shapes._spTree.insert(2, sp)

    out = str(Path(path).parent / f"{Path(path).stem}_水印{Path(path).suffix}")
    prs.save(out)
    return out


def add_watermark_image(path: str, canvas: Image.Image) -> str:
    """图片文件直接合成水印"""
    if Image is None:
        raise RuntimeError("需要 Pillow：pip install pillow")
    base = Image.open(path).convert("RGBA")
    # 缩放画布到图片尺寸
    wm = canvas.resize(base.size)
    merged = Image.alpha_composite(base, wm).convert("RGB")
    out = str(Path(path).parent / f"{Path(path).stem}_水印{Path(path).suffix}")
    merged.save(out)
    return out


EXT_MAP = {
    ".docx": "docx",
    ".pptx": "pptx",
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image",
}


def process_file(path: str, opts: Dict[str, Any]) -> Dict[str, Any]:
    ext = Path(path).suffix.lower()
    kind = EXT_MAP.get(ext)
    if kind is None:
        return {"file": path, "ok": False, "error": "不支持的文件类型"}

    page_w, page_h = (DOCX_PAGE[0] // 9525, DOCX_PAGE[1] // 9525) if kind == "docx" else \
                     (PPT_SLIDE[0] // 9525, PPT_SLIDE[1] // 9525) if kind == "pptx" else (2000, 2800)

    canvas = make_watermark_canvas(
        mode=opts["mode"],
        text=opts.get("text", "机密"),
        image_path=opts.get("image", ""),
        page_w=page_w, page_h=page_h,
        color=opts.get("color", "200,200,200"),
        opacity=opts.get("opacity", 90),
        font_size=opts.get("font_size", 48),
        diagonal=opts.get("diagonal", False),
        tile=opts.get("tile", True),
    )

    if kind == "docx":
        out = add_watermark_docx(path, canvas)
    elif kind == "pptx":
        out = add_watermark_pptx(path, canvas)
    else:
        out = add_watermark_image(path, canvas)

    return {"file": path, "ok": True, "output": out}


def cmd_add(args):
    opts = {
        "mode": "text" if args.text else "image",
        "text": args.text or "机密",
        "image": args.image or "",
        "color": args.color,
        "opacity": args.opacity,
        "font_size": args.font_size,
        "diagonal": args.diagonal,
        "tile": not args.single,
    }
    if opts["mode"] == "image" and not opts["image"]:
        print("❌ 图片水印需指定 --image 路径")
        return 1

    if args.dir:
        results = []
        for p in sorted(Path(args.dir).rglob("*")):
            if p.suffix.lower() in EXT_MAP:
                results.append(process_file(str(p), opts))
        ok = sum(1 for r in results if r.get("ok"))
        print(f"✅ 批量水印完成：{ok}/{len(results)} 成功")
        for r in results:
            if r.get("ok"):
                print(f"   → {r['output']}")
            else:
                print(f"   ⚠️ {r['file']}: {r.get('error')}")
        return 0 if ok else 1
    else:
        if not args.file:
            print("❌ 需指定 --file 或 --dir")
            return 1
        res = process_file(args.file, opts)
        if res.get("ok"):
            print(f"✅ 水印完成：{res['output']}")
            return 0
        print(f"❌ {res.get('error')}")
        return 1


def main():
    parser = argparse.ArgumentParser(description="批量水印工具 v5.2")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("add", help="添加水印")
    p.add_argument("--file", default="", help="单个文件路径")
    p.add_argument("--dir", default="", help="批量目录")
    p.add_argument("--text", default="", help="文字水印内容")
    p.add_argument("--image", default="", help="图片水印路径（图片水印模式）")
    p.add_argument("--color", default="200,200,200", help="水印颜色 RGB，如 200,200,200")
    p.add_argument("--opacity", type=int, default=90, help="透明度 0-255")
    p.add_argument("--font-size", type=int, default=48, help="字号/水印尺寸")
    p.add_argument("--diagonal", action="store_true", help="对角线布局（否则平铺）")
    p.add_argument("--single", action="store_true", help="单张大图居中（不平铺）")
    p.set_defaults(func=cmd_add)

    args = parser.parse_args()
    if not getattr(args, "command", None):
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
