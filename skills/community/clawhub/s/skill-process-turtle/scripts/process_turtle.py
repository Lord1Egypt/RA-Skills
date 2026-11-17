#!/usr/bin/env python3
"""
过程乌龟图工具 - 流程可视化生成器
支持: 乌龟图(5M1E)、泳道图、流程图、时间线
"""

import argparse
import json
import os
import sys
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, field

# 尝试导入cairosvg用于PNG导出
try:
    import cairosvg
    HAS_CAIRO = True
except ImportError:
    HAS_CAIRO = False


@dataclass
class Node:
    """流程节点"""
    id: str
    name: str
    type: str = "process"  # process, decision, start, end
    category: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "name": self.name, "type": self.type, "category": self.category}


@dataclass
class Edge:
    """流程连线"""
    from_node: str
    to_node: str
    label: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {"from": self.from_node, "to": self.to_node, "label": self.label}


@dataclass
class FlowConfig:
    """流程配置"""
    title: str = "流程图"
    template: str = "flowchart"
    nodes: List[Node] = field(default_factory=list)
    edges: List[Edge] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FlowConfig':
        nodes = [Node(**n) for n in data.get('nodes', [])]
        edges = [Edge(**e) for e in data.get('edges', [])]
        return cls(
            title=data.get('title', '流程图'),
            template=data.get('template', 'flowchart'),
            nodes=nodes,
            edges=edges
        )


class SVGGenerator:
    """SVG图形生成器"""
    
    # 基础样式
    STYLES = {
        'width': 1200,
        'height': 800,
        'padding': 60,
        'node_width': 160,
        'node_height': 60,
        'decision_size': 80,
        'radius': 8,
        'stroke_width': 2,
        'arrow_size': 10,
    }
    
    # 颜色主题
    COLORS = {
        'background': '#ffffff',
        'title': '#333333',
        'node': {
            'start': '#4CAF50',
            'end': '#F44336',
            'process': '#2196F3',
            'decision': '#FF9800',
        },
        'border': '#333333',
        'text': '#ffffff',
        'arrow': '#666666',
        'lane_header': '#E3F2FD',
        'lane_border': '#90CAF9',
        'turtle_center': '#9C27B0',
        'turtle_man': '#E91E63',
        'turtle_machine': '#00BCD4',
        'turtle_method': '#FF5722',
        'turtle_material': '#8BC34A',
        'turtle_measurement': '#FFC107',
        'turtle_environment': '#9E9E9E',
    }
    
    # 5M1E分类
    TURTLE_CATEGORIES = {
        'man': '人\n(Man)',
        'machine': '机\n(Machine)', 
        'method': '法\n(Method)',
        'material': '料\n(Material)',
        'measurement': '测\n(Measurement)',
        'environment': '环\n(Environment)',
    }
    
    def __init__(self, config: FlowConfig):
        self.config = config
        self.svg_parts: List[str] = []
        
    def _add(self, content: str):
        self.svg_parts.append(content)
    
    def _header(self) -> str:
        w, h = self.STYLES['width'], self.STYLES['height']
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<rect width="100%" height="100%" fill="{self.COLORS['background']}"/>'''
    
    def _footer(self) -> str:
        return '</svg>'
    
    def _title(self, text: str, x: int, y: int) -> str:
        return f'''<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="{self.COLORS['title']}" text-anchor="middle">{text}</text>'''
    
    def _node(self, x: int, y: int, name: str, node_type: str = 'process', color: str = None) -> str:
        w, h = self.STYLES['node_width'], self.STYLES['node_height']
        r = self.STYLES['radius']
        
        if color is None:
            color = self.COLORS['node'].get(node_type, self.COLORS['node']['process'])
        
        if node_type == 'start' or node_type == 'end':
            # 圆角矩形（开始/结束）
            return f'''<rect x="{x-w//2}" y="{y-h//2}" width="{w}" height="{h}" rx="{h//2}" ry="{h//2}" fill="{color}" stroke="{self.COLORS['border']}" stroke-width="{self.STYLES['stroke_width']}"/>
<text x="{x}" y="{y+5}" font-family="Arial, sans-serif" font-size="14" fill="{self.COLORS['text']}" text-anchor="middle">{name}</text>'''
        elif node_type == 'decision':
            # 菱形（判断）
            s = self.STYLES['decision_size']
            points = f"{x},{y-s//2} {x+s//2},{y} {x},{y+s//2} {x-s//2},{y}"
            return f'''<polygon points="{points}" fill="{color}" stroke="{self.COLORS['border']}" stroke-width="{self.STYLES['stroke_width']}"/>
<text x="{x}" y="{y+4}" font-family="Arial, sans-serif" font-size="12" fill="{self.COLORS['text']}" text-anchor="middle">{name}</text>'''
        else:
            # 普通矩形（处理）
            return f'''<rect x="{x-w//2}" y="{y-h//2}" width="{w}" height="{h}" rx="{r}" ry="{r}" fill="{color}" stroke="{self.COLORS['border']}" stroke-width="{self.STYLES['stroke_width']}"/>
<text x="{x}" y="{y+5}" font-family="Arial, sans-serif" font-size="14" fill="{self.COLORS['text']}" text-anchor="middle">{name}</text>'''
    
    def _arrow(self, x1: int, y1: int, x2: int, y2: int, label: str = "") -> str:
        """绘制带箭头的连线"""
        s = self.STYLES['arrow_size']
        
        # 计算方向向量
        dx, dy = x2 - x1, y2 - y1
        length = (dx**2 + dy**2)**0.5
        if length == 0:
            return ""
        
        # 归一化
        dx, dy = dx/length, dy/length
        
        # 计算箭头起点（稍微缩进避免重叠）
        ax1, ay1 = x1 + dx * 30, y1 + dy * 30
        ax2, ay2 = x2 - dx * 30, y2 - dy * 30
        
        # 箭头方向
        px, py = -dy, dx  # 垂直向量
        arrow_points = f"{ax2},{ay2} {ax2-s*dx-s*0.5*px},{ay2-s*dy-s*0.5*py} {ax2-s*dx+s*0.5*px},{ay2-s*dy+s*0.5*py}"
        
        svg = f'''<line x1="{ax1}" y1="{ay1}" x2="{ax2}" y2="{ay2}" stroke="{self.COLORS['arrow']}" stroke-width="{self.STYLES['stroke_width']}"/>
<polygon points="{arrow_points}" fill="{self.COLORS['arrow']}"/>'''
        
        if label:
            mx, my = (ax1 + ax2) / 2, (ay1 + ay2) / 2
            svg += f'''<text x="{mx}" y="{my-8}" font-family="Arial, sans-serif" font-size="11" fill="#666" text-anchor="middle">{label}</text>'''
        
        return svg
    
    def generate_turtle(self) -> str:
        """生成乌龟图 (5M1E)"""
        w, h = self.STYLES['width'], self.STYLES['height']
        cx, cy = w // 2, h // 2
        
        self._add(self._header())
        self._add(self._title(self.config.title, cx, 40))
        
        # 中心节点
        center_color = self.COLORS['turtle_center']
        self._add(f'''<ellipse cx="{cx}" cy="{cy}" rx="80" ry="50" fill="{center_color}" stroke="{self.COLORS['border']}" stroke-width="3"/>
<text x="{cx}" y="{cy+5}" font-family="Arial, sans-serif" font-size="16" fill="white" text-anchor="middle" font-weight="bold">{self.config.title}</text>''')
        
        # 六个分支方向
        angles = [0, 60, 120, 180, 240, 300]  # 从顶部开始，顺时针
        keys = ['man', 'machine', 'method', 'material', 'measurement', 'environment']
        radius = 280
        
        # 分支节点
        for angle, key in zip(angles, keys):
            rad = -angle * 3.14159 / 180
            nx = int(cx + radius * ( -1 if angle > 90 and angle < 270 else 1) * abs(rad - 3.14159/2 if abs(rad) > 0.01 else rad))
            ny = int(cy + radius * (1 if abs(rad) < 0.01 else (1 if abs(rad - 3.14159) < 0.01 else -1 if abs(rad - 3.14159/2) < 0.01 or abs(rad + 3.14159/2) < 0.01 else (1 if angle < 180 else -1))))
        
        # 重新计算位置
        positions = []
        for i, (angle, key) in enumerate(zip(angles, keys)):
            rad = (angle - 90) * 3.14159 / 180
            nx = int(cx + radius * (1 if angle <= 90 or angle >= 270 else -1) * abs(3.14159/2 - rad) / (3.14159/2))
            ny = int(cy + radius * (-1 if angle == 0 else (1 if angle <= 180 else -1)) * abs(rad) / abs(rad) if rad != 0 else -radius)
        
        # 简化的位置计算
        positions = [
            (cx, cy - radius),        # 上 - man
            (cx + radius*0.866, cy - radius*0.5),  # 右上 - machine  
            (cx + radius*0.866, cy + radius*0.5),   # 右下 - method
            (cx, cy + radius),         # 下 - material
            (cx - radius*0.866, cy + radius*0.5),  # 左下 - measurement
            (cx - radius*0.866, cy - radius*0.5),   # 左上 - environment
        ]
        
        colors = [
            self.COLORS['turtle_man'],
            self.COLORS['turtle_machine'],
            self.COLORS['turtle_method'],
            self.COLORS['turtle_material'],
            self.COLORS['turtle_measurement'],
            self.COLORS['turtle_environment'],
        ]
        
        # 绘制分支和节点
        for i, ((angle, key), (nx, ny), color) in enumerate(zip(zip(angles, keys), positions, colors)):
            # 连线到中心
            self._add(self._arrow(cx, cy, nx, ny))
            
            # 分支标签
            label = self.TURTLE_CATEGORIES.get(key, key)
            
            # 分支节点 - 使用椭圆
            self._add(f'''<ellipse cx="{nx}" cy="{ny}" rx="70" ry="45" fill="{color}" stroke="{self.COLORS['border']}" stroke-width="2"/>
<text x="{nx}" y="{ny-8}" font-family="Arial, sans-serif" font-size="12" fill="white" text-anchor="middle" font-weight="bold">{label.split(chr(10))[0]}</text>
<text x="{nx}" y="{ny+8}" font-family="Arial, sans-serif" font-size="12" fill="white" text-anchor="middle" font-weight="bold">{label.split(chr(10))[1] if chr(10) in label else ''}</text>''')
        
        # 如果有自定义节点，按类别分组显示
        if self.config.nodes:
            self._add('<g id="custom-nodes">')
            start_y = h - 120
            col = 0
            row = 0
            max_cols = 6
            
            for node in self.config.nodes:
                if node.category in keys:
                    cat_idx = keys.index(node.category)
                    bx, by = positions[cat_idx]
                    # 在分支节点下方显示详细项
                    item_x = bx + (col % 3 - 1) * 120
                    item_y = by + 70 + row * 40
                    if col % 3 == 2:
                        row += 1
                    col += 1
                    
                    self._add(f'''<rect x="{item_x-50}" y="{item_y-15}" width="100" height="30" rx="4" fill="white" stroke="{colors[cat_idx]}" stroke-width="1"/>
<text x="{item_x}" y="{item_y+4}" font-family="Arial, sans-serif" font-size="11" fill="#333" text-anchor="middle">{node.name}</text>''')
            self._add('</g>')
        
        self._add(self._footer())
        return '\n'.join(self.svg_parts)
    
    def generate_swimlane(self) -> str:
        """生成泳道图"""
        w, h = self.STYLES['height'], self.STYLES['width']  # 横向布局
        cfg_w, cfg_h = self.STYLES['width'], self.STYLES['height']
        
        self._add(self._header())
        self._add(self._title(self.config.title, cfg_w // 2, 40))
        
        # 获取所有泳道
        lanes = set()
        for node in self.config.nodes:
            if node.category:
                lanes.add(node.category)
        if not lanes:
            lanes = {'流程'}
        
        lanes = list(lanes)
        n_lanes = len(lanes)
        
        # 布局参数
        header_h = 50
        lane_w = (cfg_w - 120) // n_lanes
        start_y = 80
        node_h = self.STYLES['node_height']
        
        # 绘制泳道
        for i, lane in enumerate(lanes):
            x = 60 + i * lane_w
            self._add(f'''<rect x="{x}" y="{start_y}" width="{lane_w-5}" height="{cfg_h-start_y-60}" fill="{self.COLORS['lane_header']}" stroke="{self.COLORS['lane_border']}" stroke-width="2"/>
<text x="{x + lane_w//2}" y="{start_y+30}" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#333" text-anchor="middle">{lane}</text>''')
        
        # 绘制节点
        node_positions = {}
        for lane_idx, lane in enumerate(lanes):
            lane_nodes = [n for n in self.config.nodes if n.category == lane]
            for j, node in enumerate(lane_nodes):
                x = 60 + lane_idx * lane_w + lane_w // 2
                y = start_y + 80 + j * (node_h + 30)
                self._add(self._node(x, y, node.name, node.type))
                node_positions[node.id] = (x, y)
        
        # 绘制连线
        for edge in self.config.edges:
            if edge.from_node in node_positions and edge.to_node in node_positions:
                x1, y1 = node_positions[edge.from_node]
                x2, y2 = node_positions[edge.to_node]
                self._add(self._arrow(x1, y1, x2, y2, edge.label))
        
        self._add(self._footer())
        return '\n'.join(self.svg_parts)
    
    def generate_flowchart(self) -> str:
        """生成标准流程图"""
        cfg_w, cfg_h = self.STYLES['width'], self.STYLES['height']
        
        self._add(self._header())
        self._add(self._title(self.config.title, cfg_w // 2, 40))
        
        if not self.config.nodes:
            self._add(self._footer())
            return '\n'.join(self.svg_parts)
        
        # 拓扑排序确定顺序
        sorted_nodes = self._topological_sort()
        
        # 布局
        node_w = self.STYLES['node_width']
        node_h = self.STYLES['node_height']
        h_gap = 100
        v_gap = 80
        
        # 计算节点位置
        positions = {}
        x = 100
        y = 120
        
        for i, node in enumerate(sorted_nodes):
            # 判断节点类型决定宽度
            if node.type == 'decision':
                positions[node.id] = (x, y)
                y += v_gap + 40
            else:
                positions[node.id] = (x, y)
                y += v_gap + node_h // 2
                
                # 绘制连线
                for edge in self.config.edges:
                    if edge.from_node == node.id and edge.to_node in positions:
                        x1, y1 = positions[node.id]
                        x2, y2 = positions[edge.to_node]
                        self._add(self._arrow(x1, y1 + node_h//2, x2, y2 - node_h//2, edge.label))
            
            x += h_gap + node_w
        
        # 绘制节点
        for node in sorted_nodes:
            x, y = positions[node.id]
            self._add(self._node(x, y, node.name, node.type))
        
        self._add(self._footer())
        return '\n'.join(self.svg_parts)
    
    def generate_timeline(self) -> str:
        """生成时间线图"""
        cfg_w, cfg_h = self.STYLES['width'], self.STYLES['height']
        
        self._add(self._header())
        self._add(self._title(self.config.title, cfg_w // 2, 40))
        
        if not self.config.nodes:
            self._add(self._footer())
            return '\n'.join(self.svg_parts)
        
        # 水平时间线
        line_y = cfg_h // 2
        start_x = 100
        end_x = cfg_w - 100
        n_nodes = len(self.config.nodes)
        gap = (end_x - start_x) // max(n_nodes - 1, 1)
        
        # 绘制主线
        self._add(f'''<line x1="{start_x-20}" y1="{line_y}" x2="{end_x+20}" y2="{line_y}" stroke="{self.COLORS['border']}" stroke-width="3"/>''')
        
        # 绘制节点
        for i, node in enumerate(self.config.nodes):
            x = start_x + i * gap
            
            # 节点圆点
            color = self.COLORS['node'].get(node.type, self.COLORS['node']['process'])
            self._add(f'''<circle cx="{x}" cy="{line_y}" r="15" fill="{color}" stroke="{self.COLORS['border']}" stroke-width="2"/>''')
            
            # 标签在节点上方或下方交替
            label_y = line_y - 40 if i % 2 == 0 else line_y + 55
            self._add(f'''<text x="{x}" y="{label_y}" font-family="Arial, sans-serif" font-size="12" fill="#333" text-anchor="middle">{node.name}</text>''')
            
            # 连接线
            self._add(f'''<line x1="{x}" y1="{line_y-15 if i % 2 == 0 else line_y+15}" x2="{x}" y2="{label_y+5 if i % 2 == 0 else label_y-10}" stroke="{self.COLORS['arrow']}" stroke-width="1"/>''')
            
            # 序号
            self._add(f'''<text x="{x}" y="{line_y+5}" font-family="Arial, sans-serif" font-size="10" fill="white" text-anchor="middle">{i+1}</text>''')
        
        # 绘制箭头
        self._add(f'''<polygon points="{end_x+20},{line_y} {end_x},{line_y-8} {end_x},{line_y+8}" fill="{self.COLORS['border']}"/>''')
        
        self._add(self._footer())
        return '\n'.join(self.svg_parts)
    
    def _topological_sort(self) -> List[Node]:
        """拓扑排序确定节点顺序"""
        if not self.config.nodes:
            return []
        
        # 构建邻接表
        in_degree = {n.id: 0 for n in self.config.nodes}
        adj = {n.id: [] for n in self.config.nodes}
        
        for edge in self.config.edges:
            if edge.from_node in adj and edge.to_node in adj:
                adj[edge.from_node].append(edge.to_node)
                in_degree[edge.to_node] += 1
        
        # 找到入度为0的节点
        queue = [n for n in self.config.nodes if in_degree[n.id] == 0]
        result = []
        
        while queue:
            node = queue.pop(0)
            result.append(node)
            for next_id in adj[node.id]:
                in_degree[next_id] -= 1
                if in_degree[next_id] == 0:
                    for n in self.config.nodes:
                        if n.id == next_id:
                            queue.append(n)
                            break
        
        # 如果有环，返回原顺序
        if len(result) != len(self.config.nodes):
            return self.config.nodes
        return result
    
    def generate(self, template: str = None) -> str:
        """根据模板生成SVG"""
        t = template or self.config.template
        
        if t == 'turtle':
            return self.generate_turtle()
        elif t == 'swimlane':
            return self.generate_swimlane()
        elif t == 'timeline':
            return self.generate_timeline()
        else:
            return self.generate_flowchart()


def load_config(config_path: str) -> FlowConfig:
    """加载JSON配置"""
    with open(config_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return FlowConfig.from_dict(data)


def save_svg(content: str, output_path: str):
    """保存SVG文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)


def save_png(svg_content: str, output_path: str):
    """保存PNG文件"""
    if not HAS_CAIRO:
        print("Warning: cairosvg not installed, PNG export skipped")
        print("Install with: pip install cairosvg")
        return False
    
    # 将.svg改为.png
    png_path = output_path.rsplit('.', 1)[0] + '.png'
    cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), write_to=png_path)
    return True


def main():
    parser = argparse.ArgumentParser(description='过程乌龟图工具 - 流程可视化生成器')
    parser.add_argument('--config', '-c', required=True, help='JSON配置文件路径')
    parser.add_argument('--type', '-t', choices=['turtle', 'swimlane', 'flowchart', 'timeline'], 
                        help='模板类型(覆盖配置文件)')
    parser.add_argument('--output', '-o', help='输出文件名(不含扩展名)')
    parser.add_argument('--format', '-f', choices=['svg', 'png', 'both'], default='svg',
                        help='输出格式')
    
    args = parser.parse_args()
    
    # 加载配置
    try:
        config = load_config(args.config)
    except FileNotFoundError:
        print(f"Error: Config file not found: {args.config}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}")
        sys.exit(1)
    
    # 确定输出文件名
    output_name = args.output or config.title.replace(' ', '_')
    
    # 确定模板类型
    template = args.type or config.template
    
    # 生成SVG
    generator = SVGGenerator(config)
    svg_content = generator.generate(template)
    
    # 保存SVG
    svg_path = f"{output_name}.svg"
    save_svg(svg_content, svg_path)
    print(f"SVG saved: {svg_path}")
    
    # 保存PNG
    if args.format in ['png', 'both']:
        if save_png(svg_content, svg_path):
            png_path = f"{output_name}.png"
            print(f"PNG saved: {png_path}")
    
    # 输出结果JSON
    result = {
        "status": "success",
        "template": template,
        "svg_path": svg_path,
        "png_path": f"{output_name}.png" if args.format in ['png', 'both'] and HAS_CAIRO else None,
        "node_count": len(config.nodes),
        "edge_count": len(config.edges)
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
