"""
模组内容预加载缓存 —— 避免 LLM 反复读取文件
"""

DEPRECATED: file-based persistence. Use the campaign database instead.

This module exists only for backward compatibility with older dnd-engine
workflows. NanoBot stores all campaign state in the SQL database via
CampaignSnapshotService / CampaignService / ModuleProgressService.
No new code should call this module.
import os
import json
import re

CACHE_FILE = 'module_cache.json'

def load_chapter_cache(module_name, chapter_num):
    """
    加载指定章节到缓存（读取并缓存结构化的章节内容）
    
    从 modules/ 读取文件 → 按段落标记解析 → 缓存到 module_cache.json
    后续访问直接读缓存，不再读文件
    
    参数:
        module_name: str - 模组名
        chapter_num: int - 章节号
    
    返回:
        dict: {"scenes": [...], "npcs": [...], "encounters": [...], "locations": [...]}
    """
    # 尝试读缓存
    cache = _read_cache()
    cache_key = f"{module_name}_Ch{chapter_num}"
    
    if cache_key in cache:
        return cache[cache_key]
    
    # 从文件加载
    from dnd_engine.module.scanner import read_chapter
    result = read_chapter(module_name, chapter_num)
    if not result:
        return None
    
    content = result['content']
    
    # 按场景标记解析
    parsed = {
        "module": module_name,
        "chapter": chapter_num,
        "filename": result['filename'],
        "scenes": _parse_scenes(content),
        "npcs": _parse_npcs(content),
        "encounters": _parse_encounters(content),
        "locations": _parse_locations(content),
        "text": content,  # 保留完整原文
    }
    
    # 写入缓存
    cache[cache_key] = parsed
    _write_cache(cache)
    
    return parsed


def get_scene(cache_entry, scene_name):
    """从已加载的章节中获取指定场景"""
    if not cache_entry:
        return None
    for s in cache_entry.get('scenes', []):
        if scene_name.lower() in s.get('name', '').lower():
            return s
    return None


def get_scene_text(cache_entry, scene_name):
    """获取场景的纯文本内容"""
    scene = get_scene(cache_entry, scene_name)
    return scene.get('text', '') if scene else ''


def get_npc_info(cache_entry, npc_name):
    """获取 NPC 信息"""
    if not cache_entry:
        return None
    for n in cache_entry.get('npcs', []):
        if npc_name.lower() in n.get('name', '').lower():
            return n
    return None


def get_encounter(cache_entry, encounter_name):
    """获取遭遇信息"""
    if not cache_entry:
        return None
    for e in cache_entry.get('encounters', []):
        if encounter_name.lower() in e.get('name', '').lower():
            return e
    return None


def get_location(cache_entry, location_name):
    """获取地点信息"""
    if not cache_entry:
        return None
    for l in cache_entry.get('locations', []):
        if location_name.lower() in l.get('name', '').lower():
            return l
    return None


def clear_cache():
    """清除缓存"""
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)


def _read_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def _write_cache(cache):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def _parse_scenes(content):
    """解析场景段落"""
    scenes = []
    # 匹配 "**场景**"、"**遭遇**"、"###" 等段落标记
    for match in re.finditer(r'(?:^|\n)(?:\*{1,2}|#)\s*(场景|遭遇|事件)\s*\*{0,2}\s*(.+?)(?:\n|$)', content, re.MULTILINE):
        scenes.append({
            "name": match.group(2).strip(),
            "type": match.group(1),
            "text": _extract_section(content, match.end()),
        })
    return scenes


def _parse_npcs(content):
    """解析 NPC"""
    npcs = []
    for match in re.finditer(r'(?:^|\n)\*{1,2}(?:NPC|人物|角色)\s*\*{0,2}\s*(.+?)(?:\n|$)', content, re.MULTILINE):
        npcs.append({
            "name": match.group(1).strip(),
            "text": _extract_section(content, match.end()),
        })
    return npcs


def _parse_encounters(content):
    """解析遭遇"""
    encounters = []
    for match in re.finditer(r'(?:^|\n)\*{1,2}遭遇\s*\*{0,2}\s*(.+?)(?:\n|$)', content, re.MULTILINE):
        encounters.append({
            "name": match.group(1).strip(),
            "text": _extract_section(content, match.end()),
        })
    return encounters


def _parse_locations(content):
    """解析地点标记"""
    locations = []
    for match in re.finditer(r'(?:^|\n)\*{1,2}地点\s*\*{0,2}\s*(.+?)(?:\n|$)', content, re.MULTILINE):
        locations.append({
            "name": match.group(1).strip(),
            "text": _extract_section(content, match.end()),
        })
    return locations


def _extract_section(content, start_pos):
    """从当前位置提取到下一个段落标题前的内容"""
    remaining = content[start_pos:]
    next_heading = re.search(r'(?:^|\n)(?:\*{1,2}|#)\s*(?:场景|遭遇|事件|NPC|人物|角色|地点)\s*\*{0,2}', remaining)
    if next_heading:
        return remaining[:next_heading.start()].strip()
    return remaining.strip()
