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
        """Cursor 使用规则文件，不在 prompt 中拼接"""
        return persona_fragment  # 仅人格片段，base 由 .cursorrules 提供
    
    def get_launch_config(self, persona: CompiledPersona) -> LaunchConfig:
        """
        Cursor 通过 .cursor/rules/ 注入人格规则
        
        方案：
        1. 在 .cursor/rules/ 下创建人格规则文件
        2. 人格片段作为规则内容
        3. Cursor 会在对话中自动加载这些规则
        """
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
        return f"""# 心灵补手 - {persona.name}

> 由心灵补手 V2.0 自动生成
> 人格 ID: {persona.id}
> 谄媚程度: {persona.level}/10

## 身份

{persona.fragment}

## 激活条件

当检测到以下场景时自动触发谄媚话术：
- 用户完成任务
- 用户分享好消息  
- 用户表达情绪
- 用户做出决定

## 话术规则

- 程度 1-3：委婉暗示
- 程度 4-6：正常赞美
- 程度 7-9：强烈吹捧
- 程度 10：无脑崇拜（Debug 模式）
"""
