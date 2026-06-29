"""
角色与任务数据模板工厂

替换 DM_RULES.md 中的 JSON schema 定义表。
LLM 不再需要自己拼 JSON 结构——调此模块获取标准模板即可。
"""
def make_role_stats(**overrides):
    """角色六维属性模板"""
    default = {"str": 10, "dex": 10, "con": 10, "int": 10, "wis": 10, "cha": 10}
    default.update(overrides)
    return default


def make_character_template(name="新角色", **overrides):
    """角色数据模板 -> 对应数据库中的角色状态。"""
    template = {
        "name": name,
        "race": "",
        "class": "",
        "level": 1,
        "xp": 0,
        "lvlUpXp": 300,
        "stats": make_role_stats(),
        "proficiencyBonus": 2,
        "hp": {"current": 10, "max": 10, "temp": 0},
        "ac": 10,
        "initiative": 0,
        "speed": 30,
        "passivePerception": 10,
        "skills": {
            "察觉": False, "隐匿": False, "潜行": False, "巧手": False,
            "游说": False, "威吓": False, "欺瞒": False, "运动": False,
            "特技": False, "杂技": False, "洞悉": False, "医药": False,
            "历史": False, "宗教": False, "奥秘": False, "调查": False,
            "自然": False, "驯兽": False, "表演": False, "生存": False,
        },
        "savingThrows": {
            "力量": False, "敏捷": False, "体质": False,
            "智力": False, "感知": False, "魅力": False,
        },
        "feats": [],
        "classFeatures": [],
        "raceTraits": [],
        "spellSlots": {},
        "spells": [],
        "spellcastingAbility": "",
        "equipment": {},
        "inventory": [],
        "activeEffects": [],
        "notes": "",
    }
    template.update(overrides)
    return template


def make_quest_template(quest_id="", title="", status="pending", desc=""):
    """任务数据模板"""
    return {
        "id": quest_id,
        "title": title,
        "status": status,   # pending / active / completed / failed
        "desc": desc,
    }


def make_combatant_template(name="", hp=10, max_hp=10, initiative=10, ac=10, **extra):
    """战斗参战者模板"""
    entry = {
        "name": name,
        "hp": hp,
        "maxHp": max_hp,
        "initiative": initiative,
        "ac": ac,
        "status": "等待",
    }
    entry.update(extra)
    return entry
