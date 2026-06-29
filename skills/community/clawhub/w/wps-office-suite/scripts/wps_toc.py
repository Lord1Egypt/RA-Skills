"""
WPS Office 全家桶 - 目录生成（TOC）
自动生成 Word 文档目录，支持 WPS 和 Pure Python 双路径
"""
import sys
import json
import re
from pathlib import Path

from wps_common import get_wps, release_wps, get_engine, safe_path


def extract_headings(filepath: str) -> list:
    """
    从 Word 文档中提取标题列表
    返回: [{"level": 1, "text": "标题", "page": 1}, ...]
    """
    engine = get_engine()

    if engine in ("WPS", "MSOFFICE"):
        return _extract_headings_com(filepath)
    else:
        return _extract_headings_pure(filepath)


def _extract_headings_com(filepath: str) -> list:
    """WPS/MS Office COM 方式"""
    try:
        wps = get_wps()
        doc = wps.Documents.Open(filepath)
        headings = []

        for para in doc.Paragraphs:
            style = para.Range.Style.NameLocal
            text = para.Range.Text.strip()

            if not text:
                continue

            # 匹配 "标题 1" / "Heading 1" 等样式名
            match = re.search(r"标题\s*(\d+)|Heading\s*(\d+)", style)
            if match:
                level = int(match.group(1) or match.group(2))
                headings.append({
                    "level": level,
                    "text": text,
                    "page": 1  # WPS 无法直接获取页码，需计算
                })

        doc.Close()
        release_wps()
        return headings
    except Exception as e:
        release_wps()
        raise


def _extract_headings_pure(filepath: str) -> list:
    """Pure Python 方式（python-docx）"""
    try:
        from docx import Document

        doc = Document(filepath)
        headings = []

        for para in doc.paragraphs:
            if para.style.name.startswith("Heading"):
                match = re.search(r"(\d+)", para.style.name)
                if match:
                    level = int(match.group(1))
                    text = para.text.strip()
                    if text:
                        headings.append({
                            "level": level,
                            "text": text,
                            "page": 1  # Python-docx 不支持页码
                        })

        return headings
    except Exception as e:
        raise


def generate_toc(filepath: str, output_path: str = None, engine: str = None) -> dict:
    """
    生成目录文件

    目录结构：
    - <1个字符的缩进> 标题 1：级别1 目录项
    - <缩进>    标题 2-1：级别2 目录项（左侧缩进 1 字符）
    - <缩进>      标题 3-1：级别3 目录项（左侧缩进 2 字符）
    """
    try:
        filepath = safe_path(filepath)
        if not filepath.exists():
            return {"success": False, "error": f"文件不存在: {filepath}"}

        eng = engine or get_engine()
        headings = extract_headings(filepath.__str__())

        if not headings:
            return {"success": True, "headings": [], "note": "文档中无标题"}

        # 生成 TOC 文件内容
        output_p = Path(output_path) if output_path else filepath.parent / f"{filepath.stem}_toc.txt"

        lines = []
        lines.append("=" * 50)
        lines.append("文档目录")
        lines.append("=" * 50)
        lines.append("")

        for h in headings:
            level = h["level"]
            text = h["text"]

            # 缩进：第 1 级不缩进，每多一级缩进 2 个空格
            indent = "  " * (level - 1)

            # 页码：暂不显示（后续可扩展）
            lines.append(f"{indent}{text}")

        lines.append("")
        lines.append("=" * 50)
        lines.append("生成时间：" + __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%S"))
        lines.append("生成工具：WPS Office 全家桶")
        lines.append("=" * 50)

        toc_text = "\n".join(lines)

        # 写入文件
        output_p.write_text(toc_text, encoding="utf-8")

        return {
            "success": True,
            "path": str(output_p),
            "headings": headings,
            "heading_count": len(headings),
            "engine": eng,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def insert_toc_to_doc(filepath: str, engine: str = None) -> dict:
    """
    在 Word 文档中插入目录域（仅 WPS 模式）
    插入位置：文档开头（第一个段落之前）
    """
    try:
        filepath = safe_path(filepath)
        eng = engine or get_engine()

        if eng not in ("WPS", "MSOFFICE"):
            return {
                "success": False,
                "error": "纯 Python 模式不支持目录域插入，请使用 `generate-toc` 生成外部目录文件",
                "hint": "或者安装 WPS Office 后重试",
            }

        wps = get_wps()
        doc = wps.Documents.Open(filepath.__str__())

        # 提取标题
        headings = extract_headings(filepath.__str__())
        if not headings:
            doc.Close()
            release_wps()
            return {"success": True, "note": "无标题"}

        # 在文档开头插入目录域
        # WPS 目录域代码：TOC \o "1-3" \h \z \u
        # \o "1-3" : 包含 1-3 级标题
        # \h      : 插入超链接
        # \z      : 隐藏制表位
        # \u      : 使用段落 outline level

        first_para = doc.Paragraphs(1)
        first_para.Range.InsertBefore("目录\n")
        first_para.Range.InsertAfter("\n")

        # 插入域代码（WPS 的 Field 接口）
        # 注意：域的插入需要使用特定的方法
        # 这里使用 Range.InsertParagraphAfter + 手动构建域

        # 构建 TOC 域代码
        toc_code = 'TOC \\o "1-3" \\h \\z \\u'

        # 插入段落并设置域代码
        range_for_field = doc.Paragraphs(1).Range
        range_for_field.Collapse(0)  # 折叠到开头
        doc.Fields.Add(range_for_field, None, toc_code)

        doc.Save()
        doc.Close()
        release_wps()

        return {
            "success": True,
            "inserted": True,
            "heading_count": len(headings),
            "engine": eng,
            "note": "目录已插入到文档开头，更新目录请右键域代码选择更新域",
        }
    except Exception as e:
        release_wps()
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="目录生成")
    sub = parser.add_subparsers(dest="command", required=True)

    p_extract = sub.add_parser("extract")
    p_extract.add_argument("--file", required=True)

    p_generate = sub.add_parser("generate")
    p_generate.add_argument("--file", required=True)
    p_generate.add_argument("--output", default="")

    p_insert = sub.add_parser("insert")
    p_insert.add_argument("--file", required=True)

    args = parser.parse_args()

    if args.command == "extract":
        result = extract_headings(args.file)
        print(json.dumps({"ok": True, "headings": result}, ensure_ascii=False, default=str))
    elif args.command == "generate":
        result = generate_toc(args.file, args.output)
        print(json.dumps(result, ensure_ascii=False, default=str))
    elif args.command == "insert":
        result = insert_toc_to_doc(args.file)
        print(json.dumps(result, ensure_ascii=False, default=str))
    else:
        print(json.dumps({"ok": False, "error": "未知命令"}))
