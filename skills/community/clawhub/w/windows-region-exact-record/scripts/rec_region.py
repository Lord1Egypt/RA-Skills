#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Record a fixed screen region for an EXACT number of seconds (Windows).

Needs ffmpeg. Lookup order:
  1. env var FFMPEG
  2. <this folder>\\ffmpeg\\bin\\ffmpeg.exe   (portable drop-in, no install)
  3. ffmpeg on PATH

Usage:
  python rec_region.py --sec 10 --pick          # click 2 corners, then record 10s
  python rec_region.py --sec 10                 # region from last_region.txt
  python rec_region.py --sec 10 --region 100 200 800 600
  python rec_region.py --check                  # show the capture box for 3s, no file written
  python rec_region.py --sec 10 --countdown 3   # 3s lead-in, then exactly 10s
"""
import argparse
import datetime as dt
import pathlib
import shutil
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT_OUTDIR = pathlib.Path.home() / "Videos" / "Screen Recordings"


def find_ffmpeg():
    import os

    env = os.environ.get("FFMPEG")
    if env and pathlib.Path(env).exists():
        return env
    local = HERE / "ffmpeg" / "bin" / "ffmpeg.exe"
    if local.exists():
        return str(local)
    return shutil.which("ffmpeg")


def pick_interactive():
    """Click top-left then bottom-right; returns (x, y, w, h) and caches it."""
    sys.path.insert(0, str(HERE))
    import pick_region as pr

    pr.set_dpi_aware()
    print("pick region: click the TOP-LEFT corner ...  (ESC to abort)", flush=True)
    tl = pr.wait_click("top-left")
    if tl is None:
        print("aborted")
        sys.exit(1)
    print("pick region: click the BOTTOM-RIGHT corner ...", flush=True)
    br = pr.wait_click("bottom-right")
    if br is None:
        print("aborted")
        sys.exit(1)

    x = min(tl[0], br[0])
    y = min(tl[1], br[1])
    w = abs(br[0] - tl[0])
    h = abs(br[1] - tl[1])
    w -= w % 2
    h -= h % 2
    (HERE / "last_region.txt").write_text("%d %d %d %d\n" % (x, y, w, h), encoding="ascii")
    print("region saved to last_region.txt", flush=True)
    return x, y, w, h


def parse_region(args):
    if args.region:
        parts = [int(v) for v in args.region.replace(",", " ").split()]
    else:
        f = HERE / "last_region.txt"
        if not f.exists():
            print("no region: run pick_region.py first, or pass --region X Y W H")
            sys.exit(2)
        parts = [int(v) for v in f.read_text().split()]
    if len(parts) != 4:
        print("region needs 4 numbers: X Y W H")
        sys.exit(2)
    x, y, w, h = parts
    w -= w % 2
    h -= h % 2
    return x, y, w, h


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sec", type=float, default=10.0, help="exact duration in seconds")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--region", help='"X Y W H" (physical px); default: last_region.txt')
    ap.add_argument("--out", help="output mp4 path")
    ap.add_argument("--outdir", default=str(DEFAULT_OUTDIR))
    ap.add_argument("--countdown", type=int, default=3, help="lead-in seconds before capture")
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--no-mouse", action="store_true", help="do not draw the cursor")
    ap.add_argument("--pick", action="store_true", help="click two corners to choose the region first")
    ap.add_argument("--check", action="store_true", help="draw the capture box for 3s, write nothing")
    a = ap.parse_args()

    ff = find_ffmpeg()
    if not ff:
        print("ffmpeg not found. Either:")
        print('  winget install --id Gyan.FFmpeg -e')
        print("  ...or drop a portable build into %s" % (HERE / "ffmpeg" / "bin" / "ffmpeg.exe"))
        sys.exit(3)

    x, y, w, h = pick_interactive() if a.pick else parse_region(a)

    common = [
        ff, "-hide_banner", "-loglevel", "error", "-stats",
        "-f", "gdigrab",
        "-framerate", str(a.fps),
        "-draw_mouse", "0" if a.no_mouse else "1",
        "-offset_x", str(x), "-offset_y", str(y),
        "-video_size", "%dx%d" % (w, h),
    ]

    print("region  : x=%d y=%d  %dx%d  (physical px)" % (x, y, w, h))
    print("ffmpeg  : %s" % ff)

    if a.check:
        cmd = common + ["-show_region", "1", "-i", "desktop", "-t", "3", "-f", "null", "-"]
        print("check   : the capture box will blink on screen for 3s ...")
        return subprocess.call(cmd)

    out = pathlib.Path(a.out) if a.out else (
        pathlib.Path(a.outdir)
        / ("region_%s_%gs.mp4" % (dt.datetime.now().strftime("%Y%m%d_%H%M%S"), a.sec))
    )
    out.parent.mkdir(parents=True, exist_ok=True)

    for i in range(a.countdown, 0, -1):
        print("  starting in %d ..." % i, flush=True)
        time.sleep(1)

    cmd = common + [
        "-i", "desktop",
        "-t", ("%g" % a.sec),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", str(a.crf),
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-y", str(out),
    ]
    print("recording exactly %gs ..." % a.sec, flush=True)
    rc = subprocess.call(cmd)
    if rc == 0 and out.exists():
        print("")
        print("OK  %s  (%.2f MB)" % (out, out.stat().st_size / 1048576))
    else:
        print("ffmpeg exited with code %s" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
