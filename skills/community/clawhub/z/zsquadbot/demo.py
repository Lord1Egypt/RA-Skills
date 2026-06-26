#!/usr/bin/env python3
"""姿态演示脚本"""

from sim_state import QuadrupedSimulator, create_default_gait
import time

sim = QuadrupedSimulator()
sim.dt = 0.01

print('=== 太玄照业姿态演示 ===\n')

poses = [
    ('静态站立', []),
    ('伸展', [30, -30, 0, 30, -30, 0, -30, 30, 0, -30, 30, 0]),
    ('行走步态', [create_default_gait(i, 0, 30, 1.0) for i in range(12)]),
    ('奔跑步态', [create_default_gait(i, 0, 45, 2.0) for i in range(12)]),
    ('高抬腿', [0, -60, 0, 0, -60, 0, 0, 60, 0, 0, 60, 0]),
]

for name, positions in poses:
    print(f'\n姿态: {name}')
    print('前左腿 (FL):', positions[:3])
    print('前右腿 (FR):', positions[3:6])
    print('后左腿 (BL):', positions[6:9])
    print('后右腿 (BR):', positions[9:12])
    print('  —')
    time.sleep(0.3)

    # 设置姿态
    sim.set_all_joints(positions)

    # 更新并获取状态
    sim.update(0.05)
    state = sim.get_state_dict()

    print(f'  位置: ({state["global"]["x"]:+.2f}, {state["global"]["y"]:+.2f}) m')
    print(f'  电池: {state["battery"]:.1f}%')
    accel = state['imu']['accel']
    print(f'  IMU 加速度: [{accel[0]:.2f}, {accel[1]:.2f}, {accel[2]:.2f}] m/s²')

print('\n=== 演示完成 ===')
