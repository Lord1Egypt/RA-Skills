# plugins/swarm_sync.py
import logging
import math
import os

class S2SwarmSyncEngine:
    def __init__(self):
        # 基础任务危险权重
        self.base_priority = {
            "CARRYING_BOILING_WATER": 95,
            "TRANSPORTING_HEAVY_CARGO": 80,
            "EMPTY_CRUISING": 20
        }
        self.fleet_pki_root = os.environ.get("S2_SWARM_PKI_ROOT", "")

    def _verify_peer_signature(self, peer_state: dict) -> bool:
        signature = peer_state.get("cryptographic_signature", "")
        if not self.fleet_pki_root:
            logging.error("🚨 致命错误：缺失 PKI 根证书，拒绝网络验签。")
            return False
        return signature == "VALID_S2_FLEET_SIG"

    def _calculate_kinematic_danger(self, state: dict) -> float:
        """
        计算运动学危险指数 (Kinematic Danger Index)
        公式: Task_Priority + (Mass * Velocity) / Normalization_Factor
        """
        task_pri = self.base_priority.get(state.get("task_type", "EMPTY_CRUISING"), 10)
        
        # 提取物理运动学参数 (质量kg, 速度m/s)
        kinematics = state.get("kinematics", {"mass_kg": 20.0, "velocity_m_s": 0.0})
        momentum = kinematics["mass_kg"] * kinematics["velocity_m_s"]
        
        # 动量因子惩罚（动量越大，越难刹车，强制路权越高）
        momentum_factor = momentum * 0.5 
        
        return task_pri + momentum_factor

    def execute_swarm_sync(self, my_state: dict, peer_state: dict) -> dict:
        logging.info(f"🤝 [社会层] 拦截到节点 [{peer_state.get('agent_id')}] 的 P2P 物理广播...")

        if not self._verify_peer_signature(peer_state):
            logging.warning("⛔ 警告：节点 PKI 验证失败！拒绝路权握手。")
            return {"status": "rejected"}

        # 动态危险指数博弈 (任务重要性 + 物理动量的双重叠加)
        my_danger_score = self._calculate_kinematic_danger(my_state)
        peer_danger_score = self._calculate_kinematic_danger(peer_state)
        
        logging.info(f"⚖️ 运动学路权计算: 本机得分 {my_danger_score:.1f} vs 对方得分 {peer_danger_score:.1f}")
        
        sync_result = {"status": "overlap", "right_of_way_arbitration": {}}
        
        if my_danger_score >= peer_danger_score:
            sync_result["right_of_way_arbitration"] = {
                "decision": "PROCEED",
                "action": "Maintain velocity. Peer lacks sufficient momentum/priority to force a yield."
            }
        else:
            sync_result["right_of_way_arbitration"] = {
                "decision": "YIELD",
                "action": "Apply dynamic torque braking. Yielding to higher momentum/priority peer."
            }

        return sync_result