#!/usr/bin/env python3
"""
Tesseract OCR 自动安装脚本
适用于Windows系统
"""

import os
import sys
import subprocess
import requests
import tempfile
import shutil
from pathlib import Path
import time

def print_header():
    """打印标题"""
    print("=" * 60)
    print("OPENCLAW(龙虾)-屏幕查看器 - Tesseract OCR安装程序")
    print("=" * 60)
    print("此脚本将自动下载和安装Tesseract OCR引擎")
    print("用于屏幕文字识别功能")
    print("=" * 60)

def check_os():
    """检查操作系统"""
    print("\n检查操作系统...")
    if sys.platform != "win32":
        print(f"[警告] 当前系统: {sys.platform}")
        print("此脚本仅支持Windows系统")
        print("其他系统请手动安装:")
        print("  macOS: brew install tesseract")
        print("  Linux: sudo apt-get install tesseract-ocr")
        return False
    print("[成功] Windows系统检测通过")
    return True

def check_existing_tesseract():
    """检查是否已安装Tesseract"""
    print("\n检查Tesseract OCR...")
    
    paths_to_check = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.join(os.environ.get("ProgramFiles", ""), "Tesseract-OCR", "tesseract.exe"),
    ]
    
    for tesseract_path in paths_to_check:
        if os.path.exists(tesseract_path):
            print(f"[成功] 发现Tesseract: {tesseract_path}")
            # 测试版本
            try:
                result = subprocess.run([tesseract_path, "--version"], 
                                      capture_output=True, text=True, encoding='utf-8')
                if result.returncode == 0:
                    version_info = result.stdout.strip().split('\n')[0]
                    print(f"[成功] 版本: {version_info}")
                    return tesseract_path
            except:
                pass
            return tesseract_path
    
    print("[信息] 未发现已安装的Tesseract OCR")
    return None

def download_tesseract_installer():
    """下载Tesseract安装程序"""
    print("\n下载Tesseract OCR安装程序...")
    
    # Tesseract下载URL（使用UB-Mannheim的最新版本）
    # 注意：这里使用一个稳定的版本URL
    tesseract_version = "5.4.0.20241124"
    download_url = f"https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-{tesseract_version}.exe"
    
    # 备用下载链接
    backup_url = "https://github.com/UB-Mannheim/tesseract/releases/latest/download/tesseract-ocr-w64-setup.exe"
    
    temp_dir = tempfile.gettempdir()
    installer_path = os.path.join(temp_dir, "tesseract_installer.exe")
    
    try:
        print(f"下载URL: {download_url}")
        print(f"保存到: {installer_path}")
        
        # 使用requests下载
        response = requests.get(download_url, stream=True, timeout=30)
        
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(installer_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # 显示进度
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\r下载进度: {percent:.1f}% ({downloaded/1024/1024:.1f}MB/{total_size/1024/1024:.1f}MB)", end='')
            
            print(f"\n[成功] 下载完成: {os.path.getsize(installer_path)/1024/1024:.1f} MB")
            return installer_path
        else:
            print(f"[失败] 下载失败，状态码: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"[失败] 下载错误: {e}")
        
        # 尝试备用链接
        print("尝试备用下载链接...")
        try:
            response = requests.get(backup_url, stream=True, timeout=30)
            if response.status_code == 200:
                with open(installer_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print(f"[成功] 使用备用链接下载完成")
                return installer_path
        except Exception as e2:
            print(f"[失败] 备用链接下载失败: {e2}")
            
        return None

def install_tesseract(installer_path):
    """安装Tesseract"""
    print("\n安装Tesseract OCR...")
    
    if not os.path.exists(installer_path):
        print(f"[失败] 安装文件不存在: {installer_path}")
        return False
    
    # 默认安装路径
    default_install_path = r"C:\Program Files\Tesseract-OCR"
    
    try:
        # 静默安装参数
        # /S: 静默安装
        # /D=<路径>: 安装目录
        install_command = f'"{installer_path}" /S /D={default_install_path}'
        
        print(f"安装命令: {install_command}")
        print("正在安装，请稍候...")
        
        # 运行安装程序
        result = subprocess.run(
            install_command,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            print(f"[成功] Tesseract安装完成")
            
            # 验证安装
            time.sleep(2)  # 等待安装完成
            tesseract_exe = os.path.join(default_install_path, "tesseract.exe")
            
            if os.path.exists(tesseract_exe):
                print(f"[成功] Tesseract可执行文件: {tesseract_exe}")
                
                # 检查版本
                version_result = subprocess.run(
                    [tesseract_exe, "--version"],
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                
                if version_result.returncode == 0:
                    print(f"[成功] Tesseract版本信息:")
                    for line in version_result.stdout.strip().split('\n'):
                        if line.strip():
                            print(f"  {line}")
                
                return tesseract_exe
            else:
                print(f"[警告] 未在预期位置找到Tesseract")
                return default_install_path
        else:
            print(f"[失败] 安装失败，返回码: {result.returncode}")
            if result.stderr:
                print(f"错误信息: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"[失败] 安装过程出错: {e}")
        return False

def download_language_packs(tesseract_path):
    """下载语言包"""
    print("\n下载语言包...")
    
    # 创建tessdata目录
    tessdata_dir = os.path.join(os.path.dirname(tesseract_path), "tessdata")
    os.makedirs(tessdata_dir, exist_ok=True)
    
    language_files = {
        "eng": "英语",
        "chi_sim": "简体中文",
        "chi_tra": "繁体中文",
        "jpn": "日语",
        "kor": "韩语"
    }
    
    base_url = "https://github.com/tesseract-ocr/tessdata/raw/main/"
    
    for lang_code, lang_name in language_files.items():
        lang_file = f"{lang_code}.traineddata"
        lang_path = os.path.join(tessdata_dir, lang_file)
        
        if os.path.exists(lang_path):
            print(f"[信息] {lang_name}语言包已存在，跳过下载")
            continue
        
        download_url = f"{base_url}{lang_file}"
        
        try:
            print(f"下载{lang_name}语言包...")
            response = requests.get(download_url, stream=True, timeout=30)
            
            if response.status_code == 200:
                with open(lang_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print(f"[成功] {lang_name}语言包下载完成")
            else:
                print(f"[警告] {lang_name}语言包下载失败，状态码: {response.status_code}")
                
        except Exception as e:
            print(f"[警告] {lang_name}语言包下载失败: {e}")

def configure_python_environment(tesseract_exe):
    """配置Python环境"""
    print("\n配置Python环境...")
    
    config_example = f'''#!/usr/bin/env python3
"""
OCR配置示例
"""

import pytesseract
import os

# 设置Tesseract路径
if os.path.exists("{tesseract_exe}"):
    pytesseract.pytesseract.tesseract_cmd = r"{tesseract_exe}"
    print("Tesseract路径已配置")
else:
    print("[警告] 未找到Tesseract，请检查安装")
    print("或者手动设置路径:")
    print('pytesseract.pytesseract.tesseract_cmd = r"C:\\\\Program Files\\\\Tesseract-OCR\\\\tesseract.exe"')

# 测试OCR
try:
    version = pytesseract.get_tesseract_version()
    print(f"Tesseract版本: {version}")
except:
    print("无法获取Tesseract版本，请检查安装")
'''

    # 保存配置示例
    config_file = "ocr_config_example.py"
    with open(config_file, "w", encoding="utf-8") as f:
        f.write(config_example)
    
    print(f"[成功] 配置示例已保存到: {config_file}")

def test_ocr_installation(tesseract_exe):
    """测试OCR安装"""
    print("\n测试OCR安装...")
    
    try:
        # 测试Tesseract可执行文件
        result = subprocess.run(
            [tesseract_exe, "--list-langs"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.returncode == 0:
            print("[成功] Tesseract安装验证通过")
            if result.stdout.strip():
                print("支持的语言:")
                langs = [lang.strip() for lang in result.stdout.strip().split('\n') if lang.strip()]
                for lang in langs:
                    print(f"  - {lang}")
            return True
        else:
            print("[失败] Tesseract验证失败")
            return False
            
    except Exception as e:
        print(f"[失败] 测试失败: {e}")
        return False

def main():
    """主函数"""
    print_header()
    
    # 检查操作系统
    if not check_os():
        print("\n[失败] 系统不支持，请手动安装")
        return False
    
    # 检查是否已安装
    existing_tesseract = check_existing_tesseract()
    if existing_tesseract:
        print("\n[信息] Tesseract已安装，跳过下载安装")
        tesseract_exe = existing_tesseract
    else:
        # 下载安装程序
        installer_path = download_tesseract_installer()
        if not installer_path:
            print("\n[失败] 无法下载安装程序，请手动下载")
            print("请访问: https://github.com/UB-Mannheim/tesseract/wiki")
            return False
        
        # 安装Tesseract
        tesseract_exe = install_tesseract(installer_path)
        if not tesseract_exe:
            print("\n[失败] 安装失败，请手动安装")
            return False
        
        # 下载语言包
        download_language_packs(tesseract_exe)
    
    # 配置Python环境
    configure_python_environment(tesseract_exe)
    
    # 测试安装
    if test_ocr_installation(tesseract_exe):
        print("\n" + "=" * 60)
        print("[成功] Tesseract OCR安装完成!")
        print("=" * 60)
        print("\n下一步操作:")
        print("1. 安装Python OCR库: pip install pytesseract")
        print("2. 运行OCR测试: python scripts/test_ocr.py")
        print("3. 查看配置示例: cat ocr_config_example.py")
        print("\n如果遇到问题，请查看 docs/OCR_SETUP_GUIDE.md")
        return True
    else:
        print("\n[警告] Tesseract安装完成，但测试失败")
        print("请手动检查安装")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n[信息] 用户中断安装")
        sys.exit(1)