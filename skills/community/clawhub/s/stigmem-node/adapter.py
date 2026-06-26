"""Compatibility shim for the ClawHub skill bundle.

The skill installs ``stigmem-openclaw`` and re-exports the packaged adapter so
OpenClaw users can continue to import ``adapter`` from the skill directory.
"""

from __future__ import annotations

from stigmem_openclaw.adapter import SYSTEM_PROMPT_DIRECTIVE, BootContext, OpenClawStigmemAdapter

__all__ = ["BootContext", "OpenClawStigmemAdapter", "SYSTEM_PROMPT_DIRECTIVE"]
