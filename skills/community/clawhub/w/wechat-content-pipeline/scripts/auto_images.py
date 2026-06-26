#!/usr/bin/env python3
"""
自动配图脚本 v1.1
功能：
1. 读取每篇文章内容
2. 根据关键词搜索免费图库
3. 自动下载图片到文章目录
4. 在正文中插入图片引用
5. 确保每篇文章≥5张配图
"""

import os
import sys
import json
import re
import time
import hashlib
import requests
from pathlib import Path

# 文章目录
ARTICLES_DIR = Path(__file__).parent.parent / "articles"

# 免费图库（可用的）
FREE_IMAGE_SOURCES = [
    "https://picsum.photos/800/600",      # Picsum免费图库
    "https://picsum.photos/800/400",      # 横向
    "https://picsum.photos/600/800",      # 纵向
]

# 每篇文章最少配图数量
MIN_IMAGES_PER_ARTICLE = 5

def get_article_keywords(article_path):
    """从文章中提取关键词"""
    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取标题作为主要关键词
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else ""
    
    # 提取小标题作为次要关键词
    headers = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
    
    # 提取技术术语作为关键词
    tech_terms = re.findall(r'\b(Python|深度学习|神经网络|CNN|RNN|Transformer|PyTorch|TensorFlow|AI|机器学习|数据|模型|训练)\b', content)
    
    keywords = [title] + headers[:3] + list(set(tech_terms))[:5]
    return [k for k in keywords if k], content

def generate_image_url(keyword, index):
    """生成图片URL（使用Picsum）"""
    # 使用关键词的hash生成不同的随机种子
    seed_str = f"{keyword}_{index}"
    seed = int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16) % 1000
    
    # 随机选择横向或纵向
    if index % 3 == 0:
        width, height = 800, 600
    elif index % 3 == 1:
        width, height = 800, 400
    else:
        width, height = 600, 800
    
    return f"https://picsum.photos/seed/{seed}/{width}/{height}"

def download_image(url, save_path):
    """下载图片"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
        if response.status_code == 200 and len(response.content) > 10000:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"  下载失败: {e}")
    return False

def insert_images_to_article(article_path, images_info):
    """将图片插入文章内容"""
    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 构建图片引用
    image_refs = []
    for i, img in enumerate(images_info, 1):
        keyword_short = img["keyword"][:30] if len(img["keyword"]) > 30 else img["keyword"]
        ref = f'\n![{keyword_short}](images/{img["filename"]})\n'
        image_refs.append(ref)
    
    # 在段落之间插入图片（每隔2-3个段落插入一张）
    paragraphs = content.split('\n\n')
    new_content = []
    img_idx = 0
    inserted_count = 0
    
    for i, para in enumerate(paragraphs):
        new_content.append(para)
        # 每隔2个段落插入一张图片
        if (i + 1) % 2 == 0 and img_idx < len(image_refs):
            new_content.append(image_refs[img_idx])
            img_idx += 1
            inserted_count += 1
    
    # 如果图片数量不足，在结尾添加剩余图片
    while img_idx < len(image_refs):
        new_content.append(image_refs[img_idx])
        img_idx += 1
        inserted_count += 1
    
    # 添加AI生成标识（如果没有的话）
    if '本文由AI辅助创作' not in content:
        new_content.append('\n\n---\n**本文由AI辅助创作**\n**作者：TJMtaotao**\n**发表于：MEITUSTYLE**\n')
    
    return '\n\n'.join(new_content), inserted_count

def process_article(article_dir):
    """处理单篇文章"""
    article_path = article_dir / "正文.md"
    images_dir = article_dir / "images"
    
    if not article_path.exists():
        print(f"  ⚠️ 文章不存在: {article_path}")
        return False
    
    # 确保图片目录存在
    images_dir.mkdir(exist_ok=True)
    
    print(f"\n  📄 处理文章: {article_dir.name}")
    
    # 提取关键词
    keywords, content = get_article_keywords(article_path)
    print(f"  🔍 关键词: {', '.join(keywords[:5])}")
    
    # 计算需要下载的图片数量
    existing_images = list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.png")) + list(images_dir.glob("*.jpeg"))
    needed_images = max(0, MIN_IMAGES_PER_ARTICLE - len(existing_images))
    
    print(f"  📊 已有图片: {len(existing_images)}, 需要下载: {needed_images}")
    
    if needed_images == 0:
        print(f"  ✅ 已满足配图要求")
        return True
    
    # 下载图片
    downloaded = []
    for i in range(needed_images):
        # 使用关键词和索引生成不同的图片URL
        keyword = keywords[i % len(keywords)] if keywords else "ai"
        url = generate_image_url(keyword, i)
        
        filename = f"image_{i+1:03d}.jpg"
        save_path = images_dir / filename
        
        print(f"  📥 下载图片 {i+1}/{needed_images}: {keyword[:20]}...")
        
        if download_image(url, save_path):
            print(f"  ✅ 成功: {filename}")
            downloaded.append({
                "keyword": keyword,
                "filename": filename,
                "source": "picsum"
            })
            time.sleep(0.3)  # 避免请求过快
        else:
            print(f"  ⚠️ 下载失败，使用替代URL...")
            # 尝试不带seed的URL
            alt_url = FREE_IMAGE_SOURCES[i % len(FREE_IMAGE_SOURCES)]
            if download_image(alt_url, save_path):
                downloaded.append({
                    "keyword": keyword,
                    "filename": filename,
                    "source": "picsum"
                })
                print(f"  ✅ 替代成功: {filename}")
    
    # 更新文章内容
    if downloaded:
        updated_content, inserted = insert_images_to_article(article_path, downloaded)
        with open(article_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"  ✅ 文章已更新，插入 {inserted} 张图片")
    else:
        print(f"  ⚠️ 未能下载到图片")
    
    return len(downloaded) > 0

def main():
    """主流程"""
    print("=" * 60)
    print("🚀 公众号文章自动配图工具 v1.1")
    print("=" * 60)
    
    if not ARTICLES_DIR.exists():
        print(f"❌ 文章目录不存在: {ARTICLES_DIR}")
        return
    
    # 获取所有文章目录
    article_dirs = sorted([d for d in ARTICLES_DIR.iterdir() if d.is_dir()])
    
    print(f"\n📁 发现 {len(article_dirs)} 篇文章")
    print(f"📋 每篇文章最少配图: {MIN_IMAGES_PER_ARTICLE} 张")
    
    success_count = 0
    total_images = 0
    
    for article_dir in article_dirs:
        try:
            if process_article(article_dir):
                success_count += 1
                # 统计图片数量
                images_dir = article_dir / "images"
                img_count = len(list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.png")) + list(images_dir.glob("*.jpeg")))
                total_images += img_count
        except Exception as e:
            print(f"  ❌ 处理失败: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 完成！成功处理 {success_count}/{len(article_dirs)} 篇文章")
    print(f"📸 共下载图片: {total_images} 张")
    print("=" * 60)

if __name__ == "__main__":
    main()