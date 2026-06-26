#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR Skill - 使用 PaddleOCR 识别图片中的文字
"""

import base64
import json
import re
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

try:
    from openai import OpenAI
except ImportError:
    print("错误: 需要安装 openai 库")
    print("运行: pip install openai")
    sys.exit(1)


def image_to_base64(image_path: str) -> str:
    """将图片文件转换为 base64 字符串"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_image_size(image_path: str) -> Tuple[int, int]:
    """获取图片尺寸"""
    from PIL import Image
    with Image.open(image_path) as img:
        return img.size


def get_mime_type(image_path: str) -> str:
    """根据文件扩展名获取 MIME 类型"""
    ext = Path(image_path).suffix.lower()
    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".bmp": "image/bmp",
        ".gif": "image/gif",
    }
    return mime_types.get(ext, "image/jpeg")


def parse_loc_tags(content: str, image_size: Tuple[int, int]) -> List[Dict[str, Any]]:
    """
    解析 PaddleOCR-VL 模型返回的 <|LOC_xxx|> 标记
    返回带真实像素坐标的文字列表

    格式: 文本<|LOC_x1|><|LOC_y1|><|LOC_x2|><|LOC_y2|><|LOC_x3|><|LOC_y3|><|LOC_x4|><|LOC_y4|>文本...

    坐标转换: LOC 是归一化值，需要乘以缩放系数得到真实像素坐标
    """
    img_width, img_height = image_size

    text_coord_pairs = re.findall(r'([^\|<]+?)((?:<\|LOC_\d+\|\>)+)', content)

    # 先扫描所有 LOC 值，找到最大值用于计算缩放系数
    all_loc_values = []
    for _, loc_tags in text_coord_pairs:
        coords = [int(c) for c in re.findall(r'LOC_(\d+)', loc_tags)]
        all_loc_values.extend(coords)

    max_loc = max(all_loc_values) if all_loc_values else 972

    # 计算缩放系数
    x_scale = img_width / max_loc if max_loc > 0 else 1
    y_scale = img_height / max_loc if max_loc > 0 else 1

    texts = []

    for text_chunk, loc_tags in text_coord_pairs:
        text = text_chunk.strip()
        if not text:
            continue

        # 提取 LOC 数值
        coord_matches = re.findall(r'LOC_(\d+)', loc_tags)
        coords = [int(c) for c in coord_matches]

        # 转换为真实像素坐标
        if len(coords) >= 8:
            # 4个点(每个点2个坐标): x1,y1,x2,y2,x3,y3,x4,y4
            box = []
            for i in range(0, 8, 2):
                x = int(coords[i] * x_scale)
                y = int(coords[i+1] * y_scale)
                box.append([x, y])
        elif len(coords) >= 4:
            # 4个值: x1,y1,x2,y2 (边界框)
            x1 = int(coords[0] * x_scale)
            y1 = int(coords[1] * y_scale)
            x2 = int(coords[2] * x_scale)
            y2 = int(coords[3] * y_scale)
            box = [
                [x1, y1],
                [x2, y1],
                [x2, y2],
                [x1, y2]
            ]
        else:
            # 没有足够坐标
            box = [[0, 0], [0, 0], [0, 0], [0, 0]]

        texts.append({
            "text": text,
            "box": box,
        })

    return texts


def ocr_image(
    image_path: str,
    api_key: str,
    model: str = "PaddlePaddle/PaddleOCR-VL-1.5",
    prompt: str = "请识别这张图片中的所有文字。",
    max_tokens: int = 2000
) -> Dict[str, Any]:
    """
    调用硅基流动平台的 OCR 模型识别图片中的文字，返回结构化数据

    Args:
        image_path: 图片文件路径
        api_key: API 密钥
        model: 使用的模型名称
        prompt: 识别提示词
        max_tokens: 最大返回 token 数

    Returns:
        Dict: {
            "image_path": str,
            "image_size": [width, height],
            "texts": List[Dict],  # 文本项列表
            "full_text": str,     # 所有文本的组合
        }
    """
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.siliconflow.cn/v1"
    )

    # 获取图片尺寸
    image_size = get_image_size(image_path)

    # 转换图片为 base64
    base64_image = image_to_base64(image_path)
    mime_type = get_mime_type(image_path)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=max_tokens
    )

    content = response.choices[0].message.content
    if not content:
        return {
            "image_path": image_path,
            "image_size": list(image_size),
            "texts": [],
            "full_text": ""
        }

    # 解析 LOC 标记，提取文本和位置信息（包含坐标转换）
    texts = parse_loc_tags(content, image_size)

    full_text = "\n".join([t.get("text", "") for t in texts])

    return {
        "image_path": image_path,
        "image_size": list(image_size),
        "texts": texts,
        "full_text": full_text
    }


def resolve_glob_pattern(pattern: str) -> List[str]:
    """解析 glob 模式返回文件列表"""
    import glob
    return glob.glob(pattern)


def get_api_key() -> Optional[str]:
    """从环境变量获取 API Key"""
    import os
    return os.environ.get("SILICONFLOW_API_KEY")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="OCR - 使用 PaddleOCR 识别图片中的文字",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Use cases:
  - 单张图片识别:
      %(prog)s ./test.jpg

  - 多张图片批处理:
      %(prog)s ./images/*.png

  - 自定义模型:
      %(prog)s -m 模型名 ./test.jpg

  - 自定义提示词:
      %(prog)s -p "请识别并翻译成英文" ./test.jpg
        """
    )

    parser.add_argument(
        "images",
        nargs="+",
        help="图片路径或 glob 模式（支持 *.jpg, *.png 等）"
    )
    parser.add_argument(
        "-k", "--api-key",
        default=None,
        help="API 密钥（默认从 SILICONFLOW_API_KEY 环境变量读取）"
    )
    parser.add_argument(
        "-m", "--model",
        default="PaddlePaddle/PaddleOCR-VL-1.5",
        help="使用的模型名称（默认: PaddlePaddle/PaddleOCR-VL-1.5）"
    )
    parser.add_argument(
        "-p", "--prompt",
        default="请识别这张图片中的所有文字。",
        help="识别提示词"
    )
    parser.add_argument(
        "-j", "--json",
        action="store_true",
        help="以 JSON 格式输出结果（便于程序解析）"
    )
    parser.add_argument(
        "-o", "--output",
        help="将结果保存到指定文件"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=2000,
        help="最大返回 token 数（默认: 2000）"
    )

    args = parser.parse_args()

    # 获取 API Key
    api_key = args.api_key or get_api_key()
    if not api_key:
        print("错误: 未提供 API Key", file=sys.stderr)
        print("请通过以下方式之一提供:", file=sys.stderr)
        print("  1. 设置环境变量: export SILICONFLOW_API_KEY=your_key", file=sys.stderr)
        print("  2. 使用 -k 参数: %(prog)s -k your_key image.png" % {"prog": parser.prog}, file=sys.stderr)
        sys.exit(1)

    # 解析图片列表
    image_files: List[str] = []
    for pattern in args.images:
        files = resolve_glob_pattern(pattern)
        if files:
            image_files.extend(files)
        else:
            # 如果 glob 没匹配到，可能是精确路径
            if Path(pattern).exists():
                image_files.append(pattern)
            else:
                print(f"警告: 未找到匹配的文件: {pattern}", file=sys.stderr)

    if not image_files:
        print("错误: 没有找到有效的图片文件", file=sys.stderr)
        sys.exit(1)

    # 处理每张图片
    results = {}
    for image_path in image_files:
        if not Path(image_path).exists():
            print(f"警告: 跳过不存在的文件: {image_path}", file=sys.stderr)
            continue

        try:
            result = ocr_image(
                image_path,
                api_key,
                model=args.model,
                prompt=args.prompt,
                max_tokens=args.max_tokens
            )

            file_name = Path(image_path).name
            results[file_name] = result

            # 输出结果
            if args.json:
                pass  # JSON 输出在最后统一处理
            else:
                print(f"--- {file_name} ---")
                print(result.get("full_text", ""))
                if result.get("texts"):
                    print(f"识别到 {len(result['texts'])} 处文字区域")
                print()

        except Exception as e:
            print(f"错误: 处理 {image_path} 时出错 - {e}", file=sys.stderr)
            results[Path(image_path).name] = {"error": str(e)}

    # JSON 输出或保存到文件
    if args.json or args.output:
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"结果已保存到: {args.output}", file=sys.stderr)
        else:
            print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
