#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 拆分工具
按页码拆分 PDF 文件
"""

import sys
import os
import json

try:
    from pypdf import PdfWriter, PdfReader
except ImportError:
    print(json.dumps({
        "error": "缺少依赖：pypdf",
        "install": "pip install pypdf"
    }, ensure_ascii=False))
    sys.exit(1)


def split_pdf(input_file: str, output_pattern: str, pages: str = None) -> dict:
    """
    拆分 PDF 文件
    
    Args:
        input_file: 输入文件
        output_pattern: 输出文件模式（如 output_{}.pdf，{}会被页码替换）
        pages: 页码范围（如"1-5"提取指定页，"all"每页一个文件）
    
    Returns:
        结果字典
    """
    try:
        if not os.path.exists(input_file):
            return {"error": f"文件不存在：{input_file}"}
        
        reader = PdfReader(input_file)
        total_pages = len(reader.pages)
        
        output_files = []
        
        if pages == "all" or pages is None:
            # 每页一个文件
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                
                output_file = output_pattern.format(i + 1)
                with open(output_file, "wb") as f:
                    writer.write(f)
                output_files.append(output_file)
            
            return {
                "success": True,
                "message": f"成功拆分为 {len(output_files)} 个文件",
                "output_files": output_files
            }
        
        elif '-' in pages or ',' in pages:
            # 提取指定页码
            writer = PdfWriter()
            page_indices = []
            
            for part in pages.split(','):
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    page_indices.extend(range(start - 1, min(end, total_pages)))
                else:
                    page_num = int(part)
                    if page_num <= total_pages:
                        page_indices.append(page_num - 1)
            
            for i in page_indices:
                writer.add_page(reader.pages[i])
            
            output_file = output_pattern.format("extracted")
            with open(output_file, "wb") as f:
                writer.write(f)
            output_files.append(output_file)
            
            return {
                "success": True,
                "message": f"成功提取 {len(page_indices)} 页",
                "output_files": output_files
            }
        
        else:
            return {"error": "页码格式错误，使用'1-5'或'1,3,5'或'all'"}
        
    except Exception as e:
        return {"error": f"拆分失败：{str(e)}"}


def main():
    args = sys.argv[1:]
    
    if len(args) < 2:
        print(json.dumps({
            "error": "用法：split_pdf.py --input input.pdf --output output_{}.pdf [--pages 1-5|all]",
            "example": "python split_pdf.py --input file.pdf --output page_{}.pdf --pages 1-5"
        }, ensure_ascii=False))
        sys.exit(1)
    
    # 解析参数
    input_file = None
    output_pattern = None
    pages = None
    
    i = 0
    while i < len(args):
        if args[i] == "--input" and i + 1 < len(args):
            input_file = args[i + 1]
            i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            output_pattern = args[i + 1]
            i += 2
        elif args[i] == "--pages" and i + 1 < len(args):
            pages = args[i + 1]
            i += 2
        else:
            i += 1
    
    if not input_file or not output_pattern:
        print(json.dumps({"error": "请指定输入和输出文件"}))
        sys.exit(1)
    
    # 确保输出模式包含{}
    if '{}' not in output_pattern:
        output_pattern = output_pattern.replace('.pdf', '_{}.pdf')
    
    # 执行拆分
    result = split_pdf(input_file, output_pattern, pages)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
