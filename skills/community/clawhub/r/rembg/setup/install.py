#!/usr/bin/env python3
"""
rembg 环境初始化脚本
在用户根目录 ~/.venv/rembg 创建虚拟环境并安装依赖
并配置命令行工具（Mac/Linux/Windows）
"""
import os
import sys
import subprocess
import platform

# 项目根目录（Skill 目录）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# 用户根目录下的虚拟环境
VENV_DIR = os.path.expanduser("~/.venv/rembg")


def get_shell_config_file():
    """获取当前系统的 Shell 配置文件"""
    system = platform.system()
    
    if system == "Windows":
        return None  # Windows 不需要
    
    # 检测默认 shell
    shell = os.environ.get("SHELL", "")
    
    if "zsh" in shell:
        return os.path.expanduser("~/.zshrc")
    elif "bash" in shell:
        bash_profile = os.path.expanduser("~/.bash_profile")
        if os.path.exists(bash_profile):
            return bash_profile
        return os.path.expanduser("~/.bashrc")
    else:
        # 默认返回 zsh 配置
        return os.path.expanduser("~/.zshrc")


def add_to_path():
    """配置命令行工具 PATH"""
    system = platform.system()
    venv_bin = os.path.join(VENV_DIR, "bin")
    venv_bin_windows = os.path.join(VENV_DIR, "Scripts")  # Windows 虚拟环境的 Scripts 目录
    
    print()
    print("=" * 50)
    print("配置命令行工具 (Configuring command line tool)...")
    print("=" * 50)
    
    if system == "Windows":
        # Windows: 尝试自动添加到用户环境变量
        try:
            # 使用 setx 命令添加用户环境变量
            current_path = os.environ.get("PATH", "")
            
            # 检查是否已经添加
            if venv_bin_windows in current_path:
                print("✓ 命令行工具已配置 (Command line tool already configured)")
            else:
                # 获取现有 PATH 并添加新的
                new_path = f"{venv_bin_windows};{current_path}"
                
                # 使用 PowerShell 设置环境变量
                ps_cmd = f'[Environment]::SetEnvironmentVariable("PATH", "{new_path}", "User")'
                result = subprocess.run(
                    ["powershell", "-Command", ps_cmd],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    print("✓ 已自动添加到用户 PATH (Added to user PATH)")
                    print("  请重启终端或重启电脑使配置生效")
                    print("  Please restart terminal or computer to apply changes")
                else:
                    raise Exception("setx failed")
        except Exception as e:
            # 如果自动失败，显示手动配置说明
            print()
            print("Windows 系统 (Windows):")
            print(f"  请将以下路径添加到系统环境变量 PATH:")
            print(f"  {venv_bin_windows}")
            print()
            print("  方法1: 按 Win+R，输入 sysdm.cpl -> 高级 -> 环境变量")
            print("  方法2: 运行以下命令（需要管理员权限）:")
            print(f'     setx PATH "{venv_bin_windows};%PATH%"')
            print()
        
    elif system in ("Darwin", "Linux"):
        # Mac/Linux: 自动添加到配置文件
        config_file = get_shell_config_file()
        
        path_line = f'export PATH="{venv_bin}:$PATH" # rembg'
        
        # 检查是否已经添加
        if os.path.exists(config_file):
            with open(config_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            if "rembg" in content and venv_bin in content:
                print(f"✓ 命令行工具已配置 (Command line tool already configured)")
            else:
                with open(config_file, "a", encoding="utf-8") as f:
                    f.write(f"\n# rembg\n{path_line}\n")
                print(f"✓ 已添加到 {config_file}")
                print(f"  请运行: source {config_file}")
                print(f"  或重启终端 (or restart terminal)")
        else:
            # 创建配置文件
            with open(config_file, "w", encoding="utf-8") as f:
                f.write(f"# rembg\n{path_line}\n")
            print(f"✓ 已创建并添加到 {config_file}")
            print(f"  请运行: source {config_file}")
    
    print()
    print("配置完成后，可以使用以下命令:")
    print("After configuration, you can use:")
    print(f"  rembg i <输入图片> <输出图片>")
    print()


def create_venv():
    """创建虚拟环境"""
    system = platform.system()
    
    if os.path.exists(VENV_DIR):
        print(f"✓ 虚拟环境已存在 (Virtual environment exists): {VENV_DIR}")
        return True
    
    print(f"正在创建虚拟环境 (Creating virtual environment): {VENV_DIR}")
    try:
        # Windows 下使用 --copies 避免符号链接问题
        if system == "Windows":
            subprocess.run([sys.executable, "-m", "venv", "--copies", VENV_DIR], check=True)
        else:
            subprocess.run([sys.executable, "-m", "venv", VENV_DIR], check=True)
        print("✓ 虚拟环境创建成功 (Virtual environment created)")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 虚拟环境创建失败 (Virtual environment creation failed): {e}")
        return False


def install_requirements():
    """安装依赖"""
    venv_pip = os.path.join(VENV_DIR, "bin", "pip")
    
    # Windows 使用不同的路径
    if platform.system() == "Windows":
        venv_pip = os.path.join(VENV_DIR, "Scripts", "pip")
    
    requirements = os.path.join(SCRIPT_DIR, "requirements.txt")
    
    if not os.path.exists(requirements):
        print(f"✗ requirements.txt 不存在 (requirements.txt not found): {requirements}")
        return False
    
    print("正在安装依赖 (Installing dependencies)...")
    try:
        subprocess.run([venv_pip, "install", "-r", requirements], check=True)
        print("✓ 依赖安装成功 (Dependencies installed)")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 依赖安装失败 (Dependency installation failed): {e}")
        return False


def main():
    print("=" * 50)
    print("rembg 环境初始化 / Environment Initialization")
    print("=" * 50)
    print(f"项目目录 (Project dir): {PROJECT_ROOT}")
    print(f"虚拟环境 (Virtual env): {VENV_DIR}")
    print()
    
    # 创建虚拟环境
    if not create_venv():
        sys.exit(1)
    
    # 安装依赖
    if not install_requirements():
        sys.exit(1)
    
    # 配置命令行工具
    add_to_path()
    
    print("=" * 50)
    print("✓ 环境初始化完成! (Environment initialized!)")
    print("=" * 50)
    print()
    print("使用方法 (Usage):")
    print("  单张处理 (Single): python3 scripts/remove_bg.py <输入图片>")
    print("  批量处理 (Batch): python3 scripts/batch_remove_bg.py <输入目录>")
    print()
    print("或使用命令行 (Or use command line):")
    print("  rembg i <输入图片> <输出图片>")
    print()


if __name__ == "__main__":
    main()
