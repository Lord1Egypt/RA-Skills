"""
野狐围棋下载适配器

封装 weiqi-foxwq 的 download_share.py 功能，供 weiqi-fetcher 调用
"""

from .download_share import (
    extract_via_api,
    extract_via_websocket,
    extract_game_info,
    extract_from_share_link,
    parse_share_url,
    create_sgf,
    parse_sgf_info,
)

__all__ = [
    'extract_via_api',
    'extract_via_websocket',
    'extract_game_info',
    'extract_from_share_link',
    'parse_share_url',
    'create_sgf',
    'parse_sgf_info',
]
