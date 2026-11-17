#!/usr/bin/env python3
# reset_scene.py — 场景级回退（L3）：重置指定场景到「start_snapshot 状态」（清空场景内动态叙事·不撤销世界进度）
# 用法: python3 scripts/reset_scene.py <世界名> [<场景ID>] [--force]
#   <场景ID> 缺省 = 当前焦点场景（world_state.焦点场景）；支持短 ID（S05）或完整目录名
# 回退体系：L1 世界级 snap.py load（快照·主动存档）/ L2 场景级本脚本 / L3 手工重建（详见 references/rollback.md）
# 破坏性操作（重置前自动存档·可回滚；存档失败即中止）：
#   - narrative.md → 轮转归档为 narrative.r{轮次}.<时间戳>.md（保留历史叙事·轮次=叙事内容首行或 world_state 顶层轮次·无轮次时纯时间戳），新 narrative.md 置空
#   - scene_state.yaml：场景时间线 → ''；核心状态 → 待填充占位（按 start_snapshot.md 恢复开场状态）
#   - 静态基线保留：物理锚点/道具/关键场景信息/出场角色摘要（场景物理定义，不因重置销毁）
#   - world_state 时间/轮次回退至场景开场（start_snapshot 冻结时间/开场轮次）——「时间只增不减」只约束正常推进·显式重置是主动回退例外
# 重置后：按 start_snapshot.md 重新填充 scene_state 核心状态并继续叙事（世界时间/轮次已与场景开场一致）
# 确认：交互终端提示 [y/N]（默认拒绝）；非交互环境（stdin 非 tty）需追加 --force 标志，否则拒绝执行。
import os, re, sys, yaml
from datetime import datetime, timezone
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        if _s and _s.encoding and _s.encoding.lower().replace("-", "") != "utf8":
            _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _paths import assert_no_links, resolve_world, snapshot_or_abort, validate_name


def main():
    argv = sys.argv[1:]
    world = argv[0] if len(argv) >= 1 else ""
    scene_id = ""
    force = False
    for a in argv[1:]:
        if a == "--force":
            force = True
        elif not scene_id:
            scene_id = a

    if not world:
        print("用法: python3 scripts/reset_scene.py <世界名> [<场景ID>] [--force]", file=sys.stderr)
        sys.exit(1)
    world_dir = resolve_world(world)
    assert_no_links(world_dir / "states")
    assert_no_links(world_dir / "scenes")

    # ── 解析场景目录（缺省=焦点场景；短 ID 前缀匹配完整目录名）──
    scene_dir = None
    if scene_id:
        validate_name(scene_id, "场景 ID")
        if (world_dir / "scenes" / scene_id).is_dir():
            scene_dir = world_dir / "scenes" / scene_id
        else:
            cand = sorted((world_dir / "scenes").glob(scene_id + "-*"))
            scene_dir = cand[0] if cand else None
    else:
        ws = world_dir / "states" / "world_state.yaml"
        if ws.is_file():
            try:
                for line in ws.read_text(encoding="utf-8").splitlines():
                    if line.startswith("焦点场景:"):
                        focus = re.sub(r"^焦点场景:\s*", "", line).strip()
                        if focus:
                            cand = sorted((world_dir / "scenes").glob(focus + "-*"))
                            scene_dir = cand[0] if cand else None
                        break
            except Exception:
                pass
    if not scene_dir or not scene_dir.is_dir():
        print(f"[ERR] 场景不存在: {scene_id or '<焦点场景>'}（检查 scenes/ 目录与 world_state.焦点场景）", file=sys.stderr)
        sys.exit(1)
    scene_base = scene_dir.name

    # 破坏性操作确认：--force 直过；交互终端提示 [y/N]（默认拒绝）；非交互且无 --force → 拒绝执行
    if not force:
        if not sys.stdin.isatty():
            print(f"错误: 非交互环境执行场景重置需显式 --force 标志（python3 scripts/reset_scene.py {world} {scene_id} --force）", file=sys.stderr)
            sys.exit(1)
        print(f"重置场景 '{scene_base}' 到 start_snapshot 状态（清空动态叙事·自动存档可回滚）[y/N] ", end="", flush=True)
        ans = sys.stdin.buffer.readline().decode("utf-8").strip()
        if ans.lower() not in ("y", "yes"):
            print("已取消")
            sys.exit(0)

    # ── 安全网：自动存档（可回滚·存档失败即中止——不可回滚就不执行破坏性重置）──
    snapname = f"_before_reset_scene_{scene_base}_{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    snapshot_or_abort(world, snapname)

    # ── 1. narrative.md 轮转归档 + 置空 ──
    narr_file = scene_dir / "narrative.md"
    if narr_file.is_file() and narr_file.stat().st_size > 0:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        round_no = ""
        try:
            first = narr_file.read_text(encoding="utf-8").splitlines()[0] if narr_file.read_text(encoding="utf-8").strip() else ""
            m = re.search(r"轮次\s*(\d+)", first)
            if m:
                round_no = m.group(1)
        except Exception:
            pass
        if not round_no:
            ws = world_dir / "states" / "world_state.yaml"
            try:
                for line in ws.read_text(encoding="utf-8").splitlines():
                    if line.startswith("轮次:"):
                        mm = re.search(r"(\d+)", line)
                        if mm:
                            round_no = mm.group(1)
                        break
            except Exception:
                pass
        if round_no:
            os.replace(str(narr_file), str(scene_dir / f"narrative.r{round_no}.{ts}.md"))
            print(f"  归档: narrative.md -> narrative.r{round_no}.{ts}.md")
        else:
            os.replace(str(narr_file), str(scene_dir / f"narrative.{ts}.md"))
            print(f"  归档: narrative.md -> narrative.{ts}.md")
    narr_file.write_text("", encoding="utf-8", newline="")
    print("  清空: narrative.md")

    # ── 2. scene_state.yaml：场景时间线置空 + 核心状态待填充（保留静态基线）──
    ss_file = scene_dir / "scene_state.yaml"
    if ss_file.is_file():
        try:
            data = yaml.safe_load(ss_file.read_text(encoding="utf-8")) or {}
            if isinstance(data, dict):
                changed = []
                if data.get("场景时间线"):
                    data["场景时间线"] = ""
                    changed.append("场景时间线")
                if data.get("核心状态"):
                    data["核心状态"] = "<!-- 已重置：待按 start_snapshot.md 恢复开场状态 -->"
                    changed.append("核心状态")
                ss_file.write_text(yaml.dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8", newline="")
                if changed:
                    print(f"  重置: {'/'.join(changed)}")
                else:
                    print("  无变化: scene_state.yaml（场景时间线/核心状态已为空）")
            else:
                print("[WARN] scene_state.yaml 顶层非映射，跳过重置", file=sys.stderr)
        except Exception as e:
            print(f"[WARN] scene_state.yaml 解析失败，跳过场景状态重置: {e}", file=sys.stderr)
    else:
        print("[WARN] scene_state.yaml 不存在，跳过场景状态重置", file=sys.stderr)

    # ── 3. start_snapshot.md 确认存在（恢复依据）──
    snap_file = scene_dir / "start_snapshot.md"
    if snap_file.is_file():
        print("  恢复依据: start_snapshot.md（按此重新填充核心状态/道具/角色姿态）")
    else:
        print("[WARN] start_snapshot.md 不存在——重置后无恢复依据，建议补写", file=sys.stderr)

    # ── 4. world_state 时间/轮次回退至场景开场 ──
    ws_file = world_dir / "states" / "world_state.yaml"
    start_time = ""
    start_round = ""
    if snap_file.is_file():
        try:
            sstext = snap_file.read_text(encoding="utf-8")
            for line in sstext.splitlines():
                m = re.match(r"^冻结时间\s*[:：]\s*(.+)$", line)
                if m:
                    start_time = m.group(1).strip()
                    break
            if not start_time:
                mm = re.search(r"^## 冻结时间[^\n]*\n\s*([^\n]+)", sstext, re.M)
                if mm:
                    start_time = mm.group(1).strip()
            for line in sstext.splitlines():
                m = re.match(r"^开场轮次\s*[:：]\s*(.+)$", line)
                if m:
                    start_round = m.group(1).strip().strip("'\"")
                    break
            if not start_round:
                mm = re.search(r"^## 开场轮次[^\n]*\n\s*([^\n]+)", sstext, re.M)
                if mm:
                    start_round = mm.group(1).strip().strip("'\"")
        except Exception:
            pass
    if ws_file.is_file():
        text = ws_file.read_text(encoding="utf-8")
        if start_time:
            text = re.sub(r"^  具体时间:.*", f"  具体时间: {start_time}", text, count=1, flags=re.M)
            text = re.sub(r"^  基准时间:.*", f"  基准时间: {start_time}", text, count=1, flags=re.M)
            ws_file.write_text(text, encoding="utf-8", newline="")
            print(f"  回退: world_state 时间 → {start_time}（场景开场）")
        else:
            print("[WARN] start_snapshot.md 无冻结时间，跳过 world_state 时间回退（请补填 start_snapshot「## 冻结时间」）", file=sys.stderr)
        if start_round:
            text = ws_file.read_text(encoding="utf-8")
            text = re.sub(r"^轮次:.*", f"轮次: '{start_round}'", text, count=1, flags=re.M)
            ws_file.write_text(text, encoding="utf-8", newline="")
            print(f"  回退: world_state 轮次 → {start_round}（场景开场）")
        else:
            print("[WARN] start_snapshot.md 无开场轮次，跳过 world_state 轮次回退（请补填 start_snapshot「## 开场轮次」）", file=sys.stderr)

    print("")
    print(f"已重置场景 '{scene_base}' 到 start_snapshot 状态（静态基线保留·动态叙事清空·世界时间/轮次已回退至开场）")
    print("下一步: 戏剧家按 start_snapshot.md 重新填充 scene_state 核心状态，继续叙事")
    print("")
    print("【回退后必查·脚本不自动处理·LLM 按 references/rollback.md 涉及文件清单逐项核对】:")
    print("  1. conflicts.yaml         CT 上轮结算.关系状态/上轮结算.内部状态/相位回退·拍指针对照 snapshot 开场态重设")
    print("  2. direction.yaml         写作指针对照 snapshot 开场态重设·escalation_flags 清空/重估")
    print("  3. CHAR_*_state.yaml      核心状态/情绪/位置恢复开场形态；记忆锚点/连续行动轨迹/信念演化/偏离登记按开场轮次裁剪")
    print("                            （外部者如 Guest 必须裁剪未来记忆·Host 可保留作既视感/碎片素材）")
    print("  4. world_state.yaml       前情描述/外部倒计时/全局标记（脚本只回退了时间/轮次·其余仍可能是回退前状态）")
    print("  5. scene_state.yaml       核心状态/出场角色摘要恢复开场形态（脚本只清了时间线·静态基线保留）")
    print("  6. scenes/{当前焦点场景}/pending_actions.yaml     焦外条目回退（最易漏）")
    print("  7. world_map.yaml         回退期间新登记的区域（如有）")
    sys.exit(0)


if __name__ == "__main__":
    main()
