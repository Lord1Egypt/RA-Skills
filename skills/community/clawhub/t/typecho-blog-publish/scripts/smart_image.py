#!/usr/bin/env python3
"""
智能配图工具
根据文章标题和内容自动搜索并下载相关主题的图片
"""
import urllib.request
import os
import re
from datetime import datetime

# 主题图片映射表 - 使用稳定的 Unsplash 图片
THEME_IMAGES = {
    # AI/科技类
    'ai': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=600&fit=crop',
    '科技': 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&h=600&fit=crop',
    '技术': 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&h=600&fit=crop',
    '智能': 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800&h=600&fit=crop',
    'AI': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=600&fit=crop',
    
    # 创业/搞钱类
    '创业': 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800&h=600&fit=crop',
    '搞钱': 'https://images.unsplash.com/photo-1579532537598-459ecdaf39cc?w=800&h=600&fit=crop',
    '财富': 'https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=800&h=600&fit=crop',
    '赚钱': 'https://images.unsplash.com/photo-1553721505-5265d8168854?w=800&h=600&fit=crop',
    '副业': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&h=600&fit=crop',
    '自动化': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=600&fit=crop',
    
    # 生活/情感类
    '生活': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&h=600&fit=crop',
    '情感': 'https://images.unsplash.com/photo-1499209974431-276138d71b31?w=800&h=600&fit=crop',
    '心情': 'https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?w=800&h=600&fit=crop',
    
    # 默认图片
    'default': 'https://images.unsplash.com/photo-1557683316-973673baf926?w=800&h=600&fit=crop'
}

def extract_keywords(text):
    """从文本中提取关键词"""
    keywords = []
    # 提取标题、分类、标签中的关键词
    for line in text.split('\n'):
        if line.startswith('title:') or line.startswith('categories:') or line.startswith('tags:'):
            keywords.extend(re.findall(r'[\u4e00-\u9fa5a-zA-Z]+', line))
    return keywords

def find_matching_image(title, content):
    """根据标题和内容匹配最相关的图片"""
    text = (title + ' ' + content).lower()
    keywords = extract_keywords(title + '\n' + content)
    
    best_match = 'default'
    best_score = 0
    
    for theme, url in THEME_IMAGES.items():
        score = 0
        # 检查主题词是否出现
        if theme in text:
            score += 10
        # 检查相关关键词
        for keyword in keywords:
            if keyword.lower() in theme or theme in keyword.lower():
                score += 5
        
        if score > best_score:
            best_score = score
            best_match = theme
    
    return THEME_IMAGES.get(best_match, THEME_IMAGES['default']), best_match

def download_image(url, save_path):
    """下载图片"""
    try:
        print(f"📥 正在下载：{url}")
        urllib.request.urlretrieve(url, save_path)
        if os.path.exists(save_path) and os.path.getsize(save_path) > 0:
            print(f"✅ 下载成功：{save_path} ({os.path.getsize(save_path)} 字节)")
            return True
        return False
    except Exception as e:
        print(f"❌ 下载失败：{e}")
        return False

def get_theme_image(theme):
    """根据主题获取图片 URL"""
    return THEME_IMAGES.get(theme, THEME_IMAGES['default'])

if __name__ == "__main__":
    # 测试
    title = "2026 年 AI 搞钱实战指南"
    content = "AI 创业 技术 搞钱 副业"
    
    url, theme = find_matching_image(title, content)
    print(f"\n🎯 匹配结果:")
    print(f"   主题：{theme}")
    print(f"   图片：{url}")
    
    # 下载测试
    test_path = "/tmp/theme_test.jpg"
    download_image(url, test_path)
