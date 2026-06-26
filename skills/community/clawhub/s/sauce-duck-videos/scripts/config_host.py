#!/usr/bin/env python3
"""
检查并设置sauce-duck-videos.env.RH_HOST
用法: python config_host.py [--check] [--set RH_HOST]
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


def get_host():
    """获取sauce-duck-videos.env.RH_HOST"""
    skill_config = get_skill_config()
    if not skill_config:
        return None
    env = skill_config.get("env", {})
    return env.get("RH_HOST")


def set_host(host):
    """设置sauce-duck-videos.env.RH_HOST"""
    config = load_config() or {}
    
    if "skills" not in config:
        config["skills"] = {}
    if "entries" not in config["skills"]:
        config["skills"]["entries"] = {}
    
    skill_config = config["skills"]["entries"].get("sauce-duck-videos", {})
    skill_config["enabled"] = True
    if "env" not in skill_config:
        skill_config["env"] = {}
    skill_config["env"]["RH_HOST"] = host
    
    config["skills"]["entries"]["sauce-duck-videos"] = skill_config
    save_config(config)


def main():
    if len(sys.argv) < 2:
        print("Usage: python config_host.py [--check] [--set RH_HOST]", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "--check":
        host = get_host()
        result = {
            "has_host": host is not None,
            "host": host
        }
        print(json.dumps(result, ensure_ascii=False))
    elif sys.argv[1] == "--set" and len(sys.argv) >= 3:
        host = sys.argv[2]
        set_host(host)
        print(json.dumps({"success": True, "message": "RH_HOST已保存"}, ensure_ascii=False))
    else:
        print("Usage: python config_host.py [--check] [--set RH_HOST]", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
