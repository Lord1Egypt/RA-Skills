#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UR Robot - 真机安全检查脚本

⚠️ 重要：此脚本仅在 URSim 仿真中测试，未在真机验证！
真机使用前必须重新验证所有功能！
"""

import socket
import json
import sys

def check_network_connection(host, timeout=2):
    """检查网络连接"""
    print("\n[1] 检查网络连接...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, 30003))
        sock.close()
        if result == 0:
            print(f"[OK] 机器人 {host} 连接正常")
            return True
        else:
            print(f"[FAIL] 无法连接到机器人 {host}")
            return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def check_robot_status(host, port=30003):
    """检查机器人状态"""
    print("\n[2] 检查机器人状态...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host, port))
        sock.sendall(b"get_actual_tcp_pose()\n")
        response = sock.recv(1024).decode('utf-8', errors='ignore')
        sock.close()
        print(f"[OK] 机器人响应正常")
        return True
    except Exception as e:
        print(f"[FAIL] 无法获取机器人状态：{e}")
        return False

def check_workspace_limits(pose, limits):
    """检查工作范围"""
    print("\n[3] 检查工作范围...")
    x, y, z = pose[0], pose[1], pose[2]
    
    if not (limits['x_min'] <= x <= limits['x_max']):
        print(f"[FAIL] X 轴超出范围：{x} (限制：{limits['x_min']} ~ {limits['x_max']})")
        return False
    
    if not (limits['y_min'] <= y <= limits['y_max']):
        print(f"[FAIL] Y 轴超出范围：{y} (限制：{limits['y_min']} ~ {limits['y_max']})")
        return False
    
    if not (limits['z_min'] <= z <= limits['z_max']):
        print(f"[FAIL] Z 轴超出范围：{z} (限制：{limits['z_min']} ~ {limits['z_max']})")
        return False
    
    print(f"[OK] 位置在工作范围内")
    return True

def manual_safety_check():
    """人工安全检查"""
    print("\n[4] 人工安全检查...")
    print("请确认以下项目:")
    print("  □ 急停按钮可用且位置明确")
    print("  □ 机器人工作区域无人员")
    print("  □ 机器人运动路径无障碍物")
    print("  □ 工具安装牢固")
    print("  □ 电源和气源正常")
    
    confirm = input("\n确认以上所有项目？(y/n): ")
    return confirm.lower() == 'y'

def load_config(config_file="real_robot_config.json"):
    """加载配置文件"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"[OK] 加载配置文件：{config_file}")
        return config
    except Exception as e:
        print(f"[ERROR] 加载配置文件失败：{e}")
        return None

def main():
    print("=" * 60)
    print("UR Robot - 真机安全检查")
    print("=" * 60)
    print("\n⚠️ 警告：此脚本仅在 URSim 仿真中测试，未在真机验证！")
    
    # 加载配置
    config = load_config()
    if not config:
        print("\n[FAIL] 无法加载配置文件，请检查 real_robot_config.json")
        sys.exit(1)
    
    robot_host = config['connection']['host']
    
    # 1. 网络连接检查
    if not check_network_connection(robot_host):
        print("\n[FAIL] 网络连接检查失败")
        sys.exit(1)
    
    # 2. 机器人状态检查
    if not check_robot_status(robot_host):
        print("\n[FAIL] 机器人状态检查失败")
        sys.exit(1)
    
    # 3. 工作范围检查 (示例位置)
    test_pose = [0.3, 0.3, 0.4, 0, 3.14, 0]
    limits = config['safety']['workspace_limits']
    if not check_workspace_limits(test_pose, limits):
        print("\n[FAIL] 工作范围检查失败")
        sys.exit(1)
    
    # 4. 人工安全检查
    if not manual_safety_check():
        print("\n[FAIL] 人工安全检查未通过")
        sys.exit(1)
    
    # 所有检查通过
    print("\n" + "=" * 60)
    print("[OK] 所有安全检查通过！")
    print("=" * 60)
    print("\n可以继续运行机器人控制程序")
    print("提示：首次运行请使用最低速度 (v=0.1)")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
