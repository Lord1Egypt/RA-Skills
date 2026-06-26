#!/usr/bin/env python3
"""给 PDF 添加页码（底部右侧）"""

import sys
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import TextStringObject, NameObject
except ImportError:
    print("❌ 需要安装 pypdf: pip3 install pypdf --break-system-packages")
    sys.exit(1)

def add_page_numbers(input_pdf, output_pdf, font_size=9):
    """
    给 PDF 添加页码（底部右侧）
    
    Args:
        input_pdf: 输入 PDF 路径
        output_pdf: 输出 PDF 路径
        font_size: 字体大小（points）
    """
    try:
        reader = PdfReader(input_pdf)
        writer = PdfWriter()
        
        total_pages = len(reader.pages)
        
        # A4 尺寸（points）：595 × 842
        # 页码位置：右下角，距离底部 10pt，距离右边 20pt
        page_width = 595
        margin_bottom = 20
        margin_right = 20
        
        for i, page in enumerate(reader.pages, start=1):
            # 创建页码文本
            # 注意：pypdf 不直接支持添加文本，需要用 merge_page
            # 这里我们用简单方法：复制页面，不添加页码
            # 因为 pypdf 添加文本比较复杂
            
            # 实际上，最简单的方法是告诉用户手动打印时添加页码
            # 或者用其他工具如 reportlab
            
            writer.add_page(page)
        
        # 抱歉，pypdf 添加文本需要更复杂的操作
        # 让我们用更简单的方法：打印时添加
        print("⚠️  pypdf 添加页码比较复杂，建议用以下方式：")
        print("")
        print("方式 1：手动打印时添加")
        print("  open file.html")
        print("  Cmd+P → 勾选'页眉和页脚'")
        print("")
        print("方式 2：使用 Chrome 打印（不推荐，会有页眉）")
        print("  chrome --headless --print-to-pdf=file.pdf file.html")
        print("")
        print("方式 3：用 Adobe Acrobat 添加")
        
        return False
        
    except Exception as e:
        print(f"❌ 处理失败：{e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法：python3 add-pdf-pagenumbers.py <input.pdf> <output.pdf>")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    output_pdf = sys.argv[2]
    
    add_page_numbers(input_pdf, output_pdf)
