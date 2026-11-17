#!/usr/bin/env python3
# create_world.py — 创建新世界脚手架（只生成 .md 静态骨架·零 yaml）
# 用法: python3 scripts/create_world.py <世界名>
# 动态文件（states/ 下 yaml）由启动世界 init-states 物化生成（见 references/session_recovery.md 第二章）
# 创作填充顺序见 references/session_recovery.md 第一章
import os, re, shutil, sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        if _s and _s.encoding and _s.encoding.lower().replace("-", "") != "utf8":
            _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _paths import SKILL_DIR, worlds_root

WORLDS_ROOT = worlds_root()


def main():
    argv = sys.argv[1:]
    if not argv or not argv[0]:
        print("用法: python3 scripts/create_world.py <世界名>", file=sys.stderr)
        sys.exit(1)
    world = argv[0]

    # 世界名校验：仅字母/数字/下划线/连字符（防路径穿越）——与旧 create_world.py 一致
    if not re.fullmatch(r"[A-Za-z0-9_-]+", world):
        print("错误: 世界名只能包含字母/数字/下划线/连字符", file=sys.stderr)
        sys.exit(1)

    world_dir = WORLDS_ROOT / world
    if world_dir.is_dir():
        print(f"错误: 世界 '{world}' 已存在: {world_dir}", file=sys.stderr)
        sys.exit(1)

    for sub in ("", "characters", "states", "story_architecture"):
        (world_dir / sub).mkdir(parents=True, exist_ok=True)

    for f in ("SETTING.md",):
        src = SKILL_DIR / "templates" / f
        if src.is_file():
            shutil.copy2(src, world_dir / f)
            print(f"  生成: {f}")
        else:
            print(f"  警告: 模板缺失 templates/{f}", file=sys.stderr)

    seed_src = SKILL_DIR / "templates" / "CONFLICTS_SEED.md"
    if seed_src.is_file():
        shutil.copy2(seed_src, world_dir / "story_architecture" / "CONFLICTS_SEED.md")
        print("  生成: story_architecture/CONFLICTS_SEED.md")
    else:
        print("  警告: 模板缺失 templates/CONFLICTS_SEED.md", file=sys.stderr)

    print("")
    print(f"已创建世界 '{world}': {world_dir}（仅 .md 静态骨架·零 yaml）")
    print("")
    print("【待填清单】创作填充顺序（见 references/session_recovery.md 第一章）:")
    print("  1. SETTING.md                世界观/地理/势力/规则/核心高压法则/故事弧线(可选·顶层唯一文件)")
    print("  2. characters/CHAR_*.md      每角色一个档案（从 templates/CHAR_.md 复制改名填写）")
    print("  3. story_architecture/        故事架构（CONFLICTS_SEED.md 2-5 条冲突种子·LOOPS.md 循环世界必填【协调索引·完整日程在各 CHAR_ 默认循环时间线】·CROSS_NARRATIVES.md 可选）")
    print("  4. regions/                   可选·区域静态档案（见 templates/REGION.md）")
    print("")
    print("动态文件（states/ 下 yaml）由『启动世界』init-states 物化生成。")
    sys.exit(0)


if __name__ == "__main__":
    main()
