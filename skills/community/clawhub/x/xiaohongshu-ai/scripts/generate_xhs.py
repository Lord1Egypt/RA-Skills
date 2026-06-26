#!/usr/bin/env python3
"""
从文字描述自动生成小红书内容，并用 AI 图片模型直接生成宣传图。

使用方法:
    python3 scripts/generate_xhs.py "你的产品/活动/知识点描述" -o ./output
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from ai_services import chatgpt_service, volcengine_service

DEFAULT_PROVIDER = os.getenv("XHS_PROVIDER") or os.getenv("XHS_IMAGE_PROVIDER")


CONTENT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "emoji",
        "title",
        "subtitle",
        "theme",
        "visual_prompt",
        "publish_desc",
        "cards",
        "tags",
    ],
    "properties": {
        "emoji": {"type": "string"},
        "title": {"type": "string"},
        "subtitle": {"type": "string"},
        "theme": {
            "type": "string",
            "enum": [
                "default",
                "playful-geometric",
                "neo-brutalism",
                "botanical",
                "professional",
                "retro",
                "terminal",
                "sketch",
            ],
        },
        "visual_prompt": {"type": "string"},
        "publish_desc": {"type": "string"},
        "cards": {
            "type": "array",
            "minItems": 0,
            "maxItems": 8,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["heading", "body"],
                "properties": {
                    "heading": {"type": "string"},
                    "body": {"type": "array", "minItems": 2, "maxItems": 6, "items": {"type": "string"}},
                },
            },
        },
        "tags": {"type": "array", "minItems": 4, "maxItems": 10, "items": {"type": "string"}},
    },
}


def content_prompts(description: str, image_count: Optional[int] = None) -> Tuple[str, str]:
    count_instruction = ""
    if image_count == 1:
        count_instruction = "用户要单张宣传图，只生成封面所需内容，cards 返回空数组。"
    elif image_count:
        body_count = max(0, image_count - 1)
        count_instruction = f"用户要 {image_count} 张宣传图，总数包含封面；cards 生成 {body_count} 页正文卡片。"

    system_prompt = (
        "你是资深小红书内容策划和视觉总监。根据用户输入生成适合小红书图文笔记的结构化内容。"
        "标题不超过 20 个中文字符，副标题不超过 24 个中文字符。正文要口语化、信息密度高、"
        "适合生成 3:4 竖版小红书宣传图，每页不要过长。visual_prompt 必须描述最终宣传图的"
        "视觉风格、主体、构图、配色和质感，不要要求生成 logo 或水印。"
        f"{count_instruction}"
    )
    user_prompt = f"用户输入描述：\n{description.strip()}"
    return system_prompt, user_prompt


def print_generated_content(content: Dict[str, Any]) -> None:
    print("\n📝 生成内容预览")
    print(f"  Emoji：{content['emoji']}")
    print(f"  标题：{content['title']}")
    print(f"  副标题：{content['subtitle']}")
    print(f"  主题：{content['theme']}")
    print(f"  视觉提示：{content['visual_prompt']}")
    print(f"  发布文案：{content['publish_desc']}")
    print(f"  Tags：{' '.join('#' + tag.lstrip('#') for tag in content['tags'])}")
    print("  正文卡片：")
    for index, card in enumerate(content["cards"], 1):
        print(f"\n  [{index}] {card['heading']}")
        for line in card["body"]:
            print(f"      {line}")
    print()


def target_image_count(content: Dict[str, Any], image_count: Optional[int]) -> int:
    if image_count:
        return image_count
    return min(max(1, 1 + len(content.get("cards", []))), 9)


def image_jobs(content: Dict[str, Any], image_count: Optional[int]) -> List[Tuple[Path, str]]:
    total = target_image_count(content, image_count)
    jobs: List[Tuple[Path, str]] = []

    cover_prompt = (
        f"{content['visual_prompt']}\n\n"
        "Create one polished vertical Xiaohongshu/RedNote promotional poster, 3:4 ratio. "
        f"Main headline text: {content['title']}. "
        f"Subtitle text: {content['subtitle']}. "
        "Use clear, readable Chinese typography, premium social-media poster layout, no watermark, no fake UI, no QR code. "
        "The final image should be ready to publish as a promotional cover."
    )
    jobs.append((Path("cover.png"), cover_prompt))

    cards = content.get("cards", [])[: max(0, total - 1)]
    for index, card in enumerate(cards, 1):
        body = "；".join(card["body"])
        prompt = (
            f"{content['visual_prompt']}\n\n"
            "Create one polished vertical Xiaohongshu/RedNote carousel promotional image, 3:4 ratio. "
            f"Page heading text: {card['heading']}. "
            f"Body copy to include: {body}. "
            "Use clear, readable Chinese typography with strong hierarchy, premium poster composition, no watermark, no fake UI, no QR code."
        )
        jobs.append((Path(f"card_{index}.png"), prompt))

    return jobs[:total]


def normalize_provider(provider: str) -> str:
    normalized = provider.strip().lower()
    if normalized in {"volcengine", "ark", "doubao", "seedream"}:
        return "volcengine"
    if normalized in {"openai", "chatgpt", "gpt"}:
        return "openai"
    raise RuntimeError("不支持的服务提供方。可选值：openai、volcengine")


def resolve_provider(provider: Optional[str]) -> str:
    if provider:
        return normalize_provider(provider)
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    if os.getenv("ARK_API_KEY"):
        return "volcengine"
    raise RuntimeError("缺少 API Key。请配置 OPENAI_API_KEY 或 ARK_API_KEY 其中一个")


def provider_service(provider: str) -> Any:
    if provider == "volcengine":
        return volcengine_service
    return chatgpt_service


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="自动生成小红书主题、内容和 AI 宣传图")
    parser.add_argument("description", nargs="?", help="用户输入的文字描述")
    parser.add_argument("--input-file", help="从文件读取描述")
    parser.add_argument("-o", "--output-dir", default="./output", help="输出目录")
    parser.add_argument("--provider", default=DEFAULT_PROVIDER, help="服务提供方：openai/chatgpt 或 volcengine/ark；默认根据可用 Key 自动选择")
    parser.add_argument("--image-provider", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--text-model", help="内容生成模型；OpenAI 默认 gpt-5-mini，火山默认 doubao-seed-2-0-pro-260215")
    parser.add_argument("--image-size", help="宣传图尺寸；OpenAI 默认 1024x1536，火山默认 2K")
    parser.add_argument("--image-quality", choices=["low", "medium", "high", "auto"], help="OpenAI 图片质量")
    parser.add_argument("--ark-base-url", default=volcengine_service.ARK_BASE_URL, help="火山引擎 Ark OpenAI 兼容接口地址")
    parser.add_argument("--volcengine-watermark", action="store_true", default=volcengine_service.DEFAULT_WATERMARK, help="火山引擎图片生成时添加水印")
    parser.add_argument("--skip-image", action="store_true", help="不调用图片模型，只生成 manifest.json")
    parser.add_argument("--image-count", type=int, choices=range(1, 10), metavar="1-9", help="目标输出图片总数，包含封面；单张宣传图使用 1")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.input_file:
        description = Path(args.input_file).read_text(encoding="utf-8").strip()
    else:
        description = (args.description or "").strip()
    if not description:
        raise RuntimeError("请提供文字描述，或使用 --input-file 指定输入文件")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"

    provider = resolve_provider(args.provider or args.image_provider)
    service = provider_service(provider)
    client = service.create_client(args.ark_base_url) if provider == "volcengine" else service.create_client()
    text_model = args.text_model or service.DEFAULT_TEXT_MODEL
    system_prompt, user_prompt = content_prompts(description, args.image_count)

    print(f"🧠 使用 {provider}/{text_model} 生成主题和内容...")
    content = service.generate_content(client, system_prompt, user_prompt, CONTENT_SCHEMA, text_model)
    print_generated_content(content)

    if args.skip_image:
        print("🖼️ 跳过 AI 宣传图生成")
    else:
        jobs = image_jobs(content, args.image_count)
        print(f"🖼️ 使用 {provider}/{service.IMAGE_MODEL} 生成 {len(jobs)} 张宣传图...")
        generated_images = []
        for index, (relative_path, prompt) in enumerate(jobs, 1):
            output_path = output_dir / relative_path
            print(f"  生成 {index}/{len(jobs)}：{output_path.name}")
            if provider == "volcengine":
                service.generate_image(client, prompt, output_path, args.image_size, args.volcengine_watermark)
            else:
                service.generate_image(client, prompt, output_path, args.image_size, args.image_quality)
            generated_images.append(str(output_path))
        content["images"] = generated_images
        content["provider"] = provider
        content["text_model"] = text_model
        content["image_model"] = service.IMAGE_MODEL

    manifest_path.write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ 结构化内容：{manifest_path}")

    print(f"✨ 完成，输出目录：{output_dir}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ 已取消")
        sys.exit(1)
    except Exception as exc:
        print(f"\n❌ 生成失败：{exc}")
        sys.exit(1)
