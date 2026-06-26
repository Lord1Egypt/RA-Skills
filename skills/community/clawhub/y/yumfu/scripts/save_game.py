#!/usr/bin/env python3
"""
YumFu Game Save Script
统一的存档保存工具 - 避免AI猜测存档格式

Usage:
    uv run ~/clawd/skills/yumfu/scripts/save_game.py \
        --user-id 1309815719 \
        --universe xiaoao \
        --data '{"character": {"name": "小虾米", "level": 1, ...}, ...}'

Or pipe JSON:
    echo '{"character": {...}}' | uv run save_game.py --user-id 123 --universe xiaoao
"""

import json
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

WORLD_DIR = Path.home() / "clawd" / "skills" / "yumfu" / "worlds"


def normalize_lang(value: str | None) -> str | None:
    if not value:
        return None
    v = str(value).strip().lower()
    if v in {'zh', 'zh-cn', 'zh-hans', 'zh-tw', 'zh-hant', 'cn', 'chinese', '中文'}:
        return 'zh'
    if v in {'en', 'en-us', 'en-gb', 'english'}:
        return 'en'
    return None


def load_world_language(universe: str) -> str | None:
    direct = WORLD_DIR / f"{universe}.json"
    nested = WORLD_DIR / universe / 'world.json'
    path = direct if direct.exists() else nested
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        return normalize_lang(data.get('language'))
    except Exception:
        return None


def save_game(user_id: str, universe: str, data: dict, backup: bool = True) -> dict:
    """
    保存游戏进度到标准路径
    
    Args:
        user_id: Telegram/Platform user ID
        universe: World name (xiaoao, harry-potter, warrior-cats, etc.)
        data: Complete save data dict
        backup: Create timestamped backup before overwriting
    
    Returns:
        {
            "success": bool,
            "save_path": str,
            "backup_path": str|None,
            "error": str|None
        }
    """
    # Standard save directory
    save_dir = Path.home() / "clawd" / "memory" / "yumfu" / "saves" / universe
    save_path = save_dir / f"user-{user_id}.json"
    
    # Create directory if needed
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # Validate data
    if not isinstance(data, dict):
        return {"success": False, "error": "Data must be a JSON object"}
    
    # Add metadata
    if "user_id" not in data:
        data["user_id"] = user_id
    if "universe" not in data:
        data["universe"] = universe
    if "version" not in data:
        data["version"] = 2  # Current save format version

    existing_lang = normalize_lang(data.get("language"))
    world_lang = load_world_language(universe)
    if not existing_lang and world_lang:
        data["language"] = world_lang
    elif existing_lang:
        data["language"] = existing_lang
    
    data["last_saved"] = datetime.now().isoformat()
    
    # Backup existing save
    backup_path = None
    if backup and save_path.exists():
        backup_dir = Path.home() / "clawd" / "memory" / "yumfu" / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = backup_dir / f"user-{user_id}-{universe}-{timestamp}.json"
        
        try:
            with open(save_path, 'r') as f:
                old_data = json.load(f)
            with open(backup_path, 'w') as f:
                json.dump(old_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Backup failed (non-fatal): {e}", file=sys.stderr)
    
    # Write new save
    try:
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Verify write
        if not save_path.exists():
            return {
                "success": False,
                "error": "Save file write succeeded but file doesn't exist!"
            }
        
        # Verify content
        with open(save_path, 'r', encoding='utf-8') as f:
            verified = json.load(f)
        
        return {
            "success": True,
            "save_path": str(save_path),
            "backup_path": str(backup_path) if backup_path else None,
            "character_name": verified.get("character", {}).get("name", "Unknown"),
            "level": verified.get("character", {}).get("level", "?"),
        }
        
    except Exception as e:
        # Emergency fallback: try temp directory
        fallback_path = Path("/tmp") / f"yumfu-emergency-{user_id}-{universe}.json"
        try:
            with open(fallback_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return {
                "success": False,
                "error": f"Primary save failed: {e}. Emergency save at {fallback_path}",
                "fallback_path": str(fallback_path)
            }
        except Exception as e2:
            return {
                "success": False,
                "error": f"Complete save failure: {e}. Fallback also failed: {e2}"
            }


def main():
    parser = argparse.ArgumentParser(description="YumFu unified save script")
    parser.add_argument("--user-id", required=True, help="User ID (Telegram/Platform)")
    parser.add_argument("--universe", required=True, 
                       choices=["xiaoao", "harry-potter", "warrior-cats", "lotr", "game-of-thrones", "yitian", "sengoku", "journey-to-west"],
                       help="Game world/universe")
    parser.add_argument("--data", help="JSON data as string (optional if using stdin)")
    parser.add_argument("--no-backup", action="store_true", help="Skip backup of existing save")
    parser.add_argument("--quiet", action="store_true", help="Only output JSON result")
    
    args = parser.parse_args()
    
    # Get data from --data or stdin
    if args.data:
        try:
            data = json.loads(args.data)
        except json.JSONDecodeError as e:
            print(json.dumps({"success": False, "error": f"Invalid JSON: {e}"}))
            sys.exit(1)
    else:
        # Read from stdin
        if sys.stdin.isatty():
            print("Error: No --data provided and stdin is empty", file=sys.stderr)
            print("Usage: echo '{...}' | save_game.py --user-id 123 --universe xiaoao", file=sys.stderr)
            sys.exit(1)
        
        try:
            data = json.load(sys.stdin)
        except json.JSONDecodeError as e:
            print(json.dumps({"success": False, "error": f"Invalid JSON from stdin: {e}"}))
            sys.exit(1)
    
    # Execute save
    result = save_game(args.user_id, args.universe, data, backup=not args.no_backup)
    
    # Output
    if args.quiet:
        print(json.dumps(result))
    else:
        if result["success"]:
            print(f"✅ Game saved successfully!")
            print(f"📁 Path: {result['save_path']}")
            if result.get("backup_path"):
                print(f"💾 Backup: {result['backup_path']}")
            print(f"👤 Character: {result.get('character_name')} (Lv.{result.get('level')})")
        else:
            print(f"❌ Save failed: {result['error']}", file=sys.stderr)
            if result.get("fallback_path"):
                print(f"⚠️ Emergency save: {result['fallback_path']}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
