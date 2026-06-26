#!/usr/bin/env python3
"""
家庭收纳智能管理系统
"""

import json
import os
import re
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

# ============== 配置 ==============
# 动态获取 workspace 路径，兼容所有系统
def get_workspace_path() -> Path:
    """获取 OpenClaw workspace 路径"""
    # 优先使用环境变量
    workspace = os.environ.get("CLAW_WORKDIR") or os.environ.get("OPENCLAW_WORKDIR")
    if workspace:
        return Path(workspace)
    # 回退到 ~/.openclaw/workspace
    return Path.home() / ".openclaw" / "workspace"

WORKSPACE = get_workspace_path()
DATA_FILE = WORKSPACE / "data" / "home_storage.json"
BACKUP_DIR = WORKSPACE / "data" / "backups"

# ============== 基础函数 ==============
def load_data() -> dict:
    """加载数据"""
    if not os.path.exists(DATA_FILE):
        return {"suites": [], "version": "2.0"}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data: dict) -> None:
    """保存数据"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def now() -> str:
    """当前时间 ISO 格式"""
    return datetime.now().isoformat()

def new_id() -> str:
    """生成新 UUID"""
    return str(uuid.uuid4())

# ============== 查找函数 ==============
def find_suite(data: dict, name: str) -> Optional[dict]:
    """查找套房"""
    return next((s for s in data.get("suites", []) if s["name"] == name), None)

def find_room(suite: dict, name: str) -> Optional[dict]:
    """查找房间"""
    return next((r for r in suite.get("rooms", []) if r["name"] == name), None)

def find_furniture(room: dict, name: str) -> Optional[dict]:
    """查找家具"""
    return next((f for f in room.get("furniture", []) if f["name"] == name), None)

def find_item(furniture: dict, name: str) -> Optional[dict]:
    """查找物品"""
    return next((i for i in furniture.get("items", []) if name in i["name"]), None)

def find_item_by_id(furniture: dict, item_id: str) -> Optional[dict]:
    """根据 ID 查找物品"""
    return next((i for i in furniture.get("items", []) if i["id"] == item_id), None)

# ============== 遍历函数 ==============
def iter_all_items(data: dict):
    """遍历所有物品 (yield: suite, room, furniture, item)"""
    for suite in data.get("suites", []):
        for room in suite.get("rooms", []):
            for furniture in room.get("furniture", []):
                for item in furniture.get("items", []):
                    yield suite, room, furniture, item

def iter_all_furniture(data: dict):
    """遍历所有家具 (yield: suite, room, furniture)"""
    for suite in data.get("suites", []):
        for room in suite.get("rooms", []):
            for furniture in room.get("furniture", []):
                yield suite, room, furniture

# ============== 更新时间戳 ==============
def update_timestamp_chain(*entities: dict) -> None:
    """更新实体链的时间戳"""
    for entity in entities:
        if entity and "updatedAt" in entity:
            entity["updatedAt"] = now()

# ============== 解析函数 ==============
def parse_suite_and_rooms(text: str):
    """解析套房创建指令"""
    patterns = [
        r'(?:套房叫|添加套房[：:])(\S+?)[，,\s]+有([^\n]+)',
        r'(\S+?)[，,\s]+有([^\n]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            rooms = [r.strip() for r in re.split(r'[、,，\s]+', match.group(2)) if r.strip()]
            return match.group(1).strip(), rooms
    return None, []

def parse_add_room(text: str):
    """解析添加房间指令"""
    patterns = [r'给(.+?)加.{0,2}房间.?叫?(.+)', r'(.+?)新增(.+)']
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip(), match.group(2).strip()
    return None, None

def parse_add_furniture(text: str, data: dict):
    """解析添加家具指令"""
    suite_name = None
    # 检查 "套房的房间有个家具" 格式
    match = re.search(r'^(.+?)的(.+?)有(.+)$', text)
    if match:
        potential_suite = match.group(1).strip()
        if find_suite(data, potential_suite):
            suite_name = potential_suite
            text = match.group(2).strip() + "有" + match.group(3).strip()
    
    # 匹配 "房间有家具" 或 "房间放家具"
    for pattern in [r'^(.+?)有(?:一个|个|张|把)?(.+)$', r'(.+?)放.{0,2}个?(.+)']:
        match = re.search(pattern, text)
        if match:
            return suite_name, match.group(1).strip(), match.group(2).strip()
    return suite_name, None, None

def parse_add_item(text: str):
    """解析添加物品指令"""
    quantity = 1
    # 提取数量
    q_match = re.search(r'数量[是为：:]?\s*(\d+)', text)
    if q_match:
        quantity = int(q_match.group(1))
    else:
        q_match = re.search(r'(\d+)个?', text)
        if q_match:
            quantity = int(q_match.group(1))
    
    # 提取物品名
    item_match = re.search(r'把(.+?)放', text)
    if not item_match:
        item_match = re.search(r'放.{0,2}个?(.+?)(?:在|到|里)', text)
    if not item_match:
        return None, None, None, quantity
    item_name = item_match.group(1).strip()
    
    # 提取位置
    location_match = re.search(r'在(.+?)(?:的|里)', text)
    if not location_match:
        location_match = re.search(r'(.+?)的(.+?)里', text)
    location = location_match.group(1).strip() if location_match else None
    
    return item_name, location, None, quantity

def parse_query_item(text: str) -> Optional[str]:
    """解析查询物品指令"""
    patterns = [r'我的(.+?)(?:放在|在)', r'我的(.+?)在哪', r'(.+?)在哪里', r'查.{0,2}(.+)']
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    return None

def parse_recommend(text: str) -> Optional[str]:
    """解析推荐位置指令"""
    # 匹配 "推荐存放位置 XXX" 或 "推荐位置 XXX" 或 "XXX 放哪"
    patterns = [r'推荐存放位置\s*(.+)', r'推荐位置\s*(.+)', r'(.+?)\s*放哪', r'哪里放(.+)']
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    # 如果没有匹配前缀，直接返回原文作为物品名
    if text.strip():
        return text.strip()
    return None

def parse_merge_item(text: str) -> tuple:
    """解析合并命令，格式：'遥控器 客厅-电视柜' 或 '遥控器|客厅-电视柜'"""
    text = text.strip()
    if '|' in text:
        parts = text.split('|')
        if len(parts) >= 2:
            return parts[0].strip(), parts[1].strip()
    parts = text.split()
    if len(parts) >= 2:
        return parts[0], parts[1]
    return None, None

def parse_continue_add(text: str) -> tuple:
    """解析继续添加命令，格式：'遥控器|卧室床头柜|1'"""
    text = text.strip()
    if '|' in text:
        parts = text.split('|')
        item_name = parts[0].strip() if len(parts) > 0 else None
        location = parts[1].strip() if len(parts) > 1 else None
        quantity = int(parts[2].strip()) if len(parts) > 2 else 1
        return item_name, location, quantity
    return None, None, 1

def parse_move_item(text: str):
    """解析搬动物品指令"""
    match = re.search(r'把(.+?)搬到(.+)', text)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    match = re.search(r'把(.+?)移到(.+)', text)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return None, None

def parse_delete_item(text: str) -> Optional[str]:
    """解析删除物品指令"""
    patterns = [r'删除(.+)', r'把(.+?)扔了']
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    return None

# ============== 智能推荐 ==============
LOCATION_RECOMMENDATIONS = {
    # 电器类
    "电器": ["电视柜", "抽屉", "收纳盒"],
    "遥控器": ["电视柜", "茶几", "沙发"],
    "充电器": ["电视柜", "抽屉", "书桌"],
    "充电宝": ["电视柜", "抽屉", "书包"],
    "耳机": ["电视柜", "抽屉", "书桌"],
    "手机": ["电视柜", "书桌", "床头柜"],
    "平板": ["电视柜", "书桌", "书架"],
    "电脑": ["书桌", "电视柜", "抽屉"],
    "笔记本": ["书桌", "书架", "抽屉"],
    "键盘": ["书桌", "电视柜"],
    "鼠标": ["书桌", "电视柜"],
    
    # 书籍类
    "书": ["书架", "书柜", "书桌"],
    "杂志": ["书架", "茶几", "沙发"],
    "漫画": ["书架", "书柜"],
    "笔记本": ["书架", "书桌", "抽屉"],
    "本子": ["书架", "书桌", "抽屉"],
    
    # 衣物类
    "衣服": ["衣柜", "抽屉", "收纳箱"],
    "裤子": ["衣柜", "抽屉"],
    "裙子": ["衣柜", "收纳箱"],
    "外套": ["衣柜", "衣架"],
    "内衣": ["衣柜", "抽屉"],
    "袜子": ["衣柜", "抽屉", "收纳盒"],
    "帽子": ["衣柜", "衣架", "挂钩"],
    "围巾": ["衣柜", "衣架", "挂钩"],
    "手套": ["衣柜", "抽屉", "收纳盒"],
    
    # 被褥类
    "被子": ["衣柜", "储物箱", "床底"],
    "毯子": ["衣柜", "沙发", "储物箱"],
    "枕头": ["床", "沙发", "衣柜"],
    "床单": ["衣柜", "抽屉", "储物箱"],
    "被套": ["衣柜", "抽屉", "储物箱"],
    
    # 食品类
    "零食": ["抽屉", "茶几", "柜子"],
    "饮料": ["冰箱", "抽屉", "茶几"],
    "水": ["冰箱", "茶几", "抽屉"],
    "茶叶": ["茶几", "抽屉", "柜子"],
    "咖啡": ["茶几", "抽屉", "柜子"],
    "方便面": ["抽屉", "柜子", "厨房"],
    "苹果": ["厨房", "冰箱", "餐桌"],
    "水果": ["厨房", "冰箱", "餐桌"],
    
    # 药品类
    "药": ["抽屉", "柜子", "床头柜"],
    "创可贴": ["抽屉", "医药箱"],
    "体温计": ["抽屉", "医药箱"],
    
    # 日常用品
    "钥匙": ["玄关", "挂钩", "抽屉"],
    "钱包": ["玄关", "衣柜", "书桌"],
    "卡": ["钱包", "抽屉", "书桌"],
    "证件": ["抽屉", "柜子", "书桌"],
    "伞": ["玄关", "门口", "阳台"],
    "包": ["玄关", "衣柜", "挂钩"],
    "书包": ["玄关", "书桌", "椅子"],
    
    # 化妆品
    "化妆品": ["抽屉", "卫生间", "化妆台"],
    "护肤品": ["抽屉", "卫生间", "化妆台"],
    "口红": ["抽屉", "化妆台"],
    "香水": ["化妆台", "抽屉", "柜子"],
    
    # 工具类
    "工具": ["抽屉", "柜子", "阳台"],
    "螺丝刀": ["抽屉", "工具箱"],
    "锤子": ["抽屉", "阳台", "工具箱"],
    "剪刀": ["抽屉", "厨房", "工具箱"],
    "胶带": ["抽屉", "书桌", "工具箱"],
    
    # 玩具
    "玩具": ["玩具箱", "书架", "抽屉"],
    "游戏机": ["电视柜", "书桌", "抽屉"],
    "积木": ["玩具箱", "书架", "抽屉"],
    
    # 运动类
    "运动": ["阳台", "抽屉", "柜子"],
    "瑜伽垫": ["阳台", "角落", "收纳筒"],
    "跳绳": ["阳台", "挂钩", "抽屉"],
    "球": ["阳台", "角落", "收纳箱"],
}

def get_recommendation(item_name: str, data: dict) -> list:
    """根据物品名获取推荐存放位置"""
    recommendations = []
    item_lower = item_name.lower()
    
    for keyword, locations in LOCATION_RECOMMENDATIONS.items():
        if keyword in item_lower:
            recommendations.extend(locations)
    
    # 如果没有关键词匹配，返回通用推荐
    if not recommendations:
        recommendations = ["抽屉", "柜子", "收纳盒", "电视柜"]
    
    # 去重并过滤实际存在的家具
    recommendations = list(dict.fromkeys(recommendations))
    
    # 检查哪些推荐位置实际存在
    existing_furniture = []
    for s, r, f in iter_all_furniture(data):
        existing_furniture.append((s["name"], r["name"], f["name"]))
    
    matched = []
    for rec in recommendations:
        for sf, rf, ff in existing_furniture:
            if rec in ff or rec in rf:
                matched.append(f"{rf}-{ff}")
    
    return matched[:5] if matched else ["请先添加家具"]

def check_location_recommendation(item_name: str, target_room_name: str, data: dict) -> tuple:
    """检查目标位置是否在推荐位置中，返回 (是否推荐, 提示信息)"""
    recommendations = []
    item_lower = item_name.lower()
    
    # 查找物品类型的推荐
    for keyword, locations in LOCATION_RECOMMENDATIONS.items():
        if keyword in item_lower:
            recommendations.extend([loc.lower() for loc in locations])
    
    if not recommendations:
        return True, ""  # 没有推荐，按用户意图来
    
    # 检查目标房间是否在推荐中
    target_room_lower = target_room_name.lower()
    for rec in recommendations:
        if rec in target_room_lower or target_room_lower in rec:
            return True, ""
    
    # 不在推荐位置，检查全屋是否有推荐位置
    similar = []
    for s, r, f, i in iter_all_items(data):
        i_name_lower = i["name"].lower()
        if i_name_lower == item_lower:
            similar.append({"room": r["name"], "furniture": f["name"]})
    
    if similar:
        # 有同类物品在其他位置
        loc_str = f"{similar[0]['room']}-{similar[0]['furniture']}"
        return False, f"""💡 '{item_name}' 通常放在：{', '.join(recommendations)}
━━━━━━━━━━━━━━━━━━━━━━
当前你想放到：{target_room_name}
全屋已有：{loc_str}
━━━━━━━━━━━━━━━━━━━━━━
【是】→ 归纳到 {loc_str}
【否】→ 坚持放到 {target_room_name}"" [TARGET:{similar[0]['room']}-{similar[0]['furniture']}]
[CONTEXT:item={item_name}|location={target_room_name}|quantity=1]"""
    
    # 没有同类物品，但位置不推荐
    return False, f"""💡 '{item_name}' 通常放在：{', '.join(recommendations)}
━━━━━━━━━━━━━━━━━━━━━━
当前选择：{target_room_name}（非推荐位置）
━━━━━━━━━━━━━━━━━━━━━━
【是】→ 确认放到 {target_room_name}
【否】→ 坚持放到 {target_room_name}"" [TARGET:{target_room_name}]
[CONTEXT:item={item_name}|location={target_room_name}|quantity=1]"""

def check_duplicate(item_name: str, furniture, quantity: int) -> tuple:
    """检查物品是否已存在，返回 (是否重复, 提示信息)"""
    for item in furniture.get("items", []):
        if item["name"] == item_name:
            new_total = item["quantity"] + quantity
            location = furniture.get("name", "")
            # 元数据用特殊格式，放在消息末尾
            meta = f"\n__META__:item={item_name}|location={location}|quantity={quantity}|action=merge_or_add"
            return True, f"""⚠️ 同位置已有 '{item_name}' (x{item['quantity']})
━━━━━━━━━━━━━━━━━━━━━━
【是】→ 数量合并为 {new_total}
【否】→ 继续添加（不合并）""" + meta
    return False, ""

def check_similar_items(item_name: str, data: dict, target_furniture) -> tuple:
    """检查全屋是否有同名/高度相似物品，返回 (是否存在, 提示信息)"""
    similar = []
    item_lower = item_name.lower()
    
    for s, r, f, i in iter_all_items(data):
        # 跳过目标位置
        if f == target_furniture:
            continue
        # 检查同名或高度相似
        i_name_lower = i["name"].lower()
        if i_name_lower == item_lower or item_lower in i_name_lower or i_name_lower in item_lower:
            similar.append({
                "name": i["name"],
                "quantity": i["quantity"],
                "suite": s["name"],
                "room": r["name"],
                "furniture": f["name"]
            })
    
    if similar:
        locs = [f"{s['room']}-{s['furniture']}" for s in similar]
        locs_str = "\n      • ".join(locs)
        target_room = target_furniture.get("name", "")
        target_suite = ""
        # 尝试获取 suite name
        for s in data.get("suites", []):
            for r in s.get("rooms", []):
                if r.get("name") == target_room:
                    target_suite = s.get("name", "")
                    break
        
        return True, f"""💡 全屋已有同类 '{item_name}'：
      • {locs_str}

当前你想放到：{target_room}
━━━━━━━━━━━━━━━━━━━━━━
【是】→ 归纳到已有位置（{similar[0]['room']}-{similar[0]['furniture']}）
【否】→ 坚持放到 {target_room}"" [TARGET:{similar[0]['room']}-{similar[0]['furniture']}]"""
    
    return False, ""

# ============== 位置解析 ==============
def parse_location(location: str, data: dict) -> tuple:
    """解析位置字符串，返回 (room_name, furniture_name)"""
    if '-' in location:
        parts = location.split('-')
        return parts[0], parts[-1]
    
    # 尝试匹配 套房名+房间名+家具名
    for suite in data.get("suites", []):
        if location.startswith(suite["name"]):
            rest = location[len(suite["name"]):]
            for room in suite.get("rooms", []):
                if rest.startswith(room["name"]):
                    return room["name"], rest[len(room["name"]):]
    
    # 尝试匹配 房间名+家具名
    for suite in data.get("suites", []):
        for room in suite.get("rooms", []):
            if location.startswith(room["name"]):
                return room["name"], location[len(room["name"]):]
    
    return None, location

def find_location(location: str, data: dict) -> tuple:
    """查找位置，返回 (room, furniture, suite)"""
    room_name, furniture_name = parse_location(location, data)
    
    for suite in data.get("suites", []):
        for room in suite.get("rooms", []):
            if room_name and room["name"] != room_name:
                continue
            for furniture in room.get("furniture", []):
                if furniture["name"] == furniture_name:
                    return room, furniture, suite
            # 模糊匹配家具名
            for furniture in room.get("furniture", []):
                if furniture_name in furniture["name"]:
                    return room, furniture, suite
    return None, None, None

# ============== 结果汇总 ==============
def summarize_results(results: list, title: str) -> str:
    """汇总查询/搜索结果"""
    if not results:
        return f"❓ 未找到结果"
    
    summary = {}
    for r in results:
        key = r["item"]["name"]
        if key not in summary:
            summary[key] = {"name": key, "total": 0, "locations": [], "note": r["item"].get("note", "")}
        summary[key]["total"] += r["item"]["quantity"]
        summary[key]["locations"].append({
            "suite": r["suite"], "room": r["room"],
            "furniture": r["furniture"], "quantity": r["item"]["quantity"]
        })
    
    msg = f"{title}\n{'=' * 40}\n"
    for info in summary.values():
        msg += f"\n📦 {info['name']}\n   总数量：{info['total']}\n   存放位置：\n"
        for loc in info["locations"]:
            msg += f"      • {loc['suite']}-{loc['room']}-{loc['furniture']} (x{loc['quantity']})\n"
    return msg.strip()

# ============== 命令函数 ==============
def cmd_init_suite(suite_name: str, rooms: list) -> str:
    """初始化套房"""
    data = load_data()
    if find_suite(data, suite_name):
        return f"❌ 套房 '{suite_name}' 已存在"
    
    t = now()
    suite = {
        "id": new_id(), "name": suite_name,
        "createdAt": t, "updatedAt": t,
        "rooms": [{"id": new_id(), "name": r, "createdAt": t, "updatedAt": t, "furniture": []} for r in rooms]
    }
    data["suites"].append(suite)
    save_data(data)
    return f"✅ 套房 '{suite_name}' 创建成功！\n包含房间：{'、'.join(rooms)}"

def cmd_add_room(suite_name: str, room_name: str) -> str:
    """添加房间"""
    data = load_data()
    suite = find_suite(data, suite_name)
    if not suite:
        return f"❌ 未找到套房 '{suite_name}'"
    if find_room(suite, room_name):
        return f"❌ 房间 '{room_name}' 已存在"
    
    t = now()
    suite["rooms"].append({"id": new_id(), "name": room_name, "createdAt": t, "updatedAt": t, "furniture": []})
    suite["updatedAt"] = t
    save_data(data)
    return f"✅ 房间 '{room_name}' 添加到套房 '{suite_name}'"

def cmd_add_furniture(suite_name: str, room_name: str, furniture_name: str) -> str:
    """添加家具"""
    data = load_data()
    
    # 查找房间
    target_room, target_suite = None, None
    if suite_name:
        suite = find_suite(data, suite_name)
        if suite:
            target_room = find_room(suite, room_name)
            target_suite = suite
    
    if not target_room:
        for suite in data.get("suites", []):
            room = find_room(suite, room_name)
            if room:
                target_room, target_suite = room, suite
                break
    
    if not target_room:
        return f"❌ 未找到房间 '{room_name}'"
    if find_furniture(target_room, furniture_name):
        return f"❌ 家具 '{furniture_name}' 已存在"
    
    t = now()
    target_room["furniture"].append({"id": new_id(), "name": furniture_name, "createdAt": t, "updatedAt": t, "items": []})
    update_timestamp_chain(target_room, target_suite)
    save_data(data)
    return f"✅ 家具 '{furniture_name}' 添加到房间 '{room_name}'"

def cmd_add_item(item_name: str, location: str, quantity: int = 1, force: bool = False, auto_merge: bool = False) -> str:
    """添加物品
    
    auto_merge: True=按用户否回答继续添加, False=正常添加(可能触发检测)
    """
    data = load_data()
    room, furniture, suite = find_location(location, data)
    if not furniture:
        # 提供智能推荐
        recommendations = get_recommendation(item_name, data)
        rec_msg = f"\n\n💡 推荐存放位置：{', '.join(recommendations)}" if recommendations else ""
        return f"❌ 未找到家具 '{location}'。请先添加家具：'客厅有个{location}'{rec_msg}"
    
    # 重复检测 + 全屋同名检测 + 智能位置推荐（除非 auto_merge=True 跳过）
    if not auto_merge:
        is_dup, dup_msg = check_duplicate(item_name, furniture, quantity)
        if is_dup:
            return dup_msg
        
        is_similar, similar_msg = check_similar_items(item_name, data, furniture)
        if is_similar:
            return similar_msg + f"\n[CONTEXT:item={item_name}|location={location}|quantity={quantity}]"
        
        # 智能位置推荐检测
        is_recommended, rec_msg = check_location_recommendation(item_name, room["name"], data)
        if not is_recommended:
            return rec_msg
    
    t = now()
    item = {"id": new_id(), "name": item_name, "quantity": quantity, "addedAt": t, "updatedAt": t, "note": ""}
    furniture["items"].append(item)
    update_timestamp_chain(furniture, room, suite)
    save_data(data)
    return f"✅ 物品 '{item_name}' (x{quantity}) 已放到 {room['name']}-{furniture['name']}"

def cmd_add_item_continue(item_name: str, location: str, quantity: int = 1) -> str:
    """用户回答"否"后，继续按原指令添加物品"""
    return cmd_add_item(item_name, location, quantity, auto_merge=True)

def cmd_merge_item(item_name: str, location: str, quantity: int = 1) -> str:
    """用户回答"是"，将物品归纳到已有位置"""
    data = load_data()
    room, furniture, suite = find_location(location, data)
    if not furniture:
        return f"❌ 位置 '{location}' 不存在"
    
    # 检查是否已有该物品，有则合并数量
    for item in furniture.get("items", []):
        if item["name"] == item_name:
            item["quantity"] += quantity
            item["updatedAt"] = now()
            update_timestamp_chain(furniture, room, suite)
            save_data(data)
            return f"✅ 已归纳！'{item_name}' 数量合并为 x{item['quantity']}，存放在 {room['name']}-{furniture['name']}"
    
    # 没有则新增
    t = now()
    item = {"id": new_id(), "name": item_name, "quantity": quantity, "addedAt": t, "updatedAt": t, "note": ""}
    furniture["items"].append(item)
    update_timestamp_chain(furniture, room, suite)
    save_data(data)
    return f"✅ 已归纳！'{item_name}' (x{quantity}) 存放在 {room['name']}-{furniture['name']}"

def cmd_add_item_force(item_name: str, location: str, quantity: int = 1) -> str:
    """强制添加物品（跳过重复检测）"""
    return cmd_add_item(item_name, location, quantity, force=True)

def cmd_recommend(item_name: str) -> str:
    """智能推荐存放位置"""
    data = load_data()
    if not data.get("suites"):
        return "❌ 尚未初始化套房，请先设置套房"
    
    recommendations = get_recommendation(item_name, data)
    if not recommendations or recommendations == ["请先添加家具"]:
        return f"💡 '{item_name}' 可以存放在：抽屉、柜子、收纳盒、电视柜等\n\n请先添加家具后告诉我具体位置"
    
    return f"💡 '{item_name}' 推荐存放在：\n" + "\n".join([f"   • {r}" for r in recommendations])

def cmd_query_item(item_name: str) -> str:
    """查询物品"""
    data = load_data()
    results = [{"suite": s["name"], "room": r["name"], "furniture": f["name"], "item": i}
               for s, r, f, i in iter_all_items(data) if item_name in i["name"]]
    return summarize_results(results, f"🔍 查询结果：{item_name}")

def cmd_list_suite(suite_name: str) -> str:
    """列出套房内容"""
    data = load_data()
    suite = find_suite(data, suite_name)
    if not suite:
        return f"❌ 未找到套房 '{suite_name}'"
    
    msg = f"🏠 {suite['name']}\n{'=' * 30}\n"
    for room in suite.get("rooms", []):
        msg += f"\n📦 {room['name']}\n"
        if not room.get("furniture"):
            msg += "   (暂无家具)\n"
            continue
        for furn in room["furniture"]:
            items = furn.get("items", [])
            if not items:
                msg += f"   🪑 {furn['name']} (空)\n"
            else:
                items_str = ", ".join([f"{i['name']} x{i['quantity']}" for i in items])
                msg += f"   🪑 {furn['name']}: {items_str}\n"
    return msg

def cmd_move_item(item_name: str, new_location: str) -> str:
    """搬动物品"""
    data = load_data()
    
    # 查找物品
    source = None
    for s, r, f, i in iter_all_items(data):
        if item_name in i["name"]:
            source = {"item": i, "furniture": f, "room": r, "suite": s}
            break
    if not source:
        return f"❓ 未找到物品 '{item_name}'"
    
    # 查找目标位置
    target_room, target_furniture, target_suite = find_location(new_location, data)
    if not target_furniture:
        return f"❌ 未找到位置 '{new_location}'"
    
    # 移动
    source["furniture"]["items"] = [i for i in source["furniture"]["items"] if i["id"] != source["item"]["id"]]
    t = now()
    source["item"]["updatedAt"] = t
    target_furniture["items"].append(source["item"])
    
    update_timestamp_chain(source["furniture"], source["room"], source["suite"], target_furniture, target_room, target_suite)
    save_data(data)
    return f"✅ '{item_name}' 已从 {source['room']['name']}-{source['furniture']['name']} 搬到 {target_room['name']}-{target_furniture['name']}"

def cmd_delete_item(item_name: str) -> str:
    """删除物品"""
    data = load_data()
    t = now()
    
    for s, r, f, i in iter_all_items(data):
        if item_name in i["name"]:
            f["items"] = [item for item in f["items"] if item["id"] != i["id"]]
            update_timestamp_chain(f, r, s)
            save_data(data)
            return f"✅ 已删除 '{item_name}'"
    return f"❓ 未找到物品 '{item_name}'"

def cmd_search(keyword: str) -> str:
    """搜索物品（模糊匹配）"""
    data = load_data()
    keyword_lower = keyword.lower()
    results = [{"suite": s["name"], "room": r["name"], "furniture": f["name"], "item": i}
               for s, r, f, i in iter_all_items(data) if keyword_lower in i["name"].lower()]
    if not results:
        return f"🔍 搜索 '{keyword}' 未找到任何物品"
    return summarize_results(results, f"🔍 搜索 '{keyword}' 找到 {len(set(r['item']['name'] for r in results))} 种物品：")

# ============== 备份导出 ==============
def cmd_backup() -> str:
    """备份数据"""
    data = load_data()
    if not data.get("suites"):
        return "❌ 当前没有数据，无需备份"
    
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"home_storage_{timestamp}.json")
    
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    backups = [f for f in os.listdir(BACKUP_DIR) if f.startswith("home_storage_") and f.endswith(".json")]
    return f"✅ 备份成功！\n📁 文件：{backup_file}\n📊 当前共有 {len(backups)} 个备份"

def cmd_list_backups() -> str:
    """列出备份"""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith("home_storage_") and f.endswith(".json")], reverse=True)
    
    if not backups:
        return "❌ 暂无可用备份"
    
    msg = f"📋 共有 {len(backups)} 个备份：\n{'=' * 40}\n"
    for i, backup in enumerate(backups[:10], 1):
        ts = backup.replace("home_storage_", "").replace(".json", "")
        try:
            ts = datetime.strptime(ts, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
        except:
            pass
        msg += f"{i}. {ts}\n   {backup}\n"
    return msg.strip()

def cmd_restore(backup_file: str) -> str:
    """恢复数据"""
    if not backup_file:
        return "❌ 请指定要恢复的备份文件"
    
    if not backup_file.endswith(".json"):
        backup_file = os.path.join(BACKUP_DIR, f"home_storage_{backup_file}.json")
    else:
        backup_file = os.path.join(BACKUP_DIR, os.path.basename(backup_file))
    
    if not os.path.exists(backup_file):
        return f"❌ 备份文件不存在：{backup_file}\n可使用 '列出备份' 查看可用备份"
    
    with open(backup_file, 'r', encoding='utf-8') as f:
        backup_data = json.load(f)
    
    # 恢复前备份当前数据
    current = load_data()
    if current.get("suites"):
        pre_backup = os.path.join(BACKUP_DIR, f"pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(pre_backup, 'w', encoding='utf-8') as f:
            json.dump(current, f, ensure_ascii=False, indent=2)
    
    save_data(backup_data)
    suite_count = len(backup_data.get("suites", []))
    furniture_count = sum(len(r.get("furniture", [])) for s in backup_data.get("suites", []) for r in s.get("rooms", []))
    return f"✅ 数据恢复成功！\n📁 恢复自：{os.path.basename(backup_file)}\n🏠 包含 {suite_count} 个套房\n📦 包含 {furniture_count} 件家具"

def cmd_export(format_type: str = "text") -> str:
    """导出数据"""
    data = load_data()
    if not data.get("suites"):
        return "❌ 当前没有数据，无法导出"
    
    if format_type == "json":
        os.makedirs(BACKUP_DIR, exist_ok=True)
        export_file = os.path.join(BACKUP_DIR, f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return f"✅ JSON 导出成功！\n📁 文件：{export_file}"
    
    # 文本格式
    msg = f"🏠 家庭物品收纳数据导出\n{'=' * 50}\n导出时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    total = 0
    for suite in data.get("suites", []):
        msg += f"\n🏠 {suite['name']}\n"
        for room in suite.get("rooms", []):
            msg += f"  📦 {room['name']}\n"
            for furn in room.get("furniture", []):
                items = furn.get("items", [])
                total += len(items)
                if not items:
                    msg += f"      🪑 {furn['name']} (空)\n"
                else:
                    items_str = ", ".join([f"{i['name']} x{i['quantity']}" for i in items])
                    msg += f"      🪑 {furn['name']}: {items_str}\n"
    msg += f"\n{'=' * 50}\n总计：{total} 件物品"
    return msg

# ============== 帮助与主函数 ==============
HELP = """🏠 家庭收纳管理系统使用指南：

【初始化】设置一套房叫工作室，有客厅、卧室
【添加】给工作室加一个房间叫厨房 | 客厅有个电视柜 | 把遥控器放在客厅电视柜里
【查询】我的遥控器在哪？ | 查看工作室
【搜索】搜索遥控 | 找一下手机
【搬动】把遥控器搬到卧室衣柜
【删除】删除遥控器
【备份】备份数据 | 列出备份 | 恢复数据 20260325_143000
【导出】导出数据 | 导出JSON
【推荐】推荐存放位置 遥控器 | 推荐位置 书籍
【重复检测】添加物品时自动检测是否已存在
"""

def main():
    if len(sys.argv) < 2:
        print(HELP)
        return
    
    cmd, text = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else ""
    data = load_data()
    
    # 命令路由
    commands = {
        "init_suite": (lambda: parse_suite_and_rooms(text), lambda s, r: cmd_init_suite(s, r), "设置一套房叫工作室，有客厅、卧室"),
        "add_room": (lambda: parse_add_room(text), lambda s, r: cmd_add_room(s, r), "给工作室加一个房间叫厨房"),
        "add_furniture": (lambda: parse_add_furniture(text, data), lambda s, r, f: cmd_add_furniture(s, r, f), "客厅有个电视柜"),
        "add_item": (lambda: parse_add_item(text), lambda n, l, q=None, f=False: cmd_add_item(n, l, q or 1, f), "把遥控器放在客厅电视柜里"),
        "recommend": (lambda: (parse_recommend(text), None), lambda n, _: cmd_recommend(n) if n else "❌ 请指定物品名称，例如：推荐存放位置 遥控器", "推荐存放位置 遥控器"),
        "query": (lambda: (parse_query_item(text), None), lambda n, _: cmd_query_item(n), "我的遥控器在哪？"),
        "list": (lambda: (text, None), lambda n: cmd_list_suite(n) if n else HELP, "查看工作室"),
        "move": (lambda: parse_move_item(text), lambda n, l: cmd_move_item(n, l), "把遥控器搬到卧室衣柜"),
        "delete": (lambda: (parse_delete_item(text), None), lambda n, _: cmd_delete_item(n) if n else "❌ 格式错误，例如：删除遥控器", "删除遥控器"),
        "search": (lambda: (text, None), lambda n, _: cmd_search(n) if n else "❌ 格式错误，例如：搜索遥控", "搜索遥控"),
        "backup": (lambda: (None, None), lambda: cmd_backup(), "备份数据"),
        "list_backups": (lambda: (None, None), lambda: cmd_list_backups(), "列出备份"),
        "restore": (lambda: (text, None), lambda f: cmd_restore(f) if f else "❌ 请指定备份文件", "恢复数据 20260325_143000"),
        "export": (lambda: (text, None), lambda f: cmd_export("json" if "json" in f.lower() else "text"), "导出数据"),
        # 确认处理命令
        "merge_item": (lambda: parse_merge_item(text), lambda n, l: cmd_merge_item(n, l) if n and l else "❌ 格式错误，例如：merge 遥控器|客厅-电视柜", "merge 遥控器|客厅-电视柜"),
        "continue_add": (lambda: parse_continue_add(text), lambda n, l, q=1: cmd_add_item_continue(n, l, q) if n and l else "❌ 格式错误", "continue_add 遥控器|卧室床头柜|1"),
    }
    
    if cmd not in commands:
        print(HELP)
        return
    
    parser, handler, example = commands[cmd]
    args = parser()
    
    try:
        if cmd in ("init_suite",):
            s, r = args
            print(handler(s, r) if s and r else f"❌ 格式错误，例如：{example}")
        elif cmd in ("add_room",):
            s, r = args
            print(handler(s, r) if s and r else f"❌ 格式错误，例如：{example}")
        elif cmd in ("add_furniture",):
            s, r, f = args
            print(handler(s, r, f) if r and f else f"❌ 格式错误，例如：{example}")
        elif cmd in ("add_item",):
            n, l, _, q = args
            print(handler(n, l, q) if n and l else f"❌ 格式错误，例如：{example}")
        elif cmd in ("query", "search", "recommend"):
            n, _ = args
            print(handler(n, _) if n else f"❌ 格式错误，例如：{example}")
        elif cmd in ("list", "restore", "export"):
            n, _ = args
            print(handler(n))
        elif cmd in ("move",):
            n, l = args
            print(handler(n, l) if n and l else f"❌ 格式错误，例如：{example}")
        elif cmd in ("delete",):
            n, _ = args
            print(handler(n, _))
        elif cmd in ("merge_item",):
            n, l = args
            print(handler(n, l) if n and l else f"❌ 格式错误，例如：{example}")
        elif cmd in ("continue_add",):
            n, l, q = args
            print(handler(n, l, q) if n and l else f"❌ 格式错误，例如：{example}")
        else:
            print(handler())
    except Exception as e:
        print(f"❌ 执行错误：{e}")

if __name__ == "__main__":
    main()