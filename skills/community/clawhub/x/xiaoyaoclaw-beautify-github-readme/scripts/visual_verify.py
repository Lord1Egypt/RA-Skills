#!/usr/bin/env python3
"""Render-and-verify GitHub README visual assets.

Complements audit_readme.py (static XML checks) with what static checks cannot
see: real rendering, clipped/edge-touching content, and WCAG text contrast.

Checks performed per SVG asset:
  1. Render the SVG with headless Chrome at its declared size (PNG output).
  2. Edge scan: warn when rendered content is NOT a uniform full-bleed
     background on every edge (possible clipping or accidental border content).
  3. Contrast check: every <text> fill vs the dominant <rect> background fill
     (WCAG: 4.5:1 body / 3:1 large text, using the 900px GitHub render scale).
  4. Structural sanity: viewBox present, <title> + <desc> present, no
     <script>/<foreignObject>/remote font references.

Usage:
  python3 scripts/visual_verify.py /path/to/repository/README.md [--out DIR]
  python3 scripts/visual_verify.py /path/to/hero.svg [--out DIR]

Prints a report and exits non-zero when issues are found.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import tempfile
import threading
import xml.etree.ElementTree as ET
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# Shared trust boundary for untrusted SVG input; see scripts/svg_safety.py.
try:
    from svg_safety import is_safe_to_render, run_external, safety_issues
except ImportError:  # allow `python3 scripts/visual_verify.py` from any cwd
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from svg_safety import is_safe_to_render, run_external, safety_issues

# ---------------------------------------------------------------- discovery

MARKDOWN_IMAGE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")
HTML_IMAGE = re.compile(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"'][^>]*>", re.I)


def find_chrome() -> str | None:
    """Locate a Chromium-family browser binary.

    Reads standard OS environment variables only (PROGRAMFILES,
    PROGRAMFILES(X86), LOCALAPPDATA on Windows; PATH via shutil.which) to find
    the installed browser. The declared `env` capability in SKILL.md covers
    exactly this lookup — no other environment data is read.
    """
    candidates = []
    if sys.platform == "win32":
        base = os.environ.get("PROGRAMFILES", r"C:\Program Files")
        base86 = os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)")
        local = os.environ.get("LOCALAPPDATA", "")
        candidates = [
            os.path.join(base, "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(base86, "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(local, "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(base86, "Microsoft", "Edge", "Application", "msedge.exe"),
        ]
    elif sys.platform == "darwin":
        candidates = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        ]
    else:
        for name in ("google-chrome", "chromium", "chromium-browser", "microsoft-edge"):
            hit = shutil.which(name)
            if hit:
                return hit
    for c in candidates:
        if c and os.path.exists(c):
            return c
    return None


def local_svg_sources(readme: Path) -> list[tuple[str, Path]]:
    """Return [(src_text, absolute_path)] for local SVG references.

    Only references that resolve inside the README's own directory tree are
    accepted; anything pointing outside it (e.g. ``../../``, root-absolute, or
    Windows-drive paths) is skipped so the checker never reads files from
    outside the requested repository.
    """
    text = readme.read_text(encoding="utf-8")
    srcs = list(MARKDOWN_IMAGE.findall(text))
    srcs += [m for m in HTML_IMAGE.findall(text)]
    root = readme.parent.resolve()
    out = []
    skipped = []
    for src in dict.fromkeys(srcs):
        if src.startswith(("http://", "https://", "data:", "#")):
            continue
        clean = src.split("#", 1)[0].split("?", 1)[0]
        if not clean.lower().endswith(".svg"):
            continue
        p = (readme.parent / clean).resolve()
        try:
            p.relative_to(root)
        except ValueError:
            skipped.append(src)
            continue
        if p.is_file():
            out.append((src, p))
    if skipped:
        print(f"WARNING: skipped SVG reference(s) resolving outside the README tree: {skipped}")
    return out


# ---------------------------------------------------------------- contrast

def parse_color(value: str) -> tuple[int, int, int] | None:
    v = value.strip()
    m = re.fullmatch(r"#([0-9a-fA-F]{6})", v)
    if m:
        h = m.group(1)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    m = re.fullmatch(r"#([0-9a-fA-F]{3})", v)
    if m:
        h = m.group(1)
        return tuple(int(c * 2, 16) for c in h)
    m = re.fullmatch(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", v)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None


def luminance(rgb: tuple[int, int, int]) -> float:
    def chan(c: int) -> float:
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (chan(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def svg_contrast_issues(path: Path) -> tuple[list[str], list[str]]:
    """Check each <text> fill against its container <rect> background.

    Background resolution order: the first filled <rect> declared inside the
    text's own parent group, then up the ancestor chain, then the largest
    <rect> in the document (fallback).

    Returns (issues, notices). `issues` are real contrast failures; `notices`
    are cases the checker cannot decide (e.g. a gradient/pattern background),
    which are reported without failing the run — a legitimate gradient hero
    must not be reported as a defect.
    """
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        return [f"invalid SVG XML: {exc}"], []
    raw_tag = root.tag
    ns = raw_tag.rsplit("}", 1)[0] + "}" if "}" in raw_tag else ""
    def tag(name: str) -> str:
        return f"{ns}{name}"

    # parent map
    parent_of: dict[ET.Element, ET.Element | None] = {root: None}
    for node in root.iter():
        for child in node:
            parent_of[child] = node

    rects: list[tuple[float, tuple[int, int, int]]] = []
    painted_rects = 0
    for rect in root.iter(tag("rect")):
        w = float(rect.get("width", "0") or 0)
        h = float(rect.get("height", "0") or 0)
        raw_fill = (rect.get("fill", "") or "").strip()
        fill = parse_color(raw_fill)
        if fill:
            rects.append((w * h, fill))
        elif raw_fill and raw_fill.lower() != "none":
            painted_rects += 1  # gradient (url(#id)), pattern, currentColor, ...
    if not rects:
        if painted_rects:
            return [], [
                f"{painted_rects} filled <rect> use a non-solid paint "
                "(gradient/pattern); text contrast not machine-verifiable - "
                "inspect the rendered PNG visually"
            ]
        return ["no <rect> background found; cannot verify contrast"], []
    dominant = max(rects, key=lambda r: r[0])[1]

    def container_bg(text_el: ET.Element) -> tuple[int, int, int] | None:
        """Nearest plausible container background.

        Walk ancestors; inside each group take the last filled <rect> declared
        BEFORE the text in document order (paint order: background first).
        Ignore tiny decorative rects (area smaller than roughly the text's own
        bounding box) so small color chips are not mistaken for backgrounds.
        Fall back to the largest rect in the document.
        """
        fs = float(text_el.get("font-size", "16") or 16)
        est = fs * fs * 2  # rough text bbox area
        node: ET.Element | None = text_el
        while node is not None:
            children = list(node)
            try:
                my_idx = children.index(text_el)
            except ValueError:
                my_idx = len(children)
            best: tuple[int, int, int] | None = None
            for child in children[:my_idx]:
                if child.tag != tag("rect"):
                    continue
                fill = parse_color(child.get("fill", ""))
                if not fill:
                    continue
                w = float(child.get("width", "0") or 0)
                h = float(child.get("height", "0") or 0)
                if w * h >= est:
                    best = fill  # last qualifying rect before the text wins
            if best is not None:
                return best
            node = parent_of.get(node)
        return None

    issues: list[str] = []
    for text in root.iter(tag("text")):
        fill = parse_color(text.get("fill", ""))
        if not fill:
            continue
        bg = container_bg(text) or dominant
        size = float(text.get("font-size", "16") or 16)
        weight = text.get("font-weight", "400")
        bold = weight in ("bold", "700", "800", "900") or (weight.isdigit() and int(weight) >= 700)
        # 900px GitHub render => 0.75 scale; large-text thresholds at 24px+ / 18.66px bold+
        rendered = size * 0.75
        large = rendered >= 24 or (bold and rendered >= 18.66)
        ratio = contrast_ratio(fill, bg)
        limit = 3.0 if large else 4.5
        if ratio < limit:
            sample = (text.text or "").strip()[:28]
            issues.append(
                f"low contrast: fill={text.get('fill')} vs bg #{''.join(f'{c:02X}' for c in bg)} "
                f"ratio={ratio:.2f} (<{limit:.1f}, {'large' if large else 'body'} text @{rendered:.0f}px): {sample!r}"
            )
    return issues, []


# ---------------------------------------------------------------- rendering

def render_svg(svg: Path, chrome: str, out_png: Path) -> tuple[int, str]:
    """Render one SVG to PNG inside a hardened sandbox. Returns (ok, err).

    Trust boundary: the SVG under test is treated as untrusted input (it may
    come from a third-party repository). Five layers of isolation:

      1. The SVG is copied into a fresh, empty directory; nothing else from the
         repository is reachable, so the SVG cannot read sibling files.
      2. A static gate (svg_safety.is_safe_to_render) already refused scripts,
         foreignObject, remote fonts, and any non-local resource reference
         (href/src, CSS `url(...)`, `@import`).
      3. The preview origin serves **exactly one URL**: the isolated SVG. A
         request for any other path, host, or port is answered with 403.
      4. That origin is also the browser's only proxy, and Chrome's implicit
         loopback bypass is disabled (`--proxy-bypass-list=<-loopback>`), so
         every request Chrome makes — including literal 127.0.0.1 / localhost
         URLs and other loopback ports — passes the filter in (3). A crafted
         SVG therefore cannot probe or call other services on the loopback
         interface (this is the SSRF containment the previous revision lacked).
      5. DNS resolution is blocked for every hostname (`--host-resolver-rules`),
         so no name leaves the machine even if a reference slipped past (2).
         Loopback stays resolvable only so the gate itself can be reached;
         reaching it does not grant access to anything else, because the gate
         answers 403 for every host, port and path it does not serve.
    """
    svg = svg.resolve()
    content = svg.read_bytes()
    with tempfile.TemporaryDirectory(prefix="vverify-serve-") as td:
        serve_dir = Path(td)
        isolated = serve_dir / svg.name
        shutil.copy2(svg, isolated)

        class GateOriginHandler(BaseHTTPRequestHandler):
            """Serve only the isolated SVG; refuse everything else.

            Because this handler doubles as Chrome's proxy, `self.path` may be
            an absolute URI (`GET http://host:port/path`). Requests that are
            not for the single allowed origin+path are rejected, so the
            rendering browser has no route to any other service.
            """

            protocol_version = "HTTP/1.0"
            allowed_path = f"/{isolated.name}"

            def _reject(self) -> None:
                body = b"blocked by visual_verify render sandbox\n"
                self.send_response(403)
                self.send_header("Content-Type", "text/plain")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def _request_target(self) -> tuple[str, str] | None:
                target = self.path
                if "://" in target:
                    parts = urlsplit(target)
                    return parts.netloc.lower(), parts.path
                return None, target

            def do_GET(self) -> None:  # noqa: N802 (http.server API)
                netloc, path = self._request_target()
                allowed = (
                    netloc in (None, f"127.0.0.1:{self.server.server_port}")
                    and path == self.allowed_path
                )
                if not allowed:
                    self._reject()
                    return
                self.send_response(200)
                self.send_header("Content-Type", "image/svg+xml")
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Cache-Control", "no-store")
                # 第二道防线（静态闸门之外的运行时防线）：即使某个事件处理器
                # 漏过了 svg_safety，CSP 也不允许执行任何脚本、发起任何连接。
                self.send_header(
                    "Content-Security-Policy",
                    "default-src 'none'; img-src data:; style-src 'unsafe-inline'; "
                    "script-src 'none'; connect-src 'none'; font-src 'none'; "
                    "frame-src 'none'; object-src 'none'; base-uri 'none'; "
                    "form-action 'none'",
                )
                self.end_headers()
                self.wfile.write(content)

            def do_HEAD(self) -> None:  # noqa: N802
                self._reject()

            def do_CONNECT(self) -> None:  # noqa: N802
                self._reject()

            def do_POST(self) -> None:  # noqa: N802
                self._reject()

            def log_message(self, *a):  # silence access log noise
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), GateOriginHandler)  # ephemeral port
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            url = f"http://127.0.0.1:{port}/{isolated.name}"
            size = svg_size(svg)
            if size:
                w, h = size
            else:
                w = h = 1200
            cmd = [
                chrome, "--headless", "--disable-gpu", "--hide-scrollbars",
                "--no-first-run", "--no-default-browser-check",
                # Every request Chrome makes — including 127.0.0.1 and localhost
                # on any port — is forced through the single-origin gate above;
                # `<-loopback>` removes Chrome's implicit loopback proxy bypass.
                # Without that token a crafted asset could still reach other
                # services bound to the loopback interface.
                "--proxy-server=http://127.0.0.1:%d" % port,
                "--proxy-bypass-list=<-loopback>",
                # Second layer: no hostname resolves except loopback itself (the
                # gate). Resolvable loopback does not imply reachable: the gate
                # still answers 403 for every path, host, or port it does not
                # serve.
                "--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1",
                # Third layer: JavaScript disabled at the engine level, so an
                # event handler that slipped past both the static gate and the
                # CSP has nothing to execute in.
                "--blink-settings=scriptEnabled=false",
                "--disable-javascript",
                "--user-data-dir=" + str(tempfile.mkdtemp(prefix="chrome-vverify-")),
                f"--window-size={w},{h}",
                f"--screenshot={out_png}",
                url,
            ]
            proc = run_external(cmd, timeout=120, label="Chrome render", check=False)
            if not out_png.exists() or out_png.stat().st_size == 0:
                detail = (proc.stderr or "") + " | STDOUT: " + (proc.stdout or "")
                return False, f"rc={proc.returncode} " + (detail.strip() or "no screenshot produced")[:400]
            return True, ""
        except SystemExit as exc:  # raised by run_external on timeout/missing binary
            return False, str(exc)
        finally:
            server.shutdown()
            thread.join(timeout=5)


def svg_size(path: Path) -> tuple[int, int] | None:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError:
        return None
    w = root.get("width")
    h = root.get("height")
    if w and h:
        try:
            return int(float(w)), int(float(h))
        except ValueError:
            return None
    vb = root.get("viewBox")
    if vb:
        parts = vb.split()
        if len(parts) == 4:
            try:
                return int(float(parts[2])), int(float(parts[3]))
            except ValueError:
                return None
    return None


def edge_scan_issues(png: Path) -> tuple[list[str], list[str]]:
    """Warn when rendered content is not a uniform full-bleed background.

    Transparent pixels (rounded-corner outside areas) and the white canvas
    Chrome paints outside the SVG are ignored. Each 4px edge band is compared
    against its own **median** colour: pixels that deviate strongly from that
    median are treated as content touching the edge (possible clipping).

    Using a median + deviation threshold (rather than "dominant colour") keeps
    deliberate full-bleed gradients and subtle background ramps out of the
    failure path, while a real element touching the edge still trips it.

    Returns (issues, notices); notices mark bands that cannot be judged
    (photographic/noisy edges) instead of failing the run.
    """
    if not HAS_PIL:
        return [], []
    im = Image.open(png).convert("RGBA")
    w, h = im.size
    px = im.load()
    issues: list[str] = []
    notices: list[str] = []
    # max per-channel deviation from the band median that still counts as
    # "same background"; 48/255 keeps gradients and AA ramps quiet while any
    # distinctly coloured element crossing the edge stands out.
    DEVIATION = 48
    edges = {"top": [(x, y) for x in range(w) for y in range(min(4, h))],
             "bottom": [(x, y) for x in range(w) for y in range(max(0, h - 4), h)],
             "left": [(x, y) for x in range(min(4, w)) for y in range(h)],
             "right": [(x, y) for x in range(max(0, w - 4), w) for y in range(h)]}
    for name, cells in edges.items():
        band: list[tuple[int, int, int]] = []
        for x, y in cells:
            r, g, b, a = px[x, y]
            if a < 128 or (r, g, b) == (255, 255, 255):
                continue
            band.append((r, g, b))
        total = len(band)
        if total == 0:
            continue
        ordered = sorted(band, key=lambda c: 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2])
        median = ordered[total // 2]
        deviating = sum(
            1 for c in band if max(abs(c[0] - median[0]), abs(c[1] - median[1]), abs(c[2] - median[2])) > DEVIATION
        )
        if deviating / total > 0.06:
            issues.append(
                f"edge '{name}' has {deviating / total:.0%} pixels deviating from the band "
                f"background ({median}) in the 4px band - content may touch/clip the edge; "
                "inspect the render"
            )
        elif len(set(band)) > 200:
            notices.append(
                f"edge '{name}' is a photographic/noisy edge ({len(set(band))} colours) - "
                "clipping not machine-verifiable; inspect the render"
            )
    return issues, notices


# ---------------------------------------------------------------- main

def audit_svg_static(path: Path) -> list[str]:
    issues: list[str] = []
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        return [f"invalid SVG XML: {exc}"]
    if "viewBox" not in root.attrib:
        issues.append("missing viewBox")
    found_title = found_desc = False
    for node in root.iter():
        tag = node.tag.rsplit("}", 1)[-1]
        if tag == "title":
            found_title = True
        if tag == "desc":
            found_desc = True
    if not found_title:
        issues.append("missing <title>")
    if not found_desc:
        issues.append("missing <desc>")
    # Trust-boundary problems (scripts, foreignObject, remote fonts, external or
    # non-local resource references) come from the shared gate so both render
    # paths report the same findings.
    issues.extend(safety_issues(path))
    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("target", help="README.md or an .svg file")
    ap.add_argument("--out", default=None, help="directory for rendered PNG previews")
    args = ap.parse_args()

    target = Path(args.target).expanduser().resolve()
    if not target.is_file():
        print(f"ERROR: not found: {target}")
        return 2

    if target.suffix.lower() == ".svg":
        sources = [("(direct)", target)]
    else:
        sources = local_svg_sources(target)
        if not sources:
            print(f"No local SVG references found in {target.name}")

    chrome = find_chrome()
    if not chrome and sources:
        print("WARNING: Chrome/Edge not found - rendering skipped (static checks only)")

    out_dir = Path(args.out).expanduser().resolve() if args.out else Path(
        tempfile.mkdtemp(prefix="readme-vverify-")
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    failures = 0
    for src, svg in sources:
        print(f"\n== {svg.relative_to(target.parent) if target.suffix.lower() != '.svg' else svg.name}")
        static = audit_svg_static(svg)
        contrast, notices = svg_contrast_issues(svg)
        for issue in static:
            print(f"  [static] {issue}")
        for notice in notices:
            print(f"  [notice] {notice}")
        for issue in contrast:
            print(f"  [contrast] {issue}")
        if static or contrast:
            failures += 1

        if chrome:
            safe, reason = is_safe_to_render(svg)
            if not safe:
                print(f"  [render] SKIPPED (untrusted content: {reason})")
                failures += 1
                continue
            png = out_dir / (svg.stem + ".png")
            ok, err = render_svg(svg, chrome, png)
            if not ok:
                print(f"  [render] FAILED: {err}")
                failures += 1
            else:
                print(f"  [render] {png.name} ({png.stat().st_size // 1024} KB)")
                edge_issues, edge_notices = edge_scan_issues(png)
                for notice in edge_notices:
                    print(f"  [notice] {notice}")
                for issue in edge_issues:
                    print(f"  [edge] {issue}")
                    failures += 1
        else:
            print("  [render] skipped (no Chrome/Edge)")

    print(f"\nRendered previews: {out_dir}")
    print("Next: visually inspect every PNG at GitHub width (~900px) and 360px, "
          "then confirm with a vision model before publishing.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
