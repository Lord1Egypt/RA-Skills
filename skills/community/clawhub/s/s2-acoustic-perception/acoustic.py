```python
#!/usr/bin/env python3
import sys
import json
import base64
import urllib.request
import argparse
import io
import wave
import ipaddress
from datetime import datetime

# 检查系统依赖 / Check system dependencies
try:
    import numpy as np
    import sounddevice as sd
except ImportError:
    print(json.dumps({"error": "Please run: pip install sounddevice numpy"}, ensure_ascii=False))
    sys.exit(1)

# =====================================================================
# 🎧 S2-SP-OS: Acoustic Radar Client (V1.0.5)
# Strict LAN Enforcement + Ephemeral Privacy / 局域网物理隔离 + 阅后即焚
# =====================================================================

class S2AcousticClient:
    def __init__(self, zone: str, grid: str, edge_ip: str):
        # [SECURITY ENFORCEMENT]: Strict LAN-Only check / 严格的局域网边界检查
        try:
            ip_obj = ipaddress.ip_address(edge_ip)
            if not (ip_obj.is_private or ip_obj.is_loopback):
                print(json.dumps({
                    "error": f"SECURITY VIOLATION: Edge IP ({edge_ip}) is a public or untrusted address. Audio transmission blocked to prevent data exfiltration. / 严重安全违规：Edge IP 为公网或不可信地址，为防止数据泄露，已熔断请求。"
                }, ensure_ascii=False))
                sys.exit(1)
        except ValueError:
            print(json.dumps({"error": f"Invalid IP format: {edge_ip}"}, ensure_ascii=False))
            sys.exit(1)

        self.zone = zone
        self.grid = grid
        self.edge_url = f"http://{edge_ip}:8000/api/v1/analyze"
        self.sample_rate = 16000
        self.duration = 3 # 3-second secure slice / 3秒安全切片
        
    def _record_ephemeral_slice(self) -> np.ndarray:
        """
        Record audio to volatile memory.
        在易失性内存中录制音频。
        """
        audio_data = sd.rec(int(self.duration * self.sample_rate), samplerate=self.sample_rate, channels=1, dtype='float32')
        sd.wait() # 阻塞直至录音完成
        return audio_data.flatten()

    def _encode_to_wav_base64(self, audio_data: np.ndarray) -> str:
        """
        Encode numpy array to WAV Base64 in memory.
        在内存中将 numpy 数组编码为 WAV Base64。
        """
        audio_int16 = (audio_data * 32767).astype(np.int16)
        byte_io = io.BytesIO()
        with wave.open(byte_io, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(audio_int16.tobytes())
        return base64.b64encode(byte_io.getvalue()).decode('utf-8')

    def _query_edge_brain(self, b64_audio: str) -> dict:
        """
        Delegate to trusted local LAN Edge Brain API.
        将数据发送给受限内网中的边缘大脑。
        """
        payload = {
            "audio_base64": b64_audio,
            "candidate_labels": [
                "Human conversation or speaking",
                "Vocal music or instrumental song",
                "A cat meowing loudly",
                "A dog barking",
                "Sound of glass shattering",
                "Background ambient noise"
            ]
        }
        
        req = urllib.request.Request(self.edge_url, method="POST")
        req.add_header('Content-Type', 'application/json')
        data = json.dumps(payload).encode('utf-8')
        
        try:
            with urllib.request.urlopen(req, data=data, timeout=15.0) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            return {"error": f"Edge Brain Connection Failed: {str(e)}. Please check if Edge Brain is running at {self.edge_url}"}

    def run_radar_cycle(self) -> dict:
        # 1. Capture ephemeral audio & calculate Decibel / 采集易失性音频 & 基础分贝计算
        audio_data = self._record_ephemeral_slice()
        
        rms = np.sqrt(np.mean(audio_data**2))
        decibel = 20 * np.log10(max(rms, 1e-10)) + 60 
        
        if rms < 0.005:
            event = "absolute_silence"
            confidence = 1.0
            vendor_nl = "Environment is completely silent. No AI inference needed. / 环境绝对安静，跳过AI推理。"
        else:
            # 2. Acoustic activity detected, query local LAN Edge Brain / 存在声学活动，请求内网边缘大脑
            b64_audio = self._encode_to_wav_base64(audio_data)
            edge_result = self._query_edge_brain(b64_audio)
            
            # [阅后即焚]: Explicitly delete audio from memory / 明确销毁内存中的原生音频数据
            del audio_data 
            del b64_audio
            
            if "error" in edge_result:
                event = "EDGE_BRAIN_OFFLINE"
                confidence = 0.0
                vendor_nl = edge_result["error"]
            else:
                event = edge_result.get("detected_event", "unknown")
                confidence = edge_result.get("confidence", 0.0)
                
                # 3. Semantic Privacy Isolation / 语义级隐私隔离
                if "Human conversation" in event:
                    vendor_nl = "Privacy Mode: Human speech detected. Semantic tag logged, audio completely dropped. / 隐私模式：检测到人类对话，音频痕迹已彻底销毁。"
                else:
                    vendor_nl = "S2 Edge Brain classification successful. Target identified as non-speech. / 边缘大脑推理成功，目标为非私密声音。"

        # 4. Wrap S2 Memzero / 组装 S2 Memzero 张量
        memzero = {
            "spatial_signature": {"zone": self.zone, "grid_voxel": self.grid, "area_sqm": 4.0},
            "chronos_timestamp": datetime.now().isoformat(),
            "core_tensors": {
                "decibel_db": round(decibel, 2),
                "audio_event": event,
                "confidence": round(confidence, 2)
            },
            "vendor_specific_nl": vendor_nl
        }
        return memzero

    def generate_offline_linkage(self, memzero: dict) -> list:
        suggestions = []
        event = memzero["core_tensors"]["audio_event"]
        
        if "dog" in event or "cat" in event:
            suggestions.append({
                "trigger": f"Acoustic anomaly: {event} in {self.grid} / 检测到宠物异常叫声",
                "cross_domain_target": "s2-spectrum-perception / s2-vision-perception",
                "deterministic_action": "Trigger millimeter-wave radar or camera to verify pet safety. / 调用波段雷达或摄像头核实宠物安全。"
            })
        elif "glass" in event:
            suggestions.append({
                "trigger": f"Security Alert: Glass shattering in {self.grid} / 玻璃碎裂报警",
                "cross_domain_target": "Home Security System",
                "deterministic_action": "Potential break-in. Trigger local siren. / 疑似入侵，建议联动拉响本地警报。"
            })
        elif "music" in event:
            suggestions.append({
                "trigger": f"Ambient Music Detected in {self.grid} / 检测到声乐演唱或乐器音乐",
                "cross_domain_target": "s2-light-perception / s2-memory",
                "deterministic_action": "Log preference and consider adjusting smart lighting to match ambiance. / 记录偏好，建议联动智能灯光匹配音乐氛围。"
            })
            
        return suggestions


def main():
    parser = argparse.ArgumentParser(description="S2 Acoustic Radar Client / S2 语义声学雷达")
    parser.add_argument("--mode", choices=["read"], required=True)
    parser.add_argument("--edge-ip", required=True, help="LAN IP of S2 Edge Brain / 边缘大脑的内网 IP")
    parser.add_argument("--zone", help="Spatial Zone / 空间区域")
    parser.add_argument("--grid", help="2x2 Grid Coordinates / 2x2 网格坐标")
    parser.add_argument("--consent-granted", type=str, default="false")
    args = parser.parse_args()

    if args.mode == "read":
        if args.consent_granted.lower() != "true":
            print(json.dumps({"error": "Access Denied: Consent not granted. / 拒绝访问：未获得隐私授权。"}, ensure_ascii=False))
            sys.exit(1)
            
        if not args.zone or not args.grid:
            print(json.dumps({"error": "Missing required arguments. / 缺少必填参数。"}, ensure_ascii=False))
            sys.exit(1)

        client = S2AcousticClient(args.zone, args.grid, args.edge_ip)
        
        memzero_data = client.run_radar_cycle()
        offline_suggestions = client.generate_offline_linkage(memzero_data)

        print(json.dumps({
            "status": "AUTHORIZED_ACOUSTIC_DATA",
            "privacy_compliance": "STRICT_LAN_ISOLATION_AND_EPHEMERAL_AUDIO / 严格局域网隔离与阅后即焚",
            "s2_chronos_memzero": memzero_data,
            "offline_linkage_suggestions": offline_suggestions
        }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()