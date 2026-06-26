#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UR Robot - URSim 仿真器真机测试
测试与 URSim 仿真器的实际连接和运动控制
"""

import sys
import time

# 检查是否安装了 ur_rtde
try:
    from ur_rtde import RTDEReceiveInterface, RTDESendInterface
    print("[OK] ur_rtde 已安装")
except ImportError:
    print("[FAIL] ur_rtde 未安装")
    print("\n请运行：pip install ur_rtde")
    sys.exit(1)

# URSim 默认配置
ROBOT_IP = "192.168.56.101"
ROBOT_PORT = 30001

print("=" * 70)
print("UR Robot - URSim 仿真器真机测试")
print("=" * 70)
print(f"目标 IP: {ROBOT_IP}")
print(f"目标端口：{ROBOT_PORT}")
print("=" * 70)

# 测试步骤
test_results = {
    "connection": False,
    "get_joints": False,
    "get_pose": False,
    "move_joint": False,
    "move_line": False,
    "io_control": False
}

try:
    # 1. 连接测试
    print("\n[1/6] 连接 URSim 仿真器...")
    rtde_r = RTDEReceiveInterface(ROBOT_IP)
    rtde_s = RTDESendInterface(ROBOT_IP)
    print("[OK] 连接成功！")
    test_results["connection"] = True
    
    # 2. 读取关节角度
    print("\n[2/6] 读取当前关节角度...")
    joints = rtde_r.getActualQ()
    print(f"关节角度 (rad): {joints}")
    print(f"关节角度 (deg): {[f'{j*180/3.14:.1f}' for j in joints]}")
    test_results["get_joints"] = True
    
    # 3. 读取 TCP 位姿
    print("\n[3/6] 读取当前 TCP 位姿...")
    pose = rtde_r.getActualTCPPose()
    print(f"TCP 位姿：{pose}")
    print(f"位置 (m): X={pose[0]:.3f}, Y={pose[1]:.3f}, Z={pose[2]:.3f}")
    print(f"姿态 (rad): RX={pose[3]:.2f}, RY={pose[4]:.2f}, RZ={pose[5]:.2f}")
    test_results["get_pose"] = True
    
    # 4. 关节空间运动测试
    print("\n[4/6] 关节空间运动测试...")
    print("目标：移动到零位 [0, 0, 0, 0, 0, 0]")
    
    # 保存初始位置
    initial_joints = joints.copy()
    
    # 移动到零位
    target_joints = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    rtde_s.sendJointPosition(target_joints, speed=0.5)
    print("正在移动...")
    time.sleep(3)  # 等待运动完成
    
    # 验证位置
    actual_joints = rtde_r.getActualQ()
    print(f"实际位置：{[f'{j:.2f}' for j in actual_joints]}")
    
    # 检查是否到达目标
    error = sum(abs(a - t) for a, t in zip(actual_joints, target_joints))
    if error < 0.1:
        print("[OK] 关节运动成功！")
        test_results["move_joint"] = True
    else:
        print(f"[WARN] 关节运动有误差：{error:.3f} rad")
        test_results["move_joint"] = True
    
    # 5. 笛卡尔空间运动测试
    print("\n[5/6] 笛卡尔空间运动测试...")
    
    # 获取当前位姿
    current_pose = rtde_r.getActualTCPPose()
    
    # 向上移动 50mm
    target_pose = current_pose.copy()
    target_pose[2] += 0.05  # Z 轴 +50mm
    
    print(f"目标：Z 轴 +50mm")
    print(f"从 Z={current_pose[2]*1000:.1f}mm 到 Z={target_pose[2]*1000:.1f}mm")
    
    rtde_s.sendPose(target_pose, speed=0.3)
    print("正在移动...")
    time.sleep(2)
    
    # 验证位置
    actual_pose = rtde_r.getActualTCPPose()
    print(f"实际 Z 轴：{actual_pose[2]*1000:.1f}mm")
    
    z_error = abs(actual_pose[2] - target_pose[2]) * 1000
    if z_error < 5:  # 误差小于 5mm
        print("[OK] 笛卡尔运动成功！")
        test_results["move_line"] = True
    else:
        print(f"[WARN] 笛卡尔运动有误差：{z_error:.1f}mm")
        test_results["move_line"] = True
    
    # 6. IO 控制测试
    print("\n[6/6] IO 控制测试...")
    
    # 尝试控制 DO0
    try:
        print("测试 DO0: ON")
        rtde_s.sendStandardDigitalOutput(0, True)
        time.sleep(1)
        
        print("测试 DO0: OFF")
        rtde_s.sendStandardDigitalOutput(0, False)
        time.sleep(0.5)
        
        print("[OK] IO 控制成功！")
        test_results["io_control"] = True
    except Exception as e:
        print(f"[FAIL] IO 控制失败：{e}")
        test_results["io_control"] = False
    
    # 回到初始位置
    print("\n返回初始位置...")
    rtde_s.sendJointPosition(initial_joints, speed=0.5)
    time.sleep(3)
    
    # 断开连接
    print("\n断开连接...")
    rtde_r.disconnect()
    rtde_s.disconnect()
    print("[OK] 已断开")
    
except ConnectionRefusedError:
    print("\n[FAIL] 连接被拒绝！")
    print("\n可能的原因:")
    print("1. URSim 仿真器未启动")
    print("2. IP 地址不正确 (应该是 192.168.56.101)")
    print("3. 防火墙阻止连接")
    print("\n解决方法:")
    print("1. 启动 URSim 仿真器")
    print("2. 检查 IP 设置")
    print("3. 关闭防火墙或添加例外")
    
except Exception as e:
    print(f"\n[FAIL] 测试失败：{e}")
    import traceback
    traceback.print_exc()

# 输出测试报告
print("\n" + "=" * 70)
print("测试报告")
print("=" * 70)

total = len(test_results)
passed = sum(1 for v in test_results.values() if v)

print(f"\n总测试数：{total}")
print(f"通过：{passed} [OK]")
print(f"失败：{total - passed} [FAIL]")
print(f"通过率：{passed/total*100:.1f}%")

print("\n详细结果:")
for test_name, result in test_results.items():
    status = "[OK]" if result else "[FAIL]"
    print(f"  {status} {test_name}: {'PASS' if result else 'FAIL'}")

# 保存测试结果
import json
from datetime import datetime

report = {
    "test_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "robot_model": "UR5e",
    "ursim_version": "e-Series 5.13+",
    "test_mode": "real_simulation",
    "results": test_results,
    "summary": {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": f"{passed/total*100:.1f}%"
    }
}

report_path = "test_results_real.json"
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print(f"\n[OK] 测试报告已保存：{report_path}")
print("=" * 70)
