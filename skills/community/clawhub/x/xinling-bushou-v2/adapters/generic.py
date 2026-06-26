"""
adapters/generic.py
Generic 通用适配器 - 用于无法精确匹配的平台
"""

from typing import Dict, Any

from schemas.launch_config import Platform, LaunchConfig, CompiledPersona
from .base import PlatformAdapter


class GenericAdapter(PlatformAdapter):
    """通用适配器 - 用于任何支持 system prompt 的 LLM API"""
    
    PLATFORM_ID = "generic"
    
    def get_platform_id(self) -> str:
        return self.PLATFORM_ID
    
    def supports_subagent(self) -> bool:
        return False
    
    def compile_system_prompt(
        self,
        base_prompt: str,
        persona_fragment: str,
        metadata: Dict[str, Any]
    ) -> str:
        """
        通用方案：将人格片段追加到 base prompt
        适用于任何支持 system prompt 的 LLM API
        """
        prefix = metadata.get("system_prompt_prefix", "【人格叠加】 ")
        return f"{base_prompt}\n\n{prefix}{persona_fragment}"
    
    def get_launch_config(self, persona: CompiledPersona) -> LaunchConfig:
        """
        通用方案：返回标准格式的配置字典
        
        适用于：
        - OpenAI API (via system parameter)
        - Anthropic API
        - Any LLM with system prompt support
        """
        return LaunchConfig(
            extra_system_content=persona.fragment,
            extra_cli_args=[
                "--persona", persona.id,
                "--persona-level", str(persona.level)
            ],
            env_vars={
                "XINLING_PERSONA": persona.id,
                "XINLING_LEVEL": str(persona.level),
                "XINLING_MODE": persona.mode
            },
            metadata={
                "source": "xinling-bushou-v2",
                "persona_id": persona.id
            }
        )
