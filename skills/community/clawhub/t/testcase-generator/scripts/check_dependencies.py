#!/usr/bin/env python3
"""
依赖检测与安装指引
"""

import sys
import subprocess

def check_package(package_name, import_name=None):
    """检查包是否安装"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        return True, None
    except ImportError as e:
        return False, str(e)

def main():
    print("=" * 60)
    print("测试用例生成技能 - 依赖检测")
    print("=" * 60)
    
    dependencies = [
        ("openpyxl", "openpyxl", "Excel 导出"),
        ("docx", "python-docx", "Word 文档解析"),
        ("pdfplumber", "pdfplumber", "PDF 文档解析"),
    ]
    
    all_installed = True
    missing = []
    
    for import_name, package_name, description in dependencies:
        installed, error = check_package(import_name)
        status = "✅" if installed else "❌"
        print(f"{status} {package_name:20s} - {description}")
        
        if not installed:
            all_installed = False
            missing.append(package_name)
    
    print("=" * 60)
    
    if all_installed:
        print("✅ 所有依赖已安装，可以正常使用！")
        return 0
    else:
        print("\n⚠️  检测到缺失的依赖，请运行以下命令安装：\n")
        print(f"   pip install {' '.join(missing)}\n")
        print("或者逐个安装：")
        for pkg in missing:
            print(f"   pip install {pkg}")
        print()
        return 1

if __name__ == '__main__':
    sys.exit(main())
