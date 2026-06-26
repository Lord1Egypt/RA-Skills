#!/usr/bin/env python3
"""Compatibility shim. Prefer importing TomovieeText2MusicClient from tomoviee_text2music_client."""

try:
    from scripts.tomoviee_text2music_client import TomovieeClient, TomovieeText2MusicClient
except Exception:
    from tomoviee_text2music_client import TomovieeClient, TomovieeText2MusicClient

__all__ = ["TomovieeClient", "TomovieeText2MusicClient"]