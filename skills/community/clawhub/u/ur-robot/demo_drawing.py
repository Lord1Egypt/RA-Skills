#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UR Robot - 轨迹绘制示例
绘制正方形、圆形、三角形
"""

from ur_rtde import RTDEReceiveInterface, RTDESendInterface
import time
import math

ROBOT_IP = "192.168.56.101"

print("=" * 70)
print("UR Robot - Path Drawing Demo")
print("=" * 70)

try:
    rtde_r = RTDEReceiveInterface(ROBOT_IP)
    rtde_s = RTDESendInterface(ROBOT_IP)
    print("[OK] Connected\n")
    
    # 基础参数
    BASE_Z = 0.4  # 基础高度
    BASE_RX = 3.14  # 基础姿态
    
    # ========== 1. 绘制正方形 ==========
    print("=" * 70)
    print("1. 绘制正方形 (边长 100mm)")
    print("=" * 70)
    
    square_points = [
        [0.3, 0.3, BASE_Z, BASE_RX, 0, 0],
        [0.4, 0.3, BASE_Z, BASE_RX, 0, 0],
        [0.4, 0.4, BASE_Z, BASE_RX, 0, 0],
        [0.3, 0.4, BASE_Z, BASE_RX, 0, 0],
        [0.3, 0.3, BASE_Z, BASE_RX, 0, 0],
    ]
    
    for i, point in enumerate(square_points):
        print(f"\n点{i+1}: [{point[0]:.3f}, {point[1]:.3f}, {point[2]:.3f}]")
        rtde_s.sendPose(point, speed=0.3)
        time.sleep(1.5)
    
    print("\n正方形完成！✅")
    time.sleep(2)
    
    # ========== 2. 绘制圆形 ==========
    print("\n" + "=" * 70)
    print("2. 绘制圆形 (半径 50mm)")
    print("=" * 70)
    
    center = [0.35, 0.35, BASE_Z]
    radius = 0.05  # 50mm
    
    print(f"圆心：{center}")
    print(f"半径：{radius*1000:.0f}mm")
    
    for angle in range(0, 361, 30):
        rad = math.radians(angle)
        x = center[0] + radius * math.cos(rad)
        y = center[1] + radius * math.sin(rad)
        point = [x, y, BASE_Z, BASE_RX, 0, 0]
        
        if angle % 90 == 0:
            print(f"\n{angle}°: [{x:.3f}, {y:.3f}]")
        
        rtde_s.sendPose(point, speed=0.3)
        time.sleep(0.5)
    
    print("\n圆形完成！✅")
    time.sleep(2)
    
    # ========== 3. 绘制三角形 ==========
    print("\n" + "=" * 70)
    print("3. 绘制三角形 (边长 100mm)")
    print("=" * 70)
    
    triangle_points = [
        [0.3, 0.3, BASE_Z, BASE_RX, 0, 0],
        [0.4, 0.3, BASE_Z, BASE_RX, 0, 0],
        [0.35, 0.387, BASE_Z, BASE_RX, 0, 0],  # 等边三角形
        [0.3, 0.3, BASE_Z, BASE_RX, 0, 0],
    ]
    
    for i, point in enumerate(triangle_points):
        print(f"\n点{i+1}: [{point[0]:.3f}, {point[1]:.3f}]")
        rtde_s.sendPose(point, speed=0.3)
        time.sleep(1.5)
    
    print("\n三角形完成！✅")
    
    # 回到安全位置
    print("\n" + "=" * 70)
    print("回到安全位置...")
    print("=" * 70)
    safe_pose = [0.3, 0.3, 0.5, BASE_RX, 0, 0]
    rtde_s.sendPose(safe_pose, speed=0.5)
    time.sleep(2)
    
    # 断开
    rtde_r.disconnect()
    rtde_s.disconnect()
    
    print("\n[OK] 所有轨迹绘制完成！✅")
    print("=" * 70)
    
except Exception as e:
    print(f"\n[ERROR] {e}")
