#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成不带图的 docx 版本。

用途：每次交付带图解析稿时，同步产出一份内容完全一致、只是移除了图片的版本。
保留：全部文字、分页标题、图片标记（如 /[pic 01：简述]/、/[pic NN]*** ... ***/）
      以及图片内容解析说明。
移除：所有 story part 中的内嵌图片（DrawingML / VML），并清理图片类
      word/media 文件、docProps/thumbnail 等图片二进制及其关系。
      不删除 OLE、音频、视频或其他非图片嵌入对象；这些内容及其关系保留。

与旧版的关键区别：
- 旧版只遍历 document.body，页眉/页脚/脚注/尾注/批注中的图片会残留；
- 旧版只删 XML 引用，不删 word/media，所以文件体积几乎不变；
- 旧版只校验正文文字，图片还在也能打印“校验通过”。
本版按 OPC 包级处理，并在校验阶段强制检查“图片二进制与图片引用均为零”。

用法：
    python strip_images.py <带图解析稿.docx>
    python strip_images.py <带图解析稿.docx> -o <无图解析稿.docx>

默认输出文件名：<原名>_无图.docx（若原名已以 _无图 结尾则拒绝重复处理）。
"""
import argparse
import os
import re
import sys
import tempfile
import zipfile
from pathlib import Path

try:
    from lxml import etree
except Exception as exc:  # pragma: no cover
    raise SystemExit("缺少 lxml（python-docx 的依赖）：" + str(exc)) from exc


STORY_RE = re.compile(
    r"^word/(document\.xml|header\d*\.xml|footer\d*\.xml|"
    r"footnotes\.xml|endnotes\.xml|comments\.xml|glossary/document\.xml)$"
)
IMAGE_MEDIA_DIR = "word/media/"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff",
                    ".emf", ".wmf", ".svg", ".webp", ".ico"}
THUMBNAIL_RE = re.compile(r"^docProps/thumbnail\.(jpeg|jpg|png|gif|bmp|tif|tiff)$", re.I)
# 只删除图片关系；OLE/package/audio/video 关系保留。
IMAGE_REL_TYPES = ("/image", "/thumbnail")
IMAGE_ELEMENT_NAMES = {"blip", "imagedata", "pic"}


def text_version_path(src):
    """按约定推导无图版本路径：<stem>_无图<suffix>。"""
    src = Path(src)
    if src.stem.endswith("_无图"):
        return src
    return src.with_name(f"{src.stem}_无图{src.suffix}")


def _is_image_part(name):
    """只把 word/media 下扩展名属于图片的文件视为图片；音频/视频保留。"""
    return name.startswith(IMAGE_MEDIA_DIR) and Path(name).suffix.lower() in IMAGE_EXTENSIONS


def _local_name(el):
    try:
        return etree.QName(el).localname
    except Exception:
        return ""


def _contains_image(el):
    """判断元素子树里是否含图片引用（DrawingML/VML/OLE 预览）。"""
    for node in el.iter():
        if _local_name(node) in IMAGE_ELEMENT_NAMES:
            return True
    return False


def _strip_story_xml(data, part_name):
    """删除 story part 中的图片元素；返回 (新 XML bytes, 删除元素数)。"""
    parser = etree.XMLParser(resolve_entities=False, recover=False)
    root = etree.fromstring(data, parser)
    removed = 0

    # 1) 图片 / 背景图：只在含图片引用时删除，保留图表、SmartArt、文本框。
    #    OLE 对象（w:object）不整体删除；其内部图片预览若为 w:pict 会被单独移除，
    #    但对象本身和 word/embeddings 保留。
    for tag in ("drawing", "pict", "background"):
        for el in list(root.iter()):
            if _local_name(el) != tag:
                continue
            if _contains_image(el):
                parent = el.getparent()
                if parent is not None:
                    parent.remove(el)
                    removed += 1

    # 2) 编号图片项目符号：删除定义，并清理对应的 lvlPicBulletId 引用。
    if part_name == "word/numbering.xml":
        for el in list(root.iter()):
            if _local_name(el) == "numPicBullet" and _contains_image(el):
                parent = el.getparent()
                if parent is not None:
                    parent.remove(el)
                    removed += 1
        for el in list(root.iter()):
            if _local_name(el) == "lvlPicBulletId":
                parent = el.getparent()
                if parent is not None:
                    parent.remove(el)

    return etree.tostring(
        root, xml_declaration=True, encoding="UTF-8", standalone=True
    ), removed


def _strip_rels_xml(data):
    """删除指向图片/缩略图的关系；OLE/音频/视频关系保留。返回 (新 XML bytes, 删除关系数)。"""
    parser = etree.XMLParser(resolve_entities=False, recover=False)
    root = etree.fromstring(data, parser)
    removed = 0
    for rel in list(root):
        if _local_name(rel) != "Relationship":
            continue
        typ = rel.get("Type", "")
        if any(typ.endswith(suffix) for suffix in IMAGE_REL_TYPES):
            root.remove(rel)
            removed += 1
    return etree.tostring(
        root, xml_declaration=True, encoding="UTF-8", standalone=True
    ), removed


def _strip_content_types(data):
    """删除已移除部件的 Override 声明；保留 png/jpeg 等 Default。"""
    parser = etree.XMLParser(resolve_entities=False, recover=False)
    root = etree.fromstring(data, parser)
    removed = 0
    for ov in list(root):
        if _local_name(ov) != "Override":
            continue
        part_name = ov.get("PartName", "")
        if (
            part_name.startswith("/docProps/thumbnail.")
            or _is_image_part(part_name.lstrip("/"))
        ):
            root.remove(ov)
            removed += 1
    return etree.tostring(
        root, xml_declaration=True, encoding="UTF-8", standalone=True
    ), removed


def _collect_story_texts(zf):
    """收集所有 story part 的文字节点（正文、页眉、页脚、脚注、尾注、批注、词汇表）。"""
    texts = []
    for name in zf.namelist():
        if not STORY_RE.match(name):
            continue
        try:
            root = etree.fromstring(
                zf.read(name), etree.XMLParser(resolve_entities=False, recover=False)
            )
        except Exception:
            continue
        for el in root.iter():
            if _local_name(el) in ("t", "instrText"):
                texts.append(el.text or "")
    return texts


def _has_any_image_reference(zf):
    """检查包内是否还有图片二进制、图片关系或图片 XML 元素。"""
    names = zf.namelist()
    if any(_is_image_part(name) for name in names):
        return True, "仍存在 word/media 图片二进制"
    if any(THUMBNAIL_RE.match(name) for name in names):
        return True, "仍存在 docProps/thumbnail 缩略图"

    for name in names:
        if not (STORY_RE.match(name) or name == "word/numbering.xml"):
            continue
        try:
            root = etree.fromstring(
                zf.read(name), etree.XMLParser(resolve_entities=False, recover=False)
            )
        except Exception:
            continue
        for el in root.iter():
            if _local_name(el) in IMAGE_ELEMENT_NAMES:
                return True, f"{name} 中仍存在图片元素 <{_local_name(el)}>"
    return False, ""


def _text_diff(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return f"第 {i + 1} 个文字节点不一致：{x!r} != {y!r}"
    if len(a) != len(b):
        return f"文字节点数量不一致：{len(a)} != {len(b)}"
    return ""


def strip_docx_images(src, dst=None, verify=True):
    """复制 src 为 dst，并移除所有 story part 中的图片与图片二进制。

    返回 (dst_path, removed_count, verified, diff_detail)。
    verified 只有在文字完全一致且图片二进制/引用均为零时才为 True。
    """
    src = Path(src)
    dst = Path(dst) if dst else text_version_path(src)
    if src.resolve() == dst.resolve():
        raise ValueError("输入与输出不能是同一个文件；请指定其它输出路径。")

    dst.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(src, "r") as zf:
        infos = zf.infolist()
        original = {info.filename: zf.read(info.filename) for info in infos}

    modified = {}
    removed = 0
    rels_removed = 0
    ct_removed = 0

    for name, data in original.items():
        if STORY_RE.match(name) or name == "word/numbering.xml":
            try:
                new_data, n = _strip_story_xml(data, name)
                modified[name] = new_data
                removed += n
            except Exception as exc:
                raise RuntimeError(f"处理 {name} 失败：{exc}") from exc
        elif name.endswith(".rels"):
            try:
                new_data, n = _strip_rels_xml(data)
                modified[name] = new_data
                rels_removed += n
            except Exception as exc:
                raise RuntimeError(f"处理 {name} 失败：{exc}") from exc
        elif name == "[Content_Types].xml":
            try:
                new_data, n = _strip_content_types(data)
                modified[name] = new_data
                ct_removed += n
            except Exception as exc:
                raise RuntimeError(f"处理 {name} 失败：{exc}") from exc

    # 原子写入：先写同目录临时文件，再替换，避免半成品被读取。
    tmp_fd, tmp_name = tempfile.mkstemp(
        prefix=dst.name + ".", suffix=".tmp", dir=str(dst.parent)
    )
    os.close(tmp_fd)
    tmp_path = Path(tmp_name)
    try:
        with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as out:
            for info in infos:
                name = info.filename
                if _is_image_part(name) or THUMBNAIL_RE.match(name):
                    continue
                data = modified.get(name, original[name])
                # 保留原条目的压缩方式/时间戳，避免无意义 diff。
                out.writestr(info, data)
        os.replace(tmp_path, dst)
    finally:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)

    verified = False
    diff_detail = ""
    if verify:
        try:
            with zipfile.ZipFile(src, "r") as zf:
                a = _collect_story_texts(zf)
            with zipfile.ZipFile(dst, "r") as zf:
                b = _collect_story_texts(zf)
                has_image, why = _has_any_image_reference(zf)
            if a != b:
                diff_detail = _text_diff(a, b)
            elif has_image:
                diff_detail = why
            else:
                verified = True
        except Exception as exc:
            diff_detail = f"校验失败：{exc}"

    return dst, removed, verified, diff_detail


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="生成不带图的 docx 版本（文字与图片解析说明保持不变，图片二进制清零）"
    )
    ap.add_argument("src", help="带图解析稿 .docx")
    ap.add_argument("-o", "--out", default=None, help="输出路径（默认 <原名>_无图.docx）")
    ap.add_argument("--no-verify", action="store_true", help="跳过文字/图片残留校验")
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
    print(f"   移除图片元素：{removed} 个")
    if not args.no_verify:
        if verified:
            print("   文字一致性校验：通过（与带图版全部文字一致）")
            print("   图片残留校验：通过（图片类 word/media、thumbnail 均为 0；OLE/音频/视频保留）")
        else:
            print(f"   无图校验：未通过 —— {diff}")
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
