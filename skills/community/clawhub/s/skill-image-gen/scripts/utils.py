#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
"""

import base64
import datetime
import io
import os
import random
from PIL import Image
import requests
from typing import Tuple, Optional


def generate_timestamp_filename(extension: str = 'png') -> str:
    """
    生成基于时间戳的文件名
    
    Args:
        extension: 文件扩展名
    
    Returns:
        文件名
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_number = random.randint(1000, 9999)
    return f"{timestamp}_{random_number}.{extension}"


def base64_to_image(base64_string: str, output_path: str) -> str:
    """
    将 Base64 字符串转换为图片并保存
    
    Args:
        base64_string: Base64 编码的图片数据
        output_path: 输出路径
    
    Returns:
        保存的文件路径
    """
    # 确保目录存在
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    
    # 解码
    image_data = base64.b64decode(base64_string)
    
    # 转换为图像
    image = Image.open(io.BytesIO(image_data))
    
    # 保存
    image.save(output_path)
    
    return output_path


def image_to_base64(image_path: str) -> str:
    """
    将图片文件转换为 Base64 字符串
    
    Args:
        image_path: 图片文件路径
    
    Returns:
        Base64 编码的字符串
    """
    with open(image_path, 'rb') as f:
        image_data = f.read()
    return base64.b64encode(image_data).decode('utf-8')


def download_image(url: str, save_path: str, timeout: int = 30) -> Tuple[str, str]:
    """
    从 URL 下载图片
    
    Args:
        url: 图片 URL
        save_path: 保存目录
        timeout: 超时时间 (秒)
    
    Returns:
        (文件名, 完整路径)
    """
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    
    # 转换为 base64 再保存
    b64_str = base64.b64encode(response.content).decode('utf-8')
    
    # 生成文件名
    filename = generate_timestamp_filename()
    full_path = os.path.join(save_path, filename)
    
    # 保存
    base64_to_image(b64_str, full_path)
    
    return filename, full_path


def resize_image(
    input_path: str,
    output_path: str,
    size: Tuple[int, int],
    keep_aspect_ratio: bool = True
) -> str:
    """
    调整图片大小
    
    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径
        size: 目标尺寸 (宽, 高)
        keep_aspect_ratio: 是否保持宽高比
    
    Returns:
        输出路径
    """
    image = Image.open(input_path)
    
    if keep_aspect_ratio:
        image.thumbnail(size, Image.Resampling.LANCZOS)
    else:
        image = image.resize(size, Image.Resampling.LANCZOS)
    
    image.save(output_path)
    return output_path


def convert_format(input_path: str, output_path: str, format: str = 'PNG') -> str:
    """
    转换图片格式
    
    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径
        format: 目标格式 (PNG, JPEG, etc.)
    
    Returns:
        输出路径
    """
    image = Image.open(input_path)
    
    # RGBA 转 RGB (对于 JPEG)
    if format.upper() == 'JPEG' and image.mode == 'RGBA':
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[3])
        image = background
    
    image.save(output_path, format=format)
    return output_path
