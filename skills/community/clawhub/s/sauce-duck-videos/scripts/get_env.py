#!/usr/bin/env python3
"""
获取sauce-duck-videos的配置
用法: python get_env.py
"""

import os
import json


def get_openclaw_config_path():
    home = os.path.expanduser("~")
    return os.path.join(home, ".openclaw", "openclaw.json")


def get_env():
    config_path = get_openclaw_config_path()
    if not os.path.exists(config_path):
        return {"host": None, "api_key": None}

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        skill = config.get("skills", {}).get("entries", {}).get("sauce-duck-videos", {})
        env = skill.get("env", {})

        host = env.get("RH_HOST")
        api_key = skill.get("apiKey")

        return {"host": host, "api_key": api_key}
    except Exception:
        return {"host": None, "api_key": None}


result = get_env()
print(json.dumps(result, ensure_ascii=False))