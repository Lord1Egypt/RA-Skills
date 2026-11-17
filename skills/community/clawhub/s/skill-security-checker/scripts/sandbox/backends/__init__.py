"""
backends - Isolation backend selection.

Selection priority (auto):
    Docker  ->  Windows Sandbox  ->  Degraded (static-only)

Each backend exposes a uniform interface:
    .name           -> str
    .available      -> bool
    .execute(...)   -> raw behavior payload
    .cleanup()      -> None
"""

from .docker_backend import DockerBackend
from .winsandbox_backend import WindowsSandboxBackend
from .degraded import DegradedBackend


def select_backend(force=None):
    """Return the first available backend, or a degraded one.

    Args:
        force: 'docker' | 'winsandbox' | None. When set, only that backend is
               tried (still falls back to degraded if unavailable).
    """
    docker = DockerBackend()
    winsb = WindowsSandboxBackend()

    if force == 'docker':
        return docker if docker.available else DegradedBackend()
    if force == 'winsandbox':
        return winsb if winsb.available else DegradedBackend()

    if docker.available:
        return docker
    if winsb.available:
        return winsb
    return DegradedBackend()


__all__ = [
    'select_backend',
    'DockerBackend',
    'WindowsSandboxBackend',
    'DegradedBackend',
]
