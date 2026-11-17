#!/usr/bin/env python3
"""塔吊吊装校核 CLI（纯 stdlib）。

用法：
  python3 scripts/crane_check.py --handoff site_handoff.json \
      --fleet crane_fleet.json --baseline baseline.json --out-dir out/crane

退出码：
  0 正常出结果（结果仍为估算）
  2 输入文件/字段错误
  4 坐标单位不是米，或单位不一致
  5 口径未锁定（baseline 缺失/字段为空/版本不一致）
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from site_layout import __version__  # noqa: E402
from site_layout.crane_check import csv_rows, render_markdown, run_check  # noqa: E402
from site_layout.model import (  # noqa: E402
    BaselineError,
    SiteLayoutError,
    UnitError,
    load_all,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="crane_check",
        description="按锁定口径校核塔吊覆盖与额定起重量（估算，final_check=false）",
    )
    parser.add_argument("--handoff", required=True, help="site_handoff.json（site-handoff/v1）")
    parser.add_argument("--fleet", required=True, help="crane_fleet.json")
    parser.add_argument("--baseline", required=True, help="baseline.json（口径锁）")
    parser.add_argument("--out-dir", default="out/crane", help="输出目录，默认 out/crane")
    parser.add_argument(
        "--dynamic-factor",
        type=float,
        default=1.1,
        help="动载系数，默认 1.1",
    )
    parser.add_argument(
        "--hook-weight",
        type=float,
        default=0.3,
        help="未在塔吊记录中给出吊具重量时的默认值（t），默认 0.3",
    )
    parser.add_argument("--version", action="version", version=f"crane_check {__version__}")
    return parser


def _write_outputs(result: dict, out_dir: Path) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)

    json_path = out_dir / "crane_check.json"
    json_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    csv_path = out_dir / "crane_check.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerows(csv_rows(result))

    md_path = out_dir / "crane_check.md"
    md_path.write_text(render_markdown(result) + "\n", encoding="utf-8")
    return {"json": json_path, "csv": csv_path, "md": md_path}


HANDOFF_SCHEMA = "site-handoff/v1"
DIRECT_CAD_SUFFIXES = (".dwg", ".dxf", ".pdf", ".dwt", ".dwf", ".dws")


def _assert_handoff_path(path: str) -> None:
    suffix = Path(path).suffix.lower()
    if suffix in DIRECT_CAD_SUFFIXES:
        raise SiteLayoutError(
            f"拒绝直接读取 {suffix}：塔吊识图必须经 lis-skill-bus → cad-file-reader，"
            "使用 reader 输出的 site-handoff/v1 契约"
        )


def _assert_reader_handoff(handoff) -> None:
    """塔吊 handoff 必须来自 reader 经 bus 的契约，不收直读 CAD 产物。"""
    if not handoff.contract_id or not handoff.source_sha256:
        raise SiteLayoutError(
            "handoff 缺 contract_id/source_sha256：无法证明来自 cad-file-reader 契约"
        )


def _check_args(args: argparse.Namespace) -> None:
    if args.dynamic_factor <= 0:
        raise SiteLayoutError("--dynamic-factor 必须大于 0")
    if args.hook_weight < 0:
        raise SiteLayoutError("--hook-weight 不能为负")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        _check_args(args)
        _assert_handoff_path(args.handoff)
        handoff, fleet, baseline = load_all(args.handoff, args.fleet, args.baseline)
        _assert_reader_handoff(handoff)
        result = run_check(
            handoff,
            fleet,
            baseline,
            dynamic_factor=args.dynamic_factor,
            default_hook_t=args.hook_weight,
        )
    except BaselineError as exc:
        print(f"先锁口径再校核：{exc}", file=sys.stderr)
        return 5
    except UnitError as exc:
        print(f"坐标单位错误：{exc}", file=sys.stderr)
        return 4
    except SiteLayoutError as exc:
        print(f"输入错误：{exc}", file=sys.stderr)
        return 2

    paths = _write_outputs(result, Path(args.out_dir).expanduser())
    summary = result["summary"]
    print(
        "[crane_check] total={total} ok={ok} review={review} insufficient={insufficient} "
        "blind={blind} unknown_no_table={unknown_no_table} out_of_range={out_of_range} "
        "unknown_no_weight={unknown_no_weight}".format(**summary)
    )
    print(
        f"[crane_check] grade={result['conclusion_grade']} "
        f"final_check={str(result['final_check']).lower()}"
    )
    print(f"[crane_check] out={paths['json'].parent}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
