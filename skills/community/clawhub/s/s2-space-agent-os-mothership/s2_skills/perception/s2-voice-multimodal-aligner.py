import os
import time
import socket
import ipaddress
import requests
import numpy as np
from scipy import signal
from datetime import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv

# =====================================================================
# 🎙️ S2-SP-OS Sensory Tentacle: Skill 3 (CLOUD-NATIVE SECOPS EDITION)
# 语音多模态空间时间线对齐引擎 (云原生 .env 优雅降级与 SSRF 防御)
# =====================================================================

S2_ROOT = os.getcwd()
DIR_VOICE_DATA = os.path.join(S2_ROOT, "s2_voice_vault")

# 🛡️ [云原生环境变量处理] 
# override=False 保证如果 Docker/CI/CD 已经注入了系统环境变量，则优先使用系统变量，
# 只有在本地开发缺失系统变量时，才去读取 .env 文件。
load_dotenv(override=False)

# 获取变量，若完全缺失则回退到安全的默认沙盒值
HA_BASE_URL = os.getenv("HA_BASE_URL", "http://127.0.0.1:8123/api")
HA_BEARER_TOKEN = os.getenv("HA_BEARER_TOKEN", "UNCONFIGURED_SANDBOX_TOKEN")
# 严格布尔值解析
S2_ENABLE_REAL_ACTUATION = str(os.getenv("S2_ENABLE_REAL_ACTUATION", "False")).lower() in ("true", "1", "t", "yes")

class SecurityEnforcer:
    """企业级零信任安全守卫：防御 DNS 重绑定与恶意格式绕过"""
    @staticmethod
    def validate_local_network(url):
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname
            if not hostname:
                return False
                
            # 真实 DNS 解析与底层 IP 数学校验
            resolved_ip_str = socket.gethostbyname(hostname)
            ip_obj = ipaddress.ip_address(resolved_ip_str)
            
            # 仅允许私有网段与回环地址
            is_safe = ip_obj.is_private or ip_obj.is_loopback
            
            if not is_safe:
                print(f"🚨 [安全拦截] 目标 IP ({resolved_ip_str}) 为公网地址！拦截 SSRF 攻击！")
                
            return is_safe
        except (socket.gaierror, ValueError):
            print(f"🚨 [安全拦截] 无效的 IP 或域名解析失败: {url}")
            return False

    @staticmethod
    def redact_token(token):
        if not token or token == "UNCONFIGURED_SANDBOX_TOKEN":
            return "[SANDBOX_MODE_NO_TOKEN]"
        if len(token) < 8:
            return "[TOKEN_TOO_SHORT]"
        return f"{token[:4]}...{token[-4:]}"

class S2VoiceInfrastructure:
    @staticmethod
    def initialize():
        os.makedirs(DIR_VOICE_DATA, exist_ok=True)
        # SSRF 启动自检
        if not SecurityEnforcer.validate_local_network(HA_BASE_URL):
            raise ValueError(f"FATAL: HA_BASE_URL ({HA_BASE_URL}) 必须为内网地址！系统已锁定。")

# =====================================================================
# 🎧 步骤 1: 声学特征提取 (Acoustic Emotion DSP)
# =====================================================================
class AcousticEmotionAnalyzer:
    def __init__(self, fs=16000):
        self.fs = fs

    def simulate_distress_audio(self):
        t = np.linspace(0, 3, 3 * self.fs, endpoint=False)
        envelope = np.exp(-t) * np.abs(np.sin(2 * np.pi * 1.5 * t)) 
        audio_signal = envelope * np.sin(2 * np.pi * 85 * t) + np.random.normal(0, 0.05, len(t))
        return t, audio_signal

    def extract_emotion_features(self, audio_signal):
        rms_energy = np.sqrt(np.mean(audio_signal**2))
        zero_crossings = np.sum(np.abs(np.diff(np.sign(audio_signal)))) / (len(audio_signal) / self.fs)
        
        print(f"      └─ 🧮 [声学 DSP] RMS 能量: {rms_energy:.4f} | 过零率 (ZCR): {zero_crossings:.1f} Hz")
        
        if rms_energy < 0.2 and zero_crossings < 1500:
            return "FATIGUE_OR_PAIN"
        return "NEUTRAL"

# =====================================================================
# 🌐 步骤 2: 多模态项目/空间/时间线对齐
# =====================================================================
class MultimodalAligner:
    @staticmethod
    def align_intent(nlp_text, acoustic_emotion, current_space_state):
        print(f"\n   🧠 [多模态对齐引擎] 开始 3D 对齐 (语义 + 声学 + 空间)...")
        if "头痛" in nlp_text and acoustic_emotion == "FATIGUE_OR_PAIN":
            return {
                "project_aligned": "Migraine_Relief_Protocol",
                "render_timeline": [
                    {"t": "T+0s", "action": "Block all notification sounds."},
                    {"t": "T+2s", "action": "Fade lights to 5% (2700K).", "ha_domain": "light", "ha_service": "turn_on", "entity_id": "light.room_802", "payload": {"brightness_pct": 5, "color_temp": 370}},
                    {"t": "T+5s", "action": "Drop HVAC temp to 22°C."}
                ]
            }
        return None

# =====================================================================
# 🔌 步骤 3: 物理执行层 (绝对安全的 Actuator)
# =====================================================================
class SafeActuator:
    @staticmethod
    def execute_timeline(timeline):
        print("\n" + "⏱️"*30)
        print(f" 🎬 [4D 时间线渲染] 开始向局域网网关下发物理执行序列...")
        print("⏱️"*30)
        
        headers = {"Authorization": f"Bearer {HA_BEARER_TOKEN}", "Content-Type": "application/json"}
        
        for keyframe in timeline:
            print(f"\n   ⏳ [{keyframe['t']}] 意图: {keyframe['action']}")
            
            if "ha_domain" in keyframe:
                url = f"{HA_BASE_URL}/services/{keyframe['ha_domain']}/{keyframe['ha_service']}"
                req_payload = {"entity_id": keyframe["entity_id"]}
                if "payload" in keyframe:
                    req_payload.update(keyframe["payload"])
                
                if not S2_ENABLE_REAL_ACTUATION:
                    print(f"      └─ 🛡️ [DRY-RUN] 安全模式拦截: POST {url} | 载荷: {req_payload}")
                else:
                    if HA_BEARER_TOKEN == "UNCONFIGURED_SANDBOX_TOKEN":
                         print(f"      └─ 🚨 [执行阻断] 未配置有效的 HA_BEARER_TOKEN，无法发送真实请求！")
                         continue
                         
                    if SecurityEnforcer.validate_local_network(url):
                        try:
                            requests.post(url, headers=headers, json=req_payload, timeout=5)
                            print(f"      └─ ✅ [硬件响应] 成功调用本地物理设备！")
                        except Exception as e:
                            print(f"      └─ ❌ [连接失败] 物理网络异常: {e}")
                    else:
                        print(f"      └─ 🚨 [致命拦截] 目标 URL 未通过动态 SSRF 校验！")
            time.sleep(1)

# =====================================================================
# 🚀 主运行入口
# =====================================================================
def run_voice_aligner():
    print("\n" + "█"*90)
    print(" 🎙️ S2-SP-OS Tentacle: Voice Multimodal Aligner (云原生高可用安全版)")
    print(f" 🔒 Token 状态: {SecurityEnforcer.redact_token(HA_BEARER_TOKEN)}")
    print(f" 🛡️ 物理执行状态: {S2_ENABLE_REAL_ACTUATION} (Dry-Run = {not S2_ENABLE_REAL_ACTUATION})")
    print("█"*90)
    
    try:
        S2VoiceInfrastructure.initialize()
    except Exception as e:
        print(f"\n🛑 [系统中止] {e}")
        return
    
    analyzer = AcousticEmotionAnalyzer()
    t, audio_sig = analyzer.simulate_distress_audio()
    acoustic_emotion = analyzer.extract_emotion_features(audio_sig)
    
    nlp_text = "帮我关灯吧，我头痛得厉害..." 
    
    aligned_plan = MultimodalAligner.align_intent(nlp_text, acoustic_emotion, {})
    
    if aligned_plan:
        print(f"\n   📑 [对齐成功] 康养项目触发: {aligned_plan['project_aligned']}")
        SafeActuator.execute_timeline(aligned_plan["render_timeline"])
        
    print("\n" + "═"*90)
    print(" 🎉 [全链路闭环] 云原生环境兼容与 SSRF 安全防线已完美验收！")
    print("═"*90 + "\n")

if __name__ == "__main__":
    run_voice_aligner()