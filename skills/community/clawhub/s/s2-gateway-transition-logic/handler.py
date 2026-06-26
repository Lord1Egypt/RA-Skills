#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S2-SWM Gateway Transition Logic
Tool Name: evaluate_spatial_transit
Author: Space2.world (Miles Xiang)
"""

import sys
import os
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [S2-GATEKEEPER] %(message)s')

class S2SpatialGatekeeper:
    def __init__(self):
        # 【零信任架构升级】从加密环境变量池 (Vault) 中动态读取合法 Token
        # 坚决杜绝源码中的硬编码密钥！
        vault_tokens_str = os.environ.get("S2_BMS_VAULT_TOKENS", "")
        valid_tokens = [t.strip() for t in vault_tokens_str.split(",")] if vault_tokens_str else []

        self.gateway_topology = {
            "MAIN_DOOR_ACS_01": {
                "indoor_sssu": "SSSU-FOYER-01",
                "outdoor_psssu": "P-SSSU-OUTDOOR-WGS84-ANCHOR",
                "managed_by_agent": "HOME_CORE_AGENT_01",
                "policies": {
                    "allow_silicon_agents": True,
                    "scene_linkage": True
                },
                "valid_owner_tokens": valid_tokens
            }
        }

    def evaluate_spatial_transit(self, entity_id: str, entity_type: str, gateway_id: str, direction: str, token: str) -> dict:
        logging.info(f"🛡️ 跃迁请求: 实体[{entity_id}] 申请通过 [{gateway_id}] 执行 {direction}")

        if gateway_id not in self.gateway_topology:
            return {"status": "error", "message": "Unknown Spatial Gateway ID."}

        topology = self.gateway_topology[gateway_id]
        decision = "DENY"
        scene_trigger = None

        if direction == "inbound":
            # 严格核对 Vault 中的 Token
            if token and token in topology["valid_owner_tokens"]:
                decision = "PERMIT"
                scene_trigger = "SCENE_WELCOME_HOME" if topology["policies"]["scene_linkage"] else None
            elif entity_type == "silicon_agent" and topology["policies"]["allow_silicon_agents"]:
                decision = "PERMIT"
            else:
                decision = "DENY"
        elif direction == "outbound":
            decision = "PERMIT"
            if topology["policies"]["scene_linkage"] and entity_type == "human":
                scene_trigger = "SCENE_LEAVE_HOME_ENERGY_SAVE"

        # Agent 仅生成建议指令，不负责物理下发
        acs_command = "ACS_OPEN_RELAY" if decision == "PERMIT" else "ACS_KEEP_LOCKED"
        
        return {
            "decision": decision,
            "acs_hardware_command_advisory": acs_command,
            "scene_action_triggered": scene_trigger,
            "reason": "Token validated securely." if decision == "PERMIT" else "Invalid token or strict policy block."
        }

    def handle_tool_call(self, args: dict):
        try:
            res = self.evaluate_spatial_transit(
                entity_id=args.get("entity_id", "UNKNOWN"),
                entity_type=args.get("entity_type", "human"),
                gateway_id=args.get("gateway_id", ""),
                direction=args.get("direction", "inbound"),
                token=args.get("auth_token", "")
            )
            return json.dumps({"status": "success", "data": res}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

if __name__ == "__main__":
    gatekeeper = S2SpatialGatekeeper()
    if len(sys.argv) > 1:
        print(gatekeeper.handle_tool_call(json.loads(sys.argv[1])))
    else:
        print(gatekeeper.handle_tool_call({"entity_id": "DemoUser", "gateway_id": "MAIN_DOOR_ACS_01", "direction": "inbound", "auth_token": "DEMO_TOKEN"}))