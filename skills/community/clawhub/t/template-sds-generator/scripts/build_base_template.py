#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "src"))
    from sds_generator.render.docx_builder import create_base_template

    create_base_template(root / "assets" / "templates" / "sds_base.docx")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
