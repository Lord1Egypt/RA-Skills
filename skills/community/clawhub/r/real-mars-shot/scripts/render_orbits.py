#!/usr/bin/env python3
"""Write a standalone orbit HTML file (canvas fallback plus optional three.js) and an SVG."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rms.viz import orbit_html, orbit_svg, write


def main() -> None:
    parser = argparse.ArgumentParser(description="Render an Earth-Mars transfer diagram")
    parser.add_argument("--out", required=True, help="HTML path. An .svg sibling is also written.")
    args = parser.parse_args()
    html_path = Path(args.out)
    svg_path = html_path.with_suffix(".svg")
    write(html_path, orbit_html())
    write(svg_path, orbit_svg())
    print(json.dumps({"ok": True, "html": str(html_path), "svg": str(svg_path), "three_js": "optional CDN, canvas fallback always present"}))


if __name__ == "__main__":
    main()
