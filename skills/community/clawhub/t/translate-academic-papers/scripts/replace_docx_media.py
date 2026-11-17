#!/usr/bin/env python3
"""Replace one exact DOCX media member without changing the source file."""

from __future__ import annotations

import argparse
import tempfile
import zipfile
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_docx", type=Path)
    parser.add_argument("output_docx", type=Path)
    parser.add_argument("media_member", help="exact member such as word/media/image3.png")
    parser.add_argument("replacement_image", type=Path)
    args = parser.parse_args()

    if not args.media_member.startswith("word/media/") or ".." in args.media_member:
        raise SystemExit("media_member must be an exact safe word/media/... member")
    payload = args.replacement_image.read_bytes()
    if not payload:
        raise SystemExit("replacement image is empty")
    args.output_docx.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(args.input_docx, "r") as source:
        names = source.namelist()
        if args.media_member not in names:
            raise SystemExit(f"member not found: {args.media_member}")
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False, dir=args.output_docx.parent) as handle:
            temporary = Path(handle.name)
        try:
            with zipfile.ZipFile(temporary, "w") as target:
                for info in source.infolist():
                    data = payload if info.filename == args.media_member else source.read(info.filename)
                    target.writestr(info, data)
            temporary.replace(args.output_docx)
        finally:
            if temporary.exists():
                temporary.unlink()
    print(args.output_docx)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

