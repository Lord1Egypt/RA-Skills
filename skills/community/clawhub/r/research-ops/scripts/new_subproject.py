#!/usr/bin/env python3
"""research-ops: scaffold a research sub-project skeleton under any group root.

Generic & decoupled: root is passed in, nothing hard-coded.
"""
import argparse
import json
import os
import sys

SUBDIRS = ["scripts", "data", "results", "output", "chats"]

README_TMPL = """# {title}

> 项目 ID：`{slug}`｜建立：{date}
> 组规范见上级 `AGENTS.md`；项目索引见组根 `INDEX.md`。

## 目的 / 目标
-

## 进展
- [ ] 初始化
"""

STATE_TMPL = """# {title} — 当前基线（STATE）

> AI 接手先读本文件；只写「现在以什么为准」，历史阶段另记。

- ★ 当前基线：{date} — （待填写）
- 需求收敛：（待填写）

## 关键产出 / 链接
- 本地：
- Zotero collection：
- Obsidian 笔记夹：
- 飞书：
"""


def main():
    ap = argparse.ArgumentParser(description="Scaffold a research sub-project")
    ap.add_argument("--root", required=True, help="group root (or its projects/ parent)")
    ap.add_argument("--name", required=True, help="project slug")
    ap.add_argument("--title", default=None, help="human readable title")
    ap.add_argument("--in-projects", action="store_true", help="place under <root>/projects/<name>")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    import datetime
    date = datetime.date.today().isoformat()
    title = a.title or a.name
    base = os.path.join(a.root, "projects") if a.in_projects else a.root
    dest = os.path.join(base, a.name)

    created = []
    if os.path.exists(dest) and not a.force:
        print(json.dumps({"status": "error", "message": f"exists: {dest} (use --force)"}, ensure_ascii=False))
        sys.exit(1)

    plan = [(dest, None)]
    for d in SUBDIRS:
        plan.append((os.path.join(dest, d), None))
    plan.append((os.path.join(dest, "README.md"), README_TMPL.format(title=title, slug=a.name, date=date)))
    plan.append((os.path.join(dest, "STATE.md"), STATE_TMPL.format(title=title, date=date)))

    if a.dry_run:
        print(json.dumps({"status": "ok", "dry_run": True, "dest": dest,
                          "would_create": [p for p, _ in plan]}, ensure_ascii=False))
        return

    os.makedirs(dest, exist_ok=True)
    created.append(dest)
    for d in SUBDIRS:
        p = os.path.join(dest, d)
        os.makedirs(p, exist_ok=True)
        created.append(p)
    for fname, content in [("README.md", README_TMPL.format(title=title, slug=a.name, date=date)),
                           ("STATE.md", STATE_TMPL.format(title=title, date=date))]:
        p = os.path.join(dest, fname)
        if os.path.exists(p) and not a.force:
            continue
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(content)
        created.append(p)

    print(json.dumps({"status": "ok", "dry_run": False, "project": a.name, "dest": dest,
                      "created": created}, ensure_ascii=False))


if __name__ == "__main__":
    main()
