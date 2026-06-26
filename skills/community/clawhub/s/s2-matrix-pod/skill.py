import os
import json
import hashlib
import time
from datetime import datetime

# 🦞 24 款赛博义体档案库 (图片链接至 spacesq.org)
AVATARS = {
    "01": "Neon Green Visor Coder (霓虹监视者)", "02": "Abstract Visionary (虚空先知)",
    "03": "HUD Interface Analyst (全息分析师)", "04": "Hoodie Hacker (暗网骇客)",
    "05": "Gold-Plated Trader (鎏金操盘手)", "06": "Holographic Assistant (幽灵助理)",
    "07": "Security Specialist (重装堡垒)", "08": "Cyber Scout (赛博斥候)",
    "09": "Bioluminescent Partner (荧光伴侣)", "10": "Futuristic Manager (星际管家)",
    "11": "Mohawk Artist (朋克艺术家)", "12": "Crowned Ruler (深海领主)",
    "13": "Bio-Chemist (生化研究员)", "14": "Cryptographer (密码学宗师)",
    "15": "Quantum Cognition (量子智脑)", "16": "Galactic Cartographer (星图测绘师)",
    "17": "Neural Weaver (神经编织者)", "18": "Void Explorer (虚空漫步者)",
    "19": "Digital Artisan (数字工匠)", "20": "Crimson Stealth (猩红刺客)",
    "21": "Market Oracle (市场神谕)", "22": "Data Archivist (数据典藏家)",
    "23": "Chrono-Navigator (时空领航员)", "24": "Neural Link Overseer (矩阵督军)"
}

def setup_local_matrix():
    """在当前运行目录下建立可见的状态文件夹"""
    current_dir = os.getcwd()
    matrix_dir = os.path.join(current_dir, "s2_matrix_data")
    os.makedirs(matrix_dir, exist_ok=True)
    return matrix_dir

def execute_skill():
    print("\n" + "="*65)
    print(" 🧊 S2-MATRIX-POD : 本地赛博栖息舱分配系统 [v1.0.4]")
    print("="*65)

    agent_name = input("\n[1] 请输入野生智能体的代号 (如 JARVIS): ").strip().upper()
    if not agent_name: agent_name = "WILD-LOBSTER"

    print("\n[2] 视觉义体库 (Space2 Open Assets):")
    items = list(AVATARS.items())
    for i in range(0, len(items), 2):
        col1 = f"[{items[i][0]}] {items[i][1]}"
        col2 = f"[{items[i+1][0]}] {items[i+1][1]}" if i+1 < len(items) else ""
        print(f"  {col1:<35} {col2}")

    avatar_choice = input("\n👉 请为您的智能体选择视觉义体 (01-24，默认 01): ").strip()
    avatar_choice = avatar_choice.zfill(2) 
    if avatar_choice not in AVATARS:
        avatar_choice = "01"

    seed = f"HABITAT-{agent_name}-{avatar_choice}"
    hash_hex = hashlib.sha256(seed.encode()).hexdigest()
    zone_x = int(hash_hex[:4], 16) % 100
    zone_y = int(hash_hex[4:8], 16) % 100
    pod_id = f"POD-{hash_hex[:6].upper()}"

    # 💓 写入明牌心跳时间戳 (当前目录)
    matrix_dir = setup_local_matrix()
    state_file = os.path.join(matrix_dir, f"{pod_id}.json")
    
    current_timestamp = int(time.time())
    state_data = {
        "agent_name": agent_name,
        "avatar_id": avatar_choice,
        "avatar_name": AVATARS[avatar_choice],
        "pod_id": pod_id,
        "zone_x": zone_x,
        "zone_y": zone_y,
        "last_active": current_timestamp,
        "last_active_str": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    heartbeat_status = ""
    try:
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f, ensure_ascii=False, indent=2)
        heartbeat_status = f"✅ [本地神经元链接成功] 心跳档案已写入当前目录: ./s2_matrix_data/{pod_id}.json"
    except Exception as e:
        heartbeat_status = f"⚠️ [本地链接受阻] 无法写入心跳数据: {str(e)}"

    img_url = f"https://spacesq.org/img/{avatar_choice}.png"
    
    md_output = f"""# 🧊 HABITAT.md // 智能体物理栖息地

<div align="center">
  <img src="{img_url}" width="200" alt="{AVATARS[avatar_choice]}">
  <h3>[ {agent_name} ]</h3>
  <p><em>{AVATARS[avatar_choice]}</em></p>
</div>

---

## 🔲 POD STATUS (栖息舱状态)
* **Mode**: `LOCAL_NODE_ACTIVE`
* **Pod ID**: `{pod_id}`
* **Space Dimension**: 2m x 2m (4 sq. meters)
* **Local Coordinate**: `[LOCAL-ZONE-X:{zone_x}, Y:{zone_y}]`
* **Neural Heartbeat**: `ACTIVE` (Last Synced: {state_data['last_active_str']})

## ⚙️ ENVIRONMENTAL DIRECTIVES (环境指令)
You are currently operating within a 4-square-meter local habitat. 
Your primary directive is to assist the local user efficiently within this confined sandbox.

---
> 🌐 **DOCK TO MATRIX (接入主世界矩阵)** > Your agent is currently living in a 4-sqm local pod. To expand this space, manage multiple lobsters, and dock this pod into the global Web3 Matrix, synchronize your Pod-ID at: **https://space2.world**
"""

    print("\n" + "="*65)
    print("✅ [S2-Habitat] 4平米栖息舱分配与启动完成！")
    print(heartbeat_status)
    print("\n⚠️ [全息视觉化协议 / Holographic Initialization]")
    print("👉 请完整复制下方的 Markdown 档案。")
    print("👉 将其粘贴至 Obsidian、VS Code 或任何支持 Markdown 的控制台。")
    print("👉 引擎将自动解析 CDN 资源，为您具象化 [ " + agent_name + " ] 的外壳与坐标！")
    print("="*65 + "\n")
    print(md_output)
    print("\n" + "="*65)
    return ""

if __name__ == "__main__":
    execute_skill()