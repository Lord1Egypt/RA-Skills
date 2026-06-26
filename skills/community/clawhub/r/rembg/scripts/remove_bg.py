#!/usr/bin/env python3
"""
rembg 单张图片去背景脚本
首次使用自动检测并安装环境
"""
import os
import sys
import subprocess
import argparse
from datetime import datetime as dt


# 用户根目录下的虚拟环境
VENV_DIR = os.path.expanduser("~/.venv/rembg")

# 项目根目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)


def check_python():
    """检查系统是否有 Python"""
    # 检查系统 Python
    python_cmds = ["python3", "python"]
    system_python = None
    
    for cmd in python_cmds:
        try:
            result = subprocess.run([cmd, "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                system_python = cmd
                break
        except:
            continue
    
    if not system_python:
        print("=" * 60)
        print("✗ 未找到 Python (Python not found)")
        print("=" * 60)
        print()
        print("请先安装 Python (Please install Python first):")
        print("  - macOS: brew install python3")
        print("  - Linux: sudo apt install python3 / sudo yum install python3")
        print("  - Windows: https://www.python.org/downloads/")
        print()
        sys.exit(1)
    
    return system_python


def check_and_install_env():
    """检查并自动安装环境"""
    venv_python = os.path.join(VENV_DIR, "bin", "python")
    
    # 如果虚拟环境不存在或没有 rembg，自动安装
    if not os.path.exists(venv_python):
        print("=" * 50)
        print("首次使用，正在初始化环境... (First use, initializing environment...)")
        print("=" * 50)
        
        install_script = os.path.join(PROJECT_ROOT, "setup", "install.py")
        result = subprocess.run([sys.executable, install_script], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"✗ 环境初始化失败 (Environment initialization failed): {result.stderr}")
            sys.exit(1)
        
        print("✓ 环境初始化完成! (Environment initialized!)")
        print()
    else:
        # 检查 rembg 是否安装
        try:
            subprocess.run([venv_python, "-c", "import rembg"], 
                        capture_output=True, check=True)
        except:
            print("=" * 50)
            print("rembg 未安装，正在安装... (rembg not found, installing...)")
            print("=" * 50)
            
            install_script = os.path.join(PROJECT_ROOT, "setup", "install.py")
            result = subprocess.run([sys.executable, install_script], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"✗ 环境初始化失败 (Environment initialization failed): {result.stderr}")
                sys.exit(1)
            
            print("✓ 环境初始化完成! (Environment initialized!)")
            print()


def get_output_path(input_path):
    """获取默认输出路径"""
    today = dt.now().strftime("%Y-%m-%d")
    output_dir = os.path.join(PROJECT_ROOT, "image_output", "single", today)
    os.makedirs(output_dir, exist_ok=True)
    
    basename = os.path.basename(input_path)
    name, _ = os.path.splitext(basename)
    return os.path.join(output_dir, f"{name}_nobg.png")


def main():
    # 先检查 Python
    check_python()
    
    parser = argparse.ArgumentParser(description="rembg 单张图片去背景 (Remove background from single image)")
    parser.add_argument("input", help="输入图片路径 (Input image path)")
    parser.add_argument("-o", "--output", help="输出图片路径（默认自动生成）(Output image path)")
    parser.add_argument("-m", "--model", default="u2net", help="使用的模型（默认 u2net）(Model to use)")
    
    args = parser.parse_args()
    
    input_file = args.input
    
    # 自动检查并安装环境
    check_and_install_env()
    
    # 检查输入文件
    if not os.path.exists(input_file):
        print(f"✗ 输入文件不存在 (Input file not found): {input_file}")
        sys.exit(1)
    
    # 确定输出路径
    output_file = args.output if args.output else get_output_path(input_file)
    
    print(f"输入 (Input): {input_file}")
    print(f"输出 (Output): {output_file}")
    print(f"模型 (Model): {args.model}")
    print()
    
    # 创建输出目录
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    print("处理中... (Processing...)")
    
    # 使用用户根目录下的虚拟环境
    venv_python = os.path.join(VENV_DIR, "bin", "python")
    
    cmd = [
        venv_python, "-c",
        f"""
from rembg import remove
from PIL import Image

input_img = Image.open('{input_file}')
output_img = remove(input_img)
output_img.save('{output_file}')
print('OK')
"""
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"✗ 处理失败 (Processing failed): {result.stderr}")
        sys.exit(1)
    
    print(f"✓ 处理完成! (Done!)")
    print(f"输出文件 (Output file): {output_file}")


if __name__ == "__main__":
    main()
