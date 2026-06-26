#!/usr/bin/env python3
"""
定式发现模块 (discover)
替代原match/identify接口，简化设计
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

from ..extraction import extract_moves_all_corners, get_move_sequence
from ..core.coords import convert_to_top_right, normalize_corner_sequence
from ..matching import TrieMatcher, PrefixMatchResult


@dataclass
class DiscoverResult:
    """定式发现结果"""
    joseki_id: str      # 定式ID
    moves: str          # 树状SGF（替代原来的完整着法串）
    prefix: str         # 匹配的前缀着法串
    prefix_len: int     # 匹配的前缀长度
    total_moves: int    # 着法串长度（还原）
    source_corner: str  # 棋谱来源角 "tl"/"tr"/"bl"/"br"


class JosekiDiscoverer:
    """定式发现器"""
    
    def __init__(self, joseki_list: List[dict]):
        """
        初始化发现器
        
        Args:
            joseki_list: 定式列表，每个定式包含 id, name, moves
        """
        self.matcher = TrieMatcher()
        self.matcher.build(joseki_list)
    
    def discover_corner(self, moves: List[str], corner: str) -> Optional[DiscoverResult]:
        """
        发现单个角的定式，moves返回tree SGF
        
        Args:
            moves: 着法坐标列表（原始SGF坐标）
            corner: 来源角 "tl"/"tr"/"bl"/"br"
        
        Returns:
            最佳匹配的DiscoverResult，无匹配返回None
        """
        if not moves or len(moves) < 2:
            return None
        
        # 检查该角9路范围内是否有棋子（转换前判断）
        from ..core.coords import has_stone_in_corner_9lu
        if not has_stone_in_corner_9lu(moves, corner):
            return None  # 该角9路无棋子，无匹配
        
        tr_moves = convert_to_top_right(moves, corner)
        
        # 标准化后匹配（自动处理方向）
        std_moves, _ = normalize_corner_sequence(tr_moves)
        match = self.matcher.match(std_moves, top_k=1)
        if not match:
            return None
        
        matched_moves = std_moves
        prefix_len = match[0].prefix_len
        joseki_id = match[0].id
        
        # 生成 tree SGF
        prefix = matched_moves[:prefix_len]
        # 如果实战着法完全匹配定式（没有超出），不显示变化分支
        if len(matched_moves) == prefix_len:
            # 只显示主分支，不显示其他分支
            tree_sgf = self.matcher.export_tree(
                prefix=prefix,
                main_branch=matched_moves,
                limit=0  # limit=0 表示只显示主分支
            )
        else:
            tree_sgf = self.matcher.export_tree(
                prefix=prefix,
                main_branch=matched_moves,
                limit=5
            )
        
        return DiscoverResult(
            joseki_id=joseki_id,
            moves=tree_sgf,  # tree SGF
            prefix=" ".join(matched_moves[:prefix_len]),
            prefix_len=prefix_len,
            total_moves=len(matched_moves),  # 还原为长度
            source_corner=corner,
        )
    
    def discover(self, sgf_data: str, first_n: int = 80,
                 distance_threshold: int = 4) -> Dict[str, DiscoverResult]:
        """
        从SGF发现定式
        
        Args:
            sgf_data: SGF棋谱内容
            first_n: 提取前N手
            distance_threshold: 连通块距离阈值
        
        Returns:
            {corner: DiscoverResult, ...}
            corner: "tl"/"tr"/"bl"/"br"
        """
        # 使用新提取接口提取四角着法
        corner_moves_dict = extract_moves_all_corners(
            sgf_data, 
            first_n=first_n, 
            distance_threshold=distance_threshold
        )
        
        results = {}
        
        for corner in ['tl', 'tr', 'bl', 'br']:
            moves = corner_moves_dict.get(corner)
            if not moves:
                continue
            
            coords = get_move_sequence(moves)
            match = self.discover_corner(coords, corner)
            if match:
                results[corner] = match
        
        return results


def discover_joseki(
    sgf_data: str,
    joseki_list: List[dict],
    first_n: int = 80,
    distance_threshold: int = 4
) -> Dict[str, DiscoverResult]:
    """
    便捷函数：从SGF发现定式
    
    Args:
        sgf_data: SGF棋谱内容
        joseki_list: 定式列表
        first_n: 提取前N手
        distance_threshold: 连通块距离阈值
    
    Returns:
        {corner: DiscoverResult, ...}
    """
    discoverer = JosekiDiscoverer(joseki_list)
    return discoverer.discover(sgf_data, first_n, distance_threshold)