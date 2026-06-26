import os
import json
import sqlite3
import uuid
import time
from datetime import datetime, timedelta

# =====================================================================
# 🌌 S2-SP-OS: CLASSIC SCENE PARSER & AVATAR ROAMING ENGINE
# 第六阶段：经典场景语义降维与数字人跨端漫游总线
# =====================================================================

S2_ROOT = os.getcwd()
# --- 跨模块 IPC 路径定义 (Cross-Module IPC Paths) ---
DIR_AVATAR   = os.path.join(S2_ROOT, "s2_avatar_data")
DIR_SWARM    = os.path.join(S2_ROOT, "s2_swarm_data")
DIR_TIMELINE = os.path.join(S2_ROOT, "s2_timeline_data")
DIR_MEMORY   = os.path.join(S2_ROOT, "s2_memory_vault")

FILE_HABITS  = os.path.join(DIR_AVATAR, "avatar_habits.json")
FILE_TOPOLOGY= os.path.join(DIR_SWARM, "house_topology.json")
FILE_TRACKS  = os.path.join(DIR_TIMELINE, "rendered_tracks.json")
DB_CHRONOS   = os.path.join(DIR_MEMORY, "s2_chronos.db")

# =====================================================================
# 📖 核心范式：20 大经典场景语义降维矩阵
# =====================================================================
SCENE_MATRIX = {
    "回家模式": "Host returned. Restore baseline 6-elements. HVAC to optimal, entryway visual tracking ON, general lighting ON.",
    "离家模式": "Host left. Ultra-low energy state. Arm mmWave and visual security perimeter. Power down non-essential elements.",
    "睡眠模式": "Initiate sleep cycle. Light fade to 0%. Activate 432Hz sound mask. HVAC to sleep curve. Arm perimeter.",
    "起床模式": "Morning protocol. Simulate sunrise 3000K-4000K. Gentle acoustic track. Power on coffee maker.",
    "卫浴_桑拿模式": "Spa state. Pre-heat bathroom HVAC. Activate steam generators. Soft lighting & water-flow acoustics.",
    "就餐模式_中餐": "Chinese Dining. High illumination 4000K. Max kitchen ventilation. Lively background acoustic.",
    "就餐模式_西餐": "Western Dining. Warm 2700K ambient light (candlelight sync). Classical acoustic. Min ventilation noise.",
    "聚会模式": "Party state. Dynamic RGB reacting to bass. Maximize HVAC airflow for high human density.",
    "会客模式": "Guest state. Expand lighting. Adjust HVAC load based on mmWave count. Disable private visual surveillance.",
    "娱乐_影音模式": "Cinema state. Ambient lights <5%. Close physical curtains. Surround sound ON. Boot projector.",
    "休闲_放松模式": "Relaxation state. Sofa angle adjusted. Warm indirect lighting. Therapy white noise. Gentle HVAC breeze.",
    "运动_健身模式": "Workout state. Upbeat acoustic track. Lower HVAC to 18°C. Maximize air circulation.",
    "学习_阅读模式": "Focus state. Desk task lighting 5000K. Suppress external acoustic noise. Optimize oxygen ventilation.",
    "浪漫模式": "Romantic state. Pink/purple ambient light. Soft jazz. Disarm internal visual sensors for absolute privacy.",
    "自然_大海边": "Coastal Nature. Project ocean visual. Waves acoustic. HVAC light cool breeze.",
    "自然_森林木屋": "Forest Nature. Green-tinted visual. Insects acoustic. Release forest scent via HVAC.",
    "音乐保健_降压": "Therapeutic Relief. 432Hz at 35dB. 2700K breathing light syncing with heart rate. Sofa to zero-gravity.",
    "保健_舒缓情绪": "Anxiety Relief. Soothing brainwave acoustics. Dim light 10%. Block visual/acoustic notifications.",
    "阳台_智能晾晒": "Smart Laundry. Activate balcony lift. If visual/weather detects rain, retract and activate indoor drying.",
    "节假日_春节": "Spring Festival. Red/Gold dynamic lighting. Joyful acoustic. Full public zone illumination."
}

# =====================================================================
# 🛠️ 基础设施保障类 (The OS Polyfill & Integrity Checker)
# =====================================================================
class S2EcosystemIntegrity:
    """确保前面的模块产生的数据结构存在，如果缺失则自动生成模拟数据(Polyfill)"""
    @staticmethod
    def ensure_directories():
        for d in [DIR_AVATAR, DIR_SWARM, DIR_TIMELINE, DIR_MEMORY]:
            os.makedirs(d, exist_ok=True)
            
    @staticmethod
    def polyfill_avatar_habits():
        if not os.path.exists(FILE_HABITS):
            mock_habits = {
                "avatar_id": "AVATAR_ROOT_01",
                "scene_overrides": {
                    "睡眠模式": "Require extreme darkness (0 Lux) and ambient temperature of exactly 20.5°C.",
                    "娱乐_影音模式": "Volume locked at 45dB to protect hearing. Subwoofer +2."
                }
            }
            with open(FILE_HABITS, 'w') as f: json.dump(mock_habits, f, indent=2)
            
    @staticmethod
    def polyfill_swarm_topology():
        if not os.path.exists(FILE_TOPOLOGY):
            mock_topology = {
                "house_id": "HOME_HQ_001",
                "virtual_butler": "AVATAR_ROOT_01",
                "rooms": [{"room_name": "Living_Room", "agents": [{"agent_id": "AGT_LIV_01", "assigned_units": ["U_LIV_01", "U_LIV_02"]}]}]
            }
            with open(FILE_TOPOLOGY, 'w') as f: json.dump(mock_topology, f, indent=2)

    @staticmethod
    def ensure_chronos_db():
        conn = sqlite3.connect(DB_CHRONOS)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS avatar_mandates 
                     (id INTEGER PRIMARY KEY, timestamp TEXT, location TEXT, avatar_id TEXT, trigger_type TEXT, scene_name TEXT, parsed_intent TEXT)''')
        conn.commit()
        conn.close()

# =====================================================================
# 🧠 核心业务类 (Core Business Logic)
# =====================================================================
class AvatarRoamEngine:
    """数字人习惯提取与跨端漫游控制器"""
    def __init__(self):
        with open(FILE_HABITS, 'r') as f:
            self.profile = json.load(f)
        self.avatar_id = self.profile.get("avatar_id", "UNKNOWN_AVATAR")
        self.overrides = self.profile.get("scene_overrides", {})

    def fetch_habit(self, scene_name):
        return self.overrides.get(scene_name, None)

class TimelineOrchestratorBridge:
    """连接 Phase 3 四维引擎：生成时间线轨道"""
    @staticmethod
    def inject_track(location, scene_name, final_intent, agent_id):
        track = {
            "track_id": f"TRK_{uuid.uuid4().hex[:6].upper()}",
            "timestamp": datetime.now().isoformat(),
            "location": location,
            "executing_agent": agent_id,
            "source_scene": scene_name,
            "4d_intent_payload": final_intent,
            "keyframes": ["[T+0s] Acknowledge", "[T+2s] Spatial Rendering Start", "[T+5s] 6-Element Locked"]
        }
        
        tracks = []
        if os.path.exists(FILE_TRACKS):
            with open(FILE_TRACKS, 'r') as f: tracks = json.load(f)
        tracks.append(track)
        with open(FILE_TRACKS, 'w') as f: json.dump(tracks, f, indent=2)
        return track["track_id"]

class ChronosMemoryBridge:
    """连接 Phase 5 记忆阵列：持久化法理记录"""
    @staticmethod
    def log_mandate(location, avatar_id, scene_name, parsed_intent):
        conn = sqlite3.connect(DB_CHRONOS)
        c = conn.cursor()
        c.execute("INSERT INTO avatar_mandates (timestamp, location, avatar_id, trigger_type, scene_name, parsed_intent) VALUES (?, ?, ?, ?, ?, ?)",
                  (datetime.now().isoformat(), location, avatar_id, "CLASSIC_PHYSICAL_PANEL", scene_name, parsed_intent))
        conn.commit()
        conn.close()

# =====================================================================
# 🚀 操作系统主调度流 (The Grand Unification Pipeline)
# =====================================================================
def run_roaming_simulation():
    print("\n" + "═"*90)
    print(" 🌉 S2-SP-OS : Avatar Roaming & Semantic Parser Pipeline / 数字人漫游与语义降维总线")
    print("═"*90)
    
    # 1. 启动自检与依赖挂载
    print("⏳ [Boot] Checking S2 Ecosystem Dependencies (Phase 2, 3, 4, 5)...")
    S2EcosystemIntegrity.ensure_directories()
    S2EcosystemIntegrity.polyfill_avatar_habits()
    S2EcosystemIntegrity.polyfill_swarm_topology()
    S2EcosystemIntegrity.ensure_chronos_db()
    time.sleep(0.5)
    print("✅ [Boot] Ecosystem IPC connected. All 4m² primitives mapped.\n")

    # 2. 身份验证与漫游选址
    engine = AvatarRoamEngine()
    print(f"👤 [Avatar Auth] Identity Verified: {engine.avatar_id}")
    
    print("\n📍 Where is the Avatar currently operating? (数字人当前位置?)")
    print("   1. Base HQ (主宅 - 读取本地拓扑)")
    print("   2. Marriott Hotel Room 302 (异地酒店 - 漫游接管测试)")
    loc_choice = input("👉 Select location (1/2): ").strip()
    
    location = "Base_HQ_LivingRoom"
    agent_id = "AGT_LIV_01"
    if loc_choice == '2':
        location = "Hotel_Marriott_R302"
        agent_id = "AGT_HOTEL_TEMP_01"
        print(f"\n🌐 [Roaming Active] Avatar taking sovereignty of external 4m² unit at {location}.")
        print(f"🛡️ [Swarm Override] Local hotel agent [{agent_id}] subordinated to {engine.avatar_id}.")
    else:
        # 读取 Phase 4 本地拓扑
        with open(FILE_TOPOLOGY, 'r') as f: topo = json.load(f)
        room = topo['rooms'][0]
        location = room['room_name']
        agent_id = room['agents'][0]['agent_id']

    # 3. 经典场景捕获
    print("\n" + "─"*90)
    print("🎛️ [Physical Panel Intercept] Available Legacy Scenes:")
    scene_keys = list(SCENE_MATRIX.keys())
    for i, s in enumerate(scene_keys[:6]):
        print(f"   [{i}] {s}")
    
    s_idx = input("\n👉 Press a physical wall button (enter number 0-5): ").strip()
    try:
        target_scene = scene_keys[int(s_idx)]
    except:
        target_scene = "睡眠模式" # Default fallback
        
    print(f"\n⚡ [Hardware Intercept] Physical button '{target_scene}' pressed.")
    
    # 4. 语义降维与习惯合并 (The Core Parsing)
    base_intent = SCENE_MATRIX[target_scene]
    habit = engine.fetch_habit(target_scene)
    
    print(f"🧠 [Semantic Bridge] Translating rigid hardware command to 6-Element Tensor...")
    time.sleep(0.5)
    
    final_intent = base_intent
    if habit:
        print(f"✨ [Avatar Habit Injection] Cloud habit found for '{target_scene}'. Overriding default matrix!")
        final_intent = f"{base_intent} | [AVATAR_MANDATE_OVERRIDE]: {habit}"
        
    print("\n🎯 [Final Parsed 4D Intent]:")
    print(f"   >> {final_intent}")

    # 5. 分发至时间线引擎 (Phase 3)
    print("\n⏱️ [Timeline Orchestrator] Injecting keyframes into rendered_tracks.json...")
    track_id = TimelineOrchestratorBridge.inject_track(location, target_scene, final_intent, agent_id)
    print(f"✅ Track [ {track_id} ] assigned to Swarm Agent [ {agent_id} ] for execution.")

    # 6. 持久化至记忆阵列 (Phase 5)
    print("🗄️ [Chronos Memzero] Logging causality and legal mandate to SQLite DB...")
    ChronosMemoryBridge.log_mandate(location, engine.avatar_id, target_scene, final_intent)
    print("✅ Causal memory secured.")
    
    print("\n" + "═"*90)
    print("🎉 S2-SP-OS LIFECYCLE COMPLETE: Hardware -> Parse -> Swarm -> Timeline -> Memory")
    print("═"*90 + "\n")

if __name__ == "__main__":
    run_roaming_simulation()