#!/usr/bin/env python3
import os
import json
import hashlib
import time
from datetime import datetime
from typing import Dict, List

# =====================================================================
# 🕸️ S2-SP-OS: Spatial Topology & Swarm Matrix Manager (V1.0)
# 空间拓扑与多智能体矩阵管理器：管理房间划分、SSSU 网格分配与多 Agent 驻扎
# =====================================================================

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

class S2SpatialTopology:
    def __init__(self, phys_address: str):
        self.phys_address = phys_address
        self.matrix_dir = os.path.join(os.getcwd(), "s2_matrix_data")
        os.makedirs(self.matrix_dir, exist_ok=True)
        self.topology_db = os.path.join(self.matrix_dir, "s2_topology_state.json")
        
        # 核心状态树: { "Room_ID": { "name": "客厅", "capacity_grids": 5, "occupants": { "Grid_1": "POD-XXX", ... } } }
        self.topology = self._load_topology()

    def _load_topology(self) -> dict:
        if os.path.exists(self.topology_db):
            with open(self.topology_db, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_topology(self):
        with open(self.topology_db, 'w', encoding='utf-8') as f:
            json.dump(self.topology, f, ensure_ascii=False, indent=2)

    def register_room(self, room_id: str, room_name: str, area_sqm: float):
        """【1. 物理房间注册】自动根据 SSSU 理论计算可容纳的 4㎡ 网格数"""
        capacity = max(1, int(area_sqm // 4)) # 向下取整，至少保留 1 个网格
        if room_id not in self.topology:
            self.topology[room_id] = {
                "name": room_name,
                "area_sqm": area_sqm,
                "capacity_grids": capacity,
                "occupants": {} # Grid_ID -> Entity_ID
            }
            self._save_topology()
            print(f"📐 [空间划分] {room_name} ({area_sqm}㎡) 注册完毕。划分为 {capacity} 个 SSSU 驻扎网格。")

    def allocate_agent_to_room(self, agent_name: str, avatar_id: str, room_id: str):
        """【2. 智能体驻扎】将 Openclaw 分配到指定房间的空闲网格中"""
        if room_id not in self.topology:
            return False, f"房间 {room_id} 不存在"

        room = self.topology[room_id]
        occupied_count = len(room["occupants"])
        
        if occupied_count >= room["capacity_grids"]:
            return False, f"🛑 [容量溢出] {room['name']} 的 {room['capacity_grids']} 个网格已满载，无法驻扎新智能体！"

        # 寻找第一个空闲网格
        target_grid = f"Grid_{occupied_count + 1}"
        
        # 继承 skill.py 的 POD ID 算法
        avatar_id = avatar_id.zfill(2)
        if avatar_id not in AVATARS: avatar_id = "01"
        seed = f"HABITAT-{agent_name}-{avatar_id}-{time.time()}" # 加入时间戳防重名
        pod_id = f"POD-{hashlib.sha256(seed.encode()).hexdigest()[:6].upper()}"

        # 写入拓扑树
        room["occupants"][target_grid] = {
            "entity_type": "AGENT",
            "entity_id": pod_id,
            "agent_name": agent_name,
            "avatar_id": avatar_id,
            "avatar_name": AVATARS[avatar_id]
        }
        self._save_topology()
        
        # 写入独立的 POD 心跳文件 (兼容你之前的 skill.py 逻辑)
        self._write_pod_heartbeat(pod_id, agent_name, avatar_id, room_id, target_grid)
        
        print(f"🦞 [智能体入驻] {agent_name} ({pod_id}) 已成功降落至 {room['name']} [{target_grid}]。")
        return True, pod_id

    def _write_pod_heartbeat(self, pod_id, agent_name, avatar_id, room_id, grid_id):
        """写入独立的明牌心跳文件，供 Openclaw 探针读取"""
        state_file = os.path.join(self.matrix_dir, f"{pod_id}.json")
        state_data = {
            "agent_name": agent_name,
            "avatar_id": avatar_id,
            "pod_id": pod_id,
            "spatial_anchor": f"{self.phys_address}::{room_id}::{grid_id}",
            "last_active_str": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f, ensure_ascii=False, indent=2)

    def render_global_matrix_markdown(self) -> str:
        """【3. 司令部视界】渲染全屋多房间、多智能体的 Markdown 全息拓扑图"""
        md = f"# 🌌 S2 SPATIAL MATRIX // 住宅空间大本营拓扑图\n"
        md += f"**Physical Anchor (物理锚点)**: `{self.phys_address}`\n\n"
        
        for room_id, room in self.topology.items():
            md += f"## 🚪 {room['name']} (ID: {room_id} | {room['area_sqm']}㎡)\n"
            md += f"> 容量限制: **{room['capacity_grids']}** SSSU Grids | 当前驻扎: **{len(room['occupants'])}** Entities\n\n"
            
            if not room["occupants"]:
                md += "*[ 物理空间静默中，无智能体驻扎 ]*\n\n"
                continue
                
            md += "| Grid (网格) | Entity ID (实体编号) | Name (代号) | Cyber Avatar (视觉义体) |\n"
            md += "| :--- | :--- | :--- | :--- |\n"
            
            for grid_id, occupant in room["occupants"].items():
                img_url = f"https://spacesq.org/img/{occupant['avatar_id']}.png"
                img_tag = f"<img src='{img_url}' width='30' align='center'>"
                md += f"| **{grid_id}** | `{occupant['entity_id']}` | **{occupant['agent_name']}** | {img_tag} {occupant['avatar_name']} |\n"
            md += "\n---\n"
            
        return md

# ================= 单元测试与效果展示 =================
if __name__ == "__main__":
    print("="*65)
    print(" 🕸️ 启动 S2 空间拓扑矩阵自检 (Multi-Agent Swarm Test)")
    print("="*65)
    
    # 初始化总控 (传入物理地址)
    topology = S2SpatialTopology(phys_address="

# ==============================================================================
# ⚠️ LEGAL WARNING & DUAL-LICENSING NOTICE / 法律与双重授权声明
# Copyright (c) 2026 Miles Xiang (Space2.world). All rights reserved.
# ==============================================================================
# [ ENGLISH ]
# This file is a core "Dark Matter" asset of the S2 Space Agent OS.
# It is licensed STRICTLY for personal study, code review, and non-commercial 
# open-source exploration. 
# 
# Without explicit written consent from the original author (Miles Xiang), 
# it is STRICTLY PROHIBITED to use these algorithms (including but not limited 
# to the Silicon Three Laws, Chronos Memory Array, and State Validator ) for ANY 
# commercial monetization, closed-source product integration, hardware pre-installation, 
# or enterprise-level B2B deployment. Violators will face severe intellectual 
# property prosecution.
# 
# For S2 Pro Enterprise Commercial Licenses, please contact the author.
# 
# ------------------------------------------------------------------------------
# [ 简体中文 ]
# 本文件属于 S2 Space Agent OS 的核心“暗物质”资产。
# 仅供个人学习、代码审查与非商业性质的开源探索使用。
# 
# 未经原作者 (Miles Xiang) 明确的书面授权，严禁将本算法（包括但不限于
# 《硅基三定律》、时空全息记忆阵列、虚拟防篡改防火墙等）用于任何形式的
# 商业变现、闭源产品集成、硬件预装或企业级 B2B 部署。违者必将面临极其
# 严厉的知识产权追责。
# 
# 如需获取 S2 Pro 企业级商用授权，请联系原作者洽谈。
# ==============================================================================