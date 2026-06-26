#!/usr/bin/env python3
"""
初始化主实例脚本
作者：码爪
"""

import argparse
import json
from pathlib import Path

def init_master(name):
    """初始化爪爪主实例"""
    
    # 创建实例配置
    config = {
        "name": name,
        "type": "master",
        "role": "coordinator",
        "slaves": [],
        "status": "active",
        "capabilities": ["调度", "协调", "对外接口"]
    }
    
    # 保存配置
    config_dir = Path.home() / ".zhua" / "distributed"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    config_file = config_dir / f"{name}.json"
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"🐾 主实例初始化成功")
    print(f"名称: {name}")
    print(f"类型: {config['type']}")
    print(f"角色: {config['role']}")
    print(f"配置: {config_file}")
    print()
    print("下一步:")
    print("1. 启动主实例服务")
    print("2. 添加副实例")
    print("3. 开始任务分发")

def main():
    parser = argparse.ArgumentParser(description="初始化爪爪主实例")
    parser.add_argument("--name", type=str, default="zhua-master", help="实例名称")
    
    args = parser.parse_args()
    init_master(args.name)

if __name__ == "__main__":
    main()
