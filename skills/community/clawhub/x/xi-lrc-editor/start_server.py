#!/usr/bin/env python3
import os
import sys
import subprocess
import importlib

def install_package(package):
    """安装Python包"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_dependencies():
    """检查并安装依赖"""
    required_packages = [
        "flask",
        "pydub",
        "numpy"
    ]
    
    print("检查依赖中...")
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"{package} 已安装")
        except ImportError:
            print(f"正在安装 {package}...")
            install_package(package)
    
    print("所有依赖安装完成")

if __name__ == "__main__":
    # 设置控制台编码为UTF-8
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    # 检查依赖
    check_dependencies()
    
    # 切换到web目录
    web_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
    os.chdir(web_dir)
    
    # 启动Flask服务
    print("启动LRC歌词创作工具服务...")
    print("访问地址: http://localhost:698")
    print("按 Ctrl+C 停止服务")
    
    subprocess.run([sys.executable, "app.py"])
