#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书图片生成技能 - 针对家装、美食、穿搭等赛道

支持风格：
- 家装：现代简约、北欧、日式、美式、中式
- 美食：精致摆盘、家常菜、烘焙、饮品
- 穿搭：春夏季、秋冬、休闲、职场、约会

需要配置：
- OPENAI_API_KEY（用于 DALL-E 生成）或
- STABILITY_API_KEY（用于 Stable Diffusion）
"""

import argparse
import json
import os
import sys
import subprocess
from pathlib import Path

# 支持的风格
STYLES = {
    "家装": {
        "prefixes": ["装修设计", "室内设计", "家居风格"],
        "suffixes": ["高清摄影", "专业摄影", "ins风"],
        "styles": ["现代简约", "北欧", "日式", "美式", "中式", "轻奢", "法式"]
    },
    "美食": {
        "prefixes": ["美食摄影", "精致摆盘", "诱人美食"],
        "suffixes": ["高清摄影", "美食拍摄", "ins风"],
        "styles": ["家常菜", "烘焙", "饮品", "甜点", "日料", "西餐"]
    },
    "穿搭": {
        "prefixes": ["时尚穿搭", "穿搭博主", "ins风穿搭"],
        "suffixes": ["高清摄影", "街拍", "模特拍摄"],
        "styles": ["春夏季", "秋冬", "休闲", "职场", "约会", "运动"]
    },
    "旅行": {
        "prefixes": ["旅行摄影", "风景摄影", "ins风"],
        "suffixes": ["高清摄影", "专业摄影", "网红打卡"],
        "styles": ["海边", "山景", "城市", "古镇", "日出日落"]
    }
}

DEFAULT_STYLES = {
    "家装": "现代简约",
    "美食": "精致摆盘",
    "穿搭": "春夏季",
    "旅行": "海边"
}

# 小红书图片规格（竖屏为主）
ASPECT_RATIOS = {
    "竖屏": "9:16",
    "正方形": "1:1",
    "横屏": "16:9"
}

DEFAULT_ASPECT = "竖屏"


def check_env():
    """检查是否配置了 API Key"""
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    elif os.getenv("STABILITY_API_KEY"):
        return "stability"
    else:
        return None


def build_prompt(user_prompt, style_name, category):
    """
    构建适合小红书的图片提示词

    Args:
        user_prompt: 用户提供的核心提示词
        style_name: 具体风格（如"现代简约"）
        category: 大类（家装/美食/穿搭）

    Returns:
        增强后的提示词
    """
    style_config = STYLES.get(category, STYLES["家装"])

    # 前缀 + 风格 + 用户提示词 + 后缀
    prefix = style_config["prefixes"][0]
    suffix = style_config["suffixes"][0]

    prompt = f"{prefix}，{style_name}风格，{user_prompt}，{suffix}"

    return prompt


def generate_with_openai(prompt, output_path, aspect_ratio):
    """使用 OpenAI DALL-E 生成图片"""
    import openai

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # 根据宽高比设置 size
    size_map = {
        "1:1": "1024x1024",
        "16:9": "1792x1024",
        "9:16": "1024x1792"
    }
    size = size_map.get(aspect_ratio, "1024x1792")

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="standard",
        n=1
    )

    image_url = response.data[0].url

    # 下载图片
    import requests
    img_response = requests.get(image_url)
    with open(output_path, "wb") as f:
        f.write(img_response.content)

    return output_path


def generate_with_stability(prompt, output_path, aspect_ratio):
    """使用 Stability AI 生成图片"""
    import requests

    # 根据宽高比设置尺寸
    if aspect_ratio == "1:1":
        width, height = 1024, 1024
    elif aspect_ratio == "16:9":
        width, height = 1280, 720
    else:  # 9:16
        width, height = 720, 1280

    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

    headers = {
        "Authorization": f"Bearer {os.getenv('STABILITY_API_KEY')}",
        "Content-Type": "application/json"
    }

    body = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": 7,
        "height": height,
        "width": width,
        "steps": 30,
        "samples": 1
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code != 200:
        raise Exception(f"Stability AI 错误: {response.text}")

    data = response.json()

    # 保存图片
    import base64
    import io
    from PIL import Image

    image_data = base64.b64decode(data["artifacts"][0]["base64"])
    image = Image.open(io.BytesIO(image_data))
    image.save(output_path)

    return output_path


def fallback_generate(prompt, output_path):
    """
    降级方案：调用本地的 image-generate 技能
    """
    # 检查 image-generate 脚本是否存在
    script_path = Path.home() / ".openclaw" / "workspace" / "skills" / "image-generate" / "source" / "image_generate.py"

    if not script_path.exists():
        print(f"❌ 错误：未找到 image-generate 脚本：{script_path}")
        print("💡 建议：安装 image-generate 技能或配置 API Key")
        sys.exit(1)

    # 调用脚本
    try:
        result = subprocess.run(
            [sys.executable, str(script_path), prompt, "-o", output_path],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            print(f"❌ image-generate 执行失败：{result.stderr}")
            sys.exit(1)

        return output_path
    except subprocess.TimeoutExpired:
        print("❌ 图片生成超时（2分钟）")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="小红书图片生成技能 - 针对家装、美食、穿搭等赛道",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法：
  # 家装风格
  xiaohongshu-image-gen --prompt "客厅白色沙发搭配原木色地板" --style "家装" --substyle "现代简约"

  # 美食风格
  xiaohongshu-image-gen --prompt "日式拉面汤浓面劲道" --style "美食"

  # 穿搭风格
  xiaohongshu-image-gen --prompt "米色风衣搭配白色直筒裤" --style "穿搭" --substyle "职场"

  # 使用本地 image-generate
  xiaohongshu-image-gen --prompt "现代简约客厅设计" --use-local

配置说明：
  # OpenAI DALL-E（推荐）
  export OPENAI_API_KEY="sk-..."

  # Stability AI
  export STABILITY_API_KEY="sk-..."
        """
    )

    parser.add_argument("--prompt", "-p", required=True, help="图片描述（中文）")
    parser.add_argument("--style", "-s", choices=STYLES.keys(), default="家装", help="大类（家装/美食/穿搭/旅行）")
    parser.add_argument("--substyle", help="具体风格（如：现代简约/北欧/日式）")
    parser.add_argument("--aspect", "-a", choices=ASPECT_RATIOS.keys(), default=DEFAULT_ASPECT, help="宽高比（竖屏/正方形/横屏）")
    parser.add_argument("--output", "-o", help="输出路径（默认：xiaohongshu_image.png）")
    parser.add_argument("--use-local", action="store_true", help="使用本地 image-generate（无需 API Key）")
    parser.add_argument("--list-styles", action="store_true", help="列出所有可用风格")

    args = parser.parse_args()

    # 列出风格
    if args.list_styles:
        print("🎨 可用风格：")
        print()
        for category, config in STYLES.items():
            print(f"【{category}】")
            for style in config["styles"]:
                print(f"  • {style}")
            print()
        return

    # 确定具体风格
    if args.substyle:
        substyle = args.substyle
    else:
        substyle = DEFAULT_STYLES.get(args.style, "")

    # 构建提示词
    enhanced_prompt = build_prompt(args.prompt, substyle, args.style)

    print(f"🎨 生成图片中...")
    print(f"   风格：{args.style} - {substyle}")
    print(f"   宽高比：{args.aspect} ({ASPECT_RATIOS[args.aspect]})")
    print(f"   提示词：{enhanced_prompt}")
    print()

    # 输出路径
    if args.output:
        output_path = args.output
    else:
        timestamp = int(time.time())
        output_path = f"xiaohongshu_image_{timestamp}.png"

    # 选择生成方式
    if args.use_local:
        # 强制使用本地
        provider = "local"
    else:
        # 检查环境
        provider = check_env()

        if not provider:
            print("⚠️  未配置 API Key，降级使用本地 image-generate")
            print("   配置 OPENAI_API_KEY 或 STABILITY_API_KEY 以使用云端生成")
            print()
            provider = "local"

    # 生成图片
    try:
        if provider == "openai":
            print("📡 使用 OpenAI DALL-E 生成...")
            result = generate_with_openai(enhanced_prompt, output_path, args.aspect)
        elif provider == "stability":
            print("📡 使用 Stability AI 生成...")
            result = generate_with_stability(enhanced_prompt, output_path, args.aspect)
        else:
            print("💻 使用本地 image-generate 生成...")
            result = fallback_generate(enhanced_prompt, output_path)

        print()
        print(f"✅ 图片已生成：{result}")
        print(f"📏 大小：{os.path.getsize(result) / 1024:.1f} KB")

    except Exception as e:
        print(f"❌ 生成失败：{e}")
        sys.exit(1)


if __name__ == "__main__":
    import time
    main()
