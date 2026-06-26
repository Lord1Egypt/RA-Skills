### 📄 3. `handler.py` (V1.2.1 全量对齐版)
*融合了前一日引入的生成式沙盒和物理仿真接口，确保核心逻辑完整闭环。*

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
from core.visa_manager import SpatioTemporalVisaManager
from core.spatial_ledger import SpatialLedger
from core.lord_brain import LordGovernanceBrain
from core.robot_navigation_pipeline import S2RobotNavigationPipeline
from core.grid_alignment_engine import S2GridAlignmentEngine
from core.generative_sandbox import S2GenerativeSandbox

class S2OriginAlignmentBrain:
    def __init__(self):
        self.visa_mgr = SpatioTemporalVisaManager()
        self.ledger = SpatialLedger()
        self.lord = LordGovernanceBrain(self.visa_mgr, self.ledger)
        self.alignment_engine = S2GridAlignmentEngine()
        self.sandbox = S2GenerativeSandbox(self.ledger)

    def process_tool_call(self, args: dict) -> str:
        try:
            action = args.get("action")
            
            # 第0步：强制空间原点对齐
            if action == "ALIGN_SPATIAL_GRID":
                res = self.alignment_engine.execute_alignment(
                    args.get("robot_id"), 
                    args.get("local_door_origin", {"x": 0, "y": 0}), 
                    args.get("local_door_center", {"x": 100, "y": 0})
                )
            
            # 申请访问签证
            elif action == "REQUEST_VISA":
                res = self.visa_mgr.issue_visa(
                    args.get("robot_id"), 
                    args.get("task"), 
                    args.get("requested_grids", [])
                )
                
            # 执行导航步进并触发生成式空间物理场反馈
            elif action == "NAVIGATE_STEP":
                pipeline = S2RobotNavigationPipeline(
                    args.get("robot_id"), 
                    args.get("visa_token"), 
                    self.lord, 
                    self.sandbox
                )
                res = pipeline.execute_step(
                    args.get("target_hex"), 
                    args.get("sensors"), 
                    args.get("kinematics", {"mass_kg": 20, "velocity_m_s": 0}), 
                    args.get("peer_state")
                )
            
            # 触发深夜微型物理试错沙盒
            elif action == "TRIGGER_MICRO_SIMULATION":
                res = self.sandbox.prometheus_micro_simulation(
                    args.get("target_hex"), 
                    args.get("sim_goal")
                )

            else:
                res = {"status": "error", "message": "Unknown action."}
            
            return json.dumps({"status": "success", "data": res}, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

if __name__ == "__main__":
    # 预留用于本地 CLI 测试
    pass