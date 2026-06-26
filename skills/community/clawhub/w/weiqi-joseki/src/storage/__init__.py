#!/usr/bin/env python3
"""存储模块 - 数据持久化"""

from .json_storage import JsonStorage, DEFAULT_DB_PATH

__all__ = ['JsonStorage', 'DEFAULT_DB_PATH']
