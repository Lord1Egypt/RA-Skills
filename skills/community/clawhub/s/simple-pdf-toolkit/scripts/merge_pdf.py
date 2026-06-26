#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 合并工具
将多个 PDF 文件合并成一个
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


def merge_pdfs(input_files: list, output_file: str) -> dict:
    """
    合并多个 PDF 文件
    
    Args:
        input_files: 输入文件列表
        output_file: 输出文件路径
    
    Returns:
        结果字典
    """
    try:
        writer = PdfWriter()
        
        # 检查文件是否存在
        existing_files = []
        for file in input_files:
            if os.path.exists(file):
                existing_files.append(file)
            else:
                print(f"警告：文件不存在 - {file}", file=sys.stderr)
        
        if not existing_files:
            return {"error": "没有有效的输入文件"}
        
        # 合并 PDF
        for file in existing_files:
            reader = PdfReader(file)
            for page in reader.pages:
                writer.add_page(page)
        
        # 写入输出文件
        with open(output_file, "wb") as f:
            writer.write(f)
        
        return {
            "success": True,
            "message": f"成功合并 {len(existing_files)} 个文件",
            "output": output_file,
            "pages": len(writer.pages)
        }
        
    except Exception as e:
        return {"error": f"合并失败：{str(e)}"}


def main():
    # 简单的命令行参数解析
    args = sys.argv[1:]
    
    if len(args) < 2:
        print(json.dumps({
            "error": "用法：merge_pdf.py --output output.pdf file1.pdf [file2.pdf ...]",
            "example": "python merge_pdf.py --output merged.pdf file1.pdf file2.pdf file3.pdf"
        }, ensure_ascii=False))
        sys.exit(1)
    
    # 解析参数
    output_file = None
    input_files = []
    
    i = 0
    while i < len(args):
        if args[i] == "--output" and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        else:
            input_files.append(args[i])
            i += 1
    
    if not output_file:
        print(json.dumps({"error": "请指定输出文件：--output output.pdf"}))
        sys.exit(1)
    
    if not input_files:
        print(json.dumps({"error": "请指定至少一个输入文件"}))
        sys.exit(1)
    
    # 执行合并
    result = merge_pdfs(input_files, output_file)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
