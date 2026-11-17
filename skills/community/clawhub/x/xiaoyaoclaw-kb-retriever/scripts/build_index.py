# -*- coding: utf-8 -*-
"""自动扫描知识库目录，生成/补齐 data_structure.md 分层索引骨架。

⚠️ 这是**可选的维护脚本，不是检索**：它会在知识库目录内**新建/覆盖** `data_structure.md`。
必须在用户明确要求「建/补索引」并确认后运行；只写 `data_structure.md`，不删不改其它文件。

语言 / Language：输出默认中文，**语言可选**。

用法:
    python build_index.py <kb-root> [--force]

说明:
    - 遍历 <kb-root> 下的目录树，为每个含内容的目录生成/补齐 data_structure.md
    - 已存在 data_structure.md 的目录默认跳过（--force 时覆盖重建）
    - 目录用途推断来源：README.md 首段 / 文件名聚类 / 目录名
    - 输出符合 kb-retriever 索引规范（Purpose / Files / Coverage 三段式）
    - Windows / macOS 双平台通用（纯 Python，无外部依赖）

安全边界 / Safety（读 + 写）:
    - 只新建/覆盖知识库内的 `data_structure.md`，不改不删其它文件
    - **读取侧容器校验**：读取 README、读取文件体积等操作，同样先把目标解析成
      真实路径（解符号链接）并校验仍在知识库根内；越界的条目**跳过并计数**，
      不读取库外文件
    - **写入目标按真实路径校验**（scripts/pathguard.py）：解析符号链接后仍必须
      落在知识库根内，否则拒绝；**符号链接目录一律不进入遍历**（既不读也不写）
    - 运行前打印将写入的根目录；本操作需用户点名并确认

示例:
    python build_index.py knowledge            # 为 knowledge/ 生成索引
    python build_index.py knowledge --force    # 全部重建
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pathguard  # noqa: E402

INDEX_NAME = "data_structure.md"
README_NAME = "README.md"
TEXT_EXTS = {".md", ".txt", ".log", ".markdown"}
DOC_EXTS = {".pdf", ".xlsx", ".xls", ".docx", ".csv", ".json", ".yaml", ".yml"}
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", ".obsidian", ".idea", ".vscode"}


def infer_purpose(directory, root):
    """从 README 首段 / 目录名推断用途描述（README 读取同样过边界校验）。"""
    readme = os.path.join(directory, README_NAME)
    if os.path.isfile(readme):
        try:
            # 读取闸：解符号链接后必须仍在知识库真实根内
            real_readme = pathguard.read_within(root, readme, what="读取目标（README）")
            with open(real_readme, "r", encoding="utf-8-sig") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        return line[:120]
        except pathguard.PathEscapeError:
            pass
        except Exception:
            pass
    # 回退：目录名
    name = os.path.basename(directory) or directory
    return f"{name} 相关文档与数据"


def scan_directory(directory, root, stats):
    """扫描目录，返回 (子目录列表, 业务文件列表)。越界（符号链接）条目跳过并计数。"""
    subdirs, files = [], []
    try:
        entries = sorted(os.listdir(directory))
    except OSError as e:
        print(f"  跳过不可读目录 {directory}: {e}", file=sys.stderr)
        return [], []
    for entry in entries:
        if entry.startswith("."):
            continue
        full = os.path.join(directory, entry)
        try:
            # 读取闸：条目真实路径必须仍在知识库根内，否则跳过（不读库外文件）
            pathguard.read_within(root, full, what=f"读取目标 {entry}")
        except pathguard.PathEscapeError:
            stats["read_escaped"] += 1
            continue
        if os.path.isdir(full):
            if entry not in SKIP_DIRS:
                subdirs.append(entry)
        elif os.path.isfile(full):
            ext = os.path.splitext(entry)[1].lower()
            # README / 索引文件是说明文件，不作为业务文件列出
            if entry in (INDEX_NAME, README_NAME):
                continue
            if ext in TEXT_EXTS or ext in DOC_EXTS:
                files.append(entry)
    return subdirs, files


def format_size(path):
    try:
        size = os.path.getsize(path)
        if size >= 1024 * 1024:
            return f"{size / 1024 / 1024:.1f}MB"
        if size >= 1024:
            return f"{size / 1024:.0f}KB"
        return f"{size}B"
    except OSError:
        return "?"


def generate_index(directory, subdirs, files, root):
    """生成 data_structure.md 内容。"""
    name = os.path.basename(directory) or directory
    lines = [f"# {name}", ""]
    lines.append("## Purpose")
    lines.append(infer_purpose(directory, root))
    lines.append("")
    lines.append("## Files")
    if not subdirs and not files:
        lines.append("- （空目录）")
    for sub in subdirs:
        lines.append(f"- {sub}/ — 子目录，详见其 data_structure.md")
    for fname in files:
        full = os.path.join(directory, fname)
        ext = os.path.splitext(fname)[1].lower()
        kind = "PDF 文档" if ext == ".pdf" else ("表格数据" if ext in (".xlsx", ".xls") else "文本/Markdown")
        lines.append(f"- {fname} — {kind}（{format_size(full)}）")
    lines.append("")
    lines.append("## Coverage")
    lines.append("（待补充：时间范围 / 版本 / 来源说明）")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="生成知识库 data_structure.md 分层索引")
    parser.add_argument("kb_root", help="知识库根目录")
    parser.add_argument("--force", action="store_true", help="覆盖已有索引")
    args = parser.parse_args()

    root = os.path.abspath(os.path.expanduser(args.kb_root))
    if not os.path.isdir(root):
        print(f"错误: 目录不存在 {root}", file=sys.stderr)
        sys.exit(1)
    # 真实路径（解掉根目录自身的符号链接）——后续所有容器校验都以它为基准
    root = pathguard.real_root(root)

    print(f"[write] 将在下列目录内写入/更新 {INDEX_NAME}（只动这一个文件）：{root}")

    generated, skipped, empty, escaped = 0, 0, 0, 0
    stats = {"read_escaped": 0}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        # 跳过隐藏目录与 SKIP_DIRS；**符号链接目录一律不进入**（防越界/防环）
        dirnames[:] = [
            d for d in dirnames
            if not d.startswith(".") and d not in SKIP_DIRS
            and not os.path.islink(os.path.join(dirpath, d))
        ]
        if dirpath != root and os.path.basename(dirpath).startswith("."):
            continue

        subdirs, files = scan_directory(dirpath, root, stats)
        if not subdirs and not files:
            empty += 1
            continue

        raw_index_path = os.path.join(dirpath, INDEX_NAME)
        # ★ 先用**未被解析的原始路径**判断是否为符号链接：assert_within 会把路径
        #   解析成真实路径，解析之后 islink() 恒为 False，这个检查就白做了。
        #   索引只允许是普通文件或不存在 —— 库内一个指向其它文档的 data_structure.md
        #   链接，在 --force 下会被当成索引覆盖，等于截断那份文档。
        if os.path.islink(raw_index_path):
            escaped += 1
            print(f"  跳过（索引文件是符号链接，拒绝覆盖）: {os.path.relpath(raw_index_path, root)}",
                  file=sys.stderr)
            continue
        # 唯一写盘闸：解析符号链接后必须仍在根目录内（fail closed）
        try:
            index_path = pathguard.assert_within(root, raw_index_path, what="索引文件")
        except pathguard.PathEscapeError as exc:
            escaped += 1
            print(f"  跳过（越界，可能是符号链接）: {exc}", file=sys.stderr)
            continue
        if os.path.exists(index_path) and not args.force:
            skipped += 1
            print(f"跳过（已有索引）: {os.path.relpath(index_path, root)}")
            continue
        if os.path.exists(index_path) and not os.path.isfile(index_path):
            escaped += 1
            print(f"  跳过（索引路径不是普通文件）: {os.path.relpath(index_path, root)}",
                  file=sys.stderr)
            continue

        content = generate_index(dirpath, subdirs, files, root)
        # 独占临时文件 + 原子替换：不会截断既有文件、也不会写穿链接
        tmp_path = f"{index_path}.tmp-{os.getpid()}"
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
        try:
            fd = os.open(tmp_path, flags, 0o600)
        except OSError as exc:
            escaped += 1
            print(f"  跳过（无法创建临时索引）：{exc}", file=sys.stderr)
            continue
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
                f.write(content)
            os.replace(tmp_path, index_path)
        except OSError as exc:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            escaped += 1
            print(f"  跳过（写入索引失败）：{exc}", file=sys.stderr)
            continue
        generated += 1
        rel = os.path.relpath(index_path, root)
        print(f"生成: {rel}（{len(subdirs)} 子目录, {len(files)} 文件）")

    print(f"\n完成: 生成 {generated}，跳过 {skipped}，空目录 {empty}"
          + (f"，越界拒绝写入 {escaped}" if escaped else "")
          + (f"，越界跳过读取 {stats['read_escaped']}（未读库外文件）" if stats["read_escaped"] else ""))
    if generated == 0 and skipped == 0:
        print("提示: 知识库为空，或所有目录均无业务文件。")


if __name__ == "__main__":
    main()
