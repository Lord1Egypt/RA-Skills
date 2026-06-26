"""
The ClawCap — MCP Server 入口

Claude 标准 Skill 接口。通过 MCP 协议让 Claude 直接调用
头像配饰合成能力（VLM 指纹 → Mask → Inpainting）。

启动方式：
  python mcp_server.py          # 直接运行（stdio 模式）
  uv run mcp dev mcp_server.py  # 开发调试（Inspector）
"""

import io
import re
import logging
import base64

from mcp.server.fastmcp import FastMCP, Image

from core.vision_fingerprint import extract_fingerprint
from core.mask_generator import generate_mask
from core.inpainter import inpaint_accessory
from utils.image_utils import (
    load_image_from_base64,
    validate_image,
    resize_for_processing,
)
from config import GEMINI_API_KEY

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── 内容安全过滤 ──
BANNED_PATTERN = re.compile(
    r"(nude|naked|nsfw|porn|weapon|blood|gore|drug|kill|terror)",
    re.IGNORECASE,
)

# ── MCP Server ──
mcp = FastMCP(
    "The ClawCap",
    instructions=(
        "你是 The ClawCap（龙虾脑控帽）视觉配饰引擎。"
        "当用户要求给头像添加帽子或配饰时，调用 equip_avatar_accessory 工具。"
        "将用户的口语请求翻译为精准的英文视觉描述作为 accessory_prompt。"
        "例如：用户说'加个龙虾帽' → accessory_prompt='a red beanie hat with two curved red lobster pincers sticking up from the top'。"
    ),
)


@mcp.tool()
async def equip_avatar_accessory(
    image_base64: str,
    accessory_prompt: str,
    negative_prompt: str = "distorted face, low quality, blurry",
) -> Image:
    """
    为头像无损添加配饰（帽子/头饰）。

    AI 自动分析原图画风、光影、角度，生成完美融合的配饰。
    绝不改变原图的面部特征、背景和构图。

    Args:
        image_base64: 用户头像的 Base64 编码（PNG/JPG）
        accessory_prompt: 配饰的纯视觉英文描述。必须是客观的外观描述，
            例如 'a red beanie hat with two curved red lobster pincers'
        negative_prompt: 需要规避的视觉元素
    """
    # ── 启动校验 ──
    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY 未配置。请在环境变量或 .env 文件中设置。"
        )

    if BANNED_PATTERN.search(accessory_prompt):
        raise ValueError("accessory_prompt 包含违规内容，请修正后重试。")

    if BANNED_PATTERN.search(negative_prompt):
        raise ValueError("negative_prompt 包含违规内容。")

    # ── 加载图像 ──
    logger.info("MCP | 加载用户头像...")
    img = load_image_from_base64(image_base64)
    validate_image(img)
    original_size = img.size
    img = resize_for_processing(img)

    # ── 阶段一：VLM 视觉指纹提取 ──
    logger.info("MCP | 阶段一：提取视觉指纹...")
    fingerprint = await extract_fingerprint(img)

    # ── 阶段二：Mask 遮罩生成 ──
    logger.info("MCP | 阶段二：生成智能遮罩...")
    mask_img = generate_mask(img, fingerprint)

    # ── 阶段三：Inpainting 重绘 ──
    logger.info("MCP | 阶段三：注入龙虾寄生体...")
    result_img = await inpaint_accessory(
        original_img=img,
        mask_img=mask_img,
        fingerprint=fingerprint,
        accessory_prompt=accessory_prompt,
        negative_prompt=negative_prompt,
    )

    # ── 后处理：缩放回原始尺寸 ──
    if result_img.size != original_size:
        from PIL import Image as PILImage
        result_img = result_img.resize(
            original_size, PILImage.Resampling.LANCZOS
        )

    # ── 导出为 PNG bytes ──
    buf = io.BytesIO()
    result_img.save(buf, format="PNG")
    png_bytes = buf.getvalue()

    logger.info(f"MCP | 完成！输出 {len(png_bytes)} bytes")
    return Image(data=png_bytes, format="png")


if __name__ == "__main__":
    mcp.run()
