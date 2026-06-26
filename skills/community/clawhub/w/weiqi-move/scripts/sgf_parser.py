#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SGF 解析模块 - 可被其他技能包复用

提供完整的 SGF 文件解析能力：
- 树状结构解析（支持变化图/变例）
- 棋局信息提取
- 主分支着法提取
- 变化图提取

安全特性:
    - 仅使用标准库 (re, html, json)
    - 无网络访问
"""

import re
import html
import json


class SGFNode:
    """SGF 树节点 - 表示一个着法或根节点"""
    def __init__(self, properties=None, parent=None):
        self.properties = properties or {}  # SGF 属性，如 {'B': 'pd', 'C': 'comment'}
        self.parent = parent
        self.children = []  # 子节点列表（变化分支）
        self.is_root = False

    def add_child(self, node):
        """添加子节点"""
        node.parent = self
        self.children.append(node)
        return node


class SGFTreeParser:
    """
    SGF 树状结构解析器
    
    SGF 格式使用括号表示层级：
    - 每个 ( 开始一个新节点/分支
    - 每个 ) 结束当前节点/分支
    - ; 开始一个节点的属性列表
    - 属性格式: KEY[value] 或 KEY (无值属性)
    
    示例:
    (;GM[1]FF[4];B[pd];W[pp])
    (;GM[1](;B[pd];W[pp])(;B[dd];W[dp]))
    """

    def __init__(self):
        self.root = None
        self.errors = []

    def parse(self, sgf_content):
        """
        解析 SGF 内容，返回根节点
        遇到错误时停止遍历，返回已构建的树
        """
        self.root = None
        self.errors = []

        # 清理内容
        sgf_content = sgf_content.strip()
        if not sgf_content:
            self.errors.append("SGF内容为空")
            return None

        # 预处理：处理转义字符
        sgf_content = self._unescape(sgf_content)

        # 解析
        try:
            self.root = self._parse_tree(sgf_content)
        except Exception as e:
            self.errors.append(f"解析错误: {str(e)}")

        return self.root

    def _unescape(self, content):
        """处理 SGF 转义字符"""
        result = []
        i = 0
        while i < len(content):
            if content[i] == '\\' and i + 1 < len(content):
                next_char = content[i + 1]
                if next_char == '\\':
                    result.append('\\')
                    i += 2
                elif next_char == ']':
                    result.append(']')
                    i += 2
                elif next_char == 'n':
                    result.append('\n')
                    i += 2
                elif next_char == 'r':
                    result.append('\r')
                    i += 2
                elif next_char == 't':
                    result.append('\t')
                    i += 2
                else:
                    result.append(next_char)
                    i += 2
            else:
                result.append(content[i])
                i += 1
        return ''.join(result)

    def _parse_tree(self, content):
        """
        解析树状结构
        使用栈来跟踪当前节点
        """
        stack = []  # (node, is_paren_created) 的列表
        current_node = None
        root = None
        i = 0
        n = len(content)

        while i < n:
            char = content[i]

            if char == '(':
                # 开始新节点/分支
                new_node = SGFNode()
                if stack:
                    parent, _ = stack[-1]
                    parent.add_child(new_node)
                else:
                    root = new_node
                    new_node.is_root = True
                stack.append((new_node, True))  # 标记为由 '(' 创建
                current_node = new_node
                i += 1

            elif char == ')':
                # 出栈直到遇到由 '(' 创建的节点，并将该节点也出栈
                popped_paren = False
                while stack:
                    node, is_paren = stack.pop()
                    if is_paren:
                        popped_paren = True
                        break
                if not popped_paren:
                    self.errors.append(f"位置 {i}: 多余的右括号")
                current_node = stack[-1][0] if stack else None
                i += 1

            elif char == ';':
                if not stack:
                    root = SGFNode()
                    root.is_root = True
                    stack.append((root, False))  # 根节点不由 '(' 创建
                    current_node = root
                elif current_node.properties:
                    # 当前节点已有属性，创建新节点作为子节点
                    new_node = SGFNode()
                    current_node.add_child(new_node)
                    stack.append((new_node, False))  # 标记为由 ';' 创建
                    current_node = new_node

                props, i = self._parse_properties(content, i + 1)
                current_node.properties = props

            elif char in ' \t\n\r':
                i += 1
            else:
                self.errors.append(f"位置 {i}: 意外字符 '{char}'，尝试跳过")
                i += 1

        if stack and len(stack) > 1:
            self.errors.append("警告: 括号未完全闭合")

        return root

    def _parse_properties(self, content, start):
        """解析属性列表"""
        props = {}
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
                    value, i = self._parse_property_value(content, i + 1)
                    values.append(value)

                if values:
                    props[prop_name] = values if len(values) > 1 else values[0]
                else:
                    props[prop_name] = ''
            else:
                self.errors.append(f"位置 {i}: 属性名应为大写字母，跳过 '{char}'")
                i += 1

        return props, i

    def _parse_property_value(self, content, start):
        """解析属性值，找到匹配的 ]"""
        value = []
        i = start
        n = len(content)
        depth = 1

        while i < n and depth > 0:
            char = content[i]

            if char == '\\' and i + 1 < n:
                value.append(char)
                i += 1
            elif char == '[':
                depth += 1
                value.append(char)
                i += 1
            elif char == ']':
                depth -= 1
                if depth > 0:
                    value.append(char)
                i += 1
            else:
                value.append(char)
                i += 1

        if depth > 0:
            self.errors.append(f"位置 {start}: 属性值未闭合")

        return ''.join(value), i


def parse_with_tree_parser(sgf_content):
    """使用内置树状解析器解析 SGF"""
    parser = SGFTreeParser()
    root = parser.parse(sgf_content)

    if not root:
        return None, None, None, parser.errors

    game_info = extract_game_info_from_tree(root)

    # 提取主分支着法
    moves = []
    node = root
    while node.children:
        node = node.children[0]
        props = node.properties
        if 'B' in props:
            coord = props['B']
            moves.append({
                'color': 'B',
                'coord': coord[0] if isinstance(coord, list) else coord
            })
        elif 'W' in props:
            coord = props['W']
            moves.append({
                'color': 'W',
                'coord': coord[0] if isinstance(coord, list) else coord
            })

    variations = extract_variations_from_tree(root, moves)

    return moves, variations, game_info, parser.errors


def extract_game_info_from_tree(root):
    """从树中提取棋局信息"""
    props = root.properties if root else {}
    info = {}

    def get_prop(key, default=''):
        val = props.get(key, default)
        if isinstance(val, list) and val:
            return val[0]
        return val if val else default

    info['black'] = get_prop('PB', '黑棋')
    info['white'] = get_prop('PW', '白棋')
    info['black_rank'] = get_prop('BR')
    info['white_rank'] = get_prop('WR')
    info['game_name'] = get_prop('GN', '围棋棋谱')
    info['date'] = get_prop('DT')
    info['result'] = get_prop('RE')
    info['komi'] = get_prop('KM', '375')
    info['board_size'] = get_prop('SZ', '19')
    info['handicap'] = get_prop('HA', '0')

    handicap_stones = []
    ab_prop = props.get('AB', [])
    if isinstance(ab_prop, str):
        ab_prop = [ab_prop]
    if isinstance(ab_prop, list):
        for coord in ab_prop:
            if coord and len(coord) >= 2:
                x = ord(coord[0]) - 97
                y = ord(coord[1]) - 97
                handicap_stones.append({'x': x, 'y': y})
    info['handicap_stones'] = handicap_stones

    return info


def extract_variations_from_tree(root, main_moves):
    """从树中提取变化图"""
    variations = {}

    def traverse(node, move_num):
        if not node.children:
            return

        for i, child in enumerate(node.children):
            child_moves = []
            current = child
            while current:
                props = current.properties
                if 'B' in props or 'W' in props:
                    coord = props.get('B') or props.get('W')
                    if isinstance(coord, list):
                        coord = coord[0] if coord else ''
                    color = 'B' if 'B' in props else 'W'
                    child_moves.append({'color': color, 'coord': coord})

                if current.children:
                    current = current.children[0]
                else:
                    break

            if i > 0 and child_moves:
                if move_num not in variations:
                    variations[move_num] = []

                name = f"变化{len(variations[move_num]) + 1}"
                win_rate = name

                comment = child.properties.get('C', [''])
                if isinstance(comment, list) and comment:
                    comment = comment[0]
                else:
                    comment = str(comment)

                if comment:
                    win_match = re.search(r'([黑白]).*?(\d+\.?\d*)%', comment)
                    if win_match:
                        win_rate = f"{win_match.group(1)}{win_match.group(2)}%"
                        name += f" {win_rate}"

                variations[move_num].append({
                    'name': name,
                    'winRate': win_rate,
                    'moves': child_moves,
                    'comment': comment
                })

            next_move_num = move_num
            if child.properties and ('B' in child.properties or 'W' in child.properties):
                next_move_num = move_num + 1

            traverse(child, next_move_num)

    traverse(root, 0)
    return variations


def parse_sgf(sgf_content):
    """
    解析 SGF 的主入口函数
    
    返回: (moves, variations, game_info, parse_info)
    """
    parse_info = {
        'parser_used': 'tree_parser',
        'errors': [],
        'warnings': []
    }

    moves, variations, game_info, errors = parse_with_tree_parser(sgf_content)
    parse_info['errors'].extend(errors)
    
    return moves, variations or {}, game_info or {}, parse_info


def extract_main_branch(sgf_content):
    """从SGF中提取主分支着法"""
    moves, _, _, _ = parse_sgf(sgf_content)
    return moves


def extract_variations(sgf_content):
    """提取变化图（变例）"""
    _, variations, _, _ = parse_sgf(sgf_content)
    return variations


def extract_game_info(sgf_content):
    """提取棋局信息（兼容旧版正则方式）"""
    info = {}

    patterns = {
        'PB': ('black', r'PB\[([^\]]+)\]'),
        'PW': ('white', r'PW\[([^\]]+)\]'),
        'BR': ('black_rank', r'BR\[([^\]]+)\]'),
        'WR': ('white_rank', r'WR\[([^\]]+)\]'),
        'GN': ('game_name', r'GN\[([^\]]+)\]'),
        'DT': ('date', r'DT\[([^\]]+)\]'),
        'RE': ('result', r'RE\[([^\]]+)\]'),
        'KM': ('komi', r'KM\[([^\]]+)\]'),
        'SZ': ('board_size', r'SZ\[(\d+)\]'),
        'HA': ('handicap', r'HA\[(\d+)\]'),
    }

    for key, (name, pattern) in patterns.items():
        match = re.search(pattern, sgf_content)
        if match:
            info[name] = match.group(1)

    # 处理让子
    handicap_stones = []
    for match in re.finditer(r';AB\[([a-z]{2})\]', sgf_content):
        coord = match.group(1)
        x = ord(coord[0]) - 97
        y = ord(coord[1]) - 97
        handicap_stones.append({'x': x, 'y': y})

    if not handicap_stones:
        ab_match = re.search(r'AB((?:\[[a-z]{2}\])+)', sgf_content)
        if ab_match:
            coords = re.findall(r'\[([a-z]{2})\]', ab_match.group(1))
            for coord in coords:
                x = ord(coord[0]) - 97
                y = ord(coord[1]) - 97
                handicap_stones.append({'x': x, 'y': y})

    info['handicap_stones'] = handicap_stones

    return info


def coord_to_pos(coord):
    """将 SGF 坐标 (如 'pd') 转换为数字坐标 (x, y)"""
    if not coord or len(coord) < 2:
        return None
    x = ord(coord[0]) - 97
    y = ord(coord[1]) - 97
    return (x, y)


def pos_to_coord(x, y):
    """将数字坐标转换为 SGF 坐标"""
    return chr(97 + x) + chr(97 + y)
