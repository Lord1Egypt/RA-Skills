#!/usr/bin/env python3
"""
Typecho 博客发布技能 v2.0 - 完整版
完整流程：主题 → 搜索配图 → 生成文案 → 上传图片 → 获取真实 URL → 存草稿 → 验证 → 发布

工作流程：
1. 根据主题搜索网络配图（LoremFlickr）
2. 下载图片到本地
3. 生成 Markdown 文案（包含图片占位符）
4. 上传图片到 Typecho 服务器
5. 替换文案中的图片为真实 URL
6. 发布为草稿（不立即发布）
7. 返回草稿链接供预览检查

使用方法:
    python3 publish_v2.py "AI 改变生活的 5 种方式" "技术" "人工智能，生活，科技"
    # 参数：主题标题，分类，标签（可选）
"""

import os
import sys
import re
import requests
import xmlrpc.client
from datetime import datetime
from pathlib import Path

# 导入原有模块
sys.path.insert(0, os.path.dirname(__file__))
from publish_post import (
    load_env, 
    log_message, 
    markdown_to_html, 
    upload_image_to_typecho,
    process_markdown_images,
    publish_post,
    publish_from_file
)

# 图片搜索模块
from image_finder import search_and_download_image

# ============ 分类匹配功能 ============

def get_existing_categories(config=None):
    """
    获取博客已有分类列表
    
    Returns:
        分类字典 {分类名：分类 ID}
    """
    if config is None:
        config = load_env()
    
    XMLRPC_URL = config.get('BLOG_URL', 'http://yuanblog.tk:9980') + config.get('BLOG_XMLRPC', '/index.php/action/xmlrpc')
    USERNAME = config.get('BLOG_USERNAME', 'admin')
    PASSWORD = config.get('BLOG_PASSWORD', '')
    
    server = xmlrpc.client.ServerProxy(XMLRPC_URL)
    
    try:
        users = server.blogger.getUsersBlogs('', USERNAME, PASSWORD)
        if not users:
            return {}
        
        blog_id = users[0]['blogid']
        categories = server.metaWeblog.getCategories(blog_id, USERNAME, PASSWORD)
        
        # 转换为字典 {分类名：分类 ID}
        cat_dict = {}
        for cat in categories:
            cat_name = cat.get('title', cat.get('categoryName', ''))
            cat_id = cat.get('categoryId', '')
            if cat_name:
                cat_dict[cat_name] = cat_id
        
        return cat_dict
    
    except Exception as e:
        log_message(f"⚠️ 获取分类失败：{e}")
        return {}


def match_category(input_cat, existing_cats):
    """
    将输入分类匹配到已有分类
    
    Args:
        input_cat: 输入的分类名（如"技术"、"AI"）
        existing_cats: 已有分类字典
    
    Returns:
        匹配到的分类名，未匹配到返回原输入
    """
    if not existing_cats:
        return input_cat
    
    # 完全匹配
    if input_cat in existing_cats:
        return input_cat
    
    # 模糊匹配（包含关系）
    input_lower = input_cat.lower()
    for existing in existing_cats.keys():
        if input_lower in existing.lower() or existing.lower() in input_lower:
            return existing
    
    # 返回原输入（发布时会自动创建新分类或归入默认）
    return input_cat


# ============ 核心函数 ============

def generate_markdown_content(topic, categories, tags, image_urls=None, config=None):
    """
    根据主题生成 Markdown 文案
    
    Args:
        topic: 文章主题
        categories: 分类列表
        tags: 标签列表
        image_urls: 配图 URL 列表（可选）
        config: 配置字典（用于获取已有分类）
    
    Returns:
        Markdown 格式的完整文案
    """
    # 生成标题
    title = topic.strip()
    
    # 分类匹配：将输入分类匹配到已有分类
    existing_cats = get_existing_categories(config)
    matched_categories = []
    for cat in categories:
        matched = match_category(cat, existing_cats)
        if matched != cat:
            log_message(f"🔧 分类匹配：'{cat}' → '{matched}'")
        matched_categories.append(matched)
    
    categories = matched_categories
    
    # 生成引言
    intro = f"""# {title}

> **摘要**：本文探讨{topic}的相关内容，带你了解最新趋势和实用技巧。

"""
    
    # 生成正文（模板化结构）
    body = f"""## 引言

{topic}是当下热门话题。本文将从多个角度为你详细解析。

## 核心观点

1. **观点一**：详细内容展开...
2. **观点二**：详细内容展开...
3. **观点三**：详细内容展开...

## 实际应用

在实际生活中，{topic}有着广泛的应用场景：

- 场景一：具体应用案例
- 场景二：具体应用案例
- 场景三：具体应用案例

## 总结

{topic}的重要性不言而喻。希望本文能为你提供一些有价值的参考。

---

*本文标签：{', '.join(tags) if tags else '技术'}*
*发布时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
    
    # 组合完整 Markdown
    categories_str = ', '.join(categories) if categories else '技术'
    tags_str = ', '.join(tags) if tags else '技术'
    
    if image_urls:
        # 有图片时，插入到开头
        image_markdown = "\n".join([f"![{topic}配图 {i+1}]({url})" for i, url in enumerate(image_urls[:3])])
        markdown = f"{intro}\n{image_markdown}\n{body}"
    else:
        markdown = f"{intro}{body}"
    
    # 添加 YAML 头部
    full_markdown = f"""---
title: {title}
categories: {categories_str}
tags: {tags_str}
---

{markdown}
"""
    
    return full_markdown


def process_images_for_topic(topic, count=1):
    """
    为主题搜索并处理配图
    
    Args:
        topic: 文章主题
        count: 需要几张图
    
    Returns:
        本地图片路径列表
    """
    log_message(f"🔍 开始为 '{topic}' 搜索 {count} 张配图...")
    
    local_paths = []
    
    # 搜索并下载
    for i in range(count):
        try:
            image_path = search_and_download_image(topic, i)
            if image_path and os.path.exists(image_path):
                local_paths.append(image_path)
                log_message(f"✅ 第 {i+1} 张图下载成功：{image_path}")
            else:
                log_message(f"⚠️ 第 {i+1} 张图下载失败")
        except Exception as e:
            log_message(f"❌ 图片处理异常：{str(e)}")
    
    return local_paths


def upload_images_and_get_urls(local_paths, config=None):
    """
    上传本地图片到 Typecho，获取真实 URL
    
    Args:
        local_paths: 本地图片路径列表
        config: 配置字典
    
    Returns:
        服务器 URL 列表
    """
    if config is None:
        config = load_env()
    
    log_message(f"📤 开始上传 {len(local_paths)} 张图片到博客服务器...")
    
    server_urls = []
    for i, path in enumerate(local_paths):
        url = upload_image_to_typecho(path, config)
        if url:
            server_urls.append(url)
            log_message(f"✅ 第 {i+1} 张图上传成功：{url}")
        else:
            log_message(f"❌ 第 {i+1} 张图上传失败：{path}")
    
    return server_urls


def publish_and_publish_now(topic, categories, tags, image_urls=None, config=None):
    """
    发布文章并立即公开（不存草稿）
    
    Args:
        topic: 主题
        categories: 分类
        tags: 标签
        image_urls: 服务器图片 URL 列表
        config: 配置字典
    
    Returns:
        (成功标志，文章 ID，文章链接)
    """
    log_message("=" * 60)
    log_message("📝 开始发布文章...")
    
    # 加载配置（用于获取已有分类）
    if config is None:
        config = load_env()
    
    # 生成 Markdown 内容（带分类匹配）
    markdown_content = generate_markdown_content(topic, categories, tags, image_urls, config)
    
    # 创建临时文件
    temp_file = f"/tmp/article_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    log_message(f"📄 临时文件：{temp_file}")
    
    # 直接发布（publish_now=True）
    success = publish_from_file(temp_file, categories, tags, publish_now=True)
    
    # 清理临时文件
    if os.path.exists(temp_file):
        os.remove(temp_file)
    
    if success:
        log_message("✅ 文章发布成功！")
        # 注意：publish_from_file 内部已打印文章链接，这里不再重复
        return True, None, None
    else:
        log_message("❌ 文章发布失败")
        return False, None, None


# ============ 主函数 ============

def main():
    """主入口"""
    if len(sys.argv) < 2:
        print("❌ 参数不足！")
        print("用法：python3 publish_v2.py '主题' '分类' '标签 1，标签 2' [--image 'URL']")
        print("示例：python3 publish_v2.py 'AI 改变生活' 'AI' '人工智能，生活'")
        print("      python3 publish_v2.py 'AI 改变生活' 'AI' '人工智能' --image 'https://example.com/img.jpg'")
        sys.exit(1)
    
    topic = sys.argv[1]
    categories = sys.argv[2].split(',') if len(sys.argv) > 2 else ['技术']
    tags = sys.argv[3].split(',') if len(sys.argv) > 3 else None
    
    # 解析可选参数 --image 和 --image-file
    image_url = None
    image_file = None
    if '--image' in sys.argv:
        idx = sys.argv.index('--image')
        if idx + 1 < len(sys.argv):
            image_url = sys.argv[idx + 1]
    elif '--image-file' in sys.argv:
        idx = sys.argv.index('--image-file')
        if idx + 1 < len(sys.argv):
            image_file = sys.argv[idx + 1]
    
    log_message(f"🎯 主题：{topic}")
    log_message(f"📂 分类：{', '.join(categories)}")
    log_message(f"🏷️  标签：{', '.join(tags) if tags else '自动'}")
    
    # 加载配置
    config = load_env()
    
    # 步骤 1: 处理配图
    server_urls = []
    
    if image_url:
        # 方式 A: 使用指定的网络图片 URL
        log_message(f"\n【步骤 1】使用指定图片：{image_url}")
        # 直接上传网络图片到服务器
        url = upload_image_to_typecho(image_url, config)
        if url:
            server_urls.append(url)
            log_message(f"✅ 图片上传成功：{url}")
        else:
            log_message("❌ 图片上传失败")
    elif image_file:
        # 方式 B: 使用本地图片文件
        if os.path.exists(image_file):
            log_message(f"\n【步骤 1】使用本地图片：{image_file}")
            url = upload_image_to_typecho(image_file, config)
            if url:
                server_urls.append(url)
                log_message(f"✅ 图片上传成功：{url}")
            else:
                log_message("❌ 图片上传失败")
        else:
            log_message(f"❌ 本地图片不存在：{image_file}")
    else:
        # 方式 C: 自动搜索配图（原逻辑）
        log_message("\n【步骤 1】自动搜索配图...")
        local_images = process_images_for_topic(topic, count=1)
        
        if local_images:
            log_message("\n【步骤 2】上传图片...")
            server_urls = upload_images_and_get_urls(local_images, config)
    
    # 步骤 2: 生成文案并发布文章（直接公开）
    log_message("\n【步骤 3】生成文案并发布文章...")
    success, article_id, article_url = publish_and_publish_now(topic, categories, tags, server_urls, config)
    
    # 步骤 3: 汇报结果
    log_message("\n" + "=" * 60)
    if success:
        log_message("✅ 完成！文章已发布")
        log_message(f"🔗 查看文章：http://yuanblog.tk:9980/index.php/archives/{article_id}/")
        log_message("\n⚠️  下一步：请检查文章显示效果")
    else:
        log_message("❌ 发布失败，请检查日志")
    
    return success


if __name__ == "__main__":
    main()
