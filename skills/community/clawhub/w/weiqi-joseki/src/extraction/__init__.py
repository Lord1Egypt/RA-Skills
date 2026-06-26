#!/usr/bin/env python3
"""提取模块 - SGF解析和定式提取"""

# SGF解析（原文件）
from .sgf_parser import parse_sgf

# KataGo下载器（原文件）
from .katago_downloader import iter_sgf_from_tar

# 新提取器
from .extractor import (
    extract_main_branch,
    extract_moves,
    extract_moves_all_corners,
    convert_to_multigogm,
    get_move_sequence,
)

# 连通块检测
from .component_detector import (
    ConnectedComponent,
    find_connected_components,
    filter_nearest_component,
    extract_corner_moves,
    extract_corner_moves_9lu,
    _extract_corner_moves_lu,
)

__all__ = [
    # 原模块
    'parse_sgf',
    'iter_sgf_from_tar',
    # 新提取器
    'extract_main_branch',
    'extract_moves',
    'extract_moves_all_corners',
    'convert_to_multigogm',
    'get_move_sequence',
    # 连通块检测
    'ConnectedComponent',
    'find_connected_components',
    'filter_nearest_component',
    'extract_corner_moves',
    'extract_corner_moves_9lu',
]
