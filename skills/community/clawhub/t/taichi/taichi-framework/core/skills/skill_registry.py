import yaml
from typing import Dict, Optional, Any


class SkillRegistry:
    """Registry of available skills loaded from manifest.yaml."""

    def __init__(self, manifest_path: str):
        with open(manifest_path) as f:
            data = yaml.safe_load(f)
        self.skills: Dict[str, Dict[str, Any]] = {s["name"]: s for s in data.get("skills", [])}

    def get(self, name: str) -> Optional[Dict[str, Any]]:
        return self.skills.get(name)

    def list_all(self):
        return list(self.skills.keys())
