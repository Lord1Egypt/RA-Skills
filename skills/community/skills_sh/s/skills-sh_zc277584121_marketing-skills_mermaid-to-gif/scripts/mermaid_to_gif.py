#!/usr/bin/env python3
"""
mermaid_to_gif.py - Convert Mermaid diagrams to animated GIFs.

Pipeline: Mermaid code -> HTML with animation -> Playwright frame capture -> FFmpeg GIF

Usage:
    python mermaid_to_gif.py diagram.mmd
    python mermaid_to_gif.py document.md --style progressive
    python mermaid_to_gif.py document.md -o ./gifs/ --fps 12 --duration 5
"""

from __future__ import annotations

import argparse
import html as html_lib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


# ============================================================
# Constants
# ============================================================

MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"

STYLES = ["progressive", "highlight-walk", "pulse-flow", "wave"]
DEFAULT_STYLE = "progressive"
DEFAULT_FPS = 10
DEFAULT_DURATION = 4.0
DEFAULT_HOLD = 1.0
DEFAULT_BG = "#ffffff"
DEFAULT_THEME = "default"
DEFAULT_PADDING = 40
DEFAULT_SCALE = 2


# ============================================================
# Dependency checks
# ============================================================


def check_dependencies():
    """Verify required external tools are available."""
    errors = []
    if not shutil.which("ffmpeg"):
        errors.append(
            "FFmpeg is not installed.\n"
            "  macOS:   brew install ffmpeg\n"
            "  Ubuntu:  sudo apt install ffmpeg"
        )
    try:
        import playwright  # noqa: F401
    except ImportError:
        errors.append(
            "Playwright is not installed.\n"
            "  pip install playwright\n"
            "  playwright install chromium"
        )
    if errors:
        for e in errors:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


# ============================================================
# Input parsing
# ============================================================


def extract_mermaid_blocks(text: str) -> list[str]:
    """Extract ```mermaid code blocks from markdown text."""
    pattern = r"```mermaid\s*\n(.*?)```"
    return [m.strip() for m in re.findall(pattern, text, re.DOTALL)]


def read_input(path: str) -> list[tuple[str, str]]:
    """Read input file and return list of (name, mermaid_code) tuples."""
    p = Path(path)
    if not p.exists():
        print(f"Error: {path} does not exist", file=sys.stderr)
        sys.exit(1)

    text = p.read_text(encoding="utf-8")

    if p.suffix == ".mmd":
        return [(p.stem, text.strip())]

    # Markdown or other text file - extract mermaid blocks
    blocks = extract_mermaid_blocks(text)
    if not blocks:
        print(f"No mermaid code blocks found in {path}", file=sys.stderr)
        return []

    if len(blocks) == 1:
        return [(p.stem, blocks[0])]
    return [(f"{p.stem}-{i + 1}", block) for i, block in enumerate(blocks)]


def detect_direction(mermaid_code: str) -> str:
    """Detect diagram flow direction from mermaid source code."""
    first_line = mermaid_code.strip().split("\n")[0].lower()
    if any(d in first_line for d in ["lr", "rl"]):
        return "horizontal"
    return "vertical"


# ============================================================
# Animation JS - shared element collection logic
# ============================================================

ELEMENT_COLLECTION_JS = """
    // Collect elements by type separately for better animation control
    var clusters = [];
    var nodes = [];
    var edges = [];
    var edgeLabels = [];
    var direction = '{direction}';

    var sortFn = direction === 'horizontal'
        ? function(a, b) { return (a.x - b.x) || (a.y - b.y); }
        : function(a, b) { return (a.y - b.y) || (a.x - b.x); };

    svg.querySelectorAll('.cluster').forEach(function(el) {
        var rect = el.getBoundingClientRect();
        clusters.push({ el: el, x: rect.x, y: rect.y });
    });

    svg.querySelectorAll('.node, .actor, [class*="note"]').forEach(function(el) {
        var rect = el.getBoundingClientRect();
        nodes.push({ el: el, x: rect.x, y: rect.y });
    });

    svg.querySelectorAll('.edgePath, [class*="messageLine"], .relation').forEach(function(el) {
        var rect = el.getBoundingClientRect();
        edges.push({ el: el, x: rect.x, y: rect.y });
    });

    svg.querySelectorAll('.edgeLabel, .messageText').forEach(function(el) {
        var rect = el.getBoundingClientRect();
        edgeLabels.push({ el: el, x: rect.x, y: rect.y });
    });

    nodes.sort(sortFn);
    edges.sort(sortFn);
    edgeLabels.sort(sortFn);

    // Build a flat elements array for styles that need it
    var elements = [].concat(clusters, nodes, edges, edgeLabels);

    // Fallback: if nothing found, fade whole SVG
    if (elements.length === 0) {
        svg.style.opacity = '0';
        window.setProgress = function(t) {
            svg.style.opacity = String(Math.min(1, t * 2));
        };
        window.animationReady = true;
        return;
    }
"""


# ============================================================
# Animation JS templates
# ============================================================


def _style_js_progressive() -> str:
    return """
    // Progressive: all elements visible but dimmed, activate sequentially
    // Edges draw in with stroke animation, nodes brighten on activation
    var timeline = [];

    clusters.forEach(function(c) {
        timeline.push({ el: c.el, type: 'cluster' });
    });

    var eIdx = 0, lIdx = 0;
    nodes.forEach(function(n) {
        timeline.push({ el: n.el, type: 'node' });
        if (eIdx < edges.length) {
            timeline.push({ el: edges[eIdx].el, type: 'edge' });
            eIdx++;
        }
        if (lIdx < edgeLabels.length) {
            timeline.push({ el: edgeLabels[lIdx].el, type: 'label' });
            lIdx++;
        }
    });
    while (eIdx < edges.length) {
        timeline.push({ el: edges[eIdx].el, type: 'edge' }); eIdx++;
    }
    while (lIdx < edgeLabels.length) {
        timeline.push({ el: edgeLabels[lIdx].el, type: 'label' }); lIdx++;
    }

    // Assign timing
    timeline.forEach(function(item, i) {
        item.appearAt = (i / timeline.length) * 0.85;
    });

    // Initial state: everything visible but dimmed; edges have stroke hidden
    var dimOpacity = 0.25;
    timeline.forEach(function(item) {
        item.el.style.opacity = String(dimOpacity);
        if (item.type === 'edge') {
            var path = item.el.querySelector('path');
            if (path) {
                try {
                    var len = path.getTotalLength();
                    path.style.strokeDasharray = String(len);
                    path.style.strokeDashoffset = String(len);
                    item._path = path;
                    item._pathLen = len;
                } catch(e) {}
            }
        }
    });

    var activateWidth = 0.08;

    window.setProgress = function(t) {
        timeline.forEach(function(item) {
            if (t >= item.appearAt) {
                var local = Math.min(1, (t - item.appearAt) / activateWidth);
                // Brighten from dim to full
                item.el.style.opacity = String(dimOpacity + (1 - dimOpacity) * local);
                // Draw edge stroke
                if (item._path && item._pathLen) {
                    item._path.style.strokeDashoffset = String(item._pathLen * (1 - local));
                }
            } else {
                item.el.style.opacity = String(dimOpacity);
                if (item._path && item._pathLen) {
                    item._path.style.strokeDashoffset = String(item._pathLen);
                }
            }
        });
    };
    """


def _style_js_highlight_walk() -> str:
    return """
    // Highlight walk: all visible but dimmed, spotlight moves through
    // Build same interleaved timeline as progressive
    var timeline = [];
    clusters.forEach(function(c) { timeline.push({ el: c.el, type: 'cluster' }); });
    var eIdx = 0, lIdx = 0;
    nodes.forEach(function(n) {
        timeline.push({ el: n.el, type: 'node' });
        if (eIdx < edges.length) { timeline.push({ el: edges[eIdx].el, type: 'edge' }); eIdx++; }
        if (lIdx < edgeLabels.length) { timeline.push({ el: edgeLabels[lIdx].el, type: 'label' }); lIdx++; }
    });
    while (eIdx < edges.length) { timeline.push({ el: edges[eIdx].el, type: 'edge' }); eIdx++; }
    while (lIdx < edgeLabels.length) { timeline.push({ el: edgeLabels[lIdx].el, type: 'label' }); lIdx++; }

    timeline.forEach(function(item, i) {
        item.el.style.opacity = '0.15';
        item.target = i / timeline.length;
    });

    var spotWidth = Math.max(0.1, 1.2 / timeline.length);

    window.setProgress = function(t) {
        timeline.forEach(function(item) {
            var dist = Math.abs(t - item.target);
            if (dist < spotWidth / 2) {
                item.el.style.opacity = '1';
                item.el.style.filter = 'drop-shadow(0 0 8px rgba(59,130,246,0.8))';
            } else if (t > item.target + spotWidth / 2) {
                item.el.style.opacity = '0.9';
                item.el.style.filter = 'none';
            } else {
                item.el.style.opacity = '0.15';
                item.el.style.filter = 'none';
            }
        });
    };
    """


def _style_js_pulse_flow() -> str:
    return """
    // Pulse flow: dashed lines flowing along edges (mermaid2gif style)
    // All elements fully visible
    elements.forEach(function(item) { item.el.style.opacity = '1'; });

    // Setup flowing dashed line on edges
    var flowPaths = [];
    svg.querySelectorAll('[class*="edgePath"] path, [class*="messageLine"]').forEach(function(path) {
        try {
            var len = path.getTotalLength();
            var cs = getComputedStyle(path);
            var origWidth = parseFloat(cs.strokeWidth) || 1.5;

            // Fixed dash + gap size for consistent look across all edges
            var dashLen = 10;
            var gapLen = 6;
            path.style.strokeDasharray = dashLen + ' ' + gapLen;
            path.style.strokeWidth = String(Math.max(origWidth, 2));

            flowPaths.push({ el: path, length: len });
        } catch(e) {}
    });

    // Use a fixed flow speed (pixels per unit time) so all edges move at the same pace
    var flowSpeed = 200;

    window.setProgress = function(t) {
        flowPaths.forEach(function(fp) {
            fp.el.style.strokeDashoffset = String(-t * flowSpeed);
        });
    };
    """


def _style_js_wave() -> str:
    return """
    // Wave: all elements fully visible, a scale-pulse ripple sweeps through
    elements.forEach(function(item) { item.el.style.opacity = '1'; });

    // Build same interleaved timeline for wave order
    var timeline = [];
    clusters.forEach(function(c) { timeline.push(c.el); });
    var eIdx = 0, lIdx = 0;
    nodes.forEach(function(n) {
        timeline.push(n.el);
        if (eIdx < edges.length) { timeline.push(edges[eIdx].el); eIdx++; }
        if (lIdx < edgeLabels.length) { timeline.push(edgeLabels[lIdx].el); lIdx++; }
    });
    while (eIdx < edges.length) { timeline.push(edges[eIdx].el); eIdx++; }
    while (lIdx < edgeLabels.length) { timeline.push(edgeLabels[lIdx].el); lIdx++; }

    // Each element gets a trigger time
    var triggers = timeline.map(function(el, i) {
        return { el: el, triggerAt: (i / timeline.length) * 0.8 };
    });

    var pulseWidth = 0.10;

    window.setProgress = function(t) {
        triggers.forEach(function(item) {
            var dt = t - item.triggerAt;
            if (dt >= 0 && dt < pulseWidth) {
                // Brightness pulse + glow sweep (no transform to avoid position shift)
                var phase = dt / pulseWidth;
                var brightness = 1 + 0.4 * Math.sin(phase * Math.PI);
                item.el.style.filter = 'brightness(' + brightness + ') drop-shadow(0 0 6px rgba(59,130,246,0.6))';
            } else {
                item.el.style.filter = 'none';
            }
        });
    };
    """


STYLE_JS_MAP = {
    "progressive": _style_js_progressive,
    "highlight-walk": _style_js_highlight_walk,
    "pulse-flow": _style_js_pulse_flow,
    "wave": _style_js_wave,
}


# ============================================================
# HTML generation
# ============================================================


def generate_html(
    mermaid_code: str,
    style: str,
    theme: str,
    bg_color: str,
    padding: int,
    custom_css: str = "",
) -> str:
    """Generate self-contained HTML with Mermaid.js and animation engine."""
    direction = detect_direction(mermaid_code)
    style_setup = STYLE_JS_MAP[style]()
    escaped_code = html_lib.escape(mermaid_code)

    # Element collection JS with direction substituted
    collection_js = ELEMENT_COLLECTION_JS.replace("{direction}", direction)

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="{MERMAID_CDN}"></script>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: {bg_color};
    display: inline-block;
    padding: {padding}px;
    font-size: 16px;
  }}
  .mermaid svg {{ display: block; }}
  {custom_css}
</style>
</head>
<body>
<pre class="mermaid">{escaped_code}</pre>
<script>
(async function() {{
    mermaid.initialize({{
        startOnLoad: false,
        theme: '{theme}',
        securityLevel: 'loose',
        fontSize: 16
    }});

    try {{
        await mermaid.run();
    }} catch(e) {{
        console.error('Mermaid render error:', e);
    }}

    var svg = document.querySelector('svg');
    if (!svg) {{
        window.setProgress = function() {{}};
        window.animationReady = true;
        return;
    }}

    // Scale up small SVGs for better readability (check rendered CSS size)
    var minSvgWidth = 700;
    var svgRect = svg.getBoundingClientRect();
    if (svgRect.width > 0 && svgRect.width < minSvgWidth) {{
        var ratio = minSvgWidth / svgRect.width;
        var newW = Math.ceil(svgRect.width * ratio);
        var newH = Math.ceil(svgRect.height * ratio);
        svg.setAttribute('width', newW);
        svg.setAttribute('height', newH);
        svg.style.width = newW + 'px';
        svg.style.height = newH + 'px';
        svg.style.maxWidth = 'none';
    }}

    {collection_js}

    // ---- Style-specific animation logic ----
    {style_setup}

    window.setProgress(0);
    window.animationReady = true;
}})();
</script>
</body>
</html>"""


# ============================================================
# Frame capture with Playwright
# ============================================================


def capture_frames(
    html_path: str,
    frames_dir: str,
    fps: int,
    duration: float,
    hold: float,
    scale: int = 2,
) -> int:
    """Use Playwright to capture animation frames. Returns total frame count."""
    from playwright.sync_api import sync_playwright

    anim_frames = int(fps * duration)
    hold_frames = int(fps * hold)

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        # Use deviceScaleFactor for high-DPI rendering
        context = browser.new_context(device_scale_factor=scale)
        page = context.new_page()
        # Set a wide initial viewport so Mermaid has room to render
        page.set_viewport_size({"width": 1400, "height": 900})
        page.goto(f"file://{html_path}")
        page.wait_for_function("window.animationReady === true", timeout=20000)

        # Shrink viewport to fit actual rendered content
        size = page.evaluate(
            """() => {
            var svg = document.querySelector('svg');
            if (!svg) return { width: 800, height: 400 };
            var rect = svg.getBoundingClientRect();
            var body = document.body;
            var pad = parseFloat(getComputedStyle(body).padding) || 0;
            return {
                width: Math.ceil(rect.width + pad * 2),
                height: Math.ceil(rect.height + pad * 2)
            };
        }"""
        )
        vw = max(400, min(size["width"], 2400))
        vh = max(200, min(size["height"], 1600))
        page.set_viewport_size({"width": vw, "height": vh})

        # Capture animation frames
        for i in range(anim_frames + 1):
            t = i / anim_frames if anim_frames > 0 else 1
            page.evaluate(f"window.setProgress({t})")
            page.screenshot(path=os.path.join(frames_dir, f"frame_{i:04d}.png"))

        # Hold last frame
        for j in range(hold_frames):
            idx = anim_frames + 1 + j
            page.screenshot(path=os.path.join(frames_dir, f"frame_{idx:04d}.png"))

        context.close()
        browser.close()

    return anim_frames + 1 + hold_frames


# ============================================================
# GIF assembly with FFmpeg
# ============================================================


def assemble_gif(
    frames_dir: str,
    output_path: str,
    fps: int,
    loop: int = 0,
) -> None:
    """Two-pass FFmpeg palette-based GIF generation for optimal quality."""
    palette = os.path.join(frames_dir, "palette.png")
    pattern = os.path.join(frames_dir, "frame_%04d.png")

    # Pass 1: generate optimized palette
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-framerate", str(fps),
            "-i", pattern,
            "-vf", "palettegen=stats_mode=diff",
            palette,
        ],
        check=True,
        capture_output=True,
    )

    # Pass 2: create GIF using palette with Floyd-Steinberg dithering
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-framerate", str(fps),
            "-i", pattern,
            "-i", palette,
            "-lavfi", "paletteuse=dither=floyd_steinberg",
            "-loop", str(loop),
            output_path,
        ],
        check=True,
        capture_output=True,
    )


# ============================================================
# Main processing
# ============================================================


def process_diagram(
    name: str,
    code: str,
    style: str,
    theme: str,
    bg_color: str,
    padding: int,
    fps: int,
    duration: float,
    hold: float,
    loop: int,
    output_dir: str,
    custom_css: str,
    scale: int = 2,
) -> str:
    """Process a single Mermaid diagram and return output GIF path."""
    output_path = os.path.join(output_dir, f"{name}.gif")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Generate HTML
        html_content = generate_html(code, style, theme, bg_color, padding, custom_css)
        html_path = os.path.join(tmpdir, "diagram.html")
        Path(html_path).write_text(html_content, encoding="utf-8")

        # Capture frames
        frames_dir = os.path.join(tmpdir, "frames")
        os.makedirs(frames_dir)
        frame_count = capture_frames(html_path, frames_dir, fps, duration, hold, scale)

        # Assemble GIF
        assemble_gif(frames_dir, output_path, fps, loop)

    size_kb = os.path.getsize(output_path) / 1024
    print(f"  -> {output_path} ({size_kb:.1f} KB, {frame_count} frames)")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Convert Mermaid diagrams to animated GIFs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s diagram.mmd
  %(prog)s diagram.mmd --style highlight-walk
  %(prog)s document.md -o ./gifs/
  %(prog)s document.md --fps 12 --duration 5 --theme dark
  %(prog)s diagram.mmd --custom-css my-style.css
        """,
    )
    parser.add_argument("input", nargs="+", help="Input .mmd or .md file(s)")
    parser.add_argument(
        "-o", "--output-dir",
        help="Output directory (default: same directory as input file)",
    )
    parser.add_argument(
        "-s", "--style",
        default=DEFAULT_STYLE,
        choices=STYLES,
        help=f"Animation style (default: {DEFAULT_STYLE})",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=DEFAULT_FPS,
        help=f"Frames per second (default: {DEFAULT_FPS})",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=DEFAULT_DURATION,
        help=f"Animation duration in seconds (default: {DEFAULT_DURATION})",
    )
    parser.add_argument(
        "--hold",
        type=float,
        default=DEFAULT_HOLD,
        help=f"Hold last frame duration in seconds (default: {DEFAULT_HOLD})",
    )
    parser.add_argument(
        "--theme",
        default=DEFAULT_THEME,
        help=f"Mermaid theme: default, dark, forest, neutral (default: {DEFAULT_THEME})",
    )
    parser.add_argument(
        "--bg",
        default=DEFAULT_BG,
        help=f"Background color (default: {DEFAULT_BG})",
    )
    parser.add_argument(
        "--padding",
        type=int,
        default=DEFAULT_PADDING,
        help=f"Padding around diagram in pixels (default: {DEFAULT_PADDING})",
    )
    parser.add_argument(
        "--scale",
        type=int,
        default=DEFAULT_SCALE,
        help=f"Render scale factor for resolution (default: {DEFAULT_SCALE}, 2=retina)",
    )
    parser.add_argument(
        "--custom-css",
        help="Path to custom CSS file for additional styling",
    )
    parser.add_argument(
        "--no-loop",
        action="store_true",
        help="Play GIF once instead of looping infinitely",
    )

    args = parser.parse_args()

    check_dependencies()

    custom_css = ""
    if args.custom_css:
        css_path = Path(args.custom_css)
        if not css_path.exists():
            print(f"Error: CSS file not found: {args.custom_css}", file=sys.stderr)
            sys.exit(1)
        custom_css = css_path.read_text(encoding="utf-8")

    loop = 1 if args.no_loop else 0
    results = []

    for input_path in args.input:
        diagrams = read_input(input_path)
        if not diagrams:
            continue

        output_dir = args.output_dir or str(Path(input_path).parent)
        os.makedirs(output_dir, exist_ok=True)

        print(f"\nProcessing {input_path} ({len(diagrams)} diagram(s))...")

        for name, code in diagrams:
            try:
                gif_path = process_diagram(
                    name=name,
                    code=code,
                    style=args.style,
                    theme=args.theme,
                    bg_color=args.bg,
                    padding=args.padding,
                    fps=args.fps,
                    duration=args.duration,
                    hold=args.hold,
                    loop=loop,
                    output_dir=output_dir,
                    custom_css=custom_css,
                    scale=args.scale,
                )
                results.append(gif_path)
            except Exception as e:
                print(f"  Error processing '{name}': {e}", file=sys.stderr)

    if results:
        print(f"\nDone! {len(results)} GIF(s) generated.")
    else:
        print("\nNo diagrams processed.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
