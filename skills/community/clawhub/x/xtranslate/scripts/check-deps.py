#!/usr/bin/env python3
"""
依赖检查脚本
检查项目所需的所有依赖是否已安装
"""

import sys

REQUIRED_PACKAGES = {
    "openai": "云端模型API调用",
    "ollama": "本地Ollama模型",
    "docx": "Word文档处理 (python-docx)",
    "pdf2docx": "PDF转Word",
    "openpyxl": "Excel处理",
    "pptx": "PPT处理 (python-pptx)",
    "ezdxf": "CAD文件处理",
    "jieba": "中文分词",
    "cryptography": "加密工具",
    "translate": "Python内置翻译",
    "striprtf": "RTF文件处理",
    "customtkinter": "现代化GUI",
}

OPTIONAL_PACKAGES = {
    "PyInstaller": "打包为可执行文件",
}

def check_package(package_name):
    """检查单个包是否已安装"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def main():
    print("=" * 60)
    print("Xtranslate 依赖检查工具")
    print("=" * 60)
    
    missing_required = []
    missing_optional = []
    
    print("\n【必需依赖】")
    for pkg, desc in REQUIRED_PACKAGES.items():
        installed = check_package(pkg)
        status = "✅ 已安装" if installed else "❌ 未安装"
        print(f"  {status} {pkg:20} - {desc}")
        if not installed:
            missing_required.append(pkg)
    
    print("\n【可选依赖】")
    for pkg, desc in OPTIONAL_PACKAGES.items():
        installed = check_package(pkg)
        status = "✅ 已安装" if installed else "⚠️  未安装"
        print(f"  {status} {pkg:20} - {desc}")
        if not installed:
            missing_optional.append(pkg)
    
    print("\n" + "=" * 60)
    
    if missing_required:
        print(f"\n❌ 缺少 {len(missing_required)} 个必需依赖:")
        print(f"   pip install {' '.join(missing_required)}")
        sys.exit(1)
    else:
        print("\n✅ 所有必需依赖已安装！")
        
    if missing_optional:
        print(f"\n⚠️  可选依赖未安装: {', '.join(missing_optional)}")
        
    sys.exit(0)

if __name__ == "__main__":
    main()
