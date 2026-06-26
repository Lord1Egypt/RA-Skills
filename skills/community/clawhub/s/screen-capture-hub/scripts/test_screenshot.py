#!/usr/bin/env python3
"""
测试屏幕截图功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_basic_capture():
    """测试基本截图功能"""
    print("测试基本截图功能...")
    try:
        # 尝试导入所需的库
        from PIL import ImageGrab
        import pyautogui
        
        print("成功：依赖库导入成功")
        
        # 获取屏幕信息
        screen_width, screen_height = pyautogui.size()
        print(f"成功：屏幕分辨率：{screen_width}x{screen_height}")
        
        # 测试截图
        print("正在测试截图...")
        screenshot = ImageGrab.grab()
        
        if screenshot:
            print(f"成功：截图成功，尺寸：{screenshot.size[0]}x{screenshot.size[1]}")
            return True
        else:
            print("失败：截图失败")
            return False
            
    except ImportError as e:
        print(f"错误：导入错误：{e}")
        print("请安装依赖：pip install pillow pyautogui")
        return False
    except Exception as e:
        print(f"错误：测试失败：{e}")
        return False

def test_ocr_capability():
    """测试OCR功能"""
    print("\n测试OCR功能...")
    try:
        import pytesseract
        print("✓ pytesseract 导入成功")
        
        # 获取可用语言
        try:
            langs = pytesseract.get_languages(config='')
            print(f"✓ 可用OCR语言：{', '.join(langs[:5])}...")
            return True
        except:
            print("⚠ 无法获取语言列表，但pytesseract可用")
            return True
            
    except ImportError:
        print("警告：pytesseract 未安装，OCR功能不可用")
        print("  安装：pip install pytesseract")
        print("  还需要安装Tesseract OCR引擎")
        return False
    except Exception as e:
        print(f"失败：OCR测试失败：{e}")
        return False

def test_opencv_capability():
    """测试OpenCV功能"""
    print("\n测试OpenCV功能...")
    try:
        import cv2
        import numpy as np
        
        print(f"✓ OpenCV版本：{cv2.__version__}")
        print(f"✓ NumPy版本：{np.__version__}")
        
        # 创建一个测试图像
        test_img = np.zeros((100, 100, 3), dtype=np.uint8)
        test_img[25:75, 25:75] = [255, 0, 0]  # 红色方块
        
        # 测试边缘检测
        gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        print(f"✓ OpenCV功能测试通过")
        return True
        
    except ImportError as e:
        print(f"失败：导入错误：{e}")
        print("请安装依赖：pip install opencv-python numpy")
        return False
    except Exception as e:
        print(f"失败：OpenCV测试失败：{e}")
        return False

def main():
    """运行所有测试"""
    print("=" * 50)
    print("屏幕截图技能测试")
    print("=" * 50)
    
    results = []
    
    # 运行测试
    results.append(("基本截图", test_basic_capture()))
    results.append(("OCR功能", test_ocr_capability()))
    results.append(("OpenCV功能", test_opencv_capability()))
    
    # 显示测试结果
    print("\n" + "=" * 50)
    print("测试结果汇总：")
    print("=" * 50)
    
    all_passed = True
    for test_name, passed in results:
        status = "[通过]" if passed else "[失败]"
        print(f"{test_name:20} {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("[成功] 所有测试通过！技能可以使用。")
        print("\n可用命令：")
        print("  1. python screenshot.py --output my_screenshot.png")
        print("  2. python ocr_screenshot.py --text-output text.txt")
        print("  3. python analyze_screen.py --task screen_info")
    else:
        print("[警告] 部分测试失败，请安装缺失的依赖。")
        print("\n安装所有依赖：")
        print("  pip install pillow pyautogui pytesseract opencv-python numpy")
        print("\n注意：pytesseract还需要安装Tesseract OCR引擎")
        print("Windows: 从 https://github.com/UB-Mannheim/tesseract/wiki 下载安装")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())