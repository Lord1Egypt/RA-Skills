#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 旋转工具
旋转 PDF 页面角度
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


def rotate_pdf(input_file: str, output_file: str, angle: int = 90, pages: str = None) -> dict:
    """
    旋转 PDF 页面
    
    Args:
        input_file: 输入文件
        output_file: 输出文件
        angle: 旋转角度（90, 180, 270）
        pages: 页码范围（如"1-5"或"1,3,5"），None 表示全部
    
    Returns:
        结果字典
    """
    try:
        if not os.path.exists(input_file):
            return {"error": f"文件不存在：{input_file}"}
        
        reader = PdfReader(input_file)
        writer = PdfWriter()
        
        # 解析页码范围
        page_indices = None
        if pages:
            page_indices = []
            for part in pages.split(','):
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    page_indices.extend(range(start - 1, end))
                else:
                    page_indices.append(int(part) - 1)
        
        # 处理每一页
        for i, page in enumerate(reader.pages):
            if page_indices is None or i in page_indices:
                page.rotate(angle)
            writer.add_page(page)
        
        # 写入输出文件
        with open(output_file, "wb") as f:
            writer.write(f)
        
        return {
            "success": True,
            "message": f"成功旋转 {len(writer.pages)} 页",
            "output": output_file,
            "angle": angle
        }
        
    except Exception as e:
        return {"error": f"旋转失败：{str(e)}"}


def main():
    args = sys.argv[1:]
    
    if len(args) < 3:
        print(json.dumps({
            "error": "用法：rotate_pdf.py --input input.pdf --angle 90 --output output.pdf [--pages 1-5]",
            "example": "python rotate_pdf.py --input file.pdf --angle 90 --output rotated.pdf"
        }, ensure_ascii=False))
        sys.exit(1)
    
    # 解析参数
    input_file = None
    output_file = None
    angle = 90
    pages = None
    
    i = 0
    while i < len(args):
        if args[i] == "--input" and i + 1 < len(args):
            input_file = args[i + 1]
            i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        elif args[i] == "--angle" and i + 1 < len(args):
            angle = int(args[i + 1])
            i += 2
        elif args[i] == "--pages" and i + 1 < len(args):
            pages = args[i + 1]
            i += 2
        else:
            i += 1
    
    if not input_file or not output_file:
        print(json.dumps({"error": "请指定输入和输出文件"}))
        sys.exit(1)
    
    # 执行旋转
    result = rotate_pdf(input_file, output_file, angle, pages)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
