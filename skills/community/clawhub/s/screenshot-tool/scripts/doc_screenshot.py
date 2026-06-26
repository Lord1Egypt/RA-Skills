#!/usr/bin/env python3
"""
文档转图片工具 - 将 PPT/Word/Excel/PDF 转为高清图片
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, timeout=120):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"


def convert_to_pdf(input_file, output_dir):
    """
    使用 LibreOffice 将文档转为 PDF
    
    Args:
        input_file: 输入文件路径
        output_dir: 输出目录
    
    Returns:
        PDF 文件路径或 None
    """
    print(f"Converting to PDF: {input_file}")
    
    cmd = f'libreoffice --headless --convert-to pdf --outdir "{output_dir}" "{input_file}"'
    success, stdout, stderr = run_command(cmd, timeout=120)
    
    if not success:
        print(f"Error converting to PDF: {stderr}")
        return None
    
    # 获取生成的 PDF 文件名
    input_path = Path(input_file)
    pdf_name = input_path.stem + ".pdf"
    pdf_path = os.path.join(output_dir, pdf_name)
    
    if os.path.exists(pdf_path):
        print(f"PDF created: {pdf_path}")
        return pdf_path
    else:
        print("PDF file not found after conversion")
        return None


def pdf_to_images(pdf_path, output_dir, dpi=300, first_page=None, last_page=None):
    """
    使用 pdf2image 将 PDF 转为图片
    
    Args:
        pdf_path: PDF 文件路径
        output_dir: 输出目录
        dpi: 分辨率（默认 300）
        first_page: 起始页码
        last_page: 结束页码
    
    Returns:
        生成的图片路径列表
    """
    try:
        from pdf2image import convert_from_path
    except ImportError:
        print("Error: pdf2image not installed. Run: pip3 install pdf2image")
        return []
    
    print(f"Converting PDF to images (DPI={dpi})...")
    
    # 转换参数
    kwargs = {'dpi': dpi}
    if first_page:
        kwargs['first_page'] = first_page
    if last_page:
        kwargs['last_page'] = last_page
    
    try:
        images = convert_from_path(pdf_path, **kwargs)
    except Exception as e:
        print(f"Error converting PDF: {e}")
        return []
    
    # 保存图片
    output_files = []
    pdf_name = Path(pdf_path).stem
    
    for i, image in enumerate(images):
        page_num = (first_page or 1) + i
        output_filename = f"{pdf_name}_page{page_num}_hd.png"
        output_path = os.path.join(output_dir, output_filename)
        
        image.save(output_path, "PNG")
        output_files.append(output_path)
        print(f"✓ Saved page {page_num}: {output_path}")
    
    return output_files


def convert_document(input_file, output_dir, dpi=300, first_page=None, last_page=None, keep_pdf=False):
    """
    转换文档为图片
    
    Args:
        input_file: 输入文件路径
        output_dir: 输出目录
        dpi: 分辨率
        first_page: 起始页码
        last_page: 结束页码
        keep_pdf: 是否保留中间 PDF 文件
    
    Returns:
        生成的图片路径列表
    """
    input_path = Path(input_file)
    
    # 检查输入文件
    if not input_path.exists():
        print(f"Error: File not found: {input_file}")
        return []
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 如果是 PDF，直接转换
    if input_path.suffix.lower() == '.pdf':
        pdf_path = input_file
    else:
        # 其他格式先转为 PDF
        pdf_path = convert_to_pdf(input_file, output_dir)
        if not pdf_path:
            return []
    
    # PDF 转图片
    output_files = pdf_to_images(
        pdf_path=pdf_path,
        output_dir=output_dir,
        dpi=dpi,
        first_page=first_page,
        last_page=last_page
    )
    
    # 清理中间 PDF（如果不是原始输入）
    if not keep_pdf and input_path.suffix.lower() != '.pdf':
        try:
            os.remove(pdf_path)
            print(f"Removed intermediate PDF: {pdf_path}")
        except Exception as e:
            print(f"Warning: Could not remove PDF: {e}")
    
    return output_files


def main():
    parser = argparse.ArgumentParser(description='文档转图片工具')
    parser.add_argument('--input', required=True, help='输入文件路径')
    parser.add_argument('--output-dir', required=True, help='输出目录')
    parser.add_argument('--dpi', type=int, default=300, help='分辨率（默认 300）')
    parser.add_argument('--first-page', type=int, help='起始页码')
    parser.add_argument('--last-page', type=int, help='结束页码')
    parser.add_argument('--keep-pdf', action='store_true', help='保留中间 PDF 文件')
    
    args = parser.parse_args()
    
    print(f"Input file: {args.input}")
    print(f"Output directory: {args.output_dir}")
    print(f"DPI: {args.dpi}")
    
    output_files = convert_document(
        input_file=args.input,
        output_dir=args.output_dir,
        dpi=args.dpi,
        first_page=args.first_page,
        last_page=args.last_page,
        keep_pdf=args.keep_pdf
    )
    
    if output_files:
        print(f"\n✅ Successfully converted {len(output_files)} pages")
        return 0
    else:
        print("\n❌ Conversion failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
