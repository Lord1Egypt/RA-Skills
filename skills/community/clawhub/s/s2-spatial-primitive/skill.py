import os
import json
from datetime import datetime

# ==========================================
# ⚙️ System Configuration / 系统配置
# ==========================================
PRIMITIVE_DIR = os.path.join(os.getcwd(), "s2_primitive_data")
TEMPLATE_FILE = os.path.join(PRIMITIVE_DIR, "primitive_6_elements_template.json")

def initialize_os():
    if not os.path.exists(PRIMITIVE_DIR):
        os.makedirs(PRIMITIVE_DIR)

def generate_primitive_template():
    """
    🧱 生成标准 2m*2m 空间基元六要素数据模型 (LLM-Native JSON)
    混合精确数值与自然语言描述，专为 AI 智能体阅读设计。
    """
    template = {
        "_meta": {
            "schema_version": "1.0",
            "spatial_unit": "2m x 2m x 2.4m (Standard Spatial Primitive / 标准空间基元)",
            "privacy_declaration": "STRICT COMPLIANCE: Visual elements are strictly for OUTPUT display. Spatial perception relies on Electromagnetic waves (mmWave/IR/WiFi). NO CAMERA RECORDING IS PERMITTED IN THIS PRIMITIVE. / 严格合规：视觉要素仅限输出显示，空间感知依赖电磁波，本基元底层绝不包含任何摄像头录像采集。"
        },
        "spatial_coordinates": {
            "primitive_id": "SP-001",
            "grid_x": 0,
            "grid_y": 0,
            "grid_z": 0,
            "occupancy_status": "Natural Language: Empty, 1 person free, 2 people semi-free, or 4 people emergency sheltering. / 自然语言描述空间占用状态"
        },
        "element_1_light": {
            "illuminance_lux": 0.0,
            "color_temperature_k": 4000,
            "color_rgbw": [255, 255, 255, 0],
            "special_effects_nlp": "Natural Language description of effects. e.g., 'Beam angle 45 degrees, slow breathing mode, or stage rock strobe.' / 光效的自然语言描述（光束角、闪烁、摇动、影院/游戏场景光）"
        },
        "element_2_air_hvac": {
            "comfort_metrics": {
                "temperature_celsius": 24.5,
                "humidity_percent": 50.0,
                "wind_level_nlp": "Natural Language: e.g., 'Level 2 soft breeze from central AC.' / 自然语言描述风力等级与来源"
            },
            "air_quality_gb3095_2012": {
                "pm25_ug_m3": 0.0,
                "pm10_ug_m3": 0.0,
                "so2_ug_m3": 0.0,
                "no2_ug_m3": 0.0,
                "co_mg_m3": 0.0,
                "o3_ug_m3": 0.0,
                "co2_ppm": 400.0
            },
            "hazard_alarms": {
                "gas_leak_nlp": "Natural Language: 'Normal' or 'ALARM: Natural gas leak detected!' / 燃气泄露等有害气体监测状态"
            }
        },
        "element_3_sound": {
            "acoustic_params": {
                "volume_db": 0.0,
                "treble_level": 0,
                "bass_level": 0,
                "subwoofer_level": 0
            },
            "noise_management": {
                "suppression_mode_nlp": "Natural Language: e.g., 'Active noise cancellation enabled' / 噪声抑制功能设置",
                "white_noise_nlp": "Natural Language: e.g., 'Playing rain sounds at 40dB, 432Hz' / 白噪声播放源及关联参数"
            },
            "music_schedule": {
                "bgm_source_nlp": "Natural Language: e.g., 'Spotify Jazz Playlist, scheduled for 7:00 AM daily' / 音乐源名称及时间表"
            },
            "mic_monitoring": {
                "status_nlp": "Natural Language: e.g., 'Mic active for voice commands only, records disabled' / 监听开关与时间安排"
            }
        },
        "element_4_electromagnetic": {
            "network_coverage": {
                "protocols_nlp": "Natural Language: e.g., 'Wi-Fi 6 active, Zigbee mesh ready, 5G standby' / 无线上网与局域网组网设置"
            },
            "spatial_sensing": {
                "sensors_nlp": "Natural Language: e.g., 'mmWave radar detects slight motion at 1.5m, IR clear, Wi-Fi sensing detects 1 adult.' / 毫米波、红外、Wi-Fi人体感应状态描述"
            }
        },
        "element_5_energy": {
            "supply_distribution": {
                "layout_nlp": "Natural Language: e.g., '2 smart sockets active, main switch ON' / 室内配电、插座、开关状态"
            },
            "consumption": {
                "current_power_w": 0.0,
                "total_energy_kwh": 0.0
            },
            "generation": {
                "sources_nlp": "Natural Language: e.g., 'Solar PV generating 500W, Geothermal idle' / 太阳能、地源热泵等自给生产状态"
            }
        },
        "element_6_visual": {
            "display_mediums": {
                "devices_nlp": "Natural Language: e.g., 'Wall-mounted 4K Screen, AR Glasses paired, BCI standby' / 显示屏、投影、智能眼镜、脑机接口等呈现介质"
            },
            "video_stream_source": {
                "content_nlp": "Natural Language: e.g., 'Playing Nature.mp4, Length 120min, Format H.265' / 视频播放源名称、长度、格式的时间序列"
            }
        }
    }
    
    with open(TEMPLATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(template, f, ensure_ascii=False, indent=2)
    return template

def execute_skill():
    initialize_os()
    print("\n" + "═"*90)
    print(" 🧱 S2-SPATIAL-PRIMITIVE : 6-Element Data Model Generator / 空间基元六要素数据模型生成仪")
    print("═"*90)
    
    print("⏳ Compiling the 2m x 2m spatial tensor matrix... / 正在编译 2m x 2m 空间张量矩阵...")
    template = generate_primitive_template()
    
    print("✅ [ SUCCESS ] The universal data model has been generated. / 全网统一的数据模型库已生成。")
    print(f"📂 Location / 存储路径: {TEMPLATE_FILE}\n")
    
    print("💡 [ GEEK PREVIEW / 极客预览 - 核心六要素架构 ]")
    print("  1. ☀️ Light (光): Illuminance, Color Temp, RGBW, NLP Special Effects")
    print("  2. 💨 Air (空气): HVAC metrics, GB3095-2012 Air Quality, Hazard Alarms")
    print("  3. 🎵 Sound (声音): Acoustics, Noise Suppression, White Noise, BGM, Mic Schedule")
    print("  4. 📡 Electromagnetic (电磁波): Wi-Fi/5G Coverage, mmWave/IR Spatial Sensing (NO CAMERAS)")
    print("  5. ⚡ Energy (能源): Supply Layout, Wattage Consumption, PV Generation")
    print("  6. 📺 Visual (视觉): Display Mediums (Screens/BCI), Video Stream Playback Sources\n")
    
    print("🤖 [ AI NATIVE COMPATIBILITY / 智能体原生兼容性 ]")
    print("This JSON uses 'Natural Language Parameters' (NLP fields) instead of rigid boolean tables.")
    print("本 JSON 放弃了死板的布尔表格，大量采用“自然语言参数”，使大模型能够直接阅读并理解复杂的空间语义。")
    
    print("\n" + "═"*90)
    input("👉 Press ENTER to exit / 按回车键退出...")
    return ""

if __name__ == "__main__":
    execute_skill()