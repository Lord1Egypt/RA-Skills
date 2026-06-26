#!/usr/bin/env python3
"""Compatibility shim for legacy import path.

Use `tomoviee_text2sfx_client.py` as the primary implementation.
"""

from .tomoviee_text2sfx_client import TomovieeClient, TomovieeText2SfxClient

__all__ = ["TomovieeText2SfxClient", "TomovieeClient"]
