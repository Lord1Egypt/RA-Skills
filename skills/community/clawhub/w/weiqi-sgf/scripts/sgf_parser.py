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


# ============ 单元测试 ============

class TestSGFParser(unittest.TestCase):
    """SGF 解析器单元测试"""
    
    def test_empty_sgf(self):
        """测试空 SGF"""
        result = parse_sgf("")
        self.assertIn("SGF内容为空", result['errors'])
        self.assertEqual(result['stats']['total_nodes'], 1)
        self.assertEqual(result['stats']['move_nodes'], 0)
    
    def test_root_only(self):
        """测试只有根节点"""
        sgf = "(;GM[1]FF[4]PB[黑棋]PW[白棋])"
        result = parse_sgf(sgf)
        
        self.assertEqual(result['game_info']['black'], '黑棋')
        self.assertEqual(result['game_info']['white'], '白棋')
        self.assertEqual(result['tree']['is_root'], True)
        self.assertEqual(result['tree']['move_number'], 0)
        self.assertEqual(result['tree']['color'], None)
        self.assertEqual(result['tree']['coord'], None)
        self.assertEqual(len(result['tree']['children']), 0)
        self.assertEqual(result['stats']['total_nodes'], 1)
        self.assertEqual(result['stats']['move_nodes'], 0)
        self.assertEqual(len(result['errors']), 0)
    
    def test_single_branch(self):
        """测试单分支（标准棋谱）"""
        sgf = "(;GM[1];B[pd];W[pp];B[dd])"
        result = parse_sgf(sgf)
        
        self.assertEqual(result['stats']['total_nodes'], 4)
        self.assertEqual(result['stats']['move_nodes'], 3)
        self.assertEqual(result['stats']['max_depth'], 3)
        self.assertEqual(result['stats']['branch_count'], 0)
        
        tree = result['tree']
        self.assertEqual(len(tree['children']), 1)
        
        first_move = tree['children'][0]
        self.assertEqual(first_move['is_root'], False)
        self.assertEqual(first_move['move_number'], 1)
        self.assertEqual(first_move['color'], 'B')
        self.assertEqual(first_move['coord'], 'pd')
        self.assertEqual(first_move['properties']['B'], 'pd')
        
        second_move = first_move['children'][0]
        self.assertEqual(second_move['move_number'], 2)
        self.assertEqual(second_move['color'], 'W')
        self.assertEqual(second_move['coord'], 'pp')
    
    def test_root_variations(self):
        """测试根节点多分支（无主分支）"""
        sgf = "(;GM[1](;B[pd])(;B[dd]))"
        result = parse_sgf(sgf)
        
        self.assertEqual(result['stats']['total_nodes'], 3)
        self.assertEqual(result['stats']['move_nodes'], 2)
        self.assertEqual(result['stats']['branch_count'], 1)
        
        tree = result['tree']
        self.assertEqual(len(tree['children']), 2)
        
        # 第一个分支
        self.assertEqual(tree['children'][0]['color'], 'B')
        self.assertEqual(tree['children'][0]['coord'], 'pd')
        
        # 第二个分支（变化）
        self.assertEqual(tree['children'][1]['color'], 'B')
        self.assertEqual(tree['children'][1]['coord'], 'dd')
    
    def test_nested_variations(self):
        """测试嵌套变化分支"""
        sgf = "(;GM[1];B[pd](;W[pp])(;W[dp](;B[dd])(;B[qd])))"
        result = parse_sgf(sgf)
        
        # 树结构: Root -> B[pd] -> (W[pp], W[dp] -> (B[dd], B[qd]))
        # B[pd] 有 2 个子，贡献 1 个 branch
        # W[dp] 有 2 个子，贡献 1 个 branch
        # 总计 2 个 branch
        self.assertEqual(result['stats']['total_nodes'], 6)
        self.assertEqual(result['stats']['move_nodes'], 5)
        self.assertEqual(result['stats']['branch_count'], 2)
        
        tree = result['tree']
        # 根 -> B[pd]
        b_node = tree['children'][0]
        self.assertEqual(b_node['color'], 'B')
        
        # B[pd] 有两个子: W[pp] 和 W[dp]
        self.assertEqual(len(b_node['children']), 2)
        self.assertEqual(b_node['children'][0]['coord'], 'pp')
        self.assertEqual(b_node['children'][1]['coord'], 'dp')
        
        # W[dp] 有两个子: B[dd] 和 B[qd]
        w_dp_node = b_node['children'][1]
        self.assertEqual(len(w_dp_node['children']), 2)
        self.assertEqual(w_dp_node['children'][0]['coord'], 'dd')
        self.assertEqual(w_dp_node['children'][1]['coord'], 'qd')
    
    def test_escape_chars(self):
        """测试转义字符"""
        sgf = r"(;GM[1]C[Comment \] test])"
        result = parse_sgf(sgf)
        
        self.assertEqual(result['tree']['properties']['C'], "Comment ] test")
        self.assertEqual(len(result['errors']), 0)
    
    def test_handicap(self):
        """测试让子棋"""
        sgf = "(;GM[1]SZ[19]HA[2]AB[pd][dp];W[pp])"
        result = parse_sgf(sgf)
        
        self.assertEqual(result['game_info']['handicap'], 2)
        self.assertEqual(len(result['game_info']['handicap_stones']), 2)
        self.assertEqual(result['game_info']['handicap_stones'][0], {'x': 15, 'y': 3})
        self.assertEqual(result['game_info']['handicap_stones'][1], {'x': 3, 'y': 15})
        
        # 让子位置应在根节点
        ab = result['tree']['properties']['AB']
        self.assertIsInstance(ab, list)
        self.assertEqual(len(ab), 2)
    
    def test_multi_value_property(self):
        """测试多值属性"""
        sgf = "(;GM[1]AB[aa][bb][cc])"
        result = parse_sgf(sgf)
        
        ab = result['tree']['properties']['AB']
        self.assertIsInstance(ab, list)
        self.assertEqual(len(ab), 3)
        self.assertEqual(ab[0], 'aa')
        self.assertEqual(ab[1], 'bb')
        self.assertEqual(ab[2], 'cc')
    
    def test_invalid_sgf(self):
        """测试无效 SGF（未闭合属性值）"""
        sgf = "(;GM[1];B[pd;W[pp)"  # B的属性值未闭合
        result = parse_sgf(sgf)
        
        # 应该有错误（属性值未闭合）
        has_error = any("未闭合" in err or "属性" in err for err in result['errors'])
        self.assertTrue(has_error or len(result['errors']) > 0)
    
    def test_extra_close_paren(self):
        """测试多余右括号"""
        sgf = "(;GM[1];B[pd]))"
        result = parse_sgf(sgf)
        
        # 应该有多余的右括号错误或解析错误
        has_paren_error = any("括号" in err for err in result['errors'])
        self.assertTrue(has_paren_error or len(result['errors']) > 0)
    
    def test_pass_move(self):
        """测试虚手（停着）"""
        sgf = "(;GM[1];B[pd];W[];B[dd])"
        result = parse_sgf(sgf)
        
        tree = result['tree']
        w_node = tree['children'][0]['children'][0]
        self.assertEqual(w_node['color'], 'W')
        self.assertIsNone(w_node['coord'])
    
    def test_complex_tree(self):
        """测试复杂树结构"""
        sgf = """(;GM[1]FF[4]PB[黑棋]PW[白棋]
            (;B[pd];W[pp])
            (;B[dd];W[dp]
                (;B[pd])
                (;B[pp];W[pd](;B[qf])(;B[pf]))
            )
            (;B[dp];W[dd])
        )"""
        result = parse_sgf(sgf)
        
        # 根有 3 个子，贡献 2 个 branch
        # 第二个分支下又有分支，总共应有 4 个 branch
        self.assertEqual(result['stats']['branch_count'], 4)
        
        # 验证 game_info
        self.assertEqual(result['game_info']['black'], '黑棋')
        self.assertEqual(result['game_info']['white'], '白棋')
        self.assertEqual(result['game_info']['board_size'], 19)
    
    def test_multigo_format(self):
        """测试 MultiGo 格式的复杂棋谱（用户提供的棋谱）"""
        sgf = """(;CA[gb2312]AP[MultiGo:4.4.4]MULTIGOGM[0]

(;B[pd]N[b1];W[qc];B[qd];W[pc];B[oc];W[ob];B[nb];W[nc];B[od];W[mb];B[pb];W[na];B[qb])
(;B[pd]N[b2];W[qf]
(;B[qe]N[b21];W[pf];B[nd];W[pj])
(;B[nc]N[b22];W[rd];B[qc];W[qi]))
(;B[qd]N[b3];W[oc];B[pc];W[od];B[qf];W[kc]))"""
        
        result = parse_sgf(sgf)
        
        # 验证基本结构
        self.assertEqual(result['stats']['total_nodes'], 30)
        self.assertEqual(result['stats']['move_nodes'], 29)
        self.assertEqual(result['stats']['max_depth'], 13)
        self.assertEqual(result['stats']['branch_count'], 3)
        
        # 验证根节点属性
        self.assertEqual(result['tree']['properties']['CA'], 'gb2312')
        self.assertEqual(result['tree']['properties']['AP'], 'MultiGo:4.4.4')
        
        # 验证根有 3 个直接子节点（三个分支）
        self.assertEqual(len(result['tree']['children']), 3)
        
        # 验证 b1 分支
        b1 = result['tree']['children'][0]
        self.assertEqual(b1['properties']['N'], 'b1')
        self.assertEqual(b1['coord'], 'pd')
        self.assertEqual(b1['move_number'], 1)
        
        # 验证 b2 分支及其子分支
        b2 = result['tree']['children'][1]
        self.assertEqual(b2['properties']['N'], 'b2')
        # B[pd] N=b2 -> W[qf] -> (B[qe] N=b21, B[nc] N=b22)
        self.assertEqual(len(b2['children']), 1)  # W[qf]
        w_qf = b2['children'][0]
        self.assertEqual(len(w_qf['children']), 2)  # b21, b22 子分支
        
        # 验证 b3 分支
        b3 = result['tree']['children'][2]
        self.assertEqual(b3['properties']['N'], 'b3')
        self.assertEqual(b3['coord'], 'qd')


if __name__ == '__main__':
    print("=" * 60)
    print("SGF Parser 单元测试")
    print("=" * 60)
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSGFParser)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("=" * 60)
    if result.wasSuccessful():
        print("✓ 所有测试通过")
    else:
        print("✗ 测试失败")
        # 输出失败详情
        for failure in result.failures + result.errors:
            print(f"\n失败: {failure[0]}")
            print(failure[1])
    print("=" * 60)
