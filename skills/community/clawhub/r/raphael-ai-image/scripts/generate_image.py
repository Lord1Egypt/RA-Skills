#!/usr/bin/env python3
"""
Raphael AI Image Generation Script
==================================
This script is a DOCUMENTATION HOLDER only.

The actual image generation is done via OpenClaw Browser automation.
To generate an image:

1. Tell 紫灵 (main agent): "生成一张[风格]风格的[主题]图"
2. 紫灵 uses OpenClaw Browser to:
   - Navigate to https://raphaelai.org/zh/ai-image-generator
   - Enter the prompt text
   - Click "生成"
   - Wait ~15 seconds for generation
   - Extract image URL from DOM (cdn.raphaelai.org)
   - Download via curl
   - Send to Discord channel

Usage from sub-agent:
  Send a message to 紫灵 requesting image generation:
  
  📷 生图请求
  提示词：enchanted forest with floating lanterns
  风格：Fantasy
  
  Or simply: "帮我生成一张奇幻风格的森林图"

Supported styles (use in prompt or via style= parameter):
  Photo, Anime, Fantasy, Portrait, Landscape, Sci-Fi, Cinematic,
  Oil Painting, Pixel Art, Watercolor, Ghibli, Vintage, Film,
  Ink Wash, Dreamcore, Solarpunk, Neon Noir, Earth, Baroque Gold,
  Vaporwave, Blueprint, Wabi-Sabi, Ultra Flat, Brutalist

For reference only - not directly executable for image generation.
"""
import sys

STYLES = {
    "photo": "Photo - 专业相机质感的写实细节",
    "anime": "Anime - 充满活力的漫画风格插画",
    "fantasy": "Fantasy - 宏大魔法世界的电影感深度",
    "portrait": "Portrait - 影棚级的人物和面部强调",
    "landscape": "Landscape - 宽阔的风景构图和戏剧性天空",
    "sci-fi": "Sci-Fi - 未来科技元素和太空能量",
    "cinematic": "Cinematic - 电影剧照构图与戏剧性光线",
    "oil_painting": "Oil Painting - 古典笔触纹理和艺术深度",
    "pixel_art": "Pixel Art - 复古16位风格与清晰色块",
    "watercolor": "Watercolor - 柔和颜料晕染和绘画边缘",
    "ghibli": "Ghibli - 梦幻手绘动画的魅力",
    "vintage": "Vintage - 复古色调、颗粒感和陈旧色彩氛围",
    "film": "Film - 模拟35毫米胶片颗粒和自然光",
    "ink_wash": "Ink Wash - 水墨画笔触感和留白",
    "dreamcore": "Dreamcore - 超现实粉彩烟雾和阈限空间",
    "solarpunk": "Solarpunk - 生态乌托邦与有机新艺术风格",
    "neon_noir": "Neon Noir - 黑暗赛博朋克霓虹倒影",
    "earth": "Earth - 陶土和暖赭石纹理",
    "baroque_gold": "Baroque Gold - 金箔华丽与戏剧性对比",
    "vaporwave": "Vaporwave - 复古未来主义1980年代数字氛围",
    "blueprint": "Blueprint - 技术性钴蓝色建筑图纸",
    "wabi_sabi": "Wabi-Sabi - 不完美的日本极简主义",
    "ultra_flat": "Ultra Flat - 受动漫启发的扁平波普艺术",
    "brutalist": "Brutalist - 原始混凝土几何和纪念碑尺度",
}

PROMPT_FORMULA = "[主体] + [动作] + [环境] + [光线] + [风格] + [输出限制]"

EXAMPLE_PROMPTS = {
    "fantasy": "enchanted forest with floating lanterns magical creatures, epic fantasy landscape, dramatic lighting, cinematic composition, fantasy style, no text watermark",
    "product": "minimalist wireless earbuds product photo on clean white marble, soft studio lighting, shallow depth of field, professional e-commerce photography, no text watermark",
    "portrait": "cinematic portrait of a wise old wizard holding a glowing staff, epic fantasy background, dramatic golden hour lighting, film grain, no text watermark",
    "neon_noir": "cyberpunk city street at night, neon signs reflecting in rain puddles, lone figure walking, neon noir style, cinematic, no text watermark",
    "ghibli": "peaceful countryside with rolling hills and cherry blossoms, Studio Ghibli animation style, warm sunlight, no text watermark",
}

def print_usage():
    print(__doc__)
    print("\n=== Available Styles ===")
    for key, desc in STYLES.items():
        print(f"  {key:15s} - {desc}")
    print(f"\n=== Prompt Formula ===\n  {PROMPT_FORMULA}")
    print("\n=== Example Prompts ===")
    for name, prompt in EXAMPLE_PROMPTS.items():
        print(f"\n  [{name}]")
        print(f"  {prompt}")

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print_usage()
        sys.exit(0)
    
    # This script is documentation-only
    # Actual generation happens via OpenClaw Browser
    print("This script is for reference only.")
    print("To generate images, send a request to 紫灵 (main agent).")
    print("Example: 帮我生成一张 fantasy 风格的奇幻森林图")
