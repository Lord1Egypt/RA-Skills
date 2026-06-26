import yaml
from pathlib import Path
from typing import Dict, Any


def load_settings(config_path: Path) -> Dict[str, Any]:
    if not config_path.exists():
        return {}
        
    with open(config_path, 'r', encoding='utf-8') as f:
        settings = yaml.safe_load(f)
        
    return settings or {}


def interpolate_path(path_template: str, **kwargs) -> str:
    return path_template.format(**kwargs)
