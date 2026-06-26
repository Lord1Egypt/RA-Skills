#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UR Robot - 力控模式测试
测试 Force Mode 功能
"""

from ur_rtde import RTDEReceiveInterface, RTDESendInterface
import time

ROBOT_IP = "192.168.56.101"

print("=" * 70)
print("UR Robot - Force Mode Test")
print("=" * 70)

try:
    rtde_r = RTDEReceiveInterface(ROBOT_IP)
    rtde_s = RTDESendInterface(ROBOT_IP)
    print("[OK] Connected\n")
    
    # 力控模式参数
    task_frame = [0, 0, 0, 0, 0, 0]  # 基座标系
    selection_vector = [0, 0, 1, 0, 0, 0]  # Z 轴力控
    wrench = [0, 0, -10, 0, 0, 0]  # 10N 向下力
    bounds = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1]  # 容差
    gain = 0.5  # 增益
    
    print("=" * 70)
    print("1. 启用力控模式")
    print("=" * 70)
    print(f"力控轴：Z 轴")
    print(f"目标力：10N (向下)")
    print(f"增益：{gain}")
    
    rtde_s.sendForceMode(
        task_frame=task_frame,
        selection_vector=selection_vector,
        wrench=wrench,
        bounds=bounds,
        gain=gain
    )
    print("\n[OK] 力控模式已启用\n")
    
    time.sleep(2)
    
    # 尝试移动
    print("=" * 70)
    print("2. 力控模式下移动")
    print("=" * 70)
    
    # 小范围移动
    for i in range(5):
        z_offset = 0.45 - (i * 0.01)
        pose = [0.3, 0.3, z_offset, 3.14, 0, 0]
        print(f"\n移动到 Z={z_offset*1000:.0f}mm")
        rtde_s.sendPose(pose, speed=0.1)
        time.sleep(1)
        
        # 读取实际力
        # 注意：ur_rtde 可能需要特定版本才支持力读取
    
    # 关闭力控
    print("\n" + "=" * 70)
    print("3. 关闭力控模式")
    print("=" * 70)
    
    # 发送零力退出力控
    rtde_s.sendForceMode(
        task_frame=[0,0,0,0,0,0],
        selection_vector=[0,0,0,0,0,0],
        wrench=[0,0,0,0,0,0],
        bounds=[0.1,0.1,0.1,0.1,0.1,0.1],
        gain=0.5
    )
    print("[OK] 力控模式已关闭\n")
    
    time.sleep(1)
    
    # 回到安全位置
    print("=" * 70)
    print("4. 回到安全位置")
    print("=" * 70)
    rtde_s.sendPose([0.3, 0.3, 0.5, 3.14, 0, 0], speed=0.5)
    time.sleep(2)
    
    # 断开
    rtde_r.disconnect()
    rtde_s.disconnect()
    
    print("\n[OK] 力控测试完成！✅")
    print("=" * 70)
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    print("\n力控模式注意事项:")
    print("1. 需要 UR 机器人支持力控")
    print("2. URSim 可能不支持完整力控")
    print("3. 真机测试效果最佳")
