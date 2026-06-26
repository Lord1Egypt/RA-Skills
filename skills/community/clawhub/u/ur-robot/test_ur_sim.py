#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UR Robot - URSim 仿真测试
测试 URSim 连接和基本功能
"""

from ur_rtde import RTDEReceiveInterface, RTDESendInterface
import time

# URSim 默认 IP
ROBOT_IP = "192.168.56.101"

print("=" * 70)
print("UR Robot - URSim Connection Test")
print("=" * 70)

try:
    # 连接
    print("\n[1] 连接机器人...")
    rtde_r = RTDEReceiveInterface(ROBOT_IP)
    rtde_s = RTDESendInterface(ROBOT_IP)
    print("[OK] 连接成功")
    
    # 获取状态
    print("\n[2] 获取当前状态...")
    joints = rtde_r.getActualQ()
    print(f"关节角度：{[f'{j:.2f}' for j in joints]}")
    
    tcp_pose = rtde_r.getActualTCPPose()
    print(f"TCP 位姿：{tcp_pose}")
    
    # 速度
    speed = rtde_r.getSpeedFraction()
    print(f"速度比例：{speed*100:.1f}%")
    
    # 关节空间运动
    print("\n[3] 关节空间运动测试...")
    target_joints = [0, -0.5, 0.5, 0, 0.5, 0]
    print(f"目标关节：{target_joints}")
    rtde_s.sendJointPosition(target_joints, speed=0.5)
    time.sleep(3)
    
    actual = rtde_r.getActualQ()
    print(f"实际关节：{[f'{j:.2f}' for j in actual]}")
    
    # 笛卡尔空间运动
    print("\n[4] 笛卡尔空间运动测试...")
    target_pose = [0.3, 0.3, 0.5, 3.14, 0, 0]
    print(f"目标位姿：{target_pose}")
    rtde_s.sendPose(target_pose, speed=0.5)
    time.sleep(3)
    
    actual_pose = rtde_r.getActualTCPPose()
    print(f"实际位姿：{actual_pose}")
    
    # 回到零位
    print("\n[5] 回到零位...")
    rtde_s.sendJointPosition([0, 0, 0, 0, 0, 0], speed=0.5)
    time.sleep(3)
    
    # 断开
    print("\n[6] 断开连接...")
    rtde_r.disconnect()
    rtde_s.disconnect()
    print("[OK] 已断开")
    
    print("\n" + "=" * 70)
    print("测试完成！✅")
    print("=" * 70)
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    print("\n可能的问题:")
    print("1. URSim 未启动")
    print("2. IP 地址不正确")
    print("3. 防火墙阻止连接")
    print("\n解决方法:")
    print("1. 启动 URSim 仿真器")
    print("2. 检查 IP: 192.168.56.101")
    print("3. 关闭防火墙或添加例外")
