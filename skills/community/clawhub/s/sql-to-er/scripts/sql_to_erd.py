#!/usr/bin/env python3
"""
SQL DDL → classic Chen ER diagram.

Parse: yanleaf API first, local sql_parser fallback.
PNG: prefer Graphviz when `dot` is available; else matplotlib B&W Chen.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate_erd import normalize_model, to_mermaid, to_dot, to_gojs_model, render_graphviz
from export_word import export_design_doc
from render_chen import render as render_chen_png
from watermark import add_watermark


def _parse_tables(sql: str, prefer_api: bool = True, api_url: str | None = None) -> list:
    if prefer_api:
        try:
            from api_client import parse_sql_via_api, DEFAULT_API
            url = api_url or DEFAULT_API
            tables = parse_sql_via_api(sql, api_url=url)
            print(f"[OK] Parsed via API ({url})")
            return tables
        except Exception as e:
            print(f"[WARN] API parse failed: {e}", file=sys.stderr)
            print("[WARN] Falling back to local SQLParser", file=sys.stderr)

    from sql_parser import SQLParser
    tables = [t.to_dict() for t in SQLParser().parse(sql)]
    print("[OK] Parsed via local SQLParser")
    return tables


def _has_graphviz() -> bool:
    return shutil.which("dot") is not None


def main() -> int:
    parser = argparse.ArgumentParser(description="SQL → classic Chen ER diagram (yanleaf)")
    parser.add_argument("input", nargs="?", help="Path to .sql file")
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--out", default="erd")
    parser.add_argument(
        "--format",
        choices=["mermaid", "dot", "png", "svg", "gojs", "json", "word", "all"],
        default="all",
    )
    parser.add_argument("--style", choices=["chen", "crow"], default="chen")
    parser.add_argument("--english", action="store_true")
    parser.add_argument("--no-api", action="store_true")
    parser.add_argument("--api-url", default=None)
    parser.add_argument("--watermark", default="yanleaf.com")
    parser.add_argument("--no-watermark", action="store_true")
    parser.add_argument("--max-attrs", type=int, default=12,
                        help="Max attributes per entity for matplotlib (0=all)")
    parser.add_argument(
        "--engine",
        choices=["auto", "graphviz", "matplotlib"],
        default="auto",
        help="PNG engine: auto = Graphviz if available else matplotlib",
    )
    args = parser.parse_args()

    if args.stdin:
        sql = sys.stdin.read()
    elif args.input:
        sql = Path(args.input).read_text(encoding="utf-8")
    else:
        parser.error("Provide a .sql file or --stdin")

    tables_data = _parse_tables(sql, prefer_api=not args.no_api, api_url=args.api_url)
    if not tables_data:
        print("[ERR] No tables parsed", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(tables_data, ensure_ascii=False, indent=2))
        return 0

    model = normalize_model(tables_data)
    out_prefix = Path(args.out)
    formats = (
        ["mermaid", "dot", "png", "svg", "gojs", "word"]
        if args.format == "all"
        else [args.format]
    )
    wm = None if args.no_watermark else (args.watermark or None)

    if "mermaid" in formats:
        mmd = to_mermaid(model)
        path = out_prefix.with_suffix(".mmd")
        path.write_text(mmd, encoding="utf-8")
        print(f"[OK] Mermaid → {path}")
        if args.format == "mermaid":
            print(mmd)

    if "gojs" in formats:
        gojs = to_gojs_model(tables_data, english=args.english)
        path = out_prefix.with_suffix(".gojs.json")
        path.write_text(json.dumps(gojs, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[OK] GoJS    → {path}")

    if "png" in formats:
        png_path = out_prefix.with_suffix(".png")
        engine = args.engine
        if engine == "auto":
            engine = "graphviz" if _has_graphviz() else "matplotlib"
        try:
            if engine == "graphviz":
                dot = to_dot(model, style=args.style)
                png_path = render_graphviz(dot, out_prefix, "png")
                if wm:
                    png_path = add_watermark(png_path, text=wm)
                print(f"[OK] PNG     → {png_path}  (graphviz)")
            else:
                ma = args.max_attrs if args.max_attrs > 0 else None
                png_path = render_chen_png(model, png_path, watermark=wm, max_attrs=ma)
                print(f"[OK] PNG     → {png_path}  (matplotlib)")
        except Exception as e:
            if engine == "graphviz":
                print(f"[WARN] Graphviz PNG failed: {e}; trying matplotlib", file=sys.stderr)
                try:
                    ma = args.max_attrs if args.max_attrs > 0 else None
                    png_path = render_chen_png(model, out_prefix.with_suffix(".png"), watermark=wm, max_attrs=ma)
                    print(f"[OK] PNG     → {png_path}  (matplotlib fallback)")
                except Exception as e2:
                    print(f"[WARN] PNG failed: {e2}", file=sys.stderr)
            else:
                print(f"[WARN] PNG failed: {e}", file=sys.stderr)

    if any(f in formats for f in ("dot", "svg")):
        try:
            dot = to_dot(model, style=args.style)
            if "dot" in formats:
                path = out_prefix.with_suffix(".dot")
                path.write_text(dot, encoding="utf-8")
                print(f"[OK] DOT     → {path}")
            if "svg" in formats:
                if _has_graphviz():
                    print(f"[OK] SVG     → {render_graphviz(dot, out_prefix, 'svg')}")
                else:
                    print("[WARN] SVG needs Graphviz (dot); skipped", file=sys.stderr)
        except Exception as e:
            print(f"[WARN] Graphviz output failed: {e}", file=sys.stderr)

    if "word" in formats:
        try:
            path = out_prefix.with_suffix(".docx")
            export_design_doc(tables_data, path)
            print(f"[OK] Word    → {path}")
        except Exception as e:
            print(f"[WARN] Word failed: {e}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
