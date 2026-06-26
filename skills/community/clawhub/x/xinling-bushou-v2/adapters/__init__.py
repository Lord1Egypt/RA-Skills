"""
adapters/__init__.py
适配器注册表
"""

from typing import Dict, Type

from .base import PlatformAdapter
from .openclaw import OpenClawAdapter
from .claude_code import ClaudeCodeAdapter
from .cursor import CursorAdapter
from .generic import GenericAdapter


class AdapterRegistry:
    """适配器注册表
    
    使用方法：
        adapter_class = AdapterRegistry.get("claude_code")
        adapter = adapter_class()
    """
    
    _adapters: Dict[str, Type[PlatformAdapter]] = {
        "openclaw": OpenClawAdapter,
        "claude_code": ClaudeCodeAdapter,
        "cursor": CursorAdapter,
        "generic": GenericAdapter,
    }
    
    @classmethod
    def register(cls, platform_id: str, adapter_class: Type[PlatformAdapter]):
        """
        注册新的适配器
        
        Args:
            platform_id: 平台标识符
            adapter_class: 适配器类（必须继承 PlatformAdapter）
            
        Example:
            AdapterRegistry.register("my_platform", MyCustomAdapter)
        """
        if not issubclass(adapter_class, PlatformAdapter):
            raise TypeError(f"{adapter_class} must inherit from PlatformAdapter")
        cls._adapters[platform_id] = adapter_class
    
    @classmethod
    def get(cls, platform_id: str) -> Type[PlatformAdapter]:
        """
        获取适配器类
        
        Args:
            platform_id: 平台标识符
            
        Returns:
            适配器类
            
        Note:
            如果未找到对应平台，返回 GenericAdapter
        """
        return cls._adapters.get(platform_id, GenericAdapter)
    
    @classmethod
    def list_platforms(cls) -> list:
        """列出所有已注册的平台"""
        return list(cls._adapters.keys())
    
    @classmethod
    def supports_platform(cls, platform_id: str) -> bool:
        """检查是否支持某平台"""
        return platform_id in cls._adapters


# 便捷函数
def get_adapter(platform_id: str) -> PlatformAdapter:
    """获取适配器实例"""
    adapter_class = AdapterRegistry.get(platform_id)
    return adapter_class()


def detect_current_platform():
    """检测当前平台并返回适配器"""
    from schemas.launch_config import Platform
    detected = PlatformAdapter.detect_platform()
    return detected
