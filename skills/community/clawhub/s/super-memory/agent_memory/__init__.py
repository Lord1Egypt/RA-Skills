from __future__ import annotations

"""
Agent Memory V12 — Personal Memory OS for AI Agents
https://github.com/your-repo/agent-memory
"""

import sys as _sys

try:
    from importlib.metadata import version as _get_version
    __version__ = _get_version("agent-memory")
except Exception:
    # 开发模式 fallback：从 VERSION 文件读取
    try:
        from pathlib import Path
        _version_file = Path(__file__).parent.parent / "VERSION"
        __version__ = _version_file.read_text().strip()
    except Exception:
        __version__ = "0.0.0"

__all__ = [
    "Memory",
    "AgentMemory",
    "MemoryInput",
    "check_optional_deps",
    "__version__",
]

_OPTIONAL_DEPS: dict = {}
try:
    import sqlite_vec
    _OPTIONAL_DEPS["sqlite_vec"] = sqlite_vec
except ImportError:
    _OPTIONAL_DEPS["sqlite_vec"] = None
try:
    import transformers
    _OPTIONAL_DEPS["transformers"] = transformers
except ImportError:
    _OPTIONAL_DEPS["transformers"] = None


def _check_optional_dep(name: str, feature: str) -> None:
    if _OPTIONAL_DEPS.get(name) is None:
        raise ImportError(
            f"Feature '{feature}' requires '{name}'. Install with: pip install {name}"
        )


def check_optional_deps() -> dict:
    return {name: dep is not None for name, dep in _OPTIONAL_DEPS.items()}


def __getattr__(name: str):
    if name == "Memory":
        from .sdk import Memory
        return Memory
    if name == "AgentMemory":
        _sys.path.insert(0, __path__[0])
        from .memory_system import AgentMemory
        return AgentMemory
    if name == "MemoryInput":
        from .models import MemoryInput
        return MemoryInput
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
