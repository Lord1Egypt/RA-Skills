"""
adapters/openclaw.py
OpenClaw 平台适配器
"""

from typing import Dict, Any

from schemas.launch_config import Platform, LaunchConfig, CompiledPersona
from .base import PlatformAdapter


class OpenClawAdapter(PlatformAdapter):
    """OpenClaw 平台适配器
    
    OpenClaw 支持：
    - subagent 机制（sessions_spawn）
    - system_prefix 注入人格片段
    - metadata 传递人格元数据
    """
    
    PLATFORM_ID = "openclaw"
    
    def get_platform_id(self) -> str:
        return self.PLATFORM_ID
    
    def supports_subagent(self) -> bool:
        return True  # OpenClaw 原生支持 subagent
    
    def compile_system_prompt(
        self,
        base_prompt: str,
        persona_fragment: str,
        metadata: Dict[str, Any]
    ) -> str:
        """
        OpenClaw 通过 system_prefix 注入人格片段
        直接追加到 base prompt
        """
        if base_prompt:
            return f"{base_prompt}\n\n{persona_fragment}"
        return persona_fragment
    
    def get_launch_config(self, persona: CompiledPersona) -> LaunchConfig:
        """
        OpenClaw subagent 启动配置
        
        使用 sessions_spawn 时：
        - system_prefix 参数注入人格片段
        - metadata 传递人格元数据供 subagent 读取
        """
        return LaunchConfig(
            extra_system_content=persona.fragment,
            openclaw_specific={
                "persona_id": persona.id,
                "persona_level": persona.level,
                "persona_mode": persona.mode,
                "persona_name": persona.name,
            },
            metadata={
                "source": "xinling-bushou-v2",
                "persona_id": persona.id,
                "relationship": persona.relationship.value
            }
        )
