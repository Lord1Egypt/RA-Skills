"""
运动控制测试 - 自动执行版本
安全位置：J3=90°, J5=90°
速度：50%
"""

import sys
sys.path.insert(0, '.')
from tm_robot import TMRobot
import asyncio

async def test():
    robot = TMRobot('192.168.1.13')
    
    print('='*60)
    print('TM Robot 运动控制测试 - 安全位置')
    print('='*60)
    
    # 连接
    print('\n[连接]')
    await robot.connect_svr()
    await robot.connect_sct()
    
    # 当前位置
    print('\n[当前位置]')
    joints = await robot.get_joints()
    if joints:
        print(f'J1={joints.j1:6.1f}°, J2={joints.j2:6.1f}°, J3={joints.j3:6.1f}°')
        print(f'J4={joints.j4:6.1f}°, J5={joints.j5:6.1f}°, J6={joints.j6:6.1f}°')
    
    # 运动到安全位置
    print('\n[运动] 目标：[0, 0, 90, 0, 90, 0], 速度 50%')
    print('>>> 开始运动...')
    
    success = await robot.move_joint([0, 0, 90, 0, 90, 0], speed=0.5)
    
    if success:
        print('[OK] 运动完成')
        
        # 读取新位置
        print('\n[新位置]')
        joints2 = await robot.get_joints()
        if joints2:
            print(f'J1={joints2.j1:6.1f}°, J2={joints2.j2:6.1f}°, J3={joints2.j3:6.1f}°')
            print(f'J4={joints2.j4:6.1f}°, J5={joints2.j5:6.1f}°, J6={joints2.j6:6.1f}°')
            
            # 验证
            print('\n[验证]')
            j3_ok = abs(joints2.j3 - 90) < 2
            j5_ok = abs(joints2.j5 - 90) < 2
            print(f'J3 = {joints2.j3:.1f}° {"[OK]" if j3_ok else "[FAIL]"}')
            print(f'J5 = {joints2.j5:.1f}° {"[OK]" if j5_ok else "[FAIL]"}')
    else:
        print('[FAIL] 运动失败')
    
    await robot.disconnect()
    print('\n' + '='*60)

asyncio.run(test())
