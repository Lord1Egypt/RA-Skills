"""
core/persona_registry.py
PersonaRegistry - 人格注册表，管理所有已安装的人格
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any


class PersonaRegistry:
    """人格注册表"""
    
    REGISTRY_FILE = "personas/_registry.json"
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.registry_file = base_dir / self.REGISTRY_FILE
        self._ensure_registry()
    
    def _ensure_registry(self) -> None:
        """确保注册表文件存在"""
        if not self.registry_file.exists():
            self.base_dir.mkdir(parents=True, exist_ok=True)
            self._create_default_registry()
    
    def _create_default_registry(self) -> None:
        """创建默认注册表"""
        registry = {
            "version": "2.0.0",
            "personas": {}
        }
        with open(self.registry_file, 'w', encoding='utf-8') as f:
            json.dump(registry, f, ensure_ascii=False, indent=2)
    
    def _load_registry(self) -> Dict[str, Any]:
        """加载注册表"""
        try:
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"version": "2.0.0", "personas": {}}
    
    def _save_registry(self, registry: Dict[str, Any]) -> None:
        """保存注册表"""
        with open(self.registry_file, 'w', encoding='utf-8') as f:
            json.dump(registry, f, ensure_ascii=False, indent=2)
    
    def list_personas(self) -> List[str]:
        """列出所有已注册的人格 ID"""
        registry = self._load_registry()
        return list(registry.get("personas", {}).keys())
    
    def get_persona_info(self, persona_id: str) -> Optional[Dict[str, Any]]:
        """获取人格元信息"""
        registry = self._load_registry()
        return registry.get("personas", {}).get(persona_id)
    
    def register_persona(
        self,
        persona_id: str,
        file_path: str,
        name: str,
        description: str = "",
        tags: Optional[List[str]] = None,
        compatible_with: Optional[List[str]] = None,
        version: str = "1.0.0",
        author: str = "unknown"
    ) -> bool:
        """
        注册新人格
        
        Args:
            persona_id: 人格 ID
            file_path: 人格定义文件路径（相对于 personas/）
            name: 显示名称
            description: 描述
            tags: 标签
            compatible_with: 兼容平台列表
            version: 版本
            author: 作者
            
        Returns:
            是否注册成功
        """
        registry = self._load_registry()
        
        registry["personas"][persona_id] = {
            "file": file_path,
            "name": name,
            "description": description,
            "tags": tags or [],
            "compatible_with": compatible_with or ["generic"],
            "version": version,
            "author": author
        }
        
        self._save_registry(registry)
        return True
    
    def unregister_persona(self, persona_id: str) -> bool:
        """注销人格"""
        registry = self._load_registry()
        
        if persona_id in registry.get("personas", {}):
            del registry["personas"][persona_id]
            self._save_registry(registry)
            return True
        
        return False
    
    def get_persona_path(self, persona_id: str) -> Optional[Path]:
        """获取人格定义文件的绝对路径"""
        info = self.get_persona_info(persona_id)
        if info:
            return self.base_dir / info["file"]
        return None
    
    def load_persona(self, persona_id: str) -> Dict[str, Any]:
        """
        加载完整的人格定义
        
        Args:
            persona_id: 人格 ID
            
        Returns:
            人格定义字典
            
        Raises:
            FileNotFoundError: 人格文件不存在
            json.JSONDecodeError: 人格文件格式错误
        """
        persona_path = self.get_persona_path(persona_id)
        
        if persona_path is None:
            raise FileNotFoundError(f"Persona '{persona_id}' not found in registry")
        
        if not persona_path.exists():
            raise FileNotFoundError(f"Persona file not found: {persona_path}")
        
        with open(persona_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def reload(self) -> None:
        """重新加载注册表（用于外部修改后）"""
        pass  # 每次操作都重新读取文件，无需额外操作
