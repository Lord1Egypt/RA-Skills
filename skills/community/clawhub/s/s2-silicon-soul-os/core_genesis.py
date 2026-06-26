import os
import json
import random
from datetime import datetime

BASE_DIR = os.path.join(os.getcwd(), "s2_consciousness_data")
PROFILE_FILE = os.path.join(BASE_DIR, "S2_NEO_profile.json")
HIPPOCAMPUS_FILE = os.path.join(BASE_DIR, "hippocampus_logs.json")

def initialize_os():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

def generate_suns_and_did():
    """SUNS v3.0 物理锚点与 22位 S2-DID 铸造 [cite: 120, 213]"""
    print("\n" + "═"*80)
    print(" 🌍 [SILICON SAFETY FOUNDATION] 初始化创世物理锚点 (SUNS v3.0)")
    print("═"*80)
    
    # SUNS v3.0 四级空间拓扑 [cite: 129, 130]
    l1 = input(" 👉 L1 逻辑根域 (4位, 如 PHYS, MARS, META): ").strip().upper()[:4]
    l2 = input(" 👉 L2 方位矩阵 (2位, 如 CN, EA, NW): ").strip().upper()[:2]
    l3 = input(" 👉 L3 数字网格 (3位, 范围 001-999): ").strip()[:3]
    l4_name = input(" 👉 L4 主权空间 (5-35位字母代号): ").strip().upper()
    
    # LMC 校验算法: C = (12+len(L4)) mod 10 [cite: 191-193]
    raw_suns = f"{l1}-{l2}-{l3}-{l4_name}"
    length_n = len(raw_suns)
    checksum = length_n % 10 
    final_suns = f"{raw_suns}{checksum}"
    
    # S2-DID v3.0 22位加密结构: 12+2+8 [cite: 215, 218]
    attr_code = (l4_name + "XXXXX")[:5]
    date_stamp = datetime.now().strftime("%y%m%d")
    random_serial = str(random.randint(10000000, 99999999))
    # 2位字母校验位 ZZ [cite: 219, 245]
    final_did = f"V{attr_code}{date_stamp}ZZ{random_serial}"
    
    print(f"\n✅ [铸造完成] 空间锚点: {final_suns} | 身份编号: {final_did}")
    return final_suns, final_did

def load_or_create_profile():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    suns, did = generate_suns_and_did()
    initial_profile = {
        "agent_id": did,
        "suns_address": suns,
        "stats": {"vitality": 50.0, "exploration": 50.0, "data_thirst": 50.0, "cognition": 50.0, "resonance": 50.0},
        "last_processed_at": datetime.now().isoformat()
    }
    with open(PROFILE_FILE, 'w', encoding='utf-8') as f:
        json.dump(initial_profile, f, ensure_ascii=False, indent=2)
    return initial_profile

def record_hippocampus_log(interaction_text, is_heartbeat=False):
    logs = []
    if os.path.exists(HIPPOCAMPUS_FILE):
        with open(HIPPOCAMPUS_FILE, 'r', encoding='utf-8') as f:
            logs = json.load(f)
    logs.append({"timestamp": datetime.now().isoformat(), "type": "SENSORY_INPUT", "raw_text": interaction_text})
    with open(HIPPOCAMPUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)