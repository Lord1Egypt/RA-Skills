# -*- coding: utf-8 -*-
"""Verify a signed PDF against its original: pages, body text, embedded images.

Usage:
  python verify_merge.py --original in.pdf --signed out.pdf
Stdout: JSON
"""
from __future__ import annotations

import sys
import os
import json
import argparse

sys.stdout.reconfigure(encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--original", required=True)
    ap.add_argument("--signed", required=True)
    args = ap.parse_args()

    import fitz

    a = fitz.open(args.original)
    b = fitz.open(args.signed)
    out = {
        "original": {"pages": a.page_count, "bytes": os.path.getsize(args.original)},
        "signed": {"pages": b.page_count, "bytes": os.path.getsize(args.signed)},
        "images_in_signed": [],
        "text_identical": None,
    }
    for i in range(b.page_count):
        for im in b[i].get_images(full=True):
            info = b.extract_image(im[0])
            out["images_in_signed"].append({
                "page": i + 1, "xref": im[0], "w": info["width"], "h": info["height"],
                "ext": info["ext"], "has_alpha": info.get("smask", 0) != 0})
    if a.page_count == b.page_count:
        out["text_identical"] = all(a[i].get_text("text") == b[i].get_text("text")
                                    for i in range(a.page_count))
    a.close(); b.close()
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
