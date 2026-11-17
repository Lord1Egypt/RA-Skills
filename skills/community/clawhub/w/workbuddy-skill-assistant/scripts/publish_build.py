#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy skill 使用管理指南 · 发布构建器（单一事实源 → dist/）

把"源目录"（SKILL.md / references/ / scripts/）构建成发布副本
dist/workbuddy-skill-assistant/，并生成 manifest.json（文件清单 + sha256 + 版本），
用于：① 保证发布件与源零漂移；② 运行时版本自检对照。

maintainers/ 是作者侧资料，不随发布包分发（仅保留在源仓库）。

用法：
  python scripts/publish_build.py                 # 构建 + 同步 dist + 生成 manifest
  python scripts/publish_build.py --check-only    # 只校验 dist 是否与源同步（CI/发布前用）
  python scripts/publish_build.py --keep-state     # 拷贝开发态 state.md（默认用干净的 state.template.md）

红线：
  - 源目录是唯一真源；禁止直接手改 dist/。
  - 发布前务必跑 --check-only，输出 IN_SYNC 才可发布。
  - dist/ 顶层只允许 `workbuddy-skill-assistant/` 一个目录；出现别的子目录
    （如历史遗留的 _release/ 陈旧发布包）一律判为跑偏残留并拦下发布。
"""
import argparse
import hashlib
import json
import shutil
import sys
import tempfile
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass  # 有意忽略：防御性处理，失败不阻断

sys.path.insert(0, str(Path(__file__).resolve().parent))
from version import VERSION  # noqa: E402  单一版本源 = SKILL.md frontmatter

SRC = Path(__file__).resolve().parent.parent          # skill 根目录
DIST = SRC / "dist" / "workbuddy-skill-assistant"      # 发布副本

# 要同步的内容（maintainers/ 为作者侧资料，不进发布包）
DIRS = ["references", "scripts"]
FILES = ["SKILL.md", "CHANGELOG.md"]
STATE_TEMPLATE = "state.template.md"
# dist/ 顶层唯一合法的发布目录；其余顶层条目一律视为跑偏残留
ALLOWED_DIST_ENTRIES = {DIST.name}
# dist 卫生：构建后清除的垃圾（绝不随发布件外流）
JUNK_DIRS = ("__pycache__",)
JUNK_SUFFIX = (".pyc",)
JUNK_NAME_TAGS = (".bak",)     # 覆盖 .bak / .bak-20260827 等历史备份


def _is_junk(path: Path) -> bool:
    name = path.name
    return (path.suffix in JUNK_SUFFIX
            or any(t in name for t in JUNK_NAME_TAGS))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _copy_file(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(src), str(dst))


def _clean_dist():
    """安全清空 dist：重命名备份到 %TEMP%，而非硬删。

    原因：沙箱环境禁用 shutil.rmtree（SAFE_DELETE_FAIL_CLOSED，Windows 回收站不可用）。
    改为 rename 到临时目录，既不触发硬删拦截，又保留旧副本便于回滚。
    """
    if not DIST.exists():
        return
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = Path(tempfile.gettempdir()) / f"wba-dist-bak-{stamp}"
    n = 0
    while bak.exists():
        n += 1
        bak = Path(tempfile.gettempdir()) / f"wba-dist-bak-{stamp}-{n}"
    shutil.move(str(DIST), str(bak))


def build(keep_state: bool = False):
    _clean_dist()
    DIST.mkdir(parents=True)

    for d in DIRS:
        src_dir = SRC / d
        if src_dir.exists():
            shutil.copytree(
                str(src_dir), str(DIST / d),
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.bak*"),
            )
    for f in FILES:
        _copy_file(SRC / f, DIST / f)

    # state.md：默认干净模板；--keep-state 用开发态
    state_src = SRC / "state.md" if keep_state else SRC / STATE_TEMPLATE
    if state_src.exists():
        _copy_file(state_src, DIST / "state.md")

    # 卫生清理：__pycache__ / *.pyc / *.bak*（含历史备份）绝不进发布件
    for p in list(DIST.rglob("*")):
        try:
            if p.is_file() and (_is_junk(p) or "__pycache__" in p.parts):
                p.unlink()
            elif p.is_dir() and p.name in JUNK_DIRS:
                shutil.rmtree(str(p))
        except Exception:
            pass  # 有意忽略：防御性处理，失败不阻断

    _write_manifest()


def _write_manifest():
    manifest = {
        "name": "workbuddy-skill-assistant",
        "version": VERSION,
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        # 不写构建机绝对路径（红线：禁止 C:\Users\<用户名> 硬编码泄漏）。
        # 发布件的 "source" 仅作信息性标识，标识它属于哪个 skill 根，运行时无任何读取方。
        "source": DIST.name,
        "files": [],
    }
    for p in sorted(DIST.rglob("*")):
        if p.is_file() and p.name != "manifest.json":
            rel = str(p.relative_to(DIST)).replace("\\", "/")
            manifest["files"].append({"path": rel, "sha256": sha256(p)})
    (DIST / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def verify() -> list:
    """返回差异清单；空列表 = 同步。"""
    problems = []
    for d in DIRS:
        src_dir, dst_dir = SRC / d, DIST / d
        if not src_dir.exists():
            continue
        for s in src_dir.rglob("*"):
            if s.is_dir():
                continue
            if "__pycache__" in s.parts or _is_junk(s):
                continue
            rel = s.relative_to(src_dir)
            d2 = dst_dir / rel
            if not d2.exists():
                problems.append(f"MISSING: {d}/{rel}")
            elif sha256(s) != sha256(d2):
                problems.append(f"DIFFERS: {d}/{rel}")
    for f in FILES:
        if not (DIST / f).exists():
            problems.append(f"MISSING: {f}")
        elif sha256(SRC / f) != sha256(DIST / f):
            problems.append(f"DIFFERS: {f}")
    return problems


def verify_dist_hygiene() -> list:
    """返回 dist/ 顶层的意外条目；空列表 = 干净。

    只允许 DIST 一个发布目录。历史遗留的陈旧发布包（如 _release/，曾长期
    停在旧版本并与现行发布包版本冲突）必须被拦下——否则它会持续腐烂，还会
    让任何扫 dist/ 的人读到两个互相矛盾的版本号。
    """
    root = SRC / "dist"
    if not root.exists():
        return []
    stray = []
    for entry in sorted(root.iterdir()):
        if entry.name in ALLOWED_DIST_ENTRIES:
            continue
        kind = "dir" if entry.is_dir() else "file"
        stray.append(f"{entry.name} ({kind})")
    return stray


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-only", action="store_true")
    ap.add_argument("--keep-state", action="store_true")
    args = ap.parse_args()

    if args.check_only:
        if not DIST.exists():
            print("OUT_OF_SYNC  dist 不存在，先运行构建")
            sys.exit(1)
        problems = verify()
        stray = verify_dist_hygiene()
        if problems or stray:
            print("OUT_OF_SYNC")
            for p in problems:
                print("  " + p)
            for s in stray:
                print(f"  STRAY_DIR: dist/{s}")
            sys.exit(1)
        print("IN_SYNC  dist 与源一致")
        return

    build(keep_state=args.keep_state)
    problems = verify()
    stray = verify_dist_hygiene()
    if problems or stray:
        print("BUILD_DONE_BUT_DIFFERS")
        for p in problems:
            print("  " + p)
        for s in stray:
            print(f"  STRAY_DIR: dist/{s}")
        sys.exit(1)
    total = sum(1 for _ in DIST.rglob("*") if _.is_file())
    print(f"BUILD_OK  dist 已同步（{total} 个文件），manifest.json 已生成（v{VERSION}）")


if __name__ == "__main__":
    main()
