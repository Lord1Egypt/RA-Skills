#!/usr/bin/env python3
"""
Stable Diffusion Prompt Helper
- Chinese to English prompt translation
- Prompt optimization and quality tag injection
- Style preset management
"""

import argparse
import json
import sys
import os
import re


# ── Style Presets ───────────────────────────────────────────────────────────────
STYLE_PRESETS = {
    "realistic": {
        "positive": "photorealistic, ultra realistic, RAW photo, 8k uhd, masterpiece",
        "negative": "painting, cartoon, anime, blurry, bad anatomy"
    },
    "anime": {
        "positive": "anime style, 2d, cel shading, best quality, masterpiece",
        "negative": "3d, photorealistic, bad anatomy, bad hands"
    },
    "oil_painting": {
        "positive": "oil painting, painterly, impressionist, detailed brushwork, canvas texture",
        "negative": "photo, digital art, blurry"
    },
    "watercolor": {
        "positive": "watercolor painting, soft colors, transparent, fluid, artistic",
        "negative": "digital, sharp edges, photorealistic"
    },
    "cyberpunk": {
        "positive": "cyberpunk, neon lights, futuristic, sci-fi, high tech, dark atmosphere",
        "negative": "natural, rural, historical"
    },
    "chinese_art": {
        "positive": "chinese traditional art, ink wash painting, hanfu, guofeng, elegant",
        "negative": "western, modern clothing, photorealistic"
    },
    "pixar": {
        "positive": "pixar style, 3d render, disney, cartoon, vibrant colors, cute",
        "negative": "dark, realistic, 2d"
    },
    "sketch": {
        "positive": "pencil sketch, lineart, monochrome, detailed lines, hand drawn",
        "negative": "color, photorealistic, painting"
    },
    "fantasy": {
        "positive": "fantasy art, magical, ethereal, dramatic lighting, epic",
        "negative": "mundane, realistic, modern"
    },
    "portrait": {
        "positive": "portrait photography, studio lighting, shallow depth of field, detailed face",
        "negative": "landscape, bad face, distorted"
    }
}

# ── Chinese Keyword Mapping ─────────────────────────────────────────────────────
ZH_EN_MAP = {
    # 人物
    "女孩": "1girl", "男孩": "1boy", "女人": "woman", "男人": "man",
    "美女": "beautiful woman", "帅哥": "handsome man", "少女": "young girl",
    "老人": "elderly person", "儿童": "child",
    # 外貌
    "长发": "long hair", "短发": "short hair", "金发": "blonde hair",
    "黑发": "black hair", "卷发": "curly hair", "蓝眼": "blue eyes",
    "微笑": "smiling", "表情严肃": "serious expression",
    # 服装
    "汉服": "hanfu, traditional chinese clothing",
    "旗袍": "cheongsam, qipao",
    "和服": "kimono",
    "西装": "suit", "裙子": "dress", "T恤": "t-shirt",
    "盔甲": "armor", "战袍": "battle robe",
    # 场景
    "樱花": "cherry blossom, sakura",
    "森林": "forest", "城市": "city, urban",
    "海边": "beach, seaside", "山景": "mountain landscape",
    "夜晚": "night, nighttime", "日落": "sunset",
    "古代": "ancient, historical", "未来": "futuristic",
    "室内": "indoor, interior", "室外": "outdoor, exterior",
    # 光照
    "自然光": "natural lighting", "柔光": "soft lighting",
    "逆光": "backlit, rim lighting", "戏剧光": "dramatic lighting",
    "霓虹灯": "neon lights",
    # 质量
    "高质量": "high quality, masterpiece", "超详细": "ultra detailed",
    "4K": "4k resolution", "8K": "8k resolution",
    "超清": "ultra clear, high definition",
}

# ── Functions ───────────────────────────────────────────────────────────────────

def contains_chinese(text: str) -> bool:
    return bool(re.search(r'[\u4e00-\u9fff]', text))


def translate_zh_keywords(text: str) -> str:
    """Replace known Chinese keywords with English equivalents"""
    for zh, en in ZH_EN_MAP.items():
        text = text.replace(zh, en)
    return text


def optimize_prompt(prompt: str, style: str = None, add_quality: bool = True) -> dict:
    """
    Optimize a prompt by:
    1. Translating Chinese keywords
    2. Adding style preset
    3. Adding quality tags
    """
    # Translate Chinese
    if contains_chinese(prompt):
        print("ℹ️  检测到中文，正在转换...")
        translated = translate_zh_keywords(prompt)
        # For remaining Chinese, provide a reminder
        if contains_chinese(translated):
            remaining = re.findall(r'[\u4e00-\u9fff]+', translated)
            if remaining:
                print(f"⚠️  以下内容需手动翻译: {', '.join(set(remaining))}")
    else:
        translated = prompt

    positive_parts = [translated]
    negative_parts = []

    # Add style preset
    if style and style in STYLE_PRESETS:
        preset = STYLE_PRESETS[style]
        positive_parts.append(preset["positive"])
        negative_parts.append(preset["negative"])
        print(f"✨ 应用风格: {style}")

    # Add quality tags
    if add_quality:
        quality_positive = "masterpiece, best quality, ultra-detailed"
        quality_negative = "(worst quality:2), (low quality:2), blurry, ugly, bad anatomy, bad hands, extra fingers, deformed, mutated, poorly drawn face, watermark, text, signature"
        if quality_positive not in " ".join(positive_parts):
            positive_parts.append(quality_positive)
        negative_parts.append(quality_negative)

    final_positive = ", ".join(filter(None, positive_parts))
    final_negative = ", ".join(filter(None, negative_parts))

    return {
        "positive": final_positive,
        "negative": final_negative
    }


def list_styles():
    print("\n🎨 可用风格预设:")
    for name, preset in STYLE_PRESETS.items():
        print(f"\n  [{name}]")
        print(f"    正向: {preset['positive'][:60]}...")
        print(f"    负向: {preset['negative'][:60]}...")


def interactive_build():
    """Interactive prompt builder"""
    print("🛠️  交互式提示词生成器\n")

    subject = input("1. 主体描述 (人物/物体/场景): ").strip()
    style_input = input(f"2. 风格 ({'/'.join(STYLE_PRESETS.keys())}，留空跳过): ").strip()
    extra = input("3. 额外细节 (可选): ").strip()

    style = style_input if style_input in STYLE_PRESETS else None

    combined = ", ".join(filter(None, [subject, extra]))
    result = optimize_prompt(combined, style=style, add_quality=True)

    print(f"\n📋 优化后提示词:")
    print(f"  正向: {result['positive']}")
    print(f"  负向: {result['negative']}")

    # Output as command hint
    print(f"\n💡 使用命令:")
    print(f"  python sd_client.py --action txt2img \\")
    print(f"    --prompt \"{result['positive']}\" \\")
    print(f"    --negative-prompt \"{result['negative']}\"")


# ── Main ────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="SD Prompt Helper")
    parser.add_argument("--translate", "-t", help="翻译并优化提示词")
    parser.add_argument("--style", "-s", help="应用风格预设")
    parser.add_argument("--list-styles", action="store_true", help="列出所有风格预设")
    parser.add_argument("--no-quality", action="store_true", help="不添加质量标签")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互式构建")
    parser.add_argument("--output-format", default="text", choices=["text", "json"],
                        help="输出格式")
    args = parser.parse_args()

    if args.list_styles:
        list_styles()
        return

    if args.interactive:
        interactive_build()
        return

    if args.translate:
        result = optimize_prompt(
            args.translate,
            style=args.style,
            add_quality=not args.no_quality
        )
        if args.output_format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n✅ 正向提示词:\n{result['positive']}")
            print(f"\n❌ 负向提示词:\n{result['negative']}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
