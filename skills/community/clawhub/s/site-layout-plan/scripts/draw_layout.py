#!/usr/bin/env python3
"""施工平面布置图派生出图 CLI（DXF/PNG/图签/自检）。

用法：
  python3 scripts/draw_layout.py --site 总图.site.json \
      --handoff site_handoff.json --check crane_check.json \
      --baseline baseline.json --out-dir out/layout [--layout layout.json] [--draft]

退出码：
  0 出图成功，自检无 fail
  2 输入文件/字段/依赖错误
  4 坐标或图纸单位不是 mm/m
  5 口径未锁、契约不一致（未加 --draft）或自检存在 fail
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from site_layout import __version__  # noqa: E402
from site_layout.bootstrap import ensure_runtime  # noqa: E402
from site_layout.model import BaselineError, SiteLayoutError, UnitError  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="draw_layout",
        description="把场地底图、塔吊布置与吊装校核画成派生 DXF/PNG，并出图签与自检；原图只读。",
    )
    parser.add_argument("--site", required=True, help="cad-file-reader 的 cad-site-geometry/v1 JSON（或 prepare_site 派生的 base-map.json）；不直读 CAD/PDF")
    parser.add_argument("--handoff", required=True, help="site_handoff.json（site-handoff/v1）")
    parser.add_argument("--check", required=True, help="crane_check.json（crane-check/v1）")
    parser.add_argument("--baseline", required=True, help="baseline.json（口径锁）")
    parser.add_argument("--out-dir", required=True, help="输出目录；不能等于原图目录")
    parser.add_argument("--layout", help="塔吊布置 JSON；默认找与 site 同名的 *.layout.json")
    parser.add_argument("--titleblock", help="图签模板 JSON；默认 templates/titleblock.json")
    parser.add_argument("--draft", action="store_true", help="允许契约不一致时出 DRAFT 草稿图")
    parser.add_argument("--title", help="图签标题（覆盖模板）")
    parser.add_argument("--drawing-no", help="图号（覆盖模板）")
    parser.add_argument("--scale", help="比例，如 1:500（覆盖模板）")
    parser.add_argument("--date", help="日期 YYYY-MM-DD（覆盖模板）")
    parser.add_argument("--project", help="项目名（覆盖模板；默认取 handoff.project）")
    parser.add_argument("--revision", help="版本号（覆盖模板）")
    parser.add_argument("--site-contract-id", help="DXF 未写 CONTRACT_ID 时从命令行补契约号")
    parser.add_argument("--version", action="version", version=f"draw_layout {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        ensure_runtime(__file__)
    except RuntimeError as exc:
        print(f"[依赖错误] {exc}", file=sys.stderr)
        return 2

    from site_layout.draw import draw_layout

    try:
        result = draw_layout(
            site_path=args.site,
            handoff_path=args.handoff,
            check_path=args.check,
            baseline_path=args.baseline,
            out_dir=args.out_dir,
            layout_path=args.layout,
            titleblock_path=args.titleblock,
            draft=args.draft,
            title=args.title,
            drawing_no=args.drawing_no,
            scale=args.scale,
            date=args.date,
            project=args.project,
            revision=args.revision,
            site_contract_id=args.site_contract_id,
        )
    except UnitError as exc:
        print(f"[单位错误 exit 4] {exc}", file=sys.stderr)
        return 4
    except BaselineError as exc:
        print(f"[口径未锁 exit 5] {exc}", file=sys.stderr)
        return 5
    except SiteLayoutError as exc:
        code = int(getattr(exc, "exit_code", 2))
        print(f"[出图失败 exit {code}] {exc}", file=sys.stderr)
        return code
    except Exception as exc:  # noqa: BLE001 - CLI 兜底，保留真实错误文本
        print(f"[出图失败 exit 2] {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result.get("exit_code"):
        print(
            "[自检失败 exit 5] 文件已保留，请查看 selfcheck.json 的 fail 项",
            file=sys.stderr,
        )
    return int(result.get("exit_code", 0))


if __name__ == "__main__":
    raise SystemExit(main())
