#!/usr/bin/env python3
"""给 PDF 添加页码（使用 reportlab）"""

import sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def create_page_number_page(page_num, total_pages):
    """创建只包含页码的 PDF 页面"""
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=A4)
    
    # A4 尺寸：595 × 842 points
    # 页码位置：右下角
    text = f"Page {page_num} of {total_pages}"
    c.setFont("Helvetica", 9)
    c.setFillColorRGB(0.4, 0.45, 0.54)  # 灰色 #64748B
    c.drawRightString(575, 20, text)  # 距离右边 20pt，底部 20pt
    
    c.showPage()
    c.save()
    
    packet.seek(0)
    return packet

def add_page_numbers(input_pdf, output_pdf):
    """给 PDF 添加页码"""
    try:
        reader = PdfReader(input_pdf)
        writer = PdfWriter()
        
        total_pages = len(reader.pages)
        
        for i, page in enumerate(reader.pages, start=1):
            # 创建页码层
            page_number_packet = create_page_number_page(i, total_pages)
            page_number_pdf = PdfReader(page_number_packet)
            
            # 合并原页面和页码层
            page.merge_page(page_number_pdf.pages[0])
            writer.add_page(page)
        
        with open(output_pdf, 'wb') as f:
            writer.write(f)
        
        print(f"✅ 已添加页码（共 {total_pages} 页）")
        return True
        
    except Exception as e:
        print(f"❌ 处理失败：{e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法：python3 add-pagenumbers.py <input.pdf> <output.pdf>")
        print("示例：python3 add-pagenumbers.py input.pdf output.pdf")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    output_pdf = sys.argv[2]
    
    add_page_numbers(input_pdf, output_pdf)
