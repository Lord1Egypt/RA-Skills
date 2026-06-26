#!/usr/bin/env python3
"""
Sum2Slides 安装脚本
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def check_python_version():
    """检查Python版本"""
    
    required_version = (3, 10)
    current_version = sys.version_info[:2]
    
    if current_version < required_version:
        print(f"错误: 需要Python {required_version[0]}.{required_version[1]} 或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    
    print(f"✓ Python版本: {sys.version}")
    return True


def check_dependencies():
    """检查依赖"""
    
    required_packages = [
        'python-pptx',
        'markdown', 
        'pydantic',
        'click',
        'pyyaml',
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package} 已安装")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} 未安装")
    
    return missing_packages


def install_dependencies(missing_packages):
    """安装依赖"""
    
    if not missing_packages:
        print("✓ 所有依赖已安装")
        return True
    
    print(f"\n安装缺失的依赖: {', '.join(missing_packages)}")
    
    try:
        # 使用pip安装
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
        print("✓ 依赖安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 依赖安装失败: {e}")
        return False


def setup_development_environment():
    """设置开发环境"""
    
    dev_packages = [
        'pytest',
        'pytest-cov',
        'flake8',
        'black',
        'mypy',
    ]
    
    print("\n设置开发环境...")
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + dev_packages)
        print("✓ 开发依赖安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 开发依赖安装失败: {e}")
        return False


def create_config_directory():
    """创建配置目录"""
    
    config_dir = Path.home() / '.config' / 'sum2slides'
    
    try:
        config_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ 配置目录创建成功: {config_dir}")
        
        # 复制默认配置文件
        default_config = Path(__file__).parent.parent / 'config' / 'default.yaml'
        if default_config.exists():
            import shutil
            shutil.copy2(default_config, config_dir / 'config.yaml')
            print(f"✓ 默认配置文件已复制")
        
        return True
    except Exception as e:
        print(f"✗ 配置目录创建失败: {e}")
        return False


def install_package():
    """安装包"""
    
    print("\n安装Sum2Slides包...")
    
    try:
        # 使用pip安装当前目录的包
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-e', '.'])
        print("✓ Sum2Slides安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Sum2Slides安装失败: {e}")
        return False


def run_tests():
    """运行测试"""
    
    print("\n运行测试...")
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pytest', 'tests/', '-v'])
        print("✓ 所有测试通过")
        return True
    except subprocess.CalledProcessError:
        print("✗ 测试失败")
        return False


def create_examples():
    """创建示例文件"""
    
    examples_dir = Path(__file__).parent.parent / 'examples'
    
    if examples_dir.exists():
        print(f"✓ 示例目录已存在: {examples_dir}")
        return True
    
    try:
        examples_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ 示例目录创建成功: {examples_dir}")
        return True
    except Exception as e:
        print(f"✗ 示例目录创建失败: {e}")
        return False


def show_usage():
    """显示使用说明"""
    
    print("\n" + "="*60)
    print("Sum2Slides 安装完成！")
    print("="*60)
    
    print("\n使用方法:")
    print("1. 命令行使用:")
    print("   sum2slides convert '你的文本内容' --output presentation.pptx")
    print("   sum2slides convert --input notes.txt --output slides.pptx")
    
    print("\n2. Python API使用:")
    print("   from sum2slides import Sum2Slides")
    print("   converter = Sum2Slides()")
    print("   presentation = converter.convert('你的文本内容')")
    print("   presentation.save('output.pptx')")
    
    print("\n3. 查看帮助:")
    print("   sum2slides --help")
    print("   sum2slides convert --help")
    
    print("\n4. 验证安装:")
    print("   sum2slides validate")
    
    print("\n配置文件位置:")
    print(f"   {Path.home() / '.config' / 'sum2slides' / 'config.yaml'}")
    
    print("\n示例文件位置:")
    print(f"   {Path(__file__).parent.parent / 'examples'}")
    
    print("\n" + "="*60)


def main():
    """主函数"""
    
    print("Sum2Slides v1.0.1 安装程序")
    print("="*40)
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 检查依赖
    missing_packages = check_dependencies()
    
    # 安装依赖
    if missing_packages:
        if not install_dependencies(missing_packages):
            sys.exit(1)
    
    # 安装包
    if not install_package():
        sys.exit(1)
    
    # 创建配置目录
    if not create_config_directory():
        print("警告: 配置目录创建失败，但安装继续...")
    
    # 创建示例文件
    if not create_examples():
        print("警告: 示例目录创建失败，但安装继续...")
    
    # 运行测试
    test_option = input("\n是否运行测试? (y/N): ").lower()
    if test_option == 'y':
        if not run_tests():
            print("警告: 测试失败，但安装继续...")
    
    # 设置开发环境（可选）
    dev_option = input("\n是否设置开发环境? (y/N): ").lower()
    if dev_option == 'y':
        if not setup_development_environment():
            print("警告: 开发环境设置失败，但安装继续...")
    
    # 显示使用说明
    show_usage()
    
    print("\n✓ Sum2Slides v1.0.1 安装完成！")


if __name__ == '__main__':
    main()