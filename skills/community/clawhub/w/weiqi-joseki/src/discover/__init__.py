#!/usr/bin/env python3
"""定式发现模块 - 替代原match/identify"""

from .discoverer import (
    JosekiDiscoverer,
    DiscoverResult,
    discover_joseki,
)

__all__ = [
    'JosekiDiscoverer',
    'DiscoverResult', 
    'discover_joseki',
]
