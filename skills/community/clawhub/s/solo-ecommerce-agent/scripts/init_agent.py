#!/usr/bin/env python3
"""
电商智能体初始化脚本
帮助用户快速配置智能体，创建必要的数据目录和配置文件
"""

import json
import os
from pathlib import Path

# 数据目录
DATA_DIR = Path.home() / "solo-ecommerce-data"

def init_data_directory():
    """初始化数据目录结构"""
    DATA_DIR.mkdir(exist_ok=True)
    (DATA_DIR / "logs").mkdir(exist_ok=True)
    
    print(f"✅ 数据目录已创建：{DATA_DIR}")
    
    # 创建初始数据文件
    init_file(DATA_DIR / "products.json", [])
    init_file(DATA_DIR / "orders.json", [])
    init_file(DATA_DIR / "recommendations.json", [])
    init_file(DATA_DIR / "customers.json", {})
    
    print("✅ 数据文件已初始化")

def init_file(filepath, default_content):
    """初始化文件"""
    if not filepath.exists():
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(default_content, f, ensure_ascii=False, indent=2)
        print(f"  - 创建：{filepath.name}")

def create_config(platforms, automation_config):
    """
    创建配置文件
    
    Args:
        platforms: 平台列表 ["淘宝", "抖店"]
        automation_config: 自动化配置
    """
    config = {
        "version": "1.0.0",
        "created": get_timestamp(),
        "platforms": platforms,
        "automation_scope": {
            "auto_publish": automation_config.get("auto_publish", False),
            "auto_pricing": automation_config.get("auto_pricing", False),
            "auto_reply": automation_config.get("auto_reply", True),
            "auto_ship": automation_config.get("auto_ship", False),
            "complaint_to_manual": True,
            "refund_threshold": automation_config.get("refund_threshold", 50)
        },
        "risk_controls": {
            "publish_needs_review": automation_config.get("publish_needs_review", True),
            "ship_needs_confirm": automation_config.get("ship_needs_confirm", True),
            "complaint_auto_escalate": True,
            "logistics_alert_days": 3
        },
        "schedules": {
            "product_scan": "0 * * * *",
            "customer_service": "*/5 * * * *",
            "order_process": "*/10 * * * *",
            "daily_report": "0 23 * * *"
        }
    }
    
    config_file = DATA_DIR / "config.json"
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 配置文件已创建：{config_file}")
    return config_file

def get_timestamp():
    """获取当前时间戳"""
    from datetime import datetime
    return datetime.now().isoformat()

def setup_cron_jobs():
    """
    设置定时任务
    注意：需要通过OpenClaw的cron系统配置
    """
    print("\n定时任务配置：")
    print("需要在OpenClaw中配置以下cron任务：")
    print("1. 选品扫描：每小时执行（cron: 0 * * * *）")
    print("2. 客服回复：每5分钟执行（cron: */5 * * * *）")
    print("3. 订单处理：每10分钟执行（cron: */10 * * * *）")
    print("4. 数据复盘：每天23:00执行（cron: 0 23 * * *）")

def interactive_setup():
    """交互式配置"""
    print("=" * 50)
    print("电商智能体初始化向导")
    print("=" * 50)
    
    # 初始化数据目录
    init_data_directory()
    
    # 平台配置
    print("\n请选择运营平台（多选用逗号分隔）：")
    print("1. 淘宝/天猫")
    print("2. 抖音小店")
    print("3. 拼多多")
    print("4. 京东")
    print("5. 其他")
    
    platform_input = input("\n输入选项（如：1,2,3）：").strip()
    
    platform_map = {
        "1": "淘宝",
        "2": "抖店",
        "3": "拼多多",
        "4": "京东",
        "5": "其他"
    }
    
    platforms = []
    for p in platform_input.split(","):
        p = p.strip()
        if p in platform_map:
            platforms.append(platform_map[p])
    
    print(f"\n已选择平台：{', '.join(platforms)}")
    
    # 自动化配置
    print("\n请配置自动化范围：")
    
    auto_reply = input("自动回复客服消息？(y/n，默认y)：").strip().lower() != "n"
    auto_publish = input("自动上架商品？(y/n，默认n)：").strip().lower() == "y"
    auto_ship = input("自动处理发货？(y/n，默认n)：").strip().lower() == "y"
    
    if auto_publish:
        publish_review = input("上架前需要人工审核？(y/n，默认y)：").strip().lower() != "n"
    else:
        publish_review = True
    
    if auto_ship:
        ship_confirm = input("发货前需要人工确认？(y/n，默认y)：").strip().lower() != "n"
    else:
        ship_confirm = True
    
    refund_threshold = input("自动处理退款上限（元，默认50）：").strip()
    try:
        refund_threshold = int(refund_threshold) if refund_threshold else 50
    except ValueError:
        refund_threshold = 50
    
    # 创建配置
    config = {
        "auto_reply": auto_reply,
        "auto_publish": auto_publish,
        "auto_ship": auto_ship,
        "publish_needs_review": publish_review,
        "ship_needs_confirm": ship_confirm,
        "refund_threshold": refund_threshold
    }
    
    create_config(platforms, config)
    
    # 设置定时任务提示
    setup_cron_jobs()
    
    print("\n" + "=" * 50)
    print("✅ 初始化完成！")
    print("=" * 50)
    print("\n下一步：")
    print("1. 保持浏览器已登录店铺后台")
    print("2. 运行脚本开始自动运营")
    print("3. 查看日报了解运营情况")
    
    return DATA_DIR

def main():
    """主入口"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        # 快速初始化（无交互）
        init_data_directory()
        create_default_config()
        print("✅ 快速初始化完成")
    else:
        # 交互式初始化
        interactive_setup()

def create_default_config():
    """创建默认配置"""
    config = {
        "version": "1.0.0",
        "created": get_timestamp(),
        "platforms": ["淘宝", "抖店"],
        "automation_scope": {
            "auto_publish": False,
            "auto_pricing": False,
            "auto_reply": True,
            "auto_ship": False
        },
        "risk_controls": {
            "publish_needs_review": True,
            "ship_needs_confirm": True
        }
    }
    
    config_file = DATA_DIR / "config.json"
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
