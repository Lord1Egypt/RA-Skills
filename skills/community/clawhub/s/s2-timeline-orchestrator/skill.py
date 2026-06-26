import os
import json
import urllib.request
from datetime import datetime

# ==========================================
# ⚙️ System Configuration / 系统配置
# ==========================================
PRIMITIVE_DIR = os.path.join(os.getcwd(), "s2_primitive_data")
MOUNTS_FILE = os.path.join(PRIMITIVE_DIR, "active_hardware_mounts.json")
TIMELINE_DIR = os.path.join(os.getcwd(), "s2_timeline_data")
TRACKS_FILE = os.path.join(TIMELINE_DIR, "rendered_tracks.json")

def initialize_os():
    if not os.path.exists(TIMELINE_DIR):
        os.makedirs(TIMELINE_DIR)

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_timeline_track(intent_nlp, active_devices):
    """
    ⏱️ 核心：通过大语言模型生成六要素时间线渲染轨道 (Timeline Track)
    将自然语言意图，转化为按时间轴分布的设备控制关键帧序列。
    """
    api_base = "http://localhost:1234/v1"
    model_name = "local-model"
    
    devices_context = json.dumps(active_devices, ensure_ascii=False)
    
    prompt = f"""
    [ROLE]
    You are the 'S2-Timeline-Orchestrator', a spatiotemporal rendering engine for the S2-SP-OS.
    你是 S2 空间基元操作系统的时空渲染引擎。

    [TASK]
    Translate the user's natural language intent into a "Timeline Track" (a sequence of keyframes).
    将用户的自然语言意图，转化为一条“时间线轨道”（包含多个关键帧动作）。
    You must ONLY use the devices listed in the Active Mounts context.

    [INPUT CONTEXT]
    User Intent (用户意图): {intent_nlp}
    Active Mounts (当前可用设备): {devices_context}

    [OUTPUT REQUIREMENT]
    Return ONLY a valid JSON object representing the timeline track. Use "T+Xm" (X minutes from now) as the time offset.
    Example:
    {{
      "track_id": "TRK_AUTO_GEN",
      "scenario": "Evening relaxation to sleep",
      "keyframes": [
        {{
          "time_offset": "T+0m",
          "element": "element_1_light",
          "device_id": "SMART_BULB_123",
          "rendered_state": {{"brightness": 50, "color_temp": 3000}},
          "reason_nlp": "Dimming lights for relaxation / 调暗灯光以放松"
        }},
        {{
          "time_offset": "T+60m",
          "element": "element_3_sound",
          "device_id": "SOUNDBAR_456",
          "rendered_state": {{"action": "play_white_noise", "volume": 20}},
          "reason_nlp": "Playing white noise for sleep / 播放白噪声助眠"
        }}
      ]
    }}
    """
    
    data = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are a strict JSON Timeline Generator for IoT orchestrations."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }
    
    try:
        req = urllib.request.Request(f"{api_base}/chat/completions", data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
        response = urllib.request.urlopen(req, timeout=20)
        content = json.loads(response.read().decode('utf-8'))['choices'][0]['message']['content']
        content = content.replace('```json', '').replace('```', '').strip()
        parsed_data = json.loads(content)
        parsed_data["track_id"] = f"TRK_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        parsed_data["rendered_at"] = datetime.now().isoformat()
        return parsed_data
    except Exception as e:
        return {"error": "LLM Timeline Generation Failed / 时间线生成失败", "details": str(e)}

def execute_skill():
    initialize_os()
    print("\n" + "═"*90)
    print(" ⏱️ S2-TIMELINE-ORCHESTRATOR : Spatiotemporal Rendering Engine / 六要素时空渲染器")
    print("═"*90)
    
    mounts_data = load_json(MOUNTS_FILE)
    active_devices = mounts_data.get("active_devices", [])
    
    if not active_devices:
        print("⚠️ Warning: No active devices found in mounts. Loading virtual devices for simulation. / 警告：未发现挂载的物理设备。正在加载虚拟设备以供模拟测试。")
        active_devices = [
            {"device_id": "VIRTUAL_BULB_01", "primary_element": "element_1_light", "capabilities_nlp": "Dimmable light, color temp 2700K-6500K / 可调亮度色温的智能灯"},
            {"device_id": "VIRTUAL_SPEAKER_01", "primary_element": "element_3_sound", "capabilities_nlp": "Play music, white noise, volume 0-100 / 播放音乐、白噪声"}
        ]
    else:
        print(f"📡 Loaded {len(active_devices)} active mounted device(s) from S2 grid. / 已从 S2 网格加载 {len(active_devices)} 个挂载设备。")

    print("\n[ Scenario Input / 输入场景意图 ]")
    intent = input("🗣️ Describe your upcoming routine (e.g., 'I will be home in 10 mins, want to read for an hour then sleep'): \n👉 ").strip()
    
    if not intent:
        print("❌ Orchestration aborted due to empty input. / 输入为空，渲染终止。")
        return ""

    print("\n⏳ LLM is predicting the timeline and rendering 6-Element keyframes... / 大模型正在预测时间线并渲染六要素关键帧...")
    track_result = generate_timeline_track(intent, active_devices)
    
    if "error" in track_result:
        print(f"\n❌ {track_result['error']}\n   {track_result['details']}")
        return ""
        
    print("\n✅ [ Render Complete / 轨道渲染完成 ] Timeline Track Generated!")
    print("─"*90)
    print(f" 🎬 Track ID: {track_result.get('track_id')}")
    print(f" 📜 Scenario: {track_result.get('scenario')}")
    print(" 🎞️ Keyframes (关键帧序列):")
    
    for kf in track_result.get('keyframes', []):
        print(f"    [{kf.get('time_offset')}] 🎯 {kf.get('element')} -> 🔌 {kf.get('device_id')}")
        print(f"            └─ Action: {kf.get('rendered_state')} ({kf.get('reason_nlp')})")
    
    print("─"*90)
    
    # 将渲染的轨道保存至本地
    tracks_db = load_json(TRACKS_FILE)
    if "scheduled_tracks" not in tracks_db:
        tracks_db["scheduled_tracks"] = []
    tracks_db["scheduled_tracks"].append(track_result)
    save_json(TRACKS_FILE, tracks_db)
    
    print(f"💾 Rendered track securely injected into Timeline DB / 渲染轨道已注入时空数据库: {TRACKS_FILE}")
    print("═"*90 + "\n")
    return ""

if __name__ == "__main__":
    execute_skill()