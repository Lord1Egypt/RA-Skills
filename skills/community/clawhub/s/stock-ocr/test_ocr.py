#!/usr/bin/env python3
"""测试OCR.space API"""
import requests
import sys
import os

def compress_and_ocr(image_path):
    from PIL import Image
    import io
    
    # 打开图片
    img = Image.open(image_path)
    
    # 转换为RGB
    if img.mode == 'RGBA':
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # 缩小尺寸
    max_dim = 1200
    if max(img.size) > max_dim:
        ratio = max_dim / max(img.size[0], img.size[1])
        new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
        img = img.resize(new_size, Image.LANCZOS)
        print(f"缩放到: {new_size}")
    
    # 压缩
    quality = 60
    output = io.BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    img_data = output.getvalue()
    
    print(f"图片大小: {len(img_data)/1024:.1f}KB")
    
    # 发送OCR请求
    files = {'file': ('image.jpg', img_data, 'image/jpeg')}
    data = {
        'apikey': 'K82897662288957',
        'language': 'chs',
        'isOverlayRequired': 'false'
    }
    
    print("正在OCR识别...")
    response = requests.post(
        'https://api.ocr.space/parse/image',
        files=files,
        data=data,
        timeout=60
    )
    
    result = response.json()
    print(f"响应: {result}")
    
    if result.get('OCRExitCode') == 1:
        text = result['ParsedResults'][0]['ParsedText']
        return text
    else:
        print(f"错误: {result}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python test_ocr.py <image_path>")
        sys.exit(1)
    
    text = compress_and_ocr(sys.argv[1])
    if text:
        print("\n识别结果:")
        print("-" * 40)
        print(text)
