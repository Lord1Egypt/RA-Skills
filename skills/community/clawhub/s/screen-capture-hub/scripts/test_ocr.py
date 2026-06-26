#!/usr/bin/env python3
"""
OCR功能测试脚本
测试Tesseract OCR安装和配置
"""

import sys
import os
from pathlib import Path

def test_pytesseract_import():
    """测试pytesseract导入"""
    print("=" * 60)
    print("OCR功能测试")
    print("=" * 60)
    
    print("\n1. 测试pytesseract导入...")
    try:
        import pytesseract
        print("[成功] pytesseract导入成功")
        return pytesseract
    except ImportError as e:
        print(f"[失败] 导入错误: {e}")
        print("\n请安装pytesseract:")
        print("  pip install pytesseract")
        return None

def test_tesseract_path(pytesseract):
    """测试Tesseract路径"""
    print("\n2. 测试Tesseract路径...")
    
    # 常见Tesseract路径
    common_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files\Tesseract\tesseract.exe",
        # 环境变量中的路径
        "tesseract"
    ]
    
    tesseract_found = False
    for path in common_paths:
        try:
            # 如果是相对路径或环境变量路径
            if path == "tesseract":
                result = os.system(f"{path} --version >nul 2>nul")
                if result == 0:
                    print(f"[成功] Tesseract在环境变量中可用")
                    tesseract_found = True
                    break
            else:
                if os.path.exists(path):
                    print(f"[成功] 找到Tesseract: {path}")
                    pytesseract.pytesseract.tesseract_cmd = path
                    tesseract_found = True
                    break
        except:
            continue
    
    if not tesseract_found:
        print("[失败] 未找到Tesseract")
        print("\n请检查:")
        print("1. 是否已安装Tesseract OCR")
        print("2. 是否在环境变量PATH中")
        print("3. 或者手动设置路径:")
        print('   pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"')
        return False
    
    return True

def test_tesseract_version(pytesseract):
    """测试Tesseract版本"""
    print("\n3. 测试Tesseract版本...")
    
    try:
        version = pytesseract.get_tesseract_version()
        print(f"[成功] Tesseract版本: {version}")
        return True
    except Exception as e:
        print(f"[失败] 获取版本失败: {e}")
        return False

def test_available_languages(pytesseract):
    """测试可用语言"""
    print("\n4. 测试可用语言...")
    
    try:
        langs = pytesseract.get_languages(config='')
        print(f"[成功] 发现 {len(langs)} 种语言")
        
        # 显示语言
        if langs:
            print("支持的语言:")
            for lang in sorted(langs):
                print(f"  - {lang}")
            
            # 检查中文支持
            if 'chi_sim' in langs:
                print("[成功] 支持简体中文 (chi_sim)")
            else:
                print("[警告] 不支持简体中文，请下载语言包")
                
            if 'eng' in langs:
                print("[成功] 支持英文 (eng)")
            else:
                print("[警告] 不支持英文")
        else:
            print("[警告] 未发现语言包")
            
        return True
    except Exception as e:
        print(f"[失败] 获取语言失败: {e}")
        return False

def create_test_image():
    """创建测试图像"""
    print("\n5. 创建测试图像...")
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # 创建测试图像
        width, height = 400, 200
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        # 添加文字
        text = "Hello World\n中文测试\nOCR Test"
        
        # 使用默认字体
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        # 计算文字位置
        bbox = draw.multiline_textbbox((0, 0), text, font=font)
        text_x = (width - (bbox[2] - bbox[0])) // 2
        text_y = (height - (bbox[3] - bbox[1])) // 2
        
        # 绘制文字
        draw.multiline_text((text_x, text_y), text, font=font, fill='black', align='center')
        
        # 保存图像
        test_image_path = "ocr_test_image.png"
        image.save(test_image_path)
        print(f"[成功] 测试图像已创建: {test_image_path}")
        return test_image_path
        
    except ImportError as e:
        print(f"[失败] PIL导入错误: {e}")
        print("请安装Pillow: pip install pillow")
        return None
    except Exception as e:
        print(f"[失败] 创建图像失败: {e}")
        return None

def run_ocr_test(pytesseract, image_path):
    """运行OCR测试"""
    print("\n6. 运行OCR测试...")
    
    if not image_path or not os.path.exists(image_path):
        print("[失败] 测试图像不存在")
        return False
    
    try:
        from PIL import Image
        
        # 加载图像
        image = Image.open(image_path)
        
        print("测试英文识别...")
        text_eng = pytesseract.image_to_string(image, lang='eng')
        if text_eng.strip():
            print("[成功] 英文识别结果:")
            print("-" * 40)
            print(text_eng.strip())
            print("-" * 40)
        else:
            print("[失败] 英文识别无结果")
        
        # 测试中文识别
        try:
            print("\n测试中文识别...")
            text_chi = pytesseract.image_to_string(image, lang='chi_sim')
            if text_chi.strip():
                print("[成功] 中文识别结果:")
                print("-" * 40)
                print(text_chi.strip())
                print("-" * 40)
            else:
                print("[警告] 中文识别无结果，可能未安装中文语言包")
        except:
            print("[警告] 中文识别失败，请检查中文语言包")
        
        # 测试中英文混合
        try:
            print("\n测试中英文混合识别...")
            text_mixed = pytesseract.image_to_string(image, lang='eng+chi_sim')
            if text_mixed.strip():
                print("[成功] 混合识别结果:")
                print("-" * 40)
                print(text_mixed.strip())
                print("-" * 40)
            else:
                print("[警告] 混合识别无结果")
        except:
            print("[警告] 混合识别失败")
        
        return True
        
    except Exception as e:
        print(f"[失败] OCR测试失败: {e}")
        return False

def main():
    """主函数"""
    # 测试导入
    pytesseract = test_pytesseract_import()
    if not pytesseract:
        return False
    
    # 测试路径
    if not test_tesseract_path(pytesseract):
        return False
    
    # 测试版本
    if not test_tesseract_version(pytesseract):
        return False
    
    # 测试语言
    if not test_available_languages(pytesseract):
        return False
    
    # 创建测试图像
    image_path = create_test_image()
    
    # 运行OCR测试
    if image_path:
        run_ocr_test(pytesseract, image_path)
    
    print("\n" + "=" * 60)
    print("OCR测试完成")
    print("=" * 60)
    
    print("\n总结:")
    print("✓ pytesseract库已安装")
    print("✓ Tesseract OCR已配置")
    print("✓ 语言包已检查")
    print("✓ OCR功能测试完成")
    
    print("\n下一步:")
    print("1. 使用OCR功能: python scripts/ocr_screenshot.py")
    print("2. 查看详细文档: docs/OCR_SETUP_GUIDE.md")
    print("3. 获取帮助: python scripts/ocr_screenshot.py --help")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n[信息] 用户中断测试")
        sys.exit(1)