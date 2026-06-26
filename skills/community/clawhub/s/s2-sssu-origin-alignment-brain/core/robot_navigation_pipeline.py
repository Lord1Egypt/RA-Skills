import logging
from plugins.boundary_scanner import S2BoundaryScanner
from plugins.multimodal_fusion import S2MultimodalPredictor
from plugins.swarm_sync import S2SwarmSyncEngine

class S2RobotNavigationPipeline:
    def __init__(self, robot_id, visa_token, lord_api):
        self.robot_id = robot_id
        self.visa_token = visa_token
        self.lord_api = lord_api
        
        self.scanner = S2BoundaryScanner()
        self.fusion = S2MultimodalPredictor()
        self.swarm = S2SwarmSyncEngine()

    def execute_step(self, target_hex: str, sensors: dict, kinematics: dict, peer_state: dict = None):
        logging.info(f"\n🚀 [ROBOT {self.robot_id}] 发起向 SSSU 节点 {target_hex} 的张量级步进决策...")

        # 1. 动态边界扫描 (直接传入极坐标点云流进行解析)
        scan_res = self.scanner.execute_boundary_scan(target_hex, "North", 500)
        front_grid_state = scan_res.get("peripheral_grids_state", {}).get("Grid_Front", {})
        
        if front_grid_state.get("intrusion_percentage", 0.0) > 80.0:
            logging.warning(f"⚠️ 扫描器：物理边界侵入度高达 {front_grid_state['intrusion_percentage']}%！")

        # 2. 多模态融合去幻觉 (NumPy 矩阵潜空间交叉验证)
        fusion_res = self.fusion.generate_causal_prediction(sensors)
        metrics = fusion_res.get("fusion_metrics", {})
        
        if metrics.get("illusion_detected"):
            logging.warning("🛑 融合引擎：检测到严重物理幻觉 (如透明刚体玻璃)！")
            # 【TDOG 触发】将隐形玻璃转化为空间动态对象，写入不可篡改账本，防止后车追尾
            self.lord_api.ledger.log_event(
                target_hex, self.robot_id, "DYNAMIC_OBJECT_GENERATION", 
                {"type": "Invisible_Rigid_Obstacle", "coords": target_hex, "confidence": 0.98}
            )
            return {"status": "HALTED_BY_PHYSICS_ILLUSION", "metrics": metrics}
            
        if metrics.get("front_collision_probability", 0.0) > 0.85:
            return {"status": "HALTED_BY_HIGH_COLLISION_PROBABILITY"}

        # 3. 运动学路权博弈 (动量计算)
        if peer_state:
            my_state = {
                "agent_id": self.robot_id, "center_hex": target_hex, 
                "task_type": "EMPTY_CRUISING", "kinematics": kinematics
            }
            swarm_res = self.swarm.execute_swarm_sync(my_state, peer_state)
            if swarm_res.get("status") != "rejected":
                decision = swarm_res.get("right_of_way_arbitration", {}).get("decision")
                if decision == "YIELD":
                    logging.warning(f"⚔️ 群体引擎：动量博弈失败！对方享有路权，立即输出逆向扭矩制动！")
                    return {"status": "HALTED_BY_KINEMATIC_YIELD"}

        # 4. 领主主权协商
        if sensors.get("camera", {}).get("illuminance_lux", 0) < 10:
            logging.info("💬 导航申请：环境照度极低，向空间领主发起要素协商...")
            nego_res = self.lord_api.negotiate_environment(self.visa_token, self.robot_id, "illuminance", 300, target_hex)
            if nego_res["status"] == "DENIED_WITH_ALTERNATIVE":
                logging.info(f"🛡️ 领主回复：请求被拒 ({nego_res['reason']})。执行补偿盲导协议。")

        logging.info(f"✅ 张量闭环验证通过。物理步进至 {target_hex} 确认。")
        self.lord_api.ledger.log_event(target_hex, self.robot_id, "PHYSICAL_STEP_COMPLETE", {"hex": target_hex, "momentum": kinematics.get("mass_kg", 0) * kinematics.get("velocity_m_s", 0)})
        return {"status": "STEP_SUCCESS"}

        # 修改点：在执行完第4步的领主协商后，引入生成式物理场计算
import logging
from plugins.boundary_scanner import S2BoundaryScanner
from plugins.multimodal_fusion import S2MultimodalPredictor
from plugins.swarm_sync import S2SwarmSyncEngine

class S2RobotNavigationPipeline:
    def __init__(self, robot_id, visa_token, lord_api, generative_sandbox): # [新增入参]
        self.robot_id = robot_id
        self.visa_token = visa_token
        self.lord_api = lord_api
        self.sandbox = generative_sandbox # [注入 Flipbook/Prometheus 引擎]
        
        self.scanner = S2BoundaryScanner()
        self.fusion = S2MultimodalPredictor()
        self.swarm = S2SwarmSyncEngine()

    def execute_step(self, target_hex: str, sensors: dict, kinematics: dict, peer_state: dict = None):
        logging.info(f"\n🚀 [ROBOT {self.robot_id}] 发起向 SSSU 节点 {target_hex} 的张量级步进决策...")

        # ... (前4步原有逻辑保持不变：边界扫描、多模态融合、路权博弈、领主协商) ...

        # 5. 【新增】生成式物理场渲染 (The Flipbook Paradigm)
        # 机器人成功步进，触发空间场重构
        new_spatial_state = self.sandbox.generate_spatial_state(
            sssu_id=target_hex, 
            actor_id=self.robot_id, 
            action="PHYSICAL_STEP_INTRUSION", 
            kinematics=kinematics
        )

        logging.info(f"✅ 张量闭环验证通过。物理步进完成。")
        logging.info(f"🌍 当前空间因你的介入，实时生成新物理状态: 声场 {new_spatial_state['acoustic_db']:.1f}dB")
        
        self.lord_api.ledger.log_event(target_hex, self.robot_id, "PHYSICAL_STEP_COMPLETE", {"hex": target_hex})
        return {"status": "STEP_SUCCESS", "generated_state": new_spatial_state}