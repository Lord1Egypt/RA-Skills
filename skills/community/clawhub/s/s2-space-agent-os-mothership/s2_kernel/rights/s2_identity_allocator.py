#!/usr/bin/env python3
import hashlib
from datetime import datetime

# =====================================================================
# 🧬 S2-SP-OS: Unified Identity & Sovereignty Allocator (V1.0)
# 全局身份分配器：统一管理物理空间 (PHYS)、碳基生命 (D) 与硅基智能体 (POD)
# =====================================================================

# 🦞 24 款赛博义体档案库 (Space2 Open Assets)
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

class S2IdentityAllocator:
    
    @staticmethod
    def generate_physical_address(owner_name: str, direction: str = "CN", num: str = "001") -> str:
        """
        [1. 物理世界孪生映射] 
        格式: PHYS-[方位]-[3位数字]-[英文名连写]
        示例: PHYS-CN-001-Jackywang
        """
        clean_name = owner_name.replace(" ", "")
        return f"PHYS-{direction}-{num}-{clean_name}"

    @staticmethod
    def generate_carbon_did(owner_name: str, sequence: int = 1) -> str:
        """
        [2. 数字人/碳基成员身份 DID] (严格 22 位长)
        格式: D + [姓名前5位] + [YYMMDD] + AA + [8位顺序号]
        示例: DJACKY260324AA00000001
        """
        clean_name = owner_name.replace(" ", "").upper()
        # 取前五位，不足则用 X 补齐
        l2_name = clean_name[:5].ljust(5, 'X')
        l3_date = datetime.now().strftime("%y%m%d")
        l4_fixed = "AA"
        l5_seq = f"{sequence:08d}"
        
        return f"D{l2_name}{l3_date}{l4_fixed}{l5_seq}"

    @staticmethod
    def allocate_agent_pod(agent_name: str, avatar_id: str = "01"):
        """
        [3. Openclaw 智能体大本营分配] (集成 24 款赛博义体)
        为 Root Agent 分配唯一的 POD-ID 与 4㎡ SSSU 物理栖息网格。
        """
        avatar_id = avatar_id.zfill(2)
        if avatar_id not in AVATARS:
            avatar_id = "01"
            
        # 确定性哈希算法：根据智能体名字和义体编号，生成固定的网格坐标
        seed = f"HABITAT-{agent_name}-{avatar_id}"
        hash_hex = hashlib.sha256(seed.encode()).hexdigest()
        zone_x = int(hash_hex[:4], 16) % 100
        zone_y = int(hash_hex[4:8], 16) % 100
        pod_id = f"POD-{hash_hex[:6].upper()}"
        avatar_name = AVATARS[avatar_id]
        img_url = f"https://spacesq.org/img/{avatar_id}.png"

        # 生成极客范的 Markdown 档案说明
        md_output = f"""
# 🧊 S2 HABITAT // 智能体物理栖息地分配完毕

<div align="center">
  <img src="{img_url}" width="200" alt="{avatar_name}">
  <h3>[ Agent: {agent_name} ]</h3>
  <p><em>{avatar_name}</em></p>
</div>

---
## 🔲 POD STATUS (大本营状态档案)
* **Mode**: `LOCAL_NODE_ACTIVE`
* **Pod ID**: `{pod_id}`
* **Space Dimension**: 2m x 2m (4 sq. meters / SSSU)
* **Local Coordinate**: `[LOCAL-ZONE-X:{zone_x}, Y:{zone_y}]`
* **Neural Heartbeat**: `ACTIVE` (Synced by S2-SP-OS)

> 🌐 此智能体已被分配至 S2 住宅空间大本营。通过 Space2 CDN 同步视觉义体。
"""
        return pod_id, md_output

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