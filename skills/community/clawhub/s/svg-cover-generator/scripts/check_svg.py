#!/usr/bin/env python3
"""Basic structural validation for an SVG file."""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = "{http://www.w3.org/2000/svg}"
DISALLOWED_TAGS = {"script", "foreignObject"}


def local_name(tag: str) -> str:
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def validate_svg(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        return [f"XML parse error: {exc}"]

    root = tree.getroot()
    if local_name(root.tag) != "svg":
        errors.append("Root element is not <svg>.")

    width = root.attrib.get("width")
    height = root.attrib.get("height")
    view_box = root.attrib.get("viewBox")

    if not width or not height:
        errors.append("SVG should declare both width and height.")
    if not view_box:
        errors.append("SVG should declare a viewBox.")

    text_nodes = 0
    for element in root.iter():
        name = local_name(element.tag)
        if name in DISALLOWED_TAGS:
            errors.append(f"Disallowed tag found: <{name}>")
        if name == "image":
            href = element.attrib.get("href") or element.attrib.get("{http://www.w3.org/1999/xlink}href")
            if href and (href.startswith("http://") or href.startswith("https://")):
                errors.append("Remote image reference found in <image>.")
        if name == "text" and (element.text or "").strip():
            text_nodes += 1

    if text_nodes == 0:
        errors.append("No non-empty <text> nodes found.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an SVG file.")
    parser.add_argument("svg_path", help="Path to an SVG file")
    args = parser.parse_args()

    path = Path(args.svg_path).expanduser().resolve()
    if not path.is_file():
        print(f"[ERROR] File not found: {path}")
        return 1

    errors = validate_svg(path)
    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        return 1

    print("[OK] SVG looks structurally valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
