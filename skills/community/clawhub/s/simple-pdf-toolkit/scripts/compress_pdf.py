#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 压缩工具
压缩 PDF 文件大小
"""

import sys
import os
import json
import subprocess

try:
    from pypdf import PdfWriter, PdfReader, PdfMerger
except ImportError:
    print(json.dumps({
        "error": "缺少依赖：pypdf",
        "install": "pip install pypdf"
    }, ensure_ascii=False))
    sys.exit(1)


def compress_pdf(input_file: str, output_file: str, quality: str = "medium") -> dict:
    """
    压缩 PDF 文件
    
    Args:
        input_file: 输入文件
        output_file: 输出文件
        quality: 质量等级（low, medium, high）
    
    Returns:
        结果字典
    """
    try:
        if not os.path.exists(input_file):
            return {"error": f"文件不存在：{input_file}"}
        
        original_size = os.path.getsize(input_file)
        
        # 检查是否有 ghostscript
        has_ghostscript = False
        try:
            subprocess.run(["gs", "--version"], capture_output=True, check=True)
            has_ghostscript = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        if has_ghostscript:
            # 使用 Ghostscript 压缩（效果更好）
            dpi_map = {"low": 72, "medium": 150, "high": 300}
            dpi = dpi_map.get(quality, 150)
            
            cmd = [
                "gs", "-sDEVICE=pdfwrite",
                "-dCompatibilityLevel=1.4",
                f"-dPDFSETTINGS=/ebook" if quality == "medium" else 
                f"-dPDFSETTINGS=/screen" if quality == "low" else 
                f"-dPDFSETTINGS=/printer",
                f"-dDownsampleColorImages=true",
                f"-dColorImageResolution={dpi}",
                f"-dDownsampleGrayImages=true",
                f"-dGrayImageResolution={dpi}",
                f"-dDownsampleMonoImages=true",
                f"-dMonoImageResolution={dpi}",
                "-dNOPAUSE", "-dBATCH", "-dQUIET",
                f"-sOutputFile={output_file}",
                input_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if os.path.exists(output_file):
                compressed_size = os.path.getsize(output_file)
                ratio = (1 - compressed_size / original_size) * 100
                
                return {
                    "success": True,
                    "message": f"压缩成功，减小{ratio:.1f}%",
                    "output": output_file,
                    "original_size": f"{original_size / 1024:.1f} KB",
                    "compressed_size": f"{compressed_size / 1024:.1f} KB",
                    "method": "ghostscript"
                }
        
        # 降级方案：使用 pypdf 简单压缩
        reader = PdfReader(input_file)
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        # 压缩流
        writer.compress_identical_objects(remove_unreferenced_resources=True)
        
        with open(output_file, "wb") as f:
            writer.write(f)
        
        compressed_size = os.path.getsize(output_file)
        ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
        
        return {
            "success": True,
            "message": f"压缩成功，减小{ratio:.1f}%",
            "output": output_file,
            "original_size": f"{original_size / 1024:.1f} KB",
            "compressed_size": f"{compressed_size / 1024:.1f} KB",
            "method": "pypdf",
            "note": "安装 Ghostscript 可获得更好压缩效果"
        }
        
    except Exception as e:
        return {"error": f"压缩失败：{str(e)}"}


def main():
    args = sys.argv[1:]
    
    if len(args) < 2:
        print(json.dumps({
            "error": "用法：compress_pdf.py --input input.pdf --output output.pdf [--quality low|medium|high]",
            "example": "python compress_pdf.py --input file.pdf --output compressed.pdf --quality medium"
        }, ensure_ascii=False))
        sys.exit(1)
    
    # 解析参数
    input_file = None
    output_file = None
    quality = "medium"
    
    i = 0
    while i < len(args):
        if args[i] == "--input" and i + 1 < len(args):
            input_file = args[i + 1]
            i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        elif args[i] == "--quality" and i + 1 < len(args):
            quality = args[i + 1]
            i += 2
        else:
            i += 1
    
    if not input_file or not output_file:
        print(json.dumps({"error": "请指定输入和输出文件"}))
        sys.exit(1)
    
    if quality not in ["low", "medium", "high"]:
        print(json.dumps({"error": "质量等级必须是 low, medium, 或 high"}))
        sys.exit(1)
    
    # 执行压缩
    result = compress_pdf(input_file, output_file, quality)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
