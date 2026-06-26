"""
adapters/base.py
PlatformAdapter 基类 - 所有平台适配器的抽象基类
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path

from schemas.launch_config import Platform, LaunchConfig, CompiledPersona


class PlatformAdapter(ABC):
    """平台适配器基类"""
    
    PLATFORM_ID: str = "generic"
    
    @abstractmethod
    def get_platform_id(self) -> str:
        """返回平台标识"""
        return self.PLATFORM_ID
    
    @abstractmethod
    def compile_system_prompt(
        self,
        base_prompt: str,
        persona_fragment: str,
        metadata: Dict[str, Any]
    ) -> str:
        """
        编译完整的 system prompt
        
        Args:
            base_prompt: 基础 system prompt
            persona_fragment: 人格片段
            metadata: 元数据
            
        Returns:
            平台特定格式的完整 system prompt
        """
        pass
    
    @abstractmethod
    def get_launch_config(self, persona: CompiledPersona) -> LaunchConfig:
        """
        生成平台特定的启动配置
        
        Args:
            persona: 编译后的人格
            
        Returns:
            LaunchConfig: 启动配置
        """
        pass
    
    def supports_subagent(self) -> bool:
        """是否支持子代理机制"""
        return False
    
    @staticmethod
    def detect_platform() -> Platform:
        """检测当前运行环境"""
        import os
        
        # 优先检测环境变量
        platform_env = os.getenv("XINLING_PLATFORM")
        if platform_env:
            try:
                return Platform(platform_env)
            except ValueError:
                pass
        
        # OpenClaw 特征检测
        if os.getenv("OPENCLAW_SESSION"):
            return Platform.OPENCLAW
        
        # Claude Code 特征检测
        claude_code_env = os.getenv("CLAUDE_CODE")
        claude_json = Path(".claude.json")
        if claude_code_env or claude_json.exists():
            return Platform.CLAUDE_CODE
        
        # Cursor 特征检测
        cursorrules = Path(".cursorrules")
        if cursorrules.exists():
            return Platform.CURSOR
        
        # Roo Code 特征检测
        if os.getenv("ROO_CODE_SESSION"):
            return Platform.ROO_CODE
        
        return Platform.GENERIC
