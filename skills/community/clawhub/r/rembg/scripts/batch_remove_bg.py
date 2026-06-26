#!/usr/bin/env python3
"""
rembg 批量图片去背景脚本
首次使用自动检测并安装环境
"""
import os
import sys
import subprocess
import argparse
from datetime import datetime as dt
from pathlib import Path

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


def get_supported_extensions():
    """获取支持的图片格式"""
    return ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.gif']


def get_output_path(input_path, output_dir):
    """获取输出路径"""
    basename = os.path.basename(input_path)
    name, ext = os.path.splitext(basename)
    return os.path.join(output_dir, f"{name}_nobg.png")


def process_image(input_file, output_file):
    """处理单张图片"""
    venv_python = os.path.join(VENV_DIR, "bin", "python")
    
    cmd = [
        venv_python, "-c",
        f"""
from rembg import remove
from PIL import Image

input_img = Image.open('{input_file}')
output_img = remove(input_img)
output_img.save('{output_file}')
"""
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def main():
    # 先检查 Python
    check_python()
    
    parser = argparse.ArgumentParser(description="rembg 批量图片去背景 (Remove background from batch images)")
    parser.add_argument("input_dir", help="输入图片目录 (Input images directory)")
    parser.add_argument("output_dir", nargs="?", help="输出图片目录（默认自动生成）(Output directory)")
    parser.add_argument("-m", "--model", default="u2net", help="使用的模型（默认 u2net）(Model to use)")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细输出 (Show verbose output)")
    
    args = parser.parse_args()
    
    input_dir = args.input_dir
    
    # 自动检查并安装环境
    check_and_install_env()
    
    # 检查输入目录
    if not os.path.isdir(input_dir):
        print(f"✗ 输入目录不存在 (Input directory not found): {input_dir}")
        sys.exit(1)
    
    # 确定输出目录
    if args.output_dir:
        output_dir = args.output_dir
    else:
        today = dt.now().strftime("%Y-%m-%d")
        output_dir = os.path.join(PROJECT_ROOT, "image_output", "batch", today)
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"输入目录 (Input): {input_dir}")
    print(f"输出目录 (Output): {output_dir}")
    print(f"模型 (Model): {args.model}")
    print()
    
    # 获取所有支持的图片
    extensions = get_supported_extensions()
    image_files = []
    for ext in extensions:
        image_files.extend(Path(input_dir).glob(f"*{ext}"))
        image_files.extend(Path(input_dir).glob(f"*{ext.upper()}"))
    
    if not image_files:
        print("✗ 未找到图片文件 (No image files found)")
        sys.exit(1)
    
    print(f"找到 {len(image_files)} 张图片 (Found {len(image_files)} images)")
    print()
    
    # 批量处理
    success = 0
    failed = 0
    
    for i, image_file in enumerate(image_files, 1):
        input_path = str(image_file)
        output_path = get_output_path(input_path, output_dir)
        
        if args.verbose:
            print(f"[{i}/{len(image_files)}] 处理 (Processing): {image_file.name}")
        
        if process_image(input_path, output_path):
            success += 1
            if args.verbose:
                print(f"  ✓ 完成 (Done)")
        else:
            failed += 1
            if args.verbose:
                print(f"  ✗ 失败 (Failed)")
    
    print()
    print("=" * 50)
    print(f"处理完成! (Processing completed!)")
    print(f"  成功 (Success): {success}")
    print(f"  失败 (Failed): {failed}")
    print(f"  输出 (Output): {output_dir}")
    print("=" * 50)


if __name__ == "__main__":
    main()
