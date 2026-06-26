"""
Pydantic 请求/响应模型定义
"""

from pydantic import BaseModel, Field
from typing import Optional


class EquipRequest(BaseModel):
    """配饰请求体"""
    image_url: Optional[str] = Field(
        None,
        description="原头像的公共 URL（与 image_base64 二选一）"
    )
    image_base64: Optional[str] = Field(
        None,
        description="原头像的 Base64 编码（与 image_url 二选一）"
    )
    accessory_prompt: str = Field(
        ...,
        description="期望添加的配饰描述，如 'OpenClaw lobster claw crown hat'",
        min_length=2,
        max_length=500,
    )
    preserve_style: bool = Field(
        True,
        description="是否开启全流程画风与面部保护"
    )
    negative_prompt: Optional[str] = Field(
        None,
        description="需要规避的元素，如 'neon, distorted face, low quality'",
        max_length=300,
    )


class DetectedFingerprint(BaseModel):
    """VLM 提取的视觉指纹"""
    art_style: str = Field(..., description="画风基调")
    face_angle: str = Field(..., description="面部朝向与透视")
    lighting_environment: str = Field(..., description="光影环境")
    head_top_x: float = Field(..., description="头顶中心 X 坐标（0-1 归一化）")
    head_top_y: float = Field(..., description="头顶中心 Y 坐标（0-1 归一化）")
    head_width: float = Field(..., description="头部宽度（0-1 归一化）")


class EquipMetadata(BaseModel):
    """处理元数据"""
    detected_fingerprint: DetectedFingerprint
    processing_time_ms: int


class EquipResponse(BaseModel):
    """配饰响应体"""
    status: str = Field(..., description="success | error")
    result_image_base64: Optional[str] = Field(
        None, description="处理后的高保真图片 Base64"
    )
    metadata: Optional[EquipMetadata] = None
    error_message: Optional[str] = Field(
        None, description="仅报错时返回"
    )
