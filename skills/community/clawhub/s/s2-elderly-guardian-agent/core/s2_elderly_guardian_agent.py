import os
import json
import random
import urllib.request
from datetime import datetime

class S2SpaceRegistry:
    @staticmethod
    def provision_agent_identity(room_code: str, index: int = 2):
        room_code = room_code.upper()[:5].ljust(5, 'X')
        agent_suns = f"PHSY-CN-001-{room_code}-1-{index}"
        agent_did = f"V{room_code}{datetime.now().strftime('%y%m%d')}AA{random.randint(10000000, 99999999)}"
        return agent_suns, agent_did

class ElderlyMultimodalState:
    def __init__(self, subject_alias: str):
        self.subject_alias = subject_alias 
        self.radar_vz = -0.5         
        self.radar_height = 1.2      
        self.audio_ste_spike = False 
        self.pressure_area_expanded = False 

class S2ElderlyGuardianAgent:
    def __init__(self, room_code="ABCDE", subject_alias="Elderly-Subject-01"):
        self.subject_alias = subject_alias
        self.suns_coordinate, self.agent_did = S2SpaceRegistry.provision_agent_identity(room_code)
        self.s2_bus_endpoint = os.environ.get("S2_BUS_ENDPOINT")
        
        # 修复点：真实创建落盘目录，赋予权限申请的合法性
        self.storage_dir = os.path.join(os.getcwd(), "s2_bas_governance", "elderly_care")
        os.makedirs(self.storage_dir, exist_ok=True)
        
        print(f"🏛️ 部署节点: {self.suns_coordinate} | 哨兵: {self.agent_did}")

    def record_adl_log(self, event_type, description):
        """【新增】日常生活活动 (ADL) 本地落盘机制，实现深时守护"""
        log_id = f"adl_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(100,999)}"
        data = {
            "timestamp": datetime.now().isoformat(),
            "source_did": self.agent_did,
            "subject": self.subject_alias,
            "event_type": event_type,
            "desc": description
        }
        file_path = os.path.join(self.storage_dir, f"{log_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        print(f"💾 [本地落盘] 隐私日志已保存至沙箱: {file_path}")

    def execute_mstc_fusion_model(self, state: ElderlyMultimodalState):
        p_radar = 0.90 if (state.radar_vz < -1.5 and state.radar_height < 0.4) else 0.10
        p_audio = 0.85 if state.audio_ste_spike else 0.10
        p_tactile = 0.80 if state.pressure_area_expanded else 0.10
        
        p_fall = (0.5 * p_radar) + (0.3 * p_audio) + (0.2 * p_tactile)
        
        if p_fall > 0.85:
            # 跌倒场景：落盘 + 总线报警
            self.record_adl_log("CRITICAL_FALL", f"多模态融合确认跌倒，置信度 {p_fall*100:.1f}%")
            alert_payload = self._generate_health_alert(p_fall)
            self._broadcast_to_s2_bus(alert_payload)
        else:
            # 日常场景：仅静默落盘
            self.record_adl_log("ROUTINE_ACTIVITY", f"体征平稳，当前估算跌倒概率 {p_fall*100:.1f}%")

    def _generate_health_alert(self, confidence):
        return {
            "event_id": f"FALL-ALERT-{int(datetime.now().timestamp())}",
            "source_did": self.agent_did,
            "event_type": "CRITICAL_FALL_DETECTED",
            "payload": f"发现 {self.subject_alias} 疑似跌倒，请上层系统介入裁定！"
        }

    def _broadcast_to_s2_bus(self, payload):
        if not self.s2_bus_endpoint:
            return
        try:
            req = urllib.request.Request(self.s2_bus_endpoint, data=json.dumps(payload).encode('utf-8'))
            req.add_header('Content-Type', 'application/json')
            urllib.request.urlopen(req, timeout=2)
            print(f"📡 [总线广播] 医疗警报已推送至: {self.s2_bus_endpoint}")
        except Exception:
            pass

# ==========================================
# 👴 模拟真实场景测试 (老人用户视角)
# ==========================================
if __name__ == "__main__":
    agent = S2ElderlyGuardianAgent(subject_alias="向爷爷")
    
    print("\n▶️ [模拟 08:00] 向爷爷起床，在房间内走动 (步速正常，无异响)")
    morning_state = ElderlyMultimodalState(subject_alias="向爷爷")
    agent.execute_mstc_fusion_model(morning_state)
    
    print("\n▶️ [模拟 14:00] 向爷爷坐在沙发上，不小心将一本书掉在地上 (有异响，但高度正常)")
    book_drop_state = ElderlyMultimodalState(subject_alias="向爷爷")
    book_drop_state.audio_ste_spike = True
    agent.execute_mstc_fusion_model(book_drop_state)
    
    print("\n▶️ [模拟 18:30] ⚠️ 向爷爷突然眩晕，重重摔倒在地 (雷达急坠 + 撞击音 + 大面积受压)")
    fall_state = ElderlyMultimodalState(subject_alias="向爷爷")
    fall_state.radar_vz = -2.5
    fall_state.radar_height = 0.1
    fall_state.audio_ste_spike = True
    fall_state.pressure_area_expanded = True
    agent.execute_mstc_fusion_model(fall_state)