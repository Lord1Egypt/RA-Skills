#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UR Robot - 码垛应用示例
演示基本的码垛逻辑
"""

from ur_rtde import RTDEReceiveInterface, RTDESendInterface
import time
import math

ROBOT_IP = "192.168.56.101"

# 码垛参数
BOX_SIZE = 50  # 盒子边长 (mm)
PALLET_ROWS = 3  # 行数
PALLET_COLS = 3  # 列数
PALLET_LAYERS = 2  # 层数

# 起始位置
START_POSE = [0.3, 0.2, 0.3, 3.14, 0, 0]  # 拾取点
PALLET_ORIGIN = [0.4, 0.4, 0.1]  # 码垛原点

print("=" * 70)
print("UR Robot - Palletizing Demo")
print("=" * 70)
print(f"码垛规格：{PALLET_ROWS}x{PALLET_COLS}x{PALLET_LAYERS}")
print(f"总盒子数：{PALLET_ROWS * PALLET_COLS * PALLET_LAYERS}")
print("=" * 70)

try:
    rtde_r = RTDEReceiveInterface(ROBOT_IP)
    rtde_s = RTDESendInterface(ROBOT_IP)
    print("[OK] Connected\n")
    
    # 移动到安全位置
    safe_pose = START_POSE.copy()
    safe_pose[2] = 0.5  # Z 轴抬高
    rtde_s.sendPose(safe_pose, speed=0.5)
    time.sleep(2)
    
    box_count = 0
    
    # 码垛循环
    for layer in range(PALLET_LAYERS):
        print(f"\n{'='*70}")
        print(f"第 {layer+1} 层")
        print(f"{'='*70}")
        
        for row in range(PALLET_ROWS):
            for col in range(PALLET_COLS):
                # 计算目标位置
                x = PALLET_ORIGIN[0] + (col * BOX_SIZE / 1000)
                y = PALLET_ORIGIN[1] + (row * BOX_SIZE / 1000)
                z = PALLET_ORIGIN[2] + (layer * BOX_SIZE / 1000)
                
                box_count += 1
                print(f"\n盒子 {box_count}: ({x:.3f}, {y:.3f}, {z:.3f})")
                
                # 1. 移动到拾取点上方
                pick_pose = START_POSE.copy()
                rtde_s.sendPose(pick_pose, speed=0.5)
                time.sleep(1)
                
                # 2. 下降到拾取点
                pick_pose[2] = START_POSE[2] - 0.05
                rtde_s.sendPose(pick_pose, speed=0.3)
                time.sleep(1)
                
                # 3. 抓取 (模拟)
                print("  [模拟] 抓取盒子...")
                time.sleep(0.5)
                
                # 4. 上升
                pick_pose[2] = START_POSE[2]
                rtde_s.sendPose(pick_pose, speed=0.5)
                time.sleep(1)
                
                # 5. 移动到放置点上方
                place_pose = [x, y, z + 0.1, 3.14, 0, 0]
                rtde_s.sendPose(place_pose, speed=0.5)
                time.sleep(1)
                
                # 6. 下降到放置点
                place_pose[2] = z
                rtde_s.sendPose(place_pose, speed=0.3)
                time.sleep(1)
                
                # 7. 释放 (模拟)
                print("  [模拟] 释放盒子...")
                time.sleep(0.5)
                
                # 8. 上升
                place_pose[2] = z + 0.1
                rtde_s.sendPose(place_pose, speed=0.5)
                time.sleep(1)
        
        print(f"\n第 {layer+1} 层完成！✅")
    
    # 回到安全位置
    print(f"\n{'='*70}")
    print("码垛完成！回到安全位置...")
    print(f"{'='*70}")
    rtde_s.sendPose(safe_pose, speed=0.5)
    time.sleep(2)
    
    # 断开
    rtde_r.disconnect()
    rtde_s.disconnect()
    
    print(f"\n[OK] 码垛完成！共 {box_count} 个盒子 ✅")
    print("=" * 70)
    
except Exception as e:
    print(f"\n[ERROR] {e}")
