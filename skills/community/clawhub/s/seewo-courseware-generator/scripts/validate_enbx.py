#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_enbx.py - 校验 .enbx 文件结构合法性
检查项：
  1. ZIP 完整性 & 必要文件存在
  2. 每个 XML 文件良构（可被 XML 解析器读取）
  3. Reference.xml 中每个关系 Id 在 Resources/ 下都有实体文件
  4. 每个 Slide 的 <Id> 都出现在 Board.xml 的 <Item> 列表中（且数量一致）
  5. 每个元素引用的 id:// 资源都能在 Reference 中找到
"""
import sys
import zipfile
import xml.etree.ElementTree as ET
import os


REQUIRED_FILES = [
    "[Content_Types].xml",
    "Document.xml",
    "Reference.xml",
    "Board.xml",
    "SaveInfoMetadataFile.xml",
    "thumbnail.png",
]


def strip_bom(data):
    if data[:3] == b"\xef\xbb\xbf":
        return data[3:]
    return data


def parse_xml(z, name):
    data = z.read(name)
    data = strip_bom(data)
    return ET.fromstring(data), data.decode("utf-8", "replace")


def validate(path):
    errors = []
    warnings = []
    if not os.path.exists(path):
        return False, ["文件不存在: " + path], []

    try:
        z = zipfile.ZipFile(path, "r")
    except Exception as e:
        return False, ["ZIP 打开失败: " + str(e)], []

    bad = z.testzip()
    if bad:
        errors.append("ZIP 损坏，首个错误文件: " + bad)

    names = set(z.namelist())
    for rf in REQUIRED_FILES:
        if rf not in names:
            errors.append("缺少必要文件: " + rf)

    # 解析各 XML
    parsed = {}
    for xf in ["[Content_Types].xml", "Document.xml", "Reference.xml",
               "Board.xml", "SaveInfoMetadataFile.xml"]:
        if xf in names:
            try:
                parsed[xf] = parse_xml(z, xf)[0]
            except Exception as e:
                errors.append("XML 解析失败 {0}: {1}".format(xf, e))

    # Slide 文件
    slide_names = sorted([n for n in names if n.startswith("Slides/Slide_") and n.endswith(".xml")])
    if not slide_names:
        errors.append("没有 Slides/Slide_*.xml")
    slide_ids = []
    for sn in slide_names:
        try:
            root = parse_xml(z, sn)[0]
            sid = root.findtext("Id")
            if sid:
                slide_ids.append(sid)
        except Exception as e:
            errors.append("XML 解析失败 {0}: {1}".format(sn, e))

    # Board Items
    if "Board.xml" in parsed:
        items = [it.text for it in parsed["Board.xml"].iter("Item") if it.text]
        if len(items) != len(slide_ids):
            errors.append("Board 幻灯片数({0}) 与 Slide 文件数({1}) 不一致".format(len(items), len(slide_ids)))
        for sid in slide_ids:
            if sid not in items:
                errors.append("Slide Id 未出现在 Board 中: " + sid)

    # Reference 关系 -> Resources 实体
    ref_ids = {}
    if "Reference.xml" in parsed:
        for rel in parsed["Reference.xml"].iter("Relationship"):
            rid = rel.findtext("Id")
            tgt = rel.findtext("Target")
            if rid:
                ref_ids[rid] = tgt
            if tgt:
                tgt_norm = tgt.replace("\\", "/")
                if tgt_norm not in names:
                    errors.append("关系目标文件不存在: " + tgt_norm)

    # 元素里的 id:// 引用是否在 Reference 中
    id_prefix = "id://"
    for sn in slide_names:
        try:
            root = parse_xml(z, sn)[0]
        except Exception:
            continue
        for src in root.iter("Source"):
            v = src.text or ""
            if v.startswith(id_prefix):
                hid = v[len(id_prefix):]
                if hid not in ref_ids:
                    errors.append("{0}: 引用资源未在 Reference 注册: {1}".format(sn, hid))

    z.close()
    ok = len(errors) == 0
    return ok, errors, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_enbx.py <file.enbx>")
        sys.exit(1)
    ok, errors, warnings = validate(sys.argv[1])
    if ok:
        print("✅ 校验通过: " + sys.argv[1])
    else:
        print("❌ 校验失败: " + sys.argv[1])
        for e in errors:
            print("  - " + e)
    for w in warnings:
        print("  ! " + w)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
