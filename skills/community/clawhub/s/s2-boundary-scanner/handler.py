#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S2-SWM Boundary Scanner Engine (s2-boundary-scanner)
Core Logic: Parses mmWave radar data into Ego-Centric 9-Grid Boundary Topologies.
Author: Space2.world (Miles Xiang)
"""

import sys
import json
import logging
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s [S2-BOUNDARY-SCANNER] %(message)s')

class S2BoundaryScanner:
    """
    S2 动态边界扫描器
    基于毫米波雷达 (mmWave) 的自我中心九宫格 (Ego-Centric 9-Grid) 边界重构引擎。
    """
    def __init__(self):
        # 九宫格拓扑定义 (相对于中心点 0,0 的 X, Y 逻辑偏移)
        self.grid_topology = {
            "Grid_Front": (0, 1), "Grid_FrontRight": (1, 1), "Grid_Right": (1, 0),
            "Grid_BackRight": (1, -1), "Grid_Back": (0, -1), "Grid_BackLeft": (-1, -1),
            "Grid_Left": (-1, 0), "Grid_FrontLeft": (-1, 1)
        }

    def _get_material_by_rcs(self, rcs_value: float) -> str:
        """
        基于雷达散射截面 (Radar Cross Section) 推断边界物理材质
        """
        if rcs_value > 20.0:
            return "Metal/Glass (High Reflectivity, Rigid)"
        elif rcs_value > 5.0:
            return "Concrete/Brick (Medium Reflectivity, Rigid)"
        elif rcs_value > 1.0:
            return "Wood/Plastic (Low Reflectivity, Semi-Rigid)"
        else:
            return "Fabric/Organic (Absorbent, Soft)"

    def _simulate_mmwave_readings(self, heading_vector: str) -> dict:
        """
        模拟底层毫米波雷达的点云解析数据。
        在真实工程中，此处对接雷达串口或 ROS 话题 (如 /ti_mmwave/radar_scan)
        """
        # 假设具身机器人正向一堵玻璃墙走去，右侧有混凝土柱子
        raw_sensor_data = {
            "Grid_Front": {"distance_m": 0.8, "rcs": 25.5},       # 极近的高反光面
            "Grid_FrontRight": {"distance_m": 1.2, "rcs": 8.0},   # 混凝土结构
            "Grid_Right": {"distance_m": 3.0, "rcs": 0.5},        # 开放空间
            "Grid_BackRight": {"distance_m": 3.0, "rcs": 0.5},
            "Grid_Back": {"distance_m": 3.0, "rcs": 0.5},
            "Grid_BackLeft": {"distance_m": 3.0, "rcs": 0.5},
            "Grid_Left": {"distance_m": 2.5, "rcs": 2.0},         # 木质家具
            "Grid_FrontLeft": {"distance_m": 1.8, "rcs": 25.5}
        }
        return raw_sensor_data

    def execute_boundary_scan(self, center_hex_code: str, heading_vector: str, step_size_mm: int) -> dict:
        """
        核心动作：执行步进式边界扫描
        """
        logging.info(f"📡 实体位移 {step_size_mm}mm，启动九宫格毫米波边界扫描... 朝向: {heading_vector}")

        # 1. 获取底层雷达读数
        sensor_data = self._simulate_mmwave_readings(heading_vector)
        
        scanned_grids = {}
        collision_warnings = []

        # 2. 空间拓扑映射与侵入度计算 (Intrusion Calculus)
        for grid_id, data in sensor_data.items():
            dist = data["distance_m"]
            
            # SSSU 中心到边缘是 1.0 米。如果距离 < 1.0，说明边界侵入了该网格。
            if dist < 1.0:
                intrusion_pct = round(((1.0 - dist) / 1.0) * 100, 1)
                state = "Cut/Incomplete"
                if intrusion_pct > 80: # 侵入中心网格预警！
                     collision_warnings.append(f"CRITICAL: {grid_id} 边界已极度逼近中心绝对完整区！")
            elif dist < 2.0:
                intrusion_pct = 0.0
                state = "Intact but Blocked Adjacent"
            else:
                intrusion_pct = 0.0
                state = "Fully Open"

            scanned_grids[grid_id] = {
                "topological_state": state,
                "intrusion_percentage": intrusion_pct,
                "distance_to_boundary_m": dist,
                "material_inference": self._get_material_by_rcs(data["rcs"])
            }

        logging.info(f"✅ 36平米空间扫描完成。发现 {len(collision_warnings)} 处碰撞风险。")

        return {
            "ego_center": center_hex_code,
            "step_displacement_mm": step_size_mm,
            "peripheral_grids_state": scanned_grids,
            "collision_warnings": collision_warnings
        }

    def handle_tool_call(self, args: dict):
        try:
            res = self.execute_boundary_scan(
                center_hex_code=args.get("center_hex_code", "UNKNOWN"),
                heading_vector=args.get("heading_vector", "North"),
                step_size_mm=int(args.get("step_size_mm", 0))
            )
            return json.dumps({"status": "success", "data": res}, ensure_ascii=False, indent=2)
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

if __name__ == "__main__":
    scanner = S2BoundaryScanner()
    if len(sys.argv) > 1:
        print(scanner.handle_tool_call(json.loads(sys.argv[1])))
    else:
        # 演示：机器人向前步进 500 毫米后的环境扫描
        mock_input = {"center_hex_code": "(39.90°, 116.39°, 45.0m, 1000, 1500, 0)", "heading_vector": "North", "step_size_mm": 500}
        print(scanner.handle_tool_call(mock_input))