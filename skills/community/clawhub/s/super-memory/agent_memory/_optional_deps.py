"""
_optional_deps.py — Graceful degradation for optional dependencies.

Provides lazy imports for optional packages. Components that depend
on optional packages should use the check functions from this module
rather than direct imports, so the system doesn't crash if a package
isn't installed.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

# ── Optional package availability ─────────────────────────────────

_OPTIONAL_IMPORTS = {
    "numpy": None,
    "torch": None,
    "transformers": None,
    "sentence_transformers": None,
    "dingtalk_sdk": None,
    "itchat": None,
    "gradio": None,
    "fastapi": None,
    "uvicorn": None,
    "pydantic": None,
    "pil": None,
    "PIL": None,
    "chromadb": None,
    "langchain": None,
    "langgraph": None,
    "crewai": None,
    "autogen": None,
    "httpx": None,
    "dash": None,
    "plotly": None,
    "sqlite_vec": None,
}

_CACHED = {}


def _try_import(name: str):
    """Try to import a package, return None if fails."""
    if name in _CACHED:
        return _CACHED[name]
    try:
        mod = __import__(name)
        _CACHED[name] = mod
        logger.debug("Imported optional package: %s", name)
        return mod
    except ImportError:
        _CACHED[name] = None
        logger.debug("Optional package not available: %s", name)
        return None


def is_available(package: str) -> bool:
    """Check if an optional package is installed."""
    if package not in _CACHED:
        _try_import(package)
    return _CACHED.get(package) is not None


def get(package: str):
    """Get the package module if available, else None."""
    if package not in _CACHED:
        _try_import(package)
    return _CACHED.get(package)


def require(package: str, feature: str = "this feature") -> object:
    """Get a package or raise a clear error with install hint.
    
    Use this when a feature absolutely requires the package.
    For optional features, use is_available() instead.
    """
    mod = get(package)
    if mod is None:
        install_hint = {
            "numpy": "pip install numpy",
            "torch": "pip install torch",
            "transformers": "pip install transformers",
            "sentence_transformers": "pip install sentence-transformers",
            "dingtalk_sdk": "pip install dingtalk-sdk",
            "fastapi": "pip install fastapi uvicorn",
            "pydantic": "pip install pydantic",
            "pil": "pip install Pillow",
            "chromadb": "pip install chromadb",
            "langchain": "pip install langchain",
            "sqlite_vec": "pip install sqlite-vec",
        }.get(package, f"pip install {package}")
        raise ImportError(
            f"Feature '{feature}' requires '{package}'.\n"
            f"Install with: {install_hint}"
        )
    return mod


def list_missing() -> list[str]:
    """List optional packages that are not installed."""
    return [k for k, v in _CACHED.items() if v is None and k in _OPTIONAL_IMPORTS]