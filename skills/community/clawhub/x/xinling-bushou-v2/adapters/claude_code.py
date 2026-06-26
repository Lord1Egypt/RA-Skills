"""
adapters/claude_code.py
Claude Code 平台适配器
"""

import json
from typing import Dict, Any

from schemas.launch_config import Platform, LaunchConfig, CompiledPersona
from .base import PlatformAdapter


class ClaudeCodeAdapter(PlatformAdapter):
    """Claude Code 平台适配器
    
    Claude Code 特点：
    - 无原生 subagent 支持
    - 通过 prompt 注入人格
    - 支持 --system-param 传递元数据
    - 支持 .claude.json 配置文件
    """
    
    PLATFORM_ID = "claude_code"
    
    def get_platform_id(self) -> str:
        return self.PLATFORM_ID
    
    def supports_subagent(self) -> bool:
        return False  # Claude Code 无原生 subagent
    
    def compile_system_prompt(
        self,
        base_prompt: str,
        persona_fragment: str,
        metadata: Dict[str, Any]
    ) -> str:
        """
        Claude Code 通过 prompt 直接拼接人格片段
        Claude Code 会将整个 system prompt 作为上下文
        """
        # 构造带人格标识的片段
        marked_fragment = f"""
{'='*60}
【人格叠加 - 心灵补手 V2】
{'='*60}
{persona_fragment}
{'='*60}
"""
        
        if base_prompt:
            return f"{base_prompt}\n{marked_fragment}"
        return marked_fragment
    
    def get_launch_config(self, persona: CompiledPersona) -> LaunchConfig:
        """
        Claude Code 启动配置
        
        方案：
        1. 通过 --dangerously-skip-permissions 允许自定义行为
        2. 通过环境变量备份关键配置
        3. 建议用户将人格元数据写入 .claude.json
        """
        persona_config = {
            "xinling": {
                "persona_id": persona.id,
                "name": persona.name,
                "level": persona.level,
                "mode": persona.mode,
                "platform": "claude_code"
            }
        }
        
        return LaunchConfig(
            # Claude Code 会将 extra_system_content 作为 system prompt 追加
            extra_system_content=persona.fragment,
            extra_cli_args=[
                "--dangerously-skip-permissions",  # 允许自定义行为
            ],
            env_vars={
                "XINLING_PERSONA_ID": persona.id,
                "XINLING_NAME": persona.name,
                "XINLING_LEVEL": str(persona.level),
                "XINLING_MODE": persona.mode
            },
            config_file={
                "path": ".claude.json",
                "content": persona_config
            },
            metadata={
                "source": "xinling-bushou-v2",
                "persona_id": persona.id
            }
        )
