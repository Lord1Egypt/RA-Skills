#!/usr/bin/env python3
"""
Screenshot OCR - 截图文字识别工具
"""
import os
import sys
import argparse
import subprocess

def check_dependencies():
    """检查依赖"""
    try:
        import pytesseract
        from PIL import Image
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("\n请安装:")
        print("  pip install pytesseract pillow")
        print("\n并安装 Tesseract:")
        print("  Ubuntu: sudo apt install tesseract-ocr tesseract-ocr-chi-sim")
        print("  macOS: brew install tesseract")
        return False

def get_clipboard_image():
    """从剪贴板获取图片（Linux/macOS）"""
    try:
        # 尝试使用 xclip (Linux)
        subprocess.run(["xclip", "-selection", "clipboard", "-t", "image/png", "-o", "/tmp/clipboard.png"], 
                      check=True, capture_output=True)
        return "/tmp/clipboard.png"
    except:
        pass
    
    try:
        # 尝试使用 pbpaste (macOS)
        subprocess.run(["pbpaste", ">", "/tmp/clipboard.png"], shell=True, capture_output=True)
        if os.path.exists("/tmp/clipboard.png"):
            return "/tmp/clipboard.png"
    except:
        pass
    
    return None

def recognize_image(image_path, lang='eng+chi_sim'):
    """识别图片文字"""
    try:
        import pytesseract
        from PIL import Image
        
        img = Image.open(image_path)
        
        # 识别
        text = pytesseract.image_to_string(img, lang=lang)
        
        return text.strip()
    except Exception as e:
        return f"❌ 识别失败: {e}"

def copy_to_clipboard(text):
    """复制到剪贴板"""
    try:
        # Linux
        subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode(), check=True)
        print("✅ 已复制到剪贴板")
        return True
    except:
        pass
    
    try:
        # macOS
        subprocess.run(["pbcopy"], input=text.encode(), check=True)
        print("✅ 已复制到剪贴板")
        return True
    except:
        pass
    
    print("⚠️ 无法复制到剪贴板")
    return False

def cmd_clipboard(args):
    """从剪贴板识别"""
    if not check_dependencies():
        return
    
    print("📷 获取剪贴板图片...")
    image_path = get_clipboard_image()
    
    if not image_path or not os.path.exists(image_path):
        print("❌ 剪贴板中没有图片")
        return
    
    print("🔤 识别中...")
    text = recognize_image(image_path)
    
    if text:
        print("\n" + "=" * 50)
        print(text)
        print("=" * 50)
        
        if args.copy:
            copy_to_clipboard(text)
        
        if args.save:
            with open(args.save, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"✅ 已保存到: {args.save}")
    else:
        print("❌ 未识别到文字")

def cmd_file(args):
    """识别图片文件"""
    if not check_dependencies():
        return
    
    image_path = args.image
    
    if not os.path.exists(image_path):
        print(f"❌ 文件不存在: {image_path}")
        return
    
    print(f"🔤 识别 {image_path}...")
    text = recognize_image(image_path)
    
    if text:
        print("\n" + "=" * 50)
        print(text)
        print("=" * 50)
        
        if args.copy:
            copy_to_clipboard(text)
        
        if args.save:
            with open(args.save, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"✅ 已保存到: {args.save}")
    else:
        print("❌ 未识别到文字")

def main():
    parser = argparse.ArgumentParser(description="Screenshot OCR")
    subparsers = parser.add_subparsers()
    
    p_clip = subparsers.add_parser("clipboard", help="识别剪贴板图片")
    p_clip.add_argument("--copy", action="store_true", help="识别后复制到剪贴板")
    p_clip.add_argument("--save", help="保存到文件")
    p_clip.set_defaults(func=cmd_clipboard)
    
    p_file = subparsers.add_parser("file", help="识别图片文件")
    p_file.add_argument("image", help="图片文件路径")
    p_file.add_argument("--copy", action="store_true", help="识别后复制到剪贴板")
    p_file.add_argument("--save", help="保存到文件")
    p_file.set_defaults(func=cmd_file)
    
    args = parser.parse_args()
    
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
