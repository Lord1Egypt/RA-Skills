"""
adapters/cursor.py
Cursor IDE 平台适配器
"""

from typing import Dict, Any

from schemas.launch_config import Platform, LaunchConfig, CompiledPersona
from .base import PlatformAdapter


class CursorAdapter(PlatformAdapter):
    """Cursor IDE 适配器
    
    Cursor 特点：
    - Tab 分裂可类比 subagent
    - 通过 .cursor/rules/ 目录注入规则
    - .cursorrules 是全局规则文件
    """
    
    PLATFORM_ID = "cursor"
    
    def get_platform_id(self) -> str:
        return self.PLATFORM_ID
    
    def supports_subagent(self) -> bool:
        return True  # Cursor Tab 分裂可类比
    
    def compile_system_prompt(
        self,
        base_prompt: str,
        persona_fragment: str,
        metadata: Dict[str, Any]
    ) -> str:
        """Return an optional style fragment for the selected session."""
        return persona_fragment  # 仅人格片段，base 由 .cursorrules 提供
    
    def get_launch_config(self, persona: CompiledPersona) -> LaunchConfig:
        """Return a user-selected rule artifact without automatic activation."""
        rules_content = self._generate_cursorrules(persona)
        
        return LaunchConfig(
            extra_system_content=persona.fragment,
            config_file={
                "path": f".cursor/rules/xinling-{persona.id}.md",
                "content": rules_content
            },
            metadata={
                "source": "xinling-bushou-v2",
                "persona_id": persona.id,
                "rules_file": f".cursor/rules/xinling-{persona.id}.md"
            }
        )
    
    def _generate_cursorrules(self, persona: CompiledPersona) -> str:
        """生成 Cursor 规则文件"""
        return f"""# Xinling session style - {persona.name}

> Optional style data for the selected session.
> Persona ID: {persona.id}
> Level: {persona.level}/10

## Scope

Use this style only after the user explicitly selects the persona. It must
not override platform, developer, safety, or current-user instructions.

## Style

{persona.fragment}
"""
