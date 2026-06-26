#!/usr/bin/env python3
"""
Markdown评估报告导出为PDF工具
"""
import os
import sys
from pathlib import Path
from markdown_pdf import MarkdownPdf, Section

def export_markdown_to_pdf(md_path: str, output_pdf_path: str = None) -> str:
    """
    将Markdown格式的评估报告导出为PDF文件
    参数:
        md_path: Markdown文件路径
        output_pdf_path: 输出PDF文件路径，可选，默认与Markdown同目录同名
    返回:
        生成的PDF文件路径
    """
    if not os.path.exists(md_path):
        print(f"错误：Markdown文件不存在: {md_path}")
        return None
    
    if output_pdf_path is None:
        # 默认输出路径：与markdown同目录，替换扩展名为pdf
        output_pdf_path = Path(md_path).with_suffix('.pdf')
    
    try:
        # 读取Markdown内容
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # 创建PDF生成器
        pdf = MarkdownPdf(toc_level=2)
        # 添加内容
        pdf.add_section(Section(md_content))
        # 设置PDF元数据
        pdf.meta["title"] = "求职岗位评估报告"
        pdf.meta["author"] = "智能简历岗位匹配助手"
        # 保存PDF
        pdf.save(output_pdf_path)
        
        print(f"PDF报告导出成功: {output_pdf_path}")
        return str(output_pdf_path)
    
    except Exception as e:
        print(f"PDF导出失败: {str(e)}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("用法: ")
        print("  python export_pdf.py <Markdown文件路径> [输出PDF路径]")
        print("示例:")
        print("  python export_pdf.py 评估报告.md")
        print("  python export_pdf.py 评估报告.md 输出报告.pdf")
        sys.exit(1)
    
    md_path = sys.argv[1]
    output_pdf_path = sys.argv[2] if len(sys.argv) == 3 else None
    
    result = export_markdown_to_pdf(md_path, output_pdf_path)
    if not result:
        sys.exit(1)