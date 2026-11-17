#!/usr/bin/env python3
"""
故障树可视化脚本
生成故障树图形（PNG/SVG格式）
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from graphviz import Digraph
except ImportError:
    print(json.dumps({"status": "error", "message": "请安装 graphviz: pip install graphviz"}))
    sys.exit(1)


def load_fta_data(input_path):
    """加载FTA数据文件"""
    path = Path(input_path)
    suffix = path.suffix.lower()
    
    if suffix == '.json':
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    elif suffix in ['.yaml', '.yml']:
        try:
            import yaml
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except ImportError:
            print(json.dumps({"status": "error", "message": "请安装 pyyaml: pip install pyyaml"}))
            sys.exit(1)
    else:
        raise ValueError(f"不支持的文件格式: {suffix}")


def get_node_label(node):
    """生成节点标签"""
    label = f"{node['name']}"
    if node['type'] == 'basic' and 'probability' in node:
        prob = node['probability']
        label += f"\n(p={prob:.4f})"
    return label


def get_node_shape(node_type):
    """获取节点形状"""
    shapes = {
        'basic': 'box',
        'intermediate': 'diamond',
        'and': 'triangle',
        'or': 'diamond'
    }
    return shapes.get(node_type, 'ellipse')


def get_node_color(node_type):
    """获取节点颜色"""
    colors = {
        'basic': '#E74C3C',
        'intermediate': '#3498DB',
        'and': '#27AE60',
        'or': '#F39C12'
    }
    return colors.get(node_type, '#95A5A6')


def validate_fta_data(data):
    """验证FTA数据"""
    errors = []
    
    if 'top_event' not in data:
        errors.append("E003: 缺少 top_event 字段")
    
    if 'nodes' not in data:
        errors.append("节点定义缺失")
        return errors
    
    nodes = data.get('nodes', {})
    top_event = data.get('top_event')
    
    if top_event and top_event not in nodes:
        errors.append(f"E003: 顶事件 '{top_event}' 未定义")
    
    for node_id, node in nodes.items():
        if 'type' not in node:
            errors.append(f"节点 '{node_id}' 缺少 type 字段")
        
        if node.get('type') == 'basic':
            if 'probability' not in node:
                errors.append(f"E002: 基本事件 '{node_id}' 缺少 probability 字段")
            elif not (0 <= node['probability'] <= 1):
                errors.append(f"E007: 节点 '{node_id}' 概率值超出范围 [0,1]")
        
        if 'name' not in node:
            errors.append(f"节点 '{node_id}' 缺少 name 字段")
    
    node_ids = set(nodes.keys())
    for edge in data.get('edges', []):
        if edge.get('from') not in node_ids:
            errors.append(f"E005: 边引用了未定义的节点 '{edge.get('from')}'")
        if edge.get('to') not in node_ids:
            errors.append(f"E005: 边引用了未定义的节点 '{edge.get('to')}'")
    
    return errors


def check_cycle(data):
    """检查是否有循环引用"""
    nodes = data.get('nodes', {})
    edges = data.get('edges', [])
    
    graph = {node_id: [] for node_id in nodes}
    for edge in edges:
        if edge.get('from') in graph and edge.get('to') in graph:
            graph[edge['from']].append(edge['to'])
    
    visited = set()
    rec_stack = set()
    
    def has_cycle(node):
        visited.add(node)
        rec_stack.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                if has_cycle(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
        rec_stack.remove(node)
        return False
    
    for node in nodes:
        if node not in visited:
            if has_cycle(node):
                return True
    return False


def visualize_fta(data, output_path, img_format='png'):
    """生成故障树可视化"""
    dot = Digraph(comment=data.get('name', 'Fault Tree Analysis'))
    dot.attr(rankdir='TB', size='10,12', dpi='150')
    dot.attr('node', fontname='SimHei', fontsize='10')
    dot.attr('edge', fontname='SimHei', fontsize='9')
    
    if 'name' in data:
        dot.attr(label=f'故障树分析: {data["name"]}')
    
    nodes = data.get('nodes', {})
    
    for node_id, node in nodes.items():
        shape = get_node_shape(node['type'])
        color = get_node_color(node['type'])
        label = get_node_label(node)
        
        style = 'filled' if node['type'] in ['basic', 'and', 'or'] else ''
        fontcolor = 'white' if node['type'] == 'basic' else 'black'
        
        if node['type'] in ['and', 'or']:
            label = f"{node['name']}\n({node['type'].upper()})"
        
        dot.node(node_id, label, shape=shape, style=style, 
                 fillcolor=color if node['type'] in ['basic', 'and', 'or'] else None,
                 fontcolor=fontcolor if node['type'] == 'basic' else None,
                 color='#2C3E50', penwidth='2')
    
    for edge in data.get('edges', []):
        from_node = edge.get('from')
        to_node = edge.get('to')
        if from_node in nodes and to_node in nodes:
            dot.edge(from_node, to_node, color='#34495E', penwidth='1.5')
    
    dot.render(output_path.replace(f'.{img_format}', ''), format=img_format, cleanup=True)
    return output_path


def main():
    parser = argparse.ArgumentParser(description='故障树可视化工具')
    parser.add_argument('--input', '-i', required=True, help='输入FTA数据文件(JSON/YAML)')
    parser.add_argument('--output', '-o', required=True, help='输出图形文件路径')
    parser.add_argument('--format', '-f', default='png', choices=['png', 'svg', 'pdf'], 
                        help='输出格式(默认png)')
    
    args = parser.parse_args()
    
    try:
        data = load_fta_data(args.input)
        
        errors = validate_fta_data(data)
        if errors:
            print(json.dumps({"status": "error", "errors": errors}, ensure_ascii=False))
            sys.exit(1)
        
        if check_cycle(data):
            print(json.dumps({"status": "error", "errors": ["E006: 检测到循环引用"]}))
            sys.exit(1)
        
        output_path = visualize_fta(data, args.output, args.format)
        
        print(json.dumps({
            "status": "success",
            "output": output_path,
            "node_count": len(data.get('nodes', {})),
            "edge_count": len(data.get('edges', []))
        }, ensure_ascii=False))
        
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)


if __name__ == '__main__':
    main()
