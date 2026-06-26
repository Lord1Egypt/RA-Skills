#!/usr/bin/env python3
"""
仓配网络规划分析脚本
用法: python3 analyze.py <excel文件路径>
"""

import pandas as pd
import math
import sys

# 内置城市坐标库
CITIES_COORDS = {
    '武汉': (114.3055, 30.5928), '成都': (104.0655, 30.6595), '重庆': (106.5514, 29.5637),
    '南昌': (115.8582, 28.6820), '西安': (108.9398, 34.3416), '贵阳': (106.7134, 26.5780),
    '昆明': (102.8329, 24.8801), '荆州': (112.2394, 30.3269), '襄阳': (112.1226, 32.0101),
    '宜昌': (111.2862, 30.6918), '郑州': (113.6254, 34.7466), '开封': (114.3074, 34.7971),
    '南阳': (112.5287, 33.0004), '新乡': (113.9267, 35.3029), '漯河': (114.0166, 33.5818),
    '宜宾': (104.6431, 28.7518), '景德镇': (117.2014, 29.2689), '西双版纳': (100.7970, 21.9588)
}

def calc_distance(lng1, lat1, lng2, lat2):
    """计算两点间距离(km)"""
    R = 6371
    dLat = math.radians(lat2 - lat1)
    dLng = math.radians(lng2 - lng1)
    a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLng/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return round(R * c, 1)

def analyze(file_path, warehouse_lng=114.3055, warehouse_lat=30.5928):
    """分析函数"""
    df = pd.read_excel(file_path)
    
    # 1. 基础统计
    print("="*60)
    print("一、门店分布统计")
    print("="*60)
    
    # 城市统计
    city_stats = df.groupby('城市').size().reset_index(name='门店数')
    city_stats = city_stats.sort_values('门店数', ascending=False)
    print("\n各城市门店数量:")
    print(city_stats.to_string(index=False))
    
    # 省份统计
    if '省' in df.columns:
        province_stats = df.groupby('省').size().reset_index(name='门店数')
        province_stats = province_stats.sort_values('门店数', ascending=False)
        print("\n各省份门店数量:")
        print(province_stats.to_string(index=False))
    
    # 2. 配送距离
    print("\n" + "="*60)
    print("二、配送距离测算")
    print("="*60)
    
    for _, row in city_stats.iterrows():
        city = row['城市']
        if city in CITIES_COORDS:
            lng, lat = CITIES_COORDS[city]
            dist = calc_distance(warehouse_lng, warehouse_lat, lng, lat)
            tag = '短途' if dist <= 300 else '中途' if dist <= 600 else '长途'
            print(f"{city}: {dist}km ({tag})")
    
    print("\n分析完成！")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 analyze.py <excel文件路径>")
        sys.exit(1)
    
    analyze(sys.argv[1])