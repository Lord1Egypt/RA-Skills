#!/usr/bin/env python3
"""压缩图片"""
import sys
import os

try:
    from PIL import Image
except ImportError:
    print("请安装Pillow: pip install Pillow")
    sys.exit(1)

def compress_image(input_path: str, output_path: str = None, max_size_kb: int = 1024) -> str:
    """压缩图片到指定大小"""
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_compressed{ext}"
    
    img = Image.open(input_path)
    
    # 如果是RGBA，转换为RGB
    if img.mode == 'RGBA':
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    
    # 计算缩放比例
    quality = 85
    while quality > 10:
        img.save(output_path, 'JPEG', quality=quality, optimize=True)
        size_kb = os.path.getsize(output_path) / 1024
        if size_kb <= max_size_kb:
            break
        quality -= 5
    
    print(f"压缩完成: {os.path.getsize(input_path)/1024:.1f}KB -> {os.path.getsize(output_path)/1024:.1f}KB")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python compress_image.py <image_path>")
        sys.exit(1)
    
    compress_image(sys.argv[1])
