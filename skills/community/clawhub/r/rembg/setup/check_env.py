#!/usr/bin/env python3
"""
rembg 环境检查脚本
验证 ~/.venv/rembg 虚拟环境和 rembg 是否就绪
"""
import os
import sys
import subprocess

VENV_DIR = os.path.expanduser("~/.venv/rembg")


def check_venv():
    """检查虚拟环境"""
    if not os.path.exists(VENV_DIR):
        print("✗ 虚拟环境不存在 (Virtual environment not found)")
        print(f"  请先运行 (Please run): python3 setup/install.py")
        return False
    
    venv_python = os.path.join(VENV_DIR, "bin", "python")
    if not os.path.exists(venv_python):
        print("✗ 虚拟环境损坏 (Virtual environment corrupted)")
        return False
    
    print(f"✓ 虚拟环境存在 (Virtual environment exists): {VENV_DIR}")
    return True


def check_rembg():
    """检查 rembg 是否安装"""
    venv_python = os.path.join(VENV_DIR, "bin", "python")
    
    try:
        result = subprocess.run(
            [venv_python, "-c", "import rembg; print(rembg.__version__)"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ rembg 已安装 (rembg installed): {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError:
        print("✗ rembg 未安装 (rembg not installed)")
        print(f"  请先运行 (Please run): python3 setup/install.py")
        return False


def check_models():
    """检查模型是否已下载"""
    venv_python = os.path.join(VENV_DIR, "bin", "python")
    
    # 尝试检查 u2net 模型
    try:
        result = subprocess.run(
            [venv_python, "-c", 
             "from rembg import new_session; s = new_session('u2net'); print('OK')"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print("✓ AI 模型已下载 (AI model downloaded)")
            return True
    except:
        pass
    
    print("⚠ AI 模型未下载 (AI model not downloaded)")
    print("  首次运行时会自动下载（约 176MB）")
    print("  (Will be downloaded on first run, ~176MB)")
    return True


def main():
    print("=" * 50)
    print("rembg 环境检查 / Environment Check")
    print("=" * 50)
    print()
    print(f"虚拟环境 (Virtual env): {VENV_DIR}")
    print()
    
    checks = [
        ("虚拟环境 (Virtual environment)", check_venv),
        ("rembg", check_rembg),
        ("AI 模型 (AI model)", check_models),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"检查 (Checking) {name}...")
        results.append(check_func())
        print()
    
    print("=" * 50)
    if all(results):
        print("✓ 环境就绪，可以正常使用! (Environment ready!)")
        print()
        print("使用方法 (Usage):")
        print("  python3 scripts/remove_bg.py <输入图片>")
        print("  python3 scripts/batch_remove_bg.py <输入目录>")
    else:
        print("✗ 环境未就绪，请运行 (Environment not ready, please run):")
        print("  python3 setup/install.py")
    print("=" * 50)
    
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
