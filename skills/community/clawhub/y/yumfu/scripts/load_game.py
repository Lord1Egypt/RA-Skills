#!/usr/bin/env python3
"""
YumFu Game Load Script
统一的存档读取工具 - 避免AI猜测存档格式

Usage:
    uv run ~/clawd/skills/yumfu/scripts/load_game.py \
        --user-id YOUR_USER_ID \
        --universe xiaoao

Output: JSON to stdout (可直接pipe到其他脚本)
"""

import json
import os
import sys
import argparse
from pathlib import Path


def load_game(user_id: str, universe: str) -> dict:
    """
    从标准路径加载游戏进度
    
    Args:
        user_id: Telegram/Platform user ID
        universe: World name (xiaoao, harry-potter, warrior-cats, etc.)
    
    Returns:
        {
            "exists": bool,
            "data": dict|None,
            "error": str|None,
            "save_path": str
        }
    """
    save_path = Path.home() / "clawd" / "memory" / "yumfu" / "saves" / universe / f"user-{user_id}.json"
    
    if not save_path.exists():
        return {
            "exists": False,
            "data": None,
            "error": f"No save found for user {user_id} in {universe}",
            "save_path": str(save_path)
        }
    
    try:
        with open(save_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return {
            "exists": True,
            "data": data,
            "save_path": str(save_path),
            "character_name": data.get("character", {}).get("name", "Unknown"),
            "level": data.get("character", {}).get("level", "?"),
            "location": data.get("location", "Unknown"),
            "last_played": data.get("last_played", data.get("last_saved", "Never"))
        }
    
    except json.JSONDecodeError as e:
        return {
            "exists": True,
            "data": None,
            "error": f"Save file corrupted: {e}",
            "save_path": str(save_path)
        }
    except Exception as e:
        return {
            "exists": True,
            "data": None,
            "error": f"Failed to load save: {e}",
            "save_path": str(save_path)
        }


def check_user_exists(user_id: str) -> dict:
    """
    检查用户在所有世界中的存档
    
    Returns:
        {
            "user_id": str,
            "worlds": {
                "xiaoao": {"exists": bool, "character": str, "level": int},
                "harry-potter": {...},
                ...
            }
        }
    """
    saves_root = Path.home() / "clawd" / "memory" / "yumfu" / "saves"
    
    if not saves_root.exists():
        return {"user_id": user_id, "worlds": {}, "error": "No saves directory exists"}
    
    worlds = {}
    for world_dir in saves_root.iterdir():
        if world_dir.is_dir():
            world_name = world_dir.name
            save_file = world_dir / f"user-{user_id}.json"
            
            if save_file.exists():
                try:
                    with open(save_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    worlds[world_name] = {
                        "exists": True,
                        "character": data.get("character", {}).get("name", "Unknown"),
                        "level": data.get("character", {}).get("level", "?"),
                        "location": data.get("location", "Unknown"),
                        "last_played": data.get("last_played", data.get("last_saved", "Unknown"))
                    }
                except Exception as e:
                    worlds[world_name] = {
                        "exists": True,
                        "error": f"Corrupted: {e}"
                    }
            else:
                worlds[world_name] = {"exists": False}
    
    return {
        "user_id": user_id,
        "worlds": worlds,
        "active_worlds": [w for w, info in worlds.items() if info.get("exists")]
    }


def main():
    parser = argparse.ArgumentParser(description="YumFu unified load script")
    parser.add_argument("--user-id", required=True, help="User ID (Telegram/Platform)")
    parser.add_argument("--universe", 
                       choices=["xiaoao", "harry-potter", "warrior-cats", "lotr", "game-of-thrones", "yitian", "sengoku", "journey-to-west"],
                       help="Game world/universe (omit to check all worlds)")
    parser.add_argument("--check-all", action="store_true", help="Check all worlds for this user")
    parser.add_argument("--quiet", action="store_true", help="Only output JSON result")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    
    args = parser.parse_args()
    
    # Check all worlds mode
    if args.check_all or not args.universe:
        result = check_user_exists(args.user_id)
        
        if args.quiet:
            indent = 2 if args.pretty else None
            print(json.dumps(result, indent=indent, ensure_ascii=False))
        else:
            print(f"🔍 Checking saves for user {args.user_id}...")
            if result.get("active_worlds"):
                print(f"\n✅ Found {len(result['active_worlds'])} save(s):")
                for world in result["active_worlds"]:
                    info = result["worlds"][world]
                    print(f"  • {world}: {info['character']} (Lv.{info['level']}) - {info['location']}")
            else:
                print("\n❌ No saves found for this user")
            
            if args.pretty:
                print("\nFull data:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
        
        return
    
    # Single world load mode
    result = load_game(args.user_id, args.universe)
    
    if args.quiet:
        indent = 2 if args.pretty else None
        print(json.dumps(result, indent=indent, ensure_ascii=False))
    else:
        if result["exists"]:
            if result.get("data"):
                print(f"✅ Save found!")
                print(f"📁 Path: {result['save_path']}")
                print(f"👤 Character: {result['character_name']} (Lv.{result['level']})")
                print(f"📍 Location: {result['location']}")
                print(f"🕒 Last played: {result['last_played']}")
                
                if args.pretty:
                    print("\nFull save data:")
                    print(json.dumps(result["data"], indent=2, ensure_ascii=False))
            else:
                print(f"❌ Save exists but is corrupted: {result['error']}", file=sys.stderr)
                sys.exit(1)
        else:
            print(f"❌ {result['error']}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
