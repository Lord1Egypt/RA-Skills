# -*- coding: utf-8 -*-
"""把 PDF 每页转成 PNG 图片（扫描件 OCR 路径的可选前置步骤）。

⚠️ 这是**可选维护脚本**：会在 <output_dir> 下新建 `page_N.png`（不改源 PDF）。
必须在用户明确要求处理扫描件并确认后运行。

安全边界 / Safety（读 + 写）:
    - **读盘边界**：源 PDF 必须是**真实路径**上的普通文件 —— 路径中任一段是**符号链接
      一律拒绝**（`scripts/pathguard.py` 的 `require_real_file`，fail closed），因此本脚本
      绝不会"跟着链接"读到知识库之外；被拒时报错会回显真实位置，改用真实路径即可。
    - **写盘披露**：运行前打印将写入的目录；只新建 PNG，不删不改其它文件。
    - **写入范围**：<output_dir> 必须位于**显式传入的知识库根**（--root）内，且仍在源 PDF 所在
      目录树内；按真实路径校验（解符号链接后仍须在根内，越界即拒绝）
    - **逐页校验写目标**：每个 `page_N.png` 都单独检查（在根内、非符号链接、非目录）——
      只校验目录是不够的：库内一个指向库外的 `page_1.png` 链接会把这次写入带出去
    - 依赖 `pdf2image`（版本见 requirements-optional.txt），并需系统级 poppler；安装前须告知用户并取得确认。

语言 / Language：输出默认中文，**语言可选**（可按用户语言调整文案）。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pathguard  # noqa: E402

from pdf2image import convert_from_path  # 可选依赖，版本见 requirements-optional.txt


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(2)


def resolve_root(root_arg: str) -> str:
    """知识库根：必须显式给出、已存在的真实目录（不接受根本身是软链）。"""
    try:
        root = pathguard.real_root(root_arg)
    except pathguard.PathEscapeError as exc:
        fail(str(exc))
    if os.path.islink(os.path.abspath(os.path.expanduser(root_arg))):
        fail(f"知识库根不得是符号链接：{root_arg}")
    return root


def resolve_source(pdf_path: str, root: str) -> str:
    """源 PDF：真实路径、普通文件、任一段无符号链接，且**在知识库根内**。"""
    try:
        source = pathguard.require_real_file(pdf_path, what="源 PDF")
    except pathguard.PathEscapeError as exc:
        fail(str(exc))
    if not pathguard.is_within(root, pathguard.real_target(source)):
        fail(f"源 PDF 越出知识库根（{root}），已拒绝：{pdf_path}")
    return source


def resolve_output_within(pdf_path: str, output_dir: str) -> str:
    """校验输出目录：解析符号链接后，必须落在源 PDF 所在的（真实）目录树内。"""
    root = pathguard.real_root(os.path.dirname(os.path.abspath(os.path.expanduser(pdf_path))))
    resolved = pathguard.real_target(output_dir)
    if not pathguard.is_within(root, resolved, allow_equal=True):
        fail(f"输出目录必须位于源 PDF 所在目录内（{root}），已拒绝：{output_dir} -> {resolved}")
    return resolved


def safe_image_target(output_dir: str, root: str, index: int) -> str:
    """逐页校验写目标：在根内、非符号链接、非目录、**且尚不存在**。

    只新建、不覆盖是本脚本对外的承诺：既有的 `page_N.png` 可能是用户上一轮
    手工挑过的结果，覆盖等于销毁它。存在即跳过（调用方打印原因）。
    """
    target = os.path.join(output_dir, f"page_{index}.png")
    resolved = pathguard.real_target(target)
    if not pathguard.is_within(root, resolved, allow_equal=True):
        fail(f"写目标越出知识库根（{root}），已拒绝：{target} -> {resolved}")
    if os.path.islink(target):
        fail(f"写目标是符号链接，拒绝写入（避免覆盖链接指向的文件）：{target}")
    if os.path.isdir(target):
        fail(f"写目标是目录，拒绝写入：{target}")
    if os.path.exists(target):
        return ""     # 已存在：跳过，不覆盖
    return target


# Converts each page of a PDF to a PNG image.


def convert(pdf_path, output_dir, root, max_dim=1000):
    os.makedirs(output_dir, exist_ok=True)
    print(f"[write] 将把每页 PNG 写入：{output_dir}（源 PDF 不改动）")
    images = convert_from_path(pdf_path, dpi=200)

    for i, image in enumerate(images):
        # Scale image if needed to keep width/height under `max_dim`
        width, height = image.size
        if width > max_dim or height > max_dim:
            scale_factor = min(max_dim / width, max_dim / height)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            image = image.resize((new_width, new_height))

        # 逐页校验（不只看目录）：目标必须在根内、不是链接、不是目录
        image_path = safe_image_target(output_dir, root, i + 1)
        if not image_path:
            print(f"跳过 page_{i+1}.png（已存在，不覆盖）")
            continue
        image.save(image_path)
        print(f"Saved page {i+1} as {image_path} (size: {image.size})")

    print(f"Converted {len(images)} pages to PNG images")


if __name__ == "__main__":
    # 用法：convert_pdf_to_images.py --root <知识库根> <input.pdf> <output_dir>
    argv = sys.argv[1:]
    if len(argv) < 4 or argv[0] not in ("--root", "-r"):
        print("Usage: convert_pdf_to_images.py --root <knowledge base root> "
              "<input pdf> <output directory>", file=sys.stderr)
        sys.exit(1)
    root = resolve_root(argv[1])
    source_pdf = resolve_source(argv[2], root)
    output_directory = resolve_output_within(source_pdf, argv[3])
    print(f"[read]  知识库根：{root}")
    print(f"[read]  源 PDF（真实路径，无符号链接，在根内）：{source_pdf}")
    convert(source_pdf, output_directory, root)
