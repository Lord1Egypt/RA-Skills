#!/usr/bin/env python3
"""Functional checks using a synthetic curved table; contains no production data."""
import argparse
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.dont_write_bytecode = True
from video_table import save_json


def fixture(root):
    colors = [(228, 240, 255), (255, 237, 216), (222, 249, 229), (244, 225, 252)]
    width, height = 1200, 570
    flat = Image.new("RGB", (width, 330), "white")
    draw = ImageDraw.Draw(flat)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 28)
    except OSError:
        font = ImageFont.load_default(size=28)
    for i, color in enumerate(colors):
        y = 20 + i * 70
        draw.rectangle((20, y, 1180, y + 70), fill=color)
        draw.text((55, y + 22), f"ROW {i+1:02d}", font=font, fill="black")
        draw.text((465, y + 22), f"EVENT {i+1:02d} / VALUE {17+i}", font=font, fill="black")
        draw.line((20, y, 1180, y), fill="black", width=2)
    draw.line((20, 300, 1180, 300), fill="black", width=2)
    draw.line((430, 20, 430, 300), fill="black", width=2)
    anchors = np.array([0, 300, 600, 900, 1199], dtype=float)
    shifts = np.array([30, 88, 82, 135, 180], dtype=float)
    x = np.arange(width)
    shift = np.interp(x, anchors, shifts)
    scale = 1 + 0.12 * x / (width-1)
    yy, xx = np.indices((height, width))
    canonical_y = np.rint((yy - shift[None, :]) / scale[None, :]).astype(int)
    valid = (canonical_y >= 0) & (canonical_y < flat.height)
    array = np.full((height, width, 3), 245, dtype=np.uint8)
    array[valid] = np.asarray(flat)[canonical_y[valid], xx[valid]]
    Image.fromarray(array).save(root / "synthetic.png")
    boundaries = []
    for i in range(5):
        y = 20 + 70 * i
        boundaries.append({"id": f"b{i}", "points": [[float(a), float(s+y*(1+0.12*a/(width-1)))] for a, s in zip(anchors, shifts)]})
    grid = {"image_size": [width, height], "frame_id": "synthetic", "source_video": "synthetic-example", "time_seconds": 0, "x_range": [20, 1180], "boundaries": boundaries, "columns": [{"name": "row", "left": [[0,25],[1,25]], "right": [[0,425],[1,425]], "psm": 7}, {"name": "message", "left": [[0,435],[1,435]], "right": [[0,1175],[1,1175]], "psm": 7}], "rows": [{"id": f"R{i+1:03d}", "top": f"b{i}", "bottom": f"b{i+1}"} for i in range(4)]}
    save_json(root / "grid.json", grid)
    return colors, grid


def check(root):
    script = Path(__file__).with_name("video_table.py")
    colors, grid = fixture(root)

    def call(*args, expected=0):
        result = subprocess.run([sys.executable, str(script), *map(str, args)], capture_output=True, text=True)
        if result.returncode != expected:
            raise AssertionError(f"{args}: expected {expected}, got {result.returncode}\n{result.stdout}\n{result.stderr}")
        return result

    out = root / "extracted"
    call("split", "--image", root / "synthetic.png", "--grid", root / "grid.json", "--out", out, "--inset", 4)
    for i, color in enumerate(colors, 1):
        cell = np.asarray(Image.open(out / "cells" / f"R{i:03d}__row.png"))
        # A background strip is blank in every row, so it detects mixing adjacent colored rows.
        assert np.max(np.abs(cell[3:-3, 5:12].astype(float) - color)) < 3
    call("audit", "--manifest", out / "manifest.json", "--ledger", out / "ledger.json", expected=2)
    checked = json.loads((out / "ledger.json").read_text())
    for i, row in enumerate(checked["rows"], 1):
        for key, field in row["fields"].items():
            field.update(text=f"ROW {i:02d}" if key == "row" else f"EVENT {i:02d} / VALUE {16+i}", status="verified", reviewer="synthetic fixture oracle")
    save_json(out / "checked.json", checked)
    call("audit", "--manifest", out / "manifest.json", "--ledger", out / "checked.json")
    swapped = copy.deepcopy(checked)
    swapped["rows"][0], swapped["rows"][1] = swapped["rows"][1], swapped["rows"][0]
    save_json(out / "swapped.json", swapped)
    call("audit", "--manifest", out / "manifest.json", "--ledger", out / "swapped.json", expected=1)
    broken = copy.deepcopy(grid)
    broken["boundaries"][1]["points"] = broken["boundaries"][0]["points"]
    save_json(root / "crossed.json", broken)
    call("split", "--image", root / "synthetic.png", "--grid", root / "crossed.json", "--out", root / "rejected", expected=1)
    if shutil.which("tesseract"):
        call("ocr", "--manifest", out / "manifest.json", "--lang", "unavailable_test_language", "--out", out / "missing.json", expected=1)
        langs = subprocess.run(["tesseract", "--list-langs"], capture_output=True, text=True, check=True).stdout.splitlines()[1:]
        if "eng" in langs:
            call("ocr", "--manifest", out / "manifest.json", "--lang", "eng", "--out", out / "ocr.json")
            draft = json.loads((out / "ocr.json").read_text())
            for i, row in enumerate(draft["rows"], 1):
                assert row["fields"]["row"]["ocr_text"] == f"ROW {i:02d}"
                assert all(f["status"] == "unreviewed" and f["text"] is None for f in row["fields"].values())
    target = out / "cells" / "R001__row.png"
    target.write_bytes(target.read_bytes() + b"changed")
    call("audit", "--manifest", out / "manifest.json", "--ledger", out / "checked.json", expected=1)
    print("PASS: curved row isolation, OCR draft state, order guard, boundary rejection, missing-language rejection, evidence tamper detection")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", help="Optional NEW directory to retain synthetic test files")
    args = parser.parse_args()
    if args.out:
        root = Path(args.out).resolve()
        root.mkdir(parents=True, exist_ok=False)
        check(root)
    else:
        with tempfile.TemporaryDirectory(prefix="video-table-selftest-") as temp:
            check(Path(temp))


if __name__ == "__main__":
    main()
