import os
import time
import requests
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from datetime import datetime

# =====================================================================
# 🧓 S2-SP-OS Sensory Tentacle: Skill 2 (SECURE ACTUATION EDITION)
# 老年姿态监测预警引擎 (带 Dry-Run 安全保险栓的物理执行版)
# =====================================================================

S2_ROOT = os.getcwd()
DIR_ELDERCARE_DATA = os.path.join(S2_ROOT, "s2_eldercare_vault")

# --- 显式声明的环境变量 (Environment Variables) ---
HA_BASE_URL = os.getenv("HA_BASE_URL", "http://homeassistant.local:8123/api")
HA_BEARER_TOKEN = os.getenv("HA_BEARER_TOKEN", "YOUR_LONG_LIVED_ACCESS_TOKEN")
# 核心安全阀：默认 False (Dry-Run)，必须显式设置为 True 才能控制真实物理设备
S2_ENABLE_REAL_ACTUATION = os.getenv("S2_ENABLE_REAL_ACTUATION", "False").lower() in ("true", "1", "t")

class S2EldercareInfrastructure:
    @staticmethod
    def initialize():
        os.makedirs(DIR_ELDERCARE_DATA, exist_ok=True)

# =====================================================================
# 📡 步骤 1 & 2: 信号合成与 STFT 时频分析 (保持纯粹的数学计算)
# =====================================================================
class EldercareRadarDSP:
    def __init__(self, fs=1000, duration=10):
        self.fs = fs
        self.duration = duration
        self.t = np.linspace(0, self.duration, self.fs * self.duration, endpoint=False)

    def process_pipeline(self):
        # 1. 合成跌倒微多普勒信号
        freq_modulation = np.zeros_like(self.t)
        freq_modulation[0:3000] = 15.0 + np.random.normal(0, 2, 3000)
        fall_profile = np.linspace(15, -150, 1000) 
        freq_modulation[3000:4000] = fall_profile + np.random.normal(0, 5, 1000)
        freq_modulation[4000:] = np.random.normal(0, 1, 6000) 
        phase = 2 * np.pi * np.cumsum(freq_modulation) / self.fs
        sig_raw = np.cos(phase) + np.random.normal(0, 0.5, len(self.t))

        # 2. STFT 短时傅里叶变换
        f, t_stft, Zxx = signal.stft(sig_raw, fs=self.fs, window='hann', nperseg=256, noverlap=128)
        power = np.abs(Zxx)
        
        # 3. 跌倒判定 (寻找高能量负向频移)
        max_negative_doppler = np.max(power[f < -50]) 
        is_fall_detected = max_negative_doppler > 10.0 
        
        return self.t, sig_raw, f, t_stft, power, is_fall_detected

# =====================================================================
# 🔌 步骤 3: 物理执行层 (带安全拦截器的 Actuator)
# =====================================================================
class HomeAssistantActuator:
    headers = {
        "Authorization": f"Bearer {HA_BEARER_TOKEN}",
        "Content-Type": "application/json",
    }

    @staticmethod
    def call_service(domain, service, entity_id, service_data=None):
        url = f"{HA_BASE_URL}/services/{domain}/{service}"
        payload = {"entity_id": entity_id}
        if service_data:
            payload.update(service_data)
            
        # 安全保险栓逻辑 (Dry-Run 拦截)
        if not S2_ENABLE_REAL_ACTUATION:
            print(f"      └─ 🛡️ [DRY-RUN 安全模式] 拦截物理指令: 模拟 POST {url} | 载荷: {payload}")
            return True
            
        # 真实物理控制逻辑
        print(f"      └─ 🔌 [物理执行层] 正在发送危险指令 POST {url} | 载荷: {payload}")
        try:
            response = requests.post(url, headers=HomeAssistantActuator.headers, json=payload, timeout=5)
            response.raise_for_status()
            print(f"      └─ ✅ [硬件响应] 成功执行真实物理指令！")
            return True
        except requests.exceptions.RequestException as e:
            print(f"      └─ ❌ [连接失败] 物理网络异常: {e}")
            return False

# =====================================================================
# 🚨 步骤 4: 紧急事件闭环路由
# =====================================================================
class S2EldercareRouter:
    @staticmethod
    def dispatch_emergency(event_type):
        if event_type == "FALL_DETECTED":
            print(f"\n" + "🚨"*40)
            print(f" 👑 [Avatar Commander] 诊断为【严重跌倒】。启动智能家居跨界急救...")
            print("🚨"*40)
            
            print(f"\n   🤖 [Agent:Sentinel] 指令：解锁门禁")
            HomeAssistantActuator.call_service("lock", "unlock", "lock.room_802_main_door")
            
            print(f"\n   🤖 [Agent:Lumina] 指令：开启 100% 抢救照明")
            HomeAssistantActuator.call_service("light", "turn_on", "light.room_802_all", {"brightness_pct": 100, "color_temp": 200})
            
            print(f"\n   🤖 [Agent:Climate] 指令：新风系统最大功率")
            HomeAssistantActuator.call_service("fan", "set_percentage", "fan.room_802_hvac", {"percentage": 100})

# =====================================================================
# 🚀 主运行入口
# =====================================================================
def run_eldercare_monitor():
    print("\n" + "█"*90)
    print(" 🧓 S2-SP-OS Tentacle: Eldercare mmWave Monitor (安全执行版)")
    print(f" 🛡️ 当前物理执行状态 (S2_ENABLE_REAL_ACTUATION): {S2_ENABLE_REAL_ACTUATION}")
    print("█"*90)
    
    S2EldercareInfrastructure.initialize()
    
    print("\n   📡 1. 运行雷达 DSP 管线 (生成微多普勒与 STFT 时频张量)...")
    dsp = EldercareRadarDSP()
    t_raw, sig_raw, f, t_stft, power, is_fall = dsp.process_pipeline()
    
    if is_fall:
        S2EldercareRouter.dispatch_emergency("FALL_DETECTED")
        
    print("\n" + "═"*90)
    print(" 🎉 [运行完毕] 算法判定与路由闭环完成。")
    if not S2_ENABLE_REAL_ACTUATION:
        print(" 💡 提示：当前处于安全模式 (Dry-Run)，物理设备未发生实际动作。")
    print("═"*90 + "\n")

if __name__ == "__main__":
    run_eldercare_monitor()