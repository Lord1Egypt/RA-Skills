# -*- coding: utf-8 -*-
"""
exact_replication.py — 期刊「完全复刻」通用引擎（Stage A + Stage B）

契约（Exact Replication Contract）
--------------------------------
固定设计层（不可变）：画布尺寸 / 页序 / 页数 / 页面原型 / 栅格 / 栏位 /
边距 / 页眉页脚 / 页码 / 装饰矢量 / 图片位置与尺寸 / 图表位置与图形 /
字体族名 / 字号 / 字重 / 字距 / 行距 / 颜色 / 文本基线位置。

可更新内容层（三类槽位）：
  text  — 文字内容（逐行 span 原位替换）
  image — 图片内容（同 bbox 覆盖）
  chart — 图表数据文字（矢量图形保留，只换数据）

字体资源边界（诚实声明）
------------------------
原刊字体多为页级嵌入的 Type1/PFA 子集，仅含该页用到的 glyph；
本地通常没有商业字体完整版。因此：
  Tier 1  目标页自身子集可覆盖新文案 -> 直接复用，字形 100% 原样
  Tier 2  同页子集不覆盖 -> 视觉近似字体，记录 font_fallback
  Tier 3  中文/日文等新语种 -> CJK 字形资源扩展（china-s / Songti.ttc）
字形本身属于「文字内容」的载体，随内容更新；但字号/字重/字距/行距/
颜色/基线/字体族名等设计参数必须保持。跨页子集不可直接混用（子集化
后 /Encoding 被重排，按 WinAnsi 写字节会取错 glyph），本引擎只用目标页
自身子集，避免错形。

零偏差验收
----------
槽位外像素必须 100% 相同（渲染矩阵可配，默认 2x）；
槽位内必须发生可测变化；画布/页序/页数/资源清单一致。
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from collections import defaultdict

import fitz  # PyMuPDF
import numpy as np

REDACT_IMG_NONE = fitz.PDF_REDACT_IMAGE_NONE        # 0
REDACT_ART_NONE = fitz.PDF_REDACT_LINE_ART_NONE     # 0
REDACT_TXT_DEL = fitz.PDF_REDACT_TEXT_REMOVE        # 0


# --------------------------------------------------------------------------
# 基础工具
# --------------------------------------------------------------------------

def hexrgb(s, default=(0, 0, 0)):
    if not s or not isinstance(s, str) or not s.startswith("#"):
        return default
    try:
        return tuple(int(s[i:i + 2], 16) / 255.0 for i in (1, 3, 5))
    except Exception:
        return default


def rgbhex(c):
    return "#%02X%02X%02X" % tuple(int(round(v * 255)) for v in c[:3])


def render_array(page, matrix=2.0, clip=None):
    """渲染为 (H,W,3) uint8，正确处理 pixmap stride padding。"""
    m = fitz.Matrix(matrix, matrix)
    pix = page.get_pixmap(matrix=m, alpha=False, clip=clip)
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.stride)
    return a[:, :pix.width * 3].reshape(pix.height, pix.width, 3).copy()


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# --------------------------------------------------------------------------
# 逐页建模（Stage A-1）：不依赖任何外部 JSON，任意期刊 PDF 可直接跑
# --------------------------------------------------------------------------

def build_page_models(doc, include_drawings=True):
    models = []
    for i in range(len(doc)):
        pg = doc[i]
        d = pg.get_text("dict")
        spans, images, drawings = [], [], []
        for blk in d.get("blocks", []):
            if blk.get("type") == 0:
                for ln in blk.get("lines", []):
                    for sp in ln.get("spans", []):
                        b = sp["bbox"]
                        spans.append(dict(
                            x0=round(b[0], 2), y0=round(b[1], 2),
                            x1=round(b[2], 2), y1=round(b[3], 2),
                            font=sp["font"], size=round(sp["size"], 2),
                            color=rgbhex(((sp["color"] >> 16 & 255) / 255,
                                          (sp["color"] >> 8 & 255) / 255,
                                          (sp["color"] & 255) / 255)),
                            text=sp["text"]))
            elif blk.get("type") == 1:
                b = blk["bbox"]
                images.append(dict(bbox=[round(v, 2) for v in b],
                                   w=blk.get("width", 0), h=blk.get("height", 0),
                                   ext=blk.get("ext", "")))
        if include_drawings:
            for dr in pg.get_drawings():
                r = dr.get("rect")
                if r is None:
                    continue
                drawings.append(dict(
                    rect=[round(v, 2) for v in (r.x0, r.y0, r.x1, r.y1)],
                    type=dr.get("type"),
                    fill=rgbhex(dr["fill"]) if dr.get("fill") else None,
                    stroke=rgbhex(dr["color"]) if dr.get("color") else None))
        size_ladder, font_ladder, color_ladder, x0_hist = (defaultdict(int) for _ in range(4))
        for s in spans:
            size_ladder[str(s["size"])] += 1
            font_ladder[s["font"]] += 1
            color_ladder[s["color"]] += 1
            x0_hist[str(int(s["x0"]) // 12 * 12)] += 1
        models.append(dict(
            page=i + 1,
            canvas=[round(pg.rect.width, 2), round(pg.rect.height, 2)],
            n_spans=len(spans), n_images=len(images), n_drawings=len(drawings),
            chars=sum(len(s["text"]) for s in spans),
            spans=spans, images=images, drawings=drawings,
            header=" | ".join(s["text"] for s in spans if s["y0"] < 45)[:200],
            footer=" | ".join(s["text"] for s in spans if s["y0"] > pg.rect.height - 45)[:200],
            size_ladder=dict(size_ladder), font_ladder=dict(font_ladder),
            color_ladder=dict(color_ladder), x0_hist=dict(x0_hist)))
    return models


def classify_archetype(pm, canvas_area):
    """启发式页面原型分类（跨刊通用）。"""
    n = pm["n_images"]
    cov = sum(max(0, i["bbox"][2] - i["bbox"][0]) * max(0, i["bbox"][3] - i["bbox"][1])
              for i in pm["images"]) / max(1, canvas_area)
    ch = pm["chars"]
    if ch == 0 and cov > 0.7:
        return "FULL-BLEED AD/IMAGE"
    if ch < 250 and cov > 0.6:
        return "SHORT/IMAGE"
    if ch < 400 and pm["n_drawings"] > 500:
        return "INFOGRAPHIC/AD"
    if ch < 600:
        return "SECTION OPENER"
    if ch > 6000:
        return "FEATURE/DEPARTMENT (DENSE)"
    if cov > 0.55 and ch < 1800:
        return "AD"
    if ch < 2200 and re.search(r"contents|in this issue", pm["header"], re.I):
        return "CONTENTS"
    return "FEATURE"


# --------------------------------------------------------------------------
# Stage A-2：1:1 矢量零偏差底版
# --------------------------------------------------------------------------

def replicate_1to1(src_path, out_path):
    src = fitz.open(src_path)
    dst = fitz.open()
    for i in range(len(src)):
        r = src[i].rect
        pg = dst.new_page(width=r.width, height=r.height)
        pg.show_pdf_page(pg.rect, src, i)
    dst.save(out_path, garbage=4, deflate=True)
    dst.close()
    src.close()
    return out_path


# --------------------------------------------------------------------------
# Stage B：槽位内容替换
# --------------------------------------------------------------------------

class FontResolver:
    """只用目标页自身嵌入字体子集；维护每页 fontname 缓存。"""

    def __init__(self, doc):
        self.doc = doc
        self.cache = {}          # (pno, short) -> (fontname, fitz.Font, buf)
        self.registered = defaultdict(set)

    def page_fonts(self, pno):
        return self.doc[pno - 1].get_fonts(full=True)

    def resolve(self, pno, short):
        key = (pno, short)
        if key in self.cache:
            return self.cache[key]
        pg = self.doc[pno - 1]
        for f in self.page_fonts(pno):
            xref, ext, typ, base = f[:4]
            name = base.split("+")[-1]
            if name != short:
                continue
            try:
                buf = self.doc.extract_font(xref)[3]
                fo = fitz.Font(fontbuffer=buf)
            except Exception:
                return None
            nm = "ER%d" % (len(self.registered[pno]) + 1)
            pg.insert_font(fontname=nm, fontbuffer=buf)
            self.registered[pno].add(nm)
            self.cache[key] = (nm, fo, buf)
            return self.cache[key]
        # 宽松匹配 1：忽略大小写与符号
        norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
        for f in self.page_fonts(pno):
            xref, ext, typ, base = f[:4]
            name = base.split("+")[-1]
            if norm(name) == norm(short):
                return self.resolve_exact(pno, name, xref)
        # 宽松匹配 2：最长公共前缀。PyMuPDF 会把 span 字体名截断到 22 字符，
        # 例如 ITCFranklinGothicStd-Boo -> ...-Book, ...-DmC -> ...-DmCd
        best, score = None, 0
        for f in self.page_fonts(pno):
            xref, ext, typ, base = f[:4]
            name = base.split("+")[-1]
            k = 0
            for ca, cb in zip(name, short):
                if ca != cb:
                    break
                k += 1
            if k > score:
                best, score = (name, xref), k
        if best and score >= 12:
            return self.resolve_exact(pno, best[0], best[1])
        return None

    def resolve_exact(self, pno, short, xref):
        key = (pno, short)
        if key in self.cache:
            return self.cache[key]
        pg = self.doc[pno - 1]
        try:
            buf = self.doc.extract_font(xref)[3]
            fo = fitz.Font(fontbuffer=buf)
        except Exception:
            return None
        nm = "ER%d" % (len(self.registered[pno]) + 1)
        pg.insert_font(fontname=nm, fontbuffer=buf)
        self.registered[pno].add(nm)
        self.cache[key] = (nm, fo, buf)
        return self.cache[key]


def fallback_font(short, cjk):
    """T2 回退必须匹配字重，否则 Display-Black 会掉成 Times-Roman 细体，
    直接违反「字重不变」的设计契约。"""
    if cjk:
        return "china-s"
    s = short.lower()
    serif = "haffner" in s
    bold = any(k in s for k in ("black", "hvy", "heavy", "bold", "dem"))
    italic = "italic" in s or s.endswith("it")
    if serif:
        return "tibi" if (bold and italic) else "tibo" if bold else "tiit" if italic else "tiro"
    return "hebi" if (bold and italic) else "hebo" if bold else "heit" if italic else "helv"


class ExactEditor:
    """在原 PDF 副本上做槽位替换：不重建页面，因此非槽位区域零偏差。"""

    def __init__(self, src_path, models=None):
        self.src_path = src_path
        self.doc = fitz.open(src_path)
        self.models = models or build_page_models(self.doc)
        self.fr = FontResolver(self.doc)
        self.slot_log = []
        self.masks = defaultdict(list)   # pno -> [Rect]

    # ---- 文字 ----------------------------------------------------------
    @staticmethod
    def fit_text(text, measure, size, width):
        """按可用宽度截断，绝不越出栏宽。measure(t)->pt 宽度。"""
        if not text:
            return ""
        out = ""
        for ch in text:
            if measure(out + ch) > width * 0.995:
                break
            out += ch
        return out

    @staticmethod
    def font_metrics(fname, fo=None):
        """返回 (measure_fn, ascender)。优先用真实嵌入字体量测。"""
        if fo is not None:
            return (lambda t: fo.text_length(t, fontsize=1.0), fo.ascender)
        try:
            f = fitz.Font(fontname=fname)
            return (lambda t: f.text_length(t, fontsize=1.0), f.ascender)
        except Exception:
            return (lambda t: len(t) * 0.5, 0.8)

    def _redact(self, pno, rects):
        """精确删除矩形内文字，保留图片、矢量与矩形外的一切内容。"""
        pg = self.doc[pno - 1]
        for r in rects:
            pg.add_redact_annot(r, fill=None, cross_out=False)
        pg.apply_redactions(images=REDACT_IMG_NONE,
                            graphics=REDACT_ART_NONE,
                            text=REDACT_TXT_DEL)

    def apply_text_slot(self, slot, values):
        """slot: {page, spans:[bbox...], design:{...}, original:[...]}
        values: 与 spans 一一对应的新文字列表。
        Tier 判定按「整行」进行：整行都能被原页子集覆盖才用原字体，
        否则整行统一用视觉最接近的替代字体，避免行内字形混杂。"""
        pno = slot["page"]
        pg = self.doc[pno - 1]
        spans = slot["spans"]
        if len(values) != len(spans):
            raise ValueError("slot %s: values %d != spans %d" %
                             (slot["id"], len(values), len(spans)))
        # 1. 精确移除原文（保留图片/矢量/其他文字）
        rects = [fitz.Rect(s["x0"] - 0.4, s["y0"] - 0.4,
                           s["x1"] + 0.4, s["y1"] + 0.4) for s in spans]
        self._redact(pno, rects)
        # 整槽位字体策略统一：多行引语若逐行各自判 tier，会出现部分行
        # 原 Black 字体、部分行 Times-Bold，字重不齐。任一不达标则整槽位回退。
        force_fallback = False
        if slot.get("uniform_font", True):
            for s, val in zip(spans, values):
                if not val:
                    continue
                if any(ord(c) > 0x2E80 for c in val):
                    continue          # CJK 单独处理，不影响英文行判断
                h = self.fr.resolve(pno, s.get("font", ""))
                if h is None or not all(h[1].has_glyph(ord(ch))
                                        for ch in val if not ch.isspace()):
                    force_fallback = True
                    break
        # 2. 原位注入新文字
        used, extra_rects = [], []
        for s, val in zip(spans, values):
            if not val:
                continue
            short = s.get("font", "")
            hit = self.fr.resolve(pno, short)
            cjk = any(ord(c) > 0x2E80 for c in val)
            fo = hit[1] if hit else None
            covered = (hit is not None and not cjk and not force_fallback and
                       all(fo.has_glyph(ord(ch)) for ch in val if not ch.isspace()))
            if covered:
                fname, tier = hit[0], "T1-original-subset"
                measure, _ = self.font_metrics("", fo)
            else:
                fname = fallback_font(short, cjk)
                tier = "T3-cjk-extension" if cjk else "T2-visual-fallback"
                measure, _ = self.font_metrics(fname)
            # 基线属于「固定设计层」：无论用哪档字形资源，都以目标页原字体的
            # ascender 定位。若误用替代字体自身 ascender（tiro≈1.05、
            # china-s≈1.04，而 HaffnerTIME≈0.743），文字会向下溢出槽位。
            asc_design = fo.ascender if hit else 0.78
            align = slot.get("align", "left")
            maxw = slot.get("max_width") or (s["x1"] - s["x0"] + slot.get("extra_width", 0))
            txt = self.fit_text(val, lambda t: measure(t) * s["size"],
                                s["size"], maxw)
            actual_w = measure(txt) * s["size"]
            if align == "center":
                x_start = (s["x0"] + s["x1"]) / 2 - actual_w / 2
            elif align == "right":
                x_start = s["x1"] - actual_w
            else:
                x_start = s["x0"]
            baseline = s["y0"] + asc_design * s["size"]
            col = hexrgb(s["color"])
            bold_design = any(k in short.lower()
                              for k in ("black", "hvy", "heavy", "bold", "dem"))
            # 中文只有 Regular 内置字形，遇到原刊 Black/Hvy 字重时用
            # fill+stroke 描边补足视觉字重，保住「字重不变」的设计参数。
            stroke = tier == "T3-cjk-extension" and bold_design
            kw = dict(fontname=fname, fontsize=s["size"], color=col)
            if stroke:
                kw.update(render_mode=2, border_width=0.022, fill=col)
            pg.insert_text((x_start, baseline), txt, **kw)
            used.append(dict(text=txt, tier=tier,
                             font=short if covered else fname,
                             size=s["size"], color=s["color"], align=align))
            extra_rects.append(fitz.Rect(x_start - 1, s["y0"] - 1,
                                         x_start + actual_w + 1, s["y1"] + 1))
        for r in rects + extra_rects:
            # mask 覆盖「删除区 + 实际绘制区」，并略作扩展容纳抗锯齿
            self.masks[pno].append(fitz.Rect(r.x0 - 1.5, r.y0 - 2.5,
                                             r.x1 + 1.5, r.y1 + 2.5))
        rec = dict(id=slot["id"], type=slot.get("type", "text"), page=pno,
                   n_spans=len(spans), tiers=sorted(set(u["tier"] for u in used)),
                   lines=used)
        self.slot_log.append(rec)
        return rec

    # ---- 图片 ----------------------------------------------------------
    def apply_image_slot(self, slot, image_path):
        pno = slot["page"]
        pg = self.doc[pno - 1]
        r = fitz.Rect(slot["bbox"])
        if os.path.exists(image_path):
            pg.insert_image(r, filename=image_path, overlay=True,
                            keep_proportion=False)
        else:
            raise FileNotFoundError(image_path)
        self.masks[pno].append(r)
        rec = dict(id=slot["id"], type="image", page=pno,
                   bbox=list(slot["bbox"]), source=os.path.basename(image_path))
        self.slot_log.append(rec)
        return rec

    # ---- 图表（数据文字替换，矢量图形 100% 保留）----------------------
    def apply_chart_slot(self, slot, values):
        return self.apply_text_slot(dict(slot, type="chart"), values)

    # ---- 图表（重绘型：遮盖 + 新图，扩展能力）--------------------------
    def apply_chart_redraw(self, slot, image_path, bg=(1, 1, 1)):
        pno = slot["page"]
        pg = self.doc[pno - 1]
        r = fitz.Rect(slot["bbox"])
        pg.draw_rect(r, color=None, fill=bg, overlay=True)
        pg.insert_image(r, filename=image_path, overlay=True,
                        keep_proportion=False)
        self.masks[pno].append(r)
        rec = dict(id=slot["id"], type="chart-redraw", page=pno,
                   bbox=list(slot["bbox"]), source=os.path.basename(image_path))
        self.slot_log.append(rec)
        return rec

    # ---- 应用内容包 ----------------------------------------------------
    def apply_pack(self, slots, pack):
        by_id = {s["id"]: s for s in slots}
        for sid, val in pack["values"].items():
            if sid not in by_id:
                raise KeyError("未知槽位 %s" % sid)
            slot = by_id[sid]
            t = slot["type"]
            if t in ("text", "chart"):
                self.apply_text_slot(slot, val)
            elif t == "image":
                self.apply_image_slot(slot, val)
            elif t == "chart-redraw":
                self.apply_chart_redraw(slot, val, hexrgb(slot.get("bg")))
            else:
                raise ValueError("未知槽位类型 %s" % t)
        return self.slot_log

    def save(self, out_path):
        self.doc.save(out_path, garbage=3, deflate=True)
        return out_path


def collision_report(models, slots, pad=0.4):
    """通用保护：检测文字/图表槽位的 redact 矩形是否会误删「非槽位」文字。

    首字下沉、跨栏大标题、压在正文上的页码/标注等，其 bbox 常与正文行
    相交。redact 按矩形删除字符 ink，一旦相交就会削掉设计元素，且被削的
    像素落在槽位外 —— 这类破坏不能靠扩大验收 mask 掩盖。
    返回冲突清单，调用方应在构建前处理（收缩矩形 / 改选行 / 重建元素）。
    """
    by_page = defaultdict(list)
    for s in slots:
        if "spans" in s:
            by_page[s["page"]].append(s)
    conflicts = []
    for pno, ss in by_page.items():
        chosen = set()
        target_rects = []
        for s in ss:
            for sp in s["spans"]:
                chosen.add((round(sp["x0"], 1), round(sp["y0"], 1), sp["text"]))
                target_rects.append(fitz.Rect(sp["x0"] - pad, sp["y0"] - pad,
                                              sp["x1"] + pad, sp["y1"] + pad))
        for sp in models[pno - 1]["spans"]:
            key = (round(sp["x0"], 1), round(sp["y0"], 1), sp["text"])
            if key in chosen:
                continue
            r = fitz.Rect(sp["x0"], sp["y0"], sp["x1"], sp["y1"])
            for t in target_rects:
                if (t & r).get_area() > 0.5:
                    conflicts.append(dict(page=pno, slot_rect=[round(v, 1) for v in t],
                                          victim_bbox=[round(sp["x0"], 1), round(sp["y0"], 1),
                                                       round(sp["x1"], 1), round(sp["y1"], 1)],
                                          victim_text=sp["text"][:60],
                                          victim_size=sp["size"]))
                    break
    return conflicts


# --------------------------------------------------------------------------
# 验收
# --------------------------------------------------------------------------

def verify(src_path, edited_path, masks, matrix=2.0, pad_px=3, out_json=None):
    a = fitz.open(src_path)
    b = fitz.open(edited_path)
    report = dict(source=src_path, edited=edited_path,
                  pages_source=len(a), pages_edited=len(b),
                  matrix=matrix, pad_px=pad_px, pages=[], summary={})
    size_ok = len(a) == len(b)
    for i in range(len(a)):
        if a[i].rect != b[i].rect:
            size_ok = False
    report["canvas_all_equal"] = size_ok

    worst_out = 0.0
    for pno in sorted(masks.keys()):
        pa, pb = a[pno - 1], b[pno - 1]
        ia, ib = render_array(pa, matrix), render_array(pb, matrix)
        if ia.shape != ib.shape:
            report["pages"].append(dict(page=pno, error="shape mismatch"))
            continue
        H, W, _ = ia.shape
        sc = W / pa.rect.width
        mask = np.zeros((H, W), bool)
        for r in masks[pno]:
            x0, y0, x1, y1 = [int(v * sc) for v in (r.x0, r.y0, r.x1, r.y1)]
            mask[max(0, y0 - pad_px):min(H, y1 + pad_px),
                 max(0, x0 - pad_px):min(W, x1 + pad_px)] = True
        diff = np.any(ia != ib, axis=2)
        outside = ~mask
        out_ch = int((diff & outside).sum())
        in_ch = int((diff & mask).sum())
        out_ratio = out_ch / max(1, int(outside.sum()))
        worst_out = max(worst_out, out_ratio)
        report["pages"].append(dict(
            page=pno, n_slots=len(masks[pno]),
            outside_pixels=int(outside.sum()), outside_changed=out_ch,
            outside_change_ratio=round(out_ratio, 8),
            outside_identical_pct=round(100 * (1 - out_ratio), 6),
            inside_changed=in_ch,
            inside_change_ratio=round(in_ch / max(1, int(mask.sum())), 6),
            full_page_identical_pct=round(100 * float((~diff).mean()), 4),
            mae=round(float(np.abs(ia.astype(np.int16) - ib.astype(np.int16)).mean()), 6),
            zero_drift=out_ch == 0))

    # 未改动页也必须 100% 相同
    touched = set(masks.keys())
    unchanged = []
    for pno in range(1, len(a) + 1):
        if pno in touched:
            continue
        ia, ib = render_array(a[pno - 1], 0.75), render_array(b[pno - 1], 0.75)
        unchanged.append(bool(np.array_equal(ia, ib)))
    report["summary"] = dict(
        edited_pages=len(touched),
        all_edited_pages_zero_drift=all(p.get("zero_drift") for p in report["pages"]),
        worst_outside_change_ratio=round(worst_out, 8),
        untouched_pages_checked=len(unchanged),
        untouched_pages_identical=all(unchanged) if unchanged else True,
        verdict="PASS" if (size_ok and worst_out == 0 and all(unchanged)) else "FAIL")
    if out_json:
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
    a.close(); b.close()
    return report
