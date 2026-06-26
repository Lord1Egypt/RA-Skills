#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UR Robot - 基础运动示例
演示关节运动和直线运动的基本用法
"""

import socket
import time

ROBOT_HOST = "localhost"
ROBOT_PORT = 30003

def send_urscript(command):
    """发送 URScript 命令"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5.0)
    try:
        sock.connect((ROBOT_HOST, ROBOT_PORT))
        sock.sendall((command + "\n").encode('utf-8'))
        print("[SENT] %s" % command[:50])
        time.sleep(0.1)
        return True
    except Exception as e:
        print("[ERROR] %s" % str(e))
        return False
    finally:
        sock.close()

def main():
    print("=" * 60)
    print("UR Robot - 基础运动示例")
    print("=" * 60)
    
    # 1. Home 位置
    print("\n[1] 移动到 Home 位置...")
    send_urscript("movej([0, -1.57, 1.57, -1.57, -1.57, 0], a=0.5, v=0.5)")
    time.sleep(5)
    
    # 2. 工作位置 1
    print("\n[2] 移动到工作位置 1...")
    send_urscript("movel([0.3, 0.0, 0.4, 3.14, 0, 0], a=0.2, v=0.2)")
    time.sleep(4)
    
    # 3. 工作位置 2
    print("\n[3] 移动到工作位置 2...")
    send_urscript("movel([0.4, 0.0, 0.3, 3.14, 0, 0], a=0.2, v=0.2)")
    time.sleep(4)
    
    # 4. 抬起
    print("\n[4] 抬起...")
    send_urscript("movel([0.4, 0.0, 0.5, 3.14, 0, 0], a=0.2, v=0.2)")
    time.sleep(3)
    
    # 5. 返回 Home
    print("\n[5] 返回 Home 位置...")
    send_urscript("movej([0, -1.57, 1.57, -1.57, -1.57, 0], a=0.5, v=0.5)")
    time.sleep(5)
    
    print("\n" + "=" * 60)
    print("示例完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
