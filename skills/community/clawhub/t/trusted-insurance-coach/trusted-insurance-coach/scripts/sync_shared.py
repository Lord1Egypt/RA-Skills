#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_shared.py — 把包根 shared/ 与 compliance_scan.py 同步到各 skill 的内嵌副本

为什么要有内嵌副本：
  WB 上既可以整包装，也可能单独装某一个 skill。
  单个 skill 被单独安装时，`../../shared/` 会断链，所以每个 skill 内带一份 `shared/` 与
  `scripts/compliance_scan.py`。包根是**唯一权威源**，本脚本负责下发。

用法：
    python3 scripts/sync_shared.py            # 从包根下发到 5 个 skill
    python3 scripts/sync_shared.py --check    # 只检查是否一致（CI / 发布前用）

退出码：0 = 一致（或已同步）；1 = --check 时发现不一致
"""

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 需要下发的共享文件（相对包根）
SHARED_FILES = [
    "shared/insurance_abc.md",
    "shared/pitfalls_10.md",
    "shared/budget_design.md",
    "shared/takeaway_3_forms.md",
]
# 需要下发的脚本
SCRIPT_FILES = ["scripts/compliance_scan.py"]


def skill_dirs():
    base = ROOT / "skills"
    return sorted(p for p in base.iterdir() if p.is_dir() and (p / "SKILL.md").exists())


def run(check_only=False):
    diffs, synced = [], 0
    for rel in SHARED_FILES + SCRIPT_FILES:
        src = ROOT / rel
        if not src.exists():
            print(f"[错误] 权威源不存在：{rel}", file=sys.stderr)
            return 1
        for sd in skill_dirs():
            # shared/*.md → <skill>/shared/*.md ；scripts/x.py → <skill>/scripts/x.py
            dst = sd / rel if rel.startswith("shared/") else sd / "scripts" / Path(rel).name
            if dst.exists() and filecmp.cmp(src, dst, shallow=False):
                continue
            if check_only:
                diffs.append(f"{sd.name}: {dst.relative_to(ROOT)} 不一致")
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                synced += 1
    if check_only:
        if diffs:
            print("❌ 内嵌副本与权威源不一致（{} 处）：".format(len(diffs)))
            for d in diffs:
                print("   ·", d)
            print("\n运行  python3 scripts/sync_shared.py  修复。")
            return 1
        print(f"✅ 全部一致（{len(SHARED_FILES) + len(SCRIPT_FILES)} 个文件 × {len(skill_dirs())} 个 skill）")
        return 0
    print(f"✅ 已同步 {synced} 个文件到 {len(skill_dirs())} 个 skill")
    return 0


def main():
    ap = argparse.ArgumentParser(description="同步共享知识库到各 skill 内嵌副本")
    ap.add_argument("--check", action="store_true", help="只检查一致性，不写入")
    return run(check_only=ap.parse_args().check)


if __name__ == "__main__":
    sys.exit(main())
