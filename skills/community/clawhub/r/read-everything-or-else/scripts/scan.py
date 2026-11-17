#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scan.py - 把「用户指定的东西」展开成逐条可打卡的清单（manifest）。

零依赖，Python 3.8+。

用法:
    python scan.py <TARGET> [<TARGET> ...] -o <WORKDIR> [--chunk 600] [--all]
                   [--include "*.md" ...] [--exclude "*.lock" ...]

TARGET 可以是文件、目录、glob 表达式。

产出:
    <WORKDIR>/manifest.tsv   每条一行；必须逐条在 ledger.tsv 打卡
    <WORKDIR>/excluded.txt   被排除的路径（留痕，禁止默默跳过）

kind 含义:
    text    可直接读取的文本块（start/end 为 1-based 行号，可回查摘录）
    doc     需要专用工具打开的文档（pdf/docx/xlsx/pptx）
    media   图片/音频/视频（必须真实打开或抽帧看，不能只读文件名）
    binary  其他二进制（exe/dll/zip/...，需要说明无法读取的理由）
"""

import argparse
import fnmatch
import glob
import hashlib
import os
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SKIP_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "__pycache__", ".venv", "venv",
    ".mypy_cache", ".pytest_cache", ".ruff_cache", ".tox", ".next", ".nuxt",
    ".turbo", ".parcel-cache", ".gradle", ".idea", ".vscode", ".cache",
    "dist", "build", "target", ".terraform", ".eggs", ".ipynb_checkpoints",
}

DOC_EXT = {".pdf", ".docx", ".xlsx", ".pptx", ".doc", ".xls", ".ppt",
           ".epub", ".mobi", ".azw3", ".odt", ".ods", ".odp", ".rtf"}
MEDIA_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff",
             ".psd", ".ai", ".svg", ".ico", ".heic", ".avif",
             ".mp4", ".mov", ".mkv", ".avi", ".webm", ".flv", ".wmv", ".m4v",
             ".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac", ".aiff", ".opus"}
BINARY_EXT = {".exe", ".dll", ".so", ".dylib", ".bin", ".obj", ".o", ".a",
              ".lib", ".pyc", ".pyd", ".class", ".jar", ".war", ".zip", ".7z",
              ".rar", ".gz", ".bz2", ".xz", ".tar", ".iso", ".db", ".sqlite",
              ".sqlite3", ".woff", ".woff2", ".ttf", ".otf", ".eot", ".blend",
              ".fbx", ".glb", ".gltf", ".uasset", ".umap", ".mat", ".npy",
              ".npz", ".pt", ".pth", ".onnx", ".safetensors", ".ckpt"}


def sniff_kind(p: Path) -> str:
    ext = p.suffix.lower()
    if ext in DOC_EXT:
        return "doc"
    if ext in MEDIA_EXT:
        return "media"
    if ext in BINARY_EXT:
        return "binary"
    try:
        with open(p, "rb") as f:
            head = f.read(8192)
    except OSError:
        return "binary"
    if b"\x00" in head:
        return "binary"
    return "text"


def read_lines(p: Path):
    with open(p, "rb") as f:
        raw = f.read()
    for enc in ("utf-8-sig", "utf-8", "gb18030", "big5"):
        try:
            return raw.decode(enc).splitlines()
        except (UnicodeDecodeError, LookupError):
            continue
    return raw.decode("utf-8", errors="replace").splitlines()


def chunk_ranges(lines, size):
    """按行切片，尽量把块尾落在空行/标题上，读起来断得干净。"""
    n = len(lines)
    if n == 0:
        yield (1, 0)
        return
    start = 0
    while start < n:
        end = min(start + size, n)
        if end < n:
            look_to = min(end + 80, n)
            for i in range(end, look_to):
                s = lines[i].strip()
                if s == "" or s.startswith("#"):
                    end = i + 1 if s == "" else i
                    break
            if end <= start:
                end = min(start + size, n)
        yield (start + 1, end)
        start = end


def sha1_of(lines, s, e):
    body = "\n".join(lines[s - 1:e]) if e >= s else ""
    return hashlib.sha1(body.encode("utf-8", errors="replace")).hexdigest()[:12]


def match_filters(p: Path, includes, excludes) -> bool:
    name = p.name
    posix = p.as_posix()
    if includes and not any(fnmatch.fnmatch(name, g) or fnmatch.fnmatch(posix, g)
                            for g in includes):
        return False
    if excludes and any(fnmatch.fnmatch(name, g) or fnmatch.fnmatch(posix, g)
                        for g in excludes):
        return False
    return True


def expand(targets, includes, excludes, keep_all, outdir=None):
    files, excluded = [], []
    for t in targets:
        pat = os.path.expanduser(t)
        cand = sorted(glob.glob(pat, recursive=True))
        if not cand:
            p = Path(pat)
            if p.exists():
                cand = [pat]
            else:
                raise SystemExit("[scan] 目标不存在或 glob 无匹配: %s" % t)
        for c in cand:
            p = Path(c)
            if p.is_dir():
                for root, dirs, names in os.walk(p):
                    dirs.sort()
                    keep = []
                    for d in dirs:
                        if outdir and (Path(root) / d).resolve() == outdir:
                            excluded.append(str((Path(root) / d).resolve()) + "\t[workdir]")
                        elif d in SKIP_DIRS and not keep_all:
                            excluded.append(str((Path(root) / d).resolve()) + "\t[dir-skip]")
                        else:
                            keep.append(d)
                    dirs[:] = keep
                    for n in sorted(names):
                        fp = Path(root) / n
                        if not match_filters(fp, includes, excludes):
                            excluded.append(str(fp.resolve()) + "\t[filter]")
                            continue
                        files.append(fp.resolve())
            elif p.is_file():
                if not match_filters(p, includes, excludes):
                    excluded.append(str(p.resolve()) + "\t[filter]")
                    continue
                files.append(p.resolve())
            else:
                excluded.append(str(p) + "\t[not-a-file]")

    seen, out = set(), []
    for f in files:
        k = str(f)
        if k in seen:
            continue
        seen.add(k)
        out.append(f)
    return out, excluded


def main():
    ap = argparse.ArgumentParser(description="把目标展开成逐条可打卡的清单")
    ap.add_argument("targets", nargs="+", help="文件 / 目录 / glob")
    ap.add_argument("-o", "--out", required=True, help="工作目录（放 manifest.tsv）")
    ap.add_argument("--chunk", type=int, default=600, help="文本每块行数，默认 600")
    ap.add_argument("--include", action="append", default=[], help="只收匹配的文件")
    ap.add_argument("--exclude", action="append", default=[], help="排除匹配的文件")
    ap.add_argument("--all", action="store_true", help="不跳过 .git/node_modules 等目录")
    ap.add_argument("--base", default=None, help="label 里显示的相对基准目录")
    args = ap.parse_args()

    base = Path(args.base).resolve() if args.base else Path.cwd().resolve()
    outdir = Path(args.out).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    files, excluded = expand(args.targets, args.include, args.exclude, args.all, outdir)
    if not files:
        raise SystemExit("[scan] 没收集到任何文件，检查 target / --include / --exclude")

    rows = []
    stats = {"text": 0, "doc": 0, "media": 0, "binary": 0}
    total_lines = 0
    idx = 0

    for p in files:
        kind = sniff_kind(p)
        try:
            rel = p.relative_to(base).as_posix()
        except ValueError:
            rel = p.as_posix()
        if kind == "text":
            try:
                lines = read_lines(p)
            except OSError as e:
                rows.append(["R%04d" % (idx + 1), "binary", str(p), 0, 0,
                             p.stat().st_size, "-", "%s [读取失败:%s]" % (rel, e)])
                idx += 1
                stats["binary"] += 1
                continue
            total_lines += len(lines)
            for (s, e) in chunk_ranges(lines, args.chunk):
                idx += 1
                label = "%s:L%d-%d" % (rel, s, e) if e >= s else "%s:[空文件]" % rel
                rows.append(["R%04d" % idx, "text", str(p), s, e, max(e - s + 1, 0),
                             sha1_of(lines, s, e), label])
                stats["text"] += 1
        else:
            idx += 1
            size = p.stat().st_size
            unit = {"doc": "bytes/doc", "media": "bytes/media", "binary": "bytes"}[kind]
            rows.append(["R%04d" % idx, kind, str(p), 0, 0, size, "-",
                         "%s:%s" % (rel, unit)])
            stats[kind] += 1

    mf = outdir / "manifest.tsv"
    with open(mf, "w", encoding="utf-8", newline="") as f:
        f.write("id\tkind\tpath\tstart\tend\tunits\tsha1\tlabel\n")
        for r in rows:
            f.write("\t".join(str(x).replace("\t", " ") for x in r) + "\n")

    ex = outdir / "excluded.txt"
    with open(ex, "w", encoding="utf-8", newline="") as f:
        if excluded:
            f.write("\n".join(excluded) + "\n")
        else:
            f.write("# 无排除项\n")

    print("[scan] 文件 %d 个 -> 清单条目 %d 条" % (len(files), len(rows)))
    print("[scan] 明细: text %d / doc %d / media %d / binary %d"
          % (stats["text"], stats["doc"], stats["media"], stats["binary"]))
    print("[scan] 文本总量 %d 行（约 %d 万字符）" % (total_lines, total_lines * 30 // 10000))
    print("[scan] 清单: %s" % mf)
    print("[scan] 排除留痕: %s（%d 条）" % (ex, len(excluded)))
    if stats["doc"] or stats["media"] or stats["binary"]:
        print("[scan] 注意：doc/media/binary 条目不能用摘录回查，必须写实际观察结论")
    print("[scan] 下一步：逐条读，用 audit.py --done 打卡。全部打完再跑 audit.py 审计。")


if __name__ == "__main__":
    main()
