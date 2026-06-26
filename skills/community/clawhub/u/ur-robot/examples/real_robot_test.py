#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UR Robot - 真机测试示例

⚠️ 重要：此脚本仅在 URSim 仿真中测试，未在真机验证！
真机使用前必须：
1. 修改 robot_host 为实际 IP
2. 使用最低速度参数
3. 专业人员监督
4. 确认急停按钮可用
"""

import socket
import time
import json

# ==================== 配置区域 ====================

# ⚠️ 真机必须修改为实际 IP！
ROBOT_HOST = "192.168.1.100"  # 仿真用 "localhost"
ROBOT_PORT = 30003

# 安全参数 - 真机必须使用低速！
MAX_SPEED = 0.2        # 真机建议：0.1-0.3
MAX_ACCELERATION = 0.1  # 真机建议：0.1-0.2

# ================================================

def send_urscript(command, timeout=5):
    """发送 URScript 命令"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((ROBOT_HOST, ROBOT_PORT))
        sock.sendall((command + "\n").encode('utf-8'))
        print(f"[SENT] {command[:50]}")
        time.sleep(0.1)
        response = sock.recv(1024).decode('utf-8', errors='ignore')
        return True, response
    except Exception as e:
        print(f"[ERROR] {e}")
        return False, str(e)
    finally:
        sock.close()

def safety_confirm():
    """安全确认"""
    print("\n" + "=" * 60)
    print("真机测试安全确认")
    print("=" * 60)
    print("\n请确认以下项目:")
    print("  ✓ 急停按钮可用且位置明确")
    print("  ✓ 机器人工作区域无人员")
    print("  ✓ 机器人运动路径无障碍物")
    print("  ✓ 工具安装牢固")
    print("  ✓ 速度参数已设置为最低 (v=0.1-0.2)")
    print("\n⚠️ 警告：本脚本仅在 URSim 仿真中测试，未在真机验证！")
    
    confirm = input("\n确认开始测试？(输入 YES 继续): ")
    return confirm == "YES"

def test_basic_motion():
    """基础运动测试"""
    print("\n" + "=" * 60)
    print("测试 1: 基础运动")
    print("=" * 60)
    
    # Home 位置
    print("\n[1] 移动到 Home 位置...")
    send_urscript(f"movej([0, -1.57, 1.57, -1.57, -1.57, 0], a={MAX_ACCELERATION}, v={MAX_SPEED})")
    time.sleep(5)
    
    # 工作位置 1
    print("\n[2] 移动到工作位置 1...")
    send_urscript(f"movel([0.3, 0.0, 0.4, 3.14, 0, 0], a={MAX_ACCELERATION}, v={MAX_SPEED})")
    time.sleep(4)
    
    # 工作位置 2
    print("\n[3] 移动到工作位置 2...")
    send_urscript(f"movel([0.4, 0.0, 0.3, 3.14, 0, 0], a={MAX_ACCELERATION}, v={MAX_SPEED})")
    time.sleep(4)
    
    # 返回 Home
    print("\n[4] 返回 Home 位置...")
    send_urscript(f"movej([0, -1.57, 1.57, -1.57, -1.57, 0], a={MAX_ACCELERATION}, v={MAX_SPEED})")
    time.sleep(5)
    
    print("\n[OK] 基础运动测试完成")

def test_io():
    """IO 测试"""
    print("\n" + "=" * 60)
    print("测试 2: IO 控制")
    print("=" * 60)
    
    print("\n[1] 打开数字输出 0...")
    send_urscript("set_digital_out(0, True)")
    time.sleep(2)
    
    print("\n[2] 关闭数字输出 0...")
    send_urscript("set_digital_out(0, False)")
    time.sleep(1)
    
    print("\n[OK] IO 测试完成")

def main():
    print("\n⚠️ " + "=" * 60)
    print("UR Robot - 真机测试脚本")
    print("=" * 60)
    print("\n⚠️ 警告：此脚本仅在 URSim 仿真中测试，未在真机验证！")
    print(f"\n目标机器人：{ROBOT_HOST}")
    print(f"速度限制：v={MAX_SPEED}, a={MAX_ACCELERATION}")
    
    # 安全确认
    if not safety_confirm():
        print("\n[取消] 测试已取消")
        return
    
    # 网络连接检查
    print("\n[1] 检查网络连接...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((ROBOT_HOST, ROBOT_PORT))
        sock.close()
        if result != 0:
            print(f"[FAIL] 无法连接到机器人 {ROBOT_HOST}")
            return
        print(f"[OK] 机器人连接正常")
    except Exception as e:
        print(f"[FAIL] {e}")
        return
    
    # 运行测试
    try:
        test_basic_motion()
        test_io()
        
        print("\n" + "=" * 60)
        print("[OK] 所有测试完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR] 测试过程中出错：{e}")
        print("\n⚠️ 请立即检查机器人状态！")

if __name__ == "__main__":
    main()
