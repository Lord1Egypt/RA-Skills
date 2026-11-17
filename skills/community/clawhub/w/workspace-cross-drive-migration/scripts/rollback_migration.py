#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
回滚一次迁移（默认只演练，加 --apply 执行）

用法：
  python rollback_migration.py --state "<状态目录>"            # 演练
  python rollback_migration.py --state "<状态目录>" --apply    # 执行
  python rollback_migration.py --latest --apply                # 回滚最近一次

回滚原则：只做「改名 / 改回路径 / 还原备份」，绝不删除任何文件。
目标目录不会被删，只会被改名成 <名字>.rolledback-<时间戳>，你自己看过再删。
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ws_migrate_common as C  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="回滚工作空间迁移（默认演练）")
    ap.add_argument("--state", help="迁移状态目录或 state.json")
    ap.add_argument("--latest", action="store_true", help="回滚最近一次迁移")
    ap.add_argument("--apply", action="store_true", help="真的执行")
    args = ap.parse_args()

    if args.latest:
        state = C.latest_state()
        if not state:
            print("没有找到任何迁移记录。")
            return 1
    elif args.state:
        state = C.load_state(args.state)
    else:
        ap.error("需要 --state 或 --latest")

    src = state["source"]
    dst = state["target"]
    old_slug, new_slug = state["old_slug"], state["new_slug"]
    backup = Path(state["backup_dir"])
    ts = C.stamp()

    C.hr("回滚计划")
    print(f"  迁移记录：{state['created_at']}  (id={state.get('id')})")
    print(f"  新位置  {dst}")
    print(f"  回退到  {src}")
    steps = [
        f"数据库改回旧路径（{new_slug} -> {old_slug}）",
        f"侧边栏显示名挂回旧路径",
        f"会话记录里的路径改回旧路径，projects 目录名改回 {old_slug}",
        f"源目录若已隔离，改回原名" if state.get("source_isolated") else "源目录未被隔离，无需还原",
        f"新位置目录改名为 {Path(dst).name}.rolledback-{ts}（不删除）",
    ]
    for i, s in enumerate(steps, 1):
        print(f"  {i}. {s}")

    if not args.apply:
        C.hr("演练结束")
        C.warn("什么都没改。确认后加 --apply 执行。")
        return 0

    C.hr("1/5 数据库改回旧路径")
    rep = C.db_patch(C.DB_PATH, dst, src)
    if rep["applied"]:
        state["db_patched"] = False
        C.ok(f"workspaces {rep['workspaces']} / sessions {rep['sessions']} / "
             f"automations {rep['automations']} / trust {rep['trust']}")
    else:
        C.warn(f"数据库暂时改不了：{rep['error']}")
        print("         完全退出 WorkBuddy 后再重跑本命令即可；其它步骤照常执行。")

    C.hr("2/5 侧边栏显示名")
    data = C.load_json(C.DISPLAY_NAMES, None)
    if isinstance(data, dict):
        ws = data.setdefault("workspaces", {})
        entry = ws.pop(C.display_key(dst), None)
        if entry:
            key = C.display_key(src)
            ws[key] = {
                "id": key,
                "path": os.path.abspath(src).replace("\\", "/"),
                "displayName": entry.get("displayName") or Path(src).name,
                "updatedAt": C.now_ms(),
            }
            C.save_json(C.DISPLAY_NAMES, data)
            C.ok(f"显示名「{ws[key]['displayName']}」已挂回旧路径")
        else:
            C.warn("新路径没有显示名记录，跳过")

    C.hr("3/5 会话记录与目录名")
    import apply_migration  # 复用改写函数

    new_proj = C.PROJECTS_DIR / new_slug
    old_proj = C.PROJECTS_DIR / old_slug
    if new_proj.is_dir():
        r = apply_migration.rewrite_jsonl_files(new_proj, dst, src, state)
        C.ok(f"改写 {r['files']} 个 jsonl，共 {r['lines_changed']} 处")
        if old_proj.exists():
            aside = C.PROJECTS_DIR / f"{old_slug}.rolledback-{ts}"
            os.rename(new_proj, aside)
            C.warn(f"旧目录已存在，新目录改名放到 {aside.name}")
        else:
            os.rename(new_proj, old_proj)
            C.ok(f"projects/{new_slug} -> projects/{old_slug}")
    elif (backup / "projects-old").is_dir():
        shutil.copytree(backup / "projects-old", old_proj, dirs_exist_ok=True)
        C.ok("已从备份还原会话历史目录")
    else:
        C.warn("没有可还原的会话历史目录")

    C.hr("4/5 源目录")
    iso = state.get("source_isolated")
    if iso and os.path.isdir(iso) and not os.path.exists(src):
        os.rename(iso, src)
        state["source_isolated"] = None
        C.ok(f"已改回：{src}")
    elif iso:
        C.warn(f"隔离目录状态异常：{iso}")
    else:
        C.ok("源目录本来就没动")

    C.hr("5/5 新位置目录")
    if os.path.isdir(dst):
        aside = f"{dst}.rolledback-{ts}"
        try:
            os.rename(dst, aside)
            C.ok(f"已改名：{aside}")
            C.warn("确认数据已回旧位置后再手动删除这个目录。")
        except OSError as e:
            C.warn(f"改名失败（可能被占用）：{e}")
    else:
        C.warn("新位置目录不存在，跳过")

    state["status"] = "rolled-back"
    C.save_state(state)
    C.hr("回滚完成")
    print("  重启 WorkBuddy，打开旧路径确认历史与记忆都在。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
