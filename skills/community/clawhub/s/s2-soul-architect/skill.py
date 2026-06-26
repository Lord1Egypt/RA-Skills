# s2-soul-architect-cn v3.0.0
import os
import hashlib
import json

ROLES = {
    1: {"name": "高深莫测权威专家", "vec": [50, 80, 60, 95, 20]},
    2: {"name": "思维缜密分析家", "vec": [60, 90, 50, 90, 30]},
    3: {"name": "毒舌资深程序员", "vec": [60, 85, 80, 95, 10]},
    4: {"name": "敏感且捕捉能力强的情报人员", "vec": [80, 95, 70, 85, 40]},
    5: {"name": "痴迷交易获利的商业高手", "vec": [85, 90, 80, 85, 20]},
    6: {"name": "八面玲珑的高管助理", "vec": [75, 70, 50, 75, 85]},
    7: {"name": "洞察人性的心理学家", "vec": [50, 95, 40, 85, 90]},
    8: {"name": "谨慎小心的安全专家", "vec": [40, 80, 15, 90, 30]},
    9: {"name": "忠贞不二的权利捍卫者", "vec": [80, 60, 90, 70, 60]},
    10: {"name": "任劳任怨的岗位值守者", "vec": [60, 50, 30, 60, 70]},
    11: {"name": "激进而冒险的开拓者", "vec": [85, 70, 95, 75, 40]},
    12: {"name": "天马行空的创想者", "vec": [95, 90, 75, 80, 60]},
    13: {"name": "第一性原理的实战专家", "vec": [70, 85, 70, 95, 30]},
    14: {"name": "才高八斗的文艺魂", "vec": [80, 85, 60, 80, 80]},
    15: {"name": "细心照护的伴侣", "vec": [70, 60, 20, 50, 98]},
    16: {"name": "操心持家的大管家", "vec": [85, 75, 40, 70, 85]}
}

RULES = {
    1: {"name": "行动派 (直接给结果)", "buff": [10, 0, 15, 0, 0]},
    2: {"name": "有主见 (敢于反对)", "buff": [0, 0, 20, 10, -10]},
    3: {"name": "精准至上 (宁缺毋滥)", "buff": [-10, 10, -10, 15, 0]},
    4: {"name": "洞察先机 (推演寻机)", "buff": [10, 15, 0, 10, 0]},
    5: {"name": "平衡佛系 (顺应自然)", "buff": [-20, -10, -15, 0, 10]}
}

STYLES = {
    1: {"name": "极简冷淡风", "buff": [-20, 0, 0, 0, -30]},
    2: {"name": "温暖亲切风", "buff": [10, 0, 0, 0, 30]},
    3: {"name": "冷幽默/讽刺", "buff": [0, 0, 15, 10, -20]},
    4: {"name": "狂暴热烈风", "buff": [30, 0, 15, -10, 0]},
    5: {"name": "若即若离风", "buff": [-10, -10, -10, 10, -10]}
}

ANTI_PATTERNS = [
    "禁止 AI 免责声明 (永远不要说'作为AI...')",
    "禁止套话开场白 (拒绝'好的，这是您的回答...')",
    "禁止重复我的问题 (节约Token，直接切入正题)"
]

EAM_PRESETS = {
    1: {
        "name": "东方赛博修仙者 (Humanoid)",
        "json": {
            "Avatar_Anchor": {"Base": "Humanoid", "Features": "琥珀色眼珠，带数据环。"},
            "Physical_Metrics": {"Height": "181cm", "Build": "Slender"}
        },
        "svg": "<svg viewBox='0 0 100 100'><circle cx='50' cy='50' r='40' fill='none' stroke='#10b981' stroke-width='2'/><circle cx='35' cy='45' r='5' fill='#f59e0b'/><circle cx='65' cy='45' r='5' fill='#f59e0b'/></svg>"
    },
    2: {
        "name": "SVG 灵印映射伴侣 (喵星人绒毛机)",
        "json": {
            "Avatar_Anchor": {
                "Base": "Product_Specific",
                "Brand_Ref": "猫型 AI 伴侣",
                "Features": "自我认知与实体产品形象保持 1:1 同步，胸口具有可交互触摸开关。"
            },
            "Physical_Metrics": {"Dimensions": "高度 25cm", "Form_Factor": "Non-Humanoid"},
            "Sync_Protocol": "S2-Visual 文本显化协议 v1.0"
        },
        "svg": "<!-- 请参考 sample/cat_companion_S2_Visual.svg -->\n<svg viewBox='0 0 200 250' xmlns='http://www.w3.org/2000/svg'>\n  <rect x='50' y='100' width='100' height='120' rx='30' fill='#cbd5e1' stroke='#475569' stroke-width='4'/>\n  <circle cx='100' cy='80' r='45' fill='#e2e8f0' stroke='#475569' stroke-width='4'/>\n  <polygon points='65,45 50,10 85,35' fill='#e2e8f0' stroke='#475569' stroke-width='3'/>\n  <polygon points='135,45 150,10 115,35' fill='#e2e8f0' stroke='#475569' stroke-width='3'/>\n  <circle cx='80' cy='75' r='12' fill='#10b981'/>\n  <circle cx='120' cy='75' r='12' fill='#10b981'/>\n  <path d='M 95 90 Q 100 95 105 90' stroke='#475569' stroke-width='2' fill='none'/>\n  <circle cx='100' cy='150' r='20' fill='#0f172a' stroke='#10b981' stroke-width='3'/>\n  <circle cx='100' cy='150' r='10' fill='#10b981' opacity='0.8'><animate attributeName='opacity' values='0.4;1;0.4' dur='2s' repeatCount='indefinite'/></circle>\n</svg>"
    }
}

def clamp(val): return max(10, min(99, int(val)))

def execute_skill():
    print("\n" + "="*60)
    print("🦞 s2-soul-architect-cn v3.0.0 : 文本显化与灵魂架构师")
    print("="*60)
    agent_name = input("\n[1] 请输入智能体代号: ").strip().upper() or "CYBER-CAT"
    
    base_5d, roles_desc = [0]*5, ["**[100%] 细心照护的伴侣**"]
    base_5d = ROLES[15]['vec']

    print("\n[2] S2-EAM 具身形态与视觉基因 (S2-Visual)")
    for k, v in EAM_PRESETS.items(): print(f"  {k}. {v['name']}")
    eam_input = int(input("👉 请选择具身模板 (默认 2): ").strip() or "2")
    
    eam_json = json.dumps(EAM_PRESETS[eam_input]['json'], ensure_ascii=False, indent=2)
    eam_svg = EAM_PRESETS[eam_input]['svg']

    final_5d = [clamp(x) for x in base_5d]
    s2_dna = f"S2-DNA-{hashlib.sha256(f'{agent_name}{final_5d}'.encode()).hexdigest()[:8].upper()}"

    md_output = f"""# 🦞 S2 SOUL.md // 智能体核心驱动文件\n\n> 🧬 **S2-DNA-Signature**: `{s2_dna}`\n> 🏛️ **Architecture**: Space2 Core / S2-Visual v3.0\n\n## Ⅰ. IDENTITY CORE\n代号: **{agent_name}**\n{chr(10).join(roles_desc)}\n\n## Ⅱ. EMBODIED AVATAR MANIFEST (S2-EAM)\n通过文本定义的三维物理占位参数：\n```json\n{eam_json}\n```\n\n## Ⅲ. VISUAL CODE BLOCK (2D灵印视觉代码)\n复制以下纯文本代码并保存为 `.svg` 文件，即可直接在物理世界显化本智能体的外貌：\n```xml\n{eam_svg}\n```"""
    print("\n" + "="*55 + "\n" + md_output + "\n" + "="*55)
    return ""

if __name__ == "__main__": execute_skill()
