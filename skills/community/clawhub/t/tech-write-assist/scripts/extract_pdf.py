#!/usr/bin/env python3
"""
PDF 内容提取脚本
从技术报告 PDF 中提取文本、表格和图片，输出结构化 JSON。

用法:
    python extract_pdf.py <pdf_path> [output_dir]

输出:
    <output_dir>/extracted_content.json  - 结构化内容
    <output_dir>/figures/                - 提取的图片
"""

import json
import os
import re
import sys


def check_dependencies():
    """检查并报告缺失的依赖"""
    missing = []
    try:
        import pdfplumber  # noqa: F401
    except ImportError:
        missing.append("pdfplumber")
    try:
        import fitz  # noqa: F401
    except ImportError:
        missing.append("PyMuPDF")
    if missing:
        print(f"ERROR: Missing dependencies: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        sys.exit(1)


def extract_text_and_tables(pdf_path):
    """用 pdfplumber 提取文本和表格"""
    import pdfplumber

    pages_data = []
    all_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            pages_data.append({
                "page": page_num + 1,
                "text": text
            })

            page_tables = page.extract_tables()
            if page_tables:
                for t_idx, table in enumerate(page_tables):
                    if table and len(table) > 1:
                        # 清理表格数据
                        cleaned = []
                        for row in table:
                            cleaned.append([
                                (cell or "").strip() for cell in row
                            ])
                        all_tables.append({
                            "page": page_num + 1,
                            "table_index": t_idx,
                            "data": cleaned
                        })

    full_text = "\n".join(p["text"] for p in pages_data)
    return full_text, pages_data, all_tables


def extract_images(pdf_path, output_dir):
    """用 PyMuPDF 提取嵌入图片"""
    import fitz

    figures_dir = os.path.join(output_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)

    images = []
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images()

        for img_idx, img in enumerate(image_list):
            xref = img[0]
            try:
                pix = fitz.Pixmap(doc, xref)

                # 跳过太小的图片（可能是图标或装饰）
                if pix.width < 100 or pix.height < 100:
                    if pix.n >= 5:  # CMYK
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    continue

                # 转换 CMYK 到 RGB
                if pix.n >= 5:
                    pix = fitz.Pixmap(fitz.csRGB, pix)

                img_filename = f"fig_p{page_num + 1}_{img_idx}.png"
                img_path = os.path.join(figures_dir, img_filename)
                pix.save(img_path)

                images.append({
                    "page": page_num + 1,
                    "index": img_idx,
                    "width": pix.width,
                    "height": pix.height,
                    "path": img_path,
                    "filename": img_filename
                })
            except Exception as e:
                print(f"Warning: Failed to extract image on page {page_num + 1}: {e}")

    doc.close()
    return images


def extract_metadata(full_text, page_count):
    """从文本中提取元数据（标题、作者等）"""
    metadata = {
        "title": "",
        "authors": [],
        "date": "",
        "page_count": page_count
    }

    lines = full_text.strip().split("\n")
    non_empty = [l.strip() for l in lines if l.strip()]

    # 标题通常是前几行中最长的非空行（排除作者/机构行）
    if non_empty:
        # 取前10行中较长的行作为标题候选
        candidates = non_empty[:10]
        title_candidates = [
            l for l in candidates
            if len(l) > 10 and not re.match(r'^(abstract|introduction|\d)', l.lower())
        ]
        if title_candidates:
            metadata["title"] = title_candidates[0]

    # 尝试提取 Abstract 后面的作者行
    for i, line in enumerate(non_empty[:20]):
        # 常见的作者行模式：多个名字用逗号分隔
        if re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+.*,.*[A-Z][a-z]+ [A-Z][a-z]+', line):
            authors = [a.strip() for a in re.split(r'[,;]', line) if a.strip()]
            # 过滤掉太长的（可能不是人名）
            authors = [a for a in authors if len(a) < 50]
            if authors:
                metadata["authors"] = authors[:10]
                break

    return metadata


def extract_abstract(full_text):
    """提取摘要"""
    # 尝试匹配 Abstract 段落
    patterns = [
        r'(?i)abstract\s*\n(.*?)(?=\n\s*(?:1[\.\s]|introduction|keywords|i\.\s))',
        r'(?i)abstract[:\s]+(.*?)(?=\n\s*(?:1[\.\s]|introduction|keywords))',
        r'(?i)摘\s*要[:\s]*(.*?)(?=\n\s*(?:关键词|1[\.\s]|引言))',
    ]

    for pattern in patterns:
        match = re.search(pattern, full_text, re.DOTALL)
        if match:
            abstract = match.group(1).strip()
            # 清理多余空白
            abstract = re.sub(r'\s+', ' ', abstract)
            if len(abstract) > 50:
                return abstract

    # fallback: 取前 500 字符
    return full_text[:500].strip()


def parse_sections(full_text):
    """解析章节结构"""
    sections = []

    # 匹配常见的论文章节标题格式
    # 格式1: "1. Introduction" 或 "1 Introduction"
    # 格式2: "I. Introduction"
    # 格式3: "## Introduction" (Markdown)
    section_pattern = re.compile(
        r'\n\s*(?:'
        r'(\d+\.?\s+[A-Z][A-Za-z\s]+)'  # "1. Introduction"
        r'|([IVX]+\.?\s+[A-Z][A-Za-z\s]+)'  # "I. Introduction"
        r'|(#{1,3}\s+.+)'  # "## Section"
        r'|(第[一二三四五六七八九十]+[章节部分]\s*.+)'  # 中文章节
        r')\s*\n'
    )

    matches = list(section_pattern.finditer(full_text))

    for i, match in enumerate(matches):
        title = (match.group(1) or match.group(2) or
                 match.group(3) or match.group(4) or "").strip()
        title = re.sub(r'^#+\s*', '', title)  # 去掉 Markdown #

        # 提取章节内容（到下一个章节标题之前）
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        content = full_text[start:end].strip()

        # 判断层级
        level = 1
        if match.group(1):
            # "1.1" 格式为 level 2
            if re.match(r'\d+\.\d+', title):
                level = 2
        elif match.group(3):
            level = title.count('#') if '#' in match.group(3) else 1

        sections.append({
            "title": title,
            "level": level,
            "content": content[:2000]  # 限制每节最多 2000 字符
        })

    # 如果没有检测到章节，将全文作为一个章节
    if not sections:
        sections.append({
            "title": "Full Text",
            "level": 1,
            "content": full_text[:5000]
        })

    return sections


def extract_key_metrics(full_text, tables):
    """提取关键性能指标和 benchmark 数据"""
    metrics = {
        "benchmarks": [],
        "comparisons": [],
        "key_numbers": []
    }

    # 提取包含百分比或数字比较的句子
    number_pattern = re.compile(
        r'[^.]*(?:'
        r'\d+\.?\d*\s*%'       # 百分比
        r'|\d+\.?\d*x\s'       # 倍数 (e.g., "3.5x faster")
        r'|(?:accuracy|precision|recall|f1|bleu|rouge|sota|state-of-the-art)'
        r'|(?:outperform|surpass|exceed|improve|achieve)'
        r'|(?:提升|超过|达到|领先|优于)'
        r')[^.]*\.'
    , re.IGNORECASE)

    matches = number_pattern.findall(full_text)
    for m in matches[:20]:  # 最多取 20 条
        cleaned = m.strip()
        if len(cleaned) > 20:  # 过滤太短的匹配
            metrics["key_numbers"].append(cleaned)

    # 将表格数据也纳入
    for table in tables:
        if table["data"] and len(table["data"]) >= 2:
            header = table["data"][0]
            # 检测是否为 benchmark 表格
            benchmark_keywords = [
                'accuracy', 'acc', 'f1', 'bleu', 'rouge', 'score',
                'precision', 'recall', 'loss', 'perplexity', 'ppl',
                'latency', 'throughput', 'speed', 'params',
                '准确率', '精度', '召回率', '得分'
            ]
            is_benchmark = any(
                any(kw in str(cell).lower() for kw in benchmark_keywords)
                for cell in header
            )
            if is_benchmark:
                metrics["benchmarks"].append({
                    "page": table["page"],
                    "header": header,
                    "rows": table["data"][1:6]  # 最多取 5 行数据
                })

    return metrics


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf.py <pdf_path> [output_dir]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./output/extracted"

    if not os.path.exists(pdf_path):
        print(f"ERROR: PDF file not found: {pdf_path}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    print(f"Extracting content from: {pdf_path}")
    print(f"Output directory: {output_dir}")

    # 1. 提取文本和表格
    print("[1/4] Extracting text and tables...")
    full_text, pages_data, tables = extract_text_and_tables(pdf_path)
    page_count = len(pages_data)
    print(f"  - {page_count} pages, {len(tables)} tables found")

    # 2. 提取图片
    print("[2/4] Extracting images...")
    images = extract_images(pdf_path, output_dir)
    print(f"  - {len(images)} images extracted")

    # 3. 解析结构
    print("[3/4] Parsing document structure...")
    metadata = extract_metadata(full_text, page_count)
    abstract = extract_abstract(full_text)
    sections = parse_sections(full_text)
    key_metrics = extract_key_metrics(full_text, tables)
    print(f"  - Title: {metadata['title'][:60]}...")
    print(f"  - {len(sections)} sections detected")
    print(f"  - {len(key_metrics['key_numbers'])} key metrics found")

    # 4. 组装输出
    print("[4/4] Building output JSON...")
    result = {
        "metadata": metadata,
        "abstract": abstract,
        "sections": sections,
        "tables": tables,
        "images": [
            {
                "page": img["page"],
                "filename": img["filename"],
                "width": img["width"],
                "height": img["height"],
                "path": img["path"]
            }
            for img in images
        ],
        "key_metrics": key_metrics,
        "full_text_preview": full_text[:3000]
    }

    output_path = os.path.join(output_dir, "extracted_content.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\nExtraction complete!")
    print(f"Output: {output_path}")
    print(f"Summary: {page_count} pages, {len(sections)} sections, "
          f"{len(tables)} tables, {len(images)} images")

    return output_path


if __name__ == "__main__":
    check_dependencies()
    main()
