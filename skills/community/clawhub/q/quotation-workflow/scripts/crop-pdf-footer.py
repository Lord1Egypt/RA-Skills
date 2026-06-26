#!/usr/bin/env python3
"""裁剪 PDF 底部（移除页脚）"""

import sys
import subprocess
from pathlib import Path

def crop_pdf_header_footer(input_pdf, output_pdf, crop_top_mm=10, crop_bottom_mm=10):
    """
    裁剪 PDF 顶部和底部（移除页眉页脚）
    
    Args:
        input_pdf: 输入 PDF 路径
        output_pdf: 输出 PDF 路径
        crop_top_mm: 从顶部裁剪的高度（毫米）
        crop_bottom_mm: 从底部裁剪的高度（毫米）
    """
    # 使用 pdftk 或 qpdf 如果有的话
    # 否则用 pypdf 如果安装了
    
    try:
        import pypdf
        from pypdf import PdfReader, PdfWriter
        from pypdf.generic import RectangleObject
        
        reader = PdfReader(input_pdf)
        writer = PdfWriter()
        
        # A4 尺寸：210 × 297 mm
        # 转换为 points：1 mm = 2.83465 points
        crop_top_points = crop_top_mm * 2.83465
        crop_bottom_points = crop_bottom_mm * 2.83465
        
        for page in reader.pages:
            # 获取原始尺寸
            original_box = page.mediabox
            
            # 设置新的媒体框（裁剪顶部和底部）
            page.mediabox = RectangleObject([
                original_box.left,
                original_box.bottom + crop_bottom_points,
                original_box.right,
                original_box.top - crop_top_points
            ])
            
            # 设置裁剪框
            page.cropbox = page.mediabox
            
            writer.add_page(page)
        
        with open(output_pdf, 'wb') as f:
            writer.write(f)
        
        print(f"✅ 已裁剪顶部 {crop_top_mm}mm，底部 {crop_bottom_mm}mm")
        return True
        
    except ImportError:
        print("❌ 需要安装 pypdf: pip3 install pypdf")
        return False
    except Exception as e:
        print(f"❌ 处理失败：{e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法：python3 crop-pdf-footer.py <input.pdf> <output.pdf> [crop_top_mm] [crop_bottom_mm]")
        print("示例：python3 crop-pdf-footer.py input.pdf output.pdf 10 10")
        print("        python3 crop-pdf-footer.py input.pdf output.pdf 10  # 只裁剪底部 10mm")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    output_pdf = sys.argv[2]
    crop_top = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    crop_bottom = int(sys.argv[4]) if len(sys.argv) > 4 else crop_top
    
    crop_pdf_header_footer(input_pdf, output_pdf, crop_top, crop_bottom)
