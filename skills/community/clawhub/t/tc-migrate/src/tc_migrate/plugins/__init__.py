"""
资源迁移插件注册表 — 自动发现 + 拓扑排序

每种产品（CLB / NAT / CVM / ...）实现一个 ResourcePlugin 子类，
通过 @register_plugin 装饰器注册到全局注册表中。
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from .base import ResourcePlugin

# ── 全局插件注册表 ──
_REGISTRY: dict[str, Type[ResourcePlugin]] = {}


def register_plugin(cls: Type[ResourcePlugin]) -> Type[ResourcePlugin]:
    """装饰器：将 ResourcePlugin 子类注册到全局注册表"""
    _REGISTRY[cls.RESOURCE_TYPE] = cls
    return cls


def get_plugin(resource_type: str) -> Type[ResourcePlugin]:
    """按类型获取插件类"""
    if resource_type not in _REGISTRY:
        raise KeyError(
            f"未注册的资源类型: {resource_type}，"
            f"已注册: {list(_REGISTRY.keys())}"
        )
    return _REGISTRY[resource_type]


def get_all_plugins() -> dict[str, Type[ResourcePlugin]]:
    """获取所有已注册插件（无序）"""
    return dict(_REGISTRY)


def get_ordered_plugins() -> list[Type[ResourcePlugin]]:
    """
    按 DEPENDS_ON 拓扑排序返回插件列表（被依赖的在前）。
    用于确保创建资源时遵循依赖顺序：VPC → Subnet → SG → CLB / NAT / CVM
    """
    in_degree: dict[str, int] = {k: 0 for k in _REGISTRY}
    graph: dict[str, list[str]] = defaultdict(list)

    for rtype, cls in _REGISTRY.items():
        for dep in cls.DEPENDS_ON:
            if dep in _REGISTRY:
                graph[dep].append(rtype)
                in_degree[rtype] += 1

    queue = deque(k for k, d in in_degree.items() if d == 0)
    result: list[Type[ResourcePlugin]] = []
    while queue:
        node = queue.popleft()
        result.append(_REGISTRY[node])
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result


def list_resource_types() -> list[str]:
    """返回所有已注册的资源类型名列表"""
    return list(_REGISTRY.keys())


# ── 自动导入所有插件模块（触发 @register_plugin 装饰器）──
from . import clb_plugin as _clb  # noqa: F401, E402
from . import cvm_plugin as _cvm  # noqa: F401, E402
from . import nat_plugin as _nat  # noqa: F401, E402
from . import sg_plugin as _sg    # noqa: F401, E402
