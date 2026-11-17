#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
执行迁移：带 --apply 才真正动手，不加只打印将要做的步骤（默认演练）。

用法：
  python apply_migration.py --source "D:\\Work\\项目A" --target "G:\\迁移\\项目A"           # 演练
  python apply_migration.py --source "..." --target "..." --apply                        # 真跑
  python apply_migration.py --source "..." --target "..." --apply --skip-db              # 先不动数据库
  python apply_migration.py --state "<状态目录>" --db-only                               # 退出应用后补改数据库
  python apply_migration.py --source "..." --target "..." --apply --isolate-source       # 源目录改名隔离

做的事（顺序不能换）：
  1) 备份元数据（会话历史目录、数据库、显示名文件）
  2) 复制工作空间本体
  3) 校验文件数/字节数
  4) projects/<旧slug> 改名为 <新slug>
  5) 改写 jsonl 内的绝对路径（逐行 json.loads 校验）
  6) 改写 .workbuddy 内的 md/json 文本引用（可用 --no-rewrite-docs 关掉）
  7) workspace-display-names.json 换键
  8) 数据库四张表改路径（应用在跑时会排队，锁死就给出补改命令）
  9) 可选：把源目录改名隔离（不删除，随时可回滚）
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ws_migrate_common as C  # noqa: E402


# ------------------------------------------------------------------ 复制

def copy_tree(src: str, dst: str) -> tuple[bool, str]:
    """优先 robocopy（保留时间戳、跳过链接），非 Windows 退回 copytree。"""
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    if os.name != "nt":
        shutil.copytree(src, dst, symlinks=True)
        return True, "copytree"

    cmd = [
        "robocopy", src, dst,
        "/E",            # 含空目录
        "/COPY:DAT",     # 数据+属性+时间戳
        "/DCOPY:DAT",
        "/XJ",           # 跳过 junction，避免环
        "/R:2", "/W:2",  # 失败重试 2 次，每次等 2 秒
        "/NFL", "/NDL", "/NJH", "/NJS", "/NP",
    ]
    proc = subprocess.run(cmd, capture_output=True, check=False)
    out = (proc.stdout or b"").decode("mbcs", errors="replace")
    err = (proc.stderr or b"").decode("mbcs", errors="replace")
    # robocopy: 0-7 都算成功（1=有文件被复制，2=有额外项，3=1+2）
    if proc.returncode >= 8:
        return False, f"robocopy 退出码 {proc.returncode}\n{out[-800:]}\n{err[-400:]}"
    return True, f"robocopy rc={proc.returncode}"


# ------------------------------------------------------------------ 各步骤

def rewrite_jsonl_files(project_dir: Path, old: str, new: str, state: dict) -> dict:
    """改写会话历史 jsonl，逐行校验 JSON 结构。"""
    result = {"files": 0, "lines_changed": 0, "errors": []}
    for f in sorted(C.iter_files(project_dir)):
        if f.suffix.lower() != ".jsonl":
            continue
        try:
            raw = f.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            raw = f.read_text(encoding="utf-8", errors="surrogateescape")
        if C.count_occurrences(raw, old) == 0:
            continue
        new_lines = []
        changed = 0
        broken = False
        for line in raw.splitlines():
            if not line.strip():
                new_lines.append(line)
                continue
            rewritten, n = C.rewrite_text(line, old, new)
            if n:
                try:
                    json.loads(rewritten)
                except Exception as e:  # 宁可原样保留，也不写坏历史
                    result["errors"].append(f"{f.name}: {e}")
                    broken = True
                    new_lines.append(line)
                    continue
                changed += n
            new_lines.append(rewritten)
        if broken:
            continue
        backup = Path(state["_state_dir"]) / "backup" / "jsonl" / f.name
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, backup)
        with open(f, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(new_lines) + ("\n" if raw.endswith("\n") else ""))
        result["files"] += 1
        result["lines_changed"] += changed
    return result


def rewrite_docs(root: Path, old: str, new: str, state: dict | None = None) -> dict:
    """
    改写 .workbuddy 下 md/json/txt 里的路径引用（记忆文件里常写着绝对路径）。

    两道保险：
      1) 用 iter_files 遍历，跳过 junction/符号链接，避免顺着链接写到工作空间外面；
      2) 每个文件再校验一次真实路径必须落在工作空间内，改前复制进备份区。
    """
    result = {"files": 0, "hits": 0, "errors": [], "skipped_outside": 0}
    base = root / ".workbuddy"
    if not base.is_dir():
        return result
    root_real = os.path.realpath(str(root))
    backup_root = None
    if state:
        backup_root = Path(state["_state_dir"]) / "backup" / "docs"
    for f in C.iter_files(base):
        if f.suffix.lower() not in (".md", ".json", ".txt", ".yaml", ".yml"):
            continue
        real = os.path.realpath(str(f))
        if not (real == root_real or real.startswith(root_real + os.sep)):
            result["skipped_outside"] += 1
            continue
        try:
            if f.stat().st_size > 8 << 20:
                continue
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if C.count_occurrences(text, old) == 0:
            continue
        rewritten, n = C.rewrite_text(text, old, new)
        if f.suffix.lower() == ".json":
            try:
                json.loads(rewritten)
            except Exception as e:
                result["errors"].append(f"{f}: {e}")
                continue
        if backup_root is not None:
            try:
                dest = backup_root / f.relative_to(root)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dest)
            except OSError as e:
                result["errors"].append(f"{f}: 备份失败 {e}")
                continue
        try:
            f.write_text(rewritten, encoding="utf-8", newline="\n")
        except OSError as e:
            result["errors"].append(f"{f}: {e}")
            continue
        result["files"] += 1
        result["hits"] += n
    return result


def move_display_entry(old: str, new: str) -> dict:
    data = C.load_json(C.DISPLAY_NAMES, None)
    if not isinstance(data, dict):
        return {"updated": False, "reason": "显示名文件不存在或格式异常"}
    workspaces = data.setdefault("workspaces", {})
    old_key = C.display_key(old)
    new_key = C.display_key(new)
    entry = workspaces.get(old_key) or {}
    name = entry.get("displayName") or Path(old).name
    workspaces.pop(old_key, None)
    workspaces[new_key] = {
        "id": new_key,
        "path": os.path.abspath(new).replace("\\", "/"),
        "displayName": name,
        "updatedAt": C.now_ms(),
    }
    C.save_json(C.DISPLAY_NAMES, data)
    return {"updated": True, "displayName": name, "key": new_key}


# ------------------------------------------------------------------ 主流程

def run(args) -> int:
    src = os.path.abspath(args.source)
    dst = os.path.abspath(args.target)

    import plan_migration  # 复用体检逻辑
    plan = plan_migration.analyse(src, dst)
    if not plan["ok"]:
        plan_migration.render(plan)
        print("\n有阻断项，已停止。")
        return 2

    C.hr("迁移计划")
    print(f"  源        {src}")
    print(f"  目标      {dst}")
    print(f"  会话历史  {plan['old_slug']}  ->  {plan['new_slug']}")
    print(f"  体积      {plan['source_stats']['files']} 文件 / {C.human_bytes(plan['source_stats']['bytes'])}")
    steps = [
        "备份元数据（会话历史目录 / workbuddy.db / workspace-display-names.json）",
        "复制工作空间本体",
        "校验文件数与字节数",
        "projects/<旧slug> 改名为 <新slug>",
        "改写 jsonl 内绝对路径（逐行 JSON 校验）",
        "改写 .workbuddy 内 md/json 的路径引用" if not args.no_rewrite_docs else "（跳过）改写 .workbuddy 文本引用",
        "workspace-display-names.json 换键并保留显示名",
        "数据库四张表改路径" if not args.skip_db else "（跳过）数据库改路径 —— 稍后用 --db-only 补",
    ]
    for i, step in enumerate(steps, 1):
        print(f"  {i}. {step}")
    print(f"  +. " + ("隔离源目录（改名，不删除）" if args.isolate_source else "源目录原样保留（默认，推荐）"))

    if not args.apply:
        C.hr("演练结束")
        C.warn("这是演练，什么都没改。确认无误后加 --apply 再跑一次。")
        return 0

    # ---- 建状态与备份
    state_dir = C.new_state_dir(src, dst)
    state = C.load_state(state_dir)
    state["status"] = "running"
    C.save_state(state)
    backup_dir = Path(state["backup_dir"])
    backup_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n  迁移状态目录：{state_dir}")

    old_slug, new_slug = plan["old_slug"], plan["new_slug"]
    old_proj = C.PROJECTS_DIR / old_slug
    new_proj = C.PROJECTS_DIR / new_slug

    if old_proj.is_dir():
        shutil.copytree(old_proj, backup_dir / "projects-old", dirs_exist_ok=True)
        C.log_step(state, "备份会话历史目录", True, str(backup_dir / "projects-old"))
        C.ok(f"已备份会话历史 -> {backup_dir / 'projects-old'}")
    if C.DB_PATH.exists():
        shutil.copy2(C.DB_PATH, backup_dir / "workbuddy.db")
        for extra in ("workbuddy.db-wal", "workbuddy.db-shm"):
            p = C.APP_ROOT / extra
            if p.exists():
                shutil.copy2(p, backup_dir / extra)
        C.log_step(state, "备份数据库", True, str(backup_dir / "workbuddy.db"))
        C.ok(f"已备份数据库 -> {backup_dir / 'workbuddy.db'}")
    if C.DISPLAY_NAMES.exists():
        shutil.copy2(C.DISPLAY_NAMES, backup_dir / "workspace-display-names.json")
        C.log_step(state, "备份显示名文件", True, "")
        C.ok("已备份 workspace-display-names.json")

    # ---- 复制
    C.hr("1/8 复制工作空间")
    copied, detail = copy_tree(src, dst)
    if not copied:
        C.bad(f"复制失败：{detail}")
        C.log_step(state, "复制工作空间", False, detail)
        state["status"] = "failed"
        C.save_state(state)
        return 3
    C.ok(f"复制完成（{detail}）")
    C.log_step(state, "复制工作空间", True, detail)

    # ---- 校验
    C.hr("2/8 校验复制完整性")
    a = C.dir_stats(Path(src))
    b = C.dir_stats(Path(dst))
    print(f"  源  {a['files']} 文件 / {C.human_bytes(a['bytes'])}")
    print(f"  新  {b['files']} 文件 / {C.human_bytes(b['bytes'])}")
    if a["files"] != b["files"] or a["bytes"] != b["bytes"]:
        partial = f"{dst}.partial-{C.stamp()}"
        try:
            os.rename(dst, partial)
        except OSError:
            partial = dst
        C.bad(f"文件数或字节数不一致，已停止。目标目录：{partial}")
        C.warn("源目录没有动过，可以放心删掉上面的不完整副本后重试。")
        state["status"] = "failed"
        C.log_step(state, "校验复制完整性", False, "数量不一致")
        C.save_state(state)
        return 4
    C.ok("文件数与字节数一致")
    C.log_step(state, "校验复制完整性", True, "")

    # ---- 会话历史目录改名
    C.hr("3/8 会话历史目录改名")
    if old_proj.is_dir():
        if new_proj.exists():
            C.bad(f"目标会话目录已存在：{new_proj}")
            state["status"] = "failed"
            C.save_state(state)
            return 5
        os.rename(old_proj, new_proj)
        C.ok(f"{old_slug}  ->  {new_slug}")
        C.log_step(state, "会话历史目录改名", True, new_slug)
    else:
        C.warn("没有旧会话目录，跳过（这个工作空间可能没在本机开过）")
        C.log_step(state, "会话历史目录改名", True, "旧目录不存在")

    # ---- 改写 jsonl
    C.hr("4/8 改写会话记录内的路径")
    if new_proj.is_dir():
        r = rewrite_jsonl_files(new_proj, src, dst, state)
        C.ok(f"改写了 {r['files']} 个 jsonl，共 {r['lines_changed']} 处路径")
        for e in r["errors"][:5]:
            C.warn(f"跳过一行（JSON 校验失败，原样保留）：{e}")
        C.log_step(state, "改写 jsonl 路径", not r["errors"], json.dumps(r, ensure_ascii=False)[:300])
    else:
        C.warn("无会话记录可改")

    # ---- 改写文档
    C.hr("5/8 改写 .workbuddy 内的路径引用")
    if args.no_rewrite_docs:
        C.warn("已按 --no-rewrite-docs 跳过")
    else:
        d = rewrite_docs(Path(dst), src, dst, state)
        C.ok(f"改写 {d['files']} 个文件，共 {d['hits']} 处引用")
        if d.get("skipped_outside"):
            C.warn(f"跳过 {d['skipped_outside']} 个指向工作空间外的链接文件（不越界改写）")
        for e in d["errors"][:5]:
            C.warn(f"跳过：{e}")
        C.log_step(state, "改写文档路径引用", not d["errors"], json.dumps(d, ensure_ascii=False)[:300])

    # ---- 显示名
    C.hr("6/8 侧边栏显示名")
    dn = move_display_entry(src, dst)
    if dn.get("updated"):
        C.ok(f"显示名「{dn['displayName']}」已挂到新路径")
    else:
        C.warn(str(dn.get("reason")))
    C.log_step(state, "更新显示名", bool(dn.get("updated")), json.dumps(dn, ensure_ascii=False))

    # ---- 数据库
    C.hr("7/8 数据库改路径")
    if args.skip_db:
        C.warn("已按 --skip-db 跳过。稍后完全退出 WorkBuddy，再执行：")
        print(f"         python apply_migration.py --state \"{state_dir}\" --db-only --apply")
    else:
        rep = C.db_patch(C.DB_PATH, src, dst)
        if rep["applied"]:
            state["db_patched"] = True
            C.ok(
                f"已改：workspaces {rep['workspaces']} 行 / sessions {rep['sessions']} 行 / "
                f"automations {rep['automations']} 条 / trust {rep['trust']} 条"
            )
            C.log_step(state, "数据库改路径", True, json.dumps(rep, ensure_ascii=False))
        else:
            C.warn(f"数据库暂时改不了：{rep['error']}")
            print("         应用正在占用数据库属于正常现象。请完全退出 WorkBuddy（含托盘），再执行：")
            print(f"         python apply_migration.py --state \"{state_dir}\" --db-only --apply")
            C.log_step(state, "数据库改路径", False, rep.get("error") or "")

    # ---- 隔离源目录
    C.hr("8/8 源目录处理")
    if args.isolate_source:
        isolated = f"{src}.migrated-{C.stamp()}"
        try:
            os.rename(src, isolated)
            state["source_isolated"] = isolated
            C.ok(f"源目录已改名隔离：{isolated}")
            C.warn("确认新位置一切正常后，再手动删除这个隔离目录；出问题就用 rollback 改回来。")
        except OSError as e:
            C.warn(f"改名失败（可能有程序占用）：{e}")
    else:
        C.warn("源目录原样保留。确认新位置正常后再自行处理，别急着删。")

    state["status"] = "done" if state.get("db_patched") or args.skip_db else "done-db-pending"
    C.save_state(state)

    C.hr("完成")
    print("  接着做这几件事：")
    print("   1. 完全退出 WorkBuddy 并从托盘确认已退出，然后重新启动")
    print(f"   2. 打开新路径：{dst}")
    print("   3. 核对三样：侧边栏还在的会话历史、.workbuddy/memory 里的记忆、项目级 skills")
    print("   4. 观察一周再删源目录（或 rollback 随时可退）")
    print(f"\n  状态文件：{state_dir / 'state.json'}")
    return 0


def run_db_only(args) -> int:
    state = C.load_state(args.state)
    src, dst = state["source"], state["target"]
    C.hr("只改数据库")
    snap_old = C.db_snapshot(C.DB_PATH, src)
    snap_new = C.db_snapshot(C.DB_PATH, dst)
    print(f"  将把指向旧路径的记录改到新路径：")
    print(f"    workspaces {snap_old['workspaces']} 行（新路径已有 {snap_new['workspaces']} 行）")
    print(f"    sessions   {snap_old['sessions']} 行（新路径已有 {snap_new['sessions']} 行）")
    print(f"    automations {snap_old['automations']} 条")
    print(f"    信任记录   {snap_old['trust']} 条")
    if not args.apply:
        C.warn("这是预览，什么都没改。确认后在这条命令末尾加 --apply。")
        return 0
    rep = C.db_patch(C.DB_PATH, src, dst)
    if rep["applied"]:
        state["db_patched"] = True
        C.save_state(state)
        C.ok(
            f"workspaces {rep['workspaces']} / sessions {rep['sessions']} / "
            f"automations {rep['automations']} / trust {rep['trust']}"
        )
        return 0
    C.bad(f"仍然改不了：{rep['error']}")
    print("  请确认 WorkBuddy 已经完全退出（任务管理器里没有 WorkBuddy 进程）后重试。")
    return 6


def main() -> int:
    ap = argparse.ArgumentParser(description="WorkBuddy 工作空间跨盘迁移（默认演练）")
    ap.add_argument("--source", help="现有工作空间绝对路径")
    ap.add_argument("--target", help="迁移后的绝对路径")
    ap.add_argument("--apply", action="store_true", help="真的执行（不加只演练）")
    ap.add_argument("--skip-db", action="store_true", help="跳过数据库改路径")
    ap.add_argument("--no-rewrite-docs", action="store_true", help="不改 .workbuddy 内文本的路径引用")
    ap.add_argument("--isolate-source", action="store_true", help="迁移后把源目录改名隔离（不删除）")
    ap.add_argument("--db-only", action="store_true", help="只对已有迁移状态补改数据库")
    ap.add_argument("--state", help="迁移状态目录或 state.json 路径")
    args = ap.parse_args()

    if args.db_only:
        if not args.state:
            ap.error("--db-only 需要 --state")
        return run_db_only(args)

    if not args.source or not args.target:
        ap.error("需要 --source 和 --target")
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
