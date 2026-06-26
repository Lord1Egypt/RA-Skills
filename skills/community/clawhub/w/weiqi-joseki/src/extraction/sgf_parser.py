#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SGF 树状解析模块 - 完整支持嵌套变化分支

对外接口仅2个:
- parse_sgf(sgf_content: str) -> dict
- parse_sgf_file(filepath: str) -> dict

树节点固定结构:
{
    "properties": dict,
    "is_root": bool,
    "move_number": int,
    "color": str|None,
    "coord": str|None,
    "children": list
}
"""

import re
import json
import unittest
from typing import Optional, List, Dict, Any


def parse_sgf(sgf_content: str) -> dict:
    """
    解析 SGF 内容
    
    返回结构:
    {
        "game_info": {
            "board_size": 19,
            "black": "黑棋",
            "white": "白棋",
            "black_rank": "9d",
            "white_rank": "9d",
            "game_name": "围棋棋谱",
            "date": "2024-01-01",
            "result": "B+R",
            "komi": "375",
            "handicap": 0,
            "handicap_stones": [{"x": 15, "y": 3}, ...]
        },
        "tree": {
            "properties": {"GM": "1", "FF": "4", ...},
            "is_root": true,
            "move_number": 0,
            "color": null,
            "coord": null,
            "children": [...]
        },
        "stats": {
            "total_nodes": 150,
            "move_nodes": 149,
            "max_depth": 80,
            "branch_count": 3
        },
        "errors": []
    }
    """
    parser = _SGFParser()
    return parser.parse(sgf_content)


def parse_sgf_file(filepath: str) -> dict:
    """解析 SGF 文件"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    return parse_sgf(content)


class _SGFParser:
    """内部解析器实现"""
    
    def __init__(self):
        self.errors: List[str] = []
        self._pending_branch_props: Dict[str, Any] = {}  # 缓存分支起始处的属性
    
    def parse(self, sgf_content: str) -> dict:
        """解析 SGF 内容"""
        self.errors = []
        
        content = sgf_content.strip()
        if not content:
            self.errors.append("SGF内容为空")
            return self._create_empty_result()
        
        try:
            root_node = self._parse_tree(content)
            tree = self._node_to_dict(root_node)
            stats = self._calc_stats(tree)
            game_info = self._extract_game_info(tree)
            
            return {
                "game_info": game_info,
                "tree": tree,
                "stats": stats,
                "errors": self.errors
            }
        except Exception as e:
            self.errors.append(f"解析错误: {str(e)}")
            return self._create_empty_result()
    
    def _create_empty_result(self) -> dict:
        """创建空结果"""
        empty_tree = {
            "properties": {},
            "is_root": True,
            "move_number": 0,
            "color": None,
            "coord": None,
            "children": []
        }
        return {
            "game_info": self._extract_game_info(empty_tree),
            "tree": empty_tree,
            "stats": {"total_nodes": 1, "move_nodes": 0, "max_depth": 0, "branch_count": 0},
            "errors": self.errors
        }
    
    def _parse_tree(self, content: str) -> '_SGFNode':
        """解析树状结构
        
        SGF格式: (;GM[1](;B[pd];W[pp])(;B[dd]))
        - 序列本身不创建节点，序列内的第一个 ';' 决定父节点
        - '(' 只标记进入新层级，')' 标记退出
        """
        # 父节点栈，存储序列的父节点（即序列内第一个节点的父节点）
        parent_stack: List['_SGFNode'] = []
        # 序列内当前处理的节点
        seq_current: Optional['_SGFNode'] = None
        root: Optional['_SGFNode'] = None
        i = 0
        n = len(content)
        paren_count = 0
        
        while i < n:
            char = content[i]
            
            if char == '(':
                # 开始新序列
                if seq_current is not None:
                    # 有序列内当前节点，作为新序列的父节点
                    parent_stack.append(seq_current)
                elif parent_stack:
                    # 没有序列内节点但有父栈，复制栈顶
                    parent_stack.append(parent_stack[-1])
                elif root is not None:
                    # 没有父栈但有根，根是新序列的父
                    parent_stack.append(root)
                # else: 第一个序列，parent_stack保持为空
                
                paren_count += 1
                seq_current = None
                i += 1
                
                # 预读并缓存 '(' 后的属性（如 C[...]），直到遇到 ';' 或 ')'
                self._pending_branch_props = {}
                while i < n:
                    c = content[i]
                    if c in '();':
                        break
                    if c in ' \t\n\r':
                        i += 1
                        continue
                    if c.isupper():
                        prop_name = ''
                        while i < n and content[i].isupper():
                            prop_name += content[i]
                            i += 1
                        values = []
                        while i < n and content[i] == '[':
                            value, i, closed = self._parse_property_value(content, i + 1)
                            if not closed:
                                self.errors.append(f"属性 {prop_name} 的值未闭合")
                            values.append(value)
                        if values:
                            self._pending_branch_props[prop_name] = values if len(values) > 1 else values[0]
                    else:
                        self.errors.append(f"位置 {i}: 分支注释中意外字符 '{c}'，跳过")
                        i += 1
            
            elif char == ')':
                # 结束当前序列
                if paren_count > 0:
                    if parent_stack:
                        parent = parent_stack.pop()
                        # 序列结束后，seq_current 应该是序列的父节点
                        # 以便下一个序列能正确地挂在同一父节点下
                        seq_current = parent
                    else:
                        seq_current = None
                    paren_count -= 1
                else:
                    self.errors.append(f"位置 {i}: 多余的右括号")
                i += 1
            
            elif char == ';':
                # 创建新节点
                new_node = _SGFNode()
                
                # 确定父节点
                if seq_current is not None and not seq_current.properties:
                    # seq_current 是刚由'('创建的空白节点，给它属性
                    # 这不应该发生，因为我们不再在'('时创建节点
                    parent = seq_current
                elif seq_current is not None:
                    # 序列内已有节点，新节点作为 seq_current 的子（主分支延续）
                    seq_current.children.append(new_node)
                    new_node.parent = seq_current
                    new_node.move_number = seq_current.move_number + 1 if not seq_current.is_root else 1
                elif parent_stack:
                    # 序列的第一个节点，父节点是 parent_stack 栈顶
                    parent = parent_stack[-1]
                    parent.children.append(new_node)
                    new_node.parent = parent
                    new_node.move_number = parent.move_number + 1 if not parent.is_root else 1
                elif root is None:
                    # 第一个节点，作为根
                    root = new_node
                    new_node.is_root = True
                    new_node.move_number = 0
                else:
                    # 另一个顶级节点（无括号包裹的情况）
                    if root.is_root and len(root.children) == 0 and not root.properties:
                        # 根是空的，直接使用
                        root.properties = {}
                        new_node.parent = root
                        new_node.move_number = 1
                        root.children.append(new_node)
                    elif root.is_root:
                        # 创建包裹节点
                        wrapper = _SGFNode()
                        wrapper.is_root = True
                        wrapper.move_number = 0
                        
                        if not root.properties and len(root.children) == 0:
                            # root 是空的，替换
                            root = wrapper
                        else:
                            # 移动原root
                            root.parent = wrapper
                            root.move_number = 1
                            wrapper.children.append(root)
                            root = wrapper
                        
                        new_node.parent = root
                        new_node.move_number = 1
                        root.children.append(new_node)
                    else:
                        new_node.parent = root
                        new_node.move_number = 1
                        root.children.append(new_node)
                
                # 解析属性
                props, i = self._parse_properties(content, i + 1)
                
                # 合并缓存的分支属性（如果有）
                if self._pending_branch_props:
                    # 缓存的属性优先，但已被解析的属性不会被覆盖
                    merged_props = self._pending_branch_props.copy()
                    merged_props.update(props)
                    props = merged_props
                    self._pending_branch_props = {}  # 清空缓存
                
                new_node.properties = props
                self._extract_move_info(new_node)
                
                seq_current = new_node
            
            elif char in ' \t\n\r':
                i += 1
            else:
                self.errors.append(f"位置 {i}: 意外字符 '{char}'，跳过")
                i += 1
        
        if paren_count > 0:
            self.errors.append("警告: 括号未完全闭合")
        

        
        return root or _SGFNode()
    
    def _parse_properties(self, content: str, start: int) -> tuple:
        """解析属性列表，返回 (属性字典, 新位置)"""
        props: Dict[str, Any] = {}
        i = start
        n = len(content)
        
        while i < n:
            char = content[i]
            
            if char in '();':
                break
            
            if char in ' \t\n\r':
                i += 1
                continue
            
            if char.isupper():
                prop_name = ''
                while i < n and content[i].isupper():
                    prop_name += content[i]
                    i += 1
                
                values = []
                while i < n and content[i] == '[':
                    value, i, closed = self._parse_property_value(content, i + 1)
                    if not closed:
                        self.errors.append(f"属性 {prop_name} 的值未闭合")
                    values.append(value)
                
                if values:
                    props[prop_name] = values if len(values) > 1 else values[0]
                else:
                    props[prop_name] = ''
            else:
                self.errors.append(f"位置 {i}: 属性名应为大写字母，跳过 '{char}'")
                i += 1
        
        return props, i
    
    def _parse_property_value(self, content: str, start: int) -> tuple:
        """解析属性值，正确处理转义
        返回: (值, 新位置, 是否正常闭合)
        """
        value = []
        i = start
        n = len(content)
        
        while i < n:
            char = content[i]
            
            if char == '\\' and i + 1 < n:
                next_char = content[i + 1]
                # SGF 转义规则：\] -> ], \\ -> \, \n -> 换行等
                if next_char == ']':
                    value.append(']')
                    i += 2
                elif next_char == '\\':
                    value.append('\\')
                    i += 2
                elif next_char == 'n':
                    value.append('\n')
                    i += 2
                elif next_char == 'r':
                    value.append('\r')
                    i += 2
                elif next_char == 't':
                    value.append('\t')
                    i += 2
                else:
                    # 其他字符直接保留
                    value.append(next_char)
                    i += 2
            elif char == ']':
                # 找到闭合括号
                i += 1
                return ''.join(value), i, True
            else:
                value.append(char)
                i += 1
        
        # 未正常闭合
        return ''.join(value), i, False
    
    def _extract_move_info(self, node: '_SGFNode'):
        """从属性中提取 color 和 coord"""
        if 'B' in node.properties:
            node.color = 'B'
            node.coord = self._normalize_coord(node.properties['B'])
        elif 'W' in node.properties:
            node.color = 'W'
            node.coord = self._normalize_coord(node.properties['W'])
    
    def _normalize_coord(self, val: Any) -> Optional[str]:
        """统一坐标格式"""
        if isinstance(val, list) and val:
            return val[0] if val[0] else None
        return val if val else None
    
    def _node_to_dict(self, node: '_SGFNode') -> dict:
        """将节点转换为字典"""
        return {
            "properties": node.properties,
            "is_root": node.is_root,
            "move_number": node.move_number,
            "color": node.color,
            "coord": node.coord,
            "children": [self._node_to_dict(c) for c in node.children]
        }
    
    def _calc_stats(self, tree: dict) -> dict:
        """计算统计信息"""
        total_nodes = 0
        move_nodes = 0
        max_depth = 0
        branch_count = 0
        
        def traverse(node: dict):
            nonlocal total_nodes, move_nodes, max_depth, branch_count
            total_nodes += 1
            if not node.get("is_root", False):
                move_nodes += 1
            max_depth = max(max_depth, node.get("move_number", 0))
            children = node.get("children", [])
            # 子节点数 > 1 表示有分支（除第一个主分支外的都是变化）
            if len(children) > 1:
                branch_count += len(children) - 1
            for child in children:
                traverse(child)
        
        traverse(tree)
        
        return {
            "total_nodes": total_nodes,
            "move_nodes": move_nodes,
            "max_depth": max_depth,
            "branch_count": branch_count
        }
    
    def _extract_game_info(self, tree: dict) -> dict:
        """从根节点提取棋局信息"""
        props = tree.get("properties", {})
        
        def get_prop(key: str, default: str = '') -> str:
            val = props.get(key, default)
            if isinstance(val, list) and val:
                return str(val[0])
            return str(val) if val else default
        
        # 棋盘大小
        try:
            board_size = int(get_prop('SZ', '19'))
        except ValueError:
            board_size = 19
        
        # 让子数
        try:
            handicap = int(get_prop('HA', '0'))
        except ValueError:
            handicap = 0
        
        # 让子位置
        handicap_stones = []
        ab_prop = props.get('AB', [])
        if isinstance(ab_prop, str):
            ab_prop = [ab_prop]
        if isinstance(ab_prop, list):
            for coord in ab_prop:
                if coord and len(str(coord)) >= 2:
                    c = str(coord)
                    x = ord(c[0]) - 97
                    y = ord(c[1]) - 97
                    if 0 <= x < board_size and 0 <= y < board_size:
                        handicap_stones.append({"x": x, "y": y})
        
        return {
            "board_size": board_size,
            "black": get_prop('PB', '黑棋'),
            "white": get_prop('PW', '白棋'),
            "black_rank": get_prop('BR'),
            "white_rank": get_prop('WR'),
            "game_name": get_prop('GN', '围棋棋谱'),
            "date": get_prop('DT'),
            "result": get_prop('RE'),
            "komi": get_prop('KM', '375'),
            "handicap": handicap,
            "handicap_stones": handicap_stones
        }


class _SGFNode:
    """内部节点类"""
    
    def __init__(self):
        self.properties: Dict[str, Any] = {}
        self.is_root: bool = False
        self.move_number: int = 0
        self.color: Optional[str] = None
        self.coord: Optional[str] = None
        self.parent: Optional['_SGFNode'] = None
        self.children: List['_SGFNode'] = []


