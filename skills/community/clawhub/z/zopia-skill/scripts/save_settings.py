#!/usr/bin/env python3
"""保存或查询 Zopia 项目设置。

用法:
    # 查询设置
    python save_settings.py --base-id BASE_ID --get

    # 保存设置
    python save_settings.py --base-id BASE_ID --locale zh-CN --aspect-ratio 16:9 --style anime

支持的设置字段:
    --locale                  语言 (zh-CN, en, ja)
    --aspect-ratio            画面比例 (16:9, 9:16)
    --style                   视觉风格
    --video-model             视频模型
    --generation-method       生成方式
    --image-size              图片尺寸
    --video-resolution        视频分辨率
    --storyboard-image-model  分镜图模型
    --entity-image-model      角色场景图模型
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _common import get_settings, print_json, save_settings


def main() -> None:
    parser = argparse.ArgumentParser(description="保存或查询 Zopia 项目设置")
    parser.add_argument("--base-id", required=True, help="项目 ID")
    parser.add_argument("--get", action="store_true", help="查询当前设置")

    parser.add_argument("--locale", help="语言 (zh-CN, en, ja)")
    parser.add_argument("--aspect-ratio", help="画面比例 (16:9, 9:16)")
    parser.add_argument("--style", help="视觉风格")
    parser.add_argument("--video-model", help="视频模型")
    parser.add_argument("--generation-method", help="生成方式")
    parser.add_argument("--image-size", help="图片尺寸")
    parser.add_argument("--video-resolution", help="视频分辨率")
    parser.add_argument("--storyboard-image-model", help="分镜图模型")
    parser.add_argument("--entity-image-model", help="角色场景图模型")
    args = parser.parse_args()

    if args.get:
        result = get_settings(args.base_id)
        print_json(result)
        return

    settings: dict[str, str] = {}
    field_map = {
        "locale": args.locale,
        "aspect_ratio": args.aspect_ratio,
        "style": args.style,
        "video_model": args.video_model,
        "generation_method": args.generation_method,
        "image_size": args.image_size,
        "video_resolution": args.video_resolution,
        "storyboard_image_model": args.storyboard_image_model,
        "entity_image_model": args.entity_image_model,
    }
    for key, value in field_map.items():
        if value is not None:
            settings[key] = value

    if not settings:
        print("错误: 至少需要指定一个设置字段", file=sys.stderr)
        sys.exit(1)

    result = save_settings(args.base_id, settings)
    print_json(result)


if __name__ == "__main__":
    main()
