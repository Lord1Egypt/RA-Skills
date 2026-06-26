#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行程规划辅助脚本
用于计算和比较不同交通方式的时间、成本
"""

import json
import sys
from datetime import datetime, timedelta

def calculate_travel_time(distance_km, mode):
    """
    估算不同交通方式的旅行时间（小时）
    
    Args:
        distance_km: 距离（公里）
        mode: 交通方式 (driving/high-speed/flight)
    
    Returns:
        预计时间（小时）
    """
    if mode == "driving":
        # 驾车：平均 80km/h + 休息时间
        return distance_km / 80 + max(0, distance_km // 200) * 0.5
    elif mode == "high-speed":
        # 高铁：平均 250km/h + 进出站时间
        return distance_km / 250 + 1.0
    elif mode == "flight":
        # 飞机：平均 600km/h + 安检候机时间
        return distance_km / 600 + 2.5
    else:
        return 0

def suggest_transport(distance_km, purpose="business"):
    """
    根据距离和出行目的推荐交通方式
    
    Args:
        distance_km: 距离（公里）
        purpose: 出行目的 (business/leisure)
    
    Returns:
        推荐的交通方式列表
    """
    suggestions = []
    
    if distance_km < 50:
        suggestions = ["driving", "taxi"]
    elif distance_km < 300:
        if purpose == "business":
            suggestions = ["high-speed", "driving"]
        else:
            suggestions = ["high-speed", "driving", "flight"]
    elif distance_km < 800:
        if purpose == "business":
            suggestions = ["high-speed", "flight"]
        else:
            suggestions = ["flight", "high-speed"]
    else:
        suggestions = ["flight", "high-speed"]
    
    return suggestions

def format_duration(hours):
    """格式化时间为人类可读格式"""
    h = int(hours)
    m = int((hours - h) * 60)
    if h > 0:
        return f"{h}小时{m}分钟"
    else:
        return f"{m}分钟"

def main():
    """主函数"""
    if len(sys.argv) < 3:
        print(json.dumps({
            "error": "用法：trip-planner.py <距离 km> <出行目的 business/leisure>"
        }, ensure_ascii=False))
        sys.exit(1)
    
    try:
        distance = float(sys.argv[1])
        purpose = sys.argv[2]
        
        suggestions = suggest_transport(distance, purpose)
        
        result = {
            "distance_km": distance,
            "purpose": purpose,
            "suggested_modes": suggestions,
            "time_estimates": {
                mode: format_duration(calculate_travel_time(distance, mode))
                for mode in ["driving", "high-speed", "flight"]
            }
        }
        
        print(json.dumps(result, ensure_ascii=False))
        
    except Exception as e:
        print(json.dumps({
            "error": str(e)
        }, ensure_ascii=False))
        sys.exit(1)

if __name__ == "__main__":
    main()
