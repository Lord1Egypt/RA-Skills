"""
schemas/launch_config.py
LaunchConfig 类型定义 - 跨平台统一的启动参数结构
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
from pathlib import Path


class RelationshipMode(Enum):
    """人格关系模式"""
    INDEPENDENT = "independent"   # 完全独立，不继承主人格
    INHERIT = "inherit"          # 继承主人格 + override 覆盖
    STACK = "stack"              # 叠加（V1.0 语义）


class Platform(Enum):
    """目标平台"""
    OPENCLAW = "openclaw"
    CLAUDE_CODE = "claude_code"
    CURSOR = "cursor"
    COPILOT = "copilot"
    ROO_CODE = "roo_code"
    AIDER = "aider"
    GENERIC = "generic"


@dataclass
class LaunchConfig:
    """启动配置 - 跨平台统一格式"""
    
    # 额外要追加到 system prompt 的内容
    extra_system_content: str = ""
    
    # 平台特定的 CLI 参数
    extra_cli_args: List[str] = field(default_factory=list)
    
    # 环境变量
    env_vars: Dict[str, str] = field(default_factory=dict)
    
    # 需要写入的配置文件（path -> content）
    config_file: Optional[Dict[str, Any]] = None
    
    # OpenClaw 特定：subagent 启动参数
    openclaw_specific: Optional[Dict[str, Any]] = None
    
    # 元数据（传递给子代理）
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "extra_system_content": self.extra_system_content,
            "extra_cli_args": self.extra_cli_args,
            "env_vars": self.env_vars,
            "config_file": self.config_file,
            "openclaw_specific": self.openclaw_specific,
            "metadata": self.metadata
        }


@dataclass
class CompiledPersona:
    """编译后的人格对象"""
    id: str
    name: str
    level: int
    mode: str
    fragment: str   # 编译后的人格片段（prompt 文本）
    relationship: RelationshipMode
    source_file: Optional[Path] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "mode": self.mode,
            "fragment": self.fragment,
            "relationship": self.relationship.value,
            "source_file": str(self.source_file) if self.source_file else None,
            "metadata": self.metadata
        }
