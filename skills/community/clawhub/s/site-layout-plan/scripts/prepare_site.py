#!/usr/bin/env python3
"""reader 契约 -> 出图底图 base-map/v1（单位换算 + 红线串接 + 留痕）。

用法：
  python3 scripts/prepare_site.py --site out/场地识图/总图.site.json --out-dir out/prepared
  python3 scripts/prepare_site.py --site detail.site.json --out-dir out/prepared \
      --unit mm --confirmed-by lis

退出码：0 成功；2 输入错误/非 reader 契约/直接给 CAD；4 单位缺失或冲突。
硬链路：DWG/DXF/PDF → lis-skill-bus → cad-file-reader → cad-contract/v1 → 本脚本。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from site_layout.model import SiteLayoutError  # noqa: E402
from site_layout.prepare import (  # noqa: E402
    prepare,
    validate_reader_contract,
    validate_reader_path,
    write_outputs,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prepare_site.py",
        description="把 cad-file-reader 的 *.site.json 适配成出图底图（统一 mm）",
    )
    parser.add_argument("--site", required=True, help="reader 生成的 *.site.json")
    parser.add_argument("--out-dir", required=True, help="输出目录（不得等于输入文件路径）")
    parser.add_argument("--unit", choices=["mm", "m", "cm", "ft"], help="图纸未声明单位时的人工确认值")
    parser.add_argument(
        "--confirmed-by",
        default=os.environ.get("USER", "") or "operator-local",
        help="人工确认人（写入报告留痕，默认取本机用户名）",
    )
    parser.add_argument("--tolerance-mm", type=float, default=50.0,
                        help="红线端点聚类容差（mm）；保持小值以保住真实短边")
    parser.add_argument("--close-gap-mm", type=float, default=None,
                        help="允许一次性收口的首尾缺口上限（mm）；不改端点聚类，只闭合首尾")
    parser.add_argument("--boundary-layer", default="",
                        help="只从指定图层取边界（层名需与 reader 输出完全一致）")
    parser.add_argument("--building-layer", default="",
                        help="只从指定图层取主体轮廓（层名需与 reader 输出完全一致）；"
                             "默认按 建筑-屋顶-外轮廓 > 建筑-平面/轮廓 > BUILDING 排序自动选")
    parser.add_argument("--min-building-area-m2", type=float, default=200.0,
                        help="主体轮廓最小闭合面积（默认 200 m²，用于滤掉门房/雨棚等碎环）")
    parser.add_argument("--stem", default="base-map", help="输出文件名前缀，默认 base-map")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    path = Path(args.site).expanduser()
    if not path.is_file():
        print(f"[输入错误 exit 2] 找不到 reader 契约：{path}")
        return 2
    try:
        validate_reader_path(path)
    except SiteLayoutError as exc:
        print(f"[{type(exc).__name__} exit {exc.exit_code}] {exc}")
        return exc.exit_code
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"[输入错误 exit 2] 读取失败：{path}：{exc}")
        return 2
    try:
        validate_reader_contract(path, data)
        base_map = prepare(
            data,
            path,
            unit_override=args.unit,
            confirmed_by=args.confirmed_by,
            tolerance_mm=args.tolerance_mm,
            boundary_layer=args.boundary_layer,
            close_gap_mm=args.close_gap_mm,
            building_layer=args.building_layer,
            min_building_area_m2=args.min_building_area_m2,
        )
        json_path, md_path = write_outputs(base_map, Path(args.out_dir), stem=args.stem)
    except SiteLayoutError as exc:
        print(f"[{type(exc).__name__} exit {exc.exit_code}] {exc}")
        return exc.exit_code

    unit = base_map["unit"]
    print(
        f"[prepare] unit={base_map['coord_unit']} basis={unit['basis']} "
        f"segments={len(base_map['site_geometry'])} "
        f"redline_pts={len(base_map['redline'])} closed={base_map['redline_closed']} "
        f"buildings={len(base_map.get('buildings') or [])} "
        f"warnings={len(base_map['warnings'])}"
    )
    print(f"[prepare] out={json_path}")
    print(f"[prepare] report={md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
