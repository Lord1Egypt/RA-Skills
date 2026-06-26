#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT.parent.parent / "tmp" / "image-processing-toolkit-lab-selftest"


def run(cmd: list[str]) -> int:
    print("$", " ".join(str(c) for c in cmd))
    p = subprocess.run(cmd, cwd=ROOT)
    return p.returncode


def seed() -> None:
    from PIL import Image

    WORK.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (320, 200), (120, 30, 220)).save(WORK / "a.png")
    Image.new("RGB", (120, 120), (20, 180, 80)).save(WORK / "b.jpg", quality=92)


def main() -> int:
    py = Path(sys.executable)

    try:
        import PIL  # noqa: F401
        import img2pdf  # noqa: F401
    except Exception as e:
        print("ERR: missing deps in current interpreter:", e)
        return 2

    seed()

    cmds = [
        [str(py), "scripts/convert.py", "--input", str(WORK / "a.png"), "--format", "webp"],
        [str(py), "scripts/compress.py", "--input", str(WORK / "b.jpg"), "--quality", "70"],
        [str(py), "scripts/resize.py", "--input", str(WORK / "a.png"), "--width", "100", "--height", "100", "--mode", "cover"],
        [str(py), "scripts/to_pdf.py", "--input", str(WORK)],
        [str(py), "scripts/batch.py", "--input", str(WORK), "--format", "jpg", "--quality", "75", "--width", "80", "--height", "80", "--mode", "contain", "--dry-run"],
    ]

    rc = 0
    for c in cmds:
        code = run(c)
        if code != 0:
            rc = code

    expected = [
        WORK / "a_converted.webp",
        WORK / "b_compressed.jpg",
        WORK / "a_resized.png",
        WORK.parent / "image-processing-toolkit-lab-selftest_images.pdf",
    ]

    missing = [p for p in expected if not p.exists()]
    if missing:
        print("ERR: missing outputs:")
        for m in missing:
            print(" -", m)
        return 3

    print("Selftest OK")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
