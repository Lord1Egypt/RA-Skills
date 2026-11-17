#!/usr/bin/env python3
"""Evidence-preserving, manually anchored video-table extraction. No network calls."""
import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(args):
    return subprocess.run([str(x) for x in args], check=True, capture_output=True, text=True)


def new_dir(path):
    p = Path(path).resolve()
    if p.exists() and (not p.is_dir() or any(p.iterdir())):
        raise ValueError(f"Output must be a new or empty directory: {p}")
    p.mkdir(parents=True, exist_ok=True)
    return p


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", value):
        raise ValueError(f"Invalid file-safe identifier: {value!r}")
    return value


def doctor(_):
    data = {"python": sys.executable, "numpy": np.__version__}
    for executable in ("ffmpeg", "ffprobe", "tesseract"):
        data[executable] = shutil.which(executable)
    if data["tesseract"]:
        data["ocr_languages"] = run(["tesseract", "--list-langs"]).stdout.splitlines()[1:]
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


def frames(args):
    src = Path(args.video).resolve(strict=True)
    times = [float(t.strip()) for t in args.times.split(",")]
    if not 1 <= len(times) <= 200 or any(not math.isfinite(t) or t < 0 for t in times):
        raise ValueError("Provide 1..200 finite nonnegative times in seconds")
    if len(set(times)) != len(times):
        raise ValueError("Duplicate requested times")
    probe = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_streams", "-show_format", "-of", "json", src]).stdout)
    if not probe.get("streams"):
        raise ValueError("No video stream")
    duration = probe.get("format", {}).get("duration")
    if duration is not None and any(t >= float(duration) for t in times):
        raise ValueError("A requested time is at or beyond the video duration")
    out = new_dir(args.out)
    data = {"video": str(src), "sha256": sha256(src), "probe": probe, "frames": []}
    for i, seconds in enumerate(times, 1):
        dest = out / f"frame_{i:04d}.png"
        result = run(["ffmpeg", "-hide_banner", "-loglevel", "info", "-i", src, "-map", "0:v:0", "-vf", f"select=gte(t\\,{seconds:.9f}),showinfo", "-frames:v", "1", "-fps_mode", "vfr", "-n", dest])
        match = re.search(r"\bn:\s*0\s+pts:.*?pts_time:([\d.eE+-]+)", result.stderr)
        if not dest.exists() or not match:
            raise ValueError(f"No verifiable frame produced at {seconds}")
        with Image.open(dest) as im:
            dimensions = list(im.size)
        data["frames"].append({"file": dest.name, "requested_seconds": seconds, "pts_seconds": float(match.group(1)), "image_size": dimensions, "sha256": sha256(dest)})
        save_json(out / "frames.json", data)
    print(f"Extracted {len(data['frames'])} frames: {out / 'frames.json'}")
    return 0


def points(value, low, high, label):
    p = np.asarray(value, dtype=float)
    if p.ndim != 2 or p.shape[1] != 2 or len(p) < 2 or not np.isfinite(p).all():
        raise ValueError(f"{label}: expected at least two finite coordinate pairs")
    if not (np.diff(p[:, 0]) > 0).all() or p[0, 0] > low or p[-1, 0] < high:
        raise ValueError(f"{label}: points must increase and cover [{low}, {high}]")
    return p


def interp(p, x):
    return np.interp(x, p[:, 0], p[:, 1])


def sample(array, x, y):
    h, w = array.shape[:2]
    if x.min() < 0 or y.min() < 0 or x.max() > w - 1 or y.max() > h - 1:
        raise ValueError("Crop extends outside frame; use another frame or explicitly record clipping")
    x0 = np.floor(x).astype(int)
    y0 = np.floor(y).astype(int)
    x1, y1 = np.minimum(x0 + 1, w - 1), np.minimum(y0 + 1, h - 1)
    dx, dy = (x - x0)[..., None], (y - y0)[..., None]
    value = array[y0, x0] * (1-dx) * (1-dy) + array[y0, x1] * dx * (1-dy) + array[y1, x0] * (1-dx) * dy + array[y1, x1] * dx * dy
    return Image.fromarray(np.clip(np.rint(value), 0, 255).astype(np.uint8))


def warp(array, top, bottom, left, right, inset):
    v_check = np.unique(np.r_[np.linspace(0, 1, 100), left[:, 0], right[:, 0]])
    widths = interp(right, v_check) - interp(left, v_check)
    if widths.min() < 2:
        raise ValueError("Cell sides cross or cell is too narrow")
    x_min = min(left[:, 1].min(), right[:, 1].min())
    x_max = max(left[:, 1].max(), right[:, 1].max())
    if x_min < max(top[0, 0], bottom[0, 0]) or x_max > min(top[-1, 0], bottom[-1, 0]):
        raise ValueError("Cell extends beyond observed boundary anchors")
    x_check = np.unique(np.r_[np.linspace(x_min, x_max, 200), top[:, 0], bottom[:, 0]])
    x_check = x_check[(x_check >= x_min) & (x_check <= x_max)]
    heights = interp(bottom, x_check) - interp(top, x_check) - 2 * inset
    if heights.min() < 2:
        raise ValueError("Row borders cross, row is too short, or inset is too large")
    width, height = int(round(np.median(widths))) + 1, int(round(np.median(heights))) + 1
    if width * height > 50_000_000:
        raise ValueError("Crop exceeds 50 megapixels; inspect geometry")
    v, u = np.linspace(0, 1, height)[:, None], np.linspace(0, 1, width)[None, :]
    x = interp(left, v) + u * (interp(right, v) - interp(left, v))
    y_top, y_bottom = interp(top, x), interp(bottom, x)
    y = y_top + inset + v * (y_bottom - y_top - 2 * inset)
    return sample(array, x, y)


def split(args):
    src = Path(args.image).resolve(strict=True)
    grid = read_json(args.grid)
    im = Image.open(src).convert("RGB")
    if list(im.size) != grid["image_size"]:
        raise ValueError("Grid dimensions do not match source image")
    xlo, xhi = map(float, grid["x_range"])
    if not (math.isfinite(xlo) and math.isfinite(xhi) and 0 <= xlo < xhi <= im.width - 1):
        raise ValueError("Invalid x_range")
    if not math.isfinite(args.inset) or args.inset < 0:
        raise ValueError("Inset must be finite and nonnegative")
    boundaries = {}
    for item in grid["boundaries"]:
        key = identifier(item["id"])
        if key in boundaries:
            raise ValueError("Duplicate boundary ID")
        boundaries[key] = points(item["points"], xlo, xhi, key)
    if not grid.get("rows"):
        raise ValueError("No rows in grid")
    out = new_dir(args.out)
    (out / "rows").mkdir()
    (out / "cells").mkdir()
    overlay = im.copy()
    draw = ImageDraw.Draw(overlay)
    for key, p in boundaries.items():
        draw.line([tuple(z) for z in p], fill=(0, 210, 255), width=2)
        draw.text(tuple(p[0]), key, fill=(255, 40, 40))
    array = np.asarray(im, dtype=np.float32)
    manifest = {"schema": 1, "source_image": str(src), "source_sha256": sha256(src), "grid": grid, "inset": args.inset, "rows": []}
    ledger = {"schema": 1, "rows": []}
    seen = set()
    for spec in grid["rows"]:
        rid = identifier(spec["id"])
        if rid in seen:
            raise ValueError("Duplicate row ID")
        seen.add(rid)
        top, bottom = boundaries[spec["top"]], boundaries[spec["bottom"]]
        left, right = np.array([[0, xlo], [1, xlo]]), np.array([[0, xhi], [1, xhi]])
        row_path = out / "rows" / f"{rid}.png"
        warp(array, top, bottom, left, right, args.inset).save(row_path)
        record = {"id": rid, "top": spec["top"], "bottom": spec["bottom"], "file": str(row_path.relative_to(out)), "sha256": sha256(row_path), "cells": []}
        reviewed = {"id": rid, "fields": {}}
        columns = spec.get("columns", grid.get("columns", []))
        if not columns:
            raise ValueError(f"No columns for {rid}")
        for col in columns:
            name = identifier(col["name"])
            if name in reviewed["fields"]:
                raise ValueError("Duplicate field in row")
            sides = [points(col[side], 0, 1, f"{rid}/{name}/{side}") for side in ("left", "right")]
            for p in sides:
                if p[0, 0] != 0 or p[-1, 0] != 1 or p[:, 1].min() < xlo or p[:, 1].max() > xhi:
                    raise ValueError("Cell sides must span exactly v=0..1 and remain within x_range")
            psm = int(col.get("psm", 7))
            if psm not in (6, 7, 8, 10, 11, 13):
                raise ValueError("Unsupported PSM for a cell")
            dest = out / "cells" / f"{rid}__{name}.png"
            warp(array, top, bottom, *sides, args.inset).save(dest)
            record["cells"].append({"name": name, "file": str(dest.relative_to(out)), "sha256": sha256(dest), "psm": psm})
            reviewed["fields"][name] = {"ocr_text": None, "text": None, "status": "unreviewed", "reviewer": "", "note": ""}
            for p in sides:
                v = np.linspace(0, 1, 100)
                x = interp(p, v)
                y = interp(top, x) + v * (interp(bottom, x) - interp(top, x))
                draw.line(list(zip(x, y)), fill=(255, 210, 0), width=2)
        manifest["rows"].append(record)
        ledger["rows"].append(reviewed)
    overlay.save(out / "overlay.png")
    save_json(out / "manifest.json", manifest)
    save_json(out / "ledger.json", ledger)
    print(f"Extracted {len(seen)} rows; inspect {out / 'overlay.png'} before reading cells")
    return 0


def evidence(path):
    path = Path(path).resolve(strict=True)
    data = read_json(path)
    root = path.parent
    src = Path(data["source_image"])
    if not src.is_absolute():
        src = root / src
    if sha256(src) != data["source_sha256"]:
        raise ValueError("Source image hash mismatch")
    row_ids = []
    for row in data["rows"]:
        row_ids.append(identifier(row["id"]))
        fields = [identifier(c["name"]) for c in row["cells"]]
        if not fields or len(fields) != len(set(fields)):
            raise ValueError("Manifest has missing or duplicate fields")
        for item in [row] + row["cells"]:
            file_path = (root / item["file"]).resolve(strict=True)
            if not file_path.is_relative_to(root):
                raise ValueError("Evidence crop points outside its result directory")
            if sha256(file_path) != item["sha256"]:
                raise ValueError(f"Crop hash mismatch: {item['file']}")
    if not row_ids or len(row_ids) != len(set(row_ids)):
        raise ValueError("Manifest has missing or duplicate rows")
    return data, root


def ocr(args):
    data, root = evidence(args.manifest)
    if Path(args.out).exists():
        raise ValueError("OCR destination already exists")
    installed = set(run(["tesseract", "--list-langs"]).stdout.splitlines()[1:])
    requested = set(args.lang.split("+"))
    if not requested.issubset(installed):
        raise ValueError(f"Missing OCR languages: {sorted(requested - installed)}; use visual reading or an authorized local model")
    ledger = {"schema": 1, "ocr_language": args.lang, "rows": []}
    for row in data["rows"]:
        reviewed = {"id": row["id"], "fields": {}}
        for cell in row["cells"]:
            psm = int(cell["psm"])
            if psm not in (6, 7, 8, 10, 11, 13):
                raise ValueError("Unsupported PSM")
            tsv = run(["tesseract", root / cell["file"], "stdout", "-l", args.lang, "--psm", psm, "tsv"]).stdout
            words = [r for r in csv.DictReader(io.StringIO(tsv), delimiter="\t") if r.get("text", "").strip()]
            lines = []
            last_key = None
            for word in words:
                key = tuple(word[k] for k in ("page_num", "block_num", "par_num", "line_num"))
                if key != last_key:
                    lines.append([])
                    last_key = key
                lines[-1].append(word["text"])
            reviewed["fields"][cell["name"]] = {"ocr_text": "\n".join(" ".join(line) for line in lines), "ocr_words": words, "text": None, "status": "unreviewed", "reviewer": "", "note": ""}
        ledger["rows"].append(reviewed)
    save_json(args.out, ledger)
    print(f"OCR draft only: {args.out}; all fields remain unreviewed")
    return 0


def audit(args):
    data, _ = evidence(args.manifest)
    ledger = read_json(args.ledger)
    if [r["id"] for r in ledger["rows"]] != [r["id"] for r in data["rows"]]:
        raise ValueError("Ledger row IDs or order differ from manifest")
    counts = {s: 0 for s in ("unreviewed", "verified", "blank", "clipped", "unreadable")}
    for source, row in zip(data["rows"], ledger["rows"]):
        if set(row["fields"]) != {c["name"] for c in source["cells"]}:
            raise ValueError(f"Field set mismatch: {row['id']}")
        for name, field in row["fields"].items():
            status, value = field.get("status"), field.get("text")
            if status not in counts or (value is not None and not isinstance(value, str)):
                raise ValueError(f"Invalid status/text: {row['id']}/{name}")
            reviewer, note = field.get("reviewer"), field.get("note")
            if status != "unreviewed" and (not isinstance(reviewer, str) or not reviewer.strip()):
                raise ValueError("Reviewed fields require a reviewer")
            if status == "verified" and (not isinstance(value, str) or not value.strip()):
                raise ValueError("Verified fields require nonempty literal text")
            if status == "blank" and value != "":
                raise ValueError("Blank fields require the empty string")
            if status in ("clipped", "unreadable") and (not isinstance(note, str) or not note.strip()):
                raise ValueError("Clipped/unreadable fields require a note")
            counts[status] += 1
    print(json.dumps({"scope": "Structural evidence audit only; visual correctness is not proved", "rows": len(data["rows"]), "fields": counts}, ensure_ascii=False, indent=2))
    return 2 if any(counts[s] for s in ("unreviewed", "clipped", "unreadable")) else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor").set_defaults(func=doctor)
    p = commands.add_parser("frames")
    for option in ("video", "times", "out"):
        p.add_argument(f"--{option}", required=True)
    p.set_defaults(func=frames)
    p = commands.add_parser("split")
    for option in ("image", "grid", "out"):
        p.add_argument(f"--{option}", required=True)
    p.add_argument("--inset", type=float, default=2.0)
    p.set_defaults(func=split)
    p = commands.add_parser("ocr")
    for option in ("manifest", "out", "lang"):
        p.add_argument(f"--{option}", required=True)
    p.set_defaults(func=ocr)
    p = commands.add_parser("audit")
    for option in ("manifest", "ledger"):
        p.add_argument(f"--{option}", required=True)
    p.set_defaults(func=audit)
    args = parser.parse_args()
    try:
        return args.func(args)
    except (ValueError, KeyError, OSError, TypeError, subprocess.CalledProcessError) as exc:
        detail = exc.stderr[-2000:] if isinstance(exc, subprocess.CalledProcessError) else str(exc)
        print(f"ERROR: {detail}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
