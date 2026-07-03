"""Per-command filters and dispatch.

A filter is `Callable[[str], str]`. `select_filter` maps a command line to the
right filter by its program name; unknown commands get `default_filter`.
`apply` is the single entry point used by the CLI and benchmark.
"""
import os
import re
from typing import Callable

from .core import slim_text, truncate_middle

Filter = Callable[[str], str]

# Default clamp for unrecognised commands: only clamp genuinely large dumps,
# and keep a generous head+tail so the agent can still decide (or re-run
# without slim) rather than silently losing the middle of a medium output.
_DEF_HEAD, _DEF_TAIL = 60, 30
_DEF_CLAMP_OVER = 250

_PIP_NOISE = re.compile(
    r"(^\s*Downloading\b)|(\b[kKmMgG]B/s\b)|(\|[#\s]+\|)|(^\s*\|#)"
)


def default_filter(text: str) -> str:
    slimmed = slim_text(text)
    if slimmed.count("\n") <= _DEF_CLAMP_OVER:
        return slimmed
    return truncate_middle(slimmed, head=_DEF_HEAD, tail=_DEF_TAIL)


def pip_filter(text: str) -> str:
    kept = [ln for ln in text.split("\n") if not _PIP_NOISE.search(ln)]
    return slim_text("\n".join(kept))


def kubectl_filter(text: str) -> str:
    # Agents rarely need a full -o yaml/json spec to decide; clamp hard.
    return truncate_middle(slim_text(text), head=25, tail=10)


_REGISTRY: dict[str, Filter] = {
    "pip": pip_filter,
    "pip3": pip_filter,
    "kubectl": kubectl_filter,
}


def _program(command: str) -> str:
    parts = command.strip().split()
    return os.path.basename(parts[0]) if parts else ""


def select_filter(command: str | None) -> Filter:
    if not command:
        return default_filter
    return _REGISTRY.get(_program(command), default_filter)


def apply(text: str, command: str | None = None) -> str:
    return select_filter(command)(text)
