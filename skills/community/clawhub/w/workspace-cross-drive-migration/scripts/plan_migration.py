#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
迁移前体检（纯只读，不写任何文件、不改数据库）

用法：
  python plan_migration.py --source "D:\\Work\\项目A" --target "G:\\迁移备份\\项目A"
  python plan_migration.py --source ... --target ... --json plan.json

退出码：0 = 可迁移（可能有告警）；2 = 存在阻断项，不要继续。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ws_migrate_common as C  # noqa: E402


def analyse(source: str, target: str) -> dict:
    src = os.path.abspath(source)
    dst = os.path.abspath(target)
    res = {
        "source": src,
        "target": dst,
        "blockers": [],
        "warnings": [],
        "notes": [],
        "ok": True,
    }

    # ---- 源目录
    if not os.path.isdir(src):
        res["blockers"].append(f"源目录不存在或不是目录：{src}")
        res["ok"] = False
        return res

    src_stats = C.dir_stats(Path(src))
    res["source_stats"] = src_stats
    res["source_is_workspace"] = (Path(src) / ".workbuddy").is_dir()
    if not res["source_is_workspace"]:
        res["warnings"].append("源目录里没有 .workbuddy/，它可能不是 WorkBuddy 工作空间（普通目录也能搬，但不会有记忆/技能）")

    # ---- 目标目录
    if C.is_inside(dst, src):
        res["blockers"].append("目标目录在源目录内部，会自我复制，必须换位置")
    if C.is_inside(src, dst):
        res["blockers"].append("源目录在目标目录内部，必须换位置")
    if os.path.exists(dst):
        if os.path.isdir(dst) and not any(Path(dst).iterdir()):
            res["notes"].append("目标目录已存在但是空的，可以继续")
        else:
            res["blockers"].append(f"目标已存在且非空：{dst}（换一个目标名，或先手动清理）")
    parent = Path(dst).parent
    if not parent.exists():
        res["notes"].append(f"目标父目录不存在，执行时会自动创建：{parent}")

    vol = C.get_volume_info(dst)
    res["target_volume"] = {
        "root": vol["root"], "fs": vol["fs"], "free": vol["free"], "total": vol["total"]
    }
    if not vol["exists"]:
        res["blockers"].append(f"目标盘不存在（{vol['root']}）：移动硬盘没插好或盘符变了？")
    else:
        if vol["free"] is not None:
            need = int(src_stats["bytes"] * 1.15) + (64 << 20)
            res["required_bytes"] = need
            if vol["free"] < need:
                res["blockers"].append(
                    f"目标盘空间不足：需要约 {C.human_bytes(need)}，可用 {C.human_bytes(vol['free'])}"
                )
        fs = (vol["fs"] or "").upper()
        if fs in ("FAT32", "FAT"):
            res["blockers"].append("目标是 FAT32，单文件不能超过 4GB、也没有完整长路径支持，建议改用 NTFS/exFAT")
        elif fs == "EXFAT":
            res["warnings"].append("目标是 exFAT：不支持文件权限与符号链接，个别工具链（git/node_modules 软链）可能受影响")

    # ---- 长路径（Windows MAX_PATH）
    longest = src_stats["longest_rel"]
    if longest:
        projected = len(dst) + 1 + longest
        res["projected_longest_path"] = projected
        if projected > 240:
            res["warnings"].append(
                f"最长的相对路径搬到新位置后约 {projected} 字符，超过 240 有触发 MAX_PATH 限制的风险：{src_stats['longest_rel_path']}"
            )

    # ---- 链接点
    reparse = []
    for dirpath, dirnames, _ in os.walk(src):
        for d in dirnames:
            p = Path(dirpath) / d
            if C.is_reparse_point(p):
                reparse.append(str(p))
    if reparse:
        res["reparse_points"] = reparse[:20]
        res["warnings"].append(
            f"源目录里有 {len(reparse)} 个目录联接/符号链接，复制时会跳过链接本身（只复制真实内容）"
        )

    # ---- 嵌套工作空间
    nested = C.find_nested_workspaces(Path(src))
    if nested:
        res["nested_workspaces"] = nested[:20]
        res["warnings"].append(
            f"源目录内部还嵌着 {len(nested)} 个独立工作空间，它们会跟着一起搬，但各自的会话历史需要单独迁"
        )

    markers = C.find_repo_markers(Path(src))
    if markers:
        res["repo_markers"] = markers[:20]
        res["notes"].append(f"检测到 {len(markers)} 个 .git / node_modules / venv 等目录，会原样复制（体积可能很大）")

    # ---- 会话历史与登记信息
    old_slug = C.slug_for_path(src)
    new_slug = C.slug_for_path(dst)
    res["old_slug"] = old_slug
    res["new_slug"] = new_slug
    old_proj = C.PROJECTS_DIR / old_slug
    new_proj = C.PROJECTS_DIR / new_slug
    res["projects_dir_old"] = str(old_proj)
    res["projects_dir_old_exists"] = old_proj.is_dir()
    if not old_proj.is_dir():
        res["warnings"].append(
            f"没找到会话历史目录 projects/{old_slug}：这个工作空间可能从没在这台机器上开过，或路径大小写不同"
        )
    else:
        jsonl = list(old_proj.rglob("*.jsonl"))
        res["session_files"] = len(jsonl)
        res["session_bytes"] = sum(f.stat().st_size for f in jsonl if f.is_file())
        res["notes"].append(f"会话历史 {len(jsonl)} 个 jsonl，共 {C.human_bytes(res['session_bytes'])}")
    if new_proj.exists():
        if old_slug != new_slug:
            res["blockers"].append(
                f"目标 slug 的会话历史目录已存在：projects/{new_slug}，说明新位置以前被用过，需要先清理"
            )

    entry = C.display_name_entry(src)
    if entry:
        res["display_name"] = entry.get("displayName")
        res["notes"].append(f"侧边栏显示名：{entry.get('displayName')}")
    else:
        res["display_name"] = Path(src).name
        res["notes"].append("侧边栏没有登记显示名（不影响迁移）")

    snap = C.db_snapshot(C.DB_PATH, src)
    res["db"] = snap
    if not snap["ok"]:
        res["warnings"].append(f"读数据库失败：{snap['error']}")
    else:
        total_rows = snap["workspaces"] + snap["sessions"] + snap["automations"] + snap["trust"]
        res["notes"].append(
            f"数据库待改：工作空间 {snap['workspaces']} 行 / 会话 {snap['sessions']} 行 / "
            f"自动化 {snap['automations']} 条 / 信任记录 {snap['trust']} 条"
        )
        if snap["automations"]:
            res["warnings"].append(
                f"有 {snap['automations']} 个自动化任务绑定在这个工作空间上，迁移后必须改路径，否则下次触发会失败"
            )

    procs = C.running_app_processes()
    res["running_processes"] = procs
    if procs:
        res["notes"].append(
            "检测到 WorkBuddy 正在运行。文件复制可以在运行中做；改数据库前必须完全退出应用（含托盘）"
        )

    res["ok"] = not res["blockers"]
    return res


def render(res: dict) -> None:
    C.hr("工作空间迁移体检")
    print(f"  源：{res['source']}")
    print(f"  ->  {res['target']}")
    if "source_stats" in res:
        s = res["source_stats"]
        print(f"  体积：{s['files']} 个文件 / {C.human_bytes(s['bytes'])}")
        print(f"  slug：{res['old_slug']}  ->  {res['new_slug']}")
        vol = res.get("target_volume") or {}
        if vol.get("exists"):
            print(f"  目标盘：{vol['root']}  文件系统 {vol['fs'] or '未知'}  可用 {C.human_bytes(vol['free'] or 0)}")

    if res.get("notes"):
        C.hr("信息")
        for n in res["notes"]:
            print(f"  - {n}")

    if res.get("warnings"):
        C.hr("告警（不阻断，但要知道）")
        for w in res["warnings"]:
            C.warn(w)

    C.hr("结论")
    if res["ok"]:
        C.ok("可以做。下一步：apply_migration.py（先不加 --apply 看一遍流程，再加 --apply 真跑）")
    else:
        C.bad("有阻断项，先解决再动手：")
        for b in res["blockers"]:
            print(f"         - {b}")


def main() -> int:
    ap = argparse.ArgumentParser(description="WorkBuddy 工作空间迁移前体检（只读）")
    ap.add_argument("--source", required=True, help="现有工作空间绝对路径")
    ap.add_argument("--target", required=True, help="迁移后的绝对路径")
    ap.add_argument("--json", help="把体检结果写成 JSON 文件")
    args = ap.parse_args()

    res = analyse(args.source, args.target)
    render(res)
    if args.json:
        C.save_json(Path(args.json), res)
        print(f"\n  体检结果已写入：{args.json}")
    return 0 if res["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
