#!/usr/bin/env python3
"""Novel Writer 版本管理 & changelog"""

from pathlib import Path
from datetime import datetime

CHANGELOG_PATH = Path(__file__).parent.parent / "CHANGELOG.md"

ENTRIES = [
    ("2.1.0", "2026-04-11", "测试迁移到标准路径 tests/，修复4个脚本路径测试，SKILL.md补全参数速查"),
    ("2.0.0", "2026-04-11", "企业级重构：SKILL.md通用化，统一CLI，移除用户数据，中英README+LICENSE"),
    ("1.0.0", "2026-04-10", "初始版本：13个检测脚本，283个测试，20篇参考文档"),
]

def show():
    for ver, date, desc in ENTRIES:
        print(f"  {ver} ({date}) — {desc}")

def add(version, description):
    date = datetime.now().strftime("%Y-%m-%d")
    ENTRIES.insert(0, (version, date, description))
    _write_changelog()
    print(f"✅ 已添加 {version}: {description}")

def _write_changelog():
    lines = ["# Changelog\n"]
    for ver, date, desc in ENTRIES:
        lines.append(f"## {ver} ({date})\n- {desc}\n")
    CHANGELOG_PATH.write_text("\n".join(lines), encoding="utf-8")

def main():
    import sys
    if len(sys.argv) < 2:
        print("📖 Novel Writer 版本管理")
        print("用法: changelog [show|add <版本> <描述>]")
        show()
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd == "show":
        show()
    elif cmd == "add" and len(sys.argv) >= 4:
        add(sys.argv[2], " ".join(sys.argv[3:]))
    else:
        print(f"❌ 未知命令: {cmd}")

if __name__ == "__main__":
    main()
