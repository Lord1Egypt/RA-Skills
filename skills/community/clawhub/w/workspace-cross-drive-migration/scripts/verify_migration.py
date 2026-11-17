#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
迁移后核对（只读，不改任何东西）

用法：
  python verify_migration.py --state "<状态目录>"
  python verify_migration.py --source "D:\\Work\\项目A" --target "G:\\迁移\\项目A" --deep

--deep 对全部文件做 MD5（慢，但最踏实）；默认做「全部小文件 + 最大的若干文件」抽样。

注意：迁移会故意改写 <目标>\\.workbuddy 下文本里的路径，所以这些文件的字节数变化
属于「预期变化」，不算失败；脚本会逐对验证「源文本做同样替换后是否等于目标文本」。
退出码：0 全部通过；1 有未通过项。
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ws_migrate_common as C  # noqa: E402

TEXT_SUFFIX = {".md", ".json", ".txt", ".yaml", ".yml"}


def inventory(root: Path) -> dict:
    """返回 rel -> size。"""
    out = {}
    if not root.is_dir():
        return out
    for fp in C.iter_files(root):
        rel = str(fp.relative_to(root))
        try:
            out[rel] = fp.stat().st_size
        except OSError:
            out[rel] = 0
    return out


def expected_doc_change(src_file: Path, dst_file: Path, old: str, new: str) -> bool:
    """目标文件是否恰好等于「源文件做路径替换后的结果」。"""
    if src_file.suffix.lower() not in TEXT_SUFFIX:
        return False
    try:
        a = src_file.read_text(encoding="utf-8")
        b = dst_file.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    return C.rewrite_text(a, old, new)[0] == b


def pick_sample(rels, sizes, limit: int = 300, deep: bool = False):
    if deep:
        return list(rels)
    small = [r for r in rels if sizes.get(r, 0) <= 64 * 1024]
    big = sorted(rels, key=lambda r: sizes.get(r, 0), reverse=True)[:10]
    chosen = list(dict.fromkeys(small[:limit] + big))
    if len(small) > limit:
        chosen += random.sample(small, min(20, len(small)))
    return list(dict.fromkeys(chosen))


def main() -> int:
    ap = argparse.ArgumentParser(description="迁移后核对（只读）")
    ap.add_argument("--state", help="迁移状态目录或 state.json")
    ap.add_argument("--source")
    ap.add_argument("--target")
    ap.add_argument("--deep", action="store_true", help="全量 MD5")
    args = ap.parse_args()

    if args.state:
        state = C.load_state(args.state)
        src, dst = state["source"], state["target"]
        new_slug = state["new_slug"]
    elif args.source and args.target:
        state = None
        src, dst = os.path.abspath(args.source), os.path.abspath(args.target)
        new_slug = C.slug_for_path(dst)
    else:
        ap.error("需要 --state，或同时给 --source 与 --target")

    cmp_src = src
    if state and not os.path.isdir(cmp_src):
        iso = state.get("source_isolated")
        if iso and os.path.isdir(iso):
            cmp_src = iso

    failures, warnings = [], []

    C.hr("迁移核对")
    print(f"  源    {src}")
    print(f"  新    {dst}")
    if cmp_src != src:
        print(f"  基准  用隔离副本比对：{cmp_src}")

    if not os.path.isdir(dst):
        C.bad(f"目标目录不存在：{dst}")
        return 1

    # ---- 1. 文件清单
    C.hr("1. 文件清单")
    a = inventory(Path(cmp_src))
    b = inventory(Path(dst))
    print(f"  基准 {len(a)} 个文件 / 新 {len(b)} 个文件")
    if not a:
        warnings.append("没有可比对的源目录（可能已被删除），只做目标侧自检")
    missing = sorted(set(a) - set(b))
    extra = sorted(set(b) - set(a))
    if missing:
        C.bad(f"目标缺 {len(missing)} 个文件")
        failures.append(f"缺 {len(missing)} 个文件，例：{missing[:3]}")
    if extra:
        C.warn(f"目标多出 {len(extra)} 个文件（一般无害）")
    size_diff = [r for r in (set(a) & set(b)) if a[r] != b[r]]
    expected, unexpected = [], []
    for rel in size_diff:
        if expected_doc_change(Path(cmp_src) / rel, Path(dst) / rel, src, dst):
            expected.append(rel)
        else:
            unexpected.append(rel)
    if expected:
        C.ok(f"{len(expected)} 个文件因路径改写而体积变化（预期内）")
    if unexpected:
        C.bad(f"{len(unexpected)} 个文件长度异常，例：{unexpected[:3]}")
        failures.append("存在长度异常文件")
    if not missing and not unexpected:
        C.ok("文件清单一致")

    # ---- 2. 内容校验
    C.hr("2. 内容校验" + ("（全量 MD5）" if args.deep else "（抽样 MD5）"))
    if a:
        skip = set(expected)
        rels = pick_sample([r for r in a if r not in skip], a, deep=args.deep)
        bad = 0
        for rel in rels:
            f, t = Path(cmp_src) / rel, Path(dst) / rel
            if not t.exists():
                continue
            try:
                if C.md5_of(f) != C.md5_of(t):
                    bad += 1
                    failures.append(f"内容不一致：{rel}")
            except OSError as e:
                bad += 1
                failures.append(f"读取失败：{rel}（{e}）")
        if bad == 0:
            C.ok(f"{len(rels)} 个文件内容一致")
    else:
        warnings.append("无源目录可比对，跳过内容校验")

    # ---- 3. 关键内容
    C.hr("3. 关键内容")
    checks = [
        (".workbuddy 目录", (Path(dst) / ".workbuddy").is_dir(), False),
        ("记忆目录", (Path(dst) / ".workbuddy" / "memory").is_dir(), False),
        ("会话历史目录", (C.PROJECTS_DIR / new_slug).is_dir(), True),
    ]
    for name, good, hard in checks:
        if good:
            C.ok(name)
        elif hard:
            C.bad(f"{name} 缺失")
            failures.append(f"{name} 缺失")
        else:
            C.warn(f"{name} 不存在（原本没有属正常）")

    # ---- 4. 会话记录
    C.hr("4. 会话记录")
    proj = C.PROJECTS_DIR / new_slug
    if proj.is_dir():
        files = total = broken = residue = 0
        for f in proj.rglob("*.jsonl"):
            files += 1
            try:
                text = f.read_text(encoding="utf-8-sig")
            except UnicodeDecodeError:
                text = f.read_text(encoding="utf-8", errors="surrogateescape")
            for line in text.splitlines():
                if line.strip():
                    total += 1
                    try:
                        json.loads(line)
                    except Exception:
                        broken += 1
            residue += C.count_occurrences(text, src)
        print(f"  {files} 个 jsonl / {total} 行")
        if broken:
            C.bad(f"{broken} 行 JSON 损坏")
            failures.append("jsonl 结构损坏")
        else:
            C.ok("每行都是合法 JSON")
        if residue:
            C.warn(f"{residue} 处旧路径仍在（多出现在用户消息正文里，不影响使用）")
            warnings.append(f"旧路径残留 {residue} 处")
        else:
            C.ok("没有旧路径残留")
    else:
        warnings.append("没有会话历史目录")

    # ---- 5. 数据库与显示名
    C.hr("5. 数据库与侧边栏")
    new_side = C.db_snapshot(C.DB_PATH, dst)
    old_side = C.db_snapshot(C.DB_PATH, src)
    if new_side["ok"]:
        print(f"  指向新路径：workspaces {new_side['workspaces']} / sessions {new_side['sessions']} / "
              f"automations {new_side['automations']} / trust {new_side['trust']}")
        print(f"  仍指旧路径：workspaces {old_side['workspaces']} / sessions {old_side['sessions']} / "
              f"automations {old_side['automations']} / trust {old_side['trust']}")
        if new_side["workspaces"] or new_side["sessions"]:
            C.ok("数据库已指向新路径")
        else:
            C.warn("数据库里还没有新路径记录（未改，或应用还没打开过新工作空间）")
            warnings.append("数据库未指向新路径")
        if old_side["automations"]:
            C.bad(f"{old_side['automations']} 个自动化仍指向旧路径")
            failures.append("自动化仍指向旧路径")
    else:
        warnings.append(f"数据库读不了：{new_side['error']}")

    entry = C.display_name_entry(dst)
    if entry:
        C.ok(f"侧边栏显示名：{entry.get('displayName')}")
    else:
        C.warn("侧边栏没有新路径的记录")
        warnings.append("显示名缺失")

    # ---- 结论
    C.hr("结论")
    if failures:
        C.bad(f"{len(failures)} 项必须处理：")
        for f in failures[:15]:
            print(f"         - {f}")
        print('\n  处理不了就回滚：python rollback_migration.py --state "<状态目录>" --apply')
        return 1
    C.ok("全部通过，可以正常使用。")
    for w in warnings:
        print(f"  [提示] {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
