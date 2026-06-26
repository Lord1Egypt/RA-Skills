"""
阶段一：VLM 视觉指纹提取

使用 Gemini Flash 分析头像，提取画风、角度、光照环境，
以及头顶区域的归一化坐标（用于阶段二 Mask 生成）。
"""

import json
import logging
from typing import Dict, Any

from google import genai
from google.genai import types
from PIL import Image

from config import GEMINI_API_KEY, VLM_MODEL
from utils.image_utils import image_to_bytes

logger = logging.getLogger(__name__)

# 强约束 Prompt，强制返回 JSON
VLM_PROMPT = """You are a precision image analysis system. Analyze this avatar image and extract the following information.

RULES:
1. Return ONLY valid JSON, no markdown, no explanation, no extra text.
2. All coordinate values must be normalized to 0.0-1.0 range (relative to image width/height).
3. "head_top_x" is the X center of the top of the head/hair.
4. "head_top_y" is the Y coordinate of the very top of the head/hair (0=top of image, 1=bottom).
5. "head_width" is the approximate width of the head relative to image width.
6. If no clear head/face is detected, set all coordinates to -1.

Return this exact JSON structure:
{
  "art_style": "<one of: photorealistic, semi-realistic, flat anime illustration, detailed anime, 3d render, pixel art, cartoon, watercolor, oil painting, sketch, vector art, nft collectible, chibi>",
  "face_angle": "<one of: front-facing, 3/4 profile looking left, 3/4 profile looking right, side profile left, side profile right, looking up, looking down>",
  "lighting_environment": "<brief description, e.g.: studio soft light, harsh neon from left, flat shading no shadows, warm sunset backlight>",
  "head_top_x": <float 0.0-1.0>,
  "head_top_y": <float 0.0-1.0>,
  "head_width": <float 0.0-1.0>
}"""


async def extract_fingerprint(img: Image.Image) -> Dict[str, Any]:
    """
    调用 Gemini Flash VLM 提取图像视觉指纹。

    Returns:
        包含 art_style, face_angle, lighting_environment,
        head_top_x, head_top_y, head_width 的字典。

    Raises:
        ValueError: 未检测到有效目标
        RuntimeError: API 调用失败
    """
    client = genai.Client(api_key=GEMINI_API_KEY)

    image_bytes = image_to_bytes(img, fmt="PNG")

    try:
        response = await client.aio.models.generate_content(
            model=VLM_MODEL,
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
                types.Part.from_text(text=VLM_PROMPT),
            ],
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=500,
            ),
        )
    except Exception as e:
        logger.error(f"Gemini VLM API 调用失败: {e}")
        raise RuntimeError(f"VLM API 调用失败: {e}") from e

    # 解析 JSON 响应
    raw_text = response.text.strip()

    # 清理可能的 markdown 代码块包裹
    if raw_text.startswith("```"):
        lines = raw_text.split("\n")
        # 移除首尾的 ``` 行
        lines = [l for l in lines if not l.strip().startswith("```")]
        raw_text = "\n".join(lines)

    try:
        result = json.loads(raw_text)
    except json.JSONDecodeError as e:
        logger.error(f"VLM 返回的 JSON 解析失败: {raw_text}")
        raise RuntimeError(f"VLM 返回格式异常，无法解析: {e}") from e

    # 校验必要字段
    required_keys = [
        "art_style", "face_angle", "lighting_environment",
        "head_top_x", "head_top_y", "head_width"
    ]
    for key in required_keys:
        if key not in result:
            raise RuntimeError(f"VLM 返回缺少字段: {key}")

    # 校验是否检测到有效目标
    if result["head_top_x"] < 0 or result["head_top_y"] < 0:
        raise ValueError(
            "Error: Single valid subject required. "
            "未检测到明确的头部/人脸特征，请提供包含清晰头像的图片。"
        )

    logger.info(
        f"视觉指纹提取完成: style={result['art_style']}, "
        f"angle={result['face_angle']}, "
        f"head_top=({result['head_top_x']:.2f}, {result['head_top_y']:.2f})"
    )

    return result
