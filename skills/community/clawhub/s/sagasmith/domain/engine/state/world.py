"""
世界状态管理：派系关系、任务进度、已发现地点、关键NPC状态
"""

DEPRECATED: file-based persistence. Use the campaign database instead.

This module exists only for backward compatibility with older dnd-engine
workflows. NanoBot stores all campaign state in the SQL database via
CampaignSnapshotService / CampaignService / ModuleProgressService.
No new code should call this module.
import json
import os

WORLD_STATE_FILE = 'world_state.json'


def get_default_world_state():
    """返回默认世界状态结构"""
    return {
        "faction_relations": {},
        "discovered_locations": [],
        "quest_progress": {
            "完成": [],
            "进行中": [],
            "待触发": []
        },
        "key_npc_status": {},
        "current_chapter": 0,
        "current_scene": "",
        "day_in_game": 1,
    }


def load_world_state(filepath=None):
    """加载世界状态"""
    path = filepath or WORLD_STATE_FILE
    if not os.path.exists(path):
        return get_default_world_state()
    with open(path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            # Ensure all keys exist
            default = get_default_world_state()
            for key in default:
                if key not in data:
                    data[key] = default[key]
            return data
        except json.JSONDecodeError:
            return get_default_world_state()


def save_world_state(state, filepath=None):
    """保存世界状态"""
    path = filepath or WORLD_STATE_FILE
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    return path


def update_faction(world, faction_name, delta, note=""):
    """
    更新派系关系

    参数:
        world: dict - 世界状态
        faction_name: str - 派系名
        delta: int - 变化量 (+/-)
        note: str - 变更原因

    返回:
        str: 变更后的关系摘要
    """
    current = world['faction_relations'].get(faction_name, 0)
    current += delta
    world['faction_relations'][faction_name] = current

    if current >= 3:
        desc = "盟友"
    elif current >= 1:
        desc = "友好"
    elif current >= -1:
        desc = "中立"
    elif current >= -3:
        desc = "敌对"
    else:
        desc = "死仇"

    if note:
        print(f"[世界状态] {faction_name} 关系 {delta:+d} → {current} ({desc}): {note}")
    return f"{faction_name}: {current} ({desc})"


def discover_location(world, location_name):
    """
    记录发现新地点

    参数:
        world: dict
        location_name: str - 地点名
    """
    if location_name not in world['discovered_locations']:
        world['discovered_locations'].append(location_name)
        print(f"[世界状态] 发现新地点: {location_name}")


def update_quest(world, quest_name, new_status):
    """
    更新任务状态

    参数:
        world: dict
        quest_name: str - 任务名
        new_status: str - 完成 / 进行中 / 待触发 / 已失败
    """
    old_status = None
    for status_key in ['完成', '进行中', '待触发', '已失败']:
        if quest_name in world['quest_progress'].get(status_key, []):
            old_status = status_key
            world['quest_progress'][status_key].remove(quest_name)
            break

    world['quest_progress'].setdefault(new_status, [])
    world['quest_progress'][new_status].append(quest_name)
    print(f"[世界状态] 任务更新: {quest_name}: {old_status} → {new_status}")


def update_npc_status(world, npc_name, status):
    """
    更新NPC状态

    参数:
        world: dict
        npc_name: str
        status: str - 例如 "存活·友好", "已击倒", "待救援·未见面"
    """
    world['key_npc_status'][npc_name] = status
    print(f"[世界状态] NPC状态更新: {npc_name} → {status}")


def get_world_summary(world):
    """
    生成世界状态摘要（50-100 token）

    参数:
        world: dict

    返回:
        str: 摘要文本
    """
    lines = []

    # Chapter and scene
    lines.append(f"第{world.get('current_chapter', '?')}章·{world.get('current_scene', '?')} 游戏日#{world.get('day_in_game', 1)}")

    # Factions (compact)
    factions = world.get('faction_relations', {})
    if factions:
        desc_map = {
            5: '盟友', 4: '盟友', 3: '盟友',
            2: '友好', 1: '友好',
            0: '中立', -1: '中立',
            -2: '敌对', -3: '敌对',
            -4: '死仇', -5: '死仇'
        }
        faction_strs = []
        for name, val in sorted(factions.items(), key=lambda x: -x[1]):
            desc = desc_map.get(val, '中立')
            faction_strs.append(f"{name}({desc})")
        lines.append(f"派系: {' '.join(faction_strs)}")

    # Quests
    quests = world.get('quest_progress', {})
    active = quests.get('进行中', [])
    if active:
        lines.append(f"进行中: {' → '.join(active)}")

    # NPCs
    npcs = world.get('key_npc_status', {})
    important_npcs = {k: v for k, v in npcs.items() if '待' in v or '未' in v or '敌对' in v}
    if important_npcs:
        lines.append(f"关键NPC: {' '.join(f'{n}({s})' for n, s in important_npcs.items())}")

    return ' | '.join(lines)


def advance_day(world):
    """推进游戏内一天"""
    world['day_in_game'] = world.get('day_in_game', 1) + 1


def set_current_scene_state(world, chapter, scene):
    """设置当前章节场景"""
    world['current_chapter'] = chapter
    world['current_scene'] = scene
