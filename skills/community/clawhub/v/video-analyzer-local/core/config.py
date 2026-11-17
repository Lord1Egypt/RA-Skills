"""配置加载与管理"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

DEFAULT_CONFIG = {
    "whisper": {
        "model_name": "small",
        "language": "auto",
        "device": "cpu",
        "beam_size": 5,
        "temperature": 0.0,
    },
    "scene_detection": {
        "threshold": 0.5,
        "min_scene_duration": 2.0,
        "hist_bins": 50,
        "color_space": "hsv",
    },
    "visual_analysis": {
        "enable_scene_classification": True,
        "enable_object_detection": True,
        "enable_ocr": True,
        "scene_model_path": None,
        "object_model_path": None,
        "ocr_lang": "ch",
        "sampling_interval": 3,
    },
    "report": {
        "formats": ["html", "json", "md"],
        "enable_timeline_chart": True,
        "enable_waveform": True,
        "scenes_per_page": 20,
        "theme": "dark",
    },
    "processing": {
        "num_workers": 4,
        "keep_cache": True,
        "cache_dir": ".cache",
        "temp_dir": ".temp",
        "output_dir": "output",
        "max_duration": 7200,
        "download_timeout": 300,
    },
    "highlight": {
        "sensitivity": 0.6,
        "top_n": 10,
        "min_highlight_duration": 5,
        "audio_weight": 0.5,
        "visual_weight": 0.5,
    },
    "logging": {
        "level": "INFO",
        "format": "[%(asctime)s] %(levelname)s: %(message)s",
        "date_format": "%H:%M:%S",
    },
}


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    加载配置文件，如果不存在则使用默认配置。
    
    Args:
        config_path: YAML 配置文件路径
        
    Returns:
        配置字典
    """
    config = _deep_copy(DEFAULT_CONFIG)
    
    if config_path and os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f)
        if user_config:
            config = _deep_merge(config, user_config)
    
    return config


def _deep_copy(obj: Any) -> Any:
    """深拷贝"""
    import copy
    return copy.deepcopy(obj)


def _deep_merge(base: Dict, override: Dict) -> Dict:
    """递归合并配置字典"""
    result = _deep_copy(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = _deep_copy(value)
    return result
