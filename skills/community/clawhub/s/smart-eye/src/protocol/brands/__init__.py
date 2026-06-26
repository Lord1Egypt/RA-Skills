"""
brands/__init__.py - 品牌注册表

所有支持的摄像头品牌在此注册。
新增品牌：
  1. 在 brands/ 下创建 newbrand.py，实现 BrandBase
  2. 在 BRANDS 字典中注册：BRANDS["newbrand"] = NewBrandCamera
"""

from .base_brand import BrandBase
from .tplink import TPLinkCamera
from .huawei import HuaweiCamera

# 品牌注册表：key = brand 字段值（统一小写）
BRANDS: dict[str, type[BrandBase]] = {
    "tplink":  TPLinkCamera,
    "huawei":  HuaweiCamera,
}


def get_brand(brand_name: str) -> type[BrandBase] | None:
    """根据品牌名获取对应类。"""
    return BRANDS.get(brand_name.lower())


def register_brand(brand_name: str, cls: type[BrandBase]):
    """允许运行时动态注册新品牌（供扩展用）。"""
    BRANDS[brand_name.lower()] = cls


__all__ = ["BrandBase", "TPLinkCamera", "HuaweiCamera",
           "BRANDS", "get_brand", "register_brand"]
