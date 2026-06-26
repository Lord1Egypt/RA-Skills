"""
图片工具模块
处理图片相关操作
"""

import os
import io
import base64
from typing import Optional, Union
from PIL import Image

def resize_image(image_path: str, max_size: int = 512, output_path: str = None) -> str:
    """
    调整图片大小
    
    Args:
        image_path: 原图路径
        max_size: 最大边长
        output_path: 输出路径（默认覆盖原图）
    
    Returns:
        输出路径
    """
    img = Image.open(image_path)
    
    # 保持比例缩放
    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    
    # 保存
    output = output_path or image_path
    img.save(output, quality=85, optimize=True)
    
    return output

def compress_image(image_path: str, max_kb: int = 50, output_path: str = None) -> str:
    """
    压缩图片到指定大小
    
    Args:
        image_path: 原图路径
        max_kb: 最大文件大小（KB）
        output_path: 输出路径
    
    Returns:
        输出路径
    """
    img = Image.open(image_path)
    
    # 转换为 RGB（处理 PNG 透明通道）
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    
    output = output_path or image_path
    
    # 二分查找最佳质量
    quality = 85
    min_q, max_q = 10, 95
    
    while min_q <= max_q:
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=quality, optimize=True)
        size_kb = buffer.tell() / 1024
        
        if size_kb <= max_kb:
            # 保存结果
            with open(output, 'wb') as f:
                f.write(buffer.getvalue())
            return output
        
        max_q = quality - 1
        quality = (min_q + max_q) // 2
    
    # 无法压缩到目标大小，保存当前结果
    img.save(output, format='JPEG', quality=min_q, optimize=True)
    return output

def image_to_base64(image_path: str) -> str:
    """
    图片转 base64
    
    Args:
        image_path: 图片路径
    
    Returns:
        base64 字符串
    """
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def base64_to_image(base64_str: str, output_path: str) -> str:
    """
    base64 转图片
    
    Args:
        base64_str: base64 字符串
        output_path: 输出路径
    
    Returns:
        输出路径
    """
    img_data = base64.b64decode(base64_str)
    with open(output_path, 'wb') as f:
        f.write(img_data)
    return output_path

def create_placeholder(color: tuple = (200, 200, 200), size: tuple = (512, 512), 
                       output_path: str = None) -> str:
    """
    创建占位图
    
    Args:
        color: 背景色
        size: 尺寸
        output_path: 输出路径
    
    Returns:
        输出路径
    """
    img = Image.new('RGB', size, color)
    
    if not output_path:
        output_path = f"./placeholder_{color[0]}_{color[1]}_{color[2]}.jpg"
    
    img.save(output_path, quality=85)
    return output_path

def get_image_info(image_path: str) -> dict:
    """
    获取图片信息
    
    Args:
        image_path: 图片路径
    
    Returns:
        图片信息字典
    """
    img = Image.open(image_path)
    
    return {
        "format": img.format,
        "mode": img.mode,
        "width": img.width,
        "height": img.height,
        "size_kb": os.path.getsize(image_path) / 1024
    }
