#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 文本提取工具
从 PDF 中提取文字内容
"""

import sys
import os
import json

try:
    from pypdf import PdfReader
except ImportError:
    print(json.dumps({
        "error": "缺少依赖：pypdf",
        "install": "pip install pypdf"
    }, ensure_ascii=False))
    sys.exit(1)


def extract_text(input_file: str, output_file: str = None) -> dict:
    """
    从 PDF 中提取文本
    
    Args:
        input_file: 输入文件
        output_file: 输出文件（可选）
    
    Returns:
        结果字典
    """
    try:
        if not os.path.exists(input_file):
            return {"error": f"文件不存在：{input_file}"}
        
        reader = PdfReader(input_file)
        text_content = []
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                text_content.append(f"--- 第{i + 1}页 ---\n{text}")
        
        full_text = "\n\n".join(text_content)
        
        result = {
            "success": True,
            "message": f"成功提取 {len(reader.pages)} 页文本",
            "pages": len(reader.pages),
            "char_count": len(full_text)
        }
        
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(full_text)
            result["output"] = output_file
        else:
            result["text"] = full_text[:5000]  # 限制输出长度
            if len(full_text) > 5000:
                result["note"] = "文本过长，仅显示前 5000 字符"
        
        return result
        
    except Exception as e:
        return {"error": f"提取失败：{str(e)}"}


def main():
    args = sys.argv[1:]
    
    if len(args) < 1:
        print(json.dumps({
            "error": "用法：extract_text.py --input input.pdf [--output output.txt]",
            "example": "python extract_text.py --input file.pdf --output text.txt"
        }, ensure_ascii=False))
        sys.exit(1)
    
    # 解析参数
    input_file = None
    output_file = None
    
    i = 0
    while i < len(args):
        if args[i] == "--input" and i + 1 < len(args):
            input_file = args[i + 1]
            i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        else:
            i += 1
    
    if not input_file:
        print(json.dumps({"error": "请指定输入文件"}))
        sys.exit(1)
    
    # 执行提取
    result = extract_text(input_file, output_file)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
