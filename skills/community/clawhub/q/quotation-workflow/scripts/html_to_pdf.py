#!/usr/bin/env python3
"""从 HTML 生成 PDF - 使用浏览器打印功能"""

import sys
import os
import webbrowser
import subprocess
from pathlib import Path

def open_in_browser(html_path):
    """在默认浏览器打开 HTML 文件"""
    html_path = os.path.abspath(html_path)
    url = f"file://{html_path}"
    
    print(f"🌐 在浏览器打开：{url}")
    webbrowser.open(url)
    
    print("\n💡 导出 PDF 步骤：")
    print("   1. 等待页面完全加载")
    print("   2. 按 Cmd+P (Mac) 或 Ctrl+P (Windows)")
    print("   3. 选择 '保存为 PDF' 或 'Microsoft Print to PDF'")
    print("   4. 点击 '保存'")
    print("\n   或者点击右上角的 'Export to PDF' 按钮（如果浏览器支持）")
    
    return True

def main():
    if len(sys.argv) < 2:
        print("用法：python3 html_to_pdf.py <HTML 文件>")
        print("示例：python3 html_to_pdf.py QT-20260314-001.html")
        sys.exit(1)
    
    html_path = sys.argv[1]
    
    if not os.path.exists(html_path):
        print(f"❌ 文件不存在：{html_path}")
        sys.exit(1)
    
    open_in_browser(html_path)

if __name__ == '__main__':
    main()
