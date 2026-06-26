#!/usr/bin/env python3
"""
技能安装和设置脚本
自动安装依赖并配置环境
"""

import sys
import subprocess
import os
from pathlib import Path

def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\n{'='*60}")
    print(f"执行: {description}")
    print(f"{'='*60}")
    print(f"命令: {cmd}")
    
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.stdout:
            print(f"输出: {result.stdout}")
        
        if result.stderr:
            print(f"错误: {result.stderr}")
        
        print(f"返回码: {result.returncode}")
        
        if result.returncode == 0:
            print(f"[成功] {description} 成功")
        else:
            print(f"[失败] {description} 失败")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"[失败] 执行失败: {e}")
        return False

def check_python_version():
    """检查Python版本"""
    print("检查Python版本...")
    
    version = sys.version_info
    print(f"当前Python版本: {sys.version}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("[失败] 需要Python 3.8或更高版本")
        return False
    
    print("[成功] Python版本符合要求")
    return True

def check_pip():
    """检查pip是否可用"""
    print("\n检查pip...")
    
    success = run_command(
        "python -m pip --version",
        "检查pip版本"
    )
    
    if not success:
        print("\n[失败] pip不可用，请先安装pip")
        print("获取pip: https://pip.pypa.io/en/stable/installation/")
        return False
    
    return True

def install_dependencies():
    """安装Python依赖"""
    print("\n安装Python依赖...")
    
    # 基础依赖
    dependencies = [
        ("pillow", "图像处理库"),
        ("pyautogui", "屏幕自动化库"),
    ]
    
    all_success = True
    
    for package, description in dependencies:
        success = run_command(
            f"python -m pip install --user {package}",
            f"安装{description} ({package})"
        )
        if not success:
            all_success = False
    
    # 可选依赖提示
    print("\n" + "="*60)
    print("可选依赖安装:")
    print("如需OCR功能，请安装: python -m pip install --user pytesseract")
    print("如需图像分析功能，请安装: python -m pip install --user opencv-python numpy")
    print("Tesseract OCR引擎需要单独安装")
    print("Windows: https://github.com/UB-Mannheim/tesseract/wiki")
    print("="*60)
    
    return all_success

def create_example_scripts():
    """创建示例脚本"""
    print("\n创建示例脚本...")
    
    example_dir = Path("examples")
    example_dir.mkdir(exist_ok=True)
    
    # 创建简单示例
    example_code = '''#!/usr/bin/env python3
"""
屏幕截图示例
"""

from PIL import ImageGrab
import pyautogui
from datetime import datetime

# 获取屏幕信息
screen_width, screen_height = pyautogui.size()
print(f"屏幕分辨率: {screen_width}x{screen_height}")

# 截图
screenshot = ImageGrab.grab()
print(f"截图尺寸: {screenshot.size[0]}x{screenshot.size[1]}")

# 保存
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"example_screenshot_{timestamp}.png"
screenshot.save(filename)
print(f"截图已保存: {filename}")'''
    
    example_file = example_dir / "simple_capture.py"
    with open(example_file, "w", encoding="utf-8") as f:
        f.write(example_code)
    
    print(f"[成功] 示例脚本已创建: {example_file}")
    return True

def verify_installation():
    """验证安装"""
    print("\n验证安装...")
    
    test_code = '''
try:
    from PIL import ImageGrab
    import pyautogui
    print("[成功] 基础库导入成功")
    
    # 测试屏幕信息
    w, h = pyautogui.size()
    print(f"[成功] 屏幕分辨率: {w}x{h}")
    
    # 测试截图
    img = ImageGrab.grab()
    print(f"[成功] 截图成功: {img.size[0]}x{img.size[1]}")
    
    print("\\n🎉 所有测试通过!")
    
except ImportError as e:
    print(f"[失败] 导入错误: {e}")
    return False
except Exception as e:
    print(f"[失败] 测试失败: {e}")
    return False
'''
    
    # 运行测试代码
    try:
        exec(test_code)
        return True
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("OPENCLAW(龙虾)-屏幕查看器 技能安装程序")
    print("=" * 60)
    
    steps = [
        ("检查Python版本", check_python_version),
        ("检查pip", check_pip),
        ("安装依赖", install_dependencies),
        ("创建示例", create_example_scripts),
        ("验证安装", verify_installation),
    ]
    
    all_success = True
    
    for step_name, step_func in steps:
        print(f"\n步骤: {step_name}")
        print("-" * 40)
        
        if not step_func():
            print(f"[失败] {step_name} 失败")
            all_success = False
            break
    
    print("\n" + "=" * 60)
    
    if all_success:
        print("[成功] 安装完成!")
        print("\n使用方法:")
        print("1. 基本截图: python scripts/quick_capture.py")
        print("2. OCR功能: python scripts/ocr_screenshot.py")
        print("3. 屏幕分析: python scripts/analyze_screen.py")
        print("\n更多信息请查看 README.md")
    else:
        print("[失败] 安装失败，请检查错误信息")
        sys.exit(1)

if __name__ == "__main__":
    m