"""ShotGraph: declarative shot plan (camera only, no behavior directives)."""

import hashlib
import json
from typing import Dict, List, Optional
from pathlib import Path


# Forbidden fields that would violate no_scripted_plot audit dimension
FORBIDDEN_FIELDS = {
    "action", "set_needs", "move_agent", "force_event", 
    "spawn", "kill", "teleport", "script", "dialogue",
}


def _forbidden_paths(node, prefix: str = "") -> List[str]:
    """递归扫描禁止字段并返回其路径。

    只查顶层的话，`camera.action` / `overlay.script` 这类嵌套写法能直接通过校验，
    no_scripted_plot 就成了一纸空文。
    """
    found: List[str] = []
    if isinstance(node, dict):
        for key in sorted(node):
            path = f"{prefix}.{key}" if prefix else key
            if key in FORBIDDEN_FIELDS:
                found.append(path)
            found.extend(_forbidden_paths(node[key], path))
    elif isinstance(node, list):
        for i, item in enumerate(node):
            found.extend(_forbidden_paths(item, f"{prefix}[{i}]"))
    return found


class ShotGraph:
    """Declarative shot plan for video rendering."""
    
    def __init__(self, shots: List[Dict]):
        self.shots = shots
        self._validate()
    
    def _validate(self):
        """Validate that no shot contains forbidden behavior fields."""
        for i, shot in enumerate(self.shots):
            self._validate_shot(shot, i)
    
    def _validate_shot(self, shot: Dict, index: int):
        """Validate a single shot."""
        for path in _forbidden_paths(shot):
            raise ValueError(
                f"Shot {index} contains forbidden field '{path}' "
                f"(violates no_scripted_plot audit dimension)"
            )
        
        # Validate required fields
        required = ["id", "tick_from", "tick_to", "camera"]
        for req in required:
            if req not in shot:
                raise ValueError(f"Shot {index} missing required field '{req}'")
        
        # Validate camera mode
        valid_modes = {"follow", "orbit", "static", "aoi"}
        camera = shot.get("camera", {})
        if camera.get("mode") not in valid_modes:
            raise ValueError(
                f"Shot {index}: invalid camera mode '{camera.get('mode')}', "
                f"must be one of {valid_modes}"
            )
    
    def get_shots_for_tick(self, tick: int) -> List[Dict]:
        """Get all shots active at a given tick."""
        return [
            s for s in self.shots 
            if s["tick_from"] <= tick <= s["tick_to"]
        ]
    
    def hash(self) -> str:
        """Compute SHA-256 hash of the shot graph for manifest."""
        content = json.dumps(self.shots, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(content.encode()).hexdigest()
    
    @classmethod
    def from_yaml(cls, yaml_path: str) -> "ShotGraph":
        """Load ShotGraph from YAML file."""
        try:
            import yaml
        except ImportError:
            raise ImportError("PyYAML required: pip install pyyaml")
        
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        shots = data.get("shots", []) if isinstance(data, dict) else data
        return cls(shots)
    
    @classmethod
    def from_json(cls, json_path: str) -> "ShotGraph":
        """Load ShotGraph from JSON file."""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        shots = data.get("shots", []) if isinstance(data, dict) else data
        return cls(shots)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {"shots": self.shots}


def create_demo_shot_graph(ticks: int = 600) -> ShotGraph:
    """Create a demo shot graph for testing.
    
    Args:
        ticks: Total number of ticks to cover
        
    Returns:
        ShotGraph instance with a simple static camera shot
    """
    shots = [
        {
            "id": "demo-wide",
            "tick_from": 0,
            "tick_to": ticks,
            "camera": {
                "mode": "static",
                "origin": [30.0, 30.0, 50.0],  # Center of 60x60 world, elevated
                "fov": 60.0,
                "height": 50.0,
            },
            "framing": {
                "aspect": "16:9",
                "resolution": [1920, 1080],
                "fps": 30,
            },
            "tier": "R1",
            "overlay": {
                "hud": False,
                "state_panel": False,
                "caption_from": "none",
            },
        }
    ]
    return ShotGraph(shots)
