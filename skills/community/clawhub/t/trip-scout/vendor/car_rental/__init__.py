"""
租车网点查询模块

支持平台:
  - 神州租车 (zuche): C 端公开 JSON API，无需认证
  - 一嗨租车 (ehi): Playwright 解析 SSR 页面

使用方式:
  from vendor.car_rental import get_stores
  result = get_stores("乌鲁木齐")
  # result = {"zuche": [StoreInfo, ...], "ehi": [StoreInfo, ...]}
"""

from __future__ import annotations

from .models import StoreInfo
from . import zuche, ehi


def get_stores(
    city: str,
    source: str | None = None,
) -> dict[str, list[StoreInfo] | str]:
    """
    查询某城市的租车网点。

    Args:
        city: 城市名（中文，如"乌鲁木齐"）
        source: 指定平台 "zuche" / "ehi"，None 表示双平台查询

    Returns:
        {"zuche": [...], "ehi": [...]}
        单平台异常时对应 key 的值为空列表，并添加 "{source}_error" 键记录错误信息。
    """
    result: dict[str, list[StoreInfo] | str] = {}

    sources = [source] if source else ["zuche", "ehi"]

    for src in sources:
        try:
            if src == "zuche":
                result["zuche"] = zuche.get_stores(city)
            elif src == "ehi":
                result["ehi"] = ehi.get_stores(city)
        except Exception as e:
            result[src] = []
            result[f"{src}_error"] = str(e)

    return result


__all__ = [
    "StoreInfo",
    "get_stores",
    "zuche",
    "ehi",
]
