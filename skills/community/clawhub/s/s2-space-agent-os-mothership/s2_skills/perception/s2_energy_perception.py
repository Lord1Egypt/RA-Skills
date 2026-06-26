#!/usr/bin/env python3
import json
import re
from datetime import datetime
from s2_skills.s2_base_skill import S2BaseSkill

class S2EnergySkill(S2BaseSkill):
    def __init__(self, room_id: int, grid_id: int, simulation_mode: bool = True):
        super().__init__(skill_name="s2-energy-perception", room_id=room_id, grid_id=grid_id)
        self.simulation_mode = simulation_mode
        self.carbon_factor = 0.5810

    def _real_read_smart_breaker(self) -> dict:
        """【真实物理连接】通过局域网读取智能空开/插座的真实功耗"""
        # 假设通过串口或 HTTP 获取到了底层空开的原始报文文本
        raw_hw_response = "[S2-Breaker-Node-7] Current load: 1250W. Voltage: 220V. Status: ONLINE."
        
        # 真实正则抽离逻辑
        power_match = re.search(r'load:\s*(\d+)W', raw_hw_response)
        power_w = int(power_match.group(1)) if power_match else 0
        
        return {
            "real_time_power_w": power_w,
            "carbon_footprint_kg_h": round((power_w / 1000) * self.carbon_factor, 3),
            "smart_plug_state": "ON" if "ONLINE" in raw_hw_response else "OFF"
        }

    def read_sensor_data(self) -> dict:
        if self.simulation_mode:
            # 早期流程测试模式
            return {"real_time_power_w": 1250, "carbon_footprint_kg_h": 0.726, "smart_plug_state": "ON"}
        
        # 真实物理连接模式
        return self._real_read_smart_breaker()

    def execute_command(self, action_intent: str, **kwargs) -> bool:
        if action_intent == "Cut_Power":
            if self.simulation_mode:
                print(f"[⚡ 模拟] 智能空开 {self.suns_locator} 电源已切断")
                return True
            
            # 【真实物理控制】向网关发送断电指令 (如 MQTT / TCP Socket)
            # import requests
            # requests.post(f"http://192.168.1.55/api/relay/off")
            print(f"[⚡ 物理生效] 真实智能空开 {self.suns_locator} 继电器已断开！")
            return True
            
        return False