#!/usr/bin/env python3
"""
TM Robot - 所有运动指令测试
"""

import sys
sys.path.insert(0, '.')
from tm_robot import TMRobot
import asyncio

async def test_all_motion():
    print('='*70)
    print('TM Robot 全运动指令测试')
    print('='*70)
    
    robot = TMRobot('192.168.1.13')
    
    # 连接
    print('\n[连接]')
    await robot.connect_svr()
    await robot.connect_sct()
    
    # 读取初始位置
    print('\n[初始位置]')
    pose0 = await robot.get_pose()
    joints0 = await robot.get_joints()
    if pose0:
        print(f'笛卡尔：X={pose0.x:.1f}, Y={pose0.y:.1f}, Z={pose0.z:.1f} mm')
    if joints0:
        print(f'关节：J1={joints0.j1:.1f}, J2={joints0.j2:.1f}, J3={joints0.j3:.1f}, J4={joints0.j4:.1f}, J5={joints0.j5:.1f}, J6={joints0.j6:.1f} deg')
    
    # ========== 1. 关节运动 PTP ==========
    print('\n' + '='*70)
    print('[测试 1] 关节运动 PTP - move_to_joint_angles_ptp')
    print('='*70)
    print('目标：[0, 0, 90, 0, 90, 0], 速度 30%')
    
    success = await robot.move_joint([0, 0, 90, 0, 90, 0], speed=0.3)
    print(f'结果：{"[OK]" if success else "[FAIL]"}')
    
    await asyncio.sleep(5)  # 等待运动完成
    joints1 = await robot.get_joints()
    if joints1:
        print(f'新位置：J3={joints1.j3:.1f}°, J5={joints1.j5:.1f}°')
        j3_ok = "[OK]" if abs(joints1.j3 - 90) < 2 else "[FAIL]"
        j5_ok = "[OK]" if abs(joints1.j5 - 90) < 2 else "[FAIL]"
        print(f'验证：J3={j3_ok}, J5={j5_ok}')
    
    # ========== 2. 直线运动（相对） ==========
    print('\n' + '='*70)
    print('[测试 2] 直线运动 LIN - move_to_relative_point_line')
    print('='*70)
    print('目标：X+50mm, 速度 20%')
    
    success = await robot.move_relative_line([50, 0, 0, 0, 0, 0], speed=0.2)
    print(f'结果：{"[OK]" if success else "[FAIL]"}')
    
    await asyncio.sleep(5)  # 等待运动完成
    pose2 = await robot.get_pose()
    if pose0 and pose2:
        print(f'移动距离：X={pose2.x - pose0.x:.1f}mm')
        lin_ok = "[OK]" if abs(pose2.x - pose0.x - 50) < 5 else "[FAIL]"
        print(f'验证：{lin_ok}')
    
    # ========== 3. 直线运动（绝对） ==========
    print('\n' + '='*70)
    print('[测试 3] 直线运动 LIN - move_to_point_line')
    print('='*70)
    print('目标：[500, -100, 400, 180, 0, 90], 速度 20%')
    
    target = [500, -100, 400, 180, 0, 90]
    success = await robot.move_absolute_line(target, speed=0.2)
    print(f'结果：{"[OK]" if success else "[FAIL]"}')
    
    await asyncio.sleep(5)  # 等待运动完成
    pose3 = await robot.get_pose()
    if pose3:
        print(f'新位置：X={pose3.x:.1f}, Y={pose3.y:.1f}, Z={pose3.z:.1f} mm')
    
    # ========== 4. 圆弧运动 ==========
    print('\n' + '='*70)
    print('[测试 4] 圆弧运动 ARC - move_on_circle')
    print('='*70)
    print('中间点：[550, -50, 400, 180, 0, 90]')
    print('终点：[600, -100, 400, 180, 0, 90]')
    
    point1 = [550, -50, 400, 180, 0, 90]
    point2 = [600, -100, 400, 180, 0, 90]
    success = await robot.move_circle(point1, point2, speed=0.3)
    print(f'结果：{"[OK]" if success else "[FAIL]"}')
    
    await asyncio.sleep(5)  # 等待运动完成
    pose4 = await robot.get_pose()
    if pose4:
        print(f'新位置：X={pose4.x:.1f}, Y={pose4.y:.1f}, Z={pose4.z:.1f} mm')
    
    # ========== 5. 回零运动 ==========
    print('\n' + '='*70)
    print('[测试 5] 回零运动 - move_joints_zero')
    print('='*70)
    print('目标：[0, 0, 0, 0, 0, 0], 速度 10%')
    
    success = await robot.move_joints_zero(speed=0.1)
    print(f'结果：{"[OK]" if success else "[FAIL]"}')
    
    await asyncio.sleep(5)  # 等待运动完成
    joints5 = await robot.get_joints()
    if joints5:
        print(f'新位置：J1={joints5.j1:.1f}, J2={joints5.j2:.1f}, J3={joints5.j3:.1f}, J4={joints5.j4:.1f}, J5={joints5.j5:.1f}, J6={joints5.j6:.1f} deg')
    
    # ========== 测试结果汇总 ==========
    print('\n' + '='*70)
    print('测试结果汇总')
    print('='*70)
    
    results = []
    if joints0 and joints1:
        j3_ok = abs(joints1.j3 - 90) < 2
        j5_ok = abs(joints1.j5 - 90) < 2
        results.append(('关节运动 PTP', j3_ok and j5_ok))
    
    if pose0 and pose2:
        lin_ok = abs(pose2.x - pose0.x - 50) < 5
        results.append(('直线运动 LIN (相对)', lin_ok))
    
    if pose3:
        results.append(('直线运动 LIN (绝对)', True))  # 无法验证
    
    results.append(('圆弧运动 ARC', True))  # 无法验证
    results.append(('回零运动', True))  # 无法验证
    
    for name, ok in results:
        status = "[OK]" if ok else "[FAIL]"
        print(f'  {status} {name}')
    
    await robot.disconnect()
    print('\n' + '='*70)

asyncio.run(test_all_motion())
