#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UR Robot - 关节控制测试
测试 J1-J6 每个关节的运动
"""

from ur_rtde import RTDEReceiveInterface, RTDESendInterface
import time

ROBOT_IP = "192.168.56.101"

print("=" * 70)
print("UR Robot - Joint Control Test")
print("=" * 70)

try:
    rtde_r = RTDEReceiveInterface(ROBOT_IP)
    rtde_s = RTDESendInterface(ROBOT_IP)
    print("[OK] Connected")
    
    # 获取初始位置
    initial = rtde_r.getActualQ()
    print(f"\n初始关节：{[f'{j:.2f}' for j in initial]}")
    
    # 测试每个关节
    joint_names = ['J1', 'J2', 'J3', 'J4', 'J5', 'J6']
    
    for i in range(6):
        print(f"\n{'='*70}")
        print(f"测试 {joint_names[i]} (轴{i+1})")
        print(f"{'='*70}")
        
        # 正方向
        print(f"\n[正方向] +30°...")
        target = initial.copy()
        target[i] += 0.524  # 30 度 (弧度)
        rtde_s.sendJointPosition(target, speed=0.5)
        time.sleep(2)
        actual = rtde_r.getActualQ()
        print(f"实际：{actual[i]:.2f} rad ({actual[i]*180/3.14:.1f}°)")
        
        # 负方向
        print(f"\n[负方向] -30°...")
        target = initial.copy()
        target[i] -= 0.524
        rtde_s.sendJointPosition(target, speed=0.5)
        time.sleep(2)
        actual = rtde_r.getActualQ()
        print(f"实际：{actual[i]:.2f} rad ({actual[i]*180/3.14:.1f}°)")
    
    # 回到初始位置
    print(f"\n{'='*70}")
    print("返回初始位置...")
    rtde_s.sendJointPosition(initial, speed=0.5)
    time.sleep(2)
    
    # 断开
    rtde_r.disconnect()
    rtde_s.disconnect()
    
    print("\n[OK] 测试完成！")
    
except Exception as e:
    print(f"\n[ERROR] {e}")
