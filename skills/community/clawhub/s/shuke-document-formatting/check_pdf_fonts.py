#!/usr/bin/env python3
"""
检查PDF中使用的字体
"""

import subprocess
import os
import sys
import re

def extract_fonts_from_pdf(pdf_path):
    """
    使用pdffonts工具提取PDF中的字体信息
    如果pdffonts不可用，使用其他方法
    """
    # 尝试使用pdffonts
    try:
        result = subprocess.run(['pdffonts', pdf_path], 
                              capture_output=True, text=True, check=True)
        print("PDF字体信息:")
        print(result.stdout)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("pdffonts工具不可用，尝试其他方法...")
    
    # 尝试使用pdfinfo
    try:
        result = subprocess.run(['pdfinfo', pdf_path], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("PDF基本信息:")
            print(result.stdout)
    except FileNotFoundError:
        pass
    
    # 使用Python的PyPDF2提取文本并分析
    try:
        import PyPDF2
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            print(f"PDF页数: {len(pdf_reader.pages)}")
            print("提取第一页文本进行分析...")
            
            if len(pdf_reader.pages) > 0:
                text = pdf_reader.pages[0].extract_text()
                
                # 分析中文字符
                chinese_chars = [c for c in text if '\u4e00' <= c <= '\u9fff']
                if chinese_chars:
                    print(f"中文字符示例: {''.join(chinese_chars[:20])}...")
                    print(f"中文字符总数: {len(chinese_chars)}")
                
                # 检查是否有特定字符
                test_chars = ['算', '力', '调', '度', '平', '台']
                for char in test_chars:
                    count = text.count(char)
                    print(f"字符 '{char}' 出现次数: {count}")
                
                # 输出前200个字符
                print("\n第一页文本前200字符:")
                print(text[:200])
    except Exception as e:
        print(f"使用PyPDF2分析时出错: {e}")
    
    return False

def check_system_fonts():
    """检查系统字体"""
    print("\n" + "="*60)
    print("系统可用中文字体:")
    print("="*60)
    
    try:
        result = subprocess.run(['fc-list', ':lang=zh'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            fonts = result.stdout.strip().split('\n')
            for font in fonts[:20]:  # 只显示前20个
                print(font)
            print(f"... 总共 {len(fonts)} 个中文字体")
    except Exception as e:
        print(f"检查系统字体时出错: {e}")

def compare_required_fonts():
    """比较要求的字体和系统可用字体"""
    required_fonts = [
        '方正小标宋简体',
        '仿宋GB2312', 
        '楷体GB2312',
        '黑体'
    ]
    
    available_fonts = []
    try:
        result = subprocess.run(['fc-list'], 
                              capture_output=True, text=True)
        font_list = result.stdout.lower()
        
        print("\n" + "="*60)
        print("要求的字体匹配情况:")
        print("="*60)
        
        for font in required_fonts:
            font_lower = font.lower()
            if font_lower in font_list:
                print(f"✓ {font} - 系统中存在")
                available_fonts.append(font)
            else:
                print(f"✗ {font} - 系统中不存在")
                
                # 寻找可能的替代字体
                print(f"  寻找替代字体...")
                if '仿宋' in font:
                    # 检查仿宋类字体
                    if 'uming' in font_list or 'noto serif cjk sc' in font_list:
                        print(f"  → 可用替代: AR PL UMing CN / Noto Serif CJK SC")
                elif '楷体' in font:
                    # 检查楷体类字体
                    if 'ukai' in font_list or 'kai' in font_list:
                        print(f"  → 可用替代: AR PL UKai CN")
                elif '黑体' in font:
                    # 检查黑体类字体
                    if 'noto sans cjk sc' in font_list or 'wqy' in font_list:
                        print(f"  → 可用替代: Noto Sans CJK SC / WenQuanYi Micro Hei")
                elif '方正小标宋简体' in font:
                    # 检查宋体类字体
                    if 'noto serif cjk sc' in font_list:
                        print(f"  → 可用替代: Noto Serif CJK SC")
        
        return available_fonts
        
    except Exception as e:
        print(f"检查字体匹配时出错: {e}")
        return []

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        if os.path.exists(pdf_path):
            extract_fonts_from_pdf(pdf_path)
            check_system_fonts()
            compare_required_fonts()
        else:
            print(f"文件不存在: {pdf_path}")
    else:
        # 检查最新的PDF文件
        pdf_path = "/root/.openclaw/workspace/英文文件名文档/01_AI_Research_Scheduling_Platform_with_fonts.pdf"
        if os.path.exists(pdf_path):
            extract_fonts_from_pdf(pdf_path)
            check_system_fonts()
            compare_required_fonts()
        else:
            print("请提供PDF文件路径")