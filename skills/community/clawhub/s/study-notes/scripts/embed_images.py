#!/usr/bin/env python3
"""embed_images.py — keep study-notes HTML standalone by base64-inlining images.

Two subcommands:

  datauri <img>        Print a data: URI for one image. Paste it into an
                       <img src="..."> in the HTML (MODE C figures).

  inline <html>        Replace every LOCAL <img src="file.png"> in an HTML file
                       with a base64 data: URI, so the final file is fully
                       self-contained. (Skips srcs that are already data:/http(s).)

Pure standard library — no third-party dependencies.
"""
import argparse
import base64
import mimetypes
import os
import re
import sys

mimetypes.add_type("image/svg+xml", ".svg")


def to_data_uri(path):
    if not os.path.exists(path):
        sys.exit(f"Image not found: {path}")
    mime, _ = mimetypes.guess_type(path)
    if mime is None:
        ext = os.path.splitext(path)[1].lower().lstrip(".")
        mime = f"image/{ext or 'png'}"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def cmd_datauri(args):
    uri = to_data_uri(args.image)
    print(uri)
    kb = (len(uri) * 3) // 4 // 1024
    sys.stderr.write(f"[{args.image}: ~{kb} KB base64]\n")


_SRC_RE = re.compile(r'(<img\b[^>]*?\bsrc\s*=\s*)(["\'])(.*?)\2', re.IGNORECASE | re.DOTALL)


def cmd_inline(args):
    if not os.path.exists(args.html):
        sys.exit(f"HTML not found: {args.html}")
    base_dir = os.path.dirname(os.path.abspath(args.html))
    with open(args.html, "r", encoding="utf-8") as f:
        html = f.read()

    stats = {"inlined": 0, "skipped_remote": 0, "missing": 0}

    def repl(m):
        prefix, quote, src = m.group(1), m.group(2), m.group(3)
        low = src.strip().lower()
        if low.startswith(("data:", "http:", "https:", "//")):
            stats["skipped_remote"] += 1
            return m.group(0)
        img_path = src if os.path.isabs(src) else os.path.join(base_dir, src)
        if not os.path.exists(img_path):
            stats["missing"] += 1
            sys.stderr.write(f"  ! missing local image, left as-is: {src}\n")
            return m.group(0)
        uri = to_data_uri(img_path)
        stats["inlined"] += 1
        return f"{prefix}{quote}{uri}{quote}"

    new_html = _SRC_RE.sub(repl, html)
    out = args.out or args.html
    with open(out, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"Inlined {stats['inlined']} image(s) -> {out}  "
          f"(skipped remote/data: {stats['skipped_remote']}, missing: {stats['missing']})")
    if stats["missing"]:
        sys.exit(1)


def main():
    p = argparse.ArgumentParser(description="Base64-inline images to keep HTML standalone.")
    sub = p.add_subparsers(dest="cmd", required=True)

    pd = sub.add_parser("datauri", help="print a data: URI for one image")
    pd.add_argument("image")
    pd.set_defaults(func=cmd_datauri)

    pi = sub.add_parser("inline", help="inline all local <img src> in an HTML file")
    pi.add_argument("html")
    pi.add_argument("-o", "--out", help="write to a new file (default: overwrite in place)")
    pi.set_defaults(func=cmd_inline)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
