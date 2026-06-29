"""
战斗状态跟踪器（JSON持久化）—— dnd-engine 版

继承自上游战斗状态模块，去掉：
  - get_combat_table() / build_combat_table（展示层，不在引擎）
  - new_combat() 中未使用的 display import
"""

DEPRECATED: file-based persistence. Use the campaign database instead.

This module exists only for backward compatibility with older dnd-engine
workflows. NanoBot stores all campaign state in the SQL database via
CampaignSnapshotService / CampaignService / ModuleProgressService.
No new code should call this module.
import json
import os
from datetime import datetime

COMBAT_FILE = 'combat_state.json'


def new_combat(combat_name, location, combatants):
    sorted_units = sorted(combatants, key=lambda x: x.get('initiative', 0), reverse=True)
    state = {
        "combat_name": combat_name,
        "location": location,
        "round": 1,
        "current_turn": 0,
        "is_active": True,
        "started_at": datetime.now().isoformat(),
        "units": sorted_units,
        "log": [f"⚔️ {combat_name} 开始！位置：{location}"],
        "environment": {"terrain": "", "light": "", "special": ""},
    }
    save_combat(state)
    return state


def save_combat(state):
    with open(COMBAT_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def load_combat():
    if not os.path.exists(COMBAT_FILE):
        return None
    try:
        with open(COMBAT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def get_current_turn_unit(state):
    idx = state['current_turn']
    if idx < len(state['units']):
        return state['units'][idx]
    return None


def advance_turn(state):
    state['current_turn'] += 1
    while state['current_turn'] < len(state['units']):
        if state['units'][state['current_turn']].get('status') != '死亡':
            break
        state['current_turn'] += 1
    if state['current_turn'] >= len(state['units']):
        state['round'] += 1
        state['current_turn'] = 0
        for unit in state['units']:
            if unit.get('status') != '死亡':
                unit['status'] = '等待'
        state['log'].append(f"--- 第 {state['round']} 轮 ---")
    save_combat(state)
    return state


def apply_damage(state, unit_name, damage, source=""):
    unit = _find_unit(state, unit_name)
    if not unit:
        return None
    old_hp = unit['hp']
    unit['hp'] = max(0, unit['hp'] - damage)
    log_msg = f"{unit_name} 受到 {damage} 点伤害 ({old_hp}→{unit['hp']})"
    if source:
        log_msg += f" [来源: {source}]"
    if unit['hp'] == 0:
        unit['status'] = '死亡'
        log_msg += " 💀已死亡"
    state['log'].append(log_msg)
    save_combat(state)
    return unit


def heal_unit(state, unit_name, heal):
    unit = _find_unit(state, unit_name)
    if not unit:
        return None
    old_hp = unit['hp']
    unit['hp'] = min(unit.get('maxHp', 999), unit['hp'] + heal)
    state['log'].append(f"{unit_name} 恢复 {heal} HP ({old_hp}→{unit['hp']})")
    save_combat(state)
    return unit


def set_status(state, unit_name, status):
    unit = _find_unit(state, unit_name)
    if not unit:
        return False
    unit['status'] = status
    save_combat(state)
    return True


def add_effect(state, unit_name, effect_name, duration, effect_desc):
    unit = _find_unit(state, unit_name)
    if not unit:
        return False
    if 'effects' not in unit:
        unit['effects'] = []
    unit['effects'].append({
        "name": effect_name,
        "duration": duration,
        "remaining": duration,
        "desc": effect_desc,
    })
    state['log'].append(f"{unit_name} 获得 {effect_name}（持续{duration}回合）")
    save_combat(state)
    return True


def tick_effects(state):
    for unit in state['units']:
        if unit.get('effects'):
            remaining = []
            for eff in unit['effects']:
                eff['remaining'] -= 1
                if eff['remaining'] > 0:
                    remaining.append(eff)
                else:
                    state['log'].append(f"{unit['name']} 的 {eff['name']} 已结束")
            unit['effects'] = remaining
    save_combat(state)
    return state


def end_combat(state, result):
    state['is_active'] = False
    state['result'] = result
    state['log'].append(f"战斗结束：{result}")
    save_combat(state)


def get_combat_summary(state):
    living = [u for u in state['units'] if u.get('status') != '死亡']
    dead = [u for u in state['units'] if u.get('status') == '死亡']
    cur = get_current_turn_unit(state)
    return (
        f"⚔️ 第{state['round']}轮 | 存活{len(living)}人 | 死亡{len(dead)}人\n"
        f"当前行动: {cur['name'] if cur else '?'}"
    )


def clear():
    if os.path.exists(COMBAT_FILE):
        os.remove(COMBAT_FILE)


def _find_unit(state, name):
    for unit in state['units']:
        if unit.get('name') == name:
            return unit
    return None
