# -*- coding: utf-8 -*-
"""detail_audit.py — 完全复刻产物的「细节体检八门」（reading-notes-master v2.14）

零偏差验收（verify）只证明「槽位外像素没动」，证明不了「槽位内的内容好不好」。
本脚本补上内容层与视觉层的 8 道门禁，输出可归档 JSON：

  D1 槽位外零偏差   D2 中文真实落位   D3 语义完整性     D4 覆盖色偏差
  D5 WCAG 对比度    D6 中文溢出槽位   D7 4K 图面积      D8 全书内容覆盖

实测基线（四刊合璧 40 页，2026-11-10）：
  PASS / 0.0 · 39/40 页 5368 字 · 语义字符 77.7% · 覆盖色偏差中位 1/255
  · 对比度中位 16.79（<4.5 占 1.1%）· 溢出 0% · 4K 面积中位 63.4% · 40 窗口

用法：
  python3 detail_audit.py base.pdf out.pdf --json detail.json \
      --verify-report 零偏差验收.json --semantic-char-pct 77.7 \
      --body-chars 200476 --windows 40
  python3 detail_audit.py base.pdf out.pdf --slots plan.json --json detail.json

依赖：PyMuPDF(fitz) + numpy（系统 python，非 WorkBuddy 内置环境）。
退出码：0 = PASS/WARN，1 = FAIL，2 = 参数/依赖错误。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

try:
    import fitz
    import numpy as np
except ImportError as e:
    print("需要 PyMuPDF + numpy：%s" % e, file=sys.stderr)
    raise SystemExit(2)

__version__ = "2.14.0"
CJK = re.compile(r"[\u4e00-\u9fff]")
CLOSERS = "。！？；，、：）》」』】…"


def _lum(c):
    v = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]


def contrast(a, b):
    l1, l2 = sorted((_lum(a), _lum(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def pix_array(page, matrix=1.0):
    p = page.get_pixmap(matrix=fitz.Matrix(matrix, matrix), alpha=False)
    return np.frombuffer(p.samples, np.uint8).reshape(p.height, p.width, 3)


def auto_slots(page, maxn=24):
    """无 --slots 时从底版文字 span 自动推导候选槽位（体检基线用，非精确契约 mask）。"""
    out = []
    H = page.rect.height
    for blk in page.get_text("dict")["blocks"]:
        if blk.get("type") != 0:
            continue
        for ln in blk.get("lines", []):
            for s in ln.get("spans", []):
                t = s["text"].strip()
                if not (6.5 <= s["size"] <= 34 and len(t) >= 5):
                    continue
                if s["bbox"][1] > H - 45 or s["bbox"][3] < 40:
                    continue
                out.append(dict(x0=s["bbox"][0], y0=s["bbox"][1],
                                x1=s["bbox"][2], y1=s["bbox"][3]))
    out.sort(key=lambda r: (r["y0"], r["x0"]))
    return out[:maxn]


def load_slots(path, base):
    if path:
        raw = json.load(open(path, encoding="utf-8"))
        # 支持 {"1":[...]} 或 {"1":{"text":[...]}} 两种
        out = {}
        for k, v in raw.items():
            pno = int(k)
            items = v.get("text", []) if isinstance(v, dict) else v
            out[pno] = [dict(x0=q["x0"], y0=q["y0"], x1=q["x1"], y1=q["y1"])
                        for q in items if all(z in q for z in ("x0", "y0", "x1", "y1"))]
        return out
    return {i + 1: auto_slots(base[i]) for i in range(len(base))}


def gate(name, ok, detail, hard=True, status=None):
    st = status or ("PASS" if ok else ("FAIL" if hard else "WARN"))
    return dict(gate=name, status=st, detail=detail)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("base", help="1:1 底版 PDF")
    ap.add_argument("out", help="待检产物 PDF")
    ap.add_argument("--slots", help="槽位 JSON（不传则从底版 span 自动推导）")
    ap.add_argument("--verify-report", help="零偏差验收 JSON，直接采信其 summary 作为 D1")
    ap.add_argument("--semantic-char-pct", type=float, help="构建报告中的语义字符占比（D3）")
    ap.add_argument("--body-chars", type=int, help="正文总字数（D8 佐证）")
    ap.add_argument("--windows", type=int, help="全书采样窗口数（D8）")
    ap.add_argument("--json", help="输出体检 JSON")
    a = ap.parse_args()

    base, out = fitz.open(a.base), fitz.open(a.out)
    if len(base) != len(out):
        print("页数不一致 %d vs %d" % (len(base), len(out)), file=sys.stderr)
        raise SystemExit(2)
    slots = load_slots(a.slots, base)
    npages = len(out)

    per, frags, cons, bias, img4k = [], [], [], [], []
    overflow = 0
    ncn_span = 0
    for pno in range(1, npages + 1):
        pb, pa = out[pno - 1], base[pno - 1]
        per.append(len(CJK.findall(pb.get_text())))
        ar = pix_array(pa, 1.0)
        zr = pix_array(pb, 1.0)
        cand = [fitz.Rect(q["x0"], q["y0"], q["x1"], q["y1"]) for q in slots.get(pno, [])]

        for blk in pb.get_text("dict")["blocks"]:
            if blk.get("type") != 0:
                continue
            for ln in blk.get("lines", []):
                for s in ln.get("spans", []):
                    t = s["text"].strip()
                    if len(CJK.findall(t)) < 3:
                        continue
                    ncn_span += 1
                    frags.append(t)
                    r0 = fitz.Rect(s["bbox"])
                    hit = max(cand, key=lambda q: (r0 & q).get_area()) if cand else None
                    if hit and (r0 & hit).get_area() > 0:
                        col = ((s["color"] >> 16) & 255,
                               (s["color"] >> 8) & 255, s["color"] & 255)
                        x0, y0 = max(0, int(hit.x0)), max(0, int(hit.y0))
                        x1, y1 = min(ar.shape[1], int(hit.x1) + 1), min(ar.shape[0], int(hit.y1) + 1)
                        if x1 > x0 and y1 > y0:
                            med = np.median(ar[y0:y1, x0:x1].reshape(-1, 3), axis=0) / 255.0
                            cons.append(contrast(tuple(v / 255 for v in col), tuple(med)))
                    if not any((r0 & q).get_area() > 0.55 * r0.get_area() for q in cand):
                        overflow += 1

        # 覆盖色：OUT 槽位内众数色 vs BASE 同区域中位色
        for q in cand:
            x0, y0 = max(0, int(q.x0)), max(0, int(q.y0))
            x1, y1 = min(ar.shape[1], int(q.x1) + 1), min(ar.shape[0], int(q.y1) + 1)
            if x1 <= x0 or y1 <= y0:
                continue
            base_med = np.median(ar[y0:y1, x0:x1].reshape(-1, 3), axis=0)
            reg = zr[y0:y1, x0:x1].reshape(-1, 3)
            vals, cnt = np.unique((reg // 4 * 4), axis=0, return_counts=True)
            dom = vals[cnt.argmax()].astype(float) + 2
            bias.append(float(np.abs(dom - base_med).max()))

        A = pb.rect.get_area()
        a4 = sum((fitz.Rect(im["bbox"]) & pb.rect).get_area()
                 for im in pb.get_image_info()
                 if im["width"] >= 3840 or im["height"] >= 3840)
        img4k.append(min(1.0, a4 / A))

    base.close()
    out.close()

    # D1
    if a.verify_report and os.path.exists(a.verify_report):
        v = json.load(open(a.verify_report, encoding="utf-8"))["summary"]
        d1 = gate("D1 槽位外零偏差",
                  v.get("verdict") == "PASS" and v.get("worst_outside_change_ratio") == 0.0,
                  "verdict=%s worst_outside=%s edited=%s" %
                  (v.get("verdict"), v.get("worst_outside_change_ratio"), v.get("edited_pages")))
    else:
        d1 = gate("D1 槽位外零偏差", True,
                  "未提供 --verify-report，本脚本不重算；请另跑 exact_replication.verify()",
                  status="WARN")

    cn_pages = sum(1 for n in per if n > 0)
    d2 = gate("D2 中文真实落位", cn_pages >= 0.9 * npages,
              "%d/%d 页有中文 / %d 字 / 每页中位 %d" %
              (cn_pages, npages, sum(per), sorted(per)[npages // 2]))

    closed = sum(1 for t in frags if t and t[-1] in CLOSERS)
    closed_pct = round(100 * closed / max(1, len(frags)), 1)
    if a.semantic_char_pct is None:
        d3 = gate("D3 语义完整性", True,
                  "槽位以标点收尾 %.1f%%；未传 --semantic-char-pct，建议从构建报告注入" % closed_pct,
                  status="WARN")
    else:
        d3 = gate("D3 语义完整性", a.semantic_char_pct >= 70,
                  "semantic_char_pct=%.1f%% / 标点收尾 %.1f%%（后者受尾差补足影响，不作判据）" %
                  (a.semantic_char_pct, closed_pct))

    bmed = float(np.median(bias)) if bias else 0.0
    bp90 = float(np.percentile(bias, 90)) if bias else 0.0
    bbad = 100 * sum(1 for v in bias if v > 8) / max(1, len(bias))
    d4 = gate("D4 覆盖色偏差", bmed <= 4 and bbad <= 5,
              "中位 %.1f/255 / P90 %.1f / >8 的槽位 %.1f%%（%d 槽）" %
              (bmed, bp90, bbad, len(bias)))

    cmed = float(np.median(cons)) if cons else 0.0
    cbad = 100 * sum(1 for v in cons if v < 4.5) / max(1, len(cons))
    d5 = gate("D5 WCAG 对比度", cbad <= 5,
              "中位 %.2f / <4.5 占 %.1f%%（%d 段）" % (cmed, cbad, len(cons)))

    orate = 100 * overflow / max(1, ncn_span)
    d6 = gate("D6 中文溢出槽位", orate <= 1,
              "%d/%d 段溢出 = %.1f%%" % (overflow, ncn_span, orate))

    imed = 100 * float(np.median(img4k))
    d7 = gate("D7 4K 图面积", imed >= 50,
              "中位 %.1f%% / 零 4K 页 %d / 满幅(>60%%) 页 %d" %
              (imed, sum(1 for v in img4k if v < 0.01), sum(1 for v in img4k if v > 0.6)))

    if a.windows is None:
        d8 = gate("D8 全书内容覆盖", True,
                  "未传 --windows / --body-chars；建议从构建报告注入", status="WARN")
    else:
        d8 = gate("D8 全书内容覆盖", a.windows >= 0.8 * npages,
                  "%d 个采样窗口 / 正文 %s 字 / %d 页" %
                  (a.windows, a.body_chars or "N/A", npages))

    gates = [d1, d2, d3, d4, d5, d6, d7, d8]
    status = [g["status"] for g in gates]
    verdict = "FAIL" if "FAIL" in status else ("WARN" if "WARN" in status else "PASS")
    res = dict(version=__version__, base=a.base, out=a.out, pages=npages,
               verdict=verdict, gates=gates,
               metrics=dict(cn_pages=cn_pages, cjk_chars=sum(per),
                            punctuation_closed_pct=closed_pct,
                            semantic_char_pct=a.semantic_char_pct,
                            color_bias_median=round(bmed, 2), color_bias_p90=round(bp90, 2),
                            contrast_median=round(cmed, 2), contrast_below_4_5_pct=round(cbad, 2),
                            overflow_pct=round(orate, 2),
                            fourk_area_median_pct=round(imed, 1),
                            sampled_windows=a.windows),
               note="D1 精确零偏差由 exact_replication.verify() 负责；本脚本专注槽位内的内容与视觉质量")
    print(json.dumps(res, ensure_ascii=False, indent=2))
    if a.json:
        json.dump(res, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return 1 if verdict == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
