#!/usr/bin/env python3
"""Embed the bundled ECharts runtime into a deliverable HTML file."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ECHARTS_MARKER = "ECharts 5.5.0 embedded for offline use"
ECHARTS_USE_RE = re.compile(r"\becharts\.init\s*\(", re.IGNORECASE)
ECHARTS_SCRIPT_RE = re.compile(
    r"<script\b[^>]*\bsrc=(['\"])(?P<src>[^'\"]*echarts[^'\"]*)\1[^>]*>\s*</script\s*>",
    re.IGNORECASE,
)
DEFAULT_BUNDLE = Path(__file__).resolve().parent.parent / "assets" / "echarts-5.5.0.min.js"


def verify_html(html: str) -> list[str]:
    if not ECHARTS_USE_RE.search(html):
        return []

    problems: list[str] = []
    external = [match.group("src") for match in ECHARTS_SCRIPT_RE.finditer(html)]
    if external:
        problems.append(f"external ECharts script remains: {external[0]}")
    if ECHARTS_MARKER not in html:
        problems.append("ECharts is used but the bundled runtime is not embedded")
    return problems


def inline_echarts(html: str, bundle: str) -> tuple[str, int]:
    if not ECHARTS_USE_RE.search(html) or ECHARTS_MARKER in html:
        return html, 0
    if "</script" in bundle.lower():
        raise ValueError("ECharts bundle unexpectedly contains </script")

    replacement = (
        "<script>\n"
        f"/* {ECHARTS_MARKER} */\n"
        f"{bundle}\n"
        "</script>"
    )
    output, count = ECHARTS_SCRIPT_RE.subn(lambda _match: replacement, html, count=1)
    if count == 0:
        raise ValueError("ECharts is used but no external ECharts <script src=...> tag was found")
    return output, count


def main() -> int:
    parser = argparse.ArgumentParser(
        description="将技能内置 ECharts 运行时嵌入 HTML，使图表可离线、跨电脑打开"
    )
    parser.add_argument("--html", required=True, help="输入 HTML 文件")
    parser.add_argument("-o", "--output", help="输出文件；默认覆盖输入文件")
    parser.add_argument("--bundle", default=str(DEFAULT_BUNDLE), help="ECharts bundle 路径")
    parser.add_argument("--check-only", action="store_true", help="只检查，不写文件")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    html_path = Path(args.html).expanduser().resolve()
    if not html_path.is_file():
        print(f"error: html not found: {html_path}", file=sys.stderr)
        return 1

    html = html_path.read_text(encoding="utf-8")
    if args.check_only:
        problems = verify_html(html)
        result = {"ok": not problems, "problems": problems}
        if args.json:
            print(json.dumps(result, ensure_ascii=False))
        else:
            for problem in problems:
                print(problem, file=sys.stderr)
        return 1 if problems else 0

    bundle_path = Path(args.bundle).expanduser().resolve()
    if not bundle_path.is_file():
        print(f"error: ECharts bundle not found: {bundle_path}", file=sys.stderr)
        return 1

    try:
        output, replaced = inline_echarts(
            html, bundle_path.read_text(encoding="utf-8")
        )
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    problems = verify_html(output)
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        return 1

    output_path = Path(args.output).expanduser().resolve() if args.output else html_path
    output_path.write_text(output, encoding="utf-8")
    result = {"ok": True, "output": str(output_path), "embedded": bool(replaced)}
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"ok: {output_path} embedded={bool(replaced)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
