#!/usr/bin/env python3
"""Decompile SWF games with FFDec/JPEXS into a porting workspace."""

from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable

WINDOWS_FFDEC = Path(r"C:\Program Files (x86)\FFDec\ffdec-cli.exe")

EXPORT_PASSES = [
    {
        "name": "actionscript",
        "out": Path("code/actionscript"),
        "pre": ["-format", "script:as", "-onerror", "ignore"],
        "cmd": ["-export", "script"],
    },
    {
        "name": "pcodehex",
        "out": Path("code/pcodehex"),
        "pre": ["-format", "script:pcodehex", "-onerror", "ignore"],
        "cmd": ["-export", "script"],
    },
    {
        "name": "images",
        "out": Path("assets/images"),
        "pre": ["-format", "image:png_gif_jpeg_alpha", "-onerror", "ignore"],
        "cmd": ["-export", "image"],
    },
    {
        "name": "shapes_svg",
        "out": Path("assets/shapes_svg"),
        "pre": ["-format", "shape:svg,morphshape:svg", "-onerror", "ignore"],
        "cmd": ["-export", "shape,morphshape"],
    },
    {
        "name": "shapes_png",
        "out": Path("assets/shapes_png"),
        "pre": ["-format", "shape:png,morphshape:png_frames", "-onerror", "ignore"],
        "cmd": ["-export", "shape,morphshape"],
    },
    {
        "name": "sounds",
        "out": Path("assets/sounds"),
        "pre": ["-format", "sound:mp3_wav", "-onerror", "ignore"],
        "cmd": ["-export", "sound"],
    },
    {
        "name": "fonts_text_binary_symbols",
        "out": Path("assets/misc"),
        "pre": ["-format", "font:ttf,text:plain", "-onerror", "ignore"],
        "cmd": ["-export", "font,font4,text,binaryData,symbolClass"],
    },
    {
        "name": "frames",
        "out": Path("timelines/frames"),
        "pre": ["-format", "frame:png", "-ignorebackground", "-onerror", "ignore"],
        "cmd": ["-export", "frame"],
    },
    {
        "name": "sprites_buttons",
        "out": Path("timelines/sprites_buttons"),
        "pre": ["-format", "sprite:png,button:png", "-ignorebackground", "-onerror", "ignore"],
        "cmd": ["-export", "sprite,button"],
    },
]

SEARCH_TERMS = [
    "onEnterFrame", "ENTER_FRAME", "addEventListener", "gotoAndStop", "gotoAndPlay",
    "attachMovie", "duplicateMovieClip", "hitTest", "startDrag", "stopDrag",
    "Key.", "Keyboard", "Mouse", "_root", "_global", "stage", "Sound", "loadMovie",
]


def find_ffdec(explicit: str | None = None) -> Path | str:
    if explicit:
        return Path(explicit)
    env = os.environ.get("FFDEC_CLI")
    if env:
        return Path(env)
    if WINDOWS_FFDEC.exists():
        return WINDOWS_FFDEC
    for candidate in ["ffdec-cli", "ffdec", "ffdec.sh"]:
        found = shutil.which(candidate)
        if found:
            return found
    raise FileNotFoundError("Could not find FFDec. Pass --ffdec or set FFDEC_CLI.")


def run(cmd: list[str], dry_run: bool = False, stdout_path: Path | None = None) -> int:
    printable = " ".join(f'"{c}"' if " " in str(c) else str(c) for c in cmd)
    print(printable)
    if dry_run:
        return 0
    if stdout_path:
        stdout_path.parent.mkdir(parents=True, exist_ok=True)
        with stdout_path.open("w", encoding="utf-8", errors="replace") as fh:
            proc = subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT, text=True)
        return proc.returncode
    proc = subprocess.run(cmd)
    return proc.returncode


def file_counts(root: Path) -> dict[str, int]:
    counts: Counter[str] = Counter()
    if not root.exists():
        return {}
    for path in root.rglob("*"):
        if path.is_file():
            counts[path.suffix.lower() or "<no_ext>"] += 1
    return dict(sorted(counts.items()))


def write_manifest(out_dir: Path) -> None:
    rows = []
    for path in sorted(out_dir.rglob("*")):
        if path.is_file() and path.name not in {"manifest.csv"}:
            rows.append({
                "path": str(path.relative_to(out_dir)).replace("\\", "/"),
                "suffix": path.suffix.lower(),
                "bytes": path.stat().st_size,
            })
    with (out_dir / "manifest.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["path", "suffix", "bytes"])
        writer.writeheader()
        writer.writerows(rows)


def scan_code(out_dir: Path) -> dict[str, list[str]]:
    hits: dict[str, list[str]] = {}
    code_roots = [out_dir / "code/actionscript", out_dir / "code/pcodehex"]
    for root in code_roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".as", ".txt", ".pcode"}:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            found = [term for term in SEARCH_TERMS if term in text]
            if found:
                hits[str(path.relative_to(out_dir)).replace("\\", "/")] = found
    return hits


def write_audit(swf: Path, out_dir: Path, results: list[dict[str, object]]) -> None:
    counts = file_counts(out_dir)
    code_hits = scan_code(out_dir)
    lines = [
        "# SWF Porting Audit",
        "",
        f"Source SWF: `{swf}`",
        f"Output folder: `{out_dir}`",
        "",
        "## Extraction Passes",
        "",
    ]
    for result in results:
        status = "ok" if result["returncode"] == 0 else f"exit {result['returncode']}"
        lines.append(f"- `{result['name']}`: {status} -> `{result['out']}`")
    lines.extend(["", "## File Counts", ""])
    for suffix, count in counts.items():
        lines.append(f"- `{suffix}`: {count}")
    lines.extend(["", "## Gameplay Search Hits", ""])
    if code_hits:
        for rel, terms in sorted(code_hits.items()):
            lines.append(f"- `{rel}`: {', '.join(terms)}")
    else:
        lines.append("- No common gameplay terms found in exported code. Check P-code and timeline XML manually.")
    lines.extend([
        "",
        "## Porting Checklist",
        "",
        "- Identify document class, exported symbols, frame scripts, and startup/preloader flow.",
        "- Map symbol IDs/classes to extracted image, shape, sprite, sound, and text assets.",
        "- Use frame/sprite renders to verify animation timing, origins, and visual states.",
        "- Rebuild gameplay systems natively in the target engine; use decompiled code as behavioral reference.",
        "- Re-inspect `structure/movie.xml` and `structure/tags.txt` for timeline-only logic and placed object transforms.",
    ])
    (out_dir / "PORTING_AUDIT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def full(args) -> int:
    swf = Path(args.swf).resolve()
    out_dir = Path(args.output).resolve()
    if not swf.exists():
        raise FileNotFoundError(swf)
    out_dir.mkdir(parents=True, exist_ok=True)
    ffdec = str(find_ffdec(args.ffdec))
    results: list[dict[str, object]] = []

    structure = out_dir / "structure"
    structure.mkdir(parents=True, exist_ok=True)
    rc = run([ffdec, "-dumpSWF", str(swf)], args.dry_run, structure / "tags.txt")
    results.append({"name": "dumpSWF", "returncode": rc, "out": "structure/tags.txt"})
    rc = run([ffdec, "-swf2xml", "-external", "all", str(swf), str(structure / "movie.xml")], args.dry_run)
    results.append({"name": "swf2xml", "returncode": rc, "out": "structure/movie.xml"})

    for export_pass in EXPORT_PASSES:
        pass_out = out_dir / export_pass["out"]
        pass_out.mkdir(parents=True, exist_ok=True)
        cmd = [ffdec] + list(export_pass["pre"]) + list(export_pass["cmd"]) + [str(pass_out), str(swf)]
        rc = run(cmd, args.dry_run)
        results.append({"name": export_pass["name"], "returncode": rc, "out": str(export_pass["out"]).replace("\\", "/")})

    if args.xfl:
        xfl_out = out_dir / "fla_xfl" / f"{swf.stem}.xfl"
        xfl_out.parent.mkdir(parents=True, exist_ok=True)
        rc = run([ffdec, "-format", f"xfl:{args.xfl_version}", "-onerror", "ignore", "-export", "xfl", str(xfl_out), str(swf)], args.dry_run)
        results.append({"name": "xfl", "returncode": rc, "out": str(xfl_out.relative_to(out_dir)).replace("\\", "/")})

    if not args.dry_run:
        write_manifest(out_dir)
        write_audit(swf, out_dir, results)
    return 0 if all(int(r["returncode"]) == 0 for r in results) else 1


def dump_command(args) -> int:
    ffdec = str(find_ffdec(args.ffdec))
    swf = str(Path(args.swf).resolve())
    out = str(Path(args.output).resolve())
    return run([ffdec, "-dumpSWF", swf], args.dry_run, Path(out))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract SWF code, assets, timelines, and structure for game porting.")
    parser.add_argument("--ffdec", help="Path to ffdec-cli/ffdec executable; defaults to FFDEC_CLI, common Windows path, or PATH")
    parser.add_argument("--dry-run", action="store_true", help="Print FFDec commands without running them")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("full", help="Run the full porting extraction pipeline")
    p.add_argument("swf")
    p.add_argument("output")
    p.add_argument("--xfl", action="store_true", help="Also export XFL; this can be large and slow")
    p.add_argument("--xfl-version", default="cs6", help="FFDec XFL target version, e.g. f8, cs3, cs6, cc")

    p = sub.add_parser("dump", help="Dump SWF tags to a text file")
    p.add_argument("swf")
    p.add_argument("output")

    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "full":
        return full(args)
    if args.command == "dump":
        return dump_command(args)
    raise ValueError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
