#!/usr/bin/env python3
"""
场景配置模块 - 统一管理图像增强场景的配置
"""
from typing import Dict, List


# 场景配置映射表
# key: 场景名
# value: 包含 data_type 的配置字典
# 仅保留图像增强相关场景，已移除 OCR、文档转换、AIGC 场景
SCENE_CONFIGS: Dict[str, Dict[str, str]] = {
    # ==================== 图像增强类 ====================
    "exam-enhance": {
        "data_type": "image",
    },
    "image-hd-enhance": {
        "data_type": "image",
    },
    "certificate-enhance": {
        "data_type": "image",
    },
    "remove-handwriting": {
        "data_type": "image",
    },
    "remove-watermark": {
        "data_type": "image",
    },
    "remove-shadow": {
        "data_type": "image",
    },
    "remove-screen-pattern": {
        "data_type": "image",
    },
    "remove-background-color": {
        "data_type": "image",
    },
    "image-crop-rectify": {
        "data_type": "image",
    },
    "sketch-drawing": {
        "data_type": "image",
    },
    "extract-lineart": {
        "data_type": "image",
    },
    "scan-document": {
        "data_type": "image",
    },
    "scan-contract": {
        "data_type": "image",
    },
}


def get_scene_config(scene_name: str) -> Dict[str, str]:
    """
    根据场景名获取配置
    
    Args:
        scene_name: 场景名称（如 'exam-enhance', 'image-hd-enhance' 等）
    
    Returns:
        包含 data_type 的字典
    
    Raises:
        ValueError: 场景名不存在时抛出
    """
    if scene_name not in SCENE_CONFIGS:
        available = ", ".join(sorted(SCENE_CONFIGS.keys()))
        raise ValueError(
            f"Unknown scene: '{scene_name}'. "
            f"Available scenes: {available}"
        )
    return SCENE_CONFIGS[scene_name]


def list_scenes() -> List[str]:
    """
    获取所有可用场景名列表
    
    Returns:
        场景名列表（已排序）
    """
    return sorted(SCENE_CONFIGS.keys())
