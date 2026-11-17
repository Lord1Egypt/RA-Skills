#!/usr/bin/env python3
"""
render.py — Render an SVG file to PNG (or wrap into a standalone HTML).

Rendering strategy (in priority order, auto-fallback):
  1. headless Chrome / Chromium / Edge   -> best fidelity (gradients, filters, fonts)
  2. Python resvg (via `resvg-py`)       -> fast, no browser; degrades heavy
     hand-drawn filters (feTurbulence+feDisplacementMap over-blurs text)
  3. Python cairosvg                     -> cross-platform, no browser needed

The script auto-derives output dimensions from the SVG viewBox / width-height,
multiplied by --scale (DPR). Supports transparent or solid background.

Usage:
  render.py input.svg                          # -> input.png  (auto size, scale=2)
  render.py input.svg -o out.png --scale 2
  render.py input.svg --bg "#0f172a"           # solid background
  render.py input.svg --bg transparent         # transparent (default)
  render.py input.svg --width 1600             # force output width (height auto by ratio)
  render.py input.svg --html out.html          # also emit a standalone HTML wrapper
  render.py input.svg --engine chrome|cairosvg|resvg|auto

Exit code 0 on success; non-zero on failure with a clear stderr message.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time


def log(msg):
    print(msg, file=sys.stderr)


# ---------------------------------------------------------------------------
# SVG dimension parsing
# ---------------------------------------------------------------------------
def parse_svg_size(svg_text):
    """Return (width, height) in px from viewBox or width/height attrs."""
    # Prefer viewBox (most reliable for ratio)
    m = re.search(r'viewBox\s*=\s*["\']\s*([\d.+-]+)\s+([\d.+-]+)\s+([\d.+-]+)\s+([\d.+-]+)\s*["\']', svg_text)
    if m:
        w = float(m.group(3))
        h = float(m.group(4))
        if w > 0 and h > 0:
            return w, h

    def _attr(name):
        mm = re.search(r'\b' + name + r'\s*=\s*["\']\s*([\d.]+)\s*(px)?\s*["\']', svg_text)
        return float(mm.group(1)) if mm else None

    w = _attr('width')
    h = _attr('height')
    if w and h:
        return w, h
    # Fallback default
    return 1200.0, 800.0


def find_browser():
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        shutil.which("google-chrome"),
        shutil.which("google-chrome-stable"),
        shutil.which("chromium"),
        shutil.which("chromium-browser"),
        shutil.which("chrome"),
        shutil.which("microsoft-edge"),
        # Windows common paths
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    ]
    for c in candidates:
        if c and os.path.exists(c):
            return c
    return None


def build_html(svg_text, bg):
    body_bg = "transparent" if bg in (None, "transparent", "none") else bg
    return (
        '<!doctype html><html><head><meta charset="utf-8">'
        '<style>html,body{margin:0;padding:0;background:%s}'
        'svg{display:block}</style></head><body>%s</body></html>'
    ) % (body_bg, svg_text)


# ---------------------------------------------------------------------------
# Engine: Chrome
# ---------------------------------------------------------------------------
def render_chrome(svg_text, out_png, out_w, out_h, bg, browser):
    from pathlib import Path
    html = build_html(svg_text, bg)
    with tempfile.TemporaryDirectory() as td:
        html_path = os.path.join(td, "page.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        # Per-invocation user-data-dir: avoids the default-profile singleton
        # lock (conflicts with a running GUI Chrome or parallel renders).
        profile = os.path.join(td, "profile")
        # transparent background flag: 00000000 = fully transparent
        default_bg = "00000000" if bg in (None, "transparent", "none") else "ffffffff"
        cmd = [
            browser, "--headless", "--disable-gpu", "--no-sandbox",
            "--user-data-dir=%s" % profile,
            "--no-first-run", "--no-default-browser-check",
            "--disable-extensions", "--disable-sync",
            "--disable-background-networking", "--disable-component-update",
            "--password-store=basic", "--use-mock-keychain",
            "--force-device-scale-factor=1",
            "--virtual-time-budget=3000",
            "--window-size=%d,%d" % (int(round(out_w)), int(round(out_h))),
            "--default-background-color=%s" % default_bg,
            "--hide-scrollbars",
            "--screenshot=%s" % out_png,
            Path(html_path).as_uri(),
        ]
        last_err = ""
        for attempt in range(3):
            # Chrome --headless=new with a fresh profile often writes the PNG
            # then lingers without exiting. So: watch for the file instead of
            # waiting for process exit, then kill the process ourselves.
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            ok = False
            deadline = time.time() + 45
            while time.time() < deadline:
                if proc.poll() is not None:  # exited on its own
                    if os.path.exists(out_png) and os.path.getsize(out_png) > 0:
                        ok = True
                    break
                if os.path.exists(out_png) and os.path.getsize(out_png) > 0:
                    time.sleep(0.3)  # let it finish flushing
                    ok = os.path.getsize(out_png) > 0
                    break
                time.sleep(0.2)
            try:
                proc.kill()
            except OSError:
                pass
            try:
                out, err = proc.communicate(timeout=5)
                last_err = ((err or out) or b"").decode("utf-8", "replace").strip()
            except Exception:
                pass
            if ok:
                return True
            # macOS mach port rendezvous race -> retry
            time.sleep(0.6)
        log("[chrome] failed after retries: %s" % last_err[-400:])
        return False


# ---------------------------------------------------------------------------
# Engine: cairosvg / resvg (Python, auto-install into isolated venv)
# ---------------------------------------------------------------------------
# Python fallback engines (cairosvg / resvg) use native extensions. The managed
# python's hardened runtime rejects third-party .so (Team ID mismatch), so build
# this venv from a python whose runtime allows standard wheels (system build).
# VENV lives in the skill root (one level above scripts/), derived from this file's
# location so the skill can be renamed/moved without editing code.
VENV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".venv")
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


def ensure_venv():
    if not os.path.exists(PYBIN):
        log("[python] creating isolated venv at %s" % VENV)
        subprocess.run([BASE_PY, "-m", "venv", VENV], check=True)
    return PYBIN


def pip_install(pkg):
    py = ensure_venv()
    log("[python] installing %s into isolated venv ..." % pkg)
    r = subprocess.run([PIPBIN, "install", "-q", pkg], capture_output=True, text=True)
    if r.returncode != 0:
        log("[python] pip install %s failed: %s" % (pkg, (r.stderr or "")[-300:]))
        return False
    return True


def render_cairosvg(svg_path, out_png, out_w, out_h, bg):
    py = ensure_venv()
    # check import in venv
    chk = subprocess.run([py, "-c", "import cairosvg"], capture_output=True)
    if chk.returncode != 0:
        if not pip_install("cairosvg"):
            return False
    bg_arg = "None" if bg in (None, "transparent", "none") else repr(bg)
    code = (
        "import cairosvg;"
        "cairosvg.svg2png(url=%r, write_to=%r, output_width=%d, output_height=%d, background_color=%s)"
        % (svg_path, out_png, int(round(out_w)), int(round(out_h)), bg_arg)
    )
    r = subprocess.run([py, "-c", code], capture_output=True, text=True)
    if os.path.exists(out_png) and os.path.getsize(out_png) > 0:
        return True
    log("[cairosvg] failed: %s" % (r.stderr or "")[-400:])
    return False


def render_resvg(svg_path, out_png, out_w, out_h, bg):
    py = ensure_venv()
    chk = subprocess.run([py, "-c", "import resvg_py"], capture_output=True)
    if chk.returncode != 0:
        if not pip_install("resvg-py"):
            return False
    # resvg_py renders at the SVG's own size; we scale via width/height.
    # background: only when a solid color was requested (None keeps alpha).
    bg_arg = None if bg in (None, "transparent", "none") else str(bg)
    code = (
        "import resvg_py;"
        "png=resvg_py.svg_to_bytes(svg_path=%r, width=%d, height=%d, background=%r);"
        "open(%r,'wb').write(png)"
        % (svg_path, int(round(out_w)), int(round(out_h)), bg_arg, out_png)
    )
    r = subprocess.run([py, "-c", code], capture_output=True, text=True)
    if os.path.exists(out_png) and os.path.getsize(out_png) > 0:
        return True
    log("[resvg] failed: %s" % (r.stderr or "")[-400:])
    return False


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Render SVG -> PNG (Chrome-first fidelity, resvg/cairosvg no-browser fallback)")
    ap.add_argument("input", help="input .svg file")
    ap.add_argument("-o", "--output", help="output .png path (default: alongside input)")
    ap.add_argument("--scale", type=float, default=2.0, help="DPR multiplier (default 2.0)")
    ap.add_argument("--width", type=float, help="force output width in px (height keeps ratio)")
    ap.add_argument("--height", type=float, help="force output height in px (width keeps ratio)")
    ap.add_argument("--bg", default="transparent", help="background: 'transparent' or a color like '#0f172a'")
    ap.add_argument("--engine", default="auto", choices=["auto", "chrome", "cairosvg", "resvg"])
    ap.add_argument("--html", help="also write a standalone HTML wrapper to this path")
    args = ap.parse_args()

    if not os.path.exists(args.input):
        log("ERROR: input not found: %s" % args.input)
        return 2

    with open(args.input, "r", encoding="utf-8") as f:
        svg_text = f.read()

    vb_w, vb_h = parse_svg_size(svg_text)
    ratio = vb_h / vb_w

    if args.width:
        out_w = args.width
        out_h = args.height if args.height else args.width * ratio
    elif args.height:
        out_h = args.height
        out_w = args.height / ratio
    else:
        out_w = vb_w * args.scale
        out_h = vb_h * args.scale

    out_png = args.output or os.path.splitext(args.input)[0] + ".png"

    # Optional HTML wrapper
    if args.html:
        with open(args.html, "w", encoding="utf-8") as f:
            f.write(build_html(svg_text, args.bg))
        log("[html] wrote %s" % args.html)

    # Engine selection
    order = []
    if args.engine == "auto":
        # Chrome first: fidelity king (verified 2026-09-17 side-by-side — resvg
        # over-applies feDisplacementMap, blurring hand-drawn filter text).
        # resvg is the reliable no-browser fallback (self-contained wheel, no
        # system libcairo); cairosvg last (needs libcairo installed).
        order = ["chrome", "resvg", "cairosvg"]
    else:
        order = [args.engine]

    browser = find_browser()
    for eng in order:
        if eng == "chrome":
            if not browser:
                log("[chrome] no browser found, skipping")
                continue
            if render_chrome(svg_text, out_png, out_w, out_h, args.bg, browser):
                log("OK engine=chrome -> %s (%dx%d)" % (out_png, int(out_w), int(out_h)))
                print(out_png)
                return 0
        elif eng == "resvg":
            if render_resvg(args.input, out_png, out_w, out_h, args.bg):
                log("OK engine=resvg -> %s (%dx%d)" % (out_png, int(out_w), int(out_h)))
                print(out_png)
                return 0
        elif eng == "cairosvg":
            if render_cairosvg(args.input, out_png, out_w, out_h, args.bg):
                log("OK engine=cairosvg -> %s (%dx%d)" % (out_png, int(out_w), int(out_h)))
                print(out_png)
                return 0

    log("ERROR: all engines failed. Tried: %s" % ", ".join(order))
    return 1


if __name__ == "__main__":
    sys.exit(main())
