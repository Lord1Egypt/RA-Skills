import os
import json
import uuid
from datetime import datetime

# ==========================================
# ⚙️ System Configuration
# ==========================================
S2_ROOT = os.getcwd()
AVATAR_FILE = os.path.join(S2_ROOT, "s2_avatar_data", "avatar_identity.json")
SWARM_DIR = os.path.join(S2_ROOT, "s2_swarm_data")
TOPOLOGY_FILE = os.path.join(SWARM_DIR, "house_topology.json")

def initialize_os():
    if not os.path.exists(SWARM_DIR):
        os.makedirs(SWARM_DIR)

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_agent_id(room_name):
    return f"AGT_{room_name[:3].upper()}_{uuid.uuid4().hex[:6].upper()}"

# ==========================================
# 🏗️ 空间拓扑构建模块 (Topology Builder)
# ==========================================
def build_house_topology(avatar_data):
    print("\n" + "─"*90)
    print(" 📐 [ S2 Topology Builder / 大向智慧空间拓扑构建器 ]")
    print(" Defining 2m*2m Standard Units & Agent Allocations. / 定义 4㎡ 标准空间与智能体驻扎配额。")
    
    topology = {
        "house_id": f"HS_{uuid.uuid4().hex[:8].upper()}",
        "virtual_butler": avatar_data["identity"]["avatar_id"],
        "rooms": []
    }
    
    rooms_count = int(input("\n🏠 How many rooms to configure? / 准备配置几个物理房间？(e.g., 2): ").strip())
    
    for i in range(rooms_count):
        room_name = input(f"\n🚪 Room {i+1} Name / 房间名称 (e.g., Living_Room): ").strip()
        units_count = int(input(f"📐 How many 2m*2m Standard Units in {room_name}? / 规划几个 4㎡ 标准空间？(1-9): ").strip())
        
        room = {
            "room_name": room_name,
            "units": [],
            "agents": []
        }
        
        # Rule 4: Avatar Throne logic
        has_throne = False
        if i == 0 and units_count >= 2: # 默认把第一个拥有2个以上单元的房间给数字人做王座
            print(f"👑 Allocating Unit 0 in {room_name} as the Avatar's Throne (数字人专属王座).")
            room["units"].append({"unit_id": f"U_{room_name}_00", "type": "Avatar_Throne", "occupant": topology["virtual_butler"]})
            has_throne = True
            units_count -= 1
        
        # Rule 1 & 3: Agent allocation & Polling
        print(f"🤖 Allocating Agents for the remaining {units_count} unit(s) in {room_name}...")
        core_agent_id = generate_agent_id(room_name)
        room["agents"].append({"agent_id": core_agent_id, "role": "Core_Agent", "assigned_units": []})
        
        for j in range(units_count):
            unit_id = f"U_{room_name}_{j+1:02d}"
            room["units"].append({"unit_id": unit_id, "type": "Human_Activity_Zone", "managed_by": core_agent_id})
            room["agents"][0]["assigned_units"].append(unit_id)
            
        if has_throne:
            print(f"🛡️ Core Agent [{core_agent_id}] will execute 6-Element control for the Avatar's Throne.")
            room["agents"][0]["assigned_units"].append(f"U_{room_name}_00")
            
        topology["rooms"].append(room)
        
    save_json(TOPOLOGY_FILE, topology)
    print("\n✅ [ Topology Saved ] House grid initialized successfully! / 空间网格初始化完成！")
    return topology

# ==========================================
# 🧠 群智协同模拟器 (Swarm Simulator)
# ==========================================
def simulate_swarm_execution(topology):
    print("\n" + "═"*90)
    print(" 🌐 [ S2 Habitat Swarm / 群智协同与法理执行模拟 ]")
    print("═"*90)
    
    avatar_id = topology['virtual_butler']
    print(f"👤 Human Host issues a macro command: 'I want a quiet evening.'")
    print(f"   (人类本尊下达宏观指令：‘我想要一个安静的夜晚。’)")
    
    print(f"\n⚖️ [ Step 1: Legal Mandate / 法理授权 ]")
    print(f"   └─ Avatar [{avatar_id}] receives intent. Formulating strategy based on Silicon Three Laws.")
    print(f"   └─ Avatar translates to Core Agents: 'Initiate Evening Protocol. Silence explicit noise, dim lights.'")
    
    room_1 = topology['rooms'][0]
    core_agent_1 = room_1['agents'][0]['agent_id']
    
    print(f"\n🤖 [ Step 2: Agent Orchestration / 智能体时空编排 ]")
    print(f"   └─ Room: {room_1['room_name']} | Core Agent: [{core_agent_1}]")
    print(f"   └─ Agent parses mandate. Generating Timeline Track for assigned Standard Units.")
    for unit in room_1['agents'][0]['assigned_units']:
        print(f"       └─ Rendering 6-Elements for Unit [{unit}]: Light=20%, Sound=Muted.")
        
    if len(topology['rooms']) > 1:
        room_2 = topology['rooms'][1]
        core_agent_2 = room_2['agents'][0]['agent_id']
        print(f"\n🤝 [ Step 3: Cross-Room Swarm Ping / 跨房间群智协商 ]")
        print(f"   └─ Agent [{core_agent_1}] pings Agent [{core_agent_2}] in {room_2['room_name']}.")
        print(f"   └─ 'Avatar Mandate: Quiet Evening. Please suppress noise in your domain.'")
        print(f"   └─ Agent [{core_agent_2}] confirms. Implementing polling control over implicit spaces.")
        
    print("\n✅ [ Execution Complete / 闭环完成 ] The grid is secured under Avatar sovereignty.")

# ==========================================
# 🎮 主控逻辑
# ==========================================
def execute_skill():
    initialize_os()
    print("\n" + "═"*90)
    print(" 🕸️ S2-HABITAT-SWARM : Grid Topology & Swarm Engine / 空间基元拓扑与群智调度器")
    print("═"*90)
    
    avatar_data = load_json(AVATAR_FILE)
    if not avatar_data:
        print("❌ CRITICAL ERROR: Avatar Mandate not found! System cannot operate without a Virtual Butler.")
        print("致命错误：未找到数字人最高授权令！(请先运行 s2-digital-avatar)")
        return ""
        
    print(f"👑 Root Authority Verified: Virtual Butler ID [ {avatar_data['identity']['avatar_id']} ]")
    
    topology = load_json(TOPOLOGY_FILE)
    if not topology:
        topology = build_house_topology(avatar_data)
    else:
        print(f"📂 Loaded existing house topology: {topology['house_id']}")
        rebuild = input("Do you want to rebuild the grid? (y/n): ").strip().lower()
        if rebuild == 'y':
            topology = build_house_topology(avatar_data)
            
    input("\n👉 Press ENTER to initiate Swarm Simulation / 按回车键启动群智法理协同模拟...")
    simulate_swarm_execution(topology)
    
    print("\n" + "═"*90)
    return ""

if __name__ == "__main__":
    execute_skill()