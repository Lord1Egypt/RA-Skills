"""Xiaohongshu MCP REST API Client"""

__version__ = "0.1.0"

from .client import XiaohongshuClient
from .account import AccountManager

__all__ = ["XiaohongshuClient", "AccountManager"]
