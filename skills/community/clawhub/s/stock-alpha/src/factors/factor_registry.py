"""
因子注册表
统一管理所有因子，便于批量计算和回测
"""

from typing import Dict, Type
from .base_factor import BaseFactor
from .slsv_factor import SLSVFactor


class FactorRegistry:
    """因子注册表"""

    _registry: Dict[str, Type[BaseFactor]] = {}

    @classmethod
    def register(cls, factor_class: Type[BaseFactor]):
        """注册因子"""
        name = factor_class.name
        cls._registry[name] = factor_class
        return factor_class

    @classmethod
    def get(cls, name: str) -> Type[BaseFactor]:
        """获取因子类"""
        return cls._registry[name]

    @classmethod
    def list_factors(cls):
        """列出所有已注册因子"""
        return list(cls._registry.keys())

    @classmethod
    def create(cls, name: str, **kwargs) -> BaseFactor:
        """创建因子实例"""
        return cls._registry[name](**kwargs)


# 自动注册内置因子
FactorRegistry.register(SLSVFactor)
