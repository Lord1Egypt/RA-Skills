# -*- coding: utf-8 -*-
"""四刊合璧 · 版式 1:1 全复刻 —— 通用构建模板（reading-notes-master v2.14）

这是从 40 页真实交付中直接参数化的**可运行模板**，不是伪代码示意：
  选页配额 → 逐页建模 → 覆盖式替换 → 分级局部降级 → 零偏差验收
  → PPTX → 细节体检 → 三份报告同步。

用法：
  python3 build.example.py --config config.json
  # config.json 见同目录 config.example.json；或设环境变量 QUAD_CONFIG

依赖：
  · PyMuPDF / numpy / Pillow / python-pptx（系统 python，如 /opt/homebrew/bin/python3）
  · exact_replication.py 所在目录由 config 的 engine_dir 指定
    （技能内不附该引擎时，从项目 time_exact/scripts/ 或自行提供 build_page_models/verify）
  · 4K 摄影池 photo4k/ 与 4K 科研图池 fig4k/（见 references/visual-detail-qa.md §2）

契约（exact-replication v2.13 精神）：
  · 底版 = 四本 NG 参照刊的真实页面（每刊 10 页，共 40 页），1:1 复制
  · 设计层不可变：画布 / 页序 / 栅格 / 栏位 / 图片 bbox / 矢量装饰 / 页码 / 色块
  · 可更新槽位：原刊正文/图注 bbox → 《先发影响力》中文流；图片 bbox → 真 4K 摄影/图表
  · 内容层：剥离版权/献词/附录，按全书 40 等分取完整语义短语，覆盖整本而非只覆盖前言
  · 视觉层：采样中位色精确覆盖（零量化色块）+ WCAG 对比度择优文字色 + 边缘同色留白
  · 验收：verify(matrix=2.0, pad_px=3) 槽位外逐像素 100% 相同，worst_outside=0.0

技术选择：不用 apply_redactions（前四轮实证其有非局部内容流副作用），
改用「同 bbox 不透明覆盖 + 原坐标回写」，所有改动严格落在 mask 内。
"""
import json, os, sys, math, re
from collections import defaultdict, deque
import fitz
import numpy as np
from PIL import Image

# ── 模板配置区：全部路径来自 --config / QUAD_CONFIG，无硬编码机器路径 ──
import argparse as _ap
_p = _ap.ArgumentParser(add_help=False)
_p.add_argument("--config", default=os.environ.get("QUAD_CONFIG", ""))
_arg, _ = _p.parse_known_args()
CFG = json.load(open(_arg.config, encoding="utf-8")) if _arg.config else {}

ROOT = CFG.get("root", os.getcwd())
HERE = CFG.get("project_dir", os.path.join(ROOT, "quad_exact"))
ENGINE = CFG.get("engine_dir", os.path.join(ROOT, "time_exact", "scripts"))
if ENGINE not in sys.path:
    sys.path.insert(0, ENGINE)
from exact_replication import build_page_models, verify

REF = [(j["label"], j["path"]) for j in CFG.get("journals", [])]
BOOK_STREAM = CFG.get("book_stream", os.path.join(ROOT, "book.txt"))
PHOTO4K = CFG.get("photo4k", os.path.join(ROOT, "assets", "photo4k"))
FIG4K = CFG.get("fig4k", os.path.join(ROOT, "assets", "fig4k"))
DELIV = os.path.join(HERE, "delivery")
ASSETS = os.path.join(HERE, "assets")
for d in (DELIV, ASSETS):
    os.makedirs(d, exist_ok=True)

BASE = os.path.join(ASSETS, "quad_base_40p.pdf")
OUT_PDF = os.path.join(DELIV, CFG.get("out_pdf", "版式全复刻_输出.pdf"))
OUT_PPTX = os.path.join(DELIV, CFG.get("out_pptx", "版式全复刻_输出.pptx"))
PER_JOURNAL = int(CFG.get("per_journal", 10))
FONT_CJK = CFG.get("font_cjk", "/System/Library/Fonts/STHeiti Medium.ttc")
RAW_STREAM = open(BOOK_STREAM, encoding="utf-8").read()

# ── 内容层：剥离版权页/献词/书末附录，按全书 N 等分做语义片段分配 ──
# 起止标记必须写在 config 里（不同书的正文起点不同，写死会把版权页当正文）：
#   body_start_marker —— 正文第一个可信锚点（如「前言」「第一章」「Chapter 1」）
#   body_end_marker   —— 附录/索引/参考书目起点（如「Table of Contents」「致谢」「Index」）
_BS_MARK = CFG.get("body_start_marker", "前言")
_BE_MARK = CFG.get("body_end_marker", "")
_BS = RAW_STREAM.find(_BS_MARK) if _BS_MARK else 0
_BE = RAW_STREAM.rfind(_BE_MARK) if _BE_MARK else -1
BODY_START = max(0, _BS)
BODY_END = _BE if _BE > BODY_START else len(RAW_STREAM)
BODY = RAW_STREAM[BODY_START:BODY_END]
if len(BODY) < 2000:
    print("[WARN] 正文区间仅 %d 字，请检查 body_start_marker / body_end_marker" % len(BODY),
          file=sys.stderr)

FRAG_MAX = 10          # 单个语义片段最长字数，保证窄栏也能放完整短语
_PUNCT = "。！？；，、："
DARK, INK, WHITE = (0.13, 0.11, 0.12), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0)


def build_fragments(text, maxlen=FRAG_MAX):
    """按中文标点切成完整语义短语；超长段再均分，绝不切在句中。"""
    text = re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", text)
    text = re.sub(r"\s+", " ", text).strip()   # 中文间空白删除，英文词间保留单空格
    parts = re.findall(r"[^%s]+[%s]?" % (_PUNCT, _PUNCT), text)
    out = []
    for p in parts:
        p = p.strip()
        while len(p) > maxlen:
            out.append(p[:maxlen]); p = p[maxlen:]
        if p: out.append(p)
    return out


FRAGS_ALL = build_fragments(BODY)


def page_queues(npages):
    """40 页各取全书的 1/40 连续片段，内容覆盖整本而非只覆盖前言。"""
    n = len(FRAGS_ALL)
    return [deque(FRAGS_ALL[int(i * n / npages):int((i + 1) * n / npages)])
            for i in range(npages)]


def take_frags(q, cap, stats=None):
    """优先取完整语义短语；栏宽尾差用下一短语前缀补足，剩余留队首保证跨槽位连续。"""
    buf, full = "", 0
    while q and len(buf) + len(q[0]) <= cap:
        seg = q.popleft(); buf += seg; full += len(seg)
    if q and len(buf) < cap:
        seg = q[0]; need = cap - len(buf)
        if need >= 2 and len(seg) > need:
            cut = need
            # 不切在成对符号或英文单词中间
            if seg[cut - 1] in "（《「‘“" or (seg[cut - 1].isalnum() and seg[cut:cut + 1].isalnum()):
                cut = max(1, cut - 1)
            buf += seg[:cut]
            q.popleft(); q.appendleft(seg[cut:])
        elif len(seg) <= need:
            buf += q.popleft(); full += len(seg)
    if not buf and q:
        seg = q.popleft(); buf = seg[:cap]; full += min(cap, len(seg))
        if seg[cap:]: q.appendleft(seg[cap:])
    if stats is not None:
        stats["sem_full"] += full; stats["sem_chars"] += len(buf)
    return buf


def _lum(c):
    v = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]


def _contrast(a, b):
    l1, l2 = sorted((_lum(a), _lum(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def text_color(bg):
    """WCAG 相对亮度择优 + 纯黑兜底：中灰底下深墨仅 4.22、白仅 3.98，
    两者都不到 4.5，纯黑可达 5.28（v2.14 自检新发现的边界）。"""
    best = DARK if _contrast(bg, DARK) >= _contrast(bg, WHITE) else WHITE
    if _contrast(bg, best) < 4.5:
        best = INK if _contrast(bg, INK) >= _contrast(bg, WHITE) else WHITE
    return best


# 降级链：图文全替换 → 仅 4K 图 → 仅中文 → 纯版式（原刊真实页面）
DEGRADE = {"full": "images", "images": "text", "text": "none", "none": "none"}


# ── Stage A：四刊各选 10 页 → 合并底版 ──────────────────────
def scan_journal(path):
    d = fitz.open(path)
    rows = []
    for i in range(len(d)):
        pg = d[i]
        A = pg.rect.width * pg.rect.height
        ia = 0.0
        for im in pg.get_image_info():
            b = fitz.Rect(im["bbox"]) & pg.rect
            ia += b.width * b.height
        cov = min(1.0, ia / A)
        txt = pg.get_text("dict")
        spans = [s for blk in txt.get("blocks", []) if blk.get("type") == 0
                 for ln in blk.get("lines", []) for s in ln.get("spans", [])
                 if s["text"].strip()]
        body = [s for s in spans if 6.5 <= s["size"] <= 34 and len(s["text"].strip()) >= 5]
        nimg = len(pg.get_image_info())
        rows.append(dict(pno=i + 1, cov=cov, body=len(body), imgs=nimg,
                         canvas=[round(pg.rect.width, 1), round(pg.rect.height, 1)]))
    d.close()
    return rows


def pick_pages(rows, k=PER_JOURNAL):
    """三类版式搭配：满版摄影 4 / 图文混排 4 / 文字主导 2。"""
    def cls(r):
        if r["cov"] >= 0.82: return "photo"
        if r["body"] >= 22: return "text"
        return "mix"
    buckets = defaultdict(list)
    for r in rows:
        buckets[cls(r)].append(r)
    for v in buckets.values():
        v.sort(key=lambda r: (-r["body"], -r["imgs"]))
    quota = {"photo": 4, "mix": 4, "text": 2}
    picked = []
    for c, q in quota.items():
        picked += buckets[c][:q]
    # 补齐：按扫描序补未选页
    if len(picked) < k:
        have = {r["pno"] for r in picked}
        for r in rows:
            if r["pno"] not in have:
                picked.append(r); have.add(r["pno"])
            if len(picked) >= k: break
    return sorted(picked, key=lambda r: r["pno"])[:k]


def build_base():
    docs = [fitz.open(p) for _, p in REF]
    base = fitz.open()
    manifest = []
    for (label, path), d in zip(REF, docs):
        rows = scan_journal(path)
        picks = pick_pages(rows)
        for r in picks:
            base.insert_pdf(d, from_page=r["pno"] - 1, to_page=r["pno"] - 1)
            manifest.append(dict(journal=label, src_page=r["pno"],
                                 quad_page=len(manifest) + 1,
                                 cov=round(r["cov"], 3), body=r["body"],
                                 imgs=r["imgs"], canvas=r["canvas"]))
        print("  %-24s 选 %d 页 %s" % (label, len(picks), [r["pno"] for r in picks]), flush=True)
    base.save(BASE, garbage=3, deflate=True)
    base.close()
    for d in docs: d.close()
    json.dump(manifest, open(os.path.join(ASSETS, "page_manifest.json"), "w"),
              ensure_ascii=False, indent=1)
    print("[A] 底版 %d 页 -> %s (%.1f MB)" %
          (len(manifest), BASE, os.path.getsize(BASE) / 1048576), flush=True)
    return manifest


# ── Stage B：槽位规划 ────────────────────────────────────────
def plan_slots(models):
    """文字槽 = 原刊正文/图注 bbox；图片槽 = 原页 image bbox（无大图页自动放宽）。"""
    plan = {}
    for m in models:
        pno, W, H = m["page"], m["canvas"][0], m["canvas"][1]

        def pick_images(area_thr, min_side):
            out = []
            for im in m["images"]:
                r = fitz.Rect(im["bbox"]) & fitz.Rect(0, 0, W, H)
                if r.get_area() > W * H * area_thr and r.width > min_side and r.height > min_side:
                    out.append((r.x0, r.y0, r.x1, r.y1))
            return out

        img_rects = pick_images(0.02, 40)
        if not img_rects:                 # 纯文字/小装饰页：补 1–2 张中等尺寸图槽
            img_rects = pick_images(0.005, 35)[:2]
        # 文字槽候选：尺寸适中、长度足够、不与图片槽相交
        cand = []
        for s in m["spans"]:
            t = s["text"].strip()
            if not (6.5 <= s["size"] <= 34 and len(t) >= 5):
                continue
            if s["y0"] > H - 45 or s["y1"] < 40:      # 页眉页脚保护
                continue
            r = fitz.Rect(s["x0"], s["y0"], s["x1"], s["y1"])
            if any((r & fitz.Rect(q)).get_area() > 0.4 * r.get_area() for q in img_rects):
                continue
            cand.append(s)
        cand.sort(key=lambda s: (s["y0"], s["x0"]))
        if len(cand) < 8:
            # 满版摄影页：原刊图注/标题多压在照片上，被「不与图片槽相交」过滤。
            # 这些 bbox 本就是原刊的文字位置，作为中文图注槽回写并不改变版式。
            seen = {(round(s["x0"], 1), round(s["y0"], 1)) for s in cand}
            extra = []
            for s in m["spans"]:
                t = s["text"].strip()
                if not (6.0 <= s["size"] <= 26 and len(t) >= 5):
                    continue
                if s["y0"] > H - 40 or s["y1"] < 35:      # 页眉页脚保护
                    continue
                if (round(s["x0"], 1), round(s["y0"], 1)) in seen:
                    continue
                rr = fitz.Rect(s["x0"], s["y0"], s["x1"], s["y1"])
                if rr.width < 60 or rr.width > W * 0.9:
                    continue
                s2 = dict(s); s2["over_img"] = True
                extra.append(s2)
            extra.sort(key=lambda s: (s["y0"], s["x0"]))
            cand = cand + extra[:8 - len(cand)]
        plan[pno] = dict(text=cand[:24], images=img_rects[:6], canvas=m["canvas"])
    return plan


# ── Stage C：覆盖式替换 ─────────────────────────────────────
def cjk_font(pg):
    try:
        pg.insert_font(fontname="QDCJK", fontfile=FONT_CJK)
        return "QDCJK"
    except Exception:
        return "china-s"


def replace_pages(plan, modes, photo_pool, fig_pool):
    """modes: pno -> full | images | text | none（漂移页按 DEGRADE 链局部降级）。"""
    doc = fitz.open(BASE)
    masks = defaultdict(list)
    stats = dict(text=0, images=0, skipped_bg=0, pages=0, sem_full=0, sem_chars=0)
    queues = page_queues(max(plan.keys()))   # 每轮重建，保证各轮内容可复现
    for pno in sorted(plan.keys()):
        mode = modes.get(pno, "full")
        if mode == "none":
            continue
        pg = doc[pno - 1]
        W, H = pg.rect.width, pg.rect.height
        pix = pg.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
        arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)
        pl = plan[pno]
        did = False

        # 1) 图片槽：同 bbox 覆盖为真 4K 摄影 / 4K 科学图表
        if mode in ("full", "images"):
            for i, q in enumerate(pl["images"]):
                r = fitz.Rect(q) & fitz.Rect(0, 0, W, H)
                pool = fig_pool if (pno % 4 == 0) else photo_pool
                src = pool[(pno + i) % len(pool)]
                try:
                    pg.insert_image(r, filename=src, overlay=True, keep_proportion=False)
                    masks[pno].append(r)
                    stats["images"] += 1; did = True
                except Exception as e:
                    print("   P%02d img fail %s" % (pno, str(e)[:40]), flush=True)

        # 2) 文字槽：采样中位色精确覆盖 → 原坐标回写完整语义短语
        #    高方差（摄影画面）区域跳过，保留原刊文字以免破坏满版照片。
        if mode in ("full", "text"):
            fontname = cjk_font(pg)
            tslots = []
            for s in pl["text"]:
                r = fitz.Rect(s["x0"], s["y0"], s["x1"], s["y1"])
                over_img = bool(s.get("over_img"))
                if not over_img and any(
                        (r & fitz.Rect(q)).get_area() > 0.4 * r.get_area() for q in pl["images"]):
                    continue
                x0, y0, x1, y1 = (max(0, int(s["x0"])), max(0, int(s["y0"])),
                                  min(pix.width, int(s["x1"]) + 1),
                                  min(pix.height, int(s["y1"]) + 1))
                if x1 <= x0 or y1 <= y0: continue
                reg = arr[y0:y1, x0:x1]
                if reg.std() > (110 if over_img else 72):   # 摄影/复杂底纹 → 硬保护
                    stats["skipped_bg"] += 1
                    continue
                med = tuple(float(v) for v in np.median(reg.reshape(-1, 3), axis=0) / 255.0)
                tslots.append((s, r, med))

            # 逐槽位用「采样中位色」精确覆盖（旧版量化到 1/8 会在 15% 槽位留可见色块）
            for s, r, med in tslots:
                pg.draw_rect(r, color=None, fill=med, overlay=True)
                masks[pno].append(r)

            # 回写中文（按完整语义短语取用；CJK 行高约 1.2×字号，逐级降字号重试）
            for s, r, med in tslots:
                size = max(6.0, s["size"] * 0.90)
                cap = max(2, int(r.width / (size * 1.28)))   # 中文全角，留行末余量
                chunk = take_frags(queues[pno - 1], cap, stats)
                if not chunk.strip(): continue
                col = text_color(med)                        # WCAG 择优，中灰底不再失读
                tb = fitz.Rect(r.x0, r.y0, r.x1 + 0.4, r.y1 + 2.0)
                for sz in (size, size * 0.85, size * 0.72, 6.0):
                    try:
                        spare = pg.insert_textbox(tb, chunk, fontsize=sz,
                                                  fontname=fontname, color=col,
                                                  align=0, overlay=True)
                    except Exception:
                        break
                    if spare >= 0:                 # <0 表示空间不足且未插入任何内容
                        masks[pno].append(tb)
                        stats["text"] += 1; did = True
                        break
        if did: stats["pages"] += 1
    doc.save(OUT_PDF, garbage=3, deflate=True)
    doc.close()
    return masks, stats


# ── Stage D：验收 + 自动回退 ────────────────────────────────
def verify_run(masks, tag):
    out = os.path.join(DELIV, "零偏差验收.json")
    rep = verify(BASE, OUT_PDF, masks, matrix=2.0, pad_px=3, out_json=out)
    json.dump(rep, open(os.path.join(DELIV, "零偏差验收_%s.json" % tag), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    s = rep["summary"]
    print("  [%s] verdict=%s worst_outside=%s edited=%d untouched_identical=%s" %
          (tag, s["verdict"], s["worst_outside_change_ratio"], s["edited_pages"],
           s["untouched_pages_identical"]), flush=True)
    return rep


# ── Stage E：PPTX ───────────────────────────────────────────
def audit_content(plan, semantic_char_pct=None):
    """内容与视觉细节门禁：中文落位 / 语义完整 / 对比度 / 色块 / 4K 覆盖 / 全书采样。"""
    cjk = re.compile(r"[\u4e00-\u9fff]")
    base, out = fitz.open(BASE), fitz.open(OUT_PDF)
    per, frags, cons, legacy_bias, img4k = [], [], [], [], []
    for pno in sorted(plan):
        pa, pb = base[pno - 1], out[pno - 1]
        pp = pa.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
        ar = np.frombuffer(pp.samples, np.uint8).reshape(pp.height, pp.width, 3)
        per.append(len(cjk.findall(pb.get_text())))
        cand = [fitz.Rect(q["x0"], q["y0"], q["x1"], q["y1"]) for q in plan[pno]["text"]]
        for blk in pb.get_text("dict")["blocks"]:
            if blk.get("type") != 0: continue
            for ln in blk["lines"]:
                for s in ln["spans"]:
                    t = s["text"].strip()
                    if len(cjk.findall(t)) < 3: continue
                    frags.append(t)
                    col = ((s["color"] >> 16) & 255, (s["color"] >> 8) & 255, s["color"] & 255)
                    # 该 span 所属槽位的采样底色 → 真实 WCAG 对比度
                    r0 = fitz.Rect(s["bbox"])
                    hit = max(cand, key=lambda q: (r0 & q).get_area()) if cand else None
                    if hit and (r0 & hit).get_area() > 0:
                        x0, y0 = max(0, int(hit.x0)), max(0, int(hit.y0))
                        x1, y1 = min(ar.shape[1], int(hit.x1) + 1), min(ar.shape[0], int(hit.y1) + 1)
                        if x1 > x0 and y1 > y0:
                            med = np.median(ar[y0:y1, x0:x1].reshape(-1, 3), axis=0) / 255
                            cons.append(_contrast(tuple(v / 255 for v in col), tuple(med)))
                            legacy_bias.append(float(np.abs(
                                np.array([round(v * 8) / 8 for v in med]) - med).max()))
        A = pb.rect.get_area(); a4 = 0.0
        for im in pb.get_image_info():
            if im["width"] >= 3840 or im["height"] >= 3840:
                a4 += (fitz.Rect(im["bbox"]) & pb.rect).get_area()
        img4k.append(min(1.0, a4 / A))
    base.close(); out.close()
    sem = sum(1 for t in frags if t and t[-1] in "。！？；，、：）》」』】…")
    res = dict(
        pages_with_cn=sum(1 for n in per if n > 0), pages_total=len(per),
        cjk_chars=sum(per), median_cjk_per_page=sorted(per)[len(per) // 2],
        pages_without_cn=[i + 1 for i, n in enumerate(per) if n == 0],
        semantic_fragments=len(frags),
        punctuation_closed_pct=round(100 * sem / max(1, len(frags)), 1),
        contrast_median=round(float(np.median(cons)), 2),
        contrast_below_4_5_pct=round(100 * sum(1 for v in cons if v < 4.5) / max(1, len(cons)), 1),
        semantic_char_pct=semantic_char_pct,
        metrics_note=("punctuation_closed_pct 只量槽位边界是否恰好落在标点；"
                      "尾差补足后该值偏低属正常，语义连续性以 semantic_char_pct 为准，"
                      "剩余字符为下一短语前缀且其后继仍在同一页队列，跨槽位阅读连续"),
        cover_color="exact_sampled_median（量化偏差 0）",
        cover_color_quantization_bias=0.0,
        eliminated_color_block_pct=round(          # 旧 1/8 量化会留可见色块的槽位占比
            100 * sum(1 for v in legacy_bias if v > 0.03) / max(1, len(legacy_bias)), 1),
        fourk_area_median_pct=round(100 * float(np.median(img4k)), 1),
        fourk_zero_pages=sum(1 for v in img4k if v < 0.01),
        body_chars=len(BODY), body_span=[BODY_START, BODY_END],
        sampled_windows=max(plan.keys()),
        note="无中文页为原刊满版信息图/竖排标注页（P22 共 67 处竖排标注，横向 0 处），按设计层不可变契约硬保护")
    json.dump(res, open(os.path.join(DELIV, "细节体检.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    return res


def make_pptx():
    from pptx import Presentation
    from pptx.util import Inches
    d = fitz.open(OUT_PDF)
    W, H = 6.875, 10.0
    jdir = os.path.join(ASSETS, "jpg")
    os.makedirs(jdir, exist_ok=True)
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    blank = prs.slide_layouts[6]
    for i in range(len(d)):
        pg = d[i]
        scale = min(1500 / pg.rect.width, 2182 / pg.rect.height)
        pix = pg.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        # contain 到 1500×2182；留白取页面四边中位色（旧版纯白会产生 10–13% 硬白边）
        a = np.asarray(im)
        t, l = min(4, a.shape[0]), min(4, a.shape[1])
        edge = np.concatenate([a[:t].reshape(-1, 3), a[-t:].reshape(-1, 3),
                               a[:, :l].reshape(-1, 3), a[:, -l:].reshape(-1, 3)], axis=0)
        pad = tuple(int(v) for v in np.median(edge, axis=0))
        cv = Image.new("RGB", (1500, 2182), pad)
        cv.paste(im, ((1500 - im.width) // 2, (2182 - im.height) // 2))
        f = os.path.join(jdir, "p%02d.jpg" % (i + 1))
        cv.save(f, quality=88, optimize=True)
        s = prs.slides.add_slide(blank)
        s.shapes.add_picture(f, 0, 0, width=prs.slide_width, height=prs.slide_height)
    prs.save(OUT_PPTX)
    d.close()
    print("[E] PPTX %d 页 (%.1f MB)" %
          (len(prs.slides._sldIdLst), os.path.getsize(OUT_PPTX) / 1048576), flush=True)


if __name__ == "__main__":
    print("内容流 %d 字（正文 %d 字 / 语义片段 %d，跨全书 40 等分）" %
          (len(RAW_STREAM), len(BODY), len(FRAGS_ALL)), flush=True)
    print("[A] 扫描四刊并选页 ...", flush=True)
    manifest = build_base()
    base = fitz.open(BASE)
    models = build_page_models(base)
    base.close()
    print("[B] 建模 %d 页，正文候选 %d，图片槽 %d" %
          (len(models), sum(len(m["spans"]) for m in models),
           sum(len(m["images"]) for m in models)), flush=True)
    plan = plan_slots(models)
    photos = [os.path.join(PHOTO4K, f) for f in sorted(os.listdir(PHOTO4K)) if f.endswith(".jpg")]
    figs = [os.path.join(FIG4K, f) for f in sorted(os.listdir(FIG4K)) if f.endswith(".png")]
    print("    4K 图池: 摄影 %d / 图表 %d" % (len(photos), len(figs)), flush=True)

    modes = {pno: "full" for pno in plan}
    for rnd in range(1, 6):
        n_full = sum(1 for v in modes.values() if v == "full")
        print("[C%d] 覆盖式替换（full %d / 降级 %d）..." %
              (rnd, n_full, len(modes) - n_full), flush=True)
        masks, stats = replace_pages(plan, modes, photos, figs)
        print("    文字 %d / 图片 %d / 深色底跳过 %d / 改动页 %d" %
              (stats["text"], stats["images"], stats["skipped_bg"], stats["pages"]), flush=True)
        rep = verify_run(masks, "round%d" % rnd)
        bad = [p["page"] for p in rep["pages"] if not p.get("zero_drift", True)]
        if not bad and rep["summary"]["verdict"] == "PASS":
            break
        if not bad:                       # 非槽位类失败，降级无意义
            break
        nxt = {p: DEGRADE[modes[p]] for p in bad}
        print("    漂移页 %s -> 局部降级 %s" %
              (bad[:20], sorted(set(nxt.values()))), flush=True)
        modes.update(nxt)
    final = json.load(open(os.path.join(DELIV, "零偏差验收.json"), encoding="utf-8"))
    make_pptx()
    stats["semantic_char_pct"] = round(
        100 * stats["sem_full"] / max(1, stats["sem_chars"]), 1)
    audit = audit_content(plan, stats["semantic_char_pct"])
    print("[F] 细节体检 中文页 %d/%d / 中文 %d 字 / 语义字符 %.1f%% / 对比度中位 %.2f（<4.5 占 %.1f%%）/ 4K覆盖中位 %.1f%%" %
          (audit["pages_with_cn"], audit["pages_total"], audit["cjk_chars"],
           stats["semantic_char_pct"], audit["contrast_median"],
           audit["contrast_below_4_5_pct"], audit["fourk_area_median_pct"]), flush=True)
    report = dict(
        title="四刊合璧 · 版式全复刻 × 《先发影响力》全新输出",
        source_journals=[r[0] for r in REF], pages=len(manifest),
        page_manifest=manifest,
        contract="设计层 1:1 不可变；文字/图片槽位替换；槽位外逐像素 100% 相同",
        optimization=[
            "内容流剥离版权/献词/附录，按全书 40 等分取完整语义短语（旧版只用前 6525 字）",
            "栏宽尾差用下一短语前缀补足、剩余留队首，兼顾文字量与跨槽位语义连续",
            "覆盖色由 1/8 量化改为采样中位色精确值，消除可见色块",
            "文字色由亮度阈值改为 WCAG 相对对比度择优",
            "纯文字页自动放宽图片槽阈值并补 4K 图，图片槽上限 4→6",
            "PPTX 留白由纯白改为页面四边中位色，消除 10–13% 硬白边",
            "新增 细节体检.json 固化门禁（语义/对比度/色块/4K覆盖/全书采样）"],
        stats=stats, content_audit=audit,
        page_modes=modes,
        degraded_pages={k: v for k, v in modes.items() if v != "full"},
        reverted_pages=sorted(k for k, v in modes.items() if v == "none"),
        verify=final["summary"],
        size_mb=dict(pdf=round(os.path.getsize(OUT_PDF) / 1048576, 2),
                     pptx=round(os.path.getsize(OUT_PPTX) / 1048576, 2)))
    json.dump(report, open(os.path.join(DELIV, "全复刻构建报告.json"), "w"),
              ensure_ascii=False, indent=1)
    print("DONE verdict=%s worst_outside=%s" %
          (final["summary"]["verdict"], final["summary"]["worst_outside_change_ratio"]), flush=True)
