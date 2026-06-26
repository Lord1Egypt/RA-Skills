#!/usr/bin/env python3
"""
封面图生成工具
生成微信公众号文章封面图（900x383px）
支持 Pillow 规则绘制和 AI 大模型生成两种方式
"""

from PIL import Image, ImageDraw, ImageFont
import os
import base64
import requests
from typing import Optional

# ==================== 配置区域 ====================

# AI 图片生成配置（从环境变量读取）
AI_IMAGE_BASE_URL = os.getenv("AI_IMAGE_BASE_URL", "https://api.openai.com/v1")
AI_IMAGE_API_KEY = os.getenv("AI_IMAGE_API_KEY", "")
AI_IMAGE_MODEL = os.getenv("AI_IMAGE_MODEL", "dall-e-3")

# 图片尺寸
COVER_WIDTH = 900
COVER_HEIGHT = 383


# ==================== AI 图片生成 ====================

def generate_cover_with_ai(
    output_path: str,
    prompt: str,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    size: str = "1024x1024"
) -> str:
    """
    使用 AI 大模型生成封面图

    Args:
        output_path: 输出路径
        prompt: 图片生成提示词
        base_url: API 基础地址（可选，默认使用环境变量）
        api_key: API 密钥（可选，默认使用环境变量）
        model: 模型名称（可选，默认使用环境变量）
        size: 图片尺寸，如 "1024x1024", "1792x1024", "1024x1792"

    Returns:
        生成的图片路径
    """
    base_url = base_url or AI_IMAGE_BASE_URL
    api_key = api_key or AI_IMAGE_API_KEY
    model = model or AI_IMAGE_MODEL

    if not api_key:
        raise ValueError("需要设置 AI_IMAGE_API_KEY 环境变量或传入 api_key 参数")

    url = f"{base_url}/images/generations"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "prompt": prompt,
        "n": 1,
        "size": size,
        "response_format": "b64_json"
    }

    response = requests.post(url, headers=headers, json=payload, timeout=120)
    response.raise_for_status()

    data = response.json()
    image_data = data["data"][0]["b64_json"]
    image_bytes = base64.b64decode(image_data)

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(image_bytes)

    return output_path


def generate_cover_with_ai_url(
    output_path: str,
    prompt: str,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    size: str = "1024x1024"
) -> str:
    """
    使用 AI 大模型生成封面图（返回 URL 格式）

    Args:
        output_path: 输出路径
        prompt: 图片生成提示词
        base_url: API 基础地址（可选）
        api_key: API 密钥（可选）
        model: 模型名称（可选）
        size: 图片尺寸

    Returns:
        生成的图片路径
    """
    base_url = base_url or AI_IMAGE_BASE_URL
    api_key = api_key or AI_IMAGE_API_KEY
    model = model or AI_IMAGE_MODEL

    if not api_key:
        raise ValueError("需要设置 AI_IMAGE_API_KEY 环境变量或传入 api_key 参数")

    url = f"{base_url}/images/generations"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "prompt": prompt,
        "n": 1,
        "size": size,
        "response_format": "url"
    }

    response = requests.post(url, headers=headers, json=payload, timeout=120)
    response.raise_for_status()

    data = response.json()
    image_url = data["data"][0]["url"]

    image_response = requests.get(image_url, timeout=60)
    image_response.raise_for_status()

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(image_response.content)

    return output_path


# ==================== Pillow 规则绘制 ====================

def generate_cover(
    output_path: str,
    title: str = "教程标题",
    subtitle: str = "副标题",
    episode: str = "",
    tagline: str = "",
    bg_color: tuple = (10, 20, 40),
    accent_color: tuple = (59, 130, 246)
) -> str:
    """
    使用 Pillow 规则绘制封面图

    Args:
        output_path: 输出路径
        title: 主标题
        subtitle: 副标题
        episode: 期数（如"第一期"）
        tagline: 标语
        bg_color: 背景色
        accent_color: 强调色

    Returns:
        生成的图片路径
    """
    width, height = COVER_WIDTH, COVER_HEIGHT
    
    # 创建画布
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # 渐变背景
    for y in range(height):
        progress = y / height
        r = int(bg_color[0] + 15 * progress)
        g = int(bg_color[1] + 20 * progress)
        b = int(bg_color[2] + 25 * progress)
        draw.rectangle([(0, y), (width, y+1)], fill=(r, g, b))
    
    # 装饰圆形
    draw.ellipse([-50, 80, 250, 330], fill=(*accent_color, 35))
    draw.ellipse([700, 50, 950, 300], fill=(139, 92, 246, 30))
    
    # 字体
    try:
        font_title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 48)
        font_subtitle = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26)
        font_normal = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
    except:
        font_title = font_subtitle = font_normal = ImageFont.load_default()
    
    # 主标题
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_x = (width - (title_bbox[2] - title_bbox[0])) // 2
    draw.text((title_x, 100), title, font=font_title, fill=accent_color)
    
    # 副标题
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
    subtitle_x = (width - (subtitle_bbox[2] - subtitle_bbox[0])) // 2
    draw.text((subtitle_x, 160), subtitle, font=font_subtitle, fill=(255, 255, 255))
    
    # 期数
    if episode:
        ep_bbox = draw.textbbox((0, 0), episode, font=font_normal)
        ep_x = (width - (ep_bbox[2] - ep_bbox[0])) // 2
        draw.text((ep_x, 220), episode, font=font_normal, fill=(156, 163, 175))
    
    # 标语
    if tagline:
        tag_bbox = draw.textbbox((0, 0), tagline, font=font_normal)
        tag_x = (width - (tag_bbox[2] - tag_bbox[0])) // 2
        draw.text((tag_x, 300), tagline, font=font_normal, fill=(16, 185, 129))
    
    # 保存
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, 'PNG', quality=95)
    
    return output_path


def batch_generate_covers(tutorial_dir: str, episodes: list):
    """
    批量生成封面
    
    Args:
        tutorial_dir: 教程根目录
        episodes: [(期数, 目录名, 标题简称), ...]
    """
    for ep_num, dir_name, title_short in episodes:
        output_path = os.path.join(tutorial_dir, dir_name, "cover.png")
        
        generate_cover(
            output_path=output_path,
            title="教程系列",
            subtitle=title_short,
            episode=f"第{ep_num}期",
            tagline=""
        )
        
        print(f"生成封面: {output_path}")


if __name__ == "__main__":
    # 示例：AI 生成封面
    # generate_cover_with_ai(
    #     output_path="./cover_ai.png",
    #     prompt="A modern tech blog cover image with abstract geometric shapes, blue and purple gradient, minimalist style, suitable for WeChat article cover, 900x383 aspect ratio",
    #     base_url="https://api.openai.com/v1",
    #     api_key="your_api_key",
    #     model="dall-e-3"
    # )
    # print("AI 封面已生成: ./cover_ai.png")

    # 示例：Pillow 绘制封面
    generate_cover(
        output_path="./cover.png",
        title="DeepSeek API",
        subtitle="实战开发教程",
        episode="第一期",
        tagline="从入门到实战"
    )
    print("封面已生成: ./cover.png")
