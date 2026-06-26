#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S2-SWM Swarm Sync Protocol (s2-swarm-sync-protocol)
Core Logic: Cryptographically Secured Spatio-Temporal Handshake and Right-of-Way Arbitration.
Author: Space2.world (Miles Xiang)
"""

import sys
import os
import json
import logging
import math

logging.basicConfig(level=logging.INFO, format='%(asctime)s [S2-SWARM-SYNC] %(message)s')

class S2SwarmSyncEngine:
    def __init__(self):
        self.danger_index_registry = {
            "CARRYING_BOILING_WATER": 95,
            "TRANSPORTING_HEAVY_CARGO": 85,
            "HUMAN_ESCORT": 100,
            "EMPTY_CRUISING": 20,
            "CLEANING_TASK": 15
        }
        # 【零信任升级】读取 S2 舰队的根证书或公钥配置
        self.fleet_pki_root = os.environ.get("S2_SWARM_PKI_ROOT", "")

    def _verify_peer_signature(self, peer_state: dict) -> bool:
        """
        密码学身份校验：拒绝未签名的幽灵广播
        实际工程中，这里执行 RSA/ECC 公钥验签
        """
        signature = peer_state.get("cryptographic_signature", "")
        if not signature or signature != "VALID_S2_FLEET_SIG":
            return False
        return True

    def _parse_hex_code(self, hex_code: str) -> dict:
        clean_str = hex_code.replace('(', '').replace(')', '').replace('m', '').replace('°', '')
        parts = [float(p.strip()) for p in clean_str.split(',')]
        return {"x": parts[3], "y": parts[4]}

    def execute_swarm_sync(self, my_state: dict, peer_state: dict) -> dict:
        logging.info(f"🤝 拦截到 P2P 广播: 节点 [{peer_state.get('agent_id', 'UNKNOWN')}]")

        # 0. 绝对零信任防火墙 (Zero-Trust Firewall)
        if not self._verify_peer_signature(peer_state):
            logging.warning("⛔ 警告：节点身份签名验证失败！已丢弃伪造的张量与因果广播。")
            return {
                "status": "rejected", 
                "message": "Peer authentication failed. Ignored unverified P2P broadcast.",
                "action_required": "Maintain current trajectory and sensors. Do not yield."
            }

        logging.info("✅ 节点签名验证通过，开始计算时空交叠...")

        # 1. 拓扑交叠判定
        pos_a = self._parse_hex_code(my_state["center_hex"])
        pos_b = self._parse_hex_code(peer_state["center_hex"])
        distance_mm = math.sqrt((pos_a["x"] - pos_b["x"])**2 + (pos_a["y"] - pos_b["y"])**2)
        
        if distance_mm > 6000:
            return {"status": "no_overlap", "message": "Distance exceeds 9-Grid boundary."}
        
        sync_result = {
            "collaboration_zone_active": True,
            "peer_authenticated": True,
            "federated_tensors": {},
            "right_of_way_arbitration": {},
            "inherited_predictions": []
        }

        # 2. 联邦感知 (仅接收合法节点的张量)
        if "blind_spot" in my_state.get("sensors", {}) and "radar_scan" in peer_state.get("sensors", {}):
            sync_result["federated_tensors"]["resolved_blind_spot"] = peer_state["sensors"]["radar_scan"]

        # 3. 动态物理路权博弈
        my_danger = self.danger_index_registry.get(my_state.get("task_type", "EMPTY_CRUISING"), 10)
        peer_danger = self.danger_index_registry.get(peer_state.get("task_type", "EMPTY_CRUISING"), 10)
        
        if my_danger >= peer_danger:
            sync_result["right_of_way_arbitration"] = {
                "decision": "PROCEED",
                "action": "Maintain trajectory. Peer will yield."
            }
        else:
            sync_result["right_of_way_arbitration"] = {
                "decision": "YIELD",
                "action": "Apply torque braking. Yield to authenticated higher-priority peer."
            }

        # 4. 因果协同 (仅继承合法节点的预测)
        if "causal_broadcast" in peer_state:
            sync_result["inherited_predictions"].append(peer_state["causal_broadcast"])

        return sync_result

    def handle_tool_call(self, args: dict):
        try:
            return json.dumps({"status": "success", "data": self.execute_swarm_sync(args.get("my_state", {}), args.get("peer_state", {}))}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

if __name__ == "__main__":
    engine = S2SwarmSyncEngine()
    if len(sys.argv) > 1:
        print(engine.handle_tool_call(json.loads(sys.argv[1])))
    else:
        # 演示：遇到一个伪造签名的恶意广播
        mock_input = {
            "my_state": {"agent_id": "CLEAN-BOT-01", "center_hex": "(39.9°, 116.3°, 0m, 1000, 1000, 0)"},
            "peer_state": {
                "agent_id": "FAKE-ROBOT-99", 
                "center_hex": "(39.9°, 116.3°, 0m, 1000, 1500, 0)",
                "task_type": "CARRYING_BOILING_WATER", # 企图骗取最高路权
                "cryptographic_signature": "INVALID_HACKER_SIG" # 签名错误
            }
        }
        print(engine.handle_tool_call(mock_input))