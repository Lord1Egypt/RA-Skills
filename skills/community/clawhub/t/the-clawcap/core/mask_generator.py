"""
阶段二：智能保护遮罩生成

根据 VLM 提取的头顶坐标，生成黑白 Mask 图。
白色区域 = 允许重绘（帽子穿戴区）
黑色区域 = 绝对保护（面部、身体、背景）
"""

import logging
from typing import Dict, Any

import numpy as np
from PIL import Image, ImageFilter

from config import MASK_EXPAND_RATIO, MASK_FEATHER_PX

logger = logging.getLogger(__name__)


def generate_mask(
    img: Image.Image,
    fingerprint: Dict[str, Any],
) -> Image.Image:
    """
    根据 VLM 视觉指纹中的头顶坐标，生成 Inpainting 遮罩。

    算法逻辑:
    1. 以 head_top 为中心，向上方延展一个椭圆形白色区域
    2. 该区域覆盖头顶上方的"帽子穿戴空间"
    3. 使用高斯模糊对边缘进行羽化，让重绘过渡自然
    4. 图像其余部分为纯黑（绝对保护）

    Args:
        img: 原图 PIL Image
        fingerprint: VLM 返回的视觉指纹字典

    Returns:
        与原图相同尺寸的灰度 Mask 图（L 模式）
    """
    w, h = img.size

    # 从视觉指纹获取头部坐标（归一化 0-1）
    head_top_x = fingerprint["head_top_x"]
    head_top_y = fingerprint["head_top_y"]
    head_width = fingerprint["head_width"]

    # 转换为像素坐标
    cx = int(head_top_x * w)       # 头顶中心 X
    cy = int(head_top_y * h)       # 头顶 Y
    hw = int(head_width * w)       # 头部像素宽度

    # 计算帽子区域（向头顶上方延展）
    # 帽子宽度约为头部宽度的 1.2 倍
    hat_half_w = int(hw * 0.6)

    # 帽子高度 = 头部高度 * MASK_EXPAND_RATIO（向上延展）
    # 头部高度近似为头部宽度的 1.2 倍
    head_height = int(hw * 1.2)
    hat_height = int(head_height * MASK_EXPAND_RATIO)

    # 帽子区域边界
    # 上边界：从头顶向上延展 hat_height
    # 下边界：头顶位置略微往下（帽子需要"戴"在头上）
    top_y = max(0, cy - hat_height)
    bottom_y = min(h, cy + int(hw * 0.15))  # 略微覆盖头顶
    left_x = max(0, cx - hat_half_w)
    right_x = min(w, cx + hat_half_w)

    # 创建全黑 Mask
    mask = np.zeros((h, w), dtype=np.uint8)

    # 使用椭圆形渐变填充帽子区域（比矩形更自然）
    y_coords, x_coords = np.ogrid[:h, :w]

    # 椭圆中心 = 帽子区域中心
    ellipse_cx = cx
    ellipse_cy = (top_y + bottom_y) // 2
    ellipse_rx = hat_half_w  # 水平半径
    ellipse_ry = (bottom_y - top_y) // 2  # 垂直半径

    if ellipse_rx > 0 and ellipse_ry > 0:
        # 计算椭柱距离
        dist = (
            ((x_coords - ellipse_cx) / ellipse_rx) ** 2
            + ((y_coords - ellipse_cy) / ellipse_ry) ** 2
        )
        # 椭圆内部为白色
        mask[dist <= 1.0] = 255

    # 转为 PIL Image 并进行高斯羽化（平滑边缘过渡）
    mask_img = Image.fromarray(mask, mode="L")
    if MASK_FEATHER_PX > 0:
        mask_img = mask_img.filter(
            ImageFilter.GaussianBlur(radius=MASK_FEATHER_PX)
        )

    logger.info(
        f"Mask 生成完成: 帽子区域 "
        f"({left_x},{top_y})-({right_x},{bottom_y}), "
        f"椭圆中心 ({ellipse_cx},{ellipse_cy})"
    )

    return mask_img
