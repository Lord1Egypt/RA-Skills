#!/usr/bin/env python3
# snap.py — 状态快照存档（V2）
# 备份范围（全量·运行期产物不按文件名枚举）：
#   - 状态: states/ 目录全部文件（快照内平铺）
#   - 场景: scenes/ 全目录（INDEX.md + 每个场景的 scene_state/pending_actions/narrative/scene_card/start_snapshot）
# 焦点场景唯一权威源 = world_state.yaml 顶层「焦点场景」（不再使用 .active 文件）
# 用法:
#   python3 scripts/snap.py <世界名> save [快照名]
#   python3 scripts/snap.py <世界名> load <快照名>
#   python3 scripts/snap.py <世界名> list
#   python3 scripts/snap.py <世界名> delete <快照名>
# 破坏性操作（load/delete）确认：交互终端提示 [y/N]（默认拒绝）；非交互环境（stdin 非 tty）需追加 --force 标志，否则拒绝执行。
import os, re, shutil, sys
from datetime import datetime
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        if _s and _s.encoding and _s.encoding.lower().replace("-", "") != "utf8":
            _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _paths import assert_no_links, resolve_world, safe_rmtree, validate_name

# 快照顶层除 states 平铺文件与 scenes/ 外还有 MANIFEST.md——恢复/对账时排除
SNAP_META = ["MANIFEST.md"]


def _states_files(d: Path) -> list[Path]:
    """目录下全部普通文件（含隐藏文件）·排除快照元数据"""
    if not d.is_dir():
        return []
    return sorted(f for f in d.iterdir() if f.is_file() and f.name not in SNAP_META)


def confirm_destructive(world: str, action: str, snapname: str, force: bool, prompt: str) -> None:
    if force:
        return
    if not sys.stdin.isatty():
        print(f"错误: 非交互环境执行破坏性操作需显式 --force 标志（python3 scripts/snap.py {world} {action} {snapname} --force）", file=sys.stderr)
        sys.exit(1)
    print(f"{prompt} [y/N] ", end="", flush=True)
    ans = sys.stdin.buffer.readline().decode("utf-8").strip()
    if ans.lower() in ("y", "yes"):
        return
    print("已取消")
    sys.exit(0)


def get_focus_scene(world_dir: Path) -> str:
    ws = world_dir / "states" / "world_state.yaml"
    try:
        for line in ws.read_text(encoding="utf-8").splitlines():
            if line.startswith("焦点场景:"):
                return re.sub(r"\s", "", re.sub(r"^焦点场景:\s*", "", line))
    except Exception:
        pass
    return ""


def get_focus_scene_name(world_dir: Path) -> str:
    scene_id = get_focus_scene(world_dir)
    if not scene_id:
        return ""
    cand = sorted((world_dir / "scenes").glob(scene_id + "-*"))
    return cand[0].name if cand else ""


def _rel_files(root: Path) -> list[str]:
    if not root.is_dir():
        return []
    out = []
    for dp, _dn, fn in os.walk(root):
        for f in fn:
            rel = os.path.relpath(Path(dp) / f, root).replace("\\", "/")
            out.append(rel)
    return sorted(out)


def main():
    argv = sys.argv[1:]
    world = argv[0] if len(argv) >= 1 else ""
    action = argv[1] if len(argv) >= 2 else ""
    snapname = ""
    force = False
    for a in argv[2:]:
        if a == "--force":
            force = True
        elif not snapname:
            snapname = a

    world_dir = resolve_world(world)
    snap_dir = world_dir / "snaps"
    archive_dir = world_dir / "archive" / "scenes"
    snap_dir.mkdir(parents=True, exist_ok=True)

    if action == "save":
        active = get_focus_scene(world_dir)
        if not snapname:
            active_name = get_focus_scene_name(world_dir)
            round_no = ""
            ws = world_dir / "states" / "world_state.yaml"
            try:
                for line in ws.read_text(encoding="utf-8").splitlines():
                    if line.startswith("轮次:"):
                        m = re.search(r"(\d+)", line)
                        if m:
                            round_no = m.group(1)
                        break
            except Exception:
                pass
            ts = datetime.now().strftime("%Y%m%d-%H%M%S")
            snapname = f"r{round_no}-{active_name}-{ts}" if round_no else f"{active_name}-{ts}"
            snapname = re.sub(r"--+", "-", snapname).strip("-")
            print(f"未指定存档名，自动生成: {snapname}")
        validate_name(snapname)
        assert_no_links(world_dir / "states")
        assert_no_links(world_dir / "scenes")
        outdir = snap_dir / snapname
        if outdir.exists():
            safe_rmtree(outdir)
        outdir.mkdir(parents=True)

        file_count = 0
        for f in _states_files(world_dir / "states"):
            shutil.copy2(f, outdir / f.name)
            file_count += 1
        if (world_dir / "scenes").is_dir():
            shutil.copytree(world_dir / "scenes", outdir / "scenes")
            file_count += len(_rel_files(outdir / "scenes"))

        manifest = outdir / "MANIFEST.md"
        lines = [f"# 存档清单: {snapname}", "", f"创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", f"来源世界: {world}"]
        if active:
            lines.append(f"焦点场景: {active} ({get_focus_scene_name(world_dir)})")
        lines += ["", "## 文件列表", ""]
        for rel in _rel_files(outdir):
            if rel == "MANIFEST.md":
                continue
            size = (outdir / rel).stat().st_size
            lines.append(f"- `{rel}` ({size} B)")
        manifest.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="")
        file_count += 1
        print(f"已保存快照: {snapname} ({file_count} 个文件，scenes 已全量备份)")

    elif action == "load":
        if not snapname:
            print("ERROR: 需要快照名称", file=sys.stderr); sys.exit(1)
        validate_name(snapname)
        srcdir = snap_dir / snapname
        if not srcdir.is_dir():
            print(f"ERROR: 快照 '{snapname}' 不存在", file=sys.stderr); sys.exit(1)
        assert_no_links(srcdir)
        assert_no_links(world_dir / "states")
        assert_no_links(world_dir / "scenes")
        assert_no_links(archive_dir)
        confirm_destructive(world, "load", snapname, force, f"载入快照 '{snapname}' 将覆盖当前世界状态（当前状态会自动备份到 _before_）")

        # 加载前自动备份当前状态
        bak_ts = str(int(datetime.now().timestamp()))
        bakdir = snap_dir / f"_before_{bak_ts}"
        bakdir.mkdir(parents=True)
        for f in _states_files(world_dir / "states"):
            shutil.copy2(f, bakdir / f.name)
        if (world_dir / "scenes").is_dir():
            shutil.copytree(world_dir / "scenes", bakdir / "scenes")
        print(f"当前状态已备份到: _before_{bak_ts}")

        restored = 0
        snap_states = _states_files(srcdir)
        for f in snap_states:
            shutil.copy2(f, world_dir / "states" / f.name)
            restored += 1
            print(f"  恢复: states/{f.name}")
        # 磁盘上有、快照中没有的状态文件 → 归档（防旧动态文件残留）
        if (world_dir / "states").is_dir():
            arc_names = {f.name for f in snap_states}
            ts = datetime.now().strftime("%Y%m%d-%H%M%S")
            for f in _states_files(world_dir / "states"):
                if f.name not in arc_names:
                    dst = archive_dir / f"load_extra_{ts}" / f.name
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    os.replace(str(f), str(dst))
                    print(f"  归档(存档无此文件): states/{f.name}")

        # ── 场景目录差异恢复 ──
        if (srcdir / "scenes").is_dir():
            (world_dir / "scenes").mkdir(parents=True, exist_ok=True)
            arc = _rel_files(srcdir / "scenes")
            disk = _rel_files(world_dir / "scenes")
            for rel in arc:
                dst = world_dir / "scenes" / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                if (srcdir / "scenes" / rel).is_file():
                    shutil.copy2(srcdir / "scenes" / rel, dst)
                    restored += 1
                    print(f"  恢复: scenes/{rel}")
            ts = datetime.now().strftime("%Y%m%d-%H%M%S")
            for rel in disk:
                if rel not in arc:
                    src = world_dir / "scenes" / rel
                    dst = archive_dir / ts / rel
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    os.replace(str(src), str(dst))
                    print(f"  归档(存档无此文件): scenes/{rel}")
            # 清理空目录（磁盘上被整体归档后留下的空壳）
            for dp, dn, _fn in sorted(os.walk(str(world_dir / "scenes")), reverse=True):
                p = Path(dp)
                if p == world_dir / "scenes":
                    continue
                if p.is_dir() and not any(p.iterdir()):
                    p.rmdir()

        # 清理遗留的 .active（已废弃——焦点场景唯一权威源 = world_state.yaml）
        if (world_dir / ".active").is_file():
            la = archive_dir / f"legacy_active_{int(datetime.now().timestamp())}"
            la.mkdir(parents=True)
            os.replace(str(world_dir / ".active"), str(la / ".active"))
            print("  已归档废弃文件: .active（焦点场景现由 world_state.yaml 顶层「焦点场景」管理）")

        print(f"已恢复快照: {snapname} ({restored} 个文件)")
        print(f"建议执行: python3 {Path(__file__).resolve().parent / 'worldctl.py'} {world} validate")

    elif action == "list":
        print(f"== {world} 的快照列表 ==")
        for d in sorted(snap_dir.glob("*/")):
            if not d.is_dir():
                continue
            name = d.name
            cnt = len(_rel_files(d))
            focus = get_focus_scene(d)
            print(f"  {name} ({cnt} 文件){(' [焦点: ' + focus + ']') if focus else ''}")

    elif action == "delete":
        if not snapname:
            print("ERROR: 需要快照名称", file=sys.stderr); sys.exit(1)
        validate_name(snapname)
        target = snap_dir / snapname
        if not target.is_dir():
            print(f"ERROR: 快照 '{snapname}' 不存在", file=sys.stderr); sys.exit(1)
        confirm_destructive(world, "delete", snapname, force, f"删除快照 '{snapname}' 不可恢复")
        safe_rmtree(target)
        print(f"已删除快照: {snapname}")

    else:
        print("用法: snap.py <世界名> save|load|delete [快照名]", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
