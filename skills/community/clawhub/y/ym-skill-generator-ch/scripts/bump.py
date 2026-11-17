#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""递增技能版本号，并在版本历史顶部插一条记录。

    python scripts/bump.py <技能目录> -m "修了什么"            # 修订号 +1：2.3.0 → 2.3.1
    python scripts/bump.py <技能目录> --minor -m "加了什么"    # 次版本 +1：2.3.1 → 2.4.0
    python scripts/bump.py <技能目录> --major -m " breaking"   # 主版本 +1：2.4.0 → 3.0.0
    python scripts/bump.py <技能目录> --set 3.0.0              # 直接指定版本
    python scripts/bump.py <技能目录> -m "说明" --dry-run      # 只看会改什么

为什么需要它：发布前要改两处（frontmatter 的 version + 版本历史），
手工改必然漏一处 —— 漏了版本历史，用户就看不出这次更新了什么。
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _friendly import explain_exit, use_utf8_stdout  # noqa: E402

VERSION_RE = re.compile(r"^version:\s*(.+)$", re.M)
CHANGELOG_HEAD_RE = re.compile(r"^##\s*版本历史\s*$", re.M)


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except OSError:
        return ""


def bump_version(old: str, part: str) -> str:
    nums = re.findall(r"\d+", old or "0.0.0")
    while len(nums) < 3:
        nums.append("0")
    major, minor, patch = (int(n) for n in nums[:3])
    if part == "major":
        return "%d.0.0" % (major + 1)
    if part == "minor":
        return "%d.%d.0" % (major, minor + 1)
    return "%d.%d.%d" % (major, minor, patch + 1)


def insert_changelog(content: str, version: str, msg: str, today: str) -> str:
    entry = "\n### v%s (%s)\n\n- %s\n" % (version, today, msg or "（未填写说明，建议补上）")
    m = CHANGELOG_HEAD_RE.search(content)
    if m:
        # 插到「## 版本历史」标题之后、第一条记录之前
        return content[:m.end()] + entry + content[m.end():]
    # 没有这个标题就追加一小节到末尾
    return content.rstrip() + "\n\n## 版本历史\n" + entry


def main() -> int:
    use_utf8_stdout()
    ap = argparse.ArgumentParser(description="递增技能版本号并追加版本历史")
    ap.add_argument("skill_dir")
    ap.add_argument("-m", "--msg", default="", help="这次改了什么（写进版本历史）")
    ap.add_argument("--major", action="store_true")
    ap.add_argument("--minor", action="store_true")
    ap.add_argument("--patch", action="store_true")
    ap.add_argument("--set", dest="set_version", default=None, help="直接指定版本号")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-changelog", action="store_true", help="只改 version，不动版本历史")
    args = ap.parse_args()

    root = Path(args.skill_dir).expanduser().resolve()
    skill_md = root / "SKILL.md"
    if not root.is_dir() or not skill_md.exists():
        print("[X] 不是技能目录（没有 SKILL.md）：%s" % root)
        print("    %s" % explain_exit(3))
        return 3

    content = read_text(skill_md)
    m = VERSION_RE.search(content)
    if not m:
        print("[X] frontmatter 里没有 version 字段。")
        print("    怎么修：在 frontmatter 加一行 `version: 0.1.0` 再跑。")
        print("    %s" % explain_exit(3))
        return 3

    old = m.group(1).strip().strip("\"'")
    if args.set_version:
        new = args.set_version
    else:
        part = "major" if args.major else ("minor" if args.minor else "patch")
        new = bump_version(old, part)

    print("版本号   : %s → %s" % (old, new))
    if not args.no_changelog:
        print("版本历史 : 追加一条「%s」" % (args.msg or "（空说明）"))

    new_content = content[:m.start(1)] + new + content[m.end(1):]
    if not args.no_changelog:
        # 版本可能在别处也被引用（CHANGELOG 里），只替换 frontmatter 那一处
        new_content = insert_changelog(new_content, new, args.msg, date.today().isoformat())

    if args.dry_run:
        print("\n[dry-run] 未落盘。")
        return 0

    try:
        skill_md.write_text(new_content, encoding="utf-8")
    except OSError as e:
        from _friendly import friendly
        what, fix = friendly(e)
        print("[X] 写入失败：%s" % what)
        print("    怎么修：%s" % fix)
        return 4

    print("\n[OK] 已更新 %s" % skill_md)
    print("    下一步：python scripts/audit_skill.py \"%s\" --market" % root)
    if not args.msg:
        print("    （这次没写说明，建议补上 -m，否则版本历史里只有个版本号）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
