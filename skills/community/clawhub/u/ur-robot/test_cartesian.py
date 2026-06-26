#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UR Robot - 笛卡尔空间测试
测试直线运动和圆弧运动
"""

from ur_rtde import RTDEReceiveInterface, RTDESendInterface
import time
import math

ROBOT_IP = "192.168.56.101"

print("=" * 70)
print("UR Robot - Cartesian Motion Test")
print("=" * 70)

try:
    rtde_r = RTDEReceiveInterface(ROBOT_IP)
    rtde_s = RTDESendInterface(ROBOT_IP)
    print("[OK] Connected\n")
    
    # 安全位置
    safe_pose = [0.3, 0.3, 0.5, 3.14, 0, 0]
    
    # 1. 直线运动测试
    print("=" * 70)
    print("1. 直线运动测试 (MovL)")
    print("=" * 70)
    
    points = [
        [0.3, 0.3, 0.5, 3.14, 0, 0],      # 起点
        [0.4, 0.3, 0.5, 3.14, 0, 0],      # X+100mm
        [0.4, 0.4, 0.5, 3.14, 0, 0],      # Y+100mm
        [0.3, 0.4, 0.5, 3.14, 0, 0],      # X-100mm
        [0.3, 0.3, 0.5, 3.14, 0, 0],      # Y-100mm (返回)
    ]
    
    print("\n绘制正方形 (边长 100mm)...")
    for i, point in enumerate(points):
        print(f"\n点{i+1}: {point}")
        rtde_s.sendPose(point, speed=0.3)
        time.sleep(2)
        
        actual = rtde_r.getActualTCPPose()
        print(f"实际：[{actual[0]:.3f}, {actual[1]:.3f}, {actual[2]:.3f}]")
    
    # 2. Z 轴上下运动
    print("\n" + "=" * 70)
    print("2. Z 轴上下运动")
    print("=" * 70)
    
    for z in [0.5, 0.45, 0.4, 0.45, 0.5]:
        point = [0.3, 0.3, z, 3.14, 0, 0]
        print(f"\nZ={z*1000:.0f}mm")
        rtde_s.sendPose(point, speed=0.3)
        time.sleep(1.5)
    
    # 3. 姿态变化
    print("\n" + "=" * 70)
    print("3. 姿态变化测试")
    print("=" * 70)
    
    base_pose = [0.3, 0.3, 0.5, 3.14, 0, 0]
    
    # RX 旋转
    print("\nRX 旋转 (±30°)...")
    for rx in [3.14, 3.14-0.52, 3.14, 3.14+0.52, 3.14]:
        base_pose[3] = rx
        rtde_s.sendPose(base_pose.copy(), speed=0.3)
        time.sleep(1.5)
        actual = rtde_r.getActualTCPPose()
        print(f"RX={actual[3]*180/3.14:.1f}°")
    
    # 回到安全位置
    print("\n" + "=" * 70)
    print("回到安全位置...")
    print("=" * 70)
    rtde_s.sendPose(safe_pose, speed=0.5)
    time.sleep(2)
    
    # 断开
    rtde_r.disconnect()
    rtde_s.disconnect()
    
    print("\n[OK] 测试完成！✅")
    print("=" * 70)
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    print("\n可能的问题:")
    print("1. URSim 未启动")
    print("2. IP 地址不正确")
    print("3. 目标位置超出工作空间")
