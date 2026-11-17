#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""土建 run_qty 接入 lis-skill-bus（可选拉起上一步 cad 契约）。

用法：
  python3 qty_statesync.py --project 项目 [--building 楼栋] [--floor 楼层] \
          --out-dir <run_qty 输出目录> [--cad-skill-dir <cad-file-reader 根目录>]

行为：
  - 调用 cad-file-reader 的 cad_statesync.py pull 拉取 cad-contract/v1。
  - 命中且契约包含可复用 detail 字段（text_records/geometry_segments）时，
    先把 detail.json / scan.json 落到 --out-dir，run_qty 建索引时会直接复用，
    不再调用底座重复解图。
  - 未命中 / bus 缺失 / 契约不含可复用 detail → 写 hit=false 状态并 exit 2/3；
    不再回退本机解图。
  - --require-core 为显式声明：土建的必选核心门槛（text_records + geometry_segments）
    默认已启用，该开关不改变行为，仅把核心口径显式暴露给调用方与文档。
  - 若 --out-dir/detail.json 已存在则不覆盖（幂等，保留已有解析）。
纯 stdlib、不联网；公司数据只落在 cad-file-reader 的 bus 本机状态文件。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path


def _default_cad_dir() -> Path:
    env = os.environ.get("CAD_SKILL_DIR")
    if env:
        return Path(env)
    cands = (
        Path.home() / ".codex" / "skills" / "cad-file-reader",
        Path.home() / ".claude" / "skills" / "cad-file-reader",
    )
    for c in cands:
        if (c / "scripts" / "cad_statesync.py").is_file():
            return c
    raise SystemExit("找不到 cad-file-reader（设 CAD_SKILL_DIR 指向其根目录）")


def _find_deps_shim(cad_dir: Path) -> Path:
    p = cad_dir / "scripts" / "cad_statesync.sh"
    if p.is_file():
        return p
    raise SystemExit(f"底座缺少 cad_statesync.sh：{cad_dir / 'scripts'}")


def _pull(cad_dir: Path, project: str, building: str, floor: str, entry_id: str) -> dict:
    shim = _find_deps_shim(cad_dir)
    cmd = ["bash", str(shim), "pull", "--project", project]
    if building:
        cmd += ["--building", building]
    if floor:
        cmd += ["--floor", floor]
    if entry_id:
        cmd += ["--entry-id", entry_id]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.stderr:
        print(r.stderr, file=sys.stderr, end="")
    if r.returncode != 0:
        # 拉取失败是降级信号，不阻断本技能
        return {"hit": False, "reason": f"cad_statesync pull 失败 rc={r.returncode}"}
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"hit": False, "reason": "cad_statesync pull 输出无法解析"}


def _usable(entry: dict, min_texts: int) -> tuple[bool, str]:
    if not isinstance(entry, dict):
        return False, "entry 非对象"
    if entry.get("schema") != "cad-contract/v1":
        return False, "schema 不是 cad-contract/v1"
    c = entry.get("contract")
    if not isinstance(c, dict):
        return False, "缺少 contract"
    texts = c.get("text_records")
    if not isinstance(texts, list):
        return False, "契约不含 text_records（无法重建 detail）"
    if len(texts) < min_texts:
        return False, f"text_records 过少（{len(texts)} < {min_texts}），避免用空契约代真图"
    if not isinstance(c.get("geometry_segments"), list) or not c.get("geometry_segments"):
        return False, "契约不含 geometry_segments（墙长/轴网缺料，仍回本机解析）"
    return True, "契约含 text_records + geometry_segments，可直接复用"


def _materialize(out_dir: Path, entry: dict) -> Path:
    c = entry["contract"]
    out_dir.mkdir(parents=True, exist_ok=True)
    detail = out_dir / "detail.json"
    if detail.exists():
        status = out_dir / "bus-pull-status.json"
        status.write_text(json.dumps({
            "hit": True, "reused": False,
            "reason": "out/detail.json 已存在，保留现有解析",
            "project_key": entry.get("project_key", {}).get("project", ""),
            "schema": entry.get("schema"),
            "contract_file": str(entry.get("source", {}).get("file", "")),
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        (out_dir / "contract.json").write_text(
            json.dumps(entry, ensure_ascii=False, indent=1), encoding="utf-8")
        return status
    detail.write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding="utf-8")
    (out_dir / "scan.json").write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding="utf-8")
    # 完整契约落盘：run_qty 直接把 contract.json 交给 qty_core
    (out_dir / "contract.json").write_text(
        json.dumps(entry, ensure_ascii=False, indent=1), encoding="utf-8")
    status = out_dir / "bus-pull-status.json"
    status.write_text(json.dumps({
        "hit": True, "reused": True,
        "project_key": entry.get("project_key", {}).get("project", ""),
        "schema": entry.get("schema"),
        "contract_file": str(entry.get("source", {}).get("file", "")),
        "written_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    return status


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="土建 run_qty 接入 lis-skill-bus 拉取")
    ap.add_argument("--project", required=True, help="项目标识")
    ap.add_argument("--building", default="", help="楼栋（可选）")
    ap.add_argument("--floor", default="", help="楼层（可选）")
    ap.add_argument("--out-dir", required=True, help="run_qty 输出目录（写入 detail.json）")
    ap.add_argument("--cad-skill-dir", default="", help="cad-file-reader 根目录")
    ap.add_argument("--entry-id", default="", help="指定 bus entry_id（默认最近一条）")
    ap.add_argument("--min-texts", type=int, default=1, help="text_records 下限，缺省 1")
    ap.add_argument("--require-core", action="store_true",
                    help="显式声明启用必选核心门槛（text_records+geometry_segments，土建默认已启用）")
    args = ap.parse_args(argv)

    cad_dir = Path(args.cad_skill_dir) if args.cad_skill_dir else _default_cad_dir()
    out_dir = Path(args.out_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    result = _pull(cad_dir, args.project, args.building, args.floor, args.entry_id)
    if not result.get("hit"):
        (out_dir / "bus-pull-status.json").write_text(
            json.dumps({"hit": False, "reason": result.get("reason", "无共享状态")},
                       ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"hit": False, "reason": result.get("reason", "无共享状态")},
                         ensure_ascii=False, indent=2))
        return 2
    entry = result.get("entry") or {}
    ok, why = _usable(entry, args.min_texts)
    if not ok:
        core_info = {"core_applied": True, "core_sections": ["text_records", "geometry_segments"]} if args.require_core else {}
        (out_dir / "bus-pull-status.json").write_text(
            json.dumps({"hit": True, "usable": False, "reason": why, **core_info},
                       ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"hit": True, "usable": False, "reason": why, **core_info},
                         ensure_ascii=False, indent=2))
        return 3
    status = _materialize(out_dir, entry)
    core_info = {"core_applied": True, "core_sections": ["text_records", "geometry_segments"]} if args.require_core else {}
    print(json.dumps({
        "hit": True, "usable": True,
        "detail": str(out_dir / "detail.json"),
        "scan": str(out_dir / "scan.json"),
        "status_file": str(status),
        "schema": entry.get("schema"),
        "project_key": entry.get("project_key", {}),
        **core_info,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
