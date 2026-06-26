#!/usr/bin/env python3
"""
检查并设置Skills配置中的sauce-duck-videos
用法: python config_api_key.py [--check] [--set API_KEY]
"""

import sys
import json
import os


def get_openclaw_config_path():
    """获取openclaw.json配置文件路径"""
    home = os.path.expanduser("~")
    return os.path.join(home, ".openclaw", "openclaw.json")


def load_config():
    """加载openclaw.json配置"""
    config_path = get_openclaw_config_path()
    if not os.path.exists(config_path):
        return None
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def save_config(config):
    """保存openclaw.json配置"""
    config_path = get_openclaw_config_path()
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def get_skill_config():
    """获取sauce-duck-videos的配置"""
    config = load_config()
    if not config:
        return None
    skills = config.get("skills", {})
    entries = skills.get("entries", {})
    return entries.get("sauce-duck-videos")


def has_skill_config():
    """检查是否存在sauce-duck-videos配置"""
    skill_config = get_skill_config()
    return skill_config is not None


def get_api_key():
    """获取sauce-duck-videos的apiKey"""
    skill_config = get_skill_config()
    if not skill_config:
        return None
    return skill_config.get("apiKey")


def set_skill_config(api_key):
    """设置sauce-duck-videos的完整配置"""
    config = load_config() or {}
    if "skills" not in config:
        config["skills"] = {}
    if "entries" not in config["skills"]:
        config["skills"]["entries"] = {}
    
    skill_config = config["skills"]["entries"].get("sauce-duck-videos", {})
    skill_config["enabled"] = True
    skill_config["apiKey"] = api_key
    if "env" not in skill_config:
        skill_config["env"] = {}
    
    config["skills"]["entries"]["sauce-duck-videos"] = skill_config
    save_config(config)


def main():
    if len(sys.argv) < 2:
        print("Usage: python config_api_key.py [--check] [--set API_KEY]", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "--check":
        has_config = has_skill_config()
        api_key = get_api_key() if has_config else None
        result = {
            "has_skill_config": has_config,
            "has_api_key": api_key is not None,
            "api_key": api_key
        }
        print(json.dumps(result, ensure_ascii=False))
    elif sys.argv[1] == "--set" and len(sys.argv) >= 3:
        api_key = sys.argv[2]
        set_skill_config(api_key)
        print(json.dumps({"success": True, "message": "skill配置已保存"}, ensure_ascii=False))
    else:
        print("Usage: python config_api_key.py [--check] [--set API_KEY]", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
