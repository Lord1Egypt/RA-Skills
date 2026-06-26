#!/usr/bin/env python3
"""
Typecho 博客发布技能 v2.0
完整流程：主题 → 搜索配图 → 生成文案 → 上传图片 → 获取真实 URL → 存草稿 → 验证 → 发布

工作流程：
1. 根据主题搜索网络配图（Unsplash/Pexels 等）
2. 下载图片到本地
3. 生成 Markdown 文案（包含图片占位符）
4. 上传图片到 Typecho 服务器
5. 替换文案中的图片为真实 URL
6. 发布为草稿（不立即发布）
7. 返回草稿链接供预览检查

使用方法:
    python3 publish_v2.py "AI 改变生活的 5 种方式" "技术，AI" "人工智能，生活，科技"
    # 参数：主题标题，分类，标签（可选）
"""

import os
import sys
import re
import requests
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

# 新增：图片搜索和下载模块
from image_finder import search_and_download_image

# ============ 核心函数 ============

def generate_markdown_content(topic, categories, tags, image_urls=None):
    """
    根据主题生成 Markdown 文案
    
    Args:
        topic: 文章主题
        categories: 分类列表
        tags: 标签列表
        image_urls: 配图 URL 列表（可选）
    
    Returns:
        Markdown 格式的完整文案
    """
    # 生成标题
    title = topic.strip()
    
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
    
    markdown = f"""---
title: {title}
categories: {categories_str}
tags: {tags_str}
---

{intro}
{body}
"""
    
    # 如果有图片，插入到开头
    if image_urls:
        image_markdown = "\n".join([f"![{topic}配图 {i+1}]({url})" for i, url in enumerate(image_urls[:3])])
        markdown = f"{intro}\n{image_markdown}\n{body}"
    
    return markdown


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
    
    # 调用图片搜索模块
    for i in range(count):
        try:
            # 搜索并下载
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


def publish_to_draft(topic, categories, tags, image_urls=None):
    """
    发布为草稿（不立即发布）
    
    Args:
        topic: 主题
        categories: 分类
        tags: 标签
        image_urls: 服务器图片 URL 列表
    
    Returns:
        (成功标志，草稿 ID，草稿链接)
    """
    log_message("=" * 60)
    log_message("📝 开始发布草稿...")
    
    # 生成 Markdown 内容
    markdown_content = generate_markdown_content(topic, categories, tags, image_urls)
    
    # 创建临时文件
    temp_file = f"/tmp/draft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    log_message(f"📄 临时文件：{temp_file}")
    
    # 发布为草稿（publish_now=False）
    success = publish_from_file(temp_file, categories, tags, publish_now=False)
    
    # 清理临时文件
    if os.path.exists(temp_file):
        os.remove(temp_file)
    
    if success:
        log_message("✅ 草稿发布成功！")
        return True, None, None
    else:
        log_message("❌ 草稿发布失败")
        return False, None, None


# ============ 主函数 ============

def main():
    """主入口"""
    if len(sys.argv) < 2:
        print("❌ 参数不足！")
        print("用法：python3 publish_v2.py '主题' '分类' '标签 1，标签 2'")
        print("示例：python3 publish_v2.py 'AI 改变生活' '技术' '人工智能，生活'")
        sys.exit(1)
    
    topic = sys.argv[1]
    categories = sys.argv[2].split(',') if len(sys.argv) > 2 else ['技术']
    tags = sys.argv[3].split(',') if len(sys.argv) > 3 else None
    
    log_message(f"🎯 主题：{topic}")
    log_message(f"📂 分类：{', '.join(categories)}")
    log_message(f"🏷️  标签：{', '.join(tags) if tags else '自动'}")
    
    # 步骤 1: 搜索并下载配图
    log_message("\n【步骤 1】搜索配图...")
    local_images = process_images_for_topic(topic, count=1)
    
    # 步骤 2: 上传图片到服务器
    server_urls = []
    if local_images:
        log_message("\n【步骤 2】上传图片...")
        config = load_env()
        server_urls = upload_images_and_get_urls(local_images, config)
    
    # 步骤 3: 生成文案并发布草稿
    log_message("\n【步骤 3】生成文案并发布草稿...")
    success, draft_id, draft_url = publish_to_draft(topic, categories, server_urls)
    
    # 步骤 4: 汇报结果
    log_message("\n" + "=" * 60)
    if success:
        log_message("✅ 完成！草稿已保存")
        log_message(f"🔗 请预览检查：http://yuanblog.tk:9980/admin/write-post.php?cid={draft_id}")
        log_message("\n⚠️  下一步：请主人预览后手动发布")
    else:
        log_message("❌ 发布失败，请检查日志")
    
    return success


if __name__ == "__main__":
    main()
