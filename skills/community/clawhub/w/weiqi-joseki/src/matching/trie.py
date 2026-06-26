#!/usr/bin/env python3
"""
Trie树实现
用于定式着法串的前缀匹配
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class PrefixMatchResult:
    """前缀匹配结果 - 最长前缀优先，同前缀选总手数最短的"""
    id: str
    name: str
    prefix_len: int      # 匹配的前缀长度（最长优先）
    total_moves: int     # 定式总手数（同前缀时越短越优先）
    matched_direction: str  # "ruld" 或 "rudl"


class TrieMatcher:
    """Trie树匹配器 - 支持ruld和rudl两个方向"""
    
    def __init__(self):
        self._trie: Dict = {}      # 标准化方向前缀树
        self._joseki_map: Dict[str, dict] = {}  # id -> 定式数据
    
    def build(self, joseki_list: List[dict]):
        """
        从定式列表构建Trie树
        
        Args:
            joseki_list: 定式列表，每个定式包含 id, name, moves
        """
        self._trie = {}
        self._joseki_map = {}
        
        for j in joseki_list:
            joseki_id = j.get("id")
            if not joseki_id:
                continue
            
            self._joseki_map[joseki_id] = j
            moves = j.get("moves", [])
            if not moves:
                continue
            
            # 直接入树（定式已标准化）
            self._add_to_trie(self._trie, moves, joseki_id)
    
    def _add_to_trie(self, trie: dict, moves: List[str], joseki_id: str):
        """将定式着法序列加入前缀树"""
        node = trie
        for move in moves:
            if move not in node:
                node[move] = {'next': {}, 'ids': []}
            node[move]['ids'].append(joseki_id)
            node = node[move]['next']
    
    def match(self, moves: List[str], top_k: int = 3) -> List[PrefixMatchResult]:
        """
        匹配着法序列，返回最佳匹配的定式
        
        Args:
            moves: 着法序列（ruld方向，将被标准化）
            top_k: 返回结果数量上限
        
        Returns:
            匹配结果列表，按 prefix_len 降序，相同按 total_moves 升序
        """
        # 标准化后匹配
        from ..core.coords import normalize_corner_sequence
        std_moves, _ = normalize_corner_sequence(moves)
        all_results = self._match_direction(self._trie, std_moves, "std")
        
        # 构建结果对象
        results = []
        for prefix_len, joseki_id, total_moves, direction in all_results:
            joseki = self._joseki_map.get(joseki_id, {})
            results.append(PrefixMatchResult(
                id=joseki_id,
                name=joseki.get("name", joseki_id),
                prefix_len=prefix_len,
                total_moves=total_moves,
                matched_direction=direction
            ))
        
        # 排序：按 prefix_len 降序，相同按 total_moves 升序
        results.sort(key=lambda x: (-x.prefix_len, x.total_moves))
        
        return results[:top_k]
    
    def _match_direction(self, trie: dict, moves: List[str], direction: str) -> List[Tuple[int, str, int, str]]:
        """
        在指定方向的Trie中匹配
        
        Returns:
            [(prefix_len, joseki_id, total_moves, direction), ...]
        """
        node = trie
        matched_ids = {}  # id -> 最深匹配长度
        
        for i, move in enumerate(moves):
            if move not in node:
                break
            
            prefix_len = i + 1
            for joseki_id in node[move]['ids']:
                matched_ids[joseki_id] = prefix_len
            
            node = node[move]['next']
        
        # 获取完整定式手数
        results = []
        for joseki_id, match_len in matched_ids.items():
            joseki = self._joseki_map.get(joseki_id, {})
            total_moves = len(joseki.get("moves", []))
            results.append((match_len, joseki_id, total_moves, direction))
        
        return results
    
    def export_tree(self, prefix: List[str] = None, main_branch: List[str] = None, limit: int = 100) -> str:
        """导出树状SGF"""
        # 定位前缀
        trie = self._trie
        for move in (prefix or []):
            if move not in trie:
                return "(;C[前缀不存在])"
            trie = trie[move]['next']
        
        # 收集包含前缀的定式终点
        paths = self._collect_joseki_endpoints(prefix or [])
        
        # 构建路径到ids的映射
        ids_map = {tuple(p[0]): p[2] for p in paths}
        
        # 分离主分支和其他路径
        other_paths = []
        main_tuple = None
        
        if main_branch:
            main_path_tuple = tuple(main_branch)
            # 检查主分支是否在定式库中
            if main_path_tuple in ids_map:
                main_freq = next(p[1] for p in paths if p[0] == main_branch)
                main_tuple = (main_branch, main_freq, ids_map[main_path_tuple])
            else:
                main_tuple = (main_branch, 0, [])
            # 其他路径排除主分支
            other_paths = [p for p in paths if p[0] != main_branch]
        else:
            other_paths = paths
        
        # 其他路径按频率排序，取limit
        other_paths.sort(key=lambda x: -x[1])
        selected = other_paths[:limit]
        
        # 主分支放第一个（不占用limit名额）
        if main_tuple:
            selected.insert(0, main_tuple)
        
        # 构建树（传递主分支用于标记）
        tree = self._build_tree_from_paths(selected, main_branch)
        
        # 使用 sgfmill 生成SGF
        prefix_str = " ".join(prefix) if prefix else "all"
        return self._tree_to_sgf(tree, 0, main_branch, 0, prefix_str)
    
    def _collect_joseki_endpoints(self, prefix):
        """收集包含指定前缀的所有定式终点
        返回: [(path, freq, ids), ...]，其中path是完整着法序列
        """
        results = []
        prefix_tuple = tuple(prefix)
        
        for joseki_id, joseki in self._joseki_map.items():
            moves = joseki.get('moves', [])
            
            # 检查是否包含前缀
            if len(moves) < len(prefix):
                continue
            if tuple(moves[:len(prefix)]) != prefix_tuple:
                continue
            
            # 这是包含前缀的定式，记录其完整路径
            freq = joseki.get('frequency', 0)
            results.append((moves, freq, [joseki_id]))
        
        return results
    
    def _build_tree_from_paths(self, paths, main_branch=None):
        """从路径列表构建树，paths是 (path, freq, ids) 三元组列表
        main_branch: 主分支路径，用于标记主分支节点
        """
        root = {}
        main_set = set()
        if main_branch:
            # 构建主分支前缀集合，用于快速判断
            for i in range(1, len(main_branch) + 1):
                main_set.add(tuple(main_branch[:i]))
        
        for path, freq, ids in paths:
            node = root
            for i, move in enumerate(path):
                if move not in node:
                    node[move] = {'next': {}, 'freq': 0, 'ids': [], 'is_main': False}
                # 标记是否为主分支的一部分
                path_so_far = tuple(path[:i+1])
                if path_so_far in main_set:
                    node[move]['is_main'] = True
                # 只在终点设置 freq 和 ids
                if i == len(path) - 1:
                    node[move]['freq'] = freq
                    node[move]['ids'] = ids
                node = node[move]['next']
        return root
    
    def _tree_to_sgf(self, tree, depth, main_branch=None, main_depth=0, prefix_str='all'):
        """生成 SGF 字符串（手动拼接，确保分支格式正确）"""
        
        def coord_to_sgf(move):
            """坐标已经是 SGF 格式，直接返回"""
            return move
        
        def build_sgf(tree, depth, main_branch, main_depth):
            if not tree and not (main_branch and main_depth < len(main_branch)):
                return ""
            
            # 确定当前节点
            current_move = None
            current_node = None
            
            if main_branch and main_depth < len(main_branch):
                current_move = main_branch[main_depth]
                if tree and current_move in tree:
                    current_node = tree[current_move]
            
            if current_node is None and tree:
                items = sorted(tree.items(), key=lambda x: -x[1].get('freq', 0))
                current_move, current_node = items[0]
            
            if current_node is None:
                # 输出剩余主分支
                if main_branch and main_depth < len(main_branch):
                    parts = []
                    for i in range(main_depth, len(main_branch)):
                        color = 'B' if i % 2 == 0 else 'W'
                        parts.append(f";{color}[{coord_to_sgf(main_branch[i])}]")
                    return "".join(parts)
                return ""
            
            # 输出当前节点
            color = 'B' if depth % 2 == 0 else 'W'
            freq = current_node.get('freq', 0)
            ids = current_node.get('ids', [])
            
            if ids and freq > 0:
                node_sgf = f";{color}[{coord_to_sgf(current_move)}]C[出现次数:{freq}]"
            else:
                node_sgf = f";{color}[{coord_to_sgf(current_move)}]"
            
            # 获取子树
            next_tree = current_node.get('next', {})
            
            # 确定主分支下一手
            main_next = None
            has_main_remaining = main_branch and main_depth + 1 < len(main_branch)
            if has_main_remaining:
                main_next = main_branch[main_depth + 1]
            
            # 收集子节点
            all_children = []
            for move, node in next_tree.items():
                is_main = (move == main_next)
                all_children.append((move, node, is_main))
            
            # 排序：主分支优先，然后按频率
            all_children.sort(key=lambda x: (-x[2], -x[1].get('freq', 0)))
            
            # 生成子节点SGF
            # 如果只有一个子节点且是主分支，直接延续（不包裹括号）
            # 否则所有子节点都用括号包裹（树状格式）
            child_parts = []
            single_main_child = (len(all_children) == 1 and all_children[0][2])
            
            for i, (child_move, child_node, is_main) in enumerate(all_children):
                branch_color = 'B' if (depth + 1) % 2 == 0 else 'W'
                child_freq = child_node.get('freq', 0)
                child_ids = child_node.get('ids', [])
                
                # 递归生成分支的后续
                if is_main and has_main_remaining:
                    branch_cont = build_sgf(child_node.get('next', {}), depth + 2, 
                                           main_branch, main_depth + 2)
                else:
                    branch_cont = build_sgf(child_node.get('next', {}), depth + 2, None, 0)
                
                if single_main_child:
                    # 只有一个主分支子节点，直接延续不包裹括号
                    if child_ids and child_freq > 0:
                        child_parts.append(f";{branch_color}[{coord_to_sgf(child_move)}]C[出现次数:{child_freq}]" + branch_cont)
                    else:
                        child_parts.append(f";{branch_color}[{coord_to_sgf(child_move)}]" + branch_cont)
                else:
                    # 多个子节点，用括号包裹
                    if child_ids and child_freq > 0:
                        branch_start = f"(;{branch_color}[{coord_to_sgf(child_move)}]C[出现次数:{child_freq}]"
                    else:
                        branch_start = f"(;{branch_color}[{coord_to_sgf(child_move)}]"
                    child_parts.append(branch_start + branch_cont + ")")
            
            # 如果子树为空但主分支还有剩余
            if not all_children and has_main_remaining:
                for i in range(main_depth + 1, len(main_branch)):
                    color = 'B' if i % 2 == 0 else 'W'
                    child_parts.append(f";{color}[{coord_to_sgf(main_branch[i])}]")
            
            return node_sgf + "".join(child_parts)
        
        # 生成完整SGF
        body = build_sgf(tree, depth, main_branch, main_depth)
        return f"(;FF[4]AP[WeiqiJoseki:1.0]C[定式树: {prefix_str}]CA[UTF-8]GM[1]SZ[19]{body})"