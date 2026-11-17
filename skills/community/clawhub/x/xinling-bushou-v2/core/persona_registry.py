"""
core/persona_registry.py
PersonaRegistry - 人格注册表，管理所有已安装的人格
"""

import json
import copy
from pathlib import Path
from typing import Dict, List, Optional, Any

from .security import (
    resolve_child_path,
    validate_bounded_data,
    validate_identifier,
)


class PersonaRegistry:
    """人格注册表"""
    
    REGISTRY_FILE = "personas/_registry.json"
    
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir).expanduser().resolve()
        self.registry_file = self.base_dir / self.REGISTRY_FILE
        self._ensure_registry()
    
    def _ensure_registry(self) -> None:
        """确保注册表文件存在"""
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
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
        persona_ids = []
        for persona_id in registry.get("personas", {}):
            try:
                validate_identifier(persona_id, "persona_id")
            except ValueError:
                continue
            persona_ids.append(persona_id)
        return persona_ids
    
    def get_persona_info(self, persona_id: str) -> Optional[Dict[str, Any]]:
        """获取人格元信息"""
        validate_identifier(persona_id, "persona_id")
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
        validate_identifier(persona_id, "persona_id")
        persona_path, registry_file = self._normalize_persona_file_path(file_path)
        if persona_path.suffix.lower() != ".json":
            raise ValueError("persona file must be a JSON file")

        registry = self._load_registry()
        
        registry["personas"][persona_id] = {
            "file": registry_file,
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
        validate_identifier(persona_id, "persona_id")
        registry = self._load_registry()
        
        if persona_id in registry.get("personas", {}):
            del registry["personas"][persona_id]
            self._save_registry(registry)
            return True
        
        return False
    
    def get_persona_path(self, persona_id: str) -> Optional[Path]:
        """获取人格定义文件的绝对路径"""
        validate_identifier(persona_id, "persona_id")
        info = self.get_persona_info(persona_id)
        if info:
            path, _ = self._normalize_persona_file_path(info.get("file"))
            if path.suffix.lower() != ".json":
                raise ValueError("persona registry path must be a JSON file")
            return path
        return None

    def _normalize_persona_file_path(self, file_path: str) -> tuple[Path, str]:
        if not isinstance(file_path, str) or not file_path:
            raise ValueError("persona file must be a non-empty relative path")
        raw_path = Path(file_path)
        if raw_path.parts and raw_path.parts[0].lower() == "personas":
            raw_path = Path(*raw_path.parts[1:])
        path = resolve_child_path(
            self.base_dir / "personas",
            raw_path.as_posix(),
            "persona file",
        )
        return path, f"personas/{raw_path.as_posix()}"
    
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
            persona = json.load(f)
        validate_bounded_data(persona, "persona")
        if not isinstance(persona, dict):
            raise ValueError("persona definition must be a JSON object")
        return persona

    def normalize_persona(self, persona_id: str, persona: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize legacy and current persona files into a safe runtime shape."""
        validate_identifier(persona_id, "persona_id")
        validate_bounded_data(persona, "persona")
        result = copy.deepcopy(persona)

        if "meta" not in result:
            result = {
                "meta": {
                    "id": persona_id,
                    "name": result.get("display_name") or result.get("name") or persona_id,
                    "version": "4.0.0",
                    "author": "ace",
                    "description": result.get("style_description", ""),
                    "tags": ["personality"],
                    "compatible_with": ["generic", "openclaw"],
                },
                "identity": {
                    "role": result.get("identity", "persona"),
                    "pronouns": {
                        "first_person": result.get("pronouns", {})
                        .get("male_user", {})
                        .get("first_person", "I"),
                        "second_person": result.get("pronouns", {})
                        .get("male_user", {})
                        .get("second_person", "you"),
                    },
                    "identity_statements": result.get("identity_statements", {}),
                },
                "behavior": {
                    "level": 5,
                    "tone": result.get("tone", "calm"),
                    "mode": "explicit",
                    "activation": {
                        "enabled": False,
                        "trigger_keywords": [],
                        "always_on": False,
                        "auto_activate": False,
                        "emotion_sensing": False,
                    },
                },
                "phrases": {
                    "seeds": {
                        key: {"default": values}
                        for key, values in result.get("sample_lines_by_level", {}).items()
                        if isinstance(values, list)
                    }
                },
            }
        else:
            result.setdefault("meta", {})
            result["meta"]["id"] = persona_id
            result.setdefault("behavior", {})
            result["behavior"].setdefault("activation", {})
            result["behavior"]["activation"].update(
                {
                    "enabled": False,
                    "trigger_keywords": [],
                    "always_on": False,
                    "auto_activate": False,
                    "emotion_sensing": False,
                }
            )

        meta = result.get("meta", {})
        if not isinstance(meta.get("name"), str) or not meta["name"].strip():
            raise ValueError("persona meta.name must be a non-empty string")
        level = result.get("behavior", {}).get("level", 5)
        if not isinstance(level, int) or not 1 <= level <= 10:
            raise ValueError("persona behavior.level must be an integer from 1 to 10")
        return result
    
    def reload(self) -> None:
        """重新加载注册表（用于外部修改后）"""
        pass  # 每次操作都重新读取文件，无需额外操作
