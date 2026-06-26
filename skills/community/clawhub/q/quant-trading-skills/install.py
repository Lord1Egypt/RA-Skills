#!/usr/bin/env python3
import sys
import subprocess
import os

def main():
    # 检查 Python 版本
    if sys.version_info < (3, 11):
        print(f'错误: 需要 Python 3.11 或更高版本，当前版本: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')
        return 1
    
    print('正在安装 Python 依赖...')
    
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    requirements_path = os.path.join(script_dir, 'requirements.txt')
    
    try:
        # 升级 pip
        print('升级 pip...')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        
        # 安装依赖
        print(f'从 {requirements_path} 安装依赖...')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
        
        print('依赖安装成功!')
        return 0
    except subprocess.CalledProcessError as e:
        print(f'错误: 安装依赖失败，退出码: {e.returncode}')
        return 1
    except Exception as e:
        print(f'错误: {str(e)}')
        return 1

if __name__ == '__main__':
    sys.exit(main())
