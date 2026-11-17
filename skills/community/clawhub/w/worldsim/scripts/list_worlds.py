#!/usr/bin/env python3
# list_worlds.py — 列出所有世界（当前 .yaml 体系）
# 用法: python3 scripts/list_worlds.py
#
# worlds 根：可被环境变量 WORLDSIM_WORLDS_DIR 覆写（用户自己的存储）；skill 根恒由脚本自身位置推导
import os, re, sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        if _s and _s.encoding and _s.encoding.lower().replace("-", "") != "utf8":
            _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _paths import worlds_root

WORLDS_ROOT = worlds_root()


def _focus_of(world_dir: Path) -> str:
    """world_state.焦点场景（tr 去全部空白）·缺省回退 .active（旧格式）。"""
    ws = world_dir / "states" / "world_state.yaml"
    if ws.is_file():
        try:
            for line in ws.read_text(encoding="utf-8").splitlines():
                if line.startswith("焦点场景:"):
                    val = re.sub(r"^焦点场景:\s*", "", line)
                    return re.sub(r"\s", "", val)
        except Exception:
            pass
    if (world_dir / ".active").is_file():
        try:
            return (world_dir / ".active").read_text(encoding="utf-8").strip() + "（旧格式）"
        except Exception:
            pass
    return ""


def main():
    for d in sorted(WORLDS_ROOT.glob("*")):
        if not d.is_dir() or d.name == "snaps":
            continue
        if not (d / "scenes").is_dir():
            continue
        name = d.name
        focus = _focus_of(d)
        if focus:
            print(f"🟢 {name}（焦点场景: {focus}）")
        else:
            print(f"⚪ {name}")
        chars = len(list((d / "characters").glob("CHAR_*.md")))
        states = len(list((d / "states").glob("CHAR_*_state.yaml")))
        scenes = len(list((d / "scenes").glob("S*/")))
        print(f"   角色: {chars} | 状态文件: {states} | 场景: {scenes}")
    sys.exit(0)


if __name__ == "__main__":
    main()
