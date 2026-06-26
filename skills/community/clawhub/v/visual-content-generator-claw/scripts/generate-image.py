#!/usr/bin/env python3
"""
视觉素材美工虾 - AI图片生成主程序
支持：本地 Stable Diffusion / DALL-E 3 / 文心一格
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

# ─────────────────────────────────────────────
# 输出目录（默认 workspace）
# ─────────────────────────────────────────────
DEFAULT_OUTPUT_DIR = Path(os.environ.get("OPENCLAW_WORKSPACE", Path.home() / ".openclaw/workspace"))


def build_prompt(prompt: str, style: str = "", negative: str = "") -> tuple[str, str]:
    """组合正向 prompt 和负向 prompt"""
    quality_suffix = "high quality, detailed, 8K, professional"
    style_part = f", {style}" if style else ""
    positive = f"{prompt}{style_part}, {quality_suffix}"

    default_negative = (
        "blurry, low quality, pixelated, distorted text, watermark, logo, "
        "signature, oversaturated, deformed, ugly, bad anatomy, low resolution"
    )
    neg = negative if negative else default_negative
    return positive, neg


def generate_with_dalle3(prompt: str, size: str, count: int, output_dir: Path) -> list[Path]:
    """使用 DALL-E 3 生成图片（需要 OPENAI_API_KEY）"""
    try:
        from openai import OpenAI
    except ImportError:
        print("[ERROR] openai 未安装，运行: pip install openai", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("[ERROR] 未设置 OPENAI_API_KEY 环境变量", file=sys.stderr)
        sys.exit(1)

    # DALL-E 3 支持的尺寸
    size_map = {
        "1024x1024": "1024x1024",
        "1080x1080": "1024x1024",  # 最接近
        "1792x1024": "1792x1024",
        "1024x1792": "1024x1792",
        "1080x1920": "1024x1792",  # 最接近
        "1920x1080": "1792x1024",  # 最接近
    }
    dalle_size = size_map.get(size, "1024x1024")
    if dalle_size != size:
        print(f"[INFO] DALL-E 3 不支持 {size}，自动使用最接近的 {dalle_size}")

    client = OpenAI(api_key=api_key)
    output_dir.mkdir(parents=True, exist_ok=True)
    saved_paths = []

    # DALL-E 3 每次只能生成 1 张，循环生成
    actual_count = min(count, 4)  # 最多4张，避免费用过高
    for i in range(actual_count):
        print(f"[INFO] 正在生成第 {i+1}/{actual_count} 张...")
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=dalle_size,
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url

        # 下载图片
        import urllib.request
        timestamp = int(time.time())
        filename = output_dir / f"generated_{timestamp}_{i+1}.png"
        urllib.request.urlretrieve(image_url, filename)
        saved_paths.append(filename)
        print(f"[OK] 已保存: {filename}")

    return saved_paths


def generate_with_stable_diffusion(prompt: str, negative: str, size: str, count: int, output_dir: Path) -> list[Path]:
    """使用本地 Stable Diffusion 生成图片（需要 diffusers + torch）"""
    try:
        import torch
        from diffusers import StableDiffusionPipeline
    except ImportError:
        print("[ERROR] diffusers/torch 未安装，运行: pip install diffusers torch", file=sys.stderr)
        sys.exit(1)

    # 解析尺寸
    try:
        w, h = map(int, size.split("x"))
        # SD 要求尺寸是 8 的倍数
        w = (w // 8) * 8
        h = (h // 8) * 8
    except ValueError:
        print(f"[ERROR] 尺寸格式错误，应为 WIDTHxHEIGHT，如 1080x1080", file=sys.stderr)
        sys.exit(1)

    model_id = os.environ.get("SD_MODEL_ID", "runwayml/stable-diffusion-v1-5")
    device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[INFO] 使用设备: {device}，模型: {model_id}")

    pipe = StableDiffusionPipeline.from_pretrained(model_id)
    pipe = pipe.to(device)

    output_dir.mkdir(parents=True, exist_ok=True)
    saved_paths = []

    for i in range(count):
        print(f"[INFO] 正在生成第 {i+1}/{count} 张...")
        result = pipe(
            prompt=prompt,
            negative_prompt=negative,
            width=w,
            height=h,
            num_inference_steps=30,
        )
        image = result.images[0]
        timestamp = int(time.time())
        filename = output_dir / f"generated_{timestamp}_{i+1}.png"
        image.save(filename)
        saved_paths.append(filename)
        print(f"[OK] 已保存: {filename}")

    return saved_paths


def apply_template(template: str, title: str) -> tuple[str, str]:
    """根据预设模板生成 prompt"""
    templates = {
        "poster-tech": (
            f"科技感海报，主题：{title}，深蓝色渐变背景，光线粒子特效，"
            "未来感设计，专业排版，高对比度，醒目标题区域",
            ""
        ),
        "poster-business": (
            f"商务风格海报，主题：{title}，简洁白色背景，"
            "几何图形装饰，专业字体排版，高端感，留白设计",
            ""
        ),
        "cover-xiaohongshu": (
            f"小红书封面图，主题：{title}，1:1构图，"
            "小清新风格，莫兰迪色系，温暖氛围，吸睛设计",
            ""
        ),
        "cover-video": (
            f"视频封面，主题：{title}，9:16竖版构图，"
            "大标题文字区域，强烈视觉冲击，高对比度色彩",
            ""
        ),
        "bg-virtual-human": (
            f"数字人视频背景，{title}场景，专业演播室氛围，"
            "虚化处理，无主体干扰，适合人物叠加",
            ""
        ),
    }
    if template not in templates:
        available = ", ".join(templates.keys())
        print(f"[ERROR] 未知模板: {template}，可用模板: {available}", file=sys.stderr)
        sys.exit(1)
    return templates[template]


def main():
    parser = argparse.ArgumentParser(description="视觉素材美工虾 - AI图片生成工具")
    parser.add_argument("--prompt", type=str, help="图片描述（正向prompt）")
    parser.add_argument("--negative", type=str, default="", help="负向prompt（不想要的元素）")
    parser.add_argument("--style", type=str, default="", help="风格关键词（会追加到prompt）")
    parser.add_argument("--size", type=str, default="1080x1080", help="图片尺寸，格式: WxH（默认 1080x1080）")
    parser.add_argument("--count", type=int, default=1, help="生成数量（默认1，建议最多4）")
    parser.add_argument("--template", type=str, default="", help="使用预设模板（poster-tech/poster-business/cover-xiaohongshu/cover-video/bg-virtual-human）")
    parser.add_argument("--title", type=str, default="", help="配合 --template 使用的标题文字")
    parser.add_argument("--engine", type=str, default="auto", help="生成引擎: auto/dalle3/sd（默认auto自动选择）")
    parser.add_argument("--output", type=str, default="", help="输出目录（默认: workspace目录）")
    parser.add_argument("--list-templates", action="store_true", help="列出所有可用模板")

    args = parser.parse_args()

    if args.list_templates:
        templates = ["poster-tech", "poster-business", "cover-xiaohongshu", "cover-video", "bg-virtual-human"]
        print("可用模板：")
        for t in templates:
            print(f"  {t}")
        return

    output_dir = Path(args.output) if args.output else DEFAULT_OUTPUT_DIR / "visual-output"

    # 处理 prompt 来源
    if args.template:
        if not args.title:
            print("[ERROR] 使用 --template 时必须提供 --title", file=sys.stderr)
            sys.exit(1)
        positive, negative = apply_template(args.template, args.title)
        if args.negative:
            negative = args.negative
    elif args.prompt:
        positive, negative = build_prompt(args.prompt, args.style, args.negative)
    else:
        print("[ERROR] 请提供 --prompt 或 --template", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    print(f"\n📋 生成配置：")
    print(f"  正向Prompt: {positive}")
    print(f"  负向Prompt: {negative}")
    print(f"  尺寸: {args.size}  数量: {args.count}  引擎: {args.engine}")
    print(f"  输出目录: {output_dir}\n")

    # 选择引擎
    engine = args.engine
    if engine == "auto":
        # 优先 SD（本地），其次 DALL-E 3
        try:
            import torch
            from diffusers import StableDiffusionPipeline  # noqa
            engine = "sd"
        except ImportError:
            if os.environ.get("OPENAI_API_KEY"):
                engine = "dalle3"
            else:
                print("[ERROR] 未找到可用的生成引擎。", file=sys.stderr)
                print("  选项1：安装 Stable Diffusion: pip install diffusers torch", file=sys.stderr)
                print("  选项2：设置 OPENAI_API_KEY 环境变量使用 DALL-E 3", file=sys.stderr)
                sys.exit(1)
        print(f"[INFO] 自动选择引擎: {engine}")

    # 执行生成
    if engine == "dalle3":
        saved = generate_with_dalle3(positive, args.size, args.count, output_dir)
    elif engine == "sd":
        saved = generate_with_stable_diffusion(positive, negative, args.size, args.count, output_dir)
    else:
        print(f"[ERROR] 未知引擎: {engine}，支持: auto/dalle3/sd", file=sys.stderr)
        sys.exit(1)

    print(f"\n✅ 生成完成！共 {len(saved)} 张图片：")
    for p in saved:
        print(f"  {p}")

    # 输出 JSON 结果（供 OpenClaw 解析）
    result = {
        "status": "success",
        "count": len(saved),
        "files": [str(p) for p in saved],
        "output_dir": str(output_dir),
    }
    print(f"\n[JSON_RESULT] {json.dumps(result, ensure_ascii=False)}")


if __name__ == "__main__":
    main()
