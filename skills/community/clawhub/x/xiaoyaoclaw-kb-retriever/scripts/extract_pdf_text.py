# -*- coding: utf-8 -*-
"""双平台通用 PDF 文本提取（pdfplumber）。

用法:
    python extract_pdf_text.py --root <知识库根> <input.pdf> <output.txt> [start_page] [end_page]

示例:
    python extract_pdf_text.py --root ~/knowledge doc.pdf doc.txt      # 全部页
    python extract_pdf_text.py --root ~/knowledge doc.pdf doc.txt 1 5  # 第 1-5 页

说明:
    - Windows / macOS 行为一致（纯 Python，无 poppler 依赖）
    - 输出写入文件而非 stdout，避免占用 LLM token

安全边界 / Safety（读 + 写）:
    - **读盘边界**：源 PDF 必须是**真实路径**上的普通文件 —— 路径中任一段是**符号链接
      一律拒绝**（`scripts/pathguard.py` 的 `require_real_file`，fail closed），
      因此本脚本绝不会"跟着链接"读到知识库之外；被拒时报错会回显真实位置，改用真实路径即可。
    - **写盘披露**：本脚本会新建/覆盖 <output.txt>（仅此一个文件，源 PDF 不动）；
      运行前会打印将写入的绝对路径。
    - **写入范围**：<output.txt> 与 <input.pdf> 都必须位于**显式传入的知识库根**（--root）内，
      按真实路径校验（解符号链接后仍须在根内，越界即拒绝）；根目录须显式给出，
      不再"从源文件目录倒推"——否则一个库外 PDF 就能把边界带出去。
    - **不破坏原件**：目标与源 PDF 若是同一文件（含硬链接）→ 拒绝；目标已存在且是符号链接 → 拒绝；
      写入采用「独占临时文件 + 原子替换」，替换的是目录项本身，不会写穿链接。
    - **本操作需用户点名并确认**：把 PDF 转成文本文件属派生写入，不是纯检索。

语言 / Language：输出默认中文，**语言可选**（可按用户语言调整文案）。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pathguard  # noqa: E402

import pdfplumber  # 可选依赖，版本见 requirements-optional.txt


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(2)


def resolve_root(root_arg: str) -> str:
    """知识库根：必须是已存在的**真实目录**（不允许库根本身是软链）。"""
    try:
        root = pathguard.real_root(root_arg)
    except pathguard.PathEscapeError as exc:
        fail(str(exc))
    if os.path.islink(os.path.abspath(os.path.expanduser(root_arg))):
        fail(f"知识库根不得是符号链接：{root_arg}")
    return root


def resolve_source(pdf_path: str, root: str) -> str:
    """源 PDF：真实路径、普通文件、任一段无符号链接，且必须**在知识库根内**。"""
    try:
        source = pathguard.require_real_file(pdf_path, what="源 PDF")
    except pathguard.PathEscapeError as exc:
        fail(str(exc))
    if not pathguard.is_within(root, pathguard.real_target(source)):
        fail(f"源 PDF 越出知识库根（{root}），已拒绝：{pdf_path}")
    return source


def resolve_output(out_path: str, root: str, source_pdf: str) -> str:
    """输出：真实路径须在知识库根内、不得等同于源 PDF、不得是符号链接。"""
    resolved = pathguard.real_target(out_path)
    if not pathguard.is_within(root, resolved) or resolved == root:
        fail(f"输出文件越出知识库根（{root}），已拒绝：{out_path} -> {resolved}")
    if os.path.islink(os.path.abspath(os.path.expanduser(out_path))):
        fail(f"输出文件是符号链接，拒绝写入（避免覆盖链接指向的文件）：{out_path}")
    # 目标与源是同一文件（含硬链接）→ 写入会截断源 PDF
    try:
        if os.path.exists(resolved) and os.path.samefile(resolved, source_pdf):
            fail(f"输出文件与源 PDF 是同一文件，拒绝写入（会破坏原件）：{out_path}")
    except OSError:
        pass
    if os.path.normcase(resolved) == os.path.normcase(os.path.realpath(source_pdf)):
        fail(f"输出文件与源 PDF 是同一路径，拒绝写入：{out_path}")
    return resolved


def write_text_atomically(dest: str, text: str) -> None:
    """独占临时文件 + 原子替换：目标若是链接，替换的是链接本身而非其指向。"""
    tmp = f"{dest}.tmp-{os.getpid()}"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
    fd = os.open(tmp, flags, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        os.replace(tmp, dest)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def main():
    # 用法：extract_pdf_text.py --root <知识库根> <input.pdf> <output.txt> [start] [end]
    argv = sys.argv[1:]
    if len(argv) < 3 or argv[0] not in ("--root", "-r"):
        print(
            "用法: python extract_pdf_text.py --root <知识库根目录> <input.pdf> <output.txt> "
            "[start_page] [end_page]",
            file=sys.stderr,
        )
        sys.exit(1)
    root_arg, input_pdf, output_txt = argv[1], argv[2], argv[3]
    start = int(argv[4]) if len(argv) > 4 else 1
    end = int(argv[5]) if len(argv) > 5 else None

    root = resolve_root(root_arg)
    source_pdf = resolve_source(input_pdf, root)
    output_txt = resolve_output(output_txt, root, source_pdf)
    print(f"[read]  知识库根：{root}")
    print(f"[read]  源 PDF（真实路径，无符号链接，在根内）：{source_pdf}")
    print(f"[write] 将写入派生文本文件：{output_txt}（源 PDF 不改动）")

    chunks: list[str] = []
    with pdfplumber.open(source_pdf) as pdf:
        total = len(pdf.pages)
        end = end or total
        for i in range(max(1, start) - 1, min(end, total)):
            text = pdf.pages[i].extract_text() or ""
            chunks.append(f"--- Page {i + 1} ---\n{text}\n")
    write_text_atomically(output_txt, "".join(chunks))
    print(f"OK: {source_pdf} -> {output_txt} ({end - start + 1} pages)")


if __name__ == "__main__":
    main()
