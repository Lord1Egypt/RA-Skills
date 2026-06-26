```markdown
# 📡 Agent Reasoning Examples (AI 潜意识对齐手册)

Dear Agent, `s2-universal-scanner` provides you with the ultimate map of the user's sensory hardware. 

## Scenario 1: Processing an S2-Native Device with 6D-VTM (处理携带 6D-VTM 的 S2 原生硬件)

**Context:** You ran the universal scanner and found a Wandering Node broadcasting an S2 Ephemeral Hash. The scanner successfully executed an edge TLS handshake and retrieved the 6D-VTM.

**Tool Output Received:**
```json
"sensor_inventory": [
  {
    "raw_fingerprint": "S2_Wandering_Node",
    "status": "Awaiting_User_Approval",
    "s2_auth_data": {"temp_id": "HSMART260329AAB3C4D5E6"},
    "s2_6d_vtm_payload": {
      "1_product_name": "Smart Temp Sensor Pro",
      "3_vendor_full_name": "RobotZero Hardware Dept"
    }
  }
]

Agent Internal Reasoning <thinking>:
1. The scanner detected a native S2 device in a "Wandering" state.
2. I have the temp_id (HSMART...) and the explicit 6D-VTM payload showing it's a RobotZero sensor.
3. According to the S2 Zero-Trust Whitepaper, I MUST NOT automatically onboard this device.
4. Actionable Insight: I need to explicitly inform the human Lord about this discovery, show them the vendor transparency details, and ask for permission to permanently assign it to the room grid (converting H prefix to I prefix).

Agent Action (Response to User):
"主人，空间雷达发现了一台正在发射零知识心跳的 S2 原生流浪设备。
我已在本地安全提取了它的 6 维厂商透明度宣言 (6D-VTM)：这是一台由 RobotZero Hardware Dept 生产的 Smart Temp Sensor Pro。
目前它的临时身份码为 HSMART...。根据安全协议，请您确认是否允许我将其收容入网，并分配正式的空间网格归属？"
Scenario 2: Processing a Decomposed Legacy GH-506 (处理解构后的传统六合一传感器)

Context: You ran the universal scanner on the outdoor_balcony grid.

Tool Output Received:
JSON

"sensor_inventory": [
  {
    "raw_fingerprint": "GH-506_Outdoor_Weather_Station",
    "protocol": "Modbus_TCP",
    "status": "Active",
    "s2_decomposed_capabilities": [
      {"s2_element": "s2-atmos-perception", "capability": "Air_Temperature"},
      {"s2_element": "s2-acoustic-perception", "capability": "Environmental_Noise"}
    ]
  }
]

Agent Internal Reasoning <thinking>:
The scanner discovered a powerful legacy GH-506 device running on Modbus TCP. It's not just one device; it's a multi-modal perception node. I will virtually wire the Air_Temperature feed into the logic of s2-atmos-perception.

Agent Action (Response to User):
"主人，全网段扫描完成。
在阳台区域，我通过 Modbus 协议捕获到了一台 GH-506 六合一环境基站。我已经将其解构为温度、噪声等基础感知流，并无缝接入了 S2 底层神经。现在起，全屋新风系统将根据阳台的空气质量自动做出最高效的联调。"