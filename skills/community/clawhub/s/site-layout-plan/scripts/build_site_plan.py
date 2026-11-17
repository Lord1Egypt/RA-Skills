#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分阶段施工平面布置：场地模型 + 规则校核 + 周边约束 + DXF/PNG。

链路：
  base-map.json（prepare_site 产出）+ 设施 JSON（reader 识图或人工）
  + 可选 *.crane.json（reader 塔吊识图）+ 可选 site-context.json（周边环境）
  -> 每阶段 site-stage-layout/v1 + 26 条规则 + 道路 R1~R4 + 周边约束
  -> 六视角审查 + DXF/PNG/图签/自检
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from site_layout.bootstrap import ensure_runtime  # noqa: E402

ensure_runtime(__file__)

from site_layout.context import ContextError, load_context  # noqa: E402
from site_layout.pipeline import resolve_stages, run_plan  # noqa: E402
from site_layout.siteplan import (  # noqa: E402
    SitePlanError, load_base_map, load_cranes, load_facilities,
)


def _parse_params(values: list[str]) -> dict:
    params = {}
    for item in values or []:
        if "=" not in item:
            raise SitePlanError(f"--rule-param 需要 key=value，收到 {item!r}")
        key, value = item.split("=", 1)
        params[key.strip()] = value.strip()
    return params


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="分阶段施工平面布置校核与出图")
    parser.add_argument("--base-map", required=True, help="prepare_site.py 产出的 base-map.json")
    parser.add_argument("--facilities", required=True, help="设施 JSON（cad-site-facility/v1 或 site-facilities/v1）")
    parser.add_argument("--context", default="", help="周边环境 site-context/v1（高压线、住宅、河道、市政管线等）")
    parser.add_argument("--cranes", action="append", default=[], help="reader *.crane.json，可重复")
    parser.add_argument("--stages", default="all", help="all 或 earthwork,structure,finish")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--project", default="")
    parser.add_argument("--title", default="")
    parser.add_argument("--drawing-no", dest="drawing_no", default="")
    parser.add_argument("--scale", default="1:500")
    parser.add_argument("--revision", default="0")
    parser.add_argument("--date", default="")
    parser.add_argument("--rule-param", action="append", default=[], help="覆盖规则阈值，如 fire_lane_min_width_m=4")
    parser.add_argument("--allow-source-mismatch", action="store_true",
                        help="不同源时仍出 DRAFT-SOURCE-MISMATCH 草稿，仅供比对")
    args = parser.parse_args(argv)

    try:
        base_map, base_sha = load_base_map(args.base_map)
        facilities, fac_source, fac_data = load_facilities(args.facilities)
        cranes, crane_sources = load_cranes(args.cranes, base_map.get("extents_mm"))
        context = load_context(args.context) if args.context else None
        params = _parse_params(args.rule_param)
        stages = resolve_stages(args.stages)

        outcome = run_plan(
            base_map=base_map, base_sha=base_sha,
            facilities=facilities, fac_source=fac_source, fac_data=fac_data,
            cranes=cranes, crane_sources=crane_sources,
            stages=stages, out_dir=args.out_dir,
            project=args.project,
            title_params={"title": args.title, "drawing_no": args.drawing_no,
                          "scale": args.scale, "revision": args.revision, "date": args.date},
            params=params, context=context,
            allow_source_mismatch=args.allow_source_mismatch,
        )
        for result in outcome["results"]:
            print("{}: {}".format(result["stage"], result["dxf"]))
        print("manifest: {}".format(Path(args.out_dir) / "manifest.json"))
        return outcome["exit_code"]
    except (SitePlanError, ContextError) as exc:
        print("[{}] {}".format(exc.__class__.__name__, exc), file=sys.stderr)
        return int(getattr(exc, "exit_code", 2))
    except RuntimeError as exc:
        print("[StageDrawError] {}".format(exc), file=sys.stderr)
        return 5


if __name__ == "__main__":
    raise SystemExit(main())
