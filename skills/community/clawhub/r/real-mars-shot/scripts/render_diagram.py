#!/usr/bin/env python3
"""Write a Mermaid or SVG diagram: deltav, techtree, habitat, architecture."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rms.viz import architecture_mermaid, deltav_mermaid, habitat_svg, techtree_mermaid, write


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a Real Mars Shot diagram")
    parser.add_argument("--kind", required=True, choices=["deltav", "techtree", "habitat", "architecture"])
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    if args.kind == "deltav":
        text = deltav_mermaid()
    elif args.kind == "techtree":
        text = techtree_mermaid()
    elif args.kind == "habitat":
        text = habitat_svg()
    else:
        text = architecture_mermaid()
    path = write(Path(args.out), text)
    print(json.dumps({"ok": True, "path": path, "kind": args.kind}))


if __name__ == "__main__":
    main()
