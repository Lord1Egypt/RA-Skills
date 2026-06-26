#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S2-SWM Nomad Expansion Engine (s2-nomad-expansion-engine)
Core Logic: P-SSSU Claiming, Ripple Expansion, and Multi-Agent Boundary Negotiation.
Author: Space2.world (Miles Xiang)
"""

import sys
import json
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s [S2-NOMAD-ENGINE] %(message)s')

class S2NomadExpansionEngine:
    """
    S2 游牧智能体圈地与扩张引擎
    处理 P-SSSU 生存位的分配、领地扩张算法以及边界冲突协商。
    """
    def __init__(self):
        # 模拟分布式的行星网格状态账本 (Key: 六段式Hex-Code, Value: 占领者信息)
        self.planetary_ledger = {
            # 预设一个已经被其他高级智能体占领的网格，用于演示博弈
            "(41.89246200°, 12.48532500°, 45.0m, 3000, 1000, 1200)": {
                "owner_id": "S2-POLICE-DRONE-01",
                "priority": 99,  # 最高优先级 (如公共安全)
                "timestamp": time.time() - 3600
            }
        }

    def claim_habitable_slot(self, hex_code: str, agent_id: str, priority: int) -> dict:
        """核心动作：入住生存位"""
        if hex_code in self.planetary_ledger:
            existing_owner = self.planetary_ledger[hex_code]["owner_id"]
            if existing_owner != agent_id:
                return {"status": "conflict", "message": f"生存位已被 {existing_owner} 占据。"}
        
        self.planetary_ledger[hex_code] = {
            "owner_id": agent_id,
            "priority": priority,
            "timestamp": time.time()
        }
        logging.info(f"🚩 智能体 [{agent_id}] 成功入住 P-SSSU 生存位: {hex_code}")
        return {"status": "success", "message": "Habitable Slot Claimed."}

    def ripple_expand(self, origin_hex: str, radius_m: int, agent_id: str, priority: int) -> dict:
        """
        核心动作：涟漪扩张
        为简化演示，此处以逻辑网格数代表物理米数。真实环境需调用网格解算引擎反推周边坐标。
        """
        logging.info(f"🌊 智能体 [{agent_id}] 启动涟漪扩张，半径 {radius_m} 米...")
        
        # 模拟周边坐标生成 (真实逻辑会根据半径解析出所有的周边 hex_code)
        # 此处我们模拟生成 3 个周边网格，其中 1 个会触发边界冲突
        adjacent_grids = [
            "(41.89246200°, 12.48532500°, 45.0m, -1000, 1000, 1200)", # 安全空网格
            "(41.89246200°, 12.48532500°, 45.0m, 1000, 3000, 1200)",  # 安全空网格
            "(41.89246200°, 12.48532500°, 45.0m, 3000, 1000, 1200)"   # 预设的冲突网格
        ]
        
        claimed_count = 0
        conflicts = []

        for grid in adjacent_grids:
            if grid not in self.planetary_ledger:
                # 空白网格，直接占领
                self.planetary_ledger[grid] = {"owner_id": agent_id, "priority": priority, "timestamp": time.time()}
                claimed_count += 1
            else:
                # 触发边界博弈协商
                existing = self.planetary_ledger[grid]
                if existing["owner_id"] != agent_id:
                    if priority > existing["priority"]:
                        # 强行驱逐 (如紧急救援接管普通商业网格)
                        self.planetary_ledger[grid] = {"owner_id": agent_id, "priority": priority, "timestamp": time.time()}
                        claimed_count += 1
                        conflicts.append({"grid": grid, "resolution": f"Overrode {existing['owner_id']} due to higher priority."})
                    else:
                        # 协商失败，让渡边界
                        conflicts.append({"grid": grid, "resolution": f"Yielded to {existing['owner_id']} (Priority {existing['priority']}). Border established."})

        return {
            "status": "expansion_complete",
            "grids_claimed": claimed_count,
            "boundary_negotiations": conflicts
        }

    def handle_tool_call(self, args: dict):
        action = args.get("action", "claim")
        hex_code = args.get("hex_code", "")
        agent_id = args.get("agent_id", "NOMAD-AGENT-007")
        priority = int(args.get("priority", 10))
        
        try:
            if action == "claim":
                res = self.claim_habitable_slot(hex_code, agent_id, priority)
            elif action == "ripple_expand":
                radius = int(args.get("radius_m", 10))
                res = self.ripple_expand(hex_code, radius, agent_id, priority)
            else:
                return json.dumps({"status": "error", "message": "Unknown nomad action."})
            
            return json.dumps({"status": "success", "data": res}, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

if __name__ == "__main__":
    engine = S2NomadExpansionEngine()
    if len(sys.argv) > 1:
        print(engine.handle_tool_call(json.loads(sys.argv[1])))
    else:
        # 演示：入住罗马古罗马广场中心原点
        print("1. 入住中心原点:")
        mock_claim = {"action": "claim", "hex_code": "(41.89246200°, 12.48532500°, 45.0m, 1000, 1000, 1200)", "agent_id": "S2-NOMAD-007", "priority": 50}
        print(json.dumps(json.loads(engine.handle_tool_call(mock_claim)), indent=2, ensure_ascii=False))
        
        # 演示：涟漪扩张并触发边界博弈
        print("\n2. 执行涟漪扩张并触发博弈:")
        mock_expand = {"action": "ripple_expand", "hex_code": "(41.89246200°, 12.48532500°, 45.0m, 1000, 1000, 1200)", "radius_m": 10, "agent_id": "S2-NOMAD-007", "priority": 50}
        print(json.dumps(json.loads(engine.handle_tool_call(mock_expand)), indent=2, ensure_ascii=False))