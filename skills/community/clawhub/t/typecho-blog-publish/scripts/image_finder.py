#!/usr/bin/env python3
"""
图片搜索和下载模块
从 Unsplash/Pexels 等免费图库搜索并下载与主题相关的图片
"""

import os
import re
import requests
from pathlib import Path
from datetime import datetime

def search_and_download_image(topic, index=0, save_dir="/tmp/blog_images"):
    """
    搜索并下载一张与主题相关的图片
    
    Args:
        topic: 搜索主题
        index: 第几张（用于区分多张图）
        save_dir: 保存目录
    
    Returns:
        本地文件路径，失败返回 None
    """
    # 创建保存目录
    os.makedirs(save_dir, exist_ok=True)
    
    # 方案 1: 使用 Unsplash Source（简单，但可能不稳定）
    # 方案 2: 使用 Lorem Flickr（稳定，免费）
    # 方案 3: 使用 Pexels API（需要 API Key）
    
    # 这里用 Lorem Flickr（无需 API Key）
    keywords = topic.replace(' ', ',')
    image_url = f"https://loremflickr.com/1200/630/{keywords}?random={index}"
    
    # 下载图片
    try:
        print(f"🔍 正在搜索图片：{topic} (第{index+1}张)...")
        print(f"📥 下载链接：{image_url}")
        
        resp = requests.get(image_url, timeout=15)
        resp.raise_for_status()
        
        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"blog_image_{timestamp}_{index}.jpg"
        local_path = os.path.join(save_dir, filename)
        
        # 保存文件
        with open(local_path, 'wb') as f:
            f.write(resp.content)
        
        print(f"✅ 图片下载成功：{local_path}")
        return local_path
        
    except Exception as e:
        print(f"❌ 图片下载失败：{str(e)}")
        return None


def search_unsplash_images(topic, count=3):
    """
    从 Unsplash 搜索多张图片（使用官方 API）
    
    注意：需要 Unsplash API Key
    """
    # 这个函数需要 API Key，暂时用 Lorem Flickr 替代
    print("⚠️  Unsplash 需要 API Key，使用 Lorem Flickr 替代")
    return []


# 测试
if __name__ == "__main__":
    topic = "人工智能"
    path = search_and_download_image(topic, 0)
    if path:
        print(f"测试成功：{path}")
        print(f"文件大小：{os.path.getsize(path)} bytes")
    else:
        print("测试失败")
