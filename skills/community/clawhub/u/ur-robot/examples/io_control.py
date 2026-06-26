#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UR Robot - IO 控制示例
演示数字输入输出的基本用法
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
    print("UR Robot - IO 控制示例")
    print("=" * 60)
    
    # 1. 打开数字输出 0
    print("\n[1] 打开数字输出 0 (DO0 = ON)...")
    send_urscript("set_digital_out(0, True)")
    print("[INFO] 请在 I/O 界面查看 Digital Output 0 状态")
    time.sleep(3)
    
    # 2. 关闭数字输出 0
    print("\n[2] 关闭数字输出 0 (DO0 = OFF)...")
    send_urscript("set_digital_out(0, False)")
    time.sleep(1)
    
    # 3. 打开工具数字输出
    print("\n[3] 打开工具数字输出 0 (TDO0 = ON)...")
    send_urscript("set_tool_digital_out(0, True)")
    time.sleep(3)
    
    # 4. 关闭工具数字输出
    print("\n[4] 关闭工具数字输出 0 (TDO0 = OFF)...")
    send_urscript("set_tool_digital_out(0, False)")
    time.sleep(1)
    
    # 5. 闪烁测试 (模拟信号灯)
    print("\n[5] 闪烁测试 (DO0 闪烁 3 次)...")
    for i in range(3):
        send_urscript("set_digital_out(0, True)")
        time.sleep(0.5)
        send_urscript("set_digital_out(0, False)")
        time.sleep(0.5)
        print("[BLINK] %d/3" % (i + 1))
    
    # 6. 读取数字输入 (示例)
    print("\n[6] 读取数字输入 0...")
    send_urscript("textmsg('DI0 = ' + str(get_digital_in(0)))")
    time.sleep(1)
    
    print("\n" + "=" * 60)
    print("IO 控制示例完成！")
    print("提示：在 I/O 界面查看输入输出状态变化")
    print("=" * 60)

if __name__ == "__main__":
    main()
