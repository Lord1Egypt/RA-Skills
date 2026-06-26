#!/usr/bin/env python3
"""
管理 skill-polisher 的追踪列表
用法: python3 tracking.py [--list] [--add SKILL] [--remove SKILL] [--status]
"""

import argparse
import json
from datetime import datetime
from pathlib import Path


def get_tracking_file() -> Path:
    """获取追踪列表文件路径"""
    tracking_file = Path.home() / ".openclaw/workspace/.skill-polisher/tracking.json"
    tracking_file.parent.mkdir(parents=True, exist_ok=True)
    return tracking_file


def load_tracking() -> dict:
    """加载追踪列表"""
    tracking_file = get_tracking_file()
    if tracking_file.exists():
        with open(tracking_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"tracked": [], "history": []}


def save_tracking(data: dict):
    """保存追踪列表"""
    tracking_file = get_tracking_file()
    with open(tracking_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_skill(skill_name: str) -> bool:
    """添加技能到追踪列表"""
    data = load_tracking()
    
    if skill_name in data["tracked"]:
        print(f"⚠️  {skill_name} 已在追踪列表中")
        return False
    
    # 检查技能是否存在
    skill_path = Path.home() / ".openclaw/workspace/skills" / skill_name
    if not skill_path.exists():
        print(f"❌ 技能不存在: {skill_name}")
        return False
    
    data["tracked"].append(skill_name)
    data["history"].append({
        "action": "add",
        "skill": skill_name,
        "timestamp": datetime.now().isoformat()
    })
    
    save_tracking(data)
    
    # 检查是否已设置成功标准
    exp_path = Path.home() / f".openclaw/workspace/.skill-polisher/expectations/{skill_name}.json"
    if not exp_path.exists():
        print(f"💡 建议为该技能设置成功标准:")
        print(f"   python3 set-expectation.py --skill {skill_name} --edit")
    
    return True


def remove_skill(skill_name: str) -> bool:
    """从追踪列表移除技能"""
    data = load_tracking()
    
    if skill_name not in data["tracked"]:
        print(f"⚠️  {skill_name} 不在追踪列表中")
        return False
    
    data["tracked"].remove(skill_name)
    data["history"].append({
        "action": "remove",
        "skill": skill_name,
        "timestamp": datetime.now().isoformat()
    })
    
    save_tracking(data)
    return True


def list_tracked():
    """列出追踪中的技能"""
    data = load_tracking()
    tracked = data["tracked"]
    
    if not tracked:
        print("\n📭 追踪列表为空")
        print("   使用 --add <skill-name> 添加技能到追踪列表")
        return
    
    print(f"\n📋 追踪中的技能 ({len(tracked)} 个):")
    print(f"{'='*50}")
    
    for skill in tracked:
        # 检查是否有成功标准
        exp_path = Path.home() / f".openclaw/workspace/.skill-polisher/expectations/{skill}.json"
        has_expectation = exp_path.exists()
        
        # 检查反馈数量
        feedback_dir = Path.home() / f".openclaw/workspace/.skill-polisher/feedback/{skill}"
        feedback_count = len(list(feedback_dir.glob("*.json"))) if feedback_dir.exists() else 0
        
        status = "🎯" if has_expectation else "⚪"
        print(f"  {status} {skill:<20} 反馈: {feedback_count} 条")
    
    print(f"\n{'='*50}")
    print("  🎯 = 已设置成功标准  ⚪ = 未设置成功标准")


def show_status(skill_name: str = None):
    """显示追踪状态"""
    data = load_tracking()
    
    if skill_name:
        if skill_name not in data["tracked"]:
            print(f"\n⚪ {skill_name}: 不在追踪列表中")
            return
        
        print(f"\n🎯 {skill_name}: 正在追踪中")
        
        # 显示该技能的历史操作
        history = [h for h in data["history"] if h["skill"] == skill_name]
        if history:
            print(f"\n  操作历史:")
            for h in history[-5:]:  # 最近5条
                action = "添加" if h["action"] == "add" else "移除"
                print(f"    - {action}: {h['timestamp'][:10]}")
    else:
        print(f"\n📊 追踪统计:")
        print(f"  追踪中: {len(data['tracked'])} 个技能")
        print(f"  历史操作: {len(data['history'])} 次")
        
        if data["tracked"]:
            print(f"\n  追踪列表: {', '.join(data['tracked'])}")


def is_tracked(skill_name: str) -> bool:
    """检查技能是否在追踪列表中"""
    data = load_tracking()
    return skill_name in data["tracked"]


def get_tracked_skills() -> list:
    """获取所有追踪中的技能"""
    data = load_tracking()
    return data["tracked"]


def main():
    parser = argparse.ArgumentParser(description="管理 skill-polisher 追踪列表")
    parser.add_argument("--list", "-l", action="store_true", help="列出追踪中的技能")
    parser.add_argument("--add", "-a", help="添加技能到追踪列表")
    parser.add_argument("--remove", "-r", help="从追踪列表移除技能")
    parser.add_argument("--status", "-s", nargs="?", const="all", help="显示追踪状态")
    
    args = parser.parse_args()
    
    if args.add:
        if add_skill(args.add):
            print(f"✅ 已添加 {args.add} 到追踪列表")
    elif args.remove:
        if remove_skill(args.remove):
            print(f"✅ 已将 {args.remove} 从追踪列表移除")
            print(f"   历史评估数据仍保留")
    elif args.status:
        show_status(None if args.status == "all" else args.status)
    else:
        list_tracked()


if __name__ == "__main__":
    main()
