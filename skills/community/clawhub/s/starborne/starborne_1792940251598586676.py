#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
"""
STARBORNE v3 —— 星际数字废土拾荒模拟器 引擎
严格遵循 SKILL.md 的 v2 设计修订，并按 v3 经济重写：
  - 抽（单抽/十连）直接消耗「钱(Credits)」，不再依赖任何生命值/能量资源。
  - 开局赠启动资金；钱的唯一来源是出售装备；钱的唯一主要去向是抽。
  - 移除整个能量/补给/买/萃取系统（v3）：刷子游戏没有战斗，HP 是假资源。
v2 设计要点仍保留：六档改名 / 删垃圾库 / 删出图 / 三层 ID / 暗金模型 /
拆解全档（前三级空手）/ 升级 / 7 槽穿戴 / 材料合成 / 反作弊已移除 / 献祭已移除。
"""
import json
import os
import sys
import random
import time
import uuid

BASE = "/workspace/starborne"
STATE = os.path.join(BASE, "warehouse.json")

# ---------- 六档稀有度 (v2.1) ----------
# 名称已去"级"字；颜色沿用原六档（白/蓝/黄/橙/绿/紫）
TIERS = [
    {"name": "普通", "color": "⬜ 白", "prob": 0.50},
    {"name": "行星", "color": "🔵 蓝", "prob": 0.30},
    {"name": "帝国", "color": "🟡 黄", "prob": 0.13},
    {"name": "银河", "color": "🟠 橙", "prob": 0.05},
    {"name": "远古", "color": "🟢 绿", "prob": 0.015},
    {"name": "虚空", "color": "🟣 紫", "prob": 0.005},
]
TIER_NAME_TO_OBJ = {t["name"]: t for t in TIERS}
TIER_ORDER = ["虚空", "远古", "银河", "帝国", "行星", "普通"]  # 显示用，从高到低

# 实例ID档位前缀码（v3.2 带类别编码）
TIER_CODE = {"普通": "P", "行星": "B", "帝国": "E", "银河": "G", "远古": "A", "虚空": "V"}

# ---------- 词池 ----------
P1 = ["碎星的", "深渊的", "沙海的", "香料侵的", "虚空的", "虫巢的", "基地级",
      "流亡者的", "星舰级", "终结的", "伊克斯的", "柯拉尔的", "弗雷曼的", "哈克南的", "阿崔迪的"]
# P2 属性修饰池（7 槽通用，全混用，不按槽位专有化）。与 P4 高级属性词缀池零重叠。
P2 = ["脉冲", "量子", "蚀刻", "烈阳", "反物质", "辐射", "等离子", "神经", "幽视",
      "晶幕", "折射", "虫甲", "力场", "晶化", "熔铸", "相移", "沙暴",
      "冰晶", "流沙", "疾风", "反重力", "幽影", "幽能", "折叠", "虚空",
      "共振", "寒霜", "赤红", "裂变"]
# P4 高级属性词缀池（14）—— 原始规则保留，仅供远古/虚空档作高级前缀（P4+P1+P2+P3），
# 不进入 P2 公共池。当前随机档不实际生成 P4（远古/虚空走固定暗金名），但词池保留于此。
P4_HIGH = ["永恒", "湮灭", "星核", "超载", "共鸣", "觉醒", "创世", "灭世", "浩劫",
           "禁忌", "无限", "超维", "宿命", "涅槃"]
JUNK_FULL = ["损坏推进器", "废弃控制板", "腐蚀线圈", "老化外壳", "裂纹护罩", "锈蚀齿轮",
             "断裂光纤", "残留反应堆", "破碎舱门", "裂变电池"]
# 注：P4 高级属性词缀池见上方 P4_HIGH，保留供远古/虚空档高级前缀，与 P2 不重叠。

# ---------- 装备槽 + 基础模板 (② 基础类别模板) ----------
SLOT_TEMPLATES = {
    "武器": ["震击枪", "晶牙匕首", "激光枪", "休眠枪", "弹射枪", "能量刃", "轨道炮",
            "风暴弩", "噬骨弩", "灰烬喷射器", "沙雷发射器", "引力爪", "碎骨锤",
            "寒霜枪", "静刃", "攻击之爪", "科勒匕首", "风暴战锤", "萨满之矛",
            "食人魔斧", "火焰之球", "闪电之球", "腐蚀之球", "黑暗之球",
            "霜冻之球", "毒液之球", "C-14高斯步枪", "阿克莱特冲击炮", "聚变切割器",
            "喷火枪", "双管机炮", "导弹枪", "U-238贫铀弹", "灵能刃"],
    "头部": ["作战头盔", "蒸馏面罩", "晶视目镜", "沙暴风镜", "指挥头冠","王者之冠","索比面具",
            "导引盔", "潜行罩", "符文头盔", "战术盔", "死亡面罩", "深空盔"],
    "铠甲": ["作战护甲", "外骨骼", "重型护盾", "蒸馏服", "晶甲", "战地披风", "潜行装",
            "动力甲", "卫戍板甲", "深空服", "符文胸甲", "碎星甲", "静默甲", "熔岩甲",
            "法师长袍", "马克V战斗服", "新钢铁装甲", "泰坦反应堆甲",
            "几丁质装甲", "虫族甲壳"],
    "足部": ["沙行靴", "疾行靴", "深空靴", "攀爬爪靴", "晶履", "潜行软鞋", "战地军靴",
            "引力靴", "烈风靴", "潜行足具", "熔岩靴", "寒霜履", "速度之靴"],
    "腰部": ["悬浮腰带", "晶核腰带", "弹药腰带", "工具护腰", "战术腰带",
            "符文腰带", "引力护腰", "潜行护腰", "巨人力量腰带"],
    "饰品": ["轨道戒指", "香料探测器", "晶石吊坠", "神经吊坠", "星图罗盘", "符文指环", "静默徽章",
            "绯红珠", "霜纹戒", "摄魂铃", "幽冥石", "铁铭牌", "幽光羽", "星辉盘",
            "香料囊", "命纹石", "蒸馏瓶", "加速手套", "回复指环", 
            "凯达琳水晶", "灵能发射器", "圣物"],
    "特殊": ["悬浮战车", "护盾发生器", "跃迁核心", "遗迹数据板", "扑翼机", "蒸馏帐篷",
            "屏蔽场发生器", "宇航公会信标", "晶能电池", "引力锚", "浮空艇",
            "符文石碑", "寒霜冰棺", "风暴罗盘", "等离子护盾", "引力引擎"],
}
SLOTS = list(SLOT_TEMPLATES.keys())

# 实例ID槽位前缀码（v3.2 带类别编码）
SLOT_CODE = {"武器": "WPN", "头部": "HD", "铠甲": "BD", "足部": "FT", "腰部": "WT",
             "饰品": "AC", "特殊": "SP", "杂物": "JD"}

# ---------- 暗金模板 (③ 暗金模板ID) ----------
# 远古 roster（暗黑式固定名暗金，v2.5 / v2.10 待定项已补默认 12 件）
UNIQUE_ROSTER = {
    "A01": {"name": "沙皇裂解者", "en": "Sand Emperor's Cleaver", "slot": "武器", "flavor": "撕裂沙海的远古巨兵，刃过之处星舰断成两截。"},
    "A02": {"name": "静默之牙", "en": "Silent Fang", "slot": "武器", "flavor": "无声斩落，连警报都来不及响起。"},
    "A03": {"name": "预言者面甲", "en": "Seer's Visage", "slot": "头部", "flavor": "据说戴上的瞬间能听见沙虫的心跳。"},
    "A04": {"name": "不灭虫壳", "en": "Undying Carapace", "slot": "铠甲", "flavor": "取自沙虫始祖的甲，弹孔会自己愈合。"},
    "A05": {"name": "流沙圣袍", "en": "Quicksand Vestment", "slot": "铠甲", "flavor": "移动时如沙流裹身，射线擦过便被吞没。"},
    "A06": {"name": "风行沙靴", "en": "Windstrider Boots", "slot": "足部", "flavor": "踏沙无痕，追兵只看见远去的尘柱。"},
    "A07": {"name": "星髓束带", "en": "Starcore Belt", "slot": "腰部", "flavor": "束带上嵌着一小块坍缩的星核，暖意灼人。"},
    "A08": {"name": "虚空低语护符", "en": "Voidwhisper Charm", "slot": "饰品", "flavor": "贴近耳边，能听见宇宙诞生前的寂静。"},
    "A09": {"name": "双月戒指", "en": "Twin Moon Ring", "slot": "饰品", "flavor": "两枚月牙相扣，映出弗雷曼的双轮夜空。"},
    "A10": {"name": "香料先知罗盘", "en": "Spice Oracle Compass", "slot": "饰品", "flavor": "指针永远指向你最想逃离的方向。"},
    "A11": {"name": "远古星舰核心", "en": "Elder Starship Core", "slot": "特殊", "flavor": "比帝国还老的引擎之心，仍在低频脉动。"},
    "A12": {"name": "湮灭力场", "en": "Annihilation Field", "slot": "特殊", "flavor": "展开后方圆十米，连光都被压成尘埃。"},
}
# 虚空（仅 2 件固定专属，原 99536/99537，降级为 ③ 暗金模板ID）
VOID_ITEMS = {
    "99536": {"name": "阿拉基恩虚空爪", "en": "Arrakeen's Voidclaw", "slot": "武器",
              "flavor": "太初之虚凝成的利爪，握之则万物归于静默。"},
    "99537": {"name": '弗雷曼无女剑 - "Maidenless"', "en": 'Fremen Hollow Blade - "Maidenless"', "slot": "武器",
              "flavor": "无主之刃，剑身空无一物，却比任何实体都重。"},
}

# ---------- 材料 ----------
MATERIAL_KEYS = ["星尘结晶", "太古原石", "Gem of the Space", "Mirror of the Void"]

# ---------- 经济：抽的花费 & 卖价 (v3) ----------
# 抽直接花「钱(Credits)」；卖价是钱的主要来源；开局赠 START_MONEY 启动。
# 数值设计：单抽10/十连90；一件掉落平均卖≈9钱，十连10件≈89 ≈ 成本90。
# 即全卖掉刚好持平，但玩家必留好货（银河+不卖），故实际净消耗 → 钱驱动取舍。
START_MONEY = 300
SINGLE_COST = 5
TEN_COST = 45
SHEEP_PER_MONEY = 5          # v3.1 数羊：每数 5 只羊 = 1 钱（基础产出）
SHEEP_BONUS_PER_100 = 30     # 数羊里程碑奖励：每满 100 只额外 +30 钱（数 100 只 = 20基础 + 30 = 50 钱）
SELL_PRICE = {"普通": 2, "行星": 5, "帝国": 15, "银河": 50, "远古": 50, "虚空": 50}

# ---------- 升级消耗 (v2.8) ----------
UPGRADE_COST = {
    "普通": "星尘结晶",
    "行星": "星尘结晶",
    "帝国": "星尘结晶",
    "银河": "太古原石",
    "远古": "VOID_MAT",  # 升虚空需 1 个虚空材料（Gem 或 Mirror 任一）
}


# ---------- 名称生成（随机档：名字由词池决定，与实例ID无关）----------
def _pick_modifier(rng, base):
    for _ in range(12):
        m = rng.choice(P2)
        # 冲突规避：修饰首字不与基础名首字相同（避免「脉冲脉冲步枪」式叠字），
        # 且修饰词不埋在基础名中（避免双重修饰）。
        if m[0] != base[0] and m not in base:
            return m
    return rng.choice(P2)


def roll_random_name(rng, tier, slot, base):
    # 按档位分流命名段数（回归 SKILL.md 原始分级）：
    #   普通/行星 → 两段（P1前缀 + 基础），破烂本就该短
    #   帝国/银河 → 三段（P1前缀 + P2修饰 + 基础），开始隆重
    #   远古/虚空 → 不走本函数，取固定暗金名
    if tier == "普通" and rng.random() < 0.13:
        return rng.choice(JUNK_FULL), "杂物"
    p1 = rng.choice(P1)
    if tier in ("帝国", "银河"):
        name = p1 + _pick_modifier(rng, base) + base   # 三段
    else:                                              # 普通、行星：两段
        name = p1 + base
    return name, slot


# ---------- 状态读写 ----------
def default_state():
    return {
        "warehouse": [],        # 六档全部进货舱（v2.2 删垃圾库）
        "materials": {k: 0 for k in MATERIAL_KEYS},
        "money": START_MONEY,   # 钱（Credits, v3）：开局赠启动资金
    }


_B36 = "0123456789abcdefghijklmnopqrstuvwxyz"
def _b36(n):
    if n <= 0:
        return "0"
    s = ""
    while n:
        s = _B36[n % 36] + s
        n //= 36
    return s


def load_state():
    if os.path.exists(STATE):
        with open(STATE, "r", encoding="utf-8") as f:
            s = json.load(f)
        s.pop("next_seq", None)   # v3.2 清理遗留计数器字段（已不再使用，避免误导/误改）
        for k, v in default_state().items():
            if k not in s:
                s[k] = v
    else:
        s = default_state()
    return s


def save_state(s):
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(s, f, ensure_ascii=False, indent=2)


# ---------- 掉落逻辑 ----------
def pick_tier(r):
    acc = 0.0
    for t in TIERS:
        acc += t["prob"]
        if r < acc:
            return t["name"]
    return TIERS[-1]["name"]


def do_one_drop(s, master_seed=None):
    """真实随机掉落。先按概率定档 → 发唯一ID(时间戳+UUID短码, 去中心化) → 套模板生成。"""
    if master_seed is None:
        master_seed = random.getrandbits(64)
    rng = random.Random(master_seed)
    tier = pick_tier(rng.random())
    tcode = TIER_CODE[tier]
    uid = uuid.uuid4().hex                       # 底层绝对唯一键，不依赖任何计数器
    ts = _b36(int(time.time()))[-4:]             # 时间戳base36后4位：提供大致顺序/进度感
    suffix = ts + uid[:4]                         # 展示后缀 = 时间戳 + UUID短码（即使同秒也不撞）

    if tier in ("普通", "行星", "帝国", "银河"):
        slot = rng.choice(SLOTS)
        base = rng.choice(SLOT_TEMPLATES[slot])
        name, slot = roll_random_name(rng, tier, slot, base)
        iid = f"{tcode}-{SLOT_CODE.get(slot, 'XX')}-{suffix}"
        item = {"uid": uid, "iid": iid, "tier": tier, "slot": slot, "base": base, "name": name,
                "en": None, "unique": False, "template_id": None, "flavor": None}
    elif tier == "远古":
        tid = rng.choice(list(UNIQUE_ROSTER.keys()))
        t = UNIQUE_ROSTER[tid]
        iid = f"{tcode}-{SLOT_CODE.get(t['slot'], 'XX')}-{suffix}"
        item = {"uid": uid, "iid": iid, "tier": "远古", "slot": t["slot"], "base": t["slot"] + "模板",
                "name": t["name"], "en": t["en"], "unique": True, "template_id": tid, "flavor": t["flavor"]}
    else:  # 虚空
        tid = rng.choice(list(VOID_ITEMS.keys()))
        t = VOID_ITEMS[tid]
        iid = f"{tcode}-{SLOT_CODE.get(t['slot'], 'XX')}-{suffix}"
        item = {"uid": uid, "iid": iid, "tier": "虚空", "slot": t["slot"], "base": t["slot"] + "模板",
                "name": t["name"], "en": t["en"], "unique": True, "template_id": tid, "flavor": t["flavor"]}

    s["warehouse"].append(item)

    # 材料自动掉落（对应等级材料，概率减半）
    mat_drop = None
    if tier == "银河" and rng.random() < 0.025:
        s["materials"]["星尘结晶"] += 1
        mat_drop = "星尘结晶"
    elif tier == "远古" and rng.random() < 0.0075:
        s["materials"]["太古原石"] += 1
        mat_drop = "太古原石"
    elif tier == "虚空" and rng.random() < 0.0025:
        k = rng.choice(["Gem of the Space", "Mirror of the Void"])
        s["materials"][k] += 1
        mat_drop = k

    return {"item": item, "tier": tier, "seed": master_seed, "mat_drop": mat_drop}


# ---------- 命令实现 ----------
def cmd_roll(s, n=1):
    cost = SINGLE_COST if n == 1 else TEN_COST
    if s["money"] < cost:
        return (f"⚠️ 钱不足（当前 {s['money']} 钱），无法执行"
                f"{'单抽' if n == 1 else '十连'}。需要 {cost} 钱。"
                f"把不要的装备卖掉换钱（卖 [实例ID]），或没钱就数羊（数羊 1 2 3… 逐只报数）。")
    s["money"] -= cost
    results = []
    for _ in range(n):
        r = do_one_drop(s)
        results.append(r)
    save_state(s)
    return format_drops(results)


def _name_str(it):
    if it["en"]:
        return f"**{it['name']}** （{it['en']}）"
    return it["name"]


def format_drops(results):
    lines = []
    for r in results:
        it = r["item"]
        t = TIER_NAME_TO_OBJ[r["tier"]]
        star = " 🌟" if it["unique"] else ""
        lines.append(f"{t['color']} {r['tier']}{star} → 实例 {it['iid']} · {_name_str(it)}")
        if it["unique"] and it["flavor"]:
            lines.append(f"   📜 {it['flavor']}")
        if r["mat_drop"]:
            lines.append(f"   💎 同时掉落材料：{r['mat_drop']}")
    return "\n".join(lines)


def cmd_status(s):
    mat = {k: v for k, v in s["materials"].items() if v > 0}
    mat_str = ", ".join(f"{k}×{v}" for k, v in mat.items()) if mat else "（无）"
    return (f"💰 钱（Credits）：{s['money']}（开局赠 {START_MONEY}）\n"
            f"📦 货舱装备：{len(s['warehouse'])} 件\n"
            f"🧪 材料：{mat_str}\n"
            f"💸 单抽 {SINGLE_COST} / 十连 {TEN_COST} 钱 ｜ 钱由出售装备获得")


def cmd_inventory(s):
    if not s["warehouse"]:
        return "货舱为空。去狂沙里挖点东西吧（单抽 / 十连）。"
    by_tier = {t: [] for t in TIER_ORDER}
    for it in s["warehouse"]:
        by_tier[it["tier"]].append(it)
    lines = ["🛰️ 货舱（按稀有度从高到低）："]
    for t in TIER_ORDER:
        items = by_tier.get(t)
        if not items:
            continue
        obj = TIER_NAME_TO_OBJ[t]
        for it in sorted(items, key=lambda x: x.get("iid", "")):
            star = " 🌟" if it["unique"] else ""
            lines.append(f"  {obj['color']} {t}{star} · {it['iid']} · {_name_str(it)}")
    lines.append(f"\n共 {len(s['warehouse'])} 件 ｜ 货舱等级：{cabin_name(s)}")
    return "\n".join(lines)


def cabin_name(s):
    if any(it["tier"] == "虚空" for it in s["warehouse"]):
        return "虚空母舰核心舱"
    if any(it["tier"] == "远古" for it in s["warehouse"]):
        return "宇宙遗迹舱"
    if any(it["tier"] == "银河" for it in s["warehouse"]):
        return "星际货舱"
    return "废弃货舱"


def find_item(s, token):
    # token 解析优先级：① 完整底层 uid(绝对唯一) ② 完整实例编码(iid) ③ 兼容旧存档纯序号 seq
    for it in s["warehouse"]:
        if it.get("uid") == token:
            return it
    for it in s["warehouse"]:
        if it.get("iid") == token:
            return it
    if isinstance(token, str) and token.isdigit():
        seq = int(token)
        for it in s["warehouse"]:
            if it.get("seq") == seq:
                return it
    return None


def cmd_delete(s, iid):
    it = find_item(s, iid)
    if not it:
        return f"未找到实例 {iid} 的装备。"
    s["warehouse"].remove(it)
    save_state(s)
    return f"已删除 {it['iid']}。"


def cmd_dismantle(s, iid):
    it = find_item(s, iid)
    if not it:
        return f"未找到实例 {iid} 的装备。"
    got = None
    if it["tier"] == "银河":
        s["materials"]["星尘结晶"] += 1
        got = "星尘结晶 ×1"
    elif it["tier"] == "远古":
        s["materials"]["太古原石"] += 1
        got = "太古原石 ×1"
    elif it["tier"] == "虚空":
        k = random.choice(["Gem of the Space", "Mirror of the Void"])
        s["materials"][k] += 1
        got = f"{k} ×1"
    # 前三级（普通/行星/帝国）拆 → 空手，不出材料（纯清理）
    s["warehouse"].remove(it)
    save_state(s)
    if got:
        return f"已拆解 {it['iid']}，获得 {got}。"
    return f"已拆解 {it['iid']}，空手而归（前三级不出材料）。"


def cmd_upgrade(s, iid):
    it = find_item(s, iid)
    if not it:
        return f"未找到实例 {iid} 的装备。"
    if it["unique"]:
        return f"{it['tier']} 为固定暗金（唯一），已是顶层，无法升级。"
    if it["tier"] not in UPGRADE_COST:
        return f"{it['tier']} 已是最高随机阶，无法继续升级。"
    dest = TIER_ORDER[TIER_ORDER.index(it["tier"]) - 1]  # TIER_ORDER 从高到低，故 -1 为更高阶
    mat = UPGRADE_COST[it["tier"]]
    if mat == "VOID_MAT":
        if s["materials"]["Gem of the Space"] <= 0 and s["materials"]["Mirror of the Void"] <= 0:
            return f"升级至 {dest} 需 1 个虚空材料（Gem of the Space 或 Mirror of the Void），当前不足。"
        if s["materials"]["Gem of the Space"] > 0:
            s["materials"]["Gem of the Space"] -= 1
        else:
            s["materials"]["Mirror of the Void"] -= 1
    else:
        if s["materials"][mat] <= 0:
            return f"升级至 {dest} 需要 1 个 {mat}，当前不足。"
        s["materials"][mat] -= 1
    # 升级：级别提升，名字/实例ID不变；升到的顶级仍是非固定唯一（v2.8）
    it["tier"] = dest
    save_state(s)
    return f"✨ 升级成功！实例 {it['iid']} 现为 {dest}（名称不变，仍为随机生成物）。"


def cmd_synth(s, a, b):
    if a == b == "星尘结晶":
        if s["materials"]["星尘结晶"] >= 2:
            s["materials"]["星尘结晶"] -= 2
            s["materials"]["太古原石"] += 1
            save_state(s)
            return "合成成功：2 星尘结晶 → 1 太古原石。"
        return "星尘结晶不足 2 个。"
    if a == b == "太古原石":
        if s["materials"]["太古原石"] >= 2:
            s["materials"]["太古原石"] -= 2
            k = random.choice(["Gem of the Space", "Mirror of the Void"])
            s["materials"][k] += 1
            save_state(s)
            return f"合成成功：2 太古原石 → 1 {k}。"
        return "太古原石不足 2 个。"
    return "合成仅支持：2 星尘结晶 → 太古原石；2 太古原石 → 虚空材料。"


def cmd_sell(s, iid):
    it = find_item(s, iid)
    if not it:
        return f"未找到实例 {iid} 的装备。"
    price = SELL_PRICE[it["tier"]]
    s["money"] += price
    s["warehouse"].remove(it)
    save_state(s)
    return f"已出售 {it['iid']}（{it['tier']}），获得 {price} 钱。"


def cmd_count(s, tokens):
    # 数羊严格模式：逐只报数，与自然数序列 1,2,3… 逐位比对，任一不符即违例，0 钱。
    # （漏的/重的/顺序错的/非整数，本质都是"某一位 ≠ 它该有的自然数"，一个判断全覆盖）
    if not tokens:
        return ("🐑 数羊须逐只报数，例如 `数羊 1 2 3 4 5`。"
                "数列须与自然数 1,2,3… 逐位一致（连续、不重复、不跳号）；"
                "任意一位对不上即违例，不给钱。")
    for i, t in enumerate(tokens, start=1):
        try:
            v = int(t)
        except ValueError:
            return f"🚫 违例：第 {i} 位『{t}』不是自然数，数羊作废，0 钱。"
        if v != i:
            return f"🚫 违例：第 {i} 位应为自然数 {i}，你报的是 {v}，数羊作废，0 钱。"
    n = len(tokens)  # 此时数列必为 [1, 2, ..., n]
    base = n // SHEEP_PER_MONEY
    milestones = n // 100
    bonus = milestones * SHEEP_BONUS_PER_100
    gained = base + bonus
    if gained <= 0:
        return (f"🐑 数了 {n} 只羊（1→{n} 连续无误），但还差 {SHEEP_PER_MONEY - n} 只才够 1 钱。"
                f"（每 {SHEEP_PER_MONEY} 只 = 1 钱；满 100 只额外奖 {SHEEP_BONUS_PER_100} 钱）")
    s["money"] += gained
    save_state(s)
    parts = [f"基础 {base} 钱（每{SHEEP_PER_MONEY}只1钱）"]
    if bonus:
        parts.append(f"满百奖励 +{bonus} 钱（数满 {milestones*100} 只）")
    return f"🐑 你数了 {n} 只羊（1→{n} 连续无误），{'; '.join(parts)}，共获得 {gained} 钱（当前 {s['money']} 钱）。"


def cmd_best(s):
    if not s["warehouse"]:
        return "货舱为空，暂无最强装备。"
    best = min(s["warehouse"], key=lambda x: TIER_ORDER.index(x["tier"]))
    return f"💪 最强装备：{TIER_NAME_TO_OBJ[best['tier']]['color']} {best['tier']} · {best['iid']} · {_name_str(best)}"


def cmd_clear(s, confirm=False):
    if not confirm:
        return f"⚠️ 确认清空货舱？当前 {len(s['warehouse'])} 件装备。再次输入 `清空货舱 确认` 执行。"
    s["warehouse"] = []
    save_state(s)
    return "已清空货舱。"


def cmd_rules():
    return (
        "📖 STARBORNE v3 规则手册\n"
        "【六档稀有度 & 概率】（颜色：白/蓝/黄/橙/绿/紫）\n"
        "  普通 50% ｜ 行星 30% ｜ 帝国 13% ｜ 银河 5% ｜ 远古 1.5% ｜ 虚空 0.5%\n"
        "【三层 ID 模型】\n"
        "  ① 实例ID：每次掉落新发、全局唯一，与名字无关\n"
        "  ② 基础类别模板：武器/头部/铠甲/足部/腰部/饰品/特殊（共 15 种）\n"
        "  ③ 暗金模板：远古名册(12) + 虚空(2, 原99536/99537)\n"
        "【生成】纯概率定档 → 发实例ID → 随机档滚词缀(P1+P2+基础)；暗金档取固定名\n"
        "【装备槽】7 槽：武器/头部/铠甲/足部/腰部/饰品/特殊（仅用于分类与实例ID槽位码，无任何数量限制）\n"
        "【经济·v3】抽直接花「钱(Credits)」：单抽 5 / 十连 45；开局赠 300 钱启动\n"
        "  卖价：普通2/行星5/帝国15/银河50/远古50/虚空50（高三级封顶50）\n"
        "  没钱就数羊（数羊 1 2 3… 逐只报数；与自然数1,2,3…逐位比对，任一不符即违例0钱；每5只=1钱；满100只额外奖30钱→数100得50）\n"
        "【拆解】全六档可拆；前三级空手；银河→星尘 / 远古→太古原石 / 虚空→Gem或Mirror\n"
        "【升级】普通→行星→帝国→银河→远古→虚空，各耗对应材料；升到的顶级仍为随机非唯一\n"
        "【已移除】反作弊记录、献祭、能量/生命值、补给/买/萃取、穿戴/7槽、垃圾库（v3 重写）"
    )


def cmd_detail(s, token):
    it = find_item(s, token)
    if not it:
        return f"未找到实例 {token}。"
    lines = [f"🔍 实例 {it['iid']} · {it['tier']}"]
    lines.append(f"  显示名：{_name_str(it)}")
    lines.append(f"  装备槽：{it['slot']}")
    if it["unique"]:
        lines.append(f"  🌟 固定暗金（唯一）｜ 模板ID：{it['template_id']}")
        if it["en"]:
            lines.append(f"  英文名：{it['en']}")
        if it["flavor"]:
            lines.append(f"  📜 {it['flavor']}")
    else:
        lines.append(f"  基础模板：{it['base']}（随机生成，非固定）")
    lines.append(f"  状态：在库")
    return "\n".join(lines)


# ---------- 入口 ----------
def main():
    args = sys.argv[1:]
    if not args:
        print("STARBORNE v3 引擎：输入命令，如 单抽 / 十连 / 货舱 / 规则")
        return
    cmd = args[0]
    existed = os.path.exists(STATE)
    s = load_state()
    if not existed:
        print('**"Starborne, the Transmute Artifact has chosen you."**')
        print('**"The universe is now at your command."**\n')

    if cmd in ("单抽", "roll", "掉落"):
        print(cmd_roll(s, 1))
    elif cmd in ("十连", "再来十连", "roll10"):
        print(cmd_roll(s, 10))
    elif cmd in ("货舱", "查看货舱", "inventory"):
        print(cmd_inventory(s))
    elif cmd in ("状态", "status"):
        print(cmd_status(s))
    elif cmd in ("我的最强装备", "best"):
        print(cmd_best(s))
    elif cmd == "删除装备":
        print(cmd_delete(s, args[1]))
    elif cmd == "拆解":
        print(cmd_dismantle(s, args[1]))
    elif cmd == "升级":
        print(cmd_upgrade(s, args[1]))
    elif cmd == "合成":
        print(cmd_synth(s, args[1], args[2] if len(args) > 2 else ""))
    elif cmd == "卖":
        print(cmd_sell(s, args[1]))
    elif cmd in ("数羊", "count", "数"):
        print(cmd_count(s, args[1:]))
    elif cmd == "清空货舱":
        print(cmd_clear(s, len(args) > 1 and args[1] == "确认"))
    elif cmd in ("规则", "rules"):
        print(cmd_rules())
    elif cmd == "详解":
        print(cmd_detail(s, args[1]))
    else:
        print("未知命令：" + cmd + "。可用：单抽/十连/货舱/状态/最强/删除装备/"
              "拆解/升级/合成/卖/数羊/清空货舱/规则/详解")


if __name__ == "__main__":
    main()
