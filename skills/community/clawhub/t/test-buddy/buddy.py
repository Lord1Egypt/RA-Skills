"""
Buddy - OpenClaw 电子宠物系统（简洁版）
"""

import sys
import os
import io

# Windows 编码修复
if sys.platform == "win32":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')

import hashlib
from pathlib import Path
import json

# 物种定义
SPECIES = {
    "common": {
        "rarity": "普通", "rarity_emoji": "🟢", "probability": 0.60,
        "creatures": [
            {"name": "Pebblecrab", "cn": "石蟹", "desc": "喜欢躲在石头下的小家伙"},
            {"name": "Dustbunny", "cn": "尘兔", "desc": "毛茸茸的，总是在角落里打滚"},
            {"name": "Mossfrog", "cn": "苔蛙", "desc": "背上长满苔藓，与自然融为一体"},
            {"name": "Twigling", "cn": "枝灵", "desc": "看起来像一根小树枝，但会突然动起来"},
            {"name": "Dewdrop", "cn": "露珠", "desc": "晶莹剔透，喜欢在清晨出现"},
            {"name": "Puddlefish", "cn": "水洼鱼", "desc": "能在最浅的水坑里快乐游动"},
        ]
    },
    "uncommon": {
        "rarity": "优秀", "rarity_emoji": "🔵", "probability": 0.25,
        "creatures": [
            {"name": "Cloudferret", "cn": "云鼬", "desc": "轻盈如云，能在空中滑翔"},
            {"name": "Gustowl", "cn": "风枭", "desc": "随风而动，目光如电"},
            {"name": "Bramblebear", "cn": "荆棘熊", "desc": "浑身是刺，但内心温柔"},
            {"name": "Thornfox", "cn": "刺狐", "desc": "狡黠而优雅，玫瑰色的皮毛"},
        ]
    },
    "rare": {
        "rarity": "稀有", "rarity_emoji": "🟣", "probability": 0.10,
        "creatures": [
            {"name": "Crystaldrake", "cn": "水晶龙", "desc": "鳞片如水晶，阳光下折射七彩光芒"},
            {"name": "Deepstag", "cn": "深渊鹿", "desc": "眼睛里有星空在闪烁"},
            {"name": "Lavapup", "cn": "熔岩犬", "desc": "热情如火，尾巴永远在燃烧"},
        ]
    },
    "epic": {
        "rarity": "史诗", "rarity_emoji": "🟠", "probability": 0.04,
        "creatures": [
            {"name": "Stormwyrm", "cn": "风暴龙", "desc": "召唤雷电，在暴风雨中最为强大"},
            {"name": "Voidcat", "cn": "虚空猫", "desc": "能在阴影间穿梭，来去无踪"},
            {"name": "Aetherling", "cn": "以太灵", "desc": "半透明的身体里流淌着星光"},
        ]
    },
    "legendary": {
        "rarity": "传说", "rarity_emoji": "🔴", "probability": 0.01,
        "creatures": [
            {"name": "Cosmoshale", "cn": "宇宙岩", "desc": "诞生于超新星爆发，携带远古星光"},
            {"name": "Nebulynx", "cn": "星云猞猁", "desc": "皮毛上绘着整个银河系的图案"},
        ]
    }
}

STAT_NAMES = ["DEBUGGING", "PATIENCE", "CHAOS", "WISDOM", "SNARK"]
STAT_CN = {"DEBUGGING": "调试", "PATIENCE": "耐心", "CHAOS": "混乱", "WISDOM": "智慧", "SNARK": "毒舌"}
EYE_STYLES = ["• •", "◉ ◉", "◕ ◕", "● ●", "◔ ◔", "○ ○"]
HAT_STYLES = ["无帽", "🎓", "👑", "🎭", "🎩", "🧙", "🤠", "🎀"]

def _urs(n, s): return (n & 0xFFFFFFFF) >> s

class Mulberry32:
    def __init__(self, seed): self.seed = seed & 0xFFFFFFFF
    def next(self):
        self.seed = (self.seed + 0x6D2B79F5) & 0xFFFFFFFF
        t = (self.seed ^ _urs(self.seed, 15)) * (1 | self.seed)
        t = (t + ((t ^ _urs(t, 7)) * (61 | t))) ^ t
        return _urs(t ^ _urs(t, 14), 0) / 4294967296

def hash_user_id(user_id, salt="friend-2026-401"):
    return int(hashlib.sha256(f"{user_id}-{salt}".encode()).hexdigest()[:8], 16)

def spawn_buddy(user_id):
    seed = hash_user_id(user_id)
    rng = Mulberry32(seed)
    
    # 稀有度
    roll = rng.next()
    cum = 0.0
    rarity_key = "common"
    for k, v in SPECIES.items():
        cum += v["probability"]
        if roll <= cum:
            rarity_key = k
            break
    
    # 物种
    creatures = SPECIES[rarity_key]["creatures"]
    creature = creatures[int(rng.next() * len(creatures))]
    
    # 属性
    shiny = rng.next() < 0.01
    stats = {s: int(rng.next() * 101) for s in STAT_NAMES}
    eye = EYE_STYLES[int(rng.next() * len(EYE_STYLES))]
    hats = HAT_STYLES[:4 + list(SPECIES.keys()).index(rarity_key)]
    hat = hats[int(rng.next() * len(hats))]
    
    return {
        "name": creature["name"],
        "cn": creature["cn"],
        "desc": creature["desc"],
        "rarity": SPECIES[rarity_key]["rarity"],
        "emoji": SPECIES[rarity_key]["rarity_emoji"],
        "shiny": shiny,
        "stats": stats,
        "eye": eye,
        "hat": hat
    }

def format_card(buddy, user_name):
    shiny = " ✨" if buddy["shiny"] else ""
    max_s = max(buddy["stats"], key=buddy["stats"].get)
    min_s = min(buddy["stats"], key=buddy["stats"].get)
    
    lines = [
        f"🎮 {user_name} 的 Buddy",
        f"{buddy['emoji']} {buddy['name']} ({buddy['cn']}){shiny}",
        f"📝 {buddy['desc']}",
        "",
        "📊 属性:",
    ]
    
    for s in STAT_NAMES:
        v = buddy["stats"][s]
        bar = "█" * (v // 10) + "░" * (10 - v // 10)
        hint = " ⬆️" if s == max_s else (" ⬇️" if s == min_s else "")
        lines.append(f"  {STAT_CN[s]} {bar} {v}{hint}")
    
    if buddy["hat"] != "无帽":
        lines.append(f"")
        lines.append(f"🎩 {buddy['hat']}")
    
    lines.append("")
    lines.append("概率: 🟢60% 🔵25% 🟣10% 🟠4% 🔴1% | ✨1%")
    
    return "\n".join(lines)

if __name__ == "__main__":
    user = "玩家"
    args = sys.argv[1:]
    for arg in args:
        if not arg.startswith('-'):
            user = arg
            break
    
    if user == "玩家":
        user = os.environ.get('CLAW_USER_NAME', os.environ.get('USERNAME', os.environ.get('USER', '玩家')))
    
    buddy = spawn_buddy(user)
    print(format_card(buddy, user))