#!/usr/bin/env python3
import json
import logging
import requests
from typing import Dict, Any

# =====================================================================
# 🤝 S2-SP-OS: Openclaw Task Bridge (V1.0)
# 脑机接口：将 S2 的高维空间意图，转化为 Openclaw 的 Root 级执行任务
# =====================================================================

class S2OpenclawBridge:
    def __init__(self, endpoint: str = "http://localhost:8080/openclaw/task", token: str = "OC_LOCAL_ROOT_TOKEN"):
        self.logger = logging.getLogger("S2_Openclaw_Bridge")
        self.endpoint = endpoint
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-System-Source": "S2-SP-OS-Kernel"
        }

    def delegate_hardware_action(self, zone: str, grid: str, target_element: str, intent_action: str, params: Dict[str, Any]) -> bool:
        """
        [下行请求]：安排 Openclaw 动硬件的苦活脏活
        S2 不管怎么连 Modbus 或 Wi-Fi，S2 只下达空间命令。
        """
        # 将 S2 的高维空间指令，打包给 Openclaw
        task_payload = {
            "task_priority": "HIGH",
            "spatial_context": {
                "zone": zone,
                "grid": grid
            },
            "hardware_target": target_element, # e.g., "HVAC_System", "Main_Light"
            "action": intent_action,           # e.g., "Set_Temperature"
            "parameters": params               # e.g., {"target_temp": 24}
        }
        
        self.logger.info(f"⚡ [向 Openclaw 派发任务] 目标: {zone}-{grid} | 操作: {intent_action}")
        
        try:
            # 向 Openclaw 提交任务
            response = requests.post(self.endpoint, headers=self.headers, json=task_payload, timeout=5)
            if response.status_code == 200:
                self.logger.info("   └─ ✅ Openclaw Agent 已接单并开始执行物理操作。")
                return True
            else:
                self.logger.error(f"   └─ ❌ Openclaw 拒接任务 (状态码: {response.status_code})")
                return False
        except requests.exceptions.RequestException as e:
            self.logger.critical(f"   └─ 🛑 无法联络 Openclaw Agent: {e}")
            return False

    def request_system_data(self, data_type: str) -> dict:
        """
        [上行索求]：向 Openclaw 索要底层 OS 数据（如防盗网关 MAC、ARP 表）
        S2 不再自己去执行 subprocess，全靠打手兄弟收集。
        """
        self.logger.info(f"📡 [向 Openclaw 索取底层数据] 类型: {data_type}")
        try:
            # 假设 Openclaw 提供了一个信息查询的专用 Endpoint
            response = requests.get(f"{self.endpoint}/info?type={data_type}", headers=self.headers, timeout=3)
            if response.status_code == 200:
                return response.json().get("data", {})
            return {}
        except requests.exceptions.RequestException:
            return {}

# ================= 协同测试 =================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bridge = S2OpenclawBridge()
    
    # 场景 1：S2 决定要降温，安排 Openclaw 去摸空调网关
    print("--- 场景 1: S2 指挥 Openclaw ---")
    bridge.delegate_hardware_action(
        zone="Master_Bedroom", grid="Grid_1", 
        target_element="CLIMATE", intent_action="Set_Temperature", 
        params={"target_temp": 22, "wind": "Auto"}
    )
    
    # 场景 2：S2 防盗自检，向 Openclaw 索要底层 MAC 地址
    print("\n--- 场景 2: S2 索取底层网卡信息 ---")
    mac_info = bridge.request_system_data("arp_gateway_mac")
    print(f"   └─ Openclaw 汇报的数据: {mac_info}")