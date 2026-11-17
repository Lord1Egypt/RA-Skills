#!/usr/bin/env python3
# index.py — 场景索引管理
#
# 用法:
#   index.py <世界名> add      <场景ID> <名称> [类型] [时间] [出场] [状态]
#   index.py <世界名> update   <场景ID> [--type 值] [--time 值] [--cast 值] [--status 值] [--name 值]
#   index.py <世界名> activate <场景ID>
#   index.py <世界名> remove   <场景ID>
#   index.py <世界名> show
#
# 示例:
#   index.py malena add S05 菜市场 EXT "1941年6月，下午4:00" "Malèna, Renato"
#   index.py malena update S03 --status COMPLETED --type INT
#   index.py malena activate S04
#
# 参数顺序兼容（2026-08-06）：`index.py <世界名> <action>`（原）与 `index.py <action> <世界名>`（LLM 直觉）都支持
import os, re, sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        if _s and _s.encoding and _s.encoding.lower().replace("-", "") != "utf8":
            _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _paths import resolve_world

ACTIONS = {"add", "update", "activate", "remove", "show"}
INDEX_HEADER = "# 场景索引\n\n| ID | 场景名称 | 类型 | 基准时间 | 出场 | 状态 |\n|----|------|------|------|------|------|\n"
SROW_RE = re.compile(r"^\|\s*[A-Z][0-9][0-9]*\s*\|")
IDROW_RE = re.compile(r"^\|\s*([^|]+?)\s*\|")


def _row_id(line: str) -> str:
    m = IDROW_RE.match(line)
    return m.group(1).strip() if m else ""


def ensure_index(filepath: Path) -> None:
    if not filepath.is_file():
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(INDEX_HEADER, encoding="utf-8", newline="")


def _insert_after_last_srow(lines: list[str], row: str) -> list[str]:
    """在最后一个 `| Sxx |` 行之后插入（保持按 ID 排序），无则追加。"""
    last = -1
    for i, ln in enumerate(lines):
        if SROW_RE.match(ln):
            last = i
    if last >= 0:
        return lines[: last + 1] + [row] + lines[last + 1 :]
    return lines + [row]


def _sync_focus(world_dir: Path, scene_id: str) -> None:
    """同步 world_state.焦点场景（唯一权威源）——旧世界无 world_state.yaml 则跳过。"""
    ws = world_dir / "states" / "world_state.yaml"
    if not ws.is_file():
        return
    text = ws.read_text(encoding="utf-8")
    if re.search(r"^焦点场景:", text, re.M):
        text = re.sub(r"^焦点场景:.*", f"焦点场景: {scene_id}", text, count=1, flags=re.M)
    else:
        text = f"焦点场景: {scene_id}\n" + text
    ws.write_text(text, encoding="utf-8", newline="")
    print(f"[OK] world_state.焦点场景 已更新为 {scene_id}")


def main():
    argv = sys.argv[1:]
    if len(argv) >= 1 and argv[0] in ACTIONS:
        action, world = argv[0], (argv[1] if len(argv) >= 2 else "")
    else:
        world, action = (argv[0] if len(argv) >= 1 else ""), (argv[1] if len(argv) >= 2 else "")
    if not world or not action:
        print("用法: index.py <世界名> <add|update|activate|remove|show> [...]", file=sys.stderr)
        sys.exit(1)

    world_dir = resolve_world(world)
    filepath = world_dir / "scenes" / "INDEX.md"

    rest = argv[2:] if argv[0] in ACTIONS else argv[2:]

    if action == "add":
        scene_id = rest[0] if len(rest) >= 1 else ""
        scene_name = rest[1] if len(rest) >= 2 else ""
        scene_type = rest[2] if len(rest) >= 3 else ""
        scene_time = rest[3] if len(rest) >= 4 else ""
        scene_cast = rest[4] if len(rest) >= 5 else ""
        scene_status = rest[5] if len(rest) >= 6 else "ACTIVE"
        if not scene_id:
            print("[ERR] 缺少场景ID (如 S05)", file=sys.stderr); sys.exit(1)
        if not scene_name:
            print("[ERR] 缺少场景名", file=sys.stderr); sys.exit(1)
        ensure_index(filepath)
        lines = filepath.read_text(encoding="utf-8").splitlines()
        if any(line.startswith(f"| {scene_id} |") for line in lines):
            print(f"[WARN] 场景 {scene_id} 已存在于索引中")
            sys.exit(0)
        row = f"| {scene_id} | {scene_name} | {scene_type} | {scene_time} | {scene_cast} | {scene_status} |"
        lines = _insert_after_last_srow(lines, row)
        filepath.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="")
        print(f"[OK] 索引 +{scene_id} {scene_name}")

    elif action == "update":
        scene_id = rest[0] if len(rest) >= 1 else ""
        if not scene_id:
            print("[ERR] 缺少场景ID", file=sys.stderr); sys.exit(1)
        if not filepath.is_file():
            print("[ERR] INDEX.md 不存在", file=sys.stderr); sys.exit(1)
        lines = filepath.read_text(encoding="utf-8").splitlines()
        idx = next((i for i, ln in enumerate(lines) if ln.startswith(f"| {scene_id} |")), None)
        if idx is None:
            print(f"[ERR] 场景 {scene_id} 不在索引中", file=sys.stderr); sys.exit(1)

        def update_col(col: int, pname: str, newval: str) -> None:
            nonlocal lines, idx
            parts = lines[idx].split("|")
            # 行格式: ['', ' ID ', ' 名称 '=col2, ' 类型 '=col3, ' 时间 '=col4, ' 出场 '=col5, ' 状态 '=col6, '']
            #   → python 索引 = col（awk $c=col+1 → parts[col]）
            col_val = parts[col].strip() if len(parts) > col else ""
            if col_val == newval:
                print(f"[OK] {scene_id} {pname}={newval}（幂等跳过）")
                return
            if len(parts) > col:
                parts[col] = f" {newval} "
            else:
                while len(parts) < col + 1:
                    parts.append("")
                parts[col] = f" {newval} "
            new_line = "|".join(parts)
            if new_line == lines[idx]:
                print(f"[ERR] {scene_id} {pname} 更新失败：索引行未变化（行格式异常），请手动修复 INDEX.md 该行", file=sys.stderr)
                sys.exit(1)
            lines[idx] = new_line

        args = rest[1:]
        i = 0
        while i < len(args):
            a = args[i]
            if a in ("--type", "--time", "--cast", "--status", "--name") and i + 1 < len(args):
                v = args[i + 1]
                colmap = {"--name": 2, "--type": 3, "--time": 4, "--cast": 5, "--status": 6}
                pname = {"--name": "名称", "--type": "类型", "--time": "时间", "--cast": "出场", "--status": "状态"}[a]
                update_col(colmap[a], pname, v)
                i += 2
            else:
                print(f"[ERR] 未知参数: {a}", file=sys.stderr); sys.exit(1)
        filepath.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="")

    elif action == "activate":
        scene_id = rest[0] if len(rest) >= 1 else ""
        if not scene_id:
            print("[ERR] 缺少场景ID", file=sys.stderr); sys.exit(1)
        if not filepath.is_file():
            print("[ERR] INDEX.md 不存在", file=sys.stderr); sys.exit(1)
        lines = filepath.read_text(encoding="utf-8").splitlines()
        changed = False
        for i, ln in enumerate(lines):
            parts = ln.split("|")
            if len(parts) < 7:
                continue
            if ln.startswith(f"| {scene_id} |"):
                parts[6] = " ACTIVE "
                lines[i] = "|".join(parts)
                changed = True
            elif ln.startswith("| S"):
                parts[6] = " COMPLETED "
                lines[i] = "|".join(parts)
        if not changed:
            print(f"[ERR] 场景 {scene_id} 不在索引中", file=sys.stderr); sys.exit(1)
        filepath.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="")
        _sync_focus(world_dir, scene_id)
        print(f"[OK] {scene_id} 设为 ACTIVE，其余标记 COMPLETED")

    elif action == "remove":
        scene_id = rest[0] if len(rest) >= 1 else ""
        if not scene_id:
            print("[ERR] 缺少场景ID", file=sys.stderr); sys.exit(1)
        if not filepath.is_file():
            print("[ERR] INDEX.md 不存在", file=sys.stderr); sys.exit(1)
        lines = [ln for ln in filepath.read_text(encoding="utf-8").splitlines() if not ln.startswith(f"| {scene_id} |")]
        filepath.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="")
        print(f"[OK] 索引已移除: {scene_id}")

    elif action == "show":
        if filepath.is_file():
            print(filepath.read_text(encoding="utf-8"), end="")
        else:
            print("(INDEX.md 不存在)")

    else:
        print(f"[ERR] 未知操作: {action} (支持: add/update/activate/remove/show)", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
