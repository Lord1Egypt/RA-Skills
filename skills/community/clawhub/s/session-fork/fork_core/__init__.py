"""fork_core — 跨产品通用的会话分叉引擎（Fork = Projection Derivative）。

业务抽象（见 分支与复活-业务层抽象-设计-20260901.md）：
  createFork(projection, {atSeq, name?}) → forkProjection

本包提供：
  - create_fork(adapter, session_ref, ...)  — 核心入口
  - list_forks(adapter, cwd)                — 谱系查询
  - get_adapter(name)                       — adapter 工厂

与平台无关；产品差异由 adapter 吸收（workbuddy / claude-code / ...）。
"""

from .adapters import available, get_adapter
from .engine import create_fork, list_forks
from .models import ForkResult, SessionMeta
from ._version import __version__, VERSION  # noqa: F401 — 单一来源

__all__ = [
    "create_fork",
    "list_forks",
    "get_adapter",
    "available",
    "ForkResult",
    "SessionMeta",
    "cli",
    "VERSION",
]
