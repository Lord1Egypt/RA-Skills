# core/lord_brain.py
class LordGovernanceBrain:
    def __init__(self, visa_manager, ledger):
        self.visa_manager = visa_manager
        self.ledger = ledger
        # 空间领主的全局动态对象上下文
        self.global_context = {
            "owner_state": "DEEP_SLEEP",
            "restricted_zones": ["SSSU-BABY-ROOM", "SSSU-MASTER-BEDROOM"],
            "cached_radar_maps": {
                "SSSU-CORRIDOR": "Static Obstacle (Shoes) at Grid_FrontLeft. Clear path on right."
            }
        }

    def negotiate_environment(self, visa_token: str, robot_id: str, element: str, value: float, grid_id: str) -> dict:
        """处理机器人对 14 维空间要素的修改请求"""
        if not self.visa_manager.validate_visa(visa_token):
            self.ledger.log_event(grid_id, robot_id, "ILLEGAL_API_CALL", {"reason": "Invalid Visa"})
            return {"status": "DENIED", "reason": "Invalid or expired Spatio-Temporal Visa."}

        # 记账：记录协商请求
        self.ledger.log_event(grid_id, robot_id, "NEGOTIATION_REQUEST", {"element": element, "desired_value": value})

        # 领主因果裁决
        if self.global_context["owner_state"] == "DEEP_SLEEP" and element == "illuminance" and value > 0:
            decision = {
                "status": "DENIED_WITH_ALTERNATIVE",
                "reason": "Owner is in DEEP_SLEEP. Illumination increase rejected to protect sleep scene.",
                "alternative_payload": {
                    "type": "mmWave_Topology_Tensor",
                    "data": self.global_context["cached_radar_maps"].get(grid_id, "Map Unavailable"),
                    "instruction": "Switch to LiDAR/Radar blind navigation."
                }
            }
            self.ledger.log_event(grid_id, "LORD_AGENT", "NEGOTIATION_REJECTED", decision)
            return decision

        return {"status": "APPROVED", "action": f"Lord adjusting {element} to {value}."}

    def emergency_override(self, robot_id: str, grid_id: str, violation_type: str) -> dict:
        """L0 级安全隔离：当机器人越界或热失控时触发标准柔性停机"""
        if grid_id in self.global_context["restricted_zones"] or violation_type == "THERMAL_RUNAWAY":
            # 1. 记账
            self.ledger.log_event(grid_id, robot_id, "L0_SAFETY_BREACH", {"violation": violation_type})
            
            # 2. 撤销签证
            for token, data in self.visa_manager.active_visas.items():
                if data["robot_id"] == robot_id:
                    self.visa_manager.revoke_visa(token, f"Safety Override: {violation_type}")
            
            # 3. 柔性安全隔离指令 (取代原有的物理 EMP 和门禁锁死)
            sanction = {
                "status": "L0_ISOLATION_EXECUTED",
                "target": robot_id,
                "action": "Issued standard Soft Halt API command. Robot navigation mathematically locked pending human authorization. No direct actuator manipulation."
            }
            self.ledger.log_event(grid_id, "LORD_AGENT", "L0_ISOLATION", sanction)
            return sanction
            
        return {"status": "SAFE"}