#!/usr/bin/env python3
"""
达明机器人基础控制示例
包含: 获取状态、移动、IO控制等基础操作
"""

import asyncio
import techmanpy


# ============================================================
# 基础配置
# ============================================================
# 请修改为你的机器人IP
ROBOT_IP = "192.168.1.1"  # TODO: 修改为实际IP


# ============================================================
# 示例1: 获取机器人状态
# ============================================================
async def get_status():
    """获取机器人关节角度和末端位置"""
    print("[INFO] 获取机器人状态...")
    
    async with techmanpy.connect_sct(robot_ip=ROBOT_IP) as conn:
        # 获取关节角度 (度)
        joints = await conn.get_joint_angles()
        print(f"  关节角度: {joints}")
        
        # 获取末端位置 (mm) 和姿态 (度)
        pose = await conn.get_cartesian_pose()
        print(f"  末端位置: {pose}")
        
        # 获取机器人模式
        print(f"  机器人模式: {await conn.get_robot_mode()}")
        
    print("[OK] 状态读取完成\n")


# ============================================================
# 示例2: 关节运动 (PTP)
# ============================================================
async def move_ptp():
    """PTP 运动 - 关节插补"""
    print("[INFO] 执行PTP运动...")
    
    async with techmanpy.connect_sct(robot_ip=ROBOT_IP) as conn:
        # 移动到目标关节角度
        # 格式: [J1, J2, J3, J4, J5, J6] 单位: 度
        # 参数: 关节角度, 速度比例(0-1), 加速度比例(0-1)
        target = [0, 0, 0, 0, 0, 0]
        speed = 0.1  # 10% 速度
        acc = 50     # 50% 加速度
        
        print(f"  目标: {target}")
        print(f"  速度: {speed}, 加速度: {acc}")
        
        await conn.move_to_joint_angles_ptp(target, speed, acc)
        print("  运动完成!")
        
    print("[OK] PTP运动完成\n")


# ============================================================
# 示例3: 直线运动 (LINE)
# ============================================================
async def move_line():
    """直线运动 - 笛卡尔空间"""
    print("[INFO] 执行直线运动...")
    
    async with techmanpy.connect_sct(robot_ip=ROBOT_IP) as conn:
        # 获取当前位置
        current = await conn.get_cartesian_pose()
        print(f"  当前位置: {current}")
        
        # 简单直线运动 - Z轴上升 100mm
        # 格式: [X, Y, Z, RX, RY, RZ] 单位: mm 和 度
        target = list(current)
        target[2] += 100  # Z轴上升
        
        print(f"  目标位置: {target}")
        
        # 速度 mm/s, 加速度 mm/s^2
        await conn.move_to_position_ptp(target, 50, 500)
        print("  运动完成!")
        
    print("[OK] 直线运动完成\n")


# ============================================================
# 示例4: IO控制
# ============================================================
async def control_io():
    """数字IO控制"""
    print("[INFO] 控制数字IO...")
    
    async with techmanpy.connect_sct(robot_ip=ROBOT_IP) as conn:
        # 读取所有数字输入
        print("  读取数字输入...")
        for i in range(8):
            val = await conn.get_digital_input(i)
            if val:
                print(f"    DI[{i}] = {val}")
        
        # 读取所有数字输出
        print("  读取数字输出...")
        for i in range(8):
            val = await conn.get_digital_output(i)
            if val:
                print(f"    DO[{i}] = {val}")
                
        # 设置数字输出 (示例: DO[0] = True)
        # await conn.set_digital_output(0, True)
        # print("  DO[0] 设置为 True")
        
    print("[OK] IO控制完成\n")


# ============================================================
# 示例5: 监听TMFlow服务器
# ============================================================
async def listen_tmflow():
    """监听TMFlow广播消息"""
    print("[INFO] 监听TMFlow服务器...")
    print("  按 Ctrl+C 退出")
    
    def print_broadcast(msg):
        print(f"  [Broadcast] {msg}")
    
    async with techmanpy.connect_svr(robot_ip=ROBOT_IP) as conn:
        conn.add_broadcast_callback(print_broadcast)
        await conn.keep_alive()


# ============================================================
# 主函数 - 运行所有测试
# ============================================================
async def run_all_tests():
    """运行所有基础测试"""
    print("=" * 50)
    print("达明机器人基础测试")
    print(f"机器人IP: {ROBOT_IP}")
    print("=" * 50 + "\n")
    
    try:
        # 依次执行测试
        await get_status()
        await move_ptp()
        await control_io()
        
        print("=" * 50)
        print("所有测试完成!")
        print("=" * 50)
        
    except Exception as e:
        print(f"[ERROR] 测试失败: {e}")


if __name__ == "__main__":
    asyncio.run(run_all_tests())
