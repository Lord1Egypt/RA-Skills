#!/usr/bin/env python3
"""
将Markdown格式的质量计划文件转换为企业级排版的HTML文件。
读取HTML模板，注入内容和元数据，自动生成目录。
"""

import argparse
import json
import os
import re
import sys

try:
    import markdown
    from markdown.extensions.toc import TocExtension
except ImportError:
    print(json.dumps({"status": "error", "message": "缺少markdown库，请执行: pip install markdown>=3.4.0"}))
    sys.exit(1)


def read_file(path):
    """读取文件内容"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_metadata_from_md(md_content):
    """从Markdown内容中提取标题结构用于目录生成"""
    headings = []
    for line in md_content.split("\n"):
        match = re.match(r"^(#{1,3})\s+(.+)$", line.strip())
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            # 生成锚点ID（与markdown库的toc行为一致）
            anchor = re.sub(r"[^\w\u4e00-\u9fff\-]", "", text.lower().replace(" ", "-"))
            headings.append({"level": level, "text": text, "id": anchor})
    return headings


def generate_toc_html(headings):
    """根据标题结构生成目录HTML"""
    if not headings:
        return ""

    toc_lines = ['<nav class="toc" id="toc">', "<h2>目 录</h2>", '<ul class="toc-list">']

    for h in headings:
        indent = "  " * (h["level"] - 1)
        toc_lines.append(
            f'{indent}<li class="toc-level-{h["level"]}"><a href="#{h["id"]}">{h["text"]}</a></li>'
        )

    toc_lines.append("</ul>")
    toc_lines.append("</nav>")
    return "\n".join(toc_lines)


def convert_md_to_html(md_content):
    """将Markdown内容转换为HTML片段"""
    extensions = [
        TocExtension(permalink=False, slugify=slugify_cn),
        "tables",
        "fenced_code",
    ]
    html_body = markdown.markdown(md_content, extensions=extensions)
    return html_body


def slugify_cn(value, separator="-"):
    """支持中文的slugify"""
    import unicodedata

    value = unicodedata.normalize("NFKC", value)
    value = re.sub(r"[^\w\u4e00-\u9fff\s-]", "", value).strip().lower()
    return re.sub(r"[\s]+", separator, value)


def build_final_html(template_content, body_html, toc_html, metadata):
    """将模板、内容和元数据组合为最终HTML"""
    # 替换元数据占位符
    result = template_content
    for key, value in metadata.items():
        result = result.replace("{{" + key + "}}", str(value))

    # 注入目录
    result = result.replace("{{toc}}", toc_html)

    # 注入正文内容
    result = result.replace("{{content}}", body_html)

    return result


def main():
    parser = argparse.ArgumentParser(description="将Markdown质量计划转换为企业级HTML")
    parser.add_argument("--input", required=True, help="输入的Markdown文件路径")
    parser.add_argument("--output", required=True, help="输出的HTML文件路径")
    parser.add_argument("--title", default="产品质量计划", help="文档标题")
    parser.add_argument("--product-name", default="", help="产品名称")
    parser.add_argument("--doc-number", default="", help="文档编号")
    parser.add_argument("--version", default="A0", help="版本号")
    parser.add_argument("--company", default="", help="公司名称")
    parser.add_argument("--date", default="", help="编制日期")
    args = parser.parse_args()

    # 验证输入文件
    if not os.path.exists(args.input):
        print(json.dumps({"status": "error", "message": f"输入文件不存在: {args.input}"}))
        sys.exit(1)

    # 确定模板路径（相对于脚本所在目录的上级assets/）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    template_path = os.path.join(skill_dir, "assets", "html-template.html")

    if not os.path.exists(template_path):
        print(json.dumps({"status": "error", "message": f"HTML模板文件不存在: {template_path}"}))
        sys.exit(1)

    # 读取输入文件
    md_content = read_file(args.input)

    # 读取模板
    template_content = read_file(template_path)

    # 构建元数据
    metadata = {
        "title": args.title,
        "product_name": args.product_name,
        "doc_number": args.doc_number,
        "version": args.version,
        "company": args.company,
        "date": args.date,
    }

    # 提取标题结构并生成目录
    headings = extract_metadata_from_md(md_content)
    toc_html = generate_toc_html(headings)

    # 转换Markdown为HTML
    body_html = convert_md_to_html(md_content)

    # 组合最终HTML
    final_html = build_final_html(template_content, body_html, toc_html, metadata)

    # 写入输出文件
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(final_html)

    result = {
        "status": "success",
        "html_path": os.path.abspath(args.output),
        "md_path": os.path.abspath(args.input),
        "headings_count": len(headings),
        "metadata": metadata,
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
