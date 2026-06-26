#!/usr/bin/env python3
"""Novel Writer 配置管理"""

import json
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "novel-writer.json"

DEFAULT_CONFIG = {
    "version": "2.1.0",
    "defaults": {
        "max_chapter_words": 3000,
        "min_chapter_words": 2000,
        "hook_interval_words": 500,
        "max_paragraph_words": 200,
        "missing_character_gap": 5,
        "foreshadow_warning_chapters": [20, 50, 100],
    },
    "novels": {},
    "active_novel": None,
}

def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        # 合并缺失的默认值
        for k, v in DEFAULT_CONFIG.items():
            if k not in cfg:
                cfg[k] = v
        return cfg
    return DEFAULT_CONFIG.copy()

def save_config(cfg):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

def register_novel(name, path):
    cfg = load_config()
    p = str(Path(path).resolve())
    if name in cfg["novels"] and cfg["novels"][name] != p:
        print(f"⚠️  '{name}' 已存在（路径: {cfg['novels'][name]}），已更新")
    cfg["novels"][name] = p
    cfg["active_novel"] = name
    save_config(cfg)
    print(f"✅ 已注册小说: {name} → {p}")

def list_novels():
    cfg = load_config()
    if not cfg["novels"]:
        print("📦 暂无注册小说。用 register <名称> <路径> 注册。")
        return
    print(f"📚 已注册小说 ({len(cfg['novels'])})\n")
    for name, path in cfg["novels"].items():
        marker = " ← 当前" if name == cfg["active_novel"] else ""
        print(f"  • {name}{marker}")
        print(f"    {path}")

def set_active(name):
    cfg = load_config()
    if name not in cfg["novels"]:
        print(f"❌ 未找到小说: {name}")
        return
    cfg["active_novel"] = name
    save_config(cfg)
    print(f"✅ 当前小说: {name}")

def get_active():
    cfg = load_config()
    name = cfg.get("active_novel")
    if not name or name not in cfg["novels"]:
        return None, None
    return name, Path(cfg["novels"][name])

def main():
    import sys
    if len(sys.argv) < 2:
        print("📖 novel-writer 配置管理")
        print("用法: config <register|list|set|show>")
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd == "register" and len(sys.argv) >= 4:
        register_novel(sys.argv[2], sys.argv[3])
    elif cmd == "list":
        list_novels()
    elif cmd == "set" and len(sys.argv) >= 3:
        set_active(sys.argv[2])
    elif cmd == "show":
        cfg = load_config()
        print(json.dumps(cfg, ensure_ascii=False, indent=2))
    else:
        print(f"❌ 未知命令: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
