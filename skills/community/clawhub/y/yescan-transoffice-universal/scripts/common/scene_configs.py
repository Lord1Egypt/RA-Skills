#!/usr/bin/env python3
"""
场景配置模块 - 管理文档转换场景的配置
"""
from typing import Dict, List


# 场景配置映射表
# key: 场景名
# value: 包含 data_type 的配置字典
SCENE_CONFIGS: Dict[str, Dict[str, str]] = {
    # ==================== 文档转换类 ====================
    "image-to-excel": {
        "data_type": "image",
    },
    "image-to-word": {
        "data_type": "image",
    },
    "image-to-pdf": {
        "data_type": "image",
    },
}


def get_scene_config(scene_name: str) -> Dict[str, str]:
    """
    根据场景名获取配置
    
    Args:
        scene_name: 场景名称（如 'image-to-word', 'image-to-excel' 等）
    
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
