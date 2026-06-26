"""
场景引擎 - 支持热重载
"""
import yaml
import time
from pathlib import Path
from typing import Optional, List
from src.models.scene import Scene, SceneTask


class SceneEngine:
    """场景引擎 - 支持热重载"""
    
    def __init__(self, config_path: str = None, auto_reload: bool = True, reload_interval: int = 60):
        self.scenes: dict[str, Scene] = {}
        self.config_path = config_path
        self.auto_reload = auto_reload
        self.reload_interval = reload_interval
        self._last_modified = 0
        
        if config_path:
            self.load_scenes(config_path)
    
    def load_scenes(self, config_path: str = None) -> None:
        """从 YAML 文件加载场景"""
        path = config_path or self.config_path
        if not path:
            return
        
        file_path = Path(path)
        if not file_path.exists():
            return
        
        # 检查文件修改时间
        mtime = file_path.stat().st_mtime
        if mtime == self._last_modified:
            return
        
        self._last_modified = mtime
        
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        if not data or 'scenes' not in data:
            return
        
        self.scenes.clear()
        
        for scene_id, scene_data in data['scenes'].items():
            tasks = []
            if 'tasks' in scene_data:
                for task_data in scene_data['tasks']:
                    task = SceneTask(
                        entity=task_data.get('entity', ''),
                        service=task_data.get('service', ''),
                        data=task_data.get('data', {})
                    )
                    tasks.append(task)
            
            scene = Scene(
                id=scene_id,
                name=scene_data.get('name', scene_id),
                keywords=scene_data.get('keywords', []),
                tasks=tasks,
                decision_tree=scene_data.get('decision_tree')
            )
            self.scenes[scene_id] = scene
    
    def check_reload(self) -> bool:
        """检查是否需要热重载"""
        if not self.auto_reload or not self.config_path:
            return False
        
        path = Path(self.config_path)
        if not path.exists():
            return False
        
        mtime = path.stat().st_mtime
        if mtime > self._last_modified:
            self.load_scenes()
            return True
        return False
    
    def reload_if_needed(self) -> bool:
        """如果需要则重载"""
        return self.check_reload()
    
    def get_scene(self, scene_id: str) -> Optional[Scene]:
        """获取场景（自动重载）"""
        self.reload_if_needed()
        return self.scenes.get(scene_id)
    
    def list_scenes(self) -> List[str]:
        """列出所有场景"""
        self.reload_if_needed()
        return list(self.scenes.keys())
    
    def get_all_scenes(self) -> dict[str, Scene]:
        """获取所有场景"""
        self.reload_if_needed()
        return self.scenes
