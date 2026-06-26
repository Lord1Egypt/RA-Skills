#!/bin/bash
# 完整测试所有四足机器人功能

set -e

echo "=== 四足机器人技能完整测试 ==="
echo ""

# 设置Python路径
export PYTHONPATH="/Users/liuxing/.openclaw/workspace/skills/quadruped:$PYTHONPATH"

# 1. 测试步态生成器
echo "1. 测试步态生成器..."
python3 scripts/gait_generator.py
echo ""

# 2. 测试运动导出
echo "2. 测试运动导出..."
python3 scripts/motion_export.py
echo ""

# 3. 测试虚拟机器人
echo "3. 测试虚拟机器人模拟..."
python3 demo.py
echo ""

# 4. 显示技能包信息
echo "4. 技能包信息..."
ls -lh quadruped.skill
echo ""

echo "=== 所有测试完成 ==="
echo ""
echo "运行交互式控制:"
echo "  python3 scripts/sim_control.py"
echo ""
echo "步态生成示例:"
echo "  python3 scripts/gait_generator.py --gait trot"
echo ""
echo "运动导出示例:"
echo "  python3 scripts/motion_export.py --format csv"
