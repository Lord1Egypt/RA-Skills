#!/usr/bin/env python3
"""
图片处理脚本：将图片压缩并转为base64内嵌格式
支持同一图片在多个问题分类下复用
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print(json.dumps({"error": "需要安装 Pillow 库: pip install Pillow"}))
    sys.exit(1)


def compress_image(input_path, max_width=600, quality=70):
    """
    压缩图片并返回base64编码
    
    Args:
        input_path: 图片文件路径
        max_width: 最大宽度（像素），默认600
        quality: JPEG质量(1-100)，默认70
    
    Returns:
        tuple: (base64字符串, 原始宽高比, 文件大小KB)
    """
    try:
        with Image.open(input_path) as img:
            # 转换为RGB（支持RGBA转RGB，PNG转JPEG）
            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            elif img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')
            
            # 计算缩放比例
            original_width, original_height = img.size
            ratio = original_height / original_width if original_width > 0 else 1
            
            # 缩放
            if original_width > max_width:
                new_width = max_width
                new_height = int(max_width * ratio)
                img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # 保存到内存获取base64
            import io
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=quality, optimize=True)
            buffer.seek(0)
            
            b64_data = base64.b64encode(buffer.read()).decode('utf-8')
            
            # 获取压缩后文件大小
            buffer.seek(0, 2)
            file_size = buffer.tell() / 1024
            
            return b64_data, ratio, round(file_size, 1)
            
    except Exception as e:
        raise Exception(f"图片处理失败: {str(e)}")


def process_images(image_dir, output_file, max_width=600, quality=70):
    """
    处理目录下所有图片，生成base64数据供HTML使用
    
    Args:
        image_dir: 图片目录路径
        output_file: 输出JSON文件路径
        max_width: 最大宽度
        quality: 压缩质量
    
    Returns:
        dict: 图片ID到base64数据的映射
    """
    image_map = {}
    image_dir = Path(image_dir)
    
    if not image_dir.exists():
        raise Exception(f"图片目录不存在: {image_dir}")
    
    # 支持的图片格式
    extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    
    # 按文件名排序，确保顺序一致
    image_files = sorted([
        f for f in image_dir.iterdir() 
        if f.is_file() and f.suffix.lower() in extensions
    ])
    
    for idx, img_path in enumerate(image_files, 1):
        try:
            b64_data, ratio, file_size = compress_image(str(img_path), max_width, quality)
            img_id = f"img_{idx}"
            
            image_map[img_id] = {
                "base64": b64_data,
                "filename": img_path.name,
                "ratio": round(ratio, 3),
                "size_kb": file_size,
                "width": max_width
            }
            print(f"已处理: {img_path.name} ({file_size}KB)", file=sys.stderr)
        except Exception as e:
            print(f"跳过 {img_path.name}: {e}", file=sys.stderr)
    
    # 保存到JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(image_map, f, ensure_ascii=False, indent=2)
    
    return image_map


def main():
    parser = argparse.ArgumentParser(description='压缩图片并转为base64')
    parser.add_argument('--image-dir', required=True, help='图片目录路径')
    parser.add_argument('--output', required=True, help='输出JSON文件路径')
    parser.add_argument('--max-width', type=int, default=600, help='最大宽度(像素)，默认600')
    parser.add_argument('--quality', type=int, default=70, help='JPEG质量(1-100)，默认70')
    
    args = parser.parse_args()
    
    try:
        image_map = process_images(args.image_dir, args.output, args.max_width, args.quality)
        
        result = {
            "status": "success",
            "image_count": len(image_map),
            "output_file": args.output,
            "total_size_kb": sum(img["size_kb"] for img in image_map.values())
        }
        print(json.dumps(result, ensure_ascii=False))
        
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
