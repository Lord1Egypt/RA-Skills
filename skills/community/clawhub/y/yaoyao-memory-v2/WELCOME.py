#!/usr/bin/env python3
"""
记忆系统对话引导 - 对话式初始化

通过对话引导用户完成配置，不需要命令行操作

用法：
    python3 welcome.py              # 启动对话引导
    python3 welcome.py --quick    # 快速设置（用户确认）
    python3 welcome.py --status     # 查看当前状态
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 路径配置
SKILL_DIR = Path(__file__).parent.parent
WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"


def print_welcome():
    """打印欢迎信息"""
    print()
    print("=" * 50)
    print("🦞 摇摇记忆系统 - 初始化向导")
    print("=" * 50)
    print()
    print("你好！我是摇摇的 AI 助手。")
    print("我将帮你完成记忆系统的初始化配置。")
    print()
    print("这个过程很简单，只需要几分钟。")
    print()


def print_status():
    """打印当前状态"""
    print()
    print("📊 当前状态")
    print("-" * 30)
    
    checks = []
    
    # 记忆目录
    if MEMORY_DIR.exists():
        files = list(MEMORY_DIR.glob("*.md"))
        checks.append(("记忆目录", True, f"{len(files)} 个文件"))
    else:
        checks.append(("记忆目录", False, "未创建"))
    
    # 数据库
    db_path = Path.home() / ".openclaw" / "memory-tdai" / "vectors.db"
    if db_path.exists():
        size = db_path.stat().st_size / 1024 / 1024
        checks.append(("数据库", True, f"{size:.1f} MB"))
    else:
        checks.append(("数据库", False, "未创建"))
    
    # 配置文件
    config_path = SKILL_DIR / "config" / "unified_config.json"
    checks.append(("配置文件", config_path.exists(), "已配置" if config_path.exists() else "未创建"))
    
    for name, ok, detail in checks:
        status = "✅" if ok else "❌"
        print(f"  {status} {name}: {detail}")
    
    print()


def ask_cloud_features():
    """询问用户需要哪些云端功能"""
    print()
    print("☁️ 云端功能（可选）")
    print("-" * 30)
    print()
    print("云端功能已拆分到独立的 yaoyao-cloud-backup 技能。")
    print("请选择你需要的功能（可多选）：")
    print()
    print("  1. ☁️ 云端备份 - 将记忆备份到云端（IMA）")
    print("  2. 📱 跨设备同步 - 多设备共享记忆")
    print("  3. 🔄 双向同步 - 本地和云端保持一致")
    print("  0. 暂不需要云端功能")
    print()
    
    features = []
    while True:
        choice = input("请选择 [多选如 1,2 或 0 跳过]: ").strip()
        
        if choice == "0" or choice == "":
            print()
            print("  ℹ️  跳过云端功能，稍后可随时开启")
            return []
        
        # 解析多选（安全校验）
        choices = [c.strip() for c in choice.split(",") if c.strip()]
        valid = True
        for c in choices:
            if c not in ["1", "2", "3"]:
                print(f"  ❌ 无效选项: {c}")
                valid = False
                break
        
        if valid:
            try:
                features = [int(c) for c in choices]
                break
            except ValueError:
                print("  ❌ 输入格式错误")
        else:
            print("请输入如 1,2 或 0")
    
    feature_names = {
        1: "云端备份",
        2: "跨设备同步", 
        3: "双向同步"
    }
    
    print()
    if features:
        print("  ✅ 已选择：" + " + ".join([feature_names[f] for f in features]))
        print()
        print("  💡 问我：\"帮我安装云备份\"")
    
    return features


def ask_enable_push():
    """询问是否启用推送"""
    print("📱 负一屏推送")
    print("-" * 30)
    print()
    print("启用后，任务完成时会收到通知。")
    print()
    print("选项：")
    print("  1. 启用（推荐）")
    print("  2. 暂不启用")
    print()
    
    while True:
        choice = input("请选择 [1/2]: ").strip()
        if choice == "1":
            return True
        elif choice == "2":
            return False
        else:
            print("请输入 1 或 2")


def save_config(push_enabled, cloud_features=None):
    """保存配置"""
    if cloud_features is None:
        cloud_features = []
    
    config_path = SKILL_DIR / "config" / "unified_config.json"
    
    feature_names = {
        1: "cloud_backup",
        2: "cross_device_sync", 
        3: "bidirectional_sync"
    }
    
    config = {
        "version": "3.9.5",
        "features": {
            "vector_search": True,
            "fts_search": True,
            "meo_push": push_enabled,
        },
        "cloud_features_requested": [feature_names.get(f, f) for f in cloud_features],
        "setup": {
            "completed_at": datetime.now().isoformat(),
            "guided": True,
        }
    }
    
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False))
    print(f"✅ 配置已保存")


def run_quick_setup():
    """快速设置 - 自动完成配置"""
    print()
    print("🔧 快速设置 - 自动配置")
    print()
    
    # 创建目录
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    print("✅ 记忆目录")
    
    # 创建数据库
    db_path = Path.home() / ".openclaw" / "memory-tdai"
    db_path.mkdir(parents=True, exist_ok=True)
    print("✅ 数据库目录")
    
    # 保存配置（快速设置不启用云功能）
    save_config(True, [])
    
    print()
    print("✅ 快速设置完成！")


def print_completion(cloud_features=None):
    """打印完成信息"""
    if cloud_features is None:
        cloud_features = []
    
    print()
    print("=" * 50)
    print("🎉 初始化完成！")
    print("=" * 50)
    print()
    print("现在你可以：")
    print("  1. 直接开始使用 - AI 会自动管理记忆")
    print("  2. 查看状态 - 输入: status")
    print("  3. 查看帮助 - 输入: help")
    print()
    
    if cloud_features:
        feature_names = {
            1: "云端备份",
            2: "跨设备同步", 
            3: "双向同步"
        }
        print("☁️ 待安装云功能：" + " + ".join([feature_names[f] for f in cloud_features]))
        print("   问我：\"帮我安装云备份\"")
        print()
    
    print("常见问题：")
    print("  • 如何查看记忆？ - 直接问我")
    print("  • 如何删除记忆？ - 告诉我要删除什么")
    print("  • 如何备份？ - 告诉我要备份，我会帮你")
    print()


def main():
    parser = argparse.ArgumentParser(description="摇摇记忆系统初始化向导")
    parser.add_argument("--quick", "-s", action="store_true", help="快速设置（用户确认）")
    parser.add_argument("--status", action="store_true", help="查看状态")
    
    args = parser.parse_args()
    
    if args.status:
        print_status()
        return
    
    if args.quick:
        run_quick_setup()
        return
    
    # 对话模式
    print_welcome()
    print_status()
    
    # 云端功能选择
    cloud_features = ask_cloud_features()
    
    # 推送配置
    push_enabled = ask_enable_push()
    
    # 保存配置
    save_config(push_enabled, len(cloud_features) > 0)
    
    print_completion(cloud_features)


if __name__ == "__main__":
    main()
