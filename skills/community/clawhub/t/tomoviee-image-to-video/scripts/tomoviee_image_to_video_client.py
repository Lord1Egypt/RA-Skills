#!/usr/bin/env python3
"""Compatibility shim. Prefer importing TomovieeImg2VideoClient from tomoviee_img2video_client."""

try:
    from scripts.tomoviee_img2video_client import TomovieeClient, TomovieeImg2VideoClient
except Exception:
    from tomoviee_img2video_client import TomovieeClient, TomovieeImg2VideoClient

__all__ = ["TomovieeClient", "TomovieeImg2VideoClient"]