#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成不带图的 docx 版本。

用途：每次交付带图解析稿时，同步产出一份内容完全一致、只是移除了图片的版本。
保留：全部文字、分页标题、图片标记（如 /[pic 01：简述]/、/[pic NN]*** ... ***/）
      以及图片内容解析说明。
移除：文档正文中所有内嵌图片（DrawingML w:drawing / VML w:pict）。
不处理：内嵌 OLE 对象（本 skill 不产生此类内容）。

用法：
    python strip_images.py <带图解析稿.docx>
    python strip_images.py <带图解析稿.docx> -o <无图解析稿.docx>

默认输出文件名：<原名>_无图.docx（若原名已以 _无图 结尾则拒绝重复处理）。
"""
import argparse
import sys
from pathlib import Path


def text_version_path(src):
    """按约定推导无图版本路径：<stem>_无图<suffix>。"""
    src = Path(src)
    if src.stem.endswith("_无图"):
        return src
    return src.with_name(f"{src.stem}_无图{src.suffix}")


def _all_text_nodes(doc):
    """提取正文全部文字节点（覆盖段落、表格、文本框）。"""
    try:
        from docx.oxml.ns import qn
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("缺少 python-docx") from exc
    return [t.text or "" for t in doc.element.body.iter(qn("w:t"))]


def strip_docx_images(src, dst=None, verify=True):
    """复制 src 为 dst，并移除正文中的全部图片。

    返回 (dst_path, removed_count, verified, diff_detail)。
    """
    try:
        from docx import Document
        from docx.oxml.ns import qn
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "缺少 python-docx，请先安装：pip install python-docx"
        ) from exc

    src = Path(src)
    dst = Path(dst) if dst else text_version_path(src)
    if src.resolve() == dst.resolve():
        raise ValueError("输入与输出不能是同一个文件；请指定其它输出路径。")

    dst.parent.mkdir(parents=True, exist_ok=True)

    doc = Document(str(src))
    body = doc.element.body

    removed = 0
    for tag in ("w:drawing", "w:pict"):
        for el in list(body.iter(qn(tag))):
            parent = el.getparent()
            if parent is not None:
                parent.remove(el)
                removed += 1

    doc.save(str(dst))

    verified = False
    diff_detail = ""
    if verify:
        original = Document(str(src))
        stripped = Document(str(dst))
        a, b = _all_text_nodes(original), _all_text_nodes(stripped)
        if a == b:
            verified = True
        else:
            verified = False
            for i, (x, y) in enumerate(zip(a, b)):
                if x != y:
                    diff_detail = f"第 {i + 1} 个文字节点不一致：{x!r} != {y!r}"
                    break
            if not diff_detail:
                diff_detail = f"文字节点数量不一致：{len(a)} != {len(b)}"

    return dst, removed, verified, diff_detail


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="生成不带图的 docx 版本（文字与图片解析说明保持不变）"
    )
    ap.add_argument("src", help="带图解析稿 .docx")
    ap.add_argument("-o", "--out", default=None, help="输出路径（默认 <原名>_无图.docx）")
    ap.add_argument("--no-verify", action="store_true", help="跳过文字一致性校验")
    args = ap.parse_args(argv)

    src = Path(args.src)
    if not src.exists():
        print(f"[错误] 文件不存在：{src}")
        return 1
    if src.suffix.lower() != ".docx":
        print(f"[错误] 仅支持 .docx：{src}")
        return 1

    try:
        dst, removed, verified, diff = strip_docx_images(
            src, args.out, verify=not args.no_verify
        )
    except Exception as exc:
        print(f"[错误] {exc}")
        return 1

    print(f"✅ 已生成无图版本：{dst}")
    print(f"   移除图片：{removed} 个")
    if not args.no_verify:
        if verified:
            print("   文字一致性校验：通过（与带图版全部文字一致）")
        else:
            print(f"   文字一致性校验：未通过 —— {diff}")
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
