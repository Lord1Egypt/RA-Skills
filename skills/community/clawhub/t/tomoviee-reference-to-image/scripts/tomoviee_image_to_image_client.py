#!/usr/bin/env python3
"""Compatibility shim. Prefer importing TomovieeImg2ImgClient from tomoviee_img2img_client."""

try:
    from scripts.tomoviee_img2img_client import TomovieeClient, TomovieeImg2ImgClient
except Exception:
    from tomoviee_img2img_client import TomovieeClient, TomovieeImg2ImgClient

__all__ = ["TomovieeClient", "TomovieeImg2ImgClient"]