#!/usr/bin/env python3
"""Interactive setup wizard for screen-activity-tracker skill."""

import json
import os
import sys

EXAMPLE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.example.json")
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")


def main():
    print("=== Screen Activity Tracker Setup ===\n")

    # Load example defaults
    with open(EXAMPLE_PATH) as f:
        config = json.load(f)

    # ===== Backend selection =====
    print(">> 1. Backend Selection")
    print("   1) local  - 记录到本地 markdown 文件")
    print("   2) siyuan - 记录到思源笔记")
    b = input("   选择后端 [local]: ").strip() or "local"
    config["backend"] = b

    if b == "siyuan":
        print("\n>> 思源笔记配置")
        url = input("   SiYuan URL [http://127.0.0.1:6806]: ").strip()
        config["siyuan"]["url"] = url or "http://127.0.0.1:6806"

        token = input("   API Token: ").strip()
        if not token:
            print("   ERROR: 使用思源后端需要 Token")
            sys.exit(1)
        config["siyuan"]["token"] = token

        nb = input("   Notebook ID: ").strip()
        if not nb:
            print("   ERROR: 需要 Notebook ID")
            sys.exit(1)
        config["siyuan"]["notebook_id"] = nb

    # ===== Local backend config =====
    if b == "local":
        print("\n>> 本地存储配置")
        od = input("   输出目录 [~/screen-activity]: ").strip()
        if od:
            config["local"]["output_dir"] = od
        kd = input(f"   截图保留天数 [{config['local']['keep_days']}]: ").strip()
        if kd:
            config["local"]["keep_days"] = int(kd)

    # ===== MLX config =====
    print("\n>> 视觉模型配置")
    mlx = input(f"   MLX URL [{config.get('mlx_url', '')}]: ").strip()
    if mlx:
        config["mlx_url"] = mlx

    # ===== Analysis mode =====
    print("\n>> 分析模式")
    print("   1) simple     - 描述在做什么（默认）")
    print("   2) category   - 分类：工作/娱乐/学习/休息")
    print("   3) productivity- 生产力评分 1-10")
    print("   4) custom     - 自定义提示词")
    am = input("   选择 [simple]: ").strip() or "simple"

    mode_map = {"1": "simple", "2": "category", "3": "productivity", "4": "custom"}
    config["analysis_mode"] = mode_map.get(am, am)

    if config["analysis_mode"] == "custom":
        p = input("   自定义提示词: ").strip()
        config["analysis_prompt"] = p

    # ===== Interval =====
    print("\n>> 定时频率")
    iv = input(f"   间隔分钟 [{config['interval_minutes']}]: ").strip()
    if iv:
        config["interval_minutes"] = int(iv)

    # ===== Idle detection =====
    print("\n>> 闲置检测")
    idl = input("   开启闲置检测（闲置>5分钟跳过）? [Y/n]: ").strip().lower()
    config["idle_detection"] = idl != "n"

    # ===== App blacklist =====
    print("\n>> 应用黑名单（匹配关键词的 App 跳过截图）")
    bl = input(f"   逗号分隔关键词 [银行,密码,支付宝,微信支付,登录]: ").strip()
    if bl:
        config["app_blacklist"] = [x.strip() for x in bl.split(",")]
    else:
        config["app_blacklist"] = ["银行", "密码", "支付宝", "微信支付", "登录"]

    # ===== Write config =====
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"\n✓ 配置已写入: {CONFIG_PATH}")
    print("\n=== 下一步 ===")
    print("   1. 测试运行:  bash scripts/screen-activity.sh")
    print("   2. 在 OpenClaw 中说: '开始追踪屏幕'")
    print("   3. 或手动创建 cron: openclaw cron add --schedule '*/5 * * * *' --command 'bash /path/to/scripts/screen-activity.sh'\n")


if __name__ == "__main__":
    main()
