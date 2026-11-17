#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HBR 商业杂志横版 build 流水线（reading-notes-master v2.7 · templates/hbr-magazine/）

从 88 页《哈佛商业评论 2025 年度精选》实战沉淀（PDF 11.7MB 三重验收通过）。
六步：合并 → Chrome 渲染 → 三重验收 → PDF 瘦身 → PPTX 同源 → 打包。

用法：
  cp build-template.py <项目>/build_mag.py    # 改下面 CONFIG 六个参数
  python3 build_mag.py                        # 系统 python3（依赖 pymupdf/PIL/python-pptx）

为什么用 Chrome headless 而不是 Playwright：杂志页是静态 HTML+CSS，
Chrome --print-to-pdf 直接出纸，矢量文本+JPEG 直通，无需浏览器驱动。
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))

# ============================================================ CONFIG（每项目改这里）
FRAGMENTS = ["_mag_a1.html", "_mag_a2.html", "_mag_b1.html",
             "_mag_b2.html", "_mag_c1.html", "_mag_c2.html"]  # 生成器产物（按序合并）
MAG_CSS = os.path.join(HERE, "mag.css")          # 设计系统（同模板目录或项目内）
BOOK_TITLE = "哈佛商业评论 2025 年度精选 · BEST OF 2025"
PAGE_W, PAGE_H = 612, 756                        # pt，MediaBox 验收锚点
PDF_NAME = "out/哈佛商业评论2025年度精选_版式复刻_88页.pdf"
PPTX_NAME = "out/哈佛商业评论2025年度精选_版式复刻_88页.pptx"
ASSET_DIRS = ["assets/mag", "assets/scrim"]      # 打包进交付目录的资产
BUILD_PPTX = True                                # 需要 PPTX 时确保 python-pptx 可用
# ============================================================ CONFIG END

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def log(*a):
    print(*a, flush=True)


# ---------------------------------------------------------------- ① 合并
def merge():
    """拼接生成器片段 → full.html（CSS 必须内联！Chrome 不保证加载外链样式的时序）"""
    body = []
    for frag in FRAGMENTS:
        p = os.path.join(HERE, frag)
        if not os.path.exists(p):
            sys.exit("[merge] 缺少片段: %s" % frag)
        body.append(open(p, encoding="utf-8").read())
    css = open(MAG_CSS, encoding="utf-8").read()
    html = ('<!DOCTYPE html>\n<html lang="zh-CN"><head><meta charset="utf-8">'
            "<title>%s</title>\n<style>%s\n</style></head>\n<body>\n%s\n</body></html>\n"
            % (BOOK_TITLE, css, "\n".join(body)))
    out = os.path.join(HERE, "full.html")
    open(out, "w", encoding="utf-8").write(html)
    n = len(re.findall(r'class="page[ "]', html))
    log("[merge] %s: %d pages, %.1f KB" % (out, n, len(html) / 1024))
    if n == 0:
        sys.exit("[merge] 0 页，检查片段产物")
    return out, n


# ---------------------------------------------------------------- ② Chrome 渲染
def render_pdf(html_path, pdf_path):
    """Chrome headless 出纸。坑：① 必须 file:// 绝对路径；② 必须全新 --user-data-dir
    （默认profile 会缓存 file:// 子资源，改 CSS 后渲染结果分毫不变）；③ --no-pdf-header-footer"""
    os.makedirs(os.path.dirname(os.path.abspath(pdf_path)), exist_ok=True)
    prof = tempfile.mkdtemp(prefix="chrome_mag_")
    url = "file://" + os.path.abspath(html_path)
    cmd = [CHROME, "--headless=new", "--user-data-dir=" + prof,
           "--no-sandbox", "--disable-gpu", "--disable-software-rasterizer",
           "--disable-dev-shm-usage", "--no-pdf-header-footer",
           "--print-to-pdf=" + os.path.abspath(pdf_path),
           "--virtual-time-budget=20000", url]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    shutil.rmtree(prof, ignore_errors=True)
    if not os.path.exists(pdf_path):
        log(r.stderr[-2000:])
        sys.exit("[render] PDF 未生成")
    log("[render] %s: %.2f MB" % (pdf_path, os.path.getsize(pdf_path) / 1e6))


# ---------------------------------------------------------------- ③ 三重验收
def validate_pdf(pdf_path):
    """MediaBox 恒定 / 逐页文本块零溢出 / 零空页（空页=无文本且无图形无图像）"""
    import pymupdf
    doc = pymupdf.open(pdf_path)
    errors, empty_pages = [], []
    for i, page in enumerate(doc, 1):
        mb = page.rect
        if abs(mb.width - PAGE_W) > 0.6 or abs(mb.height - PAGE_H) > 0.6:
            errors.append("p%d: MediaBox %.1fx%.1f != %dx%d" % (i, mb.width, mb.height, PAGE_W, PAGE_H))
        txt_len = 0
        for block in page.get_text("dict")["blocks"]:
            if block.get("type") != 0:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    txt_len += len(span["text"].strip())
                    x0, y0, x1, y1 = span["bbox"]
                    if x0 < -1 or y0 < -1 or x1 > PAGE_W + 1 or y1 > PAGE_H + 1:
                        errors.append("p%d: 文本溢出 (%.1f,%.1f,%.1f,%.1f) %r"
                                      % (i, x0, y0, x1, y1, span["text"][:30]))
        if txt_len == 0 and not page.get_drawings() and not page.get_images():
            empty_pages.append(i)
    doc.close()
    log("[validate] pages=%d MediaBox/溢出=%d 空页=%s %s"
        % (len(pymupdf.open(pdf_path)), len(errors), empty_pages[:10], errors[:10]))
    return len(errors) == 0 and not empty_pages


# ---------------------------------------------------------------- ④ PDF 瘦身
def slim_pdf(pdf_path):
    """两级瘦身（实战 18.3MB → 11.7MB，画质不变）：
    A. XObject 内容哈希去重——Chrome 对每页背景各嵌一份，跨页同图去重；
    B. garbage=4 + clean 回收孤儿对象。
    不做有损重压缩（q76→q72 实测仅省 5%，不值得）。"""
    import pymupdf
    import hashlib
    import collections
    doc = pymupdf.open(pdf_path)
    # A. 收集每页资源引用（页面 /Resources 可能是间接引用也可能内联）
    page_refs = []
    for pno in range(len(doc)):
        p = doc[pno]
        for img in p.get_images(full=True):
            page_refs.append((p.xref, img[7], img[0]))
    groups = collections.defaultdict(list)
    for _, _, x in page_refs:
        try:
            groups[hashlib.md5(doc.xref_stream_raw(x)).hexdigest()].append(x)
        except Exception:
            pass
    remap = {}
    for xs in groups.values():
        for x in xs[1:]:
            remap[x] = xs[0]
    done, miss = set(), 0
    for page_xref, name, x in page_refs:
        if x not in remap or page_xref in done:
            continue
        src = doc.xref_object(page_xref, compressed=True)
        m = re.search(r"/Resources\s+(\d+)\s+0\s+R", src)
        if m:
            rx = int(m.group(1))
            full = doc.xref_object(rx, compressed=True)
        else:
            rx = page_xref
            full = src
        old = "/%s %d 0 R" % (name, x)
        new = "/%s %d 0 R" % (name, remap[x])
        if old not in full:
            miss += 1
            continue
        doc.update_object(rx, full.replace(old, new, 1))
        done.add(page_xref)
    # B. 回收
    tmp = pdf_path + ".slim"
    doc.save(tmp, garbage=4, deflate=True, clean=True)
    doc.close()
    shutil.move(tmp, pdf_path)
    log("[slim] 去重 %d 处（miss %d）→ %.2f MB"
        % (len(remap), miss, os.path.getsize(pdf_path) / 1e6))


# ---------------------------------------------------------------- ⑤ PPTX 同源
def build_pptx(html_path, pptx_path):
    """从 full.html 解析页型同源重建 16:9 幻灯片。
    实测要点（88 页零越界）：
    - kicker 文本框宽度必须 clamp 到页宽（固定 9in 会在右侧 kicker 上越界 14 处）；
    - 期号总览网格 4 列×3 行（3×4 会超 7.5in 页高）；
    - 封面/照片用 add_picture + crop_left/right/top/bottom 按目标框宽高比裁切；
    - 编辑页翻面布局几何：照片 6.4in + 文字 5.85in，flip 时文字在左(x=0.55)。"""
    try:
        from pptx import Presentation
        from pptx.util import Inches, Pt, Emu
        from pptx.dml.color import RGBColor
        from pptx.enum.text import PP_ALIGN
        from pptx.enum.shapes import MSO_SHAPE
        from pptx.oxml.ns import qn
        from PIL import Image
    except ImportError:
        log("[pptx] python-pptx 缺失，跳过（pip install python-pptx）")
        return
    import html as H

    RED = RGBColor(0xE4, 0x18, 0x24)
    GOLD = RGBColor(0xF0, 0x9C, 0x18)
    INK = RGBColor(0x23, 0x1F, 0x20)
    GRAY = RGBColor(0x6E, 0x6A, 0x67)
    RULE = RGBColor(0xD8, 0xD5, 0xD0)
    CREAM = RGBColor(0xF4, 0xF1, 0xEA)
    WHITE = RGBColor(0xFF, 0xFF, 0xFF)
    DARK = RGBColor(0x17, 0x14, 0x1A)
    BODYTX = RGBColor(0x2B, 0x27, 0x29)
    SANS, SERIF = "PingFang SC", "Georgia"
    EMU_W, EMU_H = Inches(13.333), Inches(7.5)

    prs = Presentation()
    prs.slide_width, prs.slide_height = EMU_W, EMU_H
    BLANK = prs.slide_layouts[6]

    def _set_font(run, size, color, bold=False, font=SANS):
        f = run.font
        f.size, f.bold, f.name = Pt(size), bold, font
        f.color.rgb = color
        rPr = run._r.get_or_add_rPr()
        ea = rPr.find(qn("a:ea"))
        if ea is None:
            ea = rPr.makeelement(qn("a:ea"), {})
            rPr.append(ea)
        ea.set("typeface", font)

    def rect(s, x, y, w, h, color):
        sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
        sh.fill.solid()
        sh.fill.fore_color.rgb = color
        sh.line.fill.background()
        return sh

    def text(s, x, y, w, h, content, align=PP_ALIGN.LEFT):
        tb = s.shapes.add_textbox(x, y, w, h)
        tf = tb.text_frame
        tf.word_wrap = True
        lines = str(content[0]).split("\n")
        for i, ln in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align
            r = p.add_run()
            r.text = ln
            _set_font(r, content[1], content[2], content[3], content[4])
        return tb

    def kicker(s, x, y, label, color=RED, size=10.5):
        rect(s, x, Emu(int(y) + int(Inches(0.02))), Inches(0.09), Inches(0.09), color)
        tx = Emu(int(x) + int(Inches(0.17)))
        w = Emu(max(int(Inches(1.0)), int(EMU_W) - int(tx) - int(Inches(0.2))))  # clamp 防越界
        text(s, tx, y, w, Inches(0.26), (label, size, color, True, SANS))

    def photo(s, path, x, y, w, h):
        """按目标框宽高比裁切贴图（cover）"""
        if not os.path.exists(path):
            return
        im = Image.open(path)
        iw, ih = im.size
        tar = int(w) / int(h)
        src = iw / ih
        pic = s.shapes.add_picture(path, x, y, w, h)
        if src > tar:      # 源更宽 → 裁左右
            frac = (1 - tar / src) / 2
            pic.crop_left = frac
            pic.crop_right = frac
        elif src < tar:    # 源更高 → 裁上下
            frac = (1 - src / tar) / 2
            pic.crop_top = frac
            pic.crop_bottom = frac
        return pic

    def pageno(s, no, section=""):
        text(s, Inches(0.55), Inches(7.08), Inches(6), Inches(0.25), (str(no), 8, INK, True, SANS))
        text(s, Inches(6.8), Inches(7.08), Inches(5.98), Inches(0.25),
             (section, 8, GRAY, False, SANS), align=PP_ALIGN.RIGHT)

    def strip_tags(x):
        x = re.sub(r"<br\s*/?>", "\n", x)
        x = re.sub(r"</p>", "\n", x)
        x = re.sub(r"<[^>]+>", "", x)
        return H.unescape(x).strip()

    def get_text(chunk, cls):
        m = re.search(r'class="%s">(.*?)</div>' % cls, chunk, re.S)
        return strip_tags(m.group(1)) if m else ""

    def get_html(chunk, cls):
        m = re.search(r'class="%s">(.*?)</div>' % cls, chunk, re.S)
        return m.group(1) if m else ""

    html_text = open(html_path, encoding="utf-8").read()
    pages = re.split(r'(?=<div class="page )', html_text)[1:]
    pages = [p[: p.rfind("</div>")] for p in pages]  # 去掉页尾收口
    A = os.path.join(HERE, "..", "assets", "mag")

    def img_of(chunk, cls):
        m = re.search(r'class="%s"[^>]*url\((?:\.\./assets/mag/)?([^)]+?)(?:\.jpg)?\)' % cls, chunk)
        return os.path.join(A, m.group(1) + ".jpg") if m else None

    for i, chunk in enumerate(pages):
        s = prs.slides.add_slide(BLANK)
        no = i + 1
        if "mag-cover" in chunk:
            bg = img_of(chunk, "page fullbleed mag-cover")
            photo(s, bg, 0, 0, EMU_W, EMU_H)
            rect(s, 0, 0, EMU_W, Inches(2.6), DARK)  # 顶部压暗条（简版遮罩）
            text(s, Inches(0.55), Inches(0.5), Inches(6), Inches(0.6),
                 (get_text(chunk, "mc-mast-l"), 15, WHITE, True, SANS))
            text(s, Inches(0.55), Inches(1.7), Inches(12.2), Inches(1.8),
                 (get_text(chunk, "mc-title"), 40, WHITE, True, SANS))
            pageno(s, no)
        elif "mag-div" in chunk:
            bg = img_of(chunk, "page fullbleed mag-div")
            photo(s, bg, 0, 0, EMU_W, EMU_H)
            rect(s, 0, Inches(4.6), EMU_W, Inches(2.9), DARK)
            text(s, Inches(0.55), Inches(0.5), Inches(4), Inches(1.6),
                 (get_text(chunk, "md-num"), 96, WHITE, True, SANS))
            text(s, Inches(0.55), Inches(5.0), Inches(12.2), Inches(0.9),
                 (get_text(chunk, "md-title"), 30, WHITE, True, SANS))
            text(s, Inches(0.55), Inches(6.0), Inches(12.2), Inches(0.5),
                 (get_text(chunk, "md-sub"), 11, GOLD, True, SANS))
            pageno(s, no)
        elif "mag-ed" in chunk:
            flip = "me-flip" in chunk
            pw = Inches(6.4)
            photo(s, img_of(chunk, "me-photo"), 0 if not flip else Inches(6.93), 0, pw, EMU_H)
            tx = Inches(6.93) if not flip else Inches(0.55)
            kicker(s, tx, Inches(0.55), get_text(chunk, "me-kick"))
            text(s, tx, Inches(0.95), Inches(5.85), Inches(1.4),
                 (get_text(chunk, "me-title"), 24, INK, True, SANS))
            text(s, tx, Inches(2.4), Inches(5.85), Inches(1.2),
                 (get_text(chunk, "me-deck"), 11, BODYTX, False, SERIF))
            text(s, tx, Inches(3.7), Inches(5.85), Inches(3.2),
                 (strip_tags(get_html(chunk, "me-text")), 9.5, BODYTX, False, SANS))
            pageno(s, no)
        elif "mag-stat" in chunk:
            pw = Inches(4.3)
            photo(s, img_of(chunk, "ms-photo"), 0, 0, pw, EMU_H)
            kicker(s, Inches(4.75), Inches(0.55), get_text(chunk, "ms-kick"))
            text(s, Inches(4.75), Inches(0.95), Inches(8), Inches(1.7),
                 (get_text(chunk, "ms-num"), 88, INK, True, SANS))
            text(s, Inches(4.75), Inches(2.7), Inches(8), Inches(0.5),
                 (get_text(chunk, "ms-desc"), 12, BODYTX, True, SANS))
            text(s, Inches(4.75), Inches(3.4), Inches(8), Inches(3.4),
                 (strip_tags(get_html(chunk, "ms-text")), 10, BODYTX, False, SANS))
            pageno(s, no)
        elif "mag-chart" in chunk:
            kicker(s, Inches(0.55), Inches(0.5), get_text(chunk, "mch-kick"))
            text(s, Inches(0.55), Inches(0.88), Inches(12.2), Inches(0.9),
                 (get_text(chunk, "mch-title"), 26, INK, True, SANS))
            text(s, Inches(0.55), Inches(1.85), Inches(12.2), Inches(0.6),
                 (get_text(chunk, "mch-sub"), 11, GRAY, False, SERIF))
            st = img_of(chunk, "mch-stage")
            if st:
                photo(s, st, Inches(1.42), Inches(2.55), Inches(10.5), Inches(3.6))
            text(s, Inches(0.55), Inches(6.3), Inches(12.2), Inches(0.7),
                 (get_text(chunk, "mch-insight"), 9.5, BODYTX, False, SANS))
            pageno(s, no)
        elif "mag-photo" in chunk:
            photo(s, img_of(chunk, "page fullbleed mag-photo"), 0, 0, EMU_W, EMU_H)
            rect(s, 0, Inches(5.4), EMU_W, Inches(2.1), DARK)
            text(s, Inches(0.55), Inches(5.7), Inches(12.2), Inches(0.4),
                 (get_text(chunk, "mp-kick"), 10, GOLD, True, SANS))
            text(s, Inches(0.55), Inches(6.15), Inches(12.2), Inches(1.0),
                 (get_text(chunk, "mp-txt"), 11, WHITE, False, SERIF))
            pageno(s, no)
        elif "mag-quote" in chunk:
            photo(s, img_of(chunk, "page fullbleed mag-quote"), 0, 0, EMU_W, EMU_H)
            rect(s, 0, 0, EMU_W, EMU_H, DARK)
            text(s, Inches(1.2), Inches(2.5), Inches(10.9), Inches(2.2),
                 (get_text(chunk, "mq-quote"), 28, WHITE, True, SANS), align=PP_ALIGN.CENTER)
            text(s, Inches(1.2), Inches(5.0), Inches(10.9), Inches(0.5),
                 (get_text(chunk, "mq-src"), 10, GOLD, True, SANS), align=PP_ALIGN.CENTER)
            pageno(s, no)
        elif "mag-toc" in chunk:
            text(s, Inches(0.55), Inches(0.5), Inches(12.2), Inches(0.6),
                 ("目录 · CONTENTS", 24, INK, True, SANS))
            text(s, Inches(0.55), Inches(1.4), Inches(12.2), Inches(5.4),
                 (strip_tags(get_html(chunk, "toc-body")), 10, BODYTX, False, SANS))
            pageno(s, no)
        elif "mag-imap" in chunk:
            text(s, Inches(0.55), Inches(0.5), Inches(12.2), Inches(0.7),
                 (get_text(chunk, "im-title"), 26, INK, True, SANS))
            text(s, Inches(0.55), Inches(1.3), Inches(12.2), Inches(0.5),
                 (get_text(chunk, "im-sub"), 10, GRAY, False, SERIF))
            cards = re.findall(r'<div class="im-card">(.*?)</div>\s*</div>', chunk, re.S)
            cw, chh = Inches(2.90), Inches(1.52)
            for i2, c in enumerate(cards[:12]):
                col, row = i2 % 4, i2 // 4
                x = Emu(int(Inches(0.55)) + col * (int(cw) + int(Inches(0.19))))
                y = Emu(int(Inches(2.18)) + row * (int(chh) + int(Inches(0.14))))
                m = re.search(r'class="im-img"[^>]*url\((?:\.\./assets/(?:mag|use)/)?([^)]+?)(?:\.jpg)?\)', c)
                if m:
                    for d in ("mag", "use", "use2"):
                        p = os.path.join(HERE, "..", "assets", d, m.group(1) + ".jpg")
                        if os.path.exists(p):
                            photo(s, p, x, y, cw, Inches(0.58))
                            break
                rect(s, x, Emu(int(y) + int(Inches(0.58))), cw, Pt(2), INK)
                lab = re.search(r'class="im-lab">(.*?)</div>', c, re.S)
                if lab:
                    text(s, x, Emu(int(y) + int(Inches(0.63))), cw, Inches(0.22),
                         (strip_tags(lab.group(1)), 10.5, INK, True, SANS))
                text(s, x, Emu(int(y) + int(Inches(0.88))), cw, Inches(0.24),
                     (get_text(c, "im-theme"), 9.5, BODYTX, True, SANS))
                text(s, x, Emu(int(y) + int(Inches(1.14))), cw, Inches(0.34),
                     (get_text(c, "im-desc"), 8, GRAY, False, SANS))
            pageno(s, no)
        else:  # mag-text 等兜底：标题 + 双栏正文
            text(s, Inches(0.55), Inches(0.5), Inches(12.2), Inches(0.5),
                 (get_text(chunk, "mt-kick"), 10.5, RED, True, SANS))
            text(s, Inches(0.55), Inches(1.0), Inches(12.2), Inches(1.2),
                 (get_text(chunk, "mt-title"), 26, INK, True, SANS))
            text(s, Inches(0.55), Inches(2.4), Inches(12.2), Inches(4.4),
                 (strip_tags(get_html(chunk, "mt-text")), 10, BODYTX, False, SANS))
            pageno(s, no)
    os.makedirs(os.path.dirname(os.path.abspath(pptx_path)), exist_ok=True)
    prs.save(pptx_path)
    log("[pptx] %s: %d slides, %.1f MB"
        % (pptx_path, len(prs.slides._sldIdLst), os.path.getsize(pptx_path) / 1e6))


# ---------------------------------------------------------------- ⑥ 打包
def package(pdf_path, pptx_path):
    out = os.path.join(HERE, "delivery")
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    for f in (pdf_path, pptx_path):
        if os.path.exists(f):
            shutil.copy2(f, out)
    for d in ASSET_DIRS:
        src = os.path.join(HERE, "..", d)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(out, os.path.basename(d)))
    # HTML 交付件（自包含 CSS）
    shutil.copy2(os.path.join(HERE, "full.html"), os.path.join(out, "notes.html"))
    log("[package] -> %s" % out)


def main():
    html_path, n = merge()
    render_pdf(html_path, PDF_NAME)
    if not validate_pdf(PDF_NAME):
        sys.exit("[validate] 三重验收未过，修页面再构建")
    slim_pdf(PDF_NAME)
    if not validate_pdf(PDF_NAME):
        sys.exit("[validate] 瘦身后验收未过")
    if BUILD_PPTX:
        build_pptx(html_path, PPTX_NAME)
    package(PDF_NAME, PPTX_NAME)
    log("DONE ✅")


if __name__ == "__main__":
    main()
