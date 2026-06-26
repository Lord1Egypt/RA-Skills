#!/usr/bin/env python3
"""
连通块检测器
基于距离阈值的连通块查找和筛选
"""

from typing import List, Tuple, Set, Dict
from collections import deque


class ConnectedComponent:
    """连通块"""
    def __init__(self, positions: Set[Tuple[int, int]], corner_origin: Tuple[int, int]):
        self.positions = positions
        self.corner_origin = corner_origin  # 角的原点坐标
        self._nearest_pos = None
        self._min_distance = None
    
    @property
    def size(self) -> int:
        """连通块大小（棋子数）"""
        return len(self.positions)
    
    @property
    def nearest_to_corner(self) -> Tuple[int, int]:
        """找到连通块中离角最近的点"""
        if self._nearest_pos is None:
            min_dist = float('inf')
            nearest = None
            cx, cy = self.corner_origin
            for pos in self.positions:
                px, py = pos
                # 曼哈顿距离
                dist = abs(px - cx) + abs(py - cy)
                if dist < min_dist:
                    min_dist = dist
                    nearest = pos
            self._nearest_pos = nearest
            self._min_distance = min_dist
        return self._nearest_pos
    
    @property
    def distance_to_corner(self) -> int:
        """连通块离角的距离"""
        if self._min_distance is None:
            _ = self.nearest_to_corner
        return self._min_distance


def find_connected_components(
    positions: List[Tuple[int, int]], 
    corner_origin: Tuple[int, int],
    distance_threshold: int = 4
) -> List[ConnectedComponent]:
    """
    从位置列表中查找连通块
    
    算法：
    1. 八连通找基础连通块（上下左右 + 4个对角线方向相邻视为连通）
    2. 合并相近的块（块间最小距离 <= distance_threshold）
    3. 返回所有连通块
    
    说明：八连通是指一个棋子的8个邻接位置（上、下、左、右、左上、右上、左下、右下）
          如果相邻位置有棋子，则认为这两个棋子属于同一个连通块
    
    Args:
        positions: 棋子位置列表 [(col, row), ...]
        corner_origin: 角的原点坐标 (col, row)
        distance_threshold: 块间合并距离阈值（默认4）
    
    Returns:
        连通块列表
    """
    if not positions:
        return []
    
    # 步骤1: 八连通找基础连通块
    pos_set = set(positions)
    visited = set()
    components = []
    
    # 八邻域方向
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    for start_pos in positions:
        if start_pos in visited:
            continue
        
        # BFS找连通块
        component_pos = set()
        queue = deque([start_pos])
        visited.add(start_pos)
        
        while queue:
            curr = queue.popleft()
            component_pos.add(curr)
            cx, cy = curr
            
            for dx, dy in directions:
                neighbor = (cx + dx, cy + dy)
                if neighbor in pos_set and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        components.append(ConnectedComponent(component_pos, corner_origin))
    
    # 步骤2: 合并相近的块
    if len(components) > 1:
        components = _merge_close_components(components, distance_threshold)
    
    return components


def _merge_close_components(
    components: List[ConnectedComponent], 
    threshold: int
) -> List[ConnectedComponent]:
    """
    合并距离相近的连通块
    
    如果两个连通块之间的最小距离 <= threshold，则合并
    """
    if not components:
        return components
    
    n = len(components)
    parent = list(range(n))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
    
    # 计算所有连通块间的距离，合并相近的
    for i in range(n):
        for j in range(i + 1, n):
            dist = _component_distance(components[i], components[j])
            if dist <= threshold:
                union(i, j)
    
    # 按合并结果分组
    groups: Dict[int, Set[Tuple[int, int]]] = {}
    for i, comp in enumerate(components):
        root = find(i)
        if root not in groups:
            groups[root] = set()
        groups[root].update(comp.positions)
    
    # 重新创建连通块对象
    corner_origin = components[0].corner_origin
    return [ConnectedComponent(positions, corner_origin) for positions in groups.values()]


def _component_distance(c1: ConnectedComponent, c2: ConnectedComponent) -> int:
    """计算两个连通块之间的最小曼哈顿距离"""
    min_dist = float('inf')
    for p1 in c1.positions:
        for p2 in c2.positions:
            dist = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
            min_dist = min(min_dist, dist)
    return min_dist


def filter_nearest_component(components: List[ConnectedComponent]) -> Set[Tuple[int, int]]:
    """
    仅保留离角最近的连通块

    Args:
        components: 连通块列表

    Returns:
        最近连通块的位置集合
    """
    if not components:
        return set()

    # 找到离角最近的连通块
    nearest_comp = min(components, key=lambda c: c.distance_to_corner)
    return nearest_comp.positions


def _find_temporal_core(
    positions: Set[Tuple[int, int]],
    moves: List[Tuple[str, str]],
    max_distance: int = 4
) -> Tuple[Set[Tuple[int, int]], Set[Tuple[int, int]]]:
    """
    基于行棋时序确定核心定式区域

    从第一手开始维护活跃区域，后续着法如果距离活跃区域 <= max_distance
    则将其位置加入核心区域。用于筛选最终的局面连通块。

    Args:
        positions: 候选位置集合（如13路连通块）
        moves: [(color, coord), ...] 着法序列
        max_distance: 时序连通距离阈值

    Returns:
        (core_positions, discarded_positions)
        core_positions: 核心区域位置集合
        discarded_positions: 被标记为脱先的位置集合（用于后续回退判断）
    """
    from ..core.coords import CoordinateSystem

    core_positions = set()
    discarded_positions = set()
    active_positions = set()

    for color, coord in moves:
        if coord == 'tt' or not coord or len(coord) != 2:
            continue

        try:
            col, row = CoordinateSystem.sgf_to_nums(coord)
        except:
            continue

        # 只处理在候选位置内的着法
        if (col, row) not in positions:
            continue

        if not active_positions:
            # 第一手，加入核心
            active_positions.add((col, row))
            core_positions.add((col, row))
        else:
            # 计算到活跃区域的最小曼哈顿距离
            min_dist = min(
                abs(col - pc) + abs(row - pr)
                for (pc, pr) in active_positions
            )

            if min_dist <= max_distance:
                active_positions.add((col, row))
                core_positions.add((col, row))
            else:
                # 标记为脱先，记录下来
                discarded_positions.add((col, row))

    return core_positions, discarded_positions


def _convex_hull(points: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    计算凸包（单调链算法）
    
    Args:
        points: 点集 [(x, y), ...]
    
    Returns:
        凸包顶点列表（逆时针顺序）
    """
    if len(points) <= 1:
        return points
    
    # 去重并排序
    points = sorted(set(points))
    
    if len(points) <= 2:
        return points
    
    def cross(o, a, b):
        """叉积"""
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    # 下半部分
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    
    # 上半部分
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    
    # 合并（去掉重复端点）
    return lower[:-1] + upper[:-1]


def _point_in_polygon(point: Tuple[int, int], polygon: List[Tuple[int, int]]) -> bool:
    """
    判断点是否在多边形内（射线法，包含边界）
    
    Args:
        point: (x, y)
        polygon: 多边形顶点列表
    
    Returns:
        True 如果在多边形内或边界上
    """
    if not polygon:
        return False
    
    if len(polygon) == 1:
        return point == polygon[0]
    
    if len(polygon) == 2:
        # 线段：检查点是否在线段上
        x, y = point
        x1, y1 = polygon[0]
        x2, y2 = polygon[1]
        # 共线且在线段范围内
        cross = (x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)
        if cross != 0:
            return False
        dot = (x - x1) * (x - x2) + (y - y1) * (y - y2)
        return dot <= 0  # 在线段上或端点
    
    # 射线法
    x, y = point
    n = len(polygon)
    inside = False
    
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        
        # 检查点是否在边上
        # 共线检查
        cross = (x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)
        if cross == 0:
            # 检查是否在线段范围内
            if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
                return True  # 在边界上
        
        # 射线交叉检查
        if ((y1 > y) != (y2 > y)):
            intersect_x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x <= intersect_x:
                inside = not inside
    
    return inside


def _extract_corner_moves_lu(
    moves: List[Tuple[str, str]],
    corner_key: str,
    lu_size: int,
    distance_threshold: int = 4
) -> Tuple[List[Tuple[str, str]], Set[Tuple[int, int]], Set[Tuple[int, int]]]:
    """
    通用N路角提取（返回结果、核心位置、被剔除位置）
    
    Args:
        moves: 着法序列
        corner_key: 角标识
        lu_size: 路数（9/11/13）
        distance_threshold: 连通块阈值
    
    Returns:
        (result_moves, core_positions, discarded_positions)
    """
    from ..core.coords import CoordinateSystem
    
    # N路范围配置
    ranges = {
        9: {
            'tl': ((0, 8), (0, 8)),
            'tr': ((10, 18), (0, 8)),
            'bl': ((0, 8), (10, 18)),
            'br': ((10, 18), (10, 18)),
        },
        11: {
            'tl': ((0, 10), (0, 10)),
            'tr': ((8, 18), (0, 10)),
            'bl': ((0, 10), (8, 18)),
            'br': ((8, 18), (8, 18)),
        },
        13: {
            'tl': ((0, 12), (0, 12)),
            'tr': ((6, 18), (0, 12)),
            'bl': ((0, 12), (6, 18)),
            'br': ((6, 18), (6, 18)),
        }
    }
    
    if lu_size not in ranges:
        return [], set(), set()
    
    config = ranges[lu_size].get(corner_key)
    if not config:
        return [], set(), set()
    
    (col_min, col_max), (row_min, row_max) = config
    
    # 收集N路范围内的着法
    corner_moves = []
    for color, coord in moves:
        if coord == 'tt' or not coord or len(coord) != 2:
            continue
        try:
            col, row = CoordinateSystem.sgf_to_nums(coord)
            if col_min <= col <= col_max and row_min <= row <= row_max:
                corner_moves.append((color, coord))
        except:
            continue
    
    if not corner_moves:
        return [], set(), set()
    
    # 收集所有位置
    all_positions = set()
    for color, coord in corner_moves:
        col, row = CoordinateSystem.sgf_to_nums(coord)
        all_positions.add((col, row))
    
    # 时序连通性分析
    core_positions, discarded_positions = _find_temporal_core(
        all_positions, corner_moves, max_distance=4
    )
    
    # 构建结果
    result = []
    last_color = None
    for color, coord in corner_moves:
        col, row = CoordinateSystem.sgf_to_nums(coord)
        if (col, row) in core_positions:
            if last_color == color:
                pass_color = 'W' if color == 'B' else 'B'
                result.append((pass_color, 'tt'))
            result.append((color, coord))
            last_color = color
    
    return result, core_positions, discarded_positions


def extract_corner_moves_9lu(
    moves: List[Tuple[str, str]],
    corner_key: str,
    distance_threshold: int = 4
) -> List[Tuple[str, str]]:
    """
    提取指定角的着法（9路范围，最终回退方案）
    
    只做局面连通性过滤（不做时序过滤）：
    1. 收集9路范围内的所有棋子
    2. 找连通块，取离角最近的
    3. 保留该连通块内的所有棋子（含脱先后回归）
    """
    from ..core.coords import CoordinateSystem
    
    # 9路范围配置
    corner_config = {
        'tl': {'col_range': (0, 8), 'row_range': (0, 8), 'origin': (0, 0)},
        'tr': {'col_range': (10, 18), 'row_range': (0, 8), 'origin': (18, 0)},
        'bl': {'col_range': (0, 8), 'row_range': (10, 18), 'origin': (0, 18)},
        'br': {'col_range': (10, 18), 'row_range': (10, 18), 'origin': (18, 18)},
    }
    
    config = corner_config.get(corner_key)
    if not config:
        return []
    
    col_min, col_max = config['col_range']
    row_min, row_max = config['row_range']
    origin = config['origin']
    
    # 收集9路范围内的棋子位置和对应着法
    corner_positions = []
    corner_moves_map = {}  # (col,row) -> [(color, coord), ...]
    
    for color, coord in moves:
        if coord == 'tt' or not coord or len(coord) != 2:
            continue
        try:
            col, row = CoordinateSystem.sgf_to_nums(coord)
            if col_min <= col <= col_max and row_min <= row <= row_max:
                corner_positions.append((col, row))
                if (col, row) not in corner_moves_map:
                    corner_moves_map[(col, row)] = []
                corner_moves_map[(col, row)].append((color, coord))
        except:
            continue
    
    if not corner_positions:
        return []
    
    # 找连通块并筛选最近的（局面连通性）
    components = find_connected_components(corner_positions, origin, distance_threshold)
    valid_positions = filter_nearest_component(components)
    
    if not valid_positions:
        return []
    
    # 构建结果（不过滤时序，保留所有在连通块内的着法）
    result = []
    last_color = None
    
    for color, coord in moves:
        if coord == 'tt' or not coord or len(coord) != 2:
            continue
        try:
            col, row = CoordinateSystem.sgf_to_nums(coord)
            if (col, row) in valid_positions:
                # 检测脱先
                if last_color == color:
                    pass_color = 'W' if color == 'B' else 'B'
                    result.append((pass_color, 'tt'))
                result.append((color, coord))
                last_color = color
        except:
            continue
    
    return result


def extract_corner_moves(
    moves: List[Tuple[str, str]], 
    corner_key: str,
    distance_threshold: int = 4
) -> List[Tuple[str, str]]:
    """
    提取指定角的着法（含脱先标记）
    
    Args:
        moves: [(color, coord), ...] 完整着法序列
        corner_key: 角标识 ('tl', 'tr', 'bl', 'br')
        distance_threshold: 连通块合并距离阈值
    
    Returns:
        处理后的着法序列（含tt脱先标记）
    """
    from ..core.coords import CoordinateSystem
    
    # 定义四角的13路范围（左上角原点）和角的原点
    corner_config = {
        'tl': {'col_range': (0, 12), 'row_range': (0, 12), 'origin': (0, 0)},
        'tr': {'col_range': (6, 18), 'row_range': (0, 12), 'origin': (18, 0)},
        'bl': {'col_range': (0, 12), 'row_range': (6, 18), 'origin': (0, 18)},
        'br': {'col_range': (6, 18), 'row_range': (6, 18), 'origin': (18, 18)},
    }
    
    config = corner_config.get(corner_key)
    if not config:
        return []
    
    col_min, col_max = config['col_range']
    row_min, row_max = config['row_range']
    origin = config['origin']
    
    # 收集13路范围内的所有棋子位置
    corner_positions = []
    for color, coord in moves:
        if coord == 'tt' or not coord or len(coord) != 2:
            continue
        try:
            col, row = CoordinateSystem.sgf_to_nums(coord)
            if col_min <= col <= col_max and row_min <= row <= row_max:
                corner_positions.append((col, row))
        except:
            continue
    
    if not corner_positions:
        return []
    
    # 多级回退策略：13路 → 11路 → 9路
    # 1. 先尝试13路
    result_13, core_13, discarded_13 = _extract_corner_moves_lu(
        moves, corner_key, 13, distance_threshold
    )
    
    # 检查13路是否需要回退（被剔除的着法在凸包内）
    should_fallback_13 = False
    if discarded_13 and core_13:
        hull_13 = _convex_hull(list(core_13))
        for disc_pos in discarded_13:
            if _point_in_polygon(disc_pos, hull_13):
                should_fallback_13 = True
                break
    
    if not should_fallback_13:
        return result_13
    
    # 2. 回退到11路
    result_11, core_11, discarded_11 = _extract_corner_moves_lu(
        moves, corner_key, 11, distance_threshold
    )
    
    # 检查11路是否需要回退
    should_fallback_11 = False
    if discarded_11 and core_11:
        hull_11 = _convex_hull(list(core_11))
        for disc_pos in discarded_11:
            if _point_in_polygon(disc_pos, hull_11):
                should_fallback_11 = True
                break
    
    if not should_fallback_11:
        return result_11
    
    # 3. 最终回退到9路
    return extract_corner_moves_9lu(moves, corner_key, distance_threshold)
