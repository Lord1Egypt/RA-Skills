#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search_kb.py — 知识库安全检索（替代"把关键词拼进 shell 命令"的写法）

语言 / Language：输出默认中文，**语言可选**（用英文或其他语言提问就用该语言回应）。

为什么需要它：关键词、目录都是**用户可控文本**。把它拼进 shell 命令（
`Select-String -Pattern "<关键词>"` / `grep "<关键词>"`）会被 shell 解析，
文本里的引号、反引号、`$()`、`;` 就可能变成命令（命令注入）。
本脚本用 **argv 传参**（不经过 shell 解析），并对路径与输出量做限制。

安全边界（读与写**双向**都受知识库根约束，共用 scripts/pathguard.py）：
  1. 目标根目录必须存在且是目录，先解析成**真实路径**（realpath，解开符号链接），
     之后所有搜索、列举都只在这个真实根路径内进行。
  2. **读取侧容器校验**：每个候选文件都解析真实路径（解符号链接）并校验是否仍在
     知识库根内；**越界的条目直接跳过并计数** —— 不打开、不读取库外文件。
  3. **符号链接目录一律不进入遍历**（`os.walk(followlinks=False)` + 显式剪枝），
     既避免绕出库外，也避免链接成环。
  4. 关键词按**字面量**匹配（不按正则编译），避免正则注入 / 灾难性回溯。
  5. 结果条数、单文件读取量、单文件体积、扫描文件数都有上限（防一次拉爆上下文）。
  6. **不写任何文件**；只读。

用法：
    python search_kb.py <kb-root> <keyword> [--ext md,txt] [--max-hits 50]
    python search_kb.py <kb-root> --list [--max-files 100]     # 列举文件
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pathguard  # noqa: E402

# Windows 控制台 GBK 无法输出 emoji/中文混合，强制 UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DEFAULT_EXTS = ("md", "txt")
MAX_HITS = 50
MAX_FILES = 100
MAX_LINE_CHARS = 200
MAX_FILE_BYTES = 2 * 1024 * 1024      # 单文件最多读 2 MB
MAX_SCAN = 5000                       # 单次运行最多扫描的文件数（search 与 list 共用）
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", ".idea", ".vscode"}


class ScanStats:
    """遍历统计：本脚本只读，越界条目一律跳过并计数（不读库外文件）。"""

    def __init__(self) -> None:
        self.scanned = 0        # 通过边界校验、真正参与检索的文件数
        self.escaped = 0        # 真实路径越出知识库根（多为符号链接）→ 跳过

    def summary(self) -> str:
        extra = f"，已跳过 {self.escaped} 个越界符号链接（未读取库外文件）" if self.escaped else ""
        return f"扫描 {self.scanned} 个文件{extra}"


def resolve_root(root: str) -> str:
    """校验知识库根目录：必须存在、是目录，返回**真实路径**（解符号链接）作为基准。"""
    try:
        return pathguard.real_root(root)
    except pathguard.PathEscapeError:
        path = os.path.abspath(os.path.expanduser(str(root)))
        print(f"ERROR: 知识库目录不存在或不是目录：{path}", file=sys.stderr)
        sys.exit(2)


def iter_files(root: str, exts: tuple[str, ...], stats: ScanStats, max_scan: int = MAX_SCAN):
    """遍历真实根内的文件，逐个过读取边界；越界条目跳过并计数。

    产出 (显示用相对路径, 通过校验的真实路径) —— 读取一律使用后者。
    """
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        # 跳过隐藏目录与常见缓存目录；**符号链接目录不进入**（不跟着链接走）
        dirnames[:] = [
            d for d in dirnames
            if not d.startswith(".") and d not in SKIP_DIRS
            and not os.path.islink(os.path.join(dirpath, d))
        ]
        for name in sorted(filenames):
            if name.startswith("."):
                continue
            if exts and os.path.splitext(name)[1].lower().lstrip(".") not in exts:
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            try:
                # 读取闸：解符号链接后仍须落在知识库真实根内，否则跳过（fail closed）
                real = pathguard.read_within(root, full, what=f"读取目标 {rel}")
            except pathguard.PathEscapeError:
                stats.escaped += 1
                continue
            stats.scanned += 1
            if stats.scanned > max_scan:
                # 扫描预算：防止超大知识库 + 罕见关键词导致长时间遍历
                print(f"...（已达扫描上限 {max_scan} 个文件，用 --max-scan 调整）", file=sys.stderr)
                return
            yield rel, real


def list_files(root: str, exts: tuple[str, ...], max_files: int, stats: ScanStats,
               max_scan: int = MAX_SCAN) -> int:
    count = 0
    for rel, real in iter_files(root, exts, stats, max_scan):
        try:
            size = os.path.getsize(real)
        except OSError:
            size = -1
        print(f"{rel}\t{size}")
        count += 1
        if count >= max_files:
            print(f"...（已达上限 {max_files}，用 --max-files 调整）")
            break
    print(f"\n共列出 {count} 个文件（{stats.summary()}；根目录：{root}）")
    return 0


def search(root: str, keyword: str, exts: tuple[str, ...], max_hits: int, stats: ScanStats,
           max_scan: int = MAX_SCAN) -> int:
    """按字面量搜索关键词。关键词作为数据比对，不参与任何命令/正则解析。"""
    if not keyword:
        print("ERROR: 关键词不能为空", file=sys.stderr)
        return 2
    hits = 0
    for rel, real in iter_files(root, exts, stats, max_scan):
        try:
            if os.path.getsize(real) > MAX_FILE_BYTES:
                continue
            with open(real, "r", encoding="utf-8", errors="replace") as fh:
                for lineno, line in enumerate(fh, 1):
                    if keyword in line:                 # ← 纯字面量包含判断
                        text = line.strip()[:MAX_LINE_CHARS]
                        print(f"{rel}:{lineno}: {text}")
                        hits += 1
                        if hits >= max_hits:
                            print(f"...（已达上限 {max_hits} 条，用 --max-hits 调整）")
                            return 0
        except (OSError, UnicodeError):
            continue
    print(f"\n{stats.summary()}，命中 {hits} 条（根目录：{root}）")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="知识库安全检索（argv 传参，无 shell 解析；读取限制在知识库内）")
    parser.add_argument("kb_root", help="知识库根目录（所有搜索都限制在该目录内）")
    parser.add_argument("keyword", nargs="?", default="", help="搜索关键词（按字面量匹配）")
    parser.add_argument("--ext", default=",".join(DEFAULT_EXTS),
                        help=f"限定扩展名（逗号分隔，默认 {','.join(DEFAULT_EXTS)}）")
    parser.add_argument("--max-hits", type=int, default=MAX_HITS, help=f"最多返回条数（默认 {MAX_HITS}）")
    parser.add_argument("--max-files", type=int, default=MAX_FILES, help=f"列举模式下最多文件数（默认 {MAX_FILES}）")
    parser.add_argument("--max-scan", type=int, default=MAX_SCAN, help=f"单次运行最多扫描的文件数（默认 {MAX_SCAN}）")
    parser.add_argument("--list", action="store_true", help="只列举文件，不搜索")
    args = parser.parse_args()

    root = resolve_root(args.kb_root)
    exts = tuple(e.strip().lower().lstrip(".") for e in args.ext.split(",") if e.strip())
    stats = ScanStats()
    print(f"[kb] 检索范围：{root}（只读；扩展名 {','.join(exts) or '全部'}）")
    if args.list or not args.keyword:
        return list_files(root, exts, args.max_files, stats, args.max_scan)
    return search(root, args.keyword, exts, args.max_hits, stats, args.max_scan)


if __name__ == "__main__":
    raise SystemExit(main())
