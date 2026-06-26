"""
类型定义模块 - Python 版本
使用 dataclass 替代 TypeScript 接口
"""

from dataclasses import dataclass, field
from typing import Optional, List, Any, Callable, Dict


@dataclass
class ConfigOption:
    """配置选项"""
    value: str
    label: str
    command: str
    description: Optional[str] = None
    warning: Optional[str] = None
    requires_restart: bool = False
    required_permission: Optional[str] = None
    config_key: Optional[str] = None
    enabled_value: Any = None
    check_command: Optional[str] = None


@dataclass
class ConfigSection:
    """配置分组"""
    title: str
    options: List[str]


@dataclass
class SelectOption:
    """选择器选项"""
    value: str
    label: str
    description: Optional[str] = None
    warning: Optional[str] = None
    badge: Optional[str] = None


@dataclass
class SelectSection:
    """选择器分组"""
    title: str
    options: List[SelectOption]


@dataclass
class Button:
    """按钮"""
    text: str
    value: str


@dataclass
class ExecResult:
    """命令执行结果"""
    code: int
    stdout: str
    stderr: str
    error: Optional[str] = None


@dataclass
class CardHeader:
    """卡片头部"""
    title: str
    color: Optional[str] = None  # 'green', 'red', 'orange', 'blue'


@dataclass
class Card:
    """消息卡片"""
    header: CardHeader
    body: List[Dict[str, Any]]
    buttons: Optional[List[Button]] = None
    callback: Optional[Callable] = None


# 类型别名
InteractiveCallback = Callable[[str], Any]
Context = Any  # OpenClaw Context 类型
Message = Any  # OpenClaw Message 类型
