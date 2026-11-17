#!/usr/bin/env python3
"""PDF 图文提取工具（来源/目标无关）。

封装 trans-doc-to-md 所需的 PDF 提取能力：抽文字、全本缩略图、按分数带裁剪、
卡片检测裁剪。不依赖任何知识库，只读本地 PDF。

依赖：pymupdf(fitz) + Pillow + numpy
    pip install pymupdf pillow numpy

用法：
    # 抽纯文字 → out/paper.txt（并打印中文占比，辅助语言判定）
    python3 pdf_extract.py paper.pdf --text --out-dir out

    # 全本逐页缩略图 → out/thumbs/p001.png ...（目视核对哪些页有图表）
    python3 pdf_extract.py paper.pdf --thumbs --out-dir out [--dpi 70]

    # 按页面比例裁剪某页的一个纵向条带（自动收紧白边）
    python3 pdf_extract.py paper.pdf --crop 46 --band 0.13 0.26 --out out/images/chart_p47.png
        [--left 0.06 --right 0.94 --dpi 200]

    # 卡片检测裁剪某页最大填充矩形（报告图表卡片）
    python3 pdf_extract.py paper.pdf --card 35 --out out/images/card_p36.png

注：页码用 0 基索引（idx），即「打印第 47 页」通常是 --crop 46。
"""
import argparse
import os
import sys


def _need(mod):
    try:
        return __import__(mod)
    except ImportError:
        sys.exit(f"ERROR: 缺少依赖 {mod}，请先 `pip install pymupdf pillow numpy`")


def cmd_text(doc, out_dir):
    text = "".join(page.get_text() for page in doc)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "paper.txt")
    open(path, "w").write(text)
    head = text[:500]
    zh = sum(1 for c in head if "\u4e00" <= c <= "\u9fff")
    ratio = zh / max(len(head), 1)
    print(f"Pages: {doc.page_count}, chars: {len(text)} -> {path}")
    print(f"中文字符占比(前500字): {ratio:.0%}  =>  {'中文，跳过翻译' if ratio >= 0.30 else '非中文，需翻译为中英对照'}")


def cmd_thumbs(doc, out_dir, dpi):
    fitz = _need("fitz")
    d = os.path.join(out_dir, "thumbs")
    os.makedirs(d, exist_ok=True)
    for i in range(doc.page_count):
        pix = doc[i].get_pixmap(dpi=dpi)
        pix.save(os.path.join(d, f"p{i+1:03d}.png"))
    print(f"渲染 {doc.page_count} 页缩略图(dpi={dpi}) -> {d}/  （目视核对哪些页含图表）")


def cmd_crop(doc, idx, band, out, left, right, dpi):
    _need("numpy"); Image = _need("PIL.Image")
    import numpy as np
    from PIL import Image as PILImage
    top_frac, bot_frac = band
    pix = doc[idx].get_pixmap(dpi=dpi)
    full = PILImage.frombytes("RGB", [pix.width, pix.height], pix.samples)
    W, H = full.size
    crop = full.crop((int(W*left), int(H*top_frac), int(W*right), int(H*bot_frac)))
    arr = np.asarray(crop.convert("L")); m = arr < 245
    rs = np.where(m.any(axis=1))[0]; cs = np.where(m.any(axis=0))[0]
    pad = 16
    if len(rs) and len(cs):
        crop = crop.crop((max(int(cs[0])-pad, 0), max(int(rs[0])-pad, 0),
                          min(int(cs[-1])+pad, crop.width), min(int(rs[-1])+pad, crop.height)))
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    crop.save(out)
    print(f"{out}  {crop.size}  (page idx={idx}, band={top_frac}-{bot_frac})")
    print("→ 用 Read 工具预览，确认只含图形/卡片、无正文截断。")


def cmd_card(doc, idx, out, mat_scale=2.4, pad=7):
    fitz = _need("fitz")
    page = doc[idx]
    W, H = page.rect.width, page.rect.height
    best = None
    for dr in page.get_drawings():
        r = dr["rect"]
        if r.width <= 0 or r.height <= 0:
            continue
        af = (r.width * r.height) / (W * H)
        if 0.10 < af < 0.78 and r.width > 0.5 * W and r.height > 0.10 * H:
            if best is None or r.width * r.height > best.width * best.height:
                best = r
    if not best:
        print(f"page idx={idx}: 未检测到卡片背景矩形，改用 --crop --band 手动裁剪。")
        return
    clip = fitz.Rect(best.x0-pad, best.y0-pad, best.x1+pad, best.y1+pad)
    pix = page.get_pixmap(matrix=fitz.Matrix(mat_scale, mat_scale), clip=clip)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    pix.save(out)
    print(f"{out}  ({pix.width}x{pix.height})  card@idx{idx}")
    print("⚠️ 卡片检测对纯文字卡片也会命中，务必 Read 预览核对，只留真数据图表。")


def main():
    ap = argparse.ArgumentParser(description="PDF 图文提取工具")
    ap.add_argument("pdf")
    ap.add_argument("--out-dir", default="out")
    ap.add_argument("--text", action="store_true")
    ap.add_argument("--thumbs", action="store_true")
    ap.add_argument("--dpi", type=int, default=70)
    ap.add_argument("--crop", type=int, metavar="PAGE_IDX")
    ap.add_argument("--band", nargs=2, type=float, metavar=("TOP", "BOT"))
    ap.add_argument("--left", type=float, default=0.06)
    ap.add_argument("--right", type=float, default=0.94)
    ap.add_argument("--card", type=int, metavar="PAGE_IDX")
    ap.add_argument("--out", help="单图输出路径（--crop / --card 用）")
    args = ap.parse_args()

    fitz = _need("fitz")
    doc = fitz.open(args.pdf)

    did = False
    if args.text:
        cmd_text(doc, args.out_dir); did = True
    if args.thumbs:
        cmd_thumbs(doc, args.out_dir, args.dpi); did = True
    if args.crop is not None:
        if not (args.band and args.out):
            sys.exit("--crop 需配合 --band TOP BOT 和 --out PATH")
        cmd_crop(doc, args.crop, args.band, args.out, args.left, args.right,
                 args.dpi if args.dpi != 70 else 200)
        did = True
    if args.card is not None:
        if not args.out:
            sys.exit("--card 需配合 --out PATH")
        cmd_card(doc, args.card, args.out); did = True
    if not did:
        ap.print_help()


if __name__ == "__main__":
    main()
