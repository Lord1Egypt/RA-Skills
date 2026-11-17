#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""STARBORNE GM 工具：装备投递 + 五幕配装式冒险。

用法：
    python gm.py 送 <基础模板名> [档位]     例：python gm.py 送 黑暗之球 银河
    python gm.py 冒险 开始                   新开一局
    python gm.py 冒险 状态                   当前配装 + 可选装备清单
    python gm.py 冒险 探索                   前进，遇敌则出侦察报告
    python gm.py 冒险 配装 <部位> <序号>      换装：武器 / 法球 / 护具
    python gm.py 冒险 出战                   配装完毕，开打（自动结算）
    python gm.py 冒险 休息                   花钱回血
    python gm.py 冒险 战报                   战斗日志
    python gm.py 冒险 指南                   规则说明

==================== 设计 ====================

■ 五幕：无名边境 → 船坞 → 熔渣工厂 → 虫巢 → 虚空之门
  清完一幕进下一幕；每幕按场景顺序把全部小怪挨个打完，末尾关底 Boss。

■ 核心玩法：**配装**
  遇敌 → 侦察报告（敌人完整属性）→ 你配装 → 出战 → 自动结算。
  配装只有三个决定：
    【武器】必带 1 把。决定主伤害与元素。
    【法球】可选带 1 颗。带了才能放法术；每颗球一个法术。
    【护具】可选带 1 件（铠甲/头部/足部/腰部/特殊 任选）。
  战力只按**配装**算，不是按整个货舱 —— 带了什么才生效。

■ 配装为什么有讲究：
  · 敌人有 1 弱点(×1.5) 和 1 抗性(×0.5)，元素 物理/暗/火/雷/蚀/冰/毒
    → 带错元素，最强的刀也只能打出 0.5 倍
  · 敌人防御决定你需要多高的档位 → 史诗刀打不动就得换手段
  · 敌人的攻击决定你带不带护具 → 不带护具可能被两下打死
  · 法球带哪颗 = 选哪种战术（削防/灼烧/冻结/削弱/穿透）

■ 自动战斗：每回合引擎替你决策 —— 法术估算伤害更高就放法术，否则用武器；
  元素克制实时生效；能量刃连续命中同目标 3 次后下一击翻倍。
  你唯一的决策在战前：配装。

■ GM 只给情报，不替你决定：
  遇敌时出侦察报告（血/攻/防/弱点/抗性/预估回合与承伤）。
  打还是撤你说了算 —— `冒险 撤退` 放弃（损失 15% 钱，无掉落）。
  ★ 劣势战（战力比<1）收益更好：钱最多 ×1.8，掉落率最高 +40%。可以赌。
  ★ 失败是真的失败：血量归零 = 被击败。装备一件不扣（暗金是摇出来的运气，
    系统没收等于惩罚运气），扣钱（小怪15%/Boss30%），退回本幕起点，血量回 50%。

■ 钱的双重用途：冒险赚的钱能抽卡，抽到的装备能打怪。

存档：warehouse.json（与 play.py 共用）+ adventure.json（冒险进度）
"""
import importlib.util
import json
import math
import os
import random
import sys
import time
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
TIERS = ["普通", "行星", "帝国", "银河"]
PREFERRED_P1 = ["终焉的", "虚空的", "深渊的", "起源舰的", "流亡者的", "伊克斯的"]
PREFERRED_P2 = ["幽影", "幽能", "蚀刻", "虚空", "星界", "寒霜", "反物质"]

ADV_FILE = os.path.join(HERE, "adventure.json")
SCENARIO_FILE = os.path.join(HERE, "scenario.json")

# ---------- 数值 ----------
TIER_POWER = {"普通": 2, "行星": 6, "帝国": 18, "银河": 50, "远古": 120, "虚空": 260}
SLOT_COVER_BONUS = 0.06
CRIT_RATE = 0.12
CRIT_MULT = 1.6
REST_COST = 30
REST_HEAL = 0.60

WEAPON_DMG = {"普通": 14, "行星": 26, "帝国": 46, "银河": 78, "远古": 120, "虚空": 180}
SPELL_BASE = {"普通": 18, "行星": 32, "帝国": 55, "银河": 70, "远古": 110, "虚空": 160}
SPELL_MANA = {"普通": 12, "行星": 18, "帝国": 24, "银河": 30, "远古": 40, "虚空": 52}
MANA_MAX = 50
MANA_REGEN = 8
FLEE_CHANCE = 0.30
HEAVY_MULT = 2.0
WEAK_MULT = 1.5
RESIST_MULT = 0.5

# 配装：槽位只是分类标签，不设槽位上限。只限「总共带几件」
PART_WEAPON = "武器"
PART_ORB = "法球"
PART_ARMOR = "护具"
PART_TRINKET = "饰品"
ARMOR_SLOTS = ["铠甲", "头部", "足部", "腰部", "特殊"]
MAX_LOADOUT = 99           # 不再限制带几件（饰品/特殊 可自由叠多件）。仅作占位

# 显示分组：武器/饰品(含特殊) 放最前，后面都是「穿的」防具
WORN_SLOTS = ["头部", "铠甲", "腰部", "足部"]
WORN_ORDER = {"头部": 0, "铠甲": 1, "腰部": 2, "足部": 3}
GROUP_HEAD = {
    "武器": "⚔️ 武器（手里的）",
    "饰品": "💍 饰品 / 特殊（带的）",
    "防具": "🛡️ 防具（身上穿的）",
}


def group_key(it):
    """配装清单的分组键：武器 / 饰品(含特殊) / 防具。"""
    if it["slot"] == "武器":
        return "武器"
    if it["slot"] in ("饰品", "特殊"):
        return "饰品"
    return "防具"


def disp_slot(it):
    """显示用槽位名：特殊 当作 饰品 显示在一起。"""
    return "饰品" if it["slot"] in ("饰品", "特殊") else it["slot"]


def short_trait(it):
    """装备特性的短标签，用于配装摘要。"""
    if it["base"] in SPELLS:
        return SPELLS[it["base"]]["name"]
    tr = TRAITS.get(it["base"])
    if tr:
        return tr["name"]
    b = SPELL_BONUS.get(it["base"])
    if b:
        return f"+{int(b * 100)}%法术"
    return None


# 等级标识图标：与货舱一致（引擎 TIERS 表）—— emoji 自带颜色，终端与面板都能显色
TIER_ICON = {"普通": "⬜", "行星": "🔵", "帝国": "🟡", "银河": "🟠", "远古": "🟢", "虚空": "🟣"}

# 分类上限：武器最多 6 把，饰品/特殊最多 8 件；总件数不限
WEAPON_CAP = 6
TRINKET_CAP = 8


def cname(it):
    """档位用货舱同款彩色圆圈表示，名字走默认色。"""
    return f"{TIER_ICON.get(it['tier'], '⬜')} {it['name']}"

# 法球 → 法术
SPELLS = {
    "黑暗之球": {"name": "暗蚀术", "elem": "暗", "power": 1.60,
                 "desc": "无视敌人一半防御", "effect": "pierce"},
    "火焰之球": {"name": "焚魂火", "elem": "火", "power": 1.30,
                 "desc": "点燃敌人，之后每回合掉血", "effect": "burn"},
    "闪电之球": {"name": "连锁雷弧", "elem": "雷", "power": 1.20,
                 "desc": "连打三段", "effect": "chain"},
    "腐蚀之球": {"name": "蚀甲咒", "elem": "蚀", "power": 1.00,
                 "desc": "削掉敌人防御", "effect": "corrode"},
    "霜冻之球": {"name": "霜锁", "elem": "冰", "power": 1.00,
                 "desc": "冻住敌人一回合，它动不了", "effect": "freeze"},
    "毒液之球": {"name": "蚀骨毒", "elem": "毒", "power": 1.10,
                 "desc": "剧毒，敌人攻击变弱", "effect": "poison"},
}

# 武器的元素标签
WEAPON_ELEM = {
    "震击枪": "雷", "激光枪": "火", "寒霜枪": "冰", "灵能刃": "暗",
    "聚变切割器": "火", "喷火器": "火", "阿克莱特冲击炮": "雷", "双管机炮": "物理",
    "能量刃": "暗", "弹射矛": "物理", "轨道炮": "物理", "风暴弩": "物理",
}

# 配装后才生效的特性
TRAITS = {
    "能量刃":     {"name": "过载",   "desc": "连续命中同一目标 3 次后，下一击翻倍"},
    "寒霜枪":     {"name": "霜缓",   "desc": "命中使敌人攻击 -20%，持续 2 回合"},
    "护盾发生器": {"name": "力场",   "desc": "每 3 回合获得一次护盾，吸收一次伤害"},
    "凯达琳水晶": {"name": "星能回流", "desc": "每回合额外回灵 2"},
    "神经吊坠":   {"name": "术式增幅", "desc": "法术强度 +20%"},
    "法师长袍":   {"name": "术式增幅", "desc": "法术强度 +25%"},
    "智力斗篷":   {"name": "术式增幅", "desc": "法术强度 +20%"},
    "灵能发射器": {"name": "术式增幅", "desc": "法术强度 +25%"},
    "圣物":       {"name": "术式增幅", "desc": "法术强度 +15%"},
    "速度之靴":   {"name": "疾行",   "desc": "逃跑成功率大幅提升"},
    "疾行靴":     {"name": "轻捷",   "desc": "逃跑成功率提升"},
    "引力短靴":   {"name": "滑步",   "desc": "逃跑成功率提升"},
    "风暴罗盘":   {"name": "预判",   "desc": "逃跑成功率 +10%"},
}
SPELL_BONUS = {"神经吊坠": 0.20, "法师长袍": 0.25, "智力斗篷": 0.20,
               "灵能发射器": 0.25, "圣物": 0.15}
MANA_BONUS = {"凯达琳水晶": 2}

# 逃跑：竞速判定。成功率 = 基础 + 配装战力贡献 + 鞋子加成 - 敌人威胁
FLEE_BASE = 0.35
FLEE_POWER_BONUS = 0.35        # 你的配装战力越高越跑得掉（封顶）
FLEE_SHOE_BONUS = {"速度之靴": 0.45, "疾行靴": 0.25, "引力短靴": 0.20}
FLEE_ENEMY_PENALTY = 0.25      # 敌人攻击越高越难跑

# ---------- 五幕敌人 ----------
ACTS = [
    {
        "name": "无名边境", "money": 16,
        "foes": [
            {"name": "拾荒者", "hp": 120, "atk": 22, "def": 8, "weak": "火", "resist": "雷",
             "flavor": "钩子挂在腰上，用来从沙里刨还能用的东西。"},
            {"name": "流沙匪", "hp": 150, "atk": 26, "def": 12, "weak": "蚀", "resist": "冰",
             "flavor": "他们不抢货，只抢能走的人。"},
            {"name": "拾骨海盗", "hp": 170, "atk": 30, "def": 14, "weak": "雷", "resist": "暗",
             "flavor": "裹着从坠毁船骸上扒下来的制服。"},
            {"name": "沙虫幼虫", "hp": 200, "atk": 34, "def": 18, "weak": "冰", "resist": "火",
             "flavor": "还没学会潜沙，先学会了咬。"},
            {"name": "锈甲队长", "hp": 260, "atk": 40, "def": 24, "weak": "蚀", "resist": "雷",
             "flavor": "甲是用压路机压平的，焊得很难看。"},
        ],
        "boss": {"name": "边境锈王", "hp": 420, "atk": 52, "def": 30, "weak": "火", "resist": "雷",
                 "flavor": "他在这条边境上收过三十年过路费。"},
    },
    {
        "name": "船坞", "money": 30,
        "foes": [
            {"name": "失控巡检无人机", "hp": 240, "atk": 48, "def": 26, "weak": "雷", "resist": "物理",
             "flavor": "仍在巡逻。巡逻的区域早已没有人。"},
            {"name": "恶犬", "hp": 260, "atk": 52, "def": 28, "weak": "火", "resist": "冰",
             "flavor": "项圈上写着工号，主人已经上个月就死了。"},
            {"name": "哨兵", "hp": 280, "atk": 56, "def": 32, "weak": "暗", "resist": "雷",
             "flavor": "它还在等一句早就不再来的口令。"},
            {"name": "焊接奴工", "hp": 320, "atk": 60, "def": 30, "weak": "冰", "resist": "火",
             "flavor": "护目镜里焊进去的火星早就不烫了。"},
            {"name": "恶霸", "hp": 380, "atk": 66, "def": 38, "weak": "蚀", "resist": "物理",
             "flavor": "占了整条船坞，理由是船坞需要有人管。"},
        ],
        "boss": {"name": "坞主·铁锚", "hp": 620, "atk": 78, "def": 48, "weak": "雷", "resist": "冰",
                 "flavor": "名字是真的。他从没解开过自己的锚。"},
    },
    {
        "name": "熔渣工厂", "money": 52,
        "foes": [
            {"name": "熔渣魔", "hp": 420, "atk": 76, "def": 44, "weak": "冰", "resist": "火",
             "flavor": "渣里凝出来的形状，形状里没骨头。"},
            {"name": "焚化士兵", "hp": 450, "atk": 82, "def": 46, "weak": "毒", "resist": "火",
             "flavor": "制服烧到看不见编号，工牌是熔上去的。"},
            {"name": "焚风炉心", "hp": 500, "atk": 88, "def": 52, "weak": "冰", "resist": "雷",
             "flavor": "它一直在烧，烧了三十年也没烧完自己。"},
            {"name": "装甲机器人", "hp": 560, "atk": 96, "def": 60, "weak": "蚀", "resist": "物理",
             "flavor": "履带磨没了，滑着走了半条走廊。"},
            {"name": "熔渣暴君", "hp": 640, "atk": 104, "def": 68, "weak": "冰", "resist": "蚀",
             "flavor": "它曾是个班长。班长的部分还留着。"},
        ],
        "boss": {"name": "炉心·熔帝", "hp": 900, "atk": 118, "def": 82, "weak": "冰", "resist": "火",
                 "flavor": "整座工厂的炉子，其实是同一颗心脏。"},
    },
    {
        "name": "虫巢", "money": 88,
        "foes": [
            {"name": "巢卫甲虫", "hp": 700, "atk": 118, "def": 76, "weak": "火", "resist": "物理",
             "flavor": "外骨骼硬得能弹开子弹，弹开后就留在上面。"},
            {"name": "裂变工虫", "hp": 760, "atk": 126, "def": 80, "weak": "雷", "resist": "毒",
             "flavor": "它一边搬运一边分裂，分裂的那半继续搬。"},
            {"name": "酸液喷吐者", "hp": 820, "atk": 132, "def": 86, "weak": "火", "resist": "蚀",
             "flavor": "酸把地板烧穿，露出更深的巢。"},
            {"name": "骨甲武士", "hp": 900, "atk": 142, "def": 94, "weak": "物理", "resist": "暗",
             "flavor": "甲是用同类的壳拼的，拼得很整齐。"},
            {"name": "虫巢裂变虫后", "hp": 1000, "atk": 152, "def": 100, "weak": "火", "resist": "毒",
             "flavor": "它生下的每一个都记得它。"},
        ],
        "boss": {"name": "母巢·裂变之母", "hp": 1350, "atk": 172, "def": 122, "weak": "火", "resist": "暗",
                 "flavor": "整个巢是它身体的一部分，包括你脚下这块。"},
    },
    {
        "name": "虚空之门", "money": 145,
        "foes": [
            {"name": "虚空奴仆", "hp": 1150, "atk": 168, "def": 110, "weak": "物理", "resist": "暗",
             "flavor": "它重复着你上一次死掉的动作。"},
            {"name": "时蚀行者", "hp": 1250, "atk": 178, "def": 118, "weak": "雷", "resist": "物理",
             "flavor": "走过你身边，你的年份少了一年。"},
            {"name": "虚空低语者", "hp": 1350, "atk": 188, "def": 126, "weak": "毒", "resist": "暗",
             "flavor": "它说话时你确实听懂了，只是内容是你自己。"},
            {"name": "湮灭执行者", "hp": 1450, "atk": 198, "def": 134, "weak": "蚀", "resist": "雷",
             "flavor": "不宣判，只执行，执行完连罪名一起抹掉。"},
            {"name": "影子卫士", "hp": 1600, "atk": 212, "def": 146, "weak": "火", "resist": "冰",
             "flavor": "影子先到，身体后来。"},
        ],
        "boss": {"name": "虚空之主·阿拉基恩", "hp": 2100, "atk": 240, "def": 170, "weak": "火", "resist": "暗",
                 "flavor": "门后面那个一直在等的，终于等到了。"},
    },
]

# 剧本外置：scenario.json 若存在则以它为准（用户可单独改文案），缺失/损坏才回退内置。
if os.path.exists(SCENARIO_FILE):
    try:
        with open(SCENARIO_FILE, "r", encoding="utf-8") as _f:
            _sc = json.load(_f)
        if isinstance(_sc, list):
            ACTS = _sc
        elif isinstance(_sc, dict) and "acts" in _sc:
            ACTS = _sc["acts"]
    except Exception:
        pass

DROP_WEIGHTS = {
    0: {"普通": 55, "行星": 40, "帝国": 5},
    1: {"普通": 30, "行星": 45, "帝国": 23, "银河": 2},
    2: {"普通": 10, "行星": 40, "帝国": 40, "银河": 10},
    3: {"普通": 5, "行星": 25, "帝国": 45, "银河": 24, "远古": 1},
    4: {"行星": 10, "帝国": 35, "银河": 40, "远古": 13, "虚空": 2},
}


# ---------- 引擎加载 ----------
def load_engine():
    for fn in sorted(os.listdir(HERE)):
        if fn.startswith("starborne_") and fn.endswith(".py"):
            path = os.path.join(HERE, fn)
            break
    else:
        sys.exit("找不到引擎脚本 starborne_*.py")
    spec = importlib.util.spec_from_file_location("starborne_engine", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.STATE = os.path.join(HERE, "warehouse.json")
    return mod


def find_slot(mod, base):
    for slot, bases in mod.SLOT_TEMPLATES.items():
        if base in bases:
            return slot
    return None


def degenerate(name):
    for i in range(len(name) - 3):
        if name[i:i + 2] == name[i + 2:i + 4]:
            return True
    return False


def pick_name(mod, tier, slot, base):
    best = None
    for seed in range(3000):
        rng = random.Random(seed)
        name, _ = mod.roll_random_name(rng, tier, slot, base)
        if degenerate(name):
            continue
        score = (2 if any(name.startswith(x) for x in PREFERRED_P1) else 0) + \
                (1 if any(x in name for x in PREFERRED_P2) else 0)
        if best is None or score > best[0]:
            best = (score, name)
        if score >= 3:
            break
    return best[1]


def make_item(mod, tier, slot, base, name=None):
    uid = uuid.uuid4().hex
    suffix = mod._b36(int(time.time()))[-4:] + uid[:4]
    iid = f"{mod.TIER_CODE[tier]}-{mod.SLOT_CODE.get(slot, 'XX')}-{suffix}"
    if name is None:
        name, _ = mod.roll_random_name(random.Random(), tier, slot, base)
    return {"uid": uid, "iid": iid, "tier": tier, "slot": slot, "base": base, "name": name,
            "en": None, "unique": False, "template_id": None, "flavor": None}


def gift(mod, base, tier):
    slot = find_slot(mod, base)
    if slot is None:
        cands = [b for bases in mod.SLOT_TEMPLATES.values() for b in bases if base in b]
        sys.exit(f"找不到基础模板「{base}」。相近的有：{'、'.join(cands[:6])}")
    if tier not in TIERS:
        sys.exit(f"指定基础模板时档位只能是：{'、'.join(TIERS)}")
    s = mod.load_state()
    item = make_item(mod, tier, slot, base, pick_name(mod, tier, slot, base))
    s["warehouse"].append(item)
    mod.save_state(s)
    return item


def drop_item(mod, s, weights):
    names = list(weights.keys())
    tier = random.choices(names, weights=[weights[n] for n in names], k=1)[0]
    slot = random.choice(mod.SLOTS)
    base = random.choice(mod.SLOT_TEMPLATES[slot])
    name, slot = mod.roll_random_name(random.Random(), tier, slot, base)
    item = make_item(mod, tier, slot, base, name)
    s["warehouse"].append(item)
    return item


# ---------- 冒险状态 ----------
def default_adv():
    return {"act": 0, "step": 0, "hp": None, "log": [], "cleared": 0, "deaths": 0,
            "over": False, "won": False, "seed": random.getrandbits(32),
            "loadout": {"items": []}, "foe": None,
            "chest": None, "chests": [], "chest_act": None}


def load_adv():
    if os.path.exists(ADV_FILE):
        with open(ADV_FILE, "r", encoding="utf-8") as f:
            st = json.load(f)
        for k, v in default_adv().items():
            st.setdefault(k, v)
        # 旧版本：回合制残留的战斗状态直接清掉
        st.pop("combat", None)
        # 兼容旧存档：老的 loadout 是分部位结构，转成统一 items 列表
        lo = st.get("loadout") or {}
        if "items" not in lo:
            items = []
            for key in ("武器", "法球"):
                if lo.get(key):
                    items.append(lo[key])
            for key in ("护具", "饰品"):
                v = lo.get(key) or []
                if isinstance(v, str):
                    v = [v]
                items.extend(v)
            lo = {"items": items}
        st["loadout"] = lo
        if not st.get("foe"):
            st["foe"] = None
        return st
    return default_adv()


def save_adv(st):
    with open(ADV_FILE, "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False, indent=2)


# ---------- 配装 ----------
def weapons_of(s):
    return [it for it in s["warehouse"] if it["slot"] == "武器" and it["base"] not in SPELLS]


def foci_of(s):
    out = [it for it in s["warehouse"] if it["base"] in SPELLS]
    out.sort(key=lambda x: (list(SPELLS).index(x["base"]), -TIER_POWER.get(x["tier"], 2)))
    return out


def armors_of(s):
    return [it for it in s["warehouse"] if it["slot"] in ARMOR_SLOTS]


def trinkets_of(s):
    return [it for it in s["warehouse"] if it["slot"] == "饰品"]


def equippable_of(s):
    """全部可配装的东西，按 武器 → 饰品/特殊 → 防具(穿的) 分组排序，统一编号。

    槽位只是分类标签，不限制带什么，也不限制总件数 —— 饰品/特殊 可自由叠多件。
    特殊 视为 饰品 一类（显示在一起）。
    """
    w = weapons_of(s) + foci_of(s)
    trinkets = trinkets_of(s)
    specials = [it for it in s["warehouse"] if it["slot"] == "特殊"]
    worn = [it for it in s["warehouse"] if it["slot"] in WORN_SLOTS]
    worn.sort(key=lambda x: WORN_ORDER[x["slot"]])
    return w + trinkets + specials + worn


def equipped_items(s, loadout):
    """取出当前配装的所有件（可能为空）。"""
    out = []
    for iid in loadout.get("items", []):
        for it in s["warehouse"]:
            if it["iid"] == iid:
                out.append(it)
                break
    return out


def loadout_stats(s, loadout):
    """战力只按配装算 —— 带了什么才生效。"""
    items = equipped_items(s, loadout)
    power = sum(TIER_POWER.get(it["tier"], 2) for it in items)
    power = int(power * (1 + len(items) * SLOT_COVER_BONUS))
    atk = 8 + power * 0.14
    df = 4 + power * 0.05
    hp_max = int(120 + power * 0.55)
    # 部位加成：武器主攻，护具主防，饰品小幅加防
    for it in items:
        if it["slot"] == "武器" and it["base"] not in SPELLS:
            atk *= 1.25
        if it["slot"] in ARMOR_SLOTS:
            df *= 1.30
        if it["slot"] == "饰品":
            df *= 1.10
    mult, regen = 1.0, 0
    for it in items:
        mult += SPELL_BONUS.get(it["base"], 0.0)
        regen += MANA_BONUS.get(it["base"], 0)
    return {"power": power, "atk": atk, "df": df, "hp_max": hp_max,
            "spell_mult": mult, "mana_regen": MANA_REGEN + regen, "items": items}


def elem_mult(enemy, elem):
    """实际伤害用的克制判定 —— 读真属性（true_weak/true_resist）。"""
    m, note = 1.0, []
    if enemy.get("true_weak", enemy.get("weak")) == elem:
        m *= WEAK_MULT
        note.append("弱点")
    if enemy.get("true_resist", enemy.get("resist")) == elem:
        m *= RESIST_MULT
        note.append("抗性")
    return m, note


def elem_tag(enemy, elem):
    m, note = elem_mult(enemy, elem)
    tag = elem
    if note:
        tag += "·" + "/".join(note)
    return tag, m


# ---------- 战斗（自动结算） ----------
def auto_battle(mod, s, st, enemy, is_boss, ratio):
    """按配装自动打完这场。返回 (结果, 日志列表)。"""
    ld = st["loadout"]
    p = loadout_stats(s, ld)
    log = []

    weapon = None
    orb = None
    for it in p["items"]:
        if it["base"] in SPELLS:
            if orb is None:
                orb = it
        elif it["slot"] == "武器" and weapon is None:
            weapon = it

    ehp, ehp_max = enemy["hp"], enemy["hp"]
    # 开局灵力：按法术强度给，法术流开局就能放第一发
    mana = int(min(MANA_MAX, 10 + p["spell_mult"] * 20))
    corrode = 0.0
    burn = burn_dmg = 0
    poison = freeze = 0
    shield = shield_timer = 0
    hits = 0
    last_was = None
    turn = 0
    regen = p["mana_regen"]
    # 战斗叙事：只记值得说的时刻，普通过程压成一句
    story = []
    hits_taken = 0
    sum_dmg = 0
    spell_casts = 0
    weapon_hits = 0

    def e_def():
        return max(0.0, enemy["def"] * (1 - corrode))

    def e_atk():
        a = enemy["atk"]
        if poison > 0:
            a *= 0.85
        if is_boss and ehp < ehp_max * 0.3:
            a *= 1.4
        return a

    def has_trait(base):
        return any(it["base"] == base for it in p["items"])

    # 伏击：开场就被抢先打一下（不是最后一回合才触发）
    if enemy.get("ambush"):
        enemy["ambush"] = False
        amb = max(1, int(e_atk() * random.uniform(0.85, 1.15)))
        if shield > 0:
            shield -= 1
            log.append(f"    ⚡ 伏击！它比侦察时更快，先手打了你一下（{amb} 伤害）—— 护盾挡下了。")
        else:
            st["hp"] -= amb
            log.append(f"    ⚡ 伏击！它比侦察时更快，先手打了你一下（{amb} 伤害）。")

    while st["hp"] > 0 and ehp > 0 and turn < 60:
        turn += 1

        # 战斗开始：揭露伪装 / 突变
        if turn == 1:
            if enemy.get("disguised"):
                log.append(f"    🎭 伪装揭穿 —— 这不是普通货色。真实血量 {enemy['hp']}，攻击 {enemy['atk']}。")
                enemy["disguised"] = False
            if enemy.get("mutated"):
                kind = enemy["mutated"]
                if kind == "weak":
                    log.append(f"    🧬 突变！它的弱点是假的 —— 真正的弱点是 {enemy['true_weak']}。")
                else:
                    log.append(f"    🧬 突变！它的抗性是假的 —— 真正的抗性是 {enemy['true_resist']}。")
                enemy["mutated"] = None

        # 灼烧结算
        if burn > 0:
            ehp -= burn_dmg
            log.append(f"🔥 灼烧敌人 {burn_dmg} 点（敌余 {max(0,ehp)}）")
            burn -= 1
            if ehp <= 0:
                break

        # 引擎替你决策：法术估算更高就放，否则用武器
        use_spell = False
        spell_est = 0
        if orb:
            sp = SPELLS[orb["base"]]
            cost = SPELL_MANA.get(orb["tier"], 12)
            _, m = elem_tag(enemy, sp["elem"])
            base_est = SPELL_BASE.get(orb["tier"], 18) * sp["power"] * p["spell_mult"] * m
            # 估算必须和实际结算口径一致：扣防御、无视则只扣一半
            if sp["effect"] == "pierce":
                spell_est = max(1, base_est - e_def() * 0.5)
            else:
                spell_est = max(1, base_est - e_def() * 0.45)
            # 估算更高 **且** 灵力够，且这一发值得放（敌人还剩的血够它发挥）
            use_spell = (mana >= cost and spell_est > weapon_est(weapon, p, enemy)
                         and ehp > spell_est * 0.8)

        if use_spell:
            sp = SPELLS[orb["base"]]
            cost = SPELL_MANA.get(orb["tier"], 12)
            mana -= cost
            spell_casts += 1
            base = SPELL_BASE.get(orb["tier"], 18) * sp["power"] * p["spell_mult"]
            tag, m = elem_tag(enemy, sp["elem"])
            eff = sp["effect"]
            extra = ("（弱点×1.5）" if "弱点" in tag else "") + ("（抗性×0.5）" if "抗性" in tag else "")
            if eff == "pierce":
                crit = random.random() < CRIT_RATE
                dmg = (base * m - e_def() * 0.5) * random.uniform(0.9, 1.1)
                if crit:
                    dmg *= CRIT_MULT
                dmg = max(1, int(dmg))
                ehp -= dmg
                log.append(f"    ✨ {sp['name']}！{dmg} 伤害{extra}")
            elif eff == "chain":
                total = 0
                for _ in range(3):
                    d = max(1, int(base * m * random.uniform(0.5, 0.7)))
                    total += d
                    ehp -= d
                log.append(f"    ✨ {sp['name']}！三段雷弧共 {total} 伤害{extra}")
            elif eff == "burn":
                dmg = max(1, int((base * m - e_def() * 0.45) * random.uniform(0.9, 1.1)))
                ehp -= dmg
                burn = 3
                burn_dmg = max(2, int(base * 0.16))
                log.append(f"    ✨ {sp['name']}！{dmg} 伤害并点燃了它")
            elif eff == "corrode":
                dmg = max(1, int((base * m - e_def() * 0.45) * random.uniform(0.9, 1.1)))
                ehp -= dmg
                before = e_def()
                corrode = min(0.6, corrode + 0.15)
                log.append(f"    ✨ {sp['name']}！{dmg} 伤害，它的防御被削了（{before:.0f}→{e_def():.0f}）")
            elif eff == "freeze":
                dmg = max(1, int((base * m - e_def() * 0.45) * random.uniform(0.9, 1.1)))
                ehp -= dmg
                freeze = 2
                log.append(f"    ✨ {sp['name']}！{dmg} 伤害，把它冻住了")
            elif eff == "poison":
                dmg = max(1, int((base * m - e_def() * 0.45) * random.uniform(0.9, 1.1)))
                ehp -= dmg
                poison = 3
                log.append(f"    ✨ {sp['name']}！{dmg} 伤害，毒性开始发作")
        else:
            if not weapon:
                log.append("    你没带武器，一拳打不出声音。")
                break
            base = WEAPON_DMG.get(weapon["tier"], 14)
            elem = WEAPON_ELEM.get(weapon["base"], "物理")
            tag, m = elem_tag(enemy, elem)
            crit = random.random() < CRIT_RATE
            dmg = (base + p["atk"] * 0.35) * m * random.uniform(0.85, 1.15)
            if crit:
                dmg *= CRIT_MULT
            if weapon["base"] == "能量刃" and has_trait("能量刃"):
                hits = hits + 1 if last_was == weapon["iid"] else 1
                last_was = weapon["iid"]
                if hits >= 3:
                    hits = 0
                    dmg = int(dmg * 2)
                    log.append("    ⚡ 过载！能量刃充能完成，这一击翻倍。")
            dmg = max(1, int(dmg))
            ehp -= dmg
            weapon_hits += 1
            extra = ("（弱点×1.5）" if "弱点" in tag else "") + ("（抗性×0.5）" if "抗性" in tag else "")
            if crit:
                extra += "（暴击）"
            # 普通过程不逐条记，只在打弱点/抗性/暴击时提一句
            if extra:
                log.append(f"    ⚔️ 「{weapon['name']}」{dmg} 伤害{extra}")
            if weapon["base"] == "寒霜枪" and has_trait("寒霜枪"):
                log.append("    ❄ 霜缓：敌人攻击 -20%，持续 2 回合。")

        if ehp <= 0:
            break

    # 敌人回合
    if freeze > 0:
        freeze -= 1
        log.append("    🧊 它被冻住了，动不了。")
    else:
        heavy = (turn % 3 == 0) if is_boss else (turn % 4 == 0)
        dmg = e_atk() * (HEAVY_MULT if heavy else 1.0) * random.uniform(0.85, 1.15)
        crit = random.random() < CRIT_RATE
        if crit:
            dmg *= CRIT_MULT
        dmg = max(1, int(dmg))
        if shield > 0:
            shield -= 1
            log.append(f"    🛡 护盾挡下了这一击。")
        else:
            st["hp"] -= dmg
            hits_taken += 1
            sum_dmg += dmg
            word = "重击" if heavy else "反击"
            # 只记重击和暴击，普通反击不逐条刷屏
            if heavy:
                log.append(f"    👹 它重击你，{dmg} 伤害。")
            elif crit:
                log.append(f"    👹 它暴击了你，{dmg} 伤害。")

    # 护盾发生器
    if has_trait("护盾发生器"):
        shield_timer += 1
        if shield_timer >= 3:
            shield_timer = 0
            if shield == 0:
                shield = 1
                log.append("    🛡 力场展开：获得一次护盾。")

    mana = min(MANA_MAX, mana + regen)

    # 收尾：把省略掉的普通过程压成一句
    parts = [f"{turn} 回合", f"{weapon_hits} 记武器攻击"]
    if spell_casts:
        parts.append(f"{spell_casts} 发法术")
    if hits_taken:
        parts.append(f"你挨了 {hits_taken} 下共 {sum_dmg} 点")
    else:
        parts.append("它没碰到你")
    log.append("    （" + "，".join(parts) + "）")

    if ehp <= 0:
        return "win", log
    if st["hp"] <= 0:
        return "defeat", log
    return "draw", log


def weapon_est(weapon, p, enemy, report=False, enemy_def_val=None):
    """估算武器的单回合伤害。report=True 时用侦察报告（可能是假的）算。"""
    if not weapon:
        return 0
    base = WEAPON_DMG.get(weapon["tier"], 14)
    elem = WEAPON_ELEM.get(weapon["base"], "物理")
    if report:
        r = report_attrs(enemy)
        m = 1.0
        if r.get("weak") == elem:
            m *= WEAK_MULT
        if r.get("resist") == elem:
            m *= RESIST_MULT
        dv = r.get("def", 0)
    else:
        _, m = elem_tag(enemy, elem)
        dv = enemy_def_val if enemy_def_val is not None else enemy.get("def", 0)
    return max(1, (base + p["atk"] * 0.35) * m - dv * 0.45)


# ---------- 随机性：让侦察报告可能是假的 ----------
# 三层不确定，叠在"配装"之上 —— 你的情报不完全，你只能赌。
MUTATE_CHANCE = 0.10     # 敌人突变：报告里的弱点/抗性有一项是假的
DISGUISE_CHANCE = 0.08   # 伪装：看着是小怪，实际是精英属性
AMBUSH_CHANCE = 0.12     # 伏击：先手被抢，先挨一下

ELEMENTS_POOL = ["物理", "暗", "火", "雷", "蚀", "冰", "毒"]


def make_foe(act, is_boss, idx=None):
    """生成一个敌人，并决定它带哪几层伪装/突变。
    idx 给定时按顺序取 foes[idx]（保证把场景里的怪挨个打一遍），否则随机。"""
    if is_boss:
        src = act["boss"]
    elif idx is not None:
        src = act["foes"][idx % len(act["foes"])]
    else:
        src = random.choice(act["foes"])
    foe = dict(src)
    foe["boss"] = is_boss
    foe["true_weak"] = foe.get("weak")
    foe["true_resist"] = foe.get("resist")

    # 伪装：看着小怪，实际属性翻倍
    if not is_boss and random.random() < DISGUISE_CHANCE:
        foe["hp"] = int(foe["hp"] * 1.8)
        foe["atk"] = int(foe["atk"] * 1.7)
        foe["disguised"] = True
        foe["report_hp"] = int(foe["hp"] / 1.8)
        foe["report_atk"] = int(foe["atk"] / 1.7)
    else:
        foe["disguised"] = False
        foe["report_hp"] = foe["hp"]
        foe["report_atk"] = foe["atk"]

    # 突变：报告里的弱点/抗性有一项是假的
    foe["mutated"] = None
    if random.random() < MUTATE_CHANCE:
        kind = random.choice(["weak", "resist"])
        real = foe["true_weak"] if kind == "weak" else foe["true_resist"]
        fake = random.choice([e for e in ELEMENTS_POOL if e != real])
        if kind == "weak":
            foe["weak"] = fake
            foe["true_weak"] = random.choice([e for e in ELEMENTS_POOL if e != fake])
        else:
            foe["resist"] = fake
            foe["true_resist"] = random.choice([e for e in ELEMENTS_POOL if e != fake])
        foe["mutated"] = kind

    # 伏击：开场被先手
    foe["ambush"] = (not is_boss) and random.random() < AMBUSH_CHANCE
    return foe


# ---------- 宝箱 / 宝箱怪 ----------
# 全局掉落：六档等概率，不过滤高阶（用户决定：玩的就是概率，完全放开）
GLOBAL_DROP = {t: 1.0 for t in TIER_POWER}

def make_mimic(act):
    """宝箱怪：属性取本幕 Boss 的一半，弱点/抗性随机（伏击必触发）。"""
    b = act["boss"]
    weak = random.choice(ELEMENTS_POOL)
    resist = random.choice(ELEMENTS_POOL)
    while resist == weak:
        resist = random.choice(ELEMENTS_POOL)
    hp = int(b["hp"] * 0.5)
    atk = int(b["atk"] * 0.5)
    df = int(b["def"] * 0.5)
    return {"name": "宝箱怪", "hp": hp, "atk": atk, "def": df,
            "weak": weak, "resist": resist,
            "true_weak": weak, "true_resist": resist,
            "flavor": "它用箱盖当嘴。你伸手那一刻，它合上了。",
            "boss": False, "mimic": True, "disguised": False, "ambush": True,
            "report_hp": hp, "report_atk": atk, "mutated": None}


def flee_chance(s, st, enemy):
    """逃跑成功率：像跟它赛跑一样算。"""
    p = loadout_stats(s, st["loadout"])
    items = p["items"]
    # 配装战力 → 跑动能力（封顶加成 0.35）
    speed = min(FLEE_POWER_BONUS, p["power"] / 600.0 * FLEE_POWER_BONUS)
    # 鞋子
    for it in items:
        speed += FLEE_SHOE_BONUS.get(it["base"], 0.0)
    # 风暴罗盘：预判
    if any(it["base"] == "风暴罗盘" for it in items):
        speed += 0.10
    # 敌人威胁：它攻击越高越难跑
    threat = min(0.45, enemy["atk"] / 400.0 * FLEE_ENEMY_PENALTY)
    chance = FLEE_BASE + speed - threat
    return max(0.05, min(0.95, chance)), speed, threat


def do_flee(mod, s, st):
    """尝试逃跑：一次判定，跑掉就没有掉落，跑不掉被白打。"""
    if not st.get("foe"):
        print("当前没有敌情，没什么好跑的。")
        return
    enemy = dict(st["foe"])
    chance, speed, threat = flee_chance(s, st, enemy)
    print(f"🏃 你转身就跑 ——")
    print(f"    你的脚力 {speed*100:.0f}　它的压迫 {threat*100:.0f}　成功率 {chance*100:.0f}%")
    if random.random() < chance:
        st["foe"] = None
        mod.save_state(s)
        save_adv(st)
        print("    ✅ 跑掉了。它没追上。")
        print("    → 装备一件没丢，但也没有掉落。命比货重要。")
        print("    （想再来：再 `冒险 探索`。）")
        return
    # 跑不掉
    p = loadout_stats(s, st["loadout"])
    hit = max(1, int(enemy["atk"] * random.uniform(0.9, 1.3)))
    st["hp"] -= hit
    st["foe"] = None
    mod.save_state(s)
    save_adv(st)
    print(f"    ❌ 没跑掉。它一把薅住你 —— {hit} 点伤害。")
    if st["hp"] <= 0:
        st["hp"] = 0
        print("    💀 你倒在了逃跑的路上。")
        # 逃跑失败致死：按被击败处理
        loss = int(s["money"] * 0.15)
        s["money"] -= loss
        st["hp"] = int(p["hp_max"] * 0.5)
        st["step"] = 0
        st["deaths"] = st.get("deaths", 0) + 1
        mod.save_state(s)
        save_adv(st)
        print(f"    装备一件没丢，被搜走 {loss} 钱。退回本幕起点，血量恢复 50%。")
    else:
        print(f"    血量 {st['hp']}/{p['hp_max']}。装备一件没丢，但也没有掉落。")


def report_attrs(foe):
    """侦察报告里显示的属性（可能是假的）。"""
    return {"hp": foe.get("report_hp", foe["hp"]),
            "atk": foe.get("report_atk", foe["atk"]),
            "def": foe["def"],
            "weak": foe.get("weak"),
            "resist": foe.get("resist")}


# ---------- 侦察报告 ----------
def scout_report(s, st, enemy, is_boss):
    p = loadout_stats(s, st["loadout"])
    r = report_attrs(enemy)
    ratio = eff_power(p["atk"], p["df"], st["hp"]) / eff_power(r["atk"], r["def"], r["hp"])
    best = max((weapon_est(w, p, enemy, report=True) for w in weapons_of(s)), default=0)
    turns = max(1, math.ceil(r["hp"] / best)) if best else 99
    incoming = max(0, int((r["atk"] - p["df"]) * turns))
    v, vicon = verdict(ratio)

    print("╔══ 侦察报告 " + "═" * 40)
    print(f"║ 目标：{enemy['name']}" + ("　【关底 Boss】" if is_boss else ""))
    print(f"║ 「{enemy['flavor']}」")
    print(f"║ 血量 {r['hp']}　攻击 {r['atk']}　防御 {r['def']}")
    print(f"║ 弱点 {r['weak']}（伤害×1.5）　抗性 {r['resist']}（伤害×0.5）")
    print(f"║ 预估：你的最强武器约 {best:.0f} 伤害/回合 → 约 {turns} 回合结束，期间你大概挨 {incoming} 点")
    print(f"║ 你的血量 {st['hp']}/{p['hp_max']}　当前配装战力 {p['power']}")
    print(f"║ GM 评估：{vicon} {v}（战力比 {ratio:.2f}）")
    if ratio < 1.0:
        print(f"║ ⚠ 战力比不足 1 —— 硬打有输的可能。但险胜收益更高："
              f"钱最多 ×{1+(1-ratio)*0.8:.2f}，掉落率 +{int((1-ratio)*40)}%")
    print("╚" + "═" * 50)
    print()
    print("配装建议（`冒险 状态` 看清单，`冒险 配装 <部位> <序号>` 换）：")
    # 弱点/抗性提示（基于报告，可能被骗）
    weaks = [w for w in weapons_of(s) if WEAPON_ELEM.get(w["base"]) == r["weak"]]
    resists = [w for w in weapons_of(s) if WEAPON_ELEM.get(w["base"]) == r["resist"]]
    if weaks:
        print(f"  ★ 你有 {len(weaks)} 把武器打弱点（{r['weak']}）：" +
              "、".join(f"{w['name']}" for w in weaks[:3]))
    if resists:
        print(f"  ✗ 避开抗性（{r['resist']}）：" + "、".join(f"{w['name']}" for w in resists[:3]))
    if not weaks and not resists:
        print("  · 你手上的武器元素都不吃它的弱点/抗性 —— 只能靠档位硬压。")
    orbs = foci_of(s)
    orb_txt = "、".join("%s(%s)" % (f["name"], SPELLS[f["base"]]["name"]) for f in orbs) or "（没有）"
    print("  · 法球媒介：" + orb_txt)
    print("  → 配好了就 `冒险 出战`。不想打就 `冒险 撤退`（损失 15% 钱，无掉落）。")
    print()
    print("  ⚠ 情报不是保证。这片沙子里东西会骗人 —— 报告里的弱点未必是真弱点，")
    print("    看着不起眼的未必真不起眼。有时候你得赌一把。")
    return ratio


def eff_power(atk, df, hp):
    return atk * 3 + df * 2 + hp * 0.5


def verdict(ratio):
    if ratio >= 1.80:
        return "碾压", "🟢"
    if ratio >= 1.25:
        return "优势", "🔵"
    if ratio >= 0.95:
        return "均势", "🟡"
    if ratio >= 0.75:
        return "劣势", "🟠"
    return "守不住", "🔴"


def print_loadout(s, st):
    ld = st["loadout"]
    items = equipped_items(s, ld)
    print("🎽 配装")
    if not items:
        print("   （空）—— 没带任何东西出门")
        return
    order_grp = {"武器": 0, "饰品": 1, "防具": 2}
    items = sorted(items, key=lambda x: (order_grp[group_key(x)], WORN_ORDER.get(x["slot"], 9)))
    groups = {"武器": [], "饰品": [], "防具": []}
    for x in items:
        groups[group_key(x)].append(x)
    icon = {"武器": "⚔️", "饰品": "💍", "防具": "🛡️"}
    for g in ("武器", "饰品"):
        if groups[g]:
            line = " · ".join(
                f"{cname(x)}" + (f"〔{short_trait(x)}〕" if short_trait(x) else "")
                for x in groups[g]
            )
            print(f"  {icon[g]} {line}")
    if groups["防具"]:
        for i, x in enumerate(groups["防具"]):
            tag = f"〔{short_trait(x)}〕" if short_trait(x) else ""
            prefix = f"{icon['防具']} " if i == 0 else "  "
            print(f"  {prefix}{cname(x)}{tag}")
    p = loadout_stats(s, ld)
    print(f"  → 战力 {p['power']}　攻 {p['atk']:.0f}　防 {p['df']:.0f}　血 {p['hp_max']}　"
          f"法术 ×{p['spell_mult']:.2f}　回灵 {p['mana_regen']}")
    print()


def print_equippable(s, st):
    """统一编号的可配装清单，按 武器 → 饰品/特殊 → 防具 分组显示。"""
    pool = equippable_of(s)
    cur = set(st["loadout"].get("items", []))
    print(f"可配装清单（共 {len(pool)} 件）：")
    last_g = None
    for i, x in enumerate(pool, 1):
        g = group_key(x)
        if g != last_g:
            print(f"\n  {GROUP_HEAD[g]}")
            last_g = g
        mark = "✅" if x["iid"] in cur else "  "
        role = ""
        if x["base"] in SPELLS:
            role = f" → {SPELLS[x['base']]['name']}（{SPELLS[x['base']]['desc']}）"
        elif x["slot"] == "武器":
            role = f" · {WEAPON_ELEM.get(x['base'], '物理')}元素"
        tr = TRAITS.get(x["base"])
        if tr:
            role += f" ｜ 特性·{tr['name']}"
        slot_txt = f"（{disp_slot(x)}）" if g != "防具" else ""
        print(f"  {mark}[{i}] {cname(x)}{slot_txt}{role}")
    print("\n  → `冒险 配装 1,4,7` 一次设好（序号取自上表，逗号分隔）；`冒险 配装 0` 全部卸下")


def cmd_adv(mod, args):
    st = load_adv()
    s = mod.load_state()
    sub = args[0] if args else "状态"

    if sub == "开始":
        st = default_adv()
        p = loadout_stats(s, st["loadout"])
        st["hp"] = p["hp_max"]
        save_adv(st)
        print(f"🌌 冒险开始：{ACTS[0]['name']}。")
        print(f"当前配装战力 {p['power']}，血量 {st['hp']}/{p['hp_max']}")
        print("流程：探索遇敌 → 侦察报告 → 配装 → 出战。打穿五幕。")
        return

    if sub == "指南":
        print("📜 冒险指南")
        print("· 五幕：" + " → ".join(a["name"] for a in ACTS) + "，清完一幕进下一幕，末幕 Boss 是终点")
        print("· 遇敌 → 侦察报告（敌人血/攻/防/弱点/抗性/预估）→ 你配装 → 出战 → 自动结算")
        print(f"【配装】武器最多 {WEAPON_CAP} 把 / 法球(可选) / 防具(穿的) / 饰品·特殊(带的，最多 {TRINKET_CAP} 件)；总件数不限。战力只按配装算，带了才生效")
        print("【配装为什么有讲究】")
        print("  · 每敌 1 弱点(×1.5) + 1 抗性(×0.5)。元素：物理/暗/火/雷/蚀/冰/毒 → 带错元素白给")
        print("  · 敌人防御决定你要多高的档位；敌人攻击决定你要不要带护具")
        print("  · 法球带哪颗 = 选哪种战术：黑暗=暗蚀术(无视半防) 火焰=焚魂火(灼烧) 闪电=连锁雷弧(三段)")
        print("                    腐蚀=蚀甲咒(削防) 霜冻=霜锁(冻一回合) 毒液=蚀骨毒(削弱敌攻)")
        print("  · 饰品·特殊 能叠多件：凯达琳水晶=回灵 神经吊坠/法师长袍=法术强度 护盾发生器=力场 风暴罗盘=预判")
        print("· GM 只给情报不替你决定：打还是撤你说了算")
        print("· 劣势战(战力比<1)收益更好：钱最多×1.8，掉落率最高+40% —— 可以赌")
        print("· 失败代价：装备不扣，扣钱（小怪15%/Boss30%），退回本幕起点")
        print("· 🏠 每次探索前自动回基地：血量免费回满。钱只用来抽卡")
        print("· 逃跑是竞速判定：脚力(战力+鞋子) vs 它的压迫(攻击力)。速度之靴 +45%")
        print("· 🎁 每幕 2→5 个宝箱（Act4/5 各含一个大宝箱，一开两抽）：`冒险 开箱`——可能是真宝箱（钱+材料+1~2 件全局等概率装备），也可能是宝箱怪（开打）。怕了就 `冒险 绕开`")
        return

    if st["over"]:
        print("🏁 本局已结束（" + ("通关！" if st.get("won") else "失败") + "）。用 `冒险 开始` 重开。")
        return

    p = loadout_stats(s, st["loadout"])
    if st.get("hp") is None:
        st["hp"] = p["hp_max"]

    if sub == "状态":
        act = ACTS[st["act"]]
        print(f"📍 第 {st['act']+1}/5 幕：{act['name']}")
        print(f"❤️ 血量 {st['hp']} / {p['hp_max']}　💰 钱 {s['money']}")
        print(f"🏆 已击败 {st['cleared']} 个敌人　💀 阵亡 {st.get('deaths',0)} 次")
        print()
        print_loadout(s, st)
        print_equippable(s, st)
        if st.get("foe"):
            print()
            print("⚠ 当前有敌情，先侦察再配装：")
            scout_report(s, st, st["foe"], st["foe"].get("boss", False))
        if st.get("chest"):
            print()
            print(f"🎁 眼前宝箱：{st['chest']['name']} —— {st['chest']['flavor']}")
            print("   要 `冒险 开箱` 还是 `冒险 绕开`？")
        if st.get("chest_act") == st["act"] and st.get("chests"):
            print(f"   本幕还剩 {len(st['chests'])} 个宝箱未遇到。")
        return

    if sub == "战报":
        if not st["log"]:
            print("还没有战斗记录。")
            return
        for l in st["log"][-30:]:
            print(l)
        return

    if sub == "休息":
        # 基地免费回血 —— 休息只是补满的快捷方式
        p = loadout_stats(s, st["loadout"])
        before = st["hp"]
        st["hp"] = p["hp_max"]
        mod.save_state(s)
        save_adv(st)
        print(f"🏠 回到基地。免费回满：血量 {before} → {st['hp']}/{p['hp_max']}")
        return

    if sub == "配装":
        if len(args) < 2:
            print("用法：冒险 配装 <序号,序号,...>　序号见 `冒险 状态` 的清单")
            print(f"      武器最多 {WEAPON_CAP} 把，饰品/特殊最多 {TRINKET_CAP} 件，总件数不限；`冒险 配装 0` 全部卸下")
            return
        raw = args[1]
        pool = equippable_of(s)
        try:
            idxs = [int(x) for x in raw.replace("，", ",").split(",") if x.strip() != ""]
        except ValueError:
            print("序号得是数字。")
            return
        if not idxs or idxs == [0]:
            st["loadout"]["items"] = []
            save_adv(st)
            print("✅ 全部卸下。")
        else:
            if len(set(idxs)) != len(idxs):
                print("序号有重复。")
                return
            if any(i < 1 or i > len(pool) for i in idxs):
                print(f"序号无效。可选 1-{len(pool)}。")
                return
            sel = [pool[i - 1] for i in idxs]
            wcnt = sum(1 for it in sel if group_key(it) == "武器")
            tcnt = sum(1 for it in sel if group_key(it) == "饰品")
            if wcnt > WEAPON_CAP:
                print(f"武器最多带 {WEAPON_CAP} 把，你选了 {wcnt} 把。")
                return
            if tcnt > TRINKET_CAP:
                print(f"饰品/特殊最多 {TRINKET_CAP} 件，你选了 {tcnt} 件。")
                return
            st["loadout"]["items"] = [pool[i - 1]["iid"] for i in idxs]
            save_adv(st)
            print(f"✅ 已配 {len(idxs)} 件。")
        print()
        print_loadout(s, st)
        return

    if sub == "撤退":
        return do_flee(mod, s, st)

    if sub == "开箱":
        if not st.get("chest"):
            print("当前没有宝箱可开。先 `冒险 探索`。")
            return
        act = ACTS[st["act"]]
        chest = st["chest"]
        st["chest"] = None
        if random.random() < chest.get("mimic_chance", 0.0):
            mimic = make_mimic(act)
            ratio = scout_report(s, st, mimic, False)
            st["foe"] = mimic
            st["foe"]["ratio"] = ratio
            save_adv(st)
            print("💢 宝箱猛地裂开——是宝箱怪！")
            return
        # 真宝箱：开箱得奖励（钱 + 材料 + 固定抽数，全局等概率六档）
        s["money"] += chest.get("money", 0)
        m = chest.get("material")
        mn = chest.get("material_n", 0)
        if m and mn:
            s["materials"][m] = s["materials"].get(m, 0) + mn
        lines = [f"💰 宝箱里翻出 {chest.get('money', 0)} 钱"]
        if m and mn:
            lines.append(f"🧪 {m}×{mn}")
        for _ in range(chest.get("draws", 1)):
            item = drop_item(mod, s, GLOBAL_DROP)
            lines.append(f"🎁 抽出装备：{cname(item)}")
        for l in lines:
            print("   " + l)
        mod.save_state(s)
        save_adv(st)
        print("   继续 `冒险 探索`。")
        return

    if sub == "绕开":
        if st.get("chest"):
            st["chest"] = None
            save_adv(st)
            print("🚶 你绕开了宝箱，继续前进。")
            print("   继续 `冒险 探索`。")
            return
        print("当前没有可绕开的宝箱。")
        return

    if sub == "出战":
        if not st.get("foe"):
            print("当前没有敌情。先 `冒险 探索`。")
            return
        enemy = dict(st["foe"])
        is_boss = enemy.pop("boss", False)
        ratio = st["foe"].get("ratio", 1.0)
        st["foe"] = None
        p = loadout_stats(s, st["loadout"])
        if st["hp"] > p["hp_max"]:
            st["hp"] = p["hp_max"]
        print(f"⚔️  开战：{enemy['name']}")
        print(f"    你的配装战力 {p['power']}　攻 {p['atk']:.0f}　防 {p['df']:.0f}　血 {st['hp']}/{p['hp_max']}")
        print()
        result, log = auto_battle(mod, s, st, enemy, is_boss, ratio)
        for l in log:
            print(l)
        st["log"].append(f"〔{enemy['name']}〕" + ("　".join(log)))
        if result == "win":
            st["cleared"] += 1
            for l in reward(mod, s, st["act"], is_boss, ratio):
                print("   " + l)
            st["step"] += 1
            act = ACTS[st["act"]]
            if st["step"] > len(act["foes"]):
                if st["act"] >= len(ACTS) - 1:
                    st["over"] = True
                    st["won"] = True
                    print("🏆 虚空之门打开，你活着走了出来。五幕通关。")
                    print(f"   最终战力 {loadout_stats(s, st['loadout'])['power']}　"
                          f"击败 {st['cleared']} 个敌人　阵亡 {st.get('deaths',0)} 次　剩余 {s['money']} 钱")
                else:
                    st["act"] += 1
                    st["step"] = 0
                    st["hp"] = loadout_stats(s, st["loadout"])["hp_max"]
                    print(f"✅ {act['name']} 肃清。血量回满，进入第 {st['act']+1} 幕：{ACTS[st['act']]['name']}")
            mod.save_state(s)
            save_adv(st)
            print(f"❤️ 血量 {st['hp']} / {loadout_stats(s, st['loadout'])['hp_max']}　💰 钱 {s['money']}")
            return
        if result == "defeat":
            pct = 0.30 if is_boss else 0.15
            loss = int(s["money"] * pct)
            s["money"] -= loss
            np = loadout_stats(s, st["loadout"])
            st["hp"] = int(np["hp_max"] * 0.5)
            st["step"] = 0
            st["deaths"] = st.get("deaths", 0) + 1
            st["cleared"] = max(0, st["cleared"] - 1)
            mod.save_state(s)
            save_adv(st)
            print("💀 你被击败了。")
            print(f"    装备一件没丢，但被搜走 {loss} 钱（{'Boss' if is_boss else '小怪'}战）。")
            print(f"    退回本幕起点，血量恢复 50%（{st['hp']}/{np['hp_max']}）。")
            print(f"    → 换套配装再来，或者先 `冒险 休息` 回满血。")
            return
        # 平局
        mod.save_state(s)
        save_adv(st)
        print("⏳ 打了个平手，敌人退开了。")
        return

    if sub != "探索":
        print("未知子命令。可用：开始/状态/探索/配装/出战/开箱/绕开/休息/撤退/战报/指南")
        return

    # ---- 探索 ----
    act = ACTS[st["act"]]
    # 本幕宝箱队列：换幕或直接写入存档时自动就位（不重复、不丢已开的）
    if st.get("chest_act") != st["act"]:
        # 只收当前步及之后的宝箱；半路接档时，已经错过的（step 更小）直接丢弃
        st["chests"] = [dict(c) for c in act.get("chests", []) if c.get("step", 0) >= st["step"]]
        st["chest_act"] = st["act"]
        save_adv(st)

    if st.get("foe"):
        print("⚠ 眼前还有敌人。先配装并 `冒险 出战`，或 `冒险 撤退` 放弃。")
        scout_report(s, st, st["foe"], st["foe"].get("boss", False))
        return

    if st.get("chest"):
        print(f"🎁 眼前有个宝箱：{st['chest']['name']}")
        print(f"   {st['chest']['flavor']}")
        print("   要 `冒险 开箱` 碰碰运气，还是 `冒险 绕开` 走开？")
        return

    # 回基地：免费回满血
    p = loadout_stats(s, st["loadout"])
    if st["hp"] < p["hp_max"]:
        st["hp"] = p["hp_max"]
        save_adv(st)

    # 本幕敌人：按场景顺序依次打 foes 里的每一个，全打完再打 Boss（不按步数卡）
    n = len(act["foes"])
    is_boss = (st["step"] >= n)

    # 宝箱：本幕尚未开启的宝箱里，挑一个当前步的（同一步有多个就逐个来）
    if not is_boss:
        for i, c in enumerate(st["chests"]):
            if c["step"] == st["step"]:
                st["chest"] = st["chests"].pop(i)
                save_adv(st)
                print(f"🎁 发现一个宝箱：{st['chest']['name']}")
                print(f"   {st['chest']['flavor']}")
                print("   `冒险 开箱` 开启（可能是宝箱怪）／`冒险 绕开` 走开")
                return

    enemy = make_foe(act, is_boss, None if is_boss else st["step"])
    ratio = scout_report(s, st, enemy, is_boss)
    st["foe"] = enemy
    st["foe"]["ratio"] = ratio
    save_adv(st)


def reward(mod, s, act_idx, is_boss, ratio):
    lines = []
    risk = max(0.0, 1.0 - ratio)
    money_mult = 1.0 + risk * 0.8
    money = int(ACTS[act_idx]["money"] * random.uniform(0.75, 1.3)
                * (4.0 if is_boss else 1.0) * money_mult)
    s["money"] += money
    lines.append(f"💰 获得 {money} 钱" + (f"（险胜加成 ×{money_mult:.2f}）" if money_mult > 1.01 else ""))

    mats = []
    r = random.random()
    if act_idx <= 1:
        if r < 0.30 + risk * 0.2:
            mats.append("星尘结晶")
    elif act_idx <= 3:
        if r < 0.25 + risk * 0.2:
            mats.append("星尘结晶")
        if r < 0.45 + risk * 0.2:
            mats.append("太古原石")
    else:
        if r < 0.25 + risk * 0.2:
            mats.append("太古原石")
        if r < 0.37 + risk * 0.2:
            mats.append(random.choice(["Gem of the Space", "Mirror of the Void"]))
    for m in set(mats):
        s["materials"][m] += 1
    if mats:
        lines.append("🧪 材料：" + "、".join(f"{m}×{s['materials'][m]}" for m in sorted(set(mats))))

    if is_boss or random.random() < 0.35 + risk * 0.4:
        w = dict(DROP_WEIGHTS[act_idx])
        if is_boss:
            for k in w:
                w[k] = w[k] * 0.7 + 8
        item = drop_item(mod, s, w)
        lines.append(f"🎁 掉落：{item['tier']} · {item['name']}（{item['iid']}）")
    return lines


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    mod = load_engine()
    if args[0] == "送":
        base = args[1]
        tier = args[2] if len(args) > 2 else "银河"
        item = gift(mod, base, tier)
        print(f"🎁 GM 投递：{item['tier']} · {item['slot']} · {item['name']}")
        print(f"   实例 {item['iid']}")
        print(f"   基础模板：{item['base']}（随机生成，非固定暗金）")
    elif args[0] == "冒险":
        cmd_adv(mod, args[1:])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
