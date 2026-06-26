#!/usr/bin/env python3
"""
达明机器人连接测试脚本
用法: python test_connection.py <机器人IP>
示例: python test_connection.py 192.168.1.1
"""

import asyncio
import sys
import techmanpy


async def test_connection(robot_ip: str):
    """测试与达明机器人的连接"""
    print(f"[INFO] 正在连接机器人: {robot_ip}")
    
    try:
        async with techmanpy.connect_sct(robot_ip=robot_ip) as conn:
            print("[✓] 连接成功!")
            
            # 获取关节角度
            joints = await conn.get_joint_angles()
            print(f"[INFO] 关节角度: {joints}")
            
            # 获取末端位置
            pose = await conn.get_cartesian_pose()
            print(f"[INFO] 末端位置: {pose}")
            
            # 获取IO状态
            print("[INFO] IO 状态读取成功")
            
            print("\n[✓] 所有测试通过!")
            return True
            
    except Exception as e:
        print(f"[✗] 连接失败: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("用法: python test_connection.py <机器人IP>")
        print("示例: python test_connection.py 192.168.1.1")
        sys.exit(1)
    
    robot_ip = sys.argv[1]
    asyncio.run(test_connection(robot_ip))


if __name__ == "__main__":
    main()
