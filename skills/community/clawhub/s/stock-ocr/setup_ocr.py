#!/usr/bin/env python3
"""
OCR引擎安装和配置脚本
自动检测并安装可用的OCR引擎
"""

import os
import subprocess
import sys


def run_command(cmd, check=True):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if check and result.returncode != 0:
            return False, result.stderr
        return True, result.stdout
    except Exception as e:
        return False, str(e)


def check_pip_package(package):
    """检查pip包是否已安装"""
    success, output = run_command(f'pip show {package}', check=False)
    return success


def install_pip_package(package):
    """安装pip包"""
    print(f"正在安装 {package}...")
    success, output = run_command(f'pip install {package} --user')
    return success


def check_tesseract():
    """检查Tesseract是否安装"""
    success, output = run_command('tesseract --version', check=False)
    return success


def check_windows_ocr():
    """检查Windows OCR是否可用"""
    # Windows 10/11内置,直接返回True
    return sys.platform == 'win32'


def check_baidu_ocr():
    """检查百度OCR是否配置"""
    return bool(os.environ.get('BAIDU_ACCESS_TOKEN') or 
               (os.environ.get('BAIDU_API_KEY') and os.environ.get('BAIDU_SECRET_KEY')))


def main():
    print("=" * 60)
    print("OCR引擎安装和配置工具")
    print("=" * 60)
    print()
    
    # 检查当前状态
    print("检查OCR引擎状态:\n")
    
    engines = {
        'Windows内置OCR': check_windows_ocr(),
        '百度OCR (需配置)': check_baidu_ocr(),
        'RapidOCR': check_pip_package('rapidocr-onnxruntime'),
        'Tesseract': check_tesseract(),
    }
    
    for name, available in engines.items():
        status = "✅" if available else "❌"
        print(f"  {status} {name}")
    
    print()
    print("=" * 60)
    print("安装选项:")
    print("=" * 60)
    print()
    print("1. 安装RapidOCR (推荐 - 本地运行,免费)")
    print("2. 配置百度OCR (推荐 - 高精度,免费1000次/月)")
    print("3. 安装Tesseract OCR (可选 - 本地运行)")
    print("4. 全部安装")
    print("0. 退出")
    print()
    
    choice = input("请选择 [0-4]: ").strip()
    
    if choice == '0':
        print("退出")
        return
    
    if choice in ['1', '4']:
        print("\n安装RapidOCR...")
        if install_pip_package('rapidocr-onnxruntime'):
            print("✅ RapidOCR安装成功")
        else:
            print("❌ RapidOCR安装失败")
    
    if choice in ['2', '4']:
        print("\n配置百度OCR...")
        print("\n请访问: https://console.bce.baidu.com/ai/#/ai/ocr/overview/index")
        print("创建应用后获取 API Key 和 Secret Key\n")
        
        api_key = input("请输入 API Key (留空跳过): ").strip()
        if api_key:
            secret_key = input("请输入 Secret Key: ").strip()
            if secret_key:
                # 设置环境变量
                print("\n设置环境变量...")
                run_command(f'setx BAIDU_API_KEY "{api_key}"')
                run_command(f'setx BAIDU_SECRET_KEY "{secret_key}"')
                print("✅ 环境变量已设置")
                print("⚠️ 请重启终端或重新打开命令窗口使环境变量生效")
    
    if choice in ['3', '4']:
        print("\n安装Tesseract OCR...")
        print("请手动下载安装:")
        print("https://github.com/UB-Mannheim/tesseract/wiki")
        print("\n安装时请勾选:")
        print("  - Additional language data -> Chinese - Simplified")
        print("  - Add to PATH")
    
    print("\n" + "=" * 60)
    print("配置完成!")
    print("=" * 60)
    print("\n使用方法:")
    print("  python capture_ma20_v2.py 000001 --engine baidu")
    print("  python capture_ma20_v2.py 000001 --engine rapidocr")
    print("  python capture_ma20_v2.py --list-engines")


if __name__ == "__main__":
    main()
