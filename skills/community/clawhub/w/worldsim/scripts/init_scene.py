#!/usr/bin/env python3
# init_scene.py — 创建新场景目录及模板文件
# 用法: python3 scripts/init_scene.py <世界名> <场景ID> <场景名> [--from <旧场景ID>] [--place <档案路径>] [--type <类型>] [--time <时间>] [--cast <出场角色>]
#   --from <旧场景ID|旧场景目录名>: 继承旧场景 scene_state 的物理锚点/道具清单
#     （同物理地点切换必用——同一栋建筑的空间元素不因时间区间变化而消失，防止从零重建导致漏继承）
#   --place <档案路径>: 区域静态档案指针（相对世界目录，如 regions/甜水镇/REGION.md）——无 --from 时
#     作为 scene_state 物理锚点基线来源（首次到达·初始设定）；只校验存在性，内容由场记读档案生成
import os, re, sys, yaml
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        if _s and _s.encoding and _s.encoding.lower().replace("-", "") != "utf8":
            _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _paths import assert_no_links, resolve_world, resolve_within, validate_name

INDEX_HEADER = "# 场景索引\n\n| ID | 场景名称 | 类型 | 基准时间 | 出场 | 状态 |\n|----|------|------|------|------|------|\n"
SROW_RE = re.compile(r"^\|\s*[A-Z][0-9][0-9]*\s*\|")
SCENE_STATE_SKELETON = "核心状态: ''\n场景时间线: ''\n物理锚点: ''\n道具: ''\n关键场景信息: ''\n出场角色摘要: ''\n"


def block(text: str, key: str) -> str:
    """从 key: 起，到下一个顶层键（行首非空白非#非换行）或结尾。"""
    m = re.search(rf'^{re.escape(key)}:.*?(?=\n[^ \t#\n]|\Z)', text, re.M | re.S)
    return m.group(0) if m else ""


def main():
    argv = sys.argv[1:]
    if len(argv) < 3:
        print("用法: python3 scripts/init_scene.py <世界名> <场景ID> <场景名> [--from <旧场景ID>] [--place <档案路径>] [--type <类型>] [--time <时间>] [--cast <出场角色>]", file=sys.stderr)
        print("示例: python3 scripts/init_scene.py 遗弃之地 S07 追踪血迹 --type EXT --time '第3日 09:00' --cast 'Guest, Maeve'", file=sys.stderr)
        sys.exit(1)
    world, scene_id, scene_name = argv[0], argv[1], argv[2]
    opts = argv[3:]
    inherit_from = place_archive = scene_type = scene_time = scene_cast = ""
    i = 0
    while i < len(opts):
        a = opts[i]
        if a in ("--from", "--place", "--type", "--time", "--cast") and i + 1 < len(opts):
            v = opts[i + 1]
            if a == "--from": inherit_from = v
            elif a == "--place": place_archive = v
            elif a == "--type": scene_type = v
            elif a == "--time": scene_time = v
            elif a == "--cast": scene_cast = v
            i += 2
        else:
            print(f"[ERR] 未知参数: {a}（支持: --from <旧场景ID> / --place <档案路径> / --type <类型> / --time <时间> / --cast <出场角色>）", file=sys.stderr)
            sys.exit(1)

    if "/" in scene_name or "\\" in scene_name:
        print(f"[ERR] 场景名不能含 / 或 \\（场景名=目录名，含分隔符会破坏目录结构）: {scene_name}", file=sys.stderr)
        sys.exit(1)
    if not re.fullmatch(r"S[0-9]+", scene_id):
        print(f"[ERR] 非法场景ID '{scene_id}'（必须形如 S01：S+数字递增，目录名/索引/焦点场景均以该 ID 定位）", file=sys.stderr)
        sys.exit(1)

    world_dir = resolve_world(world)
    assert_no_links(world_dir / "scenes")
    scene_dir = world_dir / "scenes" / f"{scene_id}-{scene_name}"

    # ── 继承预检：--from 源场景必须存在且 YAML 可解析（在任何文件创建之前检查，失败即退出·不留半成品）──
    src_dir = None
    if inherit_from:
        validate_name(inherit_from, "旧场景ID")
        if (world_dir / "scenes" / inherit_from).is_dir():
            src_dir = world_dir / "scenes" / inherit_from
        else:
            cand = sorted((world_dir / "scenes").glob(inherit_from + "-*"))
            src_dir = cand[0] if cand else None
        if not src_dir or not (src_dir / "scene_state.yaml").is_file():
            print(f"[ERR] --from 场景不存在或缺 scene_state.yaml（检查: {inherit_from}）", file=sys.stderr)
            sys.exit(1)
        try:
            yaml.safe_load((src_dir / "scene_state.yaml").read_text(encoding="utf-8"))
        except Exception:
            print(f"[ERR] 源场景 scene_state.yaml 无法解析（{src_dir / 'scene_state.yaml'}）——拒绝继承坏格式，请先修复源文件再重跑", file=sys.stderr)
            sys.exit(1)

    # ── --place 预检：档案指针必须存在（相对世界目录·如 regions/甜水镇/REGION.md）──
    if place_archive:
        # 路径兼容归一（先归一再安全解析）：
        #   ① 绝对路径 → 相对世界目录（越界即拒）；② 误带世界根前缀 worlds/<世界名>/... → 剥离；
        #   ③ 传目录 → 自动补 REGION.md。三种写法等价：目录 / 相对REGION.md / 绝对REGION.md。
        _pa = place_archive.strip().strip('"').replace("\\", "/")
        _ws_abs = Path(os.path.abspath(world_dir))
        if Path(_pa).is_absolute() or (len(_pa) > 1 and _pa[1] == ":"):
            try:
                _pa = os.path.relpath(os.path.abspath(_pa), _ws_abs)
            except ValueError:
                print("[ERR] --place 绝对路径无法相对化到世界目录——拒绝", file=sys.stderr)
                sys.exit(1)
            if _pa.startswith(".."):
                print(f"[ERR] --place 绝对路径不在世界目录内（{place_archive}）——拒绝", file=sys.stderr)
                sys.exit(1)
        _parts = [p for p in Path(_pa).parts if p not in (".", "")]
        if len(_parts) >= 2 and _parts[0] == "worlds" and _parts[1] == world_dir.name:
            _parts = _parts[2:]
        _cand = Path(*_parts) if _parts else Path()
        if (world_dir / _cand).is_dir() and (world_dir / _cand / "REGION.md").is_file():
            _cand = _cand / "REGION.md"
        place_archive = str(_cand)
        place_fp = resolve_within(world_dir, place_archive, "--place 档案")
        if not place_fp.is_file():
            print(f"[ERR] --place 档案不存在（{place_fp}）——检查 regions/ 路径或补建档案（模板: templates/REGION.md）", file=sys.stderr)
            sys.exit(1)
        print(f"[OK] 物理基线来源: {place_archive}（场记据档案生成 scene_state 物理锚点·对照全局标记覆盖不可逆变更）")
        print(f"[区域] scene_card 区域行（场记生成 scene_card.md 时照抄）: | 区域 | {place_archive} |")
    else:
        # 未传 --place：从当前焦点场景区域档案的相邻/子区域自动扫描候选（脚本核对·LLM 照抄）
        print("[候选] 未传 --place——从当前焦点场景区域档案扫描相邻/子区域候选（已有 region 必须引用·禁止新建）:")
        cur_arch = ""
        ws = world_dir / "states" / "world_state.yaml"
        cur_scene = ""
        if ws.is_file():
            try:
                for line in ws.read_text(encoding="utf-8").splitlines():
                    if line.startswith("焦点场景:"):
                        cur_scene = re.sub(r"^焦点场景:\s*", "", line).strip().strip("'\" ")
                        break
            except Exception:
                pass
        if cur_scene:
            cards = sorted((world_dir / "scenes").glob(cur_scene + "-*/scene_card.md"))
            if cards:
                try:
                    for line in cards[0].read_text(encoding="utf-8").splitlines():
                        if line.startswith("| 区域 |"):
                            cur_arch = line[len("| 区域 |"):].split("|", 1)[0].strip()
                            break
                except Exception:
                    pass
        cur_fp = resolve_within(world_dir, cur_arch, "区域档案") if cur_arch else None
        if cur_fp and cur_fp.is_file():
            print(f"  当前场景区域档案: {cur_arch}")
            try:
                for line in cur_fp.read_text(encoding="utf-8").splitlines():
                    if not line.startswith("- "):
                        continue
                    name = re.split(r"[（(]", line[2:])[0].strip()
                    if not name:
                        continue
                    match = None
                    for d in sorted((world_dir / "regions").glob("*")):
                        if d.is_dir() and d.name == name:
                            match = d
                            break
                    if match:
                        print(f"  - {name} → {match.relative_to(world_dir).as_posix()}/REGION.md")
            except Exception:
                pass
        else:
            print("  （当前焦点场景无区域档案/无 scene_card·检查 regions/ 目录树）")

    scene_dir.mkdir(parents=True, exist_ok=True)

    # scene_card.md / start_snapshot.md / CHAR_state：按 templates/ 直接生成完整文件（脚本不生成内容骨架）
    # scene_state.yaml（新键表，见 references/keys.md §scene_state.yaml；脚本只建空值骨架，字段值随剧情轮 change set 注册自然累积）
    # 场景时间线【禁止预写】——剧情事件一律由每轮 change set ###APPEND: 追加（预写=把计划当记录·会与 change set 双写重复）。
    ss_file = scene_dir / "scene_state.yaml"
    ss_file.write_text(SCENE_STATE_SKELETON, encoding="utf-8", newline="")
    (scene_dir / "pending_actions.yaml").write_text("已完成: {}\n活跃中: {}\n", encoding="utf-8", newline="")

    # ── INHERIT: --from 继承旧场景物理锚点/道具（同物理地点切换必用；源存在性+可解析性已在创建前预检）──
    if src_dir is not None:
        target_text = ss_file.read_text(encoding="utf-8")
        source_text = (src_dir / "scene_state.yaml").read_text(encoding="utf-8")
        src_name = src_dir.name
        inherited = []
        for key in ("物理锚点", "道具"):
            src_block = block(source_text, key)
            if not src_block:
                print(f"[WARN] 旧场景缺字段 {key}，跳过继承")
                continue
            pattern = rf'^(# 道具清单继承自[^\n]*\n)?{re.escape(key)}:.*?(?=\n[^ \t#\n]|\Z)'
            if key == "道具":
                comment = f"# 道具清单继承自 {src_name}：状态随时间流逝自然变化，请按当前时间更新（位置一般不变）\n"
                target_text = re.sub(pattern, lambda m: comment + src_block, target_text, count=1, flags=re.M | re.S)
            else:
                target_text = re.sub(pattern, lambda m: src_block, target_text, count=1, flags=re.M | re.S)
            inherited.append(key)
        ss_file.write_text(target_text, encoding="utf-8", newline="")
        print(f"[OK] 场景继承: {src_name} -> {scene_dir.name} ({'、'.join(inherited)})")
        # 继承后立即校验新场景 YAML 可解析（防坏格式静默通过）
        try:
            yaml.safe_load(ss_file.read_text(encoding="utf-8"))
        except Exception:
            print(f"[ERR] 继承后 {ss_file} 无法解析（源格式非标准）——请手动修复该文件（如改用 '名称: 描述' 冒号格式），不要继续使用坏文件", file=sys.stderr)
            sys.exit(1)

    # narrative.md（空文件——每轮由 write_narrative.py 轮转写入，创建时留空为设计）
    (scene_dir / "narrative.md").write_text("", encoding="utf-8", newline="")

    # 更新场景索引（与 templates/INDEX.md 对齐：场景名称/基准时间）
    index_file = world_dir / "scenes" / "INDEX.md"
    if not index_file.is_file():
        index_file.write_text(INDEX_HEADER, encoding="utf-8", newline="")
    if any(line.startswith(f"| {scene_id} |") for line in index_file.read_text(encoding="utf-8").splitlines()):
        print(f"[WARN] 场景 {scene_id} 已存在于索引中，跳过索引更新")
    else:
        row = f"| {scene_id} | {scene_name} | {scene_type or '待填'} | {scene_time or '待填'} | {scene_cast or '待填'} | ACTIVE |"
        lines = index_file.read_text(encoding="utf-8").splitlines()
        last = -1
        for n, ln in enumerate(lines):
            if SROW_RE.match(ln):
                last = n
        if last >= 0:
            lines = lines[: last + 1] + [row] + lines[last + 1 :]
        else:
            lines = lines + [row]
        index_file.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="")

    print(f"[OK] 场景已创建: {scene_dir}")
    print(f"[OK] 索引文件已更新: {index_file}")

    # 同步 world_state.焦点场景（唯一权威源，顶层第一行）——旧世界无 world_state.yaml 则跳过
    ws_file = world_dir / "states" / "world_state.yaml"
    if ws_file.is_file():
        text = ws_file.read_text(encoding="utf-8")
        if re.search(r"^焦点场景:", text, re.M):
            text = re.sub(r"^焦点场景:.*", f"焦点场景: {scene_id}", text, count=1, flags=re.M)
        else:
            text = f"焦点场景: {scene_id}\n" + text
        ws_file.write_text(text, encoding="utf-8", newline="")
        print(f"[OK] world_state.焦点场景 已更新为 {scene_id}")

    # 清 direction.转场——③ 的转场决策已被本次切换消费。⑤ 无权写 direction（Single Writer），
    # 残留会让 round-check 误判「⑤转场未执行」、并静默豁免 cast 硬拦（假豁免），故由执行切换的脚本机械清除（幂等）。
    # 转场可为本行式（转场: {…}）或块式（转场:\n  子键: …，write-raw 经 yaml.dump 落块式）——须连缩进子行一并替换，只替首行会把子键泄漏成顶层键。
    dir_file = world_dir / "states" / "direction.yaml"
    if dir_file.is_file():
        try:
            _dtext = dir_file.read_text(encoding="utf-8")
            _dnew = re.sub(r"^转场:[^\n]*(?:\n[ \t]+[^\n]*)*", "转场: {}", _dtext, count=1, flags=re.M)
            if _dnew != _dtext:
                dir_file.write_text(_dnew, encoding="utf-8", newline="")
                print("[OK] direction.转场 已清空（转场决策已由本次切换消费）")
        except Exception as e:
            print(f"[WARN] direction.转场 清空失败（不影响场景创建）: {e}", file=sys.stderr)

    # ── 待填清单输出（脚本只建基础设施——内容文件按 templates/ 直接生成，禁止带模板占位运行）──
    print("")
    print("【注意】本目录已生成 scene_state.yaml / narrative.md（骨架·已存在）——后续用 Write/覆盖写前必须先 Read 该文件再改（写入工具拒绝未读覆盖）。")
    print("")
    print("【场景待填清单·创建后立即填充·禁止带模板占位（[字段定义]/(例:) 残留）运行】:")
    print("  1. scene_card.md      按 templates/scene_card.md 生成：焦外/在场 · 场景目标 · 前情钩子")
    print("  2. scene_state.yaml   已建空值骨架——元素随剧情轮 change set 注册自然累积（入场帧已涉及的元素随 change set 正常记录）")
    print("  3. start_snapshot.md  按 templates/start_snapshot.md 生成：角色姿态 / 道具位置 / 开场心理态 / 开场 conflicts 节拍态 / 开场 world_state 附加态 / 焦外待揭示")
    print("  4. CHAR_state         出场角色按 templates/CHAR_state.yaml 生成状态文件（核心状态/情绪/位置/压力水平/防御有效性等）")
    sys.exit(0)


if __name__ == "__main__":
    main()
