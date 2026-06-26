#!/usr/bin/env python3
"""读取和解析ROS地图文件"""

import argparse
import json
import numpy as np
from PIL import Image
from pathlib import Path

def load_map(map_path, yaml_path=None):
    """读取地图文件并解析"""
    map_file = Path(map_path)
    
    if not map_file.exists():
        print(f"❌ 地图文件不存在：{map_file}")
        return None
    
    # 读取yaml配置
    if yaml_path is None:
        yaml_path = map_file.with_suffix('.yaml')
    
    map_config = {}
    if yaml_path.exists():
        with open(yaml_path, 'r') as f:
            for line in f:
                if ':' in line and not line.strip().startswith('#'):
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    if key == 'image':
                        map_config['image'] = value
                    elif key == 'resolution':
                        map_config['resolution'] = float(value)
                    elif key == 'origin':
                        # 解析 [x, y, z] 格式
                        coords = value.strip('[]').split(',')
                        map_config['origin'] = [float(c) for c in coords]
                    elif key == 'occupied_thresh':
                        map_config['occupied_thresh'] = float(value)
                    elif key == 'free_thresh':
                        map_config['free_thresh'] = float(value)
                    elif key == 'negate':
                        map_config['negate'] = int(value)
    
    # 默认值
    map_config.setdefault('resolution', 0.05)
    map_config.setdefault('origin', [0, 0, 0])
    map_config.setdefault('occupied_thresh', 0.65)
    map_config.setdefault('free_thresh', 0.196)
    
    # 读取图像
    img = Image.open(map_file)
    data = np.array(img)
    
    print(f"📐 地图基本信息:")
    print(f"   文件：{map_file}")
    print(f"   图像尺寸：{data.shape[1]} x {data.shape[0]} 像素")
    print(f"   分辨率：{map_config['resolution']} m/pixel")
    print(f"   原点：{map_config['origin'][:2]}")
    print()
    
    # 分析地图
    resolution = map_config['resolution']
    origin = map_config['origin'][:2]
    H, W = data.shape
    
    # 找到有效区域
    valid = data < 250
    rows = np.where(valid.any(axis=1))[0]
    cols = np.where(valid.any(axis=0))[0]
    
    if len(rows) > 0 and len(cols) > 0:
        row_min, row_max = rows[0], rows[-1]
        col_min, col_max = cols[0], cols[-1]
        
        print(f"📍 有效建图区域:")
        print(f"   像素范围：[{col_min}:{col_max}] x [{row_min}:{row_max}]")
        
        x_min = origin[0] + col_min * resolution
        x_max = origin[0] + col_max * resolution
        y_min = origin[1] + (H - row_max) * resolution
        y_max = origin[1] + (H - row_min) * resolution
        
        print(f"   世界坐标：X=[{x_min:.1f}, {x_max:.1f}], Y=[{y_min:.1f}, {y_max:.1f}]")
        print()
    
    # 区域统计
    occupied_thresh = map_config['occupied_thresh'] * 255
    free_thresh = map_config['free_thresh'] * 255
    
    obstacles = data < free_thresh
    free = data > occupied_thresh
    unknown = (data >= free_thresh) & (data <= occupied_thresh)
    
    total = data.size
    print(f"🗺️  区域统计:")
    print(f"   障碍物 (<{free_thresh:.0f}): {np.sum(obstacles):,} ({np.sum(obstacles)/total*100:.1f}%)")
    print(f"   自由空间 (>{occupied_thresh:.0f}): {np.sum(free):,} ({np.sum(free)/total*100:.1f}%)")
    print(f"   未知区域：{np.sum(unknown):,} ({np.sum(unknown)/total*100:.1f}%)")
    print()
    
    return {
        'data': data,
        'config': map_config,
        'bounds': {
            'row_min': row_min if len(rows) > 0 else 0,
            'row_max': row_max if len(rows) > 0 else H,
            'col_min': col_min if len(cols) > 0 else 0,
            'col_max': col_max if len(cols) > 0 else W,
        }
    }

def pixel_to_world(r, c, data_shape, origin, resolution):
    """像素坐标转世界坐标"""
    H = data_shape[0]
    x = origin[0] + c * resolution
    y = origin[1] + (H - r) * resolution
    return x, y

def world_to_pixel(x, y, data_shape, origin, resolution):
    """世界坐标转像素坐标"""
    H = data_shape[0]
    c = int((x - origin[0]) / resolution)
    r = int(H - (y - origin[1]) / resolution)
    return r, c

def get_quadrant_waypoints(map_data):
    """获取四个象限的航点"""
    if map_data is None:
        return []
    
    data = map_data['data']
    config = map_data['config']
    bounds = map_data['bounds']
    
    resolution = config['resolution']
    origin = config['origin'][:2]
    H = data.shape[0]
    
    # 提取有效区域
    map_region = data[bounds['row_min']:bounds['row_max']+1, 
                      bounds['col_min']:bounds['col_max']+1]
    
    h, w = map_region.shape
    mid_h, mid_w = h // 2, w // 2
    
    quadrants = {
        '左上': (0, mid_h, 0, mid_w),
        '右上': (0, mid_h, mid_w, w),
        '右下': (mid_h, h, mid_w, w),
        '左下': (mid_h, h, 0, mid_w),
    }
    
    waypoints = []
    for name, (r1, r2, c1, c2) in quadrants.items():
        region = map_region[r1:r2, c1:c2]
        free = region > config['free_thresh'] * 255
        
        if np.any(free):
            coords = np.where(free)
            global_r = bounds['row_min'] + r1 + coords[0]
            global_c = bounds['col_min'] + c1 + coords[1]
            center_r = int(np.mean(global_r))
            center_c = int(np.mean(global_c))
            x, y = pixel_to_world(center_r, center_c, data.shape, origin, resolution)
            waypoints.append({'name': name, 'x': x, 'y': y})
    
    return waypoints

def main():
    parser = argparse.ArgumentParser(description='读取和解析ROS地图')
    parser.add_argument('--map', required=True, help='地图文件路径 (.pgm)')
    parser.add_argument('--yaml', help='YAML配置文件路径 (可选，默认与地图同名)')
    parser.add_argument('--json', action='store_true', help='输出JSON格式')
    parser.add_argument('--quadrants', action='store_true', help='输出四象限航点')
    args = parser.parse_args()
    
    map_data = load_map(args.map, args.yaml)
    
    if map_data is None:
        exit(1)
    
    if args.quadrants:
        waypoints = get_quadrant_waypoints(map_data)
        if args.json:
            print(json.dumps(waypoints, indent=2))
        else:
            print("🗺️  四象限航点:")
            for wp in waypoints:
                print(f"   {wp['name']}: ({wp['x']:.2f}, {wp['y']:.2f})")

if __name__ == '__main__':
    main()
