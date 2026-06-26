"""
API 路由定义

POST /api/skill/alpha-equip  — 头像配饰合成主接口
GET  /api/health              — 健康检查
"""

import logging
import time
import re

from fastapi import APIRouter, HTTPException, Request
from PIL import Image as PILImage
from slowapi import Limiter
from slowapi.util import get_remote_address

from api.schemas import (
    EquipRequest, EquipResponse, EquipMetadata, DetectedFingerprint,
)
from core.vision_fingerprint import extract_fingerprint
from core.mask_generator import generate_mask
from core.inpainter import inpaint_accessory
from utils.image_utils import (
    load_image_from_url, load_image_from_base64,
    validate_image, image_to_base64, resize_for_processing,
)
from config import API_TIMEOUT_MS

logger = logging.getLogger(__name__)

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

# 内容安全：敏感词正则过滤
BANNED_PATTERN = re.compile(
    r"(nude|naked|nsfw|porn|weapon|blood|gore|drug|kill|terror)",
    re.IGNORECASE,
)


@router.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "service": "alpha-avatar-equip"}


@router.post("/api/skill/alpha-equip", response_model=EquipResponse)
@limiter.limit("3/minute")
async def alpha_equip(request: Request, req: EquipRequest):
    """
    头像配饰合成主接口。

    三阶段漏斗：
    1. VLM 视觉指纹提取
    2. 智能 Mask 遮罩生成
    3. Inpainting 动态重绘
    """
    start_time = time.time()

    # ── 输入校验 ──────────────────────────────────────────
    if not req.image_url and not req.image_base64:
        raise HTTPException(
            status_code=400,
            detail="必须提供 image_url 或 image_base64 其中之一",
        )

    # 内容安全过滤
    if BANNED_PATTERN.search(req.accessory_prompt):
        raise HTTPException(
            status_code=400,
            detail="accessory_prompt 包含违规内容，请修正后重试",
        )
    if req.negative_prompt and BANNED_PATTERN.search(req.negative_prompt):
        raise HTTPException(
            status_code=400,
            detail="negative_prompt 包含违规内容",
        )

    # ── 加载图像 ──────────────────────────────────────────
    try:
        if req.image_base64:
            img = load_image_from_base64(req.image_base64)
        else:
            img = await load_image_from_url(req.image_url)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"图像加载失败: {e}",
        )

    # 校验尺寸
    try:
        validate_image(img)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 保存原始尺寸，用于最终输出缩放
    original_size = img.size
    logger.info(f"原始输入尺寸: {original_size}")

    # 缩放到适合处理的尺寸
    img = resize_for_processing(img)

    # ── 阶段一：VLM 视觉指纹提取 ─────────────────────────
    try:
        fingerprint = await extract_fingerprint(img)
    except ValueError as e:
        # 未检测到有效目标
        return EquipResponse(
            status="error",
            error_message=str(e),
        )
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    # ── 阶段二：Mask 遮罩生成 ────────────────────────────
    try:
        mask_img = generate_mask(img, fingerprint)
    except Exception as e:
        logger.error(f"Mask 生成失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Mask 生成失败: {e}",
        )

    # ── 阶段三：Inpainting 重绘 ──────────────────────────
    try:
        result_img = await inpaint_accessory(
            original_img=img,
            mask_img=mask_img,
            fingerprint=fingerprint,
            accessory_prompt=req.accessory_prompt,
            negative_prompt=req.negative_prompt,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    # ── 后处理：缩放回原始输入尺寸 ────────────────────────
    if result_img.size != original_size:
        logger.info(
            f"缩放输出: {result_img.size} → {original_size}"
        )
        result_img = result_img.resize(
            original_size, PILImage.Resampling.LANCZOS
        )

    # ── 构建响应 ─────────────────────────────────────────
    elapsed_ms = int((time.time() - start_time) * 1000)

    # 超时检查（记录但不阻断，因为图已经生成了）
    if elapsed_ms > API_TIMEOUT_MS:
        logger.warning(
            f"全流程耗时 {elapsed_ms}ms 超出阈值 {API_TIMEOUT_MS}ms"
        )

    result_b64 = image_to_base64(result_img, fmt="PNG")

    return EquipResponse(
        status="success",
        result_image_base64=result_b64,
        metadata=EquipMetadata(
            detected_fingerprint=DetectedFingerprint(
                art_style=fingerprint["art_style"],
                face_angle=fingerprint["face_angle"],
                lighting_environment=fingerprint["lighting_environment"],
                head_top_x=fingerprint["head_top_x"],
                head_top_y=fingerprint["head_top_y"],
                head_width=fingerprint["head_width"],
            ),
            processing_time_ms=elapsed_ms,
        ),
    )
