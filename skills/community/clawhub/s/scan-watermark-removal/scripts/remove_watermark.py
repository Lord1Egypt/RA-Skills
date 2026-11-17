#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remove light translucent text watermarks from scanned pages — images or PDF.

Handles two watermark families:

  * diagonal translucent text (pink / purple), pixel-level colour-cone removal
  * printed header logos made of coloured text (e.g. a brand name), removed by
    a colour wedge + shape test inside the header band only

Usage:
    python remove_watermark.py <input>                # dir, image, or .pdf
    python remove_watermark.py <input> --output <out>
    python remove_watermark.py <input.pdf> --no-logo

Exit code 0 = every page passed; 1 = at least one page needs a human look.
Requires: numpy, pillow; pymupdf only for PDF input.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import wmcore
import wm_pdf

PDF_EXTS = (".pdf",)


def is_pdf(p):
    return p.lower().endswith(PDF_EXTS)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Remove light translucent watermarks from scanned pages")
    ap.add_argument("input", help="image file, image folder, or PDF")
    ap.add_argument("--output", default=None,
                    help="image mode: output folder; PDF mode: output .pdf")
    ap.add_argument("--near", type=int, default=5,
                    help="ink-protection window in px (default 5; smaller = "
                         "more aggressive, larger = more conservative)")
    ap.add_argument("--suffix", default="_去水印",
                    help="filename suffix for image mode")
    ap.add_argument("--all", action="store_true",
                    help="also reprocess files already carrying the suffix")
    ap.add_argument("--no-pink", action="store_true", help="disable pink cone")
    ap.add_argument("--no-purple", action="store_true", help="disable purple cone")
    ap.add_argument("--no-logo", action="store_true",
                    help="keep the printed header logo")
    ap.add_argument("--quiet", action="store_true", help="only print the summary")
    a = ap.parse_args(argv)

    src = os.path.abspath(a.input)
    if not os.path.exists(src):
        sys.exit(f"input not found: {src}")

    log = (lambda s: None) if a.quiet else (lambda s: print(s, flush=True))

    if is_pdf(src):
        if wm_pdf is None or wm_pdf.pymupdf is None:
            sys.exit("PDF input requires pymupdf: pip install pymupdf")
        out = a.output or (os.path.splitext(src)[0] + "_去水印.pdf")
        if os.path.isdir(out):
            out = os.path.join(
                out, os.path.splitext(os.path.basename(src))[0] + "_去水印.pdf")
        elif not out.lower().endswith(".pdf"):
            out += ".pdf"
        rows = wm_pdf.process_pdf(
            src, out, near=a.near,
            pink=not a.no_pink, purple=not a.no_purple,
            remove_logo=not a.no_logo,
            log=log,
            report=os.path.splitext(out)[0] + "_报告.txt")
        # 硬判据是"有没有误伤真内容"和"有没有看得见的残留"，
        # 不用百分比卡阈值——抗锯齿边缘在 JPEG 里挪几个单位就能让百分比掉几点，
        # 那些从来不是内容。
        bad = [r for r in rows
               if r[9] > 0 or r[8] > 20 or min(r[3], r[4], r[5]) < 90.0
               or r[6] == "失败"]
        print(f"\n{len(rows)} pages -> {out}")
        if bad:
            print(f"need a human look ({len(bad)} pages):")
            for r in bad:
                print("  page", r[0],
                      f"erased={r[9]} visible residue={r[8]}",
                      f"retention {r[3]:.1f}/{r[4]:.1f}/{r[5]:.1f}%", r[6])
            return 1
        print("ALL PASS: watermark and header logo cleared, content retained.")
        return 0

    out = a.output or os.path.join(
        src if os.path.isdir(src) else os.path.dirname(src), "去水印输出")
    extra = None if a.no_logo else wm_pdf.logo_only
    rows = wmcore.batch_process(
        src, out, near=a.near, suffix=a.suffix,
        skip_done=not a.all,
        pink=not a.no_pink, purple=not a.no_purple, extra=extra,
        log=log, report=os.path.join(out, "处理报告.txt"))
    # 同 PDF：误伤真内容为 0 是硬指标，保留率只做量级兜底
    bad = [r for r in rows
           if r[8] > 0 or r[7] > 20 or min(r[4], r[5], r[6]) < 90.0]
    print(f"\n{len(rows)} images -> {out}")
    if bad:
        print(f"need a human look ({len(bad)} files):")
        for r in bad:
            print("  ", r)
        return 1
    print("ALL PASS: content retained, watermark residue within limit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
