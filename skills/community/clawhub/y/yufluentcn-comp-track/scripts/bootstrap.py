"""Monorepo / ClawHub 双模式：定位 cloud_cli + yufluent_api 所在目录。"""

from __future__ import annotations

import sys
from pathlib import Path

_SHARED_DIR = Path(__file__).resolve().parent

_HARNESS_PACKAGE_SRC = (
    ("tokenapi-sdk", "tokenapi_sdk"),
    ("tokenapi-harness", "tokenapi_harness"),
)


def _discover_monorepo_root(start: Path) -> Path | None:
    for parent in (start, *start.parents):
        harness_pkg = parent / "packages" / "tokenapi-harness" / "src" / "tokenapi_harness"
        if harness_pkg.is_dir() and (parent / "harness" / "catalog.yaml").is_file():
            return parent
    return None


def ensure_harness_packages_path(script_file: str | Path | None = None) -> Path | None:
    """
    确保 tokenapi_sdk / tokenapi_harness 可导入。

    - 已 pip install（requirements-dev.txt）时直接返回
    - Monorepo：将 packages/*/src 加入 sys.path
  """
    try:
        import tokenapi_harness  # noqa: F401
        return None
    except ImportError:
        pass

    start = Path(script_file).resolve().parent if script_file else Path.cwd()
    root = _discover_monorepo_root(start)
    if root is None:
        raise ImportError(
            "tokenapi-harness not found. Install monorepo dev deps: "
            "pip install -r requirements-dev.txt"
        )

    for pkg_dir, module_name in _HARNESS_PACKAGE_SRC:
        src = root / "packages" / pkg_dir / "src"
        init = src / module_name / "__init__.py"
        if not init.is_file():
            raise ImportError(f"expected {init} under monorepo root {root}")
        path = str(src)
        if path not in sys.path:
            sys.path.insert(0, path)
    return root


def ensure_cloud_client_path(script_file: str | Path) -> Path:
    """
    将 cloud 客户端目录加入 sys.path。

    - ClawHub zip：scripts/ 内已有 yufluent_api.py（package-skill 注入）
    - Monorepo：回退 skills/_shared/
    """
    scripts_dir = Path(script_file).resolve().parent
    skills_shared = scripts_dir.parent.parent / "_shared"
    for candidate in (scripts_dir, skills_shared, _SHARED_DIR):
        if candidate.is_dir() and (candidate / "yufluent_api.py").is_file():
            path = str(candidate)
            if path not in sys.path:
                sys.path.insert(0, path)
            return candidate
    raise ImportError(
        "cloud client not found: expected scripts/yufluent_api.py (ClawHub) "
        "or skills/_shared/yufluent_api.py (monorepo)"
    )
