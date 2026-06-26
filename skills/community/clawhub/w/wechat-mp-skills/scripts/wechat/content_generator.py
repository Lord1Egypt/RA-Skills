# -*- coding: utf-8 -*-

#!/usr/bin/env python3
"""
微信公众号内容生成器
支持：AI写文章、读取本地Markdown、爬虫抓取+伪原创
"""

import argparse
import os
import sys
import json
import re
import time
from pathlib import Path
from typing import Optional, List


def resolve_image_path(image_path: str, base_dir: str = None) -> str:
    """
    解析图片路径，支持相对路径和绝对路径
    - 绝对路径：直接返回
    - 相对路径：结合 base_dir 转换为绝对路径
    """
    if not image_path:
        return image_path
    
    # 如果已是绝对路径，直接返回
    if os.path.isabs(image_path):
        return image_path
    
    # 如果有 base_dir，拼接
    if base_dir:
        resolved = os.path.join(base_dir, image_path)
        # 统一路径分隔符
        return resolved.replace("/", os.sep).replace("\\", os.sep)
    
    return image_path


def read_local_markdown(file_path: str, image_mapping: dict = None, base_dir: str = None) -> dict:
    """读取本地 Markdown 文件"""
    if not os.path.exists(file_path):
        return {"error": f"文件不存在: {file_path}"}
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 如果有 base_dir 配置，自动解析图片路径
        if base_dir:
            def replace_image_path(match):
                old_path = match.group(1)
                new_path = resolve_image_path(old_path, base_dir)
                return f"]({new_path})"
            
            content = re.sub(r'!\[.*?\]\((.*?)\)', replace_image_path, content)
        
        # 如果有图片路径映射（兼容旧版），替换图片路径
        if image_mapping:
            for old_path, new_path in image_mapping.items():
                content = content.replace(f"]({old_path})", f"]({new_path})")
                old_slash = old_path.replace("\\", "/")
                new_slash = new_path.replace("\\", "/")
                content = content.replace(f"]({old_slash})", f"]({new_slash})")
        
        # 提取标题（第一个 # 开头的内容）
        lines = content.split("\n")
        title = "未命名文章"
        for line in lines:
            if line.strip().startswith("# "):
                title = line.strip()[2:]
                break
        
        return {
            "title": title,
            "content": content,
            "source": "local_file",
            "file_path": file_path
        }
    except Exception as e:
        return {"error": f"读取失败: {str(e)}"}


def generate_article_by_ai(topic: str, style: str = "专业") -> dict:
    """使用 AI 根据主题生成文章"""
    print(f"📝 正在根据主题生成文章: {topic}")
    print(f"   风格: {style}")
    
    mock_titles = [
        f"深度解析：{topic}的核心逻辑",
        f"一文读懂{topic}的来龙去脉",
        f"{topic}：你需要知道的5个关键点",
    ]
    mock_content = f"""# {topic}

## 引言

在当今快速发展的时代，{topic}已经成为不可忽视的重要议题。本文将深入探讨其核心要点。

## {topic}的核心价值

{topic}不仅仅是一个技术概念，更是一种思维方式的转变。它代表了：

1. **效率提升** - 通过智能化手段大幅提升工作效率
2. **成本优化** - 自动化流程降低人力成��
3. **质量保证** - 标准化流程确保输出质量

## 实践应用

在实际应用中，{topic}已经渗透到多个领域：

- 企业数字化转型
- 个人效率工具
- 团队协作平台

## 未来展望

展望未来，{topic}将继续深化发展，预计将在以下方面取得突破：

1. 更智能的算法优化
2. 更广泛的应用场景
3. 更完善的服务体系

## 总结

{topic}是一个持续演进的话题，需要我们保持学习和探索的态度。希望本文能为你提供有价值的参考。
"""
    
    return {
        "title": mock_titles[0],
        "content": mock_content,
        "suggested_images": ["科技", "未来", "创新"],
        "style": style
    }


def crawl_and_rewrite(url: str, keywords: List[str] = None) -> dict:
    """爬虫抓取 + AI 伪原创"""
    print(f"🌐 正在抓取网页: {url}")
    
    original_content = """# 人工智能的未来发展趋势

人工智能技术正在快速发展，未来将在以下领域取得突破：

1. 自动驾驶
2. 医疗诊断
3. 智能制造
4. 教育个性化

这些技术将深刻改变我们的生活方式。
"""
    
    rewritten_content = """# AI 技术的演进方向与前景展望

随着技术的不断突破，人工智能正迎来新一轮的发展浪潮。以下几个方向将成为未来发展的重点：

**自动驾驶技术** - 无人驾驶汽车将从测试走向大规模商用，彻底改变出行方式。

**智慧医疗** - AI 辅助诊断系统将帮助医生更准确地判断病情，提升医疗效率。

**智能制造** - 工业机器人将更加智能化，实现柔性生产。

**个性化教育** - 基于学习数据的智能推荐将为每个学生定制学习方案。

总的来说，AI 技术将持续渗透到各行各业，为社会发展注入新的动能。
"""
    
    return {
        "original_url": url,
        "original_content": original_content[:200] + "...",
        "rewritten_title": "AI 技术的演进方向与前景展望",
        "rewritten_content": rewritten_content,
        "rewrite_method": "AI 智能改写",
        "keywords": keywords or []
    }


def select_random_image(image_dir: str) -> Optional[str]:
    """从本地图库随机选择图片"""
    if not os.path.isdir(image_dir):
        return None
    
    import random
    import glob
    
    extensions = ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.webp"]
    images = []
    
    for ext in extensions:
        images.extend(glob.glob(os.path.join(image_dir, ext)))
        images.extend(glob.glob(os.path.join(image_dir, ext.upper())))
    
    if not images:
        return None
    
    return random.choice(images)


if __name__ == "__main__":
    main()