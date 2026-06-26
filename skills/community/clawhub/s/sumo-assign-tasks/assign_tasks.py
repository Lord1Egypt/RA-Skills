#!/usr/bin/env python3
"""
Sumo Assign Tasks - 任務派發方法開關

用法:
    python assign_tasks.py              # 顯示目前設定
    python assign_tasks.py 0           # 切換到 sessions_spawn
    python assign_tasks.py 1           # 切換到 clawteam
    python assign_tasks.py 2           # 切換到 SumoSubAgent
"""

import json
import os
import sys

CONFIG_PATH = r"C:\Users\rayray\.openclaw\workspace\memory\assign_method.json"

METHODS = {
    "0": "sessions_spawn",
    "1": "clawteam",
    "2": "sumosubagent"
}

METHODS_DISPLAY = {
    "sessions_spawn": "✅ sessions_spawn（蘇茉現在用的）",
    "clawteam": "clawteam",
    "sumosubagent": "SumoSubAgent"
}

def load_config():
    """載入設定"""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"method": "sessions_spawn", "name": "sessions_spawn"}

def save_config(method):
    """儲存設定"""
    config = {
        "method": method,
        "name": METHODS.get(method, method)
    }
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    return config

def show_current():
    """顯示目前設定"""
    config = load_config()
    current = config.get("name", "sessions_spawn")
    
    print("\n[Sumo Assign Tasks] Currently Using:")
    print("=" * 50)
    print("| Param | Tool               | Active?            |")
    print("| --   | --------------     | ----------------   |")
    print("| 0     | sessions_spawn   | {0} |".format(
        "[ACTIVE]" if current == "sessions_spawn" else ""
    ))
    print("| 1     | clawteam         | {0} |".format(
        "[ACTIVE]" if current == "clawteam" else ""
    ))
    print("| 2     | SumoSubAgent    | {0} |".format(
        "[ACTIVE]" if current == "SumoSubAgent" else ""
    ))
    print("=" * 50)
    print(f"\nCurrent: {current}")

def main():
    if len(sys.argv) < 2:
        show_current()
        return
    
    arg = sys.argv[1]
    
    if arg not in METHODS:
        print(f"❌ 無效的參數：{arg}")
        print("有效的參數：0, 1, 2")
        return
    
    config = save_config(METHODS[arg])
    print(f"[OK] Switched to: {config['name']}")

if __name__ == "__main__":
    main()
