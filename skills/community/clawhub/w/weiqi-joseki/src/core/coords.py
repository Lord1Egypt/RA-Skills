#!/usr/bin/env python3
"""
坐标系统模块 - 只包含坐标转换相关代码
围棋棋盘坐标系定义和转换
"""

from typing import List, Dict, Optional, Tuple


# 8个坐标系定义
class CoordinateSystem:
    """坐标系定义"""
    
    def __init__(self, name: str, origin_corner: str, x_dir: str, y_dir: str):
        self.name = name
        self.origin_corner = origin_corner
        self.x_dir = x_dir
        self.y_dir = y_dir
        self._to_local_cache: Dict[str, Tuple[int, int]] = {}
        self._to_sgf_cache: Dict[Tuple[int, int], str] = {}
        self._build_maps()
    
    @staticmethod
    def sgf_to_nums(sgf: str) -> Tuple[int, int]:
        return (ord(sgf[0]) - ord('a'), ord(sgf[1]) - ord('a'))
    
    @staticmethod
    def nums_to_sgf(c: int, r: int) -> str:
        return chr(ord('a') + c) + chr(ord('a') + r)
    
    def _sgf_to_local(self, sgf: str) -> Tuple[int, int]:
        col, row = self.sgf_to_nums(sgf)
        if self.origin_corner == 'tl':
            if self.x_dir == 'right' and self.y_dir == 'down':
                return (col, row)
            elif self.x_dir == 'down' and self.y_dir == 'right':
                return (row, col)
        elif self.origin_corner == 'bl':
            if self.x_dir == 'right' and self.y_dir == 'up':
                return (col, 18 - row)
            elif self.x_dir == 'up' and self.y_dir == 'right':
                return (18 - row, col)
        elif self.origin_corner == 'tr':
            if self.x_dir == 'left' and self.y_dir == 'down':
                return (18 - col, row)
            elif self.x_dir == 'down' and self.y_dir == 'left':
                return (row, 18 - col)
        elif self.origin_corner == 'br':
            if self.x_dir == 'left' and self.y_dir == 'up':
                return (18 - col, 18 - row)
            elif self.x_dir == 'up' and self.y_dir == 'left':
                return (18 - row, 18 - col)
        raise ValueError(f"Invalid coordinate system: {self.name}")
    
    def _local_to_sgf(self, x: int, y: int) -> str:
        if self.origin_corner == 'tl':
            if self.x_dir == 'right' and self.y_dir == 'down':
                return self.nums_to_sgf(x, y)
            elif self.x_dir == 'down' and self.y_dir == 'right':
                return self.nums_to_sgf(y, x)
        elif self.origin_corner == 'bl':
            if self.x_dir == 'right' and self.y_dir == 'up':
                return self.nums_to_sgf(x, 18 - y)
            elif self.x_dir == 'up' and self.y_dir == 'right':
                return self.nums_to_sgf(y, 18 - x)
        elif self.origin_corner == 'tr':
            if self.x_dir == 'left' and self.y_dir == 'down':
                return self.nums_to_sgf(18 - x, y)
            elif self.x_dir == 'down' and self.y_dir == 'left':
                return self.nums_to_sgf(18 - y, x)
        elif self.origin_corner == 'br':
            if self.x_dir == 'left' and self.y_dir == 'up':
                return self.nums_to_sgf(18 - x, 18 - y)
            elif self.x_dir == 'up' and self.y_dir == 'left':
                return self.nums_to_sgf(18 - y, 18 - x)
        raise ValueError(f"Invalid coordinate system: {self.name}")
    
    def _build_maps(self):
        for col in range(19):
            for row in range(19):
                sgf = self.nums_to_sgf(col, row)
                local = self._sgf_to_local(sgf)
                self._to_local_cache[sgf] = local
                self._to_sgf_cache[local] = sgf


# 8个坐标系定义
COORDINATE_SYSTEMS = {
    'lurd': CoordinateSystem('lurd', 'tl', 'right', 'down'),
    'ludr': CoordinateSystem('ludr', 'tl', 'down', 'right'),
    'ldru': CoordinateSystem('ldru', 'bl', 'right', 'up'),
    'ldur': CoordinateSystem('ldur', 'bl', 'up', 'right'),
    'ruld': CoordinateSystem('ruld', 'tr', 'left', 'down'),
    'rudl': CoordinateSystem('rudl', 'tr', 'down', 'left'),
    'rdlu': CoordinateSystem('rdlu', 'br', 'left', 'up'),
    'rdul': CoordinateSystem('rdul', 'br', 'up', 'left'),
}


def detect_corner(moves: List[str], corner_size: int = 9) -> Optional[str]:
    """
    检测定式属于哪个角
    
    Args:
        moves: 坐标列表
        corner_size: 角大小，9、11 或 13（默认9）
    
    返回: 'tl', 'tr', 'bl', 'br' 或 None（无法判断）
    """
    valid_coords = [m for m in moves if m and m != 'pass' and m != 'tt' and len(m) == 2]
    if not valid_coords:
        return None
    
    corner_counts = {'tl': 0, 'tr': 0, 'bl': 0, 'br': 0}
    
    for coord in valid_coords:
        try:
            col, row = CoordinateSystem.sgf_to_nums(coord)
            if corner_size == 9:
                # 9路边界: 左上(0-8,0-8) 右上(10-18,0-8) 左下(0-8,10-18) 右下(10-18,10-18)
                if col <= 8 and row <= 8:
                    corner_counts['tl'] += 1
                elif col >= 10 and row <= 8:
                    corner_counts['tr'] += 1
                elif col <= 8 and row >= 10:
                    corner_counts['bl'] += 1
                elif col >= 10 and row >= 10:
                    corner_counts['br'] += 1
            elif corner_size == 11:
                # 11路边界: 左上(0-10,0-10) 右上(8-18,0-10) 左下(0-10,8-18) 右下(8-18,8-18)
                if col <= 10 and row <= 10:
                    corner_counts['tl'] += 1
                elif col >= 8 and row <= 10:
                    corner_counts['tr'] += 1
                elif col <= 10 and row >= 8:
                    corner_counts['bl'] += 1
                elif col >= 8 and row >= 8:
                    corner_counts['br'] += 1
            else:  # 13路
                # 13路边界: 左上(0-12,0-12) 右上(6-18,0-12) 左下(0-12,6-18) 右下(6-18,6-18)
                if col <= 12 and row <= 12:
                    corner_counts['tl'] += 1
                elif col >= 6 and row <= 12:
                    corner_counts['tr'] += 1
                elif col <= 12 and row >= 6:
                    corner_counts['bl'] += 1
                elif col >= 6 and row >= 6:
                    corner_counts['br'] += 1
        except:
            continue
    
    # 找出数量最多的角
    max_corner = max(corner_counts, key=corner_counts.get)
    if corner_counts[max_corner] > 0:
        return max_corner
    return None


def has_stone_in_corner_9lu(moves: List[str], corner_key: str) -> bool:
    """
    检查指定角的9路范围内是否有棋子
    
    Args:
        moves: 坐标序列
        corner_key: 角标识 ('tl', 'tr', 'bl', 'br')
    
    Returns:
        True 如果该角9路范围内有棋子
    """
    # 9路范围配置（各角不重叠）
    corner_9lu_ranges = {
        'tl': (0, 8, 0, 8),    # col 0-8, row 0-8
        'tr': (10, 18, 0, 8),  # col 10-18, row 0-8
        'bl': (0, 8, 10, 18),  # col 0-8, row 10-18
        'br': (10, 18, 10, 18) # col 10-18, row 10-18
    }
    
    cmin, cmax, rmin, rmax = corner_9lu_ranges.get(corner_key, (0, 0, 0, 0))
    
    for c in moves:
        if c and len(c) == 2 and c != 'pass' and c != 'tt':
            col = ord(c[0]) - ord('a')
            row = ord(c[1]) - ord('a')
            if cmin <= col <= cmax and rmin <= row <= rmax:
                return True
    return False


def convert_to_top_right(moves: List[str], source_corner: str) -> List[str]:
    """
    将定式坐标转换为右上角（视觉）的坐标
    
    Args:
        moves: 坐标序列
        source_corner: 源角位 ('tl', 'tr', 'bl', 'br')
    
    返回:
        转换后的坐标序列（右上角视角）
    """
    # 如果已经是右上角，无需转换
    if source_corner == 'tr':
        return moves
    
    # 源角对应的坐标系
    source_coord_sys = {
        'tl': COORDINATE_SYSTEMS['lurd'],  # 左上
        'bl': COORDINATE_SYSTEMS['ldru'],  # 左下
        'br': COORDINATE_SYSTEMS['rdlu'],  # 右下
    }.get(source_corner)
    
    if not source_coord_sys:
        return moves
    
    # 目标坐标系：右上角的 ruld（左→下）
    target_coord_sys = COORDINATE_SYSTEMS['ruld']
    
    converted = []
    for coord in moves:
        if not coord or coord == 'pass' or coord == 'tt':
            converted.append(coord)
            continue
        try:
            # 先转为局部坐标
            local_x, local_y = source_coord_sys._to_local_cache.get(coord, (0, 0))
            # 再用目标坐标系转回SGF
            new_coord = target_coord_sys._to_sgf_cache.get((local_x, local_y), coord)
            converted.append(new_coord)
        except:
            converted.append(coord)
    
    return converted


def normalize_corner_sequence(moves: List[str]) -> Tuple[List[str], bool]:
    """
    将ruld方向的着法序列标准化到对角线上方（靠近上边缘）
    
    以过右上角顶点的对角线(c+r=18)为对称轴：
    - c + r == 18: 着法在对角线上
    - c + r < 18:  上半部分（靠近上边缘），已是标准方向
    - c + r > 18:  下半部分（靠近左边缘），需要翻转
    
    Args:
        moves: ruld方向的SGF坐标列表
        
    Returns:
        (标准化后的着法序列, 是否被翻转)
    """
    for sgf in moves:
        if not sgf or sgf == 'pass' or sgf == 'tt' or len(sgf) != 2:
            continue
            
        c = ord(sgf[0]) - ord('a')  # 全局列 0-18
        r = ord(sgf[1]) - ord('a')  # 全局行 0-18
        
        coord_sum = c + r
        
        if coord_sum == 18:
            continue  # 在对角线上，继续判断下一个着法
        
        if coord_sum < 18:
            # 上半部分（靠近上边缘），已是标准方向
            return moves, False
        else:
            # 下半部分（靠近左边缘），需要翻转
            # 翻转操作: (c, r) -> (18-r, 18-c)
            from ..builder import convert_to_rudl
            return convert_to_rudl(moves), True
    
    # 所有着法都在对角线上，无需处理
    return moves, False
