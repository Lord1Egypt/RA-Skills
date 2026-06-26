"""
阶段三：动态重绘融合（Inpainting）

使用 Gemini Nano Banana 2 (gemini-3.1-flash-image-preview) 进行图像编辑，
在头像上自然地添加配饰。

Prompt 工程原则（遵循扩散模型最佳实践）：
1. 空间定位交给 Mask 图像，不在文本里写坐标数字
2. 只用肯定句陈述，不用 if/else 条件逻辑
3. 加入画风同化指令，防止材质与画风撕裂
4. 负面提示词不混入正向 Prompt

参考官方 API 文档：
https://ai.google.dev/gemini-api/docs/image-generation#image-editing
"""

import io
import logging
from typing import Dict, Any, Optional

from google import genai
from google.genai import types
from PIL import Image

from config import GEMINI_API_KEY, IMAGEN_MODEL

logger = logging.getLogger(__name__)


def build_inpaint_prompt(
    fingerprint: Dict[str, Any],
    accessory_prompt: str,
) -> str:
    """
    构建符合扩散模型注意力机制的正向 Prompt。

    设计原则：
    - 肯定句陈述，无条件逻辑
    - 不写数字坐标（交给 Mask 图像引导空间定位）
    - 加入画风同化指令，避免材质/画风撕裂
    - 不混入负面提示词
    """
    art_style = fingerprint['art_style']

    prompt = (
        # ── 核心动作：替换头饰 ──
        f"Equip the subject with {accessory_prompt}. "
        f"Completely cover and replace any prior headwear. "

        # ── 空间引导：交给 Mask，文本只做语义约束 ──
        f"The new headwear fits perfectly within the highlighted area shown in the mask image. "

        # ── 画风同化指令：防止材质/画风撕裂 ──
        f"Render the headwear STRICTLY in the {art_style} style. "
        f"Translate all real-world materials into their {art_style} artistic equivalents. "

        # ── 保护指令 ──
        f"Preserve the original face, expression, body, and background exactly as-is."
    )

    return prompt


async def inpaint_accessory(
    original_img: Image.Image,
    mask_img: Image.Image,
    fingerprint: Dict[str, Any],
    accessory_prompt: str,
    negative_prompt: Optional[str] = None,
) -> Image.Image:
    """
    调用 Gemini 进行图像编辑。

    发送 contents=[prompt, original_image]，
    通过 Prompt 引导模型在头顶区域渲染配饰。

    Args:
        original_img: 原始头像
        mask_img: 黑白遮罩（预留，当前未发送给 API）
        fingerprint: VLM 视觉指纹
        accessory_prompt: 用户配饰描述
        negative_prompt: 排除元素（预留）

    Returns:
        合成后的 PIL Image
    """
    client = genai.Client(api_key=GEMINI_API_KEY)

    # ── 构建正向 Prompt ──
    prompt = build_inpaint_prompt(fingerprint, accessory_prompt)
    logger.info(f"Inpainting 指令: {prompt[:200]}...")

    # ── API 调用：[prompt, 原图] ──
    try:
        response = await client.aio.models.generate_content(
            model=IMAGEN_MODEL,
            contents=[prompt, original_img],
            config=types.GenerateContentConfig(
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=True,
                ),
            ),
        )
    except Exception as e:
        logger.error(f"Gemini Inpainting API 调用失败: {e}")
        raise RuntimeError(f"Inpainting API 调用失败: {e}") from e

    # ── 从响应中提取图像 ──
    result_image = None

    if response.parts:
        for part in response.parts:
            if part.inline_data is not None:
                try:
                    result_image = Image.open(
                        io.BytesIO(part.inline_data.data)
                    )
                    logger.info(
                        f"Inpainting 完成: 输出尺寸 {result_image.size}, "
                        f"mode={result_image.mode}, "
                        f"style={fingerprint['art_style']}"
                    )
                    break
                except Exception as e:
                    logger.error(f"图像解析失败: {e}")
            elif part.text is not None:
                logger.debug(f"文本响应: {part.text[:200]}")

    if result_image is None:
        resp_text = ""
        try:
            resp_text = response.text or ""
        except Exception:
            pass
        logger.error(f"Gemini 未返回图像。响应文本: {resp_text[:300]}")
        raise RuntimeError(
            f"Inpainting 未生成图像。模型响应: {resp_text[:200]}"
        )

    # 确保 RGBA 模式
    if result_image.mode != "RGBA":
        result_image = result_image.convert("RGBA")

    return result_image
