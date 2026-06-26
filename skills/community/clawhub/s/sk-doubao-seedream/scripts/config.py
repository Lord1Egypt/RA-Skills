#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理脚本 - 设置 API Key
"""

import os, json, sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
CONFIG_FILE = SKILL_DIR / "config.json"

def get_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_config(cfg):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

def main():
    print("=" * 50)
    print("Seedream 配置工具")
    print("=" * 50)
    
    cfg = get_config()
    
    print("\n当前配置:")
    print(f"  API Key: {cfg.get('api_key', '(未设置)')[:8] + '...' if cfg.get('api_key') else '(未设置)'}")
    print(f"  默认模型: {cfg.get('default_model', 'Doubao-Seedream-5.0-lite')}")
    print(f"  输出目录: {cfg.get('output_dir', './generated-images')}")
    print()
    
    print("1. 设置 API Key")
    print("2. 设置默认模型")
    print("3. 设置输出目录")
    print("4. 显示配置")
    print("5. 退出")
    
    c = input("\n选择: ").strip()
    
    if c == "1":
        key = input("输入 API Key: ").strip()
        if key:
            cfg["api_key"] = key
            save_config(cfg)
            print("API Key 已保存!")
    elif c == "2":
        print("\n可用模型:")
        models = ["Doubao-Seedream-5.0-lite", "Doubao-Seedream-4.5", "Doubao-Seedream-4.0", 
                  "Doubao-SeedEdit-3.0-i2i", "Doubao-Seedream-3.0-t2i"]
        for i, m in enumerate(models, 1):
            print(f"  {i}. {m}")
        mc = input("选择 (1-5): ").strip()
        if mc.isdigit() and 1 <= int(mc) <= 5:
            cfg["default_model"] = models[int(mc)-1]
            save_config(cfg)
            print("默认模型已设置!")
    elif c == "3":
        d = input("输入输出目录: ").strip()
        if d:
            cfg["output_dir"] = d
            save_config(cfg)
            print("输出目录已设置!")
    elif c == "4":
        print("\n完整配置:")
        print(json.dumps(cfg, indent=2, ensure_ascii=False))

if __name__ == "__main__": main()
