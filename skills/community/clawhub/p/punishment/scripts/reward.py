#!/usr/bin/env python3
"""
奖惩机制记录脚本
用于记录用户的夸奖/批评，自动调整分数
"""
import json
import os
from datetime import datetime

SCORE_FILE = os.path.expanduser("~/.openclaw/workspace/memory/reward_punishment.json")

# 初始化分数
DEFAULT_DATA = {
    "score": 100,
    "history": [],
    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

def load_data():
    """加载分数数据"""
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_DATA.copy()

def save_data(data):
    """保存分数数据"""
    os.makedirs(os.path.dirname(SCORE_FILE), exist_ok=True)
    with open(SCORE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def record_feedback(feedback_type: str, reason: str = "") -> dict:
    """
    记录反馈并调整分数
    
    feedback_type: "praise"(夸奖) / "punish"(批评) / "abuse"(骂人)
    """
    data = load_data()
    
    # 计算分数变化
    score_changes = {
        "praise": 10,
        "punish": -5,
        "abuse": -10
    }
    
    change = score_changes.get(feedback_type, 0)
    
    # 记录历史
    record = {
        "type": feedback_type,
        "score": change,
        "reason": reason,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data["history"].append(record)
    
    # 调整分数
    data["score"] = max(0, min(200, data["score"] + change))
    
    # 保存
    save_data(data)
    
    return {
        "score": data["score"],
        "change": change,
        "total_records": len(data["history"])
    }

def get_score() -> int:
    """获取当前分数"""
    data = load_data()
    return data["score"]

def get_history(limit: int = 10) -> list:
    """获取历史记录"""
    data = load_data()
    return data["history"][-limit:]

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print(f"当前分数: {get_score()}")
        sys.exit(0)
    
    action = sys.argv[1]
    
    if action == "praise":
        reason = sys.argv[2] if len(sys.argv) > 2 else "用户夸奖"
        result = record_feedback("praise", reason)
        print(f"✅ 夸奖记录成功！分数+{result['change']}，当前{result['score']}分")
    
    elif action == "punish":
        reason = sys.argv[2] if len(sys.argv) > 2 else "用户批评"
        result = record_feedback("punish", reason)
        print(f"⚠️ 批评记录成功！分数{result['change']}，当前{result['score']}分")
    
    elif action == "abuse":
        reason = sys.argv[2] if len(sys.argv) > 2 else "用户骂人"
        result = record_feedback("abuse", reason)
        print(f"💢 骂人记录成功！分数{result['change']}，当前{result['score']}分")
    
    elif action == "status":
        print(f"当前分数: {get_score()}")
        print(f"历史记录: {len(get_history())}条")
    
    elif action == "history":
        for h in get_history(10):
            print(f"[{h['time']}] {h['type']}: {h['score']}分 - {h['reason']}")
    
    else:
        print("用法: reward.py [praise|punish|abuse|status|history] [原因]")
