"""Platform-neutral runtime paths, replacing nanobot.config.paths dependency."""

import os
from pathlib import Path


def get_runtime_subdir(*parts: str) -> Path:
    """Return a platform-appropriate runtime data directory.

    Uses DND_DATA_DIR env var if set, otherwise ~/.sagasmith/<parts>.
    """
    if configured := os.environ.get("DND_DATA_DIR"):
        base = Path(configured)
    else:
        base = Path.home() / ".sagasmith"
    target = base.joinpath(*parts)
    target.mkdir(parents=True, exist_ok=True)
    return target


def package_data_path(package: str, filename: str) -> str:
    """Return the filesystem path to a data file within a package.

    On NanoBot, package would be 'nanobot.dnd.db'; on other platforms the
    caller passes the appropriate package name.
    """
    from importlib.resources import files as package_files

    return str(package_files(package).joinpath(filename))
