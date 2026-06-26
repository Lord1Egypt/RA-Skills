#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
场景演练：机器人从阳台进入，临时建图后，在正门执行 S2 全局原点对齐。
"""
import logging
from core.grid_alignment_engine import S2GridAlignmentEngine

logging.basicConfig(level=logging.INFO, format='%(message)s')

def run_alignment_scenario():
    print("="*60)
    print("🌍 S2-SWM 实战场景：异门闯入与强制网格吸附")
    print("="*60)

    # 1. 领主大脑初始化对齐引擎
    alignment_engine = S2GridAlignmentEngine()
    robot_id = "ROBOT-VACUUM-007"

    print(f"\n🤖 [状态] 机器人 {robot_id} 从【阳台】被开机...")
    print("🗺️  [局部建图] 机器人建立临时 SLAM，将阳台设为了本地原点 (0,0)。")
    print("❌ [空间冲突] 当前机器人的网格与领主的 SSSU 标准空间完全错位！")

    print("\n🔍 [巡航触发] 机器人移动到了【正门（入户门）】，识别到了 S2 绝对物理锚点。")
    
    # 机器人提取自己在临时 SLAM 坐标系下，看这个“正门”的位置
    # 假设在它的临时地图里，正门底线右顶点在 X=450cm, Y=320cm
    local_door_origin = {"x": 450.0, "y": 320.0} 
    # 正门底线中心点在 X=350cm, Y=320cm (意味着门朝向与领主系统有角度差)
    local_door_center = {"x": 350.0, "y": 320.0}

    print(f"📡 [发起协商] 机器人向领主提交本地锚点坐标: 原点={local_door_origin}, 中心={local_door_center}")
    
    # 2. 调用 S2 对齐引擎进行二维降维平移计算
    res = alignment_engine.execute_alignment(robot_id, local_door_origin, local_door_center)

    print("\n✅ [领主裁决] 对齐计算完成，下发二维平移矩阵：")
    transform = res["transform_matrix"]
    print(f"   -> X 轴强制平移: {transform['translation_x_cm']} cm")
    print(f"   -> Y 轴强制平移: {transform['translation_y_cm']} cm")
    print(f"   -> 坐标系旋转:  {transform['rotation_deg']} 度")
    print(f"   -> WGS84 绝对锚点已绑定: {res['anchor_wgs84']}")

    print("\n🎉 [最终结果] 机器人底层地图执行 Grid Snapping (网格吸附)。现在它与大楼数字孪生彻底同频共振！")
    print("="*60)

if __name__ == "__main__":
    run_alignment_scenario()