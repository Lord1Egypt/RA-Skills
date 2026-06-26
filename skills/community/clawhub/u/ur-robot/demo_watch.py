#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UR Robot - 演示脚本：让机器人在 URSim 中运动
在浏览器中打开 http://localhost:8080 观看机器人动作
"""

import time
from ur_rtde import RTDEReceiveInterface, RTDESendInterface

print("=" * 70)
print("UR Robot - URSim 演示：观看机器人运动")
print("=" * 70)
print("\n请打开浏览器访问：http://localhost:8080")
print("等待 10 秒，让机器人界面加载...")
print("=" * 70)

# 等待用户打开浏览器
for i in range(10, 0, -1):
    print(f"\r倒计时：{i} 秒...", end="", flush=True)
    time.sleep(1)
print("\n")

# 连接机器人
print("[1/5] 连接 URSim...")
rtde_r = RTDEReceiveInterface("192.168.56.101")
rtde_s = RTDESendInterface("192.168.56.101")
print("✅ 连接成功！")

# 读取初始位置
print("\n[2/5] 读取当前位置...")
initial_joints = rtde_r.getActualQ()
print(f"当前关节角度：{[f'{j:.1f}°' for j in initial_joints]}")

# 动作 1: 移动到零位
print("\n[3/5] 动作 1: 移动到零位...")
print("（在浏览器中观察机器人运动）")
rtde_s.sendJointPosition([0, 0, 0, 0, 0, 0], speed=0.3)
time.sleep(4)
print("✅ 完成")

# 动作 2: 抬起机械臂
print("\n[4/5] 动作 2: 抬起机械臂...")
print("（在浏览器中观察机器人运动）")
rtde_s.sendJointPosition([0, -0.5, 0.5, 0, 0.5, 0], speed=0.3)
time.sleep(4)
print("✅ 完成")

# 动作 3: Z 轴上下运动
print("\n[5/5] 动作 3: Z 轴上下运动...")
print("（在浏览器中观察机器人运动）")
current_pose = rtde_r.getActualTCPPose()
for i in range(3):
    # 向上
    target_pose = current_pose.copy()
    target_pose[2] += 0.05 * (1 if i % 2 == 0 else -1)
    rtde_s.sendPose(target_pose, speed=0.2)
    time.sleep(2)
    # 向下
    target_pose = current_pose.copy()
    target_pose[2] -= 0.05 * (1 if i % 2 == 0 else -1)
    rtde_s.sendPose(target_pose, speed=0.2)
    time.sleep(2)
print("✅ 完成")

# 回到初始位置
print("\n返回初始位置...")
rtde_s.sendJointPosition(initial_joints, speed=0.5)
time.sleep(4)

# 断开连接
rtde_r.disconnect()
rtde_s.disconnect()

print("\n" + "=" * 70)
print("演示完成！✅")
print("=" * 70)
print("\n你可以在浏览器中继续手动操作机器人，或运行其他测试脚本。")
print("关闭浏览器标签页即可。")
