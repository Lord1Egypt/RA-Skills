#!/usr/bin/env python3
"""
TM Robot - API 完整测试
测试 TMRobot 封装类的所有功能
"""

import asyncio
import sys
import os

# 添加 skill 目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tm_robot import TMRobot
from config import ROBOT_IP


async def test_connection():
    """测试连接"""
    print("\n[TEST] 建立连接...")
    robot = TMRobot(ROBOT_IP)
    
    # 测试 SVR 连接（状态读取）
    svr_ok = await robot.connect_svr()
    print(f"  SVR 连接: {'OK' if svr_ok else 'FAIL'}")
    
    # 测试 SCT 连接（运动控制）
    sct_ok = await robot.connect_sct()
    print(f"  SCT 连接: {'OK' if sct_ok else 'FAIL'}")
    
    return robot, svr_ok or sct_ok


async def test_state_read(robot):
    """测试状态读取"""
    print("\n[TEST] 读取状态...")
    
    state = await robot.get_state()
    print(f"  模式: {state.mode}")
    print(f"  错误码: {state.error_code}")
    print(f"  项目: {state.project}")
    
    if state.joints:
        print(f"  关节: {state.joints}")
    
    if state.pose:
        print(f"  位姿: {state.pose}")


async def test_joints_read(robot):
    """测试关节角度读取"""
    print("\n[TEST] 读取关节角度...")
    
    joints = await robot.get_joints()
    if joints:
        print(f"  {joints}")
        return True
    return False


async def test_pose_read(robot):
    """测试笛卡尔位姿读取"""
    print("\n[TEST] 读取位姿...")
    
    pose = await robot.get_pose()
    if pose:
        print(f"  {pose}")
        return True
    return False


async def test_motion(robot):
    """测试运动控制（仅当机器人正常时）"""
    print("\n[TEST] 运动控制...")
    
    state = await robot.get_state()
    if state.error_code != 0:
        print(f"  [SKIP] 机器人有错误码 {state.error_code}，跳过运动测试")
        return False
    
    try:
        # 尝试回零
        print("  移动到零点...")
        await robot.move_joints_zero(speed=0.05)
        print("  [OK] 回零命令已发送")
        return True
    except Exception as e:
        print(f"  [FAIL] 运动失败: {e}")
        return False


async def run_tests():
    """运行所有测试"""
    print("=" * 50)
    print("TM Robot API 完整测试")
    print(f"IP: {ROBOT_IP}")
    print("=" * 50)
    
    robot = None
    try:
        robot, connected = await test_connection()
        
        if not connected:
            print("\n[NOTE] 无法连接机器人，请检查：")
            print("  1. 机器人 IP 是否正确")
            print("  2. TMflow Listen Node 是否运行")
            print("  3. 机器人是否处于报警状态")
            return
        
        # 状态读取测试
        await test_state_read(robot)
        await test_joints_read(robot)
        await test_pose_read(robot)
        
        # 运动测试（需要机器人正常）
        await test_motion(robot)
        
        print("\n" + "=" * 50)
        print("测试完成")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n[ERROR] 测试异常: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if robot:
            await robot.disconnect()


def main():
    asyncio.run(run_tests())


if __name__ == "__main__":
    main()
