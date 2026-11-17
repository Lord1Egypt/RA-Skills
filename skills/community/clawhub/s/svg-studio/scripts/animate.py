#!/usr/bin/env python3
"""
animate.py — Build an animated image (GIF / APNG / WebP) from SVG frames.

Two input modes:

  A) FRAMES mode (most controllable, model-friendly):
     Provide a directory of numbered SVG files (frame-000.svg, frame-001.svg, ...).
     Each SVG is rendered to PNG (reusing render.py's engine logic via subprocess),
     then composited into an animation with Pillow.

       animate.py --frames-dir ./frames -o out.gif --fps 12
       animate.py --frames-dir ./frames -o out.webp --fps 24 --loop 0

  B) TEMPLATE mode (procedural): a single SVG containing the literal token
     "__T__" (a float 0..1 progress) is rendered N times with __T__ substituted.

       animate.py --template anim.svg --frames 30 -o out.gif --fps 15

Output formats by extension: .gif (palette), .webp (lossy/lossless), .apng/.png (APNG).
For MP4, pass -o out.mp4 (requires ffmpeg on PATH; falls back with a clear message).

Notes
-----
* Animated SVG with SMIL/CSS (<animate>, @keyframes) plays natively in browsers/HTML
  and needs NO conversion — just embed the .svg. Use this script only when you need a
  real animated *file* (GIF/APNG/WebP/MP4).
* All Python deps (Pillow) install into the isolated venv, never global.
"""
import argparse
import glob
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RENDER = os.path.join(HERE, "render.py")

# Native-extension packages (Pillow) must NOT use the managed python: its hardened
# runtime rejects third-party .so (Team ID mismatch). Build this venv from a python
# whose runtime allows loading standard wheels (system python.org build works).
# VENV lives in the skill root (one level above scripts/), derived from this file's
# location so the skill can be renamed/moved without editing code.
VENV = os.path.join(os.path.dirname(HERE), ".venv")
_PYDIR = "Scripts" if sys.platform == "win32" else "bin"
PYBIN = os.path.join(VENV, _PYDIR, "python.exe" if sys.platform == "win32" else "python")
PIPBIN = os.path.join(VENV, _PYDIR, "pip.exe" if sys.platform == "win32" else "pip")


def _pick_base_python():
    import pathlib
    cands = []
    # macOS
    cands += [
        "/Library/Frameworks/Python.framework/Versions/3.13/bin/python3",
        "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3",
        "/opt/homebrew/bin/python3",
        "/usr/local/bin/python3",
        "/usr/bin/python3",
    ]
    # Windows (python.org installer default & Microsoft Store)
    cands += [
        r"C:\Python313\python.exe",
        r"C:\Python312\python.exe",
        r"C:\Python311\python.exe",
        str(pathlib.Path.home() / r"AppData\Local\Programs\Python\Python313\python.exe"),
        str(pathlib.Path.home() / r"AppData\Local\Programs\Python\Python312\python.exe"),
    ]
    # Cross-platform WorkBuddy managed python
    cands.append(os.path.expanduser("~/.workbuddy/binaries/python/versions/3.13.12/bin/python3"))
    cands.append(os.path.expanduser("~/.workbuddy/binaries/python/versions/3.13.12/Scripts/python.exe"))
    for c in cands:
        if c and os.path.exists(c):
            return c
    return sys.executable


BASE_PY = _pick_base_python()


def log(m):
    print(m, file=sys.stderr)


def ensure_pillow():
    """Make sure Pillow is importable in the CURRENT interpreter.
    If we are not running under the isolated venv (which has Pillow), install
    Pillow there and re-exec this script with the venv python."""
    try:
        import PIL  # noqa: F401
        return True
    except ImportError:
        pass
    # not importable here -> ensure venv + Pillow, then re-exec under venv python
    if not os.path.exists(PYBIN):
        subprocess.run([BASE_PY, "-m", "venv", VENV], check=True)
    chk = subprocess.run([PYBIN, "-c", "import PIL"], capture_output=True)
    if chk.returncode != 0:
        log("[python] installing Pillow into isolated venv ...")
        r = subprocess.run([PIPBIN, "install", "-q", "Pillow"], capture_output=True, text=True)
        if r.returncode != 0:
            log("[python] Pillow install failed: %s" % (r.stderr or "")[-300:])
            return False
    if os.path.abspath(sys.executable) != os.path.abspath(PYBIN):
        log("[python] re-exec under isolated venv python")
        os.execv(PYBIN, [PYBIN, os.path.abspath(__file__)] + sys.argv[1:])
    return True


def render_svg_to_png(svg_path, png_path, scale, width, bg):
    cmd = [BASE_PY, RENDER, svg_path, "-o", png_path, "--bg", bg]
    if width:
        cmd += ["--width", str(width)]
    else:
        cmd += ["--scale", str(scale)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if not (os.path.exists(png_path) and os.path.getsize(png_path) > 0):
        log("[render] frame failed: %s\n%s" % (svg_path, (r.stderr or "")[-300:]))
        return False
    return True


def collect_frame_svgs(frames_dir):
    files = []
    for ext in ("*.svg", "*.SVG"):
        files += glob.glob(os.path.join(frames_dir, ext))
    # natural sort by trailing number when present
    def key(p):
        m = re.search(r'(\d+)', os.path.basename(p))
        return (int(m.group(1)) if m else 0, p)
    return sorted(files, key=key)


def build_frames_from_template(template_path, n, work):
    with open(template_path, "r", encoding="utf-8") as f:
        tpl = f.read()
    if "__T__" not in tpl:
        log("ERROR: template has no __T__ token to substitute (0..1 progress).")
        return []
    out = []
    for i in range(n):
        t = i / (n - 1) if n > 1 else 0.0
        svg = tpl.replace("__T__", "%.6f" % t)
        p = os.path.join(work, "frame-%04d.svg" % i)
        with open(p, "w", encoding="utf-8") as f:
            f.write(svg)
        out.append(p)
    return out


def save_animation(png_paths, out_path, fps, loop, quality, bg="#ffffff"):
    from PIL import Image
    duration = int(round(1000.0 / fps))  # ms per frame
    ext = os.path.splitext(out_path)[1].lower()

    frames = [Image.open(p).convert("RGBA") for p in png_paths]
    # unify size to first frame
    base_size = frames[0].size
    frames = [f if f.size == base_size else f.resize(base_size) for f in frames]

    if ext == ".gif":
        # GIF needs palette; flatten alpha on the requested matte (not a
        # hardcoded white — a colored bg must not bleed white halos).
        matte = bg if bg not in (None, "transparent", "none") else "#ffffff"
        rgb = []
        for f in frames:
            m = Image.new("RGBA", f.size, matte)
            m.alpha_composite(f)
            rgb.append(m.convert("P", palette=Image.ADAPTIVE, colors=256))
        rgb[0].save(out_path, save_all=True, append_images=rgb[1:],
                    duration=duration, loop=loop, disposal=2, optimize=True)
    elif ext == ".webp":
        frames[0].save(out_path, save_all=True, append_images=frames[1:],
                       duration=duration, loop=loop, quality=quality, method=6)
    elif ext in (".apng", ".png"):
        frames[0].save(out_path, save_all=True, append_images=frames[1:],
                       duration=duration, loop=loop, format="PNG")
    else:
        return False
    return True


def save_mp4(png_paths, out_path, fps):
    import shutil as _shutil
    ff = _shutil.which("ffmpeg")
    if not ff:
        log("[mp4] ffmpeg not found on PATH. Install ffmpeg or choose .gif/.webp.")
        return False
    with tempfile.TemporaryDirectory() as td:
        for i, p in enumerate(png_paths):
            dst = os.path.join(td, "f%05d.png" % i)
            try:
                os.symlink(os.path.abspath(p), dst)
            except OSError:
                # Windows without Developer Mode: symlinks need privileges.
                _shutil.copyfile(p, dst)
        cmd = [ff, "-y", "-framerate", str(fps), "-i", os.path.join(td, "f%05d.png"),
               "-pix_fmt", "yuv420p", "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
               out_path]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
            return True
        log("[mp4] ffmpeg failed: %s" % (r.stderr or "")[-400:])
        return False


def main():
    ap = argparse.ArgumentParser(description="Build animated image from SVG frames/template")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--frames-dir", help="directory of numbered .svg frames")
    src.add_argument("--template", help="single .svg with __T__ token (0..1 progress)")
    ap.add_argument("--frames", type=int, default=30, help="frame count for template mode")
    ap.add_argument("-o", "--output", required=True, help="output .gif/.webp/.apng/.mp4")
    ap.add_argument("--fps", type=float, default=12.0)
    ap.add_argument("--loop", type=int, default=0, help="0 = infinite")
    ap.add_argument("--scale", type=float, default=1.0, help="DPR for frame PNGs")
    ap.add_argument("--width", type=float, help="force frame width px (overrides scale)")
    ap.add_argument("--bg", default="#ffffff", help="background for frames (gif needs solid)")
    ap.add_argument("--quality", type=int, default=90, help="webp quality")
    args = ap.parse_args()

    if not ensure_pillow():
        return 1

    with tempfile.TemporaryDirectory() as work:
        # 1. gather svg frame paths
        if args.template:
            svgs = build_frames_from_template(args.template, args.frames, work)
        else:
            svgs = collect_frame_svgs(args.frames_dir)
        if not svgs:
            log("ERROR: no SVG frames found.")
            return 2
        log("[animate] %d frames" % len(svgs))

        # 2. render each frame to PNG. First frame runs alone (warms up the
        # engine choice + any venv/pip setup, avoiding concurrent pip races);
        # the rest render in parallel — each render.py gets its own Chrome
        # profile dir, so concurrent headless runs are safe.
        pngs = [os.path.join(work, "out-%04d.png" % i) for i in range(len(svgs))]
        jobs = list(zip(svgs, pngs))
        if not render_svg_to_png(jobs[0][0], jobs[0][1], args.scale, args.width, args.bg):
            return 3
        rest = jobs[1:]
        max_workers = min(8, os.cpu_count() or 4)
        if rest and max_workers > 1:
            from concurrent.futures import ThreadPoolExecutor
            log("[animate] rendering %d frames on %d workers ..." % (len(rest), max_workers))
            with ThreadPoolExecutor(max_workers=max_workers) as pool:
                results = list(pool.map(
                    lambda j: render_svg_to_png(j[0], j[1], args.scale, args.width, args.bg),
                    rest))
            if not all(results):
                return 3

        # 3. compose
        ext = os.path.splitext(args.output)[1].lower()
        ok = save_mp4(pngs, args.output, args.fps) if ext == ".mp4" \
            else save_animation(pngs, args.output, args.fps, args.loop, args.quality, args.bg)
        if not ok:
            log("ERROR: failed to write %s" % args.output)
            return 4

    log("OK -> %s (%d frames @ %sfps)" % (args.output, len(svgs), args.fps))
    print(args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
