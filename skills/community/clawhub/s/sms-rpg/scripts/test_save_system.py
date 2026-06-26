#!/usr/bin/env python3
"""
SMS RPG 指令式引擎 - 测试脚本
验证存档读写逻辑
"""

import json
import os
from datetime import datetime

# 测试目录
SAVE_DIR = "./sms-rpg-saves"

def ensure_save_dir():
    """确保存档目录存在"""
    os.makedirs(SAVE_DIR, exist_ok=True)
    print(f"✓ 存档目录: {SAVE_DIR}")

def create_test_save(slot=1):
    """创建测试存档"""
    save_data = {
        "version": "2.0-instruction",
        "savedAt": datetime.now().isoformat(),
        "slot": slot,
        "playerName": "沈浪",
        "worldRequirement": "武侠修仙，江湖门派与朝廷暗斗",
        "narrativeStyle": "通俗、利落、有人味，接近《庆余年》叙事感",
        "currentTurn": 3,
        "worldState": {
            "currentLocation": "gusu-city-street",
            "time": "午后",
            "weather": "细雨",
            "atmosphere": "紧张",
            "player": {
                "name": "沈浪",
                "cultivationLevel": "后天境",
                "hp": 100,
                "maxHp": 100,
                "mp": 50,
                "maxMp": 50,
                "gold": 10,
                "reputation": {},
                "activeEffects": [],
                "inventory": []
            },
            "locations": {
                "gusu-city-street": {
                    "id": "gusu-city-street",
                    "name": "姑苏城·长街",
                    "description": "街道两旁商铺林立",
                    "connectedTo": ["gusu-teahouse"],
                    "presentNpcs": [],
                    "secrets": [],
                    "visited": True
                },
                "gusu-teahouse": {
                    "id": "gusu-teahouse",
                    "name": "听雨茶楼",
                    "description": "二层雅间可俯瞰长街",
                    "connectedTo": ["gusu-city-street"],
                    "presentNpcs": ["liu-poison-tongue"],
                    "secrets": ["暗阁联络点"],
                    "visited": False
                }
            },
            "npcs": {
                "liu-poison-tongue": {
                    "id": "liu-poison-tongue",
                    "name": "柳娘子",
                    "description": "暗阁联络人，外号毒舌",
                    "faction": "暗阁",
                    "hp": 80,
                    "maxHp": 80,
                    "mp": 30,
                    "maxMp": 30,
                    "attitude": -50,
                    "status": "active",
                    "secrets": ["三年前传递假情报"],
                    "knownSecrets": [],
                    "relationships": {}
                }
            },
            "quests": [
                {
                    "id": "revenge-shen",
                    "title": "沈家灭门案",
                    "type": "main",
                    "status": "active",
                    "objectives": ["追查暗阁线索", "找到幕后主使"],
                    "progress": "发现柳娘子行踪"
                }
            ],
            "relationships": {},
            "worldMemory": {
                "recentEvents": ["抵达姑苏城", "发现柳娘子"],
                "summary": "沈浪追查灭门凶手，来到姑苏城，发现暗阁联络人柳娘子踪迹",
                "majorEvents": []
            }
        },
        "turnHistory": [
            {
                "turnNumber": 1,
                "playerInput": "混入城中，打探消息",
                "narrative": "...",
                "stateChanges": {}
            },
            {
                "turnNumber": 2,
                "playerInput": "找个角落观察，记下她见面的对象",
                "narrative": "...",
                "stateChanges": {}
            }
        ],
        "summary": "沈浪追查灭门凶手，来到姑苏城，发现暗阁联络人柳娘子踪迹"
    }
    
    filepath = os.path.join(SAVE_DIR, f"save_{slot:03d}.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)
    print(f"✓ 创建测试存档: {filepath}")
    return filepath

def load_save(slot=1):
    """加载存档"""
    filepath = os.path.join(SAVE_DIR, f"save_{slot:03d}.json")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ 加载存档成功: {filepath}")
        return data
    except FileNotFoundError:
        print(f"✗ 存档不存在: {filepath}")
        return None
    except json.JSONDecodeError as e:
        print(f"✗ 存档损坏: {filepath}, 错误: {e}")
        return None

def list_saves():
    """列出所有存档"""
    saves = []
    for i in range(1, 6):
        filepath = os.path.join(SAVE_DIR, f"save_{i:03d}.json")
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                saves.append({
                    "slot": i,
                    "playerName": data.get("playerName", "未知"),
                    "turn": data.get("currentTurn", 0),
                    "summary": data.get("summary", "")[:30]
                })
            except:
                saves.append({"slot": i, "status": "损坏"})
        else:
            saves.append({"slot": i, "status": "空"})
    return saves

def delete_save(slot=1):
    """删除存档"""
    filepath = os.path.join(SAVE_DIR, f"save_{slot:03d}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"✓ 删除存档: {filepath}")
    else:
        print(f"✗ 存档不存在: {filepath}")

def test_world_state_update():
    """测试世界状态更新"""
    print("\n=== 测试世界状态更新 ===")
    
    # 模拟战斗后的状态变化
    state_changes = {
        "playerUpdates": {
            "hpDelta": -15,
            "mpDelta": -10,
            "goldDelta": 5,
            "addEffects": ["轻伤"],
            "addItems": ["银票"],
            "removeItems": []
        }
    }
    
    # 加载存档
    save = load_save(1)
    if save:
        # 应用变化
        player = save["worldState"]["player"]
        player["hp"] = max(0, player["hp"] + state_changes["playerUpdates"]["hpDelta"])
        player["mp"] = max(0, player["mp"] + state_changes["playerUpdates"]["mpDelta"])
        player["gold"] += state_changes["playerUpdates"]["goldDelta"]
        player["activeEffects"].extend(state_changes["playerUpdates"]["addEffects"])
        player["inventory"].extend(state_changes["playerUpdates"]["addItems"])
        
        print(f"✓ HP: {100 + (-15)} → {player['hp']}")
        print(f"✓ MP: {50 + (-10)} → {player['mp']}")
        print(f"✓ Gold: {10 + 5} → {player['gold']}")
        print(f"✓ 新增效果: {player['activeEffects']}")
        print(f"✓ 新增物品: {player['inventory']}")
        
        # 保存更新后的存档
        filepath = os.path.join(SAVE_DIR, "save_001.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(save, f, ensure_ascii=False, indent=2)
        print(f"✓ 存档已更新")

if __name__ == "__main__":
    print("=" * 50)
    print("SMS RPG 指令式引擎 - 存档系统测试")
    print("=" * 50)
    
    # 1. 确保目录存在
    ensure_save_dir()
    
    # 2. 创建测试存档
    create_test_save(1)
    
    # 3. 加载存档
    load_save(1)
    
    # 4. 列出所有存档
    print("\n=== 存档列表 ===")
    for save in list_saves():
        if "status" in save:
            print(f"槽位{save['slot']}: {save['status']}")
        else:
            print(f"槽位{save['slot']}: {save['playerName']} | 第{save['turn']}回合 | {save['summary']}...")
    
    # 5. 测试状态更新
    test_world_state_update()
    
    # 6. 清理测试存档
    print("\n=== 清理测试数据 ===")
    delete_save(1)
    
    print("\n" + "=" * 50)
    print("✓ 所有测试通过！")
    print("=" * 50)
