"""
core/persona_engine.py
PersonaEngine - 子代理人格赋予核心引擎
V3.0 核心模块
"""

from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import asdict
from datetime import datetime

from schemas.launch_config import (
    CompiledPersona, 
    RelationshipMode, 
    Platform,
    LaunchConfig
)
from .persona_registry import PersonaRegistry
from .session_store import SessionStore
from .prompt_compiler import PromptCompiler


class PersonaEngine:
    """
    子代理人格引擎
    
    核心职责：
    1. 加载人格定义
    2. 管理人格激活/停用
    3. 为不同平台编译人格 prompt
    4. 维护会话级人格栈
    """
    
    def __init__(
        self,
        base_dir: Optional[Path] = None,
        default_platform: Platform = Platform.OPENCLAW
    ):
        if base_dir is None:
            base_dir = Path.home() / ".xinling-bushou-v2"
        
        self.base_dir = base_dir
        self.default_platform = default_platform
        
        # 初始化子模块
        self.registry = PersonaRegistry(base_dir)
        self.session_store = SessionStore(base_dir / "sessions")
        self.prompt_compiler = PromptCompiler()
        
        # 适配器缓存（懒加载）
        self._adapters: Dict[str, Any] = {}
    
    def _get_adapter(self, platform: Platform):
        """获取平台适配器（懒加载）"""
        from adapters import AdapterRegistry
        
        platform_id = platform.value
        
        if platform_id not in self._adapters:
            adapter_class = AdapterRegistry.get(platform_id)
            self._adapters[platform_id] = adapter_class()
        
        return self._adapters[platform_id]
    
    def load_persona(self, persona_id: str) -> Dict[str, Any]:
        """
        加载人格定义
        
        Args:
            persona_id: 人格 ID
            
        Returns:
            人格定义字典
        """
        return self.registry.load_persona(persona_id)
    
    def activate_persona(
        self,
        session_id: str,
        persona_id: str,
        relationship: RelationshipMode = RelationshipMode.STACK,
        override_config: Optional[Dict[str, Any]] = None,
        base_prompt: str = ""
    ) -> CompiledPersona:
        """
        激活人格
        
        核心流程：
        1. 加载人格定义
        2. 应用 override 配置
        3. 编译人格片段
        4. 保存到会话状态
        
        Args:
            session_id: 会话 ID
            persona_id: 人格 ID
            relationship: 与主人格的关系
            override_config: 运行时覆盖配置（如 level=8）
            base_prompt: 主人格 prompt（用于 inherit 模式）
            
        Returns:
            CompiledPersona: 编译后的人格对象
        """
        # 1. 加载人格定义
        persona_def = self.load_persona(persona_id)
        
        # 2. 应用 override
        if override_config:
            persona_def = self._apply_override(persona_def, override_config)
        
        # 3. 编译人格片段
        if relationship == RelationshipMode.INHERIT and base_prompt:
            # 继承模式：base + 覆盖片段
            fragment = self.prompt_compiler.compile_inherit(
                base_prompt=base_prompt,
                persona_def=persona_def
            )
        elif relationship == RelationshipMode.STACK:
            # 叠加模式：仅人格片段
            fragment = self.prompt_compiler.compile_overlay(persona_def)
        else:
            # 独立模式：完整人格定义
            fragment = self.prompt_compiler.compile_independent(persona_def)
        
        # 4. 构建 CompiledPersona
        compiled = CompiledPersona(
            id=persona_def["meta"]["id"],
            name=persona_def["meta"]["name"],
            level=persona_def["behavior"].get("level", 5),
            mode=persona_def["behavior"].get("mode", "normal"),
            fragment=fragment,
            relationship=relationship,
            source_file=self.registry.get_persona_path(persona_id),
            metadata=persona_def.get("meta", {})
        )
        
        # 5. 更新会话状态
        self.session_store.push_persona(session_id, compiled)
        
        return compiled
    
    def deactivate_persona(self, session_id: str, persona_id: str) -> bool:
        """停用人格"""
        return self.session_store.pop_persona(session_id, persona_id)
    
    def get_active_personas(self, session_id: str) -> List[CompiledPersona]:
        """获取当前活跃人格栈"""
        return self.session_store.get_personas(session_id)
    
    def compile_for_platform(
        self,
        compiled: CompiledPersona,
        platform: Optional[Platform] = None,
        base_prompt: str = ""
    ) -> str:
        """
        为指定平台编译 prompt
        
        Args:
            compiled: 编译后的人格
            platform: 目标平台
            base_prompt: 基础 prompt（由平台适配器追加）
            
        Returns:
            平台特定格式的完整 system prompt
        """
        if platform is None:
            platform = self.default_platform
        
        adapter = self._get_adapter(platform)
        
        return adapter.compile_system_prompt(
            base_prompt=base_prompt,
            persona_fragment=compiled.fragment,
            metadata=compiled.metadata
        )
    
    def get_launch_config(
        self,
        compiled: CompiledPersona,
        platform: Optional[Platform] = None
    ) -> LaunchConfig:
        """获取平台特定的启动配置"""
        if platform is None:
            platform = self.default_platform
        
        adapter = self._get_adapter(platform)
        return adapter.get_launch_config(compiled)
    
    def _apply_override(
        self,
        persona_def: Dict[str, Any],
        override: Dict[str, Any]
    ) -> Dict[str, Any]:
        """应用 override 配置到人格定义"""
        import copy
        result = copy.deepcopy(persona_def)
        
        # 深度合并 behavior
        if "behavior" in override:
            for key, value in override["behavior"].items():
                if key in result.get("behavior", {}):
                    if isinstance(value, dict):
                        result["behavior"][key].update(value)
                    else:
                        result["behavior"][key] = value
                else:
                    result["behavior"][key] = value
        
        # 直接覆盖顶层字段
        for key, value in override.items():
            if key != "behavior" and key in result:
                if isinstance(result[key], dict) and isinstance(value, dict):
                    result[key].update(value)
                else:
                    result[key] = value
            elif key not in result:
                result[key] = value
        
        return result
    
    def list_personas(self) -> List[str]:
        """列出所有已注册的人格"""
        return self.registry.list_personas()
    
    def get_persona_info(self, persona_id: str) -> Optional[Dict[str, Any]]:
        """获取人格元信息"""
        return self.registry.get_persona_info(persona_id)
