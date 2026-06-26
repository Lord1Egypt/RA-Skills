#!/usr/bin/env python3
"""
白板手绘动画 - 环境准备脚本
功能：
  1. 在 skill 目录下创建 Python 虚拟环境（如已存在则跳过）
  2. 检测所需依赖是否已安装
  3. 自动安装缺失的依赖
  4. 输出虚拟环境的 Python 可执行文件路径（供后续脚本使用）

用法：
  python setup_env.py          # 准备环境并输出 python 路径
  python setup_env.py --check  # 仅检测，不安装
"""
import os
import sys
import subprocess
import venv
from pathlib import Path

# skill 根目录 = 本脚本的上级目录
SKILL_DIR = Path(__file__).resolve().parent.parent
VENV_DIR = SKILL_DIR / ".venv"

REQUIRED_PACKAGES = {
    "cv2": "opencv-python",
    "numpy": "numpy",
    "av": "av",
}


def get_venv_python():
    """返回虚拟环境中的 python 路径"""
    if sys.platform == "win32":
        return str(VENV_DIR / "Scripts" / "python.exe")
    return str(VENV_DIR / "bin" / "python")


def create_venv():
    """创建虚拟环境（如果不存在）"""
    if VENV_DIR.exists():
        python_path = get_venv_python()
        if os.path.exists(python_path):
            print(f"[OK] 虚拟环境已存在: {VENV_DIR}")
            return
    print(f"[..] 创建虚拟环境: {VENV_DIR}")
    venv.create(str(VENV_DIR), with_pip=True)
    print(f"[OK] 虚拟环境创建完成")


def check_package(python_path, import_name):
    """检测某个包是否可在虚拟环境中导入"""
    result = subprocess.run(
        [python_path, "-c", f"import {import_name}"],
        capture_output=True,
    )
    return result.returncode == 0


def install_packages(python_path, packages):
    """在虚拟环境中安装指定包"""
    if not packages:
        return True
    print(f"[..] 安装依赖: {', '.join(packages)}")
    result = subprocess.run(
        [python_path, "-m", "pip", "install", "--quiet"] + packages,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"[错误] 安装失败:\n{result.stderr}")
        return False
    print(f"[OK] 依赖安装完成")
    return True


def main():
    check_only = "--check" in sys.argv

    # 1. 创建虚拟环境
    if not check_only:
        create_venv()
    elif not VENV_DIR.exists():
        print(f"[错误] 虚拟环境不存在: {VENV_DIR}")
        sys.exit(1)

    python_path = get_venv_python()

    # 2. 检测依赖
    missing = []
    for import_name, pip_name in REQUIRED_PACKAGES.items():
        if check_package(python_path, import_name):
            print(f"[OK] {pip_name}")
        else:
            print(f"[缺失] {pip_name}")
            missing.append(pip_name)

    # 3. 安装缺失依赖
    if missing:
        if check_only:
            print(f"\n缺失 {len(missing)} 个依赖: {', '.join(missing)}")
            sys.exit(1)
        if not install_packages(python_path, missing):
            sys.exit(1)

    # 4. 输出 python 路径（最后一行，供调用方捕获）
    print(f"\nPYTHON_PATH={python_path}")


if __name__ == "__main__":
    main()
