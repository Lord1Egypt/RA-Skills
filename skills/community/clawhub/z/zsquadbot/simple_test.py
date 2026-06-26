#!/usr/bin/env python3
"""简单的姿态演示"""

import time

# 直接读取并执行 sim_state.py
exec(open('/Users/liuxing/.openclaw/workspace/skills/quadruped/scripts/sim_state.py').read())

sim = QuadrupedSimulator()
sim.dt = 0.01

print('=== 太玄照业姿态演示 ===\n')

poses = [
    ("静态站立", [0]*12),
    ("高抬腿", [0, -60, 0, 0, -60, 0, 0, 60, 0, 0, 60, 0]),
    ("行走", [30, -30, 0, 30, -30, 0, -30, 30, 0, -30, 30, 0]),
]

for name, positions in poses:
    sim.set_all_joints(positions)
    sim.update(0.05)
    state = sim.get_state_dict()
    print(f"{name}: 位置 ({state['global']['x']:+.2f}, {state['global']['y']:+.2f}) m")

print('\n=== 演示完成 ===')
