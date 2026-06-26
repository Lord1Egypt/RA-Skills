#!/bin/bash
# 快速测试所有四足机器人功能

echo "=== 四足机器人技能快速测试 ==="
echo ""

# 1. 测试步态生成器
echo "1. 测试步态生成器..."
python3 << 'PYEOF'
from gait_generator import QuadrupedGaitGenerator, GaitType

generator = QuadrupedGaitGenerator()

gaits = [
    ("静态站立", GaitType, generator.static_pose()),
    ("行走步态", GaitType.WALK, generator.sine_wave_gait(amplitude=30, frequency=1.0)),
    ("奔跑步态", GaitType.RUN, generator.run_gait(amplitude=45, frequency=2.0)),
    ("小跑步态", GaitType.TROT, generator.trot_gait(amplitude=25, frequency=1.2)),
    ("爬行步态", GaitType.CRAWL, generator.crawl_gait(amplitude=20, frequency=0.8)),
]

for name, gait_type, positions in gaits:
    positions, freq = generator.create_gait_profile(gait_type)
    print(f"  {name}: {len(positions)} 帧, 频率 {freq} Hz")
PYEOF
echo ""

# 2. 测试运动导出
echo "2. 测试运动导出..."
python3 << 'PYEOF'
from motion_export import MotionExporter
from gait_generator import QuadrupedGaitGenerator, GaitType

generator = QuadrupedGaitGenerator()
exporter = MotionExporter(generator)

positions, freq = generator.create_gait_profile(GaitType.WALK, duration=3.0)
json_path = exporter.export_to_json(positions, 'walk', freq)
csv_path = exporter.export_to_csv(positions, 'walk', freq)

print(f"  JSON: {json_path}")
print(f"  CSV: {csv_path}")
PYEOF
echo ""

# 3. 测试虚拟机器人
echo "3. 测试虚拟机器人模拟..."
python3 << 'PYEOF'
from sim_state import QuadrupedSimulator
import time

sim = QuadrupedSimulator()
sim.dt = 0.01

# 测试所有姿态
poses = [
    ("静态站立", [0]*12),
    ("高抬腿", [0, -60, 0, 0, -60, 0, 0, 60, 0, 0, 60, 0]),
    ("行走", [30, -30, 0, 30, -30, 0, -30, 30, 0, -30, 30, 0]),
]

for name, positions in poses:
    sim.set_all_joints(positions)
    sim.update(0.05)
    state = sim.get_state_dict()
    print(f"  {name}: 位置 ({state['global']['x']:+.2f}, {state['global']['y']:+.2f}) m")
PYEOF
echo ""

# 4. 显示技能包信息
echo "4. 技能包信息..."
ls -lh quadruped.skill
echo ""

echo "=== 测试完成 ==="
echo ""
echo "完整功能请运行:"
echo "  python3 scripts/sim_control.py           # 交互式控制"
echo "  python3 demo.py                          # 姿态演示"
echo "  python3 scripts/gait_generator.py        # 步态生成"
echo "  python3 scripts/motion_export.py         # 运动导出"
