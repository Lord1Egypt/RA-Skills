#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inspect_doc.py — .docx 交付前检查工具。

基于 python-docx 与 zipfile 直接读取 docx 内部 XML，检查并报告：
    - 文档引用的所有字体（含 eastAsia 中文字体）清单；
    - 显式分页符（w:br w:type="page"）与分节符（w:sectPr）数量；
    - 批注（word/comments.xml）与修订（w:ins / w:del）残留数量；
    - 输出“可交付 / 需处理”结论（有批注或修订残留时判为需处理）。

用法：
    python scripts/inspect_doc.py <文件.docx>

依赖：python-docx（pip install python-docx）。
"""

import argparse
import os
import sys
import zipfile

try:
    from docx import Document  # noqa: F401  （验证依赖可用）
    _DOCX_OK = True
except ImportError:
    _DOCX_OK = False

import xml.etree.ElementTree as ET

# WordprocessingML 命名空间
NS_W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

# 需要扫描正文的 docx 内部部件
BODY_PARTS = ["word/document.xml"]
EXTRA_PART_PATTERNS = ("word/header", "word/footer")


def read_part(zf, name):
    """读取 zip 内某个部件的字节内容，不存在时返回 None。"""
    try:
        return zf.read(name)
    except KeyError:
        return None


def collect_fonts(root):
    """从 XML 树中收集所有 rFonts 引用到的字体名（ascii / eastAsia / hAnsi / cs）。"""
    fonts = set()
    for rfonts in root.iter(NS_W + "rFonts"):
        for attr in ("ascii", "eastAsia", "hAnsi", "cs"):
            value = rfonts.get(NS_W + attr)
            if value:
                fonts.add(value)
    return fonts


def inspect(path):
    """执行检查，返回结论字符串。"""
    if not os.path.isfile(path):
        print(f"[错误] 找不到文件：{path}")
        sys.exit(1)
    if not zipfile.is_zipfile(path):
        print(f"[错误] {path} 不是有效的 .docx 文件（docx 本质上是 zip 包）。")
        sys.exit(1)

    fonts = set()
    page_breaks = 0
    section_breaks = 0
    insertions = 0
    deletions = 0
    comments = 0

    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        # 扫描正文与页眉页脚
        body_parts = list(BODY_PARTS) + [
            n for n in names if n.startswith(EXTRA_PART_PATTERNS) and n.endswith(".xml")
        ]
        for part in body_parts:
            data = read_part(zf, part)
            if data is None:
                continue
            root = ET.fromstring(data)
            fonts |= collect_fonts(root)
            for br in root.iter(NS_W + "br"):
                if br.get(NS_W + "type") == "page":
                    page_breaks += 1
            section_breaks += sum(1 for _ in root.iter(NS_W + "sectPr"))
            insertions += sum(1 for _ in root.iter(NS_W + "ins"))
            deletions += sum(1 for _ in root.iter(NS_W + "del"))

        # 批注
        comments_data = read_part(zf, "word/comments.xml")
        if comments_data:
            comments_root = ET.fromstring(comments_data)
            comments = sum(1 for _ in comments_root.iter(NS_W + "comment"))

        # 文档默认字体（styles.xml 中的 docDefaults 也一并算入字体清单）
        styles_data = read_part(zf, "word/styles.xml")
        if styles_data:
            fonts |= collect_fonts(ET.fromstring(styles_data))

    revisions = insertions + deletions

    print(f"[文件] {path}")
    print(f"[字体] 共引用 {len(fonts)} 种字体：")
    if fonts:
        for f in sorted(fonts):
            print(f"  - {f}")
    else:
        print("  （未发现显式字体引用，可能全部继承默认样式）")
    print(f"[分页/分节] 显式分页符 {page_breaks} 处，分节符 {section_breaks} 处。")
    print(f"[批注/修订] 批注 {comments} 条，修订 {revisions} 处（插入 {insertions}、删除 {deletions}）。")

    if comments > 0 or revisions > 0:
        print("[结论] 需处理：存在批注或修订残留，请在 WPS/Word 中接受/拒绝修订并删除批注后再交付。")
        return "需处理"
    print("[结论] 可交付：未发现批注或修订残留。")
    return "可交付"


def main():
    parser = argparse.ArgumentParser(
        description=".docx 交付前检查：字体清单、分页/分节符、批注与修订残留，并给出“可交付 / 需处理”结论。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例：\n  python scripts/inspect_doc.py 合同草案-v2.docx",
    )
    parser.add_argument("file", help="待检查的 .docx 文件")
    args = parser.parse_args()

    if not _DOCX_OK:
        print("[错误] 缺少第三方库 python-docx，请先安装：")
        print("       pip install python-docx")
        sys.exit(2)

    inspect(args.file)


if __name__ == "__main__":
    main()
