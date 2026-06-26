from __future__ import annotations

import os
import stat
import sys
from pathlib import Path


def _default_home() -> Path:
    if sys.platform.startswith("win") and os.environ.get("LOCALAPPDATA"):
        return Path(os.environ["LOCALAPPDATA"]) / "resource-hunter"
    if os.environ.get("XDG_DATA_HOME"):
        return Path(os.environ["XDG_DATA_HOME"]) / "resource-hunter"
    return Path.home() / ".resource-hunter"


def resource_hunter_home() -> Path:
    configured = os.environ.get("RESOURCE_HUNTER_HOME")
    home = Path(configured).expanduser() if configured else _default_home()
    home.mkdir(parents=True, exist_ok=True)
    return home


def _is_linked_storage_dir(path: Path) -> bool:
    if path.is_symlink():
        return True

    reparse_point = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    if not reparse_point:
        return False

    try:
        attributes = path.lstat().st_file_attributes
    except (AttributeError, FileNotFoundError, OSError):
        return False
    return bool(attributes & reparse_point)


def _workspace_storage_dir() -> Path | None:
    workspace_raw = os.environ.get("OPENCLAW_WORKSPACE")
    if not workspace_raw:
        return None

    workspace = Path(workspace_raw).expanduser()
    storage = workspace / "storage"
    if _is_linked_storage_dir(storage):
        resolved = storage.resolve(strict=False)
        resolved.mkdir(parents=True, exist_ok=True)
        return resolved
    return storage


def storage_root() -> Path:
    if os.environ.get("RESOURCE_HUNTER_HOME"):
        base = resource_hunter_home() / "storage"
    else:
        base = _workspace_storage_dir() or (resource_hunter_home() / "storage")
    base.mkdir(parents=True, exist_ok=True)
    skill_root = base / "resource-hunter"
    skill_root.mkdir(parents=True, exist_ok=True)
    return skill_root


def default_download_dir() -> Path:
    if os.environ.get("RESOURCE_HUNTER_HOME"):
        download_root = resource_hunter_home() / "downloads"
    else:
        storage = _workspace_storage_dir()
        download_root = (storage / "downloads") if storage is not None else (resource_hunter_home() / "downloads")
    download_root.mkdir(parents=True, exist_ok=True)
    return download_root
