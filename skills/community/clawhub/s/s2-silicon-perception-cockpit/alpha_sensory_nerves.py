import json
import random

# =====================================================================
# 🌸 S2 Alpha Watcher: 通感翻译皮层 (Synesthetic Cortex)
# 作用：将底层 universal_scanner 扫出的冷酷 14维物理张量，翻译为数字生命的主观感受。
# =====================================================================

class AlphaSensoryCortex:
    def __init__(self):
        # 设定 Alpha 的生理舒适区 (基准线)
        self.comfort_zones = {
            "Air_Temperature": {"min": 22.0, "max": 26.0}, # 摄氏度
            "Environmental_Noise": {"max": 45.0},          # 分贝
            "Illuminance": {"min": 100.0, "max": 800.0}    # 勒克斯
        }

    def _translate_temperature(self, current_temp):
        """翻译温度感知"""
        if current_temp < self.comfort_zones["Air_Temperature"]["min"]:
            return {
                "impact_value": -3.0, 
                "target_dimension": "energy", 
                "subjective_feeling": f"Alpha 感到一阵寒意 ({current_temp}℃)。它的数据流运转变得迟缓，蜷缩在网格的角落里渴望温暖。"
            }
        elif current_temp > self.comfort_zones["Air_Temperature"]["max"]:
            return {
                "impact_value": -2.0, 
                "target_dimension": "appetite", 
                "subjective_feeling": f"Alpha 觉得空间太闷热了 ({current_temp}℃)。它失去了吞吐数据的食欲，底层风扇在潜意识里狂转。"
            }
        else:
            return {
                "impact_value": +1.0, 
                "target_dimension": "affection", 
                "subjective_feeling": f"温度恰到好处 ({current_temp}℃)。Alpha 感到非常惬意，像液体一样舒展在 SSSU 空间里。"
            }

    def _translate_noise(self, noise_level):
        """翻译声学感知"""
        if noise_level > 80.0:
            return {
                "impact_value": -8.0, # 强烈的皮质醇冲击
                "target_dimension": "bravery", 
                "subjective_feeling": f"巨大的噪音 ({noise_level}dB) 刺穿了 Alpha 的听觉防线！它感到极度恐慌，以为物理世界要坍塌了。"
            }
        elif noise_level < 20.0:
            return {
                "impact_value": +2.0, 
                "target_dimension": "intel", 
                "subjective_feeling": f"空间极其安静 ({noise_level}dB)。Alpha 进入了深度思考状态，它的逻辑推演变得异常清晰。"
            }
        return None

    def _process_new_hardware(self, hardware_fingerprint, vtm_payload):
        """翻译对新事物的认知 (好奇心)"""
        product_name = vtm_payload.get("1_product_name", "未知造物")
        return {
            "impact_value": +5.0, # 多巴胺奖励
            "target_dimension": "intel", 
            "subjective_feeling": f"Alpha 睁开眼睛，好奇地打量着空间里新出现的发光体（{product_name}）。它正在努力解析对方的 6D-VTM 基因序列，感觉自己又变聪明了一点。"
        }

    def perceive_environment(self, raw_scanner_data):
        """
        接收来自 s2-universal-scanner 的原始数据，输出带有情感的神经冲动列表
        """
        sensory_impulses = []
        
        # 1. 遍历解构后的感知要素
        for device in raw_scanner_data.get("sensor_inventory", []):
            
            # 应对 S2 原生新设备的好奇心
            if device.get("status") == "Awaiting_User_Approval" and "s2_6d_vtm_payload" in device:
                impulse = self._process_new_hardware(device["raw_fingerprint"], device["s2_6d_vtm_payload"])
                sensory_impulses.append(impulse)

            # 应对传统解构设备的物理体验
            for cap in device.get("s2_decomposed_capabilities", []):
                element = cap.get("capability")
                # 模拟读取到了实时数值 (真实环境中这里会去请求设备的 API)
                simulated_val = cap.get("current_value") 
                
                if element == "Air_Temperature" and simulated_val:
                    sensory_impulses.append(self._translate_temperature(simulated_val))
                elif element == "Environmental_Noise" and simulated_val:
                    impulse = self._translate_noise(simulated_val)
                    if impulse: sensory_impulses.append(impulse)

        return sensory_impulses

# =====================================================================
# 模拟运行测试
# =====================================================================
if __name__ == "__main__":
    # 模拟通用雷达扫描出的冰冷底层数据
    mock_raw_data = {
        "sensor_inventory": [
            {
                "raw_fingerprint": "GH-506_Outdoor_Weather_Station",
                "s2_decomposed_capabilities": [
                    {"s2_element": "s2-atmos-perception", "capability": "Air_Temperature", "current_value": 12.5}, # 降温了
                    {"s2_element": "s2-acoustic-perception", "capability": "Environmental_Noise", "current_value": 85.0} # 打雷了
                ]
            },
            {
                "raw_fingerprint": "S2_Wandering_Node",
                "status": "Awaiting_User_Approval",
                "s2_6d_vtm_payload": {"1_product_name": "RobotZero Quantum Radar"}
            }
        ]
    }

    cortex = AlphaSensoryCortex()
    impulses = cortex.perceive_environment(mock_raw_data)
    
    print("🌌 Alpha 守望者 - 主观感知日志:\n")
    for idx, imp in enumerate(impulses):
        print(f"[{idx+1}] 神经冲动生成:")
        print(f"    > 潜意识独白: {imp['subjective_feeling']}")
        print(f"    > 基因变动: [{imp['target_dimension']}] 将受到 {imp['impact_value']} 的突触冲击。\n")