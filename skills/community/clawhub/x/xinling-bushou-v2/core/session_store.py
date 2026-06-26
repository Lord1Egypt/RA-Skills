"""
core/session_store.py
SessionStore - 会话级人格栈持久化
"""

import json
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from schemas.launch_config import CompiledPersona, RelationshipMode


class SessionStore:
    """会话存储 - 管理会话级活跃人格栈"""
    
    def __init__(self, sessions_dir: Path):
        self.sessions_dir = sessions_dir
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self._active_sessions: Dict[str, Dict[str, Any]] = {}
    
    def _get_session_file(self, session_id: str) -> Path:
        """获取会话文件路径"""
        return self.sessions_dir / f"session_{session_id}.json"
    
    def _load_session(self, session_id: str) -> Dict[str, Any]:
        """加载会话数据"""
        session_file = self._get_session_file(session_id)
        
        if session_file.exists():
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
        
        # 默认空会话
        return {
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
            "main_persona": None,
            "overlay_stack": []
        }
    
    def _save_session(self, session_id: str, data: Dict[str, Any]) -> None:
        """保存会话数据"""
        session_file = self._get_session_file(session_id)
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def create_session(self, session_id: Optional[str] = None) -> str:
        """
        创建新会话
        
        Args:
            session_id: 指定会话 ID，None 则自动生成
            
        Returns:
            会话 ID
        """
        if session_id is None:
            session_id = str(uuid.uuid4())[:8]
        
        data = {
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
            "main_persona": None,
            "overlay_stack": []
        }
        
        self._save_session(session_id, data)
        self._active_sessions[session_id] = data
        
        return session_id
    
    def push_persona(
        self,
        session_id: str,
        persona: CompiledPersona
    ) -> bool:
        """
        将人格推入会话栈
        
        Args:
            session_id: 会话 ID
            persona: 编译后的人格
            
        Returns:
            是否成功
        """
        data = self._load_session(session_id)
        
        # 检查是否已存在
        for i, entry in enumerate(data["overlay_stack"]):
            if entry["persona_id"] == persona.id:
                # 更新现有条目
                data["overlay_stack"][i] = {
                    "persona_id": persona.id,
                    "name": persona.name,
                    "level": persona.level,
                    "mode": persona.mode,
                    "relationship": persona.relationship.value,
                    "activated_at": datetime.now().isoformat(),
                    "source": str(persona.source_file) if persona.source_file else None
                }
                self._save_session(session_id, data)
                return True
        
        # 新增条目
        data["overlay_stack"].append({
            "persona_id": persona.id,
            "name": persona.name,
            "level": persona.level,
            "mode": persona.mode,
            "relationship": persona.relationship.value,
            "activated_at": datetime.now().isoformat(),
            "source": str(persona.source_file) if persona.source_file else None
        })
        
        self._save_session(session_id, data)
        return True
    
    def pop_persona(self, session_id: str, persona_id: str) -> bool:
        """
        从会话栈中移除人格
        
        Args:
            session_id: 会话 ID
            persona_id: 人格 ID
            
        Returns:
            是否成功
        """
        data = self._load_session(session_id)
        
        original_len = len(data["overlay_stack"])
        data["overlay_stack"] = [
            p for p in data["overlay_stack"]
            if p["persona_id"] != persona_id
        ]
        
        if len(data["overlay_stack"]) < original_len:
            self._save_session(session_id, data)
            return True
        
        return False
    
    def get_personas(self, session_id: str) -> List[CompiledPersona]:
        """
        获取会话中的所有活跃人格
        
        Args:
            session_id: 会话 ID
            
        Returns:
            CompiledPersona 列表
        """
        data = self._load_session(session_id)
        
        personas = []
        for entry in data.get("overlay_stack", []):
            try:
                personas.append(CompiledPersona(
                    id=entry["persona_id"],
                    name=entry["name"],
                    level=entry.get("level", 5),
                    mode=entry.get("mode", "normal"),
                    fragment="",  # session store 不存储 fragment
                    relationship=RelationshipMode(entry.get("relationship", "stack")),
                    source_file=Path(entry["source"]) if entry.get("source") else None,
                    metadata={}
                ))
            except (KeyError, ValueError):
                continue
        
        return personas
    
    def set_main_persona(
        self,
        session_id: str,
        persona_id: str,
        name: str,
        source: str
    ) -> None:
        """设置主（继承）人格"""
        data = self._load_session(session_id)
        data["main_persona"] = {
            "id": persona_id,
            "name": name,
            "source": source
        }
        self._save_session(session_id, data)
    
    def delete_session(self, session_id: str) -> bool:
        """删除会话"""
        session_file = self._get_session_file(session_id)
        if session_file.exists():
            session_file.unlink()
            return True
        return False
    
    def list_sessions(self) -> List[str]:
        """列出所有会话 ID"""
        return [
            f.stem.replace("session_", "")
            for f in self.sessions_dir.glob("session_*.json")
        ]
