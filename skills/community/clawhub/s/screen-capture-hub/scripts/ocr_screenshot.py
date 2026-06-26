#!/usr/bin/env python3
"""
屏幕截图OCR工具
捕获屏幕并识别文字
"""

import argparse
import sys
import os
from datetime import datetime

def check_dependencies():
    """检查并安装必要的依赖"""
    missing_deps = []
    
    # 检查基础依赖
    try:
        from PIL import ImageGrab, Image
    except ImportError:
        missing_deps.append("pillow (图像处理库)")
        print("[提示] 缺少依赖: Pillow - 用于屏幕截图")
        print("      安装命令: pip install pillow")
    
    try:
        import pyautogui
    except ImportError:
        missing_deps.append("pyautogui (屏幕自动化库)")
        print("[提示] 缺少依赖: PyAutoGUI - 用于获取屏幕信息")
        print("      安装命令: pip install pyautogui")
    
    # 检查OCR依赖
    try:
        import pytesseract
    except ImportError:
        missing_deps.append("pytesseract (OCR文字识别库)")
        print("[提示] 缺少依赖: pytesseract - 用于文字识别")
        print("      安装命令: pip install pytesseract")
    
    if missing_deps:
        print("\n[重要] 以下依赖需要安装才能使用OCR功能:")
        for dep in missing_deps:
            print(f"  • {dep}")
        
        print("\n[安装建议]")
        print("1. 安装所有Python依赖:")
        print("   pip install pillow pyautogui pytesseract")
        
        print("\n2. 安装Tesseract OCR引擎:")
        print("   Windows: 从 https://github.com/UB-Mannheim/tesseract/wiki 下载")
        print("   macOS: brew install tesseract")
        print("   Linux: sudo apt-get install tesseract-ocr")
        
        print("\n3. 或使用一键安装脚本:")
        print("   python scripts/setup.py")
        
        return False
    
    return True

# 检查依赖
if not check_dependencies():
    print("\n[提示] 依赖检查完成，部分功能可能不可用")
    print("      如果要使用全部功能，请先安装缺少的依赖")
    print("      继续运行可能会出错...")
    
    # 询问用户是否继续
    response = input("\n要继续运行吗? (y/n): ").lower().strip()
    if response not in ['y', 'yes', '是']:
        print("[信息] 用户选择退出")
        sys.exit(0)
    print("[信息] 继续运行，部分功能可能不可用")

def check_tesseract():
    """检查Tesseract OCR是否可用"""
    try:
        import pytesseract
        # 测试是否可以导入
        return True
    except ImportError:
        print("错误：未找到pytesseract。请安装：pip install pytesseract")
        return False
    except Exception as e:
        print(f"Tesseract检查失败：{e}")
        return False

def capture_and_ocr(output_image=None, output_text=None, region=None, lang='eng+chi_sim'):
    """捕获屏幕并识别文字"""
    try:
        import pytesseract
        
        # 设置输出路径
        if output_image is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_image = f"screenshot_ocr_{timestamp}.png"
            
        if output_text is None:
            base_name = os.path.splitext(output_image)[0]
            output_text = f"{base_name}.txt"
        
        # 捕获屏幕
        if region:
            coords = region.split(',')
            if len(coords) != 4:
                print("区域格式错误，应为 'x1,y1,x2,y2'")
                return False
            x1, y1, x2, y2 = map(int, coords)
            bbox = (x1, y1, x2, y2)
            screenshot = ImageGrab.grab(bbox=bbox)
            print(f"捕获区域：{bbox}")
        else:
            screenshot = ImageGrab.grab()
            screen_width, screen_height = pyautogui.size()
            print(f"捕获全屏：{screen_width}x{screen_height}")
        
        # 保存截图
        screenshot.save(output_image)
        print(f"截图已保存：{output_image}")
        
        # 图像预处理（提高OCR准确性）
        # 转换为灰度图
        gray = screenshot.convert('L')
        
        # 可选：二值化处理
        # threshold = 150
        # binary = gray.point(lambda x: 0 if x < threshold else 255, '1')
        
        # 使用处理后的图像进行OCR
        print(f"正在识别文字（语言：{lang}）...")
        text = pytesseract.image_to_string(gray, lang=lang)
        
        # 保存文字结果
        with open(output_text, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"文字已保存：{output_text}")
        
        # 显示统计信息
        word_count = len(text.split())
        char_count = len(text)
        line_count = len(text.split('\n'))
        
        print(f"\n识别结果统计：")
        print(f"  行数：{line_count}")
        print(f"  单词数：{word_count}")
        print(f"  字符数：{char_count}")
        
        # 显示前几行文字预览
        lines = text.strip().split('\n')
        print(f"\n文字预览（前5行）：")
        for i, line in enumerate(lines[:5]):
            if line.strip():
                print(f"  {i+1}: {line[:80]}{'...' if len(line) > 80 else ''}")
        
        return True
        
    except Exception as e:
        print(f"OCR处理失败：{e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='屏幕截图OCR工具')
    parser.add_argument('--output-image', '-i', default=None,
                       help='截图输出文件路径')
    parser.add_argument('--text-output', '-t', default=None,
                       help='文字输出文件路径')
    parser.add_argument('--region', '-r', default=None,
                       help='捕获区域，格式：x1,y1,x2,y2')
    parser.add_argument('--lang', '-l', default='eng+chi_sim',
                       help='OCR语言（默认：eng+chi_sim 英文+简体中文）')
    parser.add_argument('--list-langs', action='store_true',
                       help='列出可用的OCR语言')
    
    args = parser.parse_args()
    
    # 检查Tesseract
    if not check_tesseract():
        sys.exit(1)
    
    # 列出可用的语言
    if args.list_langs:
        try:
            import pytesseract
            langs = pytesseract.get_languages(config='')
            print("可用的OCR语言：")
            for lang in sorted(langs):
                print(f"  {lang}")
            print("\n提示：使用 --lang 参数指定语言，如 --lang eng+chi_sim")
        except Exception as e:
            print(f"获取语言列表失败：{e}")
        return
    
    # 执行OCR
    success = capture_and_ocr(
        output_image=args.output_image,
        output_text=args.text_output,
        region=args.region,
        lang=args.lang
    )
    
    if not success:
        print("OCR处理失败")
        sys.exit(1)
    
    print(f"\n完成！")
    if args.output_image and os.path.exists(args.output_image):
        print(f"截图：{os.path.abspath(args.output_image)}")
    if args.text_output and os.path.exists(args.text_output):
        print(f"文字：{os.path.abspath(args.text_output)}")

if __name__ == "__main__":
    main()