#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UR Robot - IO 控制测试
测试数字 IO 和模拟 IO
"""

from ur_rtde import RTDEReceiveInterface, RTDESendInterface
import time

ROBOT_IP = "192.168.56.101"

print("=" * 70)
print("UR Robot - IO Control Test")
print("=" * 70)

try:
    rtde_r = RTDEReceiveInterface(ROBOT_IP)
    rtde_s = RTDESendInterface(ROBOT_IP)
    print("[OK] Connected\n")
    
    # 1. 数字输入测试
    print("=" * 70)
    print("1. 数字输入 (DI)")
    print("=" * 70)
    
    for i in range(8):
        try:
            # UR 的 IO 读取需要通过 getActualDigitalInputBits
            if i == 0:
                digital_inputs = rtde_r.getActualDigitalInputBits()
                print(f"所有 DI: {digital_inputs}")
                break
        except Exception as e:
            print(f"DI[{i}]: 读取失败 - {e}")
    
    # 2. 数字输出测试
    print("\n" + "=" * 70)
    print("2. 数字输出 (DO)")
    print("=" * 70)
    
    print("\n测试 DO0-DO7...")
    for i in range(8):
        try:
            # UR 的 DO 控制通过 sendStandardDigitalOutput
            rtde_s.sendStandardDigitalOutput(i, True)
            print(f"DO[{i}]: ON")
            time.sleep(0.5)
            
            rtde_s.sendStandardDigitalOutput(i, False)
            print(f"DO[{i}]: OFF")
            time.sleep(0.3)
        except Exception as e:
            print(f"DO[{i}]: 控制失败 - {e}")
    
    # 3. 模拟输入测试
    print("\n" + "=" * 70)
    print("3. 模拟输入 (AI)")
    print("=" * 70)
    
    try:
        analog_inputs = rtde_r.getAnalogInputVoltage()
        print(f"AI 电压：{analog_inputs}")
    except Exception as e:
        print(f"AI 读取失败：{e}")
    
    # 4. 模拟输出测试
    print("\n" + "=" * 70)
    print("4. 模拟输出 (AO)")
    print("=" * 70)
    
    try:
        print("\n测试 AO0 (0V → 5V → 10V → 5V → 0V)...")
        for voltage in [0, 5, 10, 5, 0]:
            rtde_s.sendStandardAnalogOutput(0, voltage/10.0)  # 0-1 归一化
            print(f"AO0: {voltage}V")
            time.sleep(1)
    except Exception as e:
        print(f"AO 控制失败：{e}")
    
    # 5. 工具 IO (如果配置了)
    print("\n" + "=" * 70)
    print("5. 工具 IO (Tool IO)")
    print("=" * 70)
    
    try:
        print("工具 IO 需要配置工具设备")
        print("跳过测试...")
    except Exception as e:
        print(f"工具 IO: {e}")
    
    # 断开
    rtde_r.disconnect()
    rtde_s.disconnect()
    
    print("\n[OK] IO 测试完成！✅")
    print("=" * 70)
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    print("\n可能的问题:")
    print("1. URSim 未启动")
    print("2. IO 模块未配置")
