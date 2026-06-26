#!/usr/bin/env python3
"""航点管理器 - 保存和加载命名航点"""

import json
import argparse
from pathlib import Path

DEFAULT_WAYPOINTS_FILE = Path(__file__).parent.parent / 'waypoints.json'

def load_waypoints(filepath=None):
    """加载航点文件"""
    if filepath is None:
        filepath = DEFAULT_WAYPOINTS_FILE
    
    if not filepath.exists():
        return {}
    
    with open(filepath, 'r') as f:
        data = json.load(f)
        # 支持两种格式：直接是航点字典 或 包含 waypoints 键
        if isinstance(data, dict) and 'waypoints' in data:
            return data['waypoints']
        return data

def save_waypoints(waypoints, filepath=None):
    """保存航点文件"""
    if filepath is None:
        filepath = DEFAULT_WAYPOINTS_FILE
    
    # 保留原有注释和结构
    data = {
        '_comment': 'ROS Navigation Waypoints - 保存常用位置',
        '_usage': '使用 waypoints_manager.py add/list/get/remove 管理航点',
        'waypoints': waypoints
    }
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 航点已保存到：{filepath}")

def add_waypoint(name, x, y, yaw=0, filepath=None):
    """添加航点"""
    waypoints = load_waypoints(filepath)
    waypoints[name] = {'x': float(x), 'y': float(y), 'yaw': float(yaw)}
    save_waypoints(waypoints, filepath)
    print(f"✅ 已保存航点 '{name}': ({x}, {y})")
    return waypoints

def remove_waypoint(name, filepath=None):
    """删除航点"""
    waypoints = load_waypoints(filepath)
    if name in waypoints:
        del waypoints[name]
        save_waypoints(waypoints, filepath)
        print(f"✅ 已删除航点 '{name}'")
    else:
        print(f"❌ 航点 '{name}' 不存在")
    return waypoints

def list_waypoints(filepath=None):
    """列出所有航点"""
    waypoints = load_waypoints(filepath)
    
    if not waypoints:
        print("📭 暂无保存的航点")
        return {}
    
    print("📍 已保存的航点:")
    for name, pos in waypoints.items():
        print(f"   {name}: ({pos['x']:.2f}, {pos['y']:.2f}), 朝向 {pos.get('yaw', 0):.1f}°")
    
    return waypoints

def get_waypoint(name, filepath=None):
    """获取单个航点"""
    waypoints = load_waypoints(filepath)
    
    if name not in waypoints:
        print(f"❌ 航点 '{name}' 不存在")
        return None
    
    wp = waypoints[name]
    print(f"📍 {name}: ({wp['x']:.2f}, {wp['y']:.2f}), 朝向 {wp.get('yaw', 0):.1f}°")
    return wp

def main():
    parser = argparse.ArgumentParser(description='航点管理器')
    subparsers = parser.add_subparsers(dest='action', help='操作类型')
    
    # list
    subparsers.add_parser('list', help='列出所有航点')
    
    # add
    add_parser = subparsers.add_parser('add', help='添加航点')
    add_parser.add_argument('name', help='航点名称')
    add_parser.add_argument('--x', type=float, required=True, help='X坐标')
    add_parser.add_argument('--y', type=float, required=True, help='Y坐标')
    add_parser.add_argument('--yaw', type=float, default=0, help='朝向角度')
    
    # remove
    remove_parser = subparsers.add_parser('remove', help='删除航点')
    remove_parser.add_argument('name', help='航点名称')
    
    # get
    get_parser = subparsers.add_parser('get', help='获取航点')
    get_parser.add_argument('name', help='航点名称')
    
    # export/import
    export_parser = subparsers.add_parser('export', help='导出航点')
    export_parser.add_argument('--output', required=True, help='输出文件')
    
    import_parser = subparsers.add_parser('import', help='导入航点')
    import_parser.add_argument('--input', required=True, help='输入文件')
    
    args = parser.parse_args()
    
    if args.action == 'list':
        list_waypoints()
    
    elif args.action == 'add':
        add_waypoint(args.name, args.x, args.y, args.yaw)
    
    elif args.action == 'remove':
        remove_waypoint(args.name)
    
    elif args.action == 'get':
        get_waypoint(args.name)
    
    elif args.action == 'export':
        waypoints = load_waypoints()
        with open(args.output, 'w') as f:
            json.dump(waypoints, f, indent=2, ensure_ascii=False)
        print(f"✅ 已导出 {len(waypoints)} 个航点到 {args.output}")
    
    elif args.action == 'import':
        with open(args.input, 'r') as f:
            waypoints = json.load(f)
        save_waypoints(waypoints)
        print(f"✅ 已导入 {len(waypoints)} 个航点")
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
