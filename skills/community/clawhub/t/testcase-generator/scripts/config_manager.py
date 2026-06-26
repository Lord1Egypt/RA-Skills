#!/usr/bin/env python3
"""
配置管理工具
查看、修改技能配置
"""

import sys
import json
import os

CONFIG_FILE = os.path.expanduser('~/.openclaw/skills/test-case-generator/config.json')

DEFAULT_CONFIG = {
    "default_prompt": "default-prompt",
    "default_format": "csv",
    "default_priority_rules": {
        "P0": ["核心功能", "关键业务流程", "高频使用"],
        "P1": ["重要功能", "中等风险", "中等频率"],
        "P2": ["次要功能", "边缘场景", "低频率"]
    },
    "required_fields": ["模块名称", "用例 ID", "用例标题", "前置条件", "步骤", "预期", "测试类型", "优先级", "测试所属阶段"],
    "min_cases_per_feature": 3,
    "enable_quality_check": True,
    "auto_generate_testdata": True
}

def load_config():
    """加载配置"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()

def save_config(config):
    """保存配置"""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def view_config():
    """查看配置"""
    config = load_config()
    print("=" * 60)
    print("测试用例生成技能 - 配置")
    print("=" * 60)
    for key, value in config.items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for k, v in value.items():
                print(f"  {k}: {v}")
        else:
            print(f"{key}: {value}")
    print("=" * 60)

def set_config(key, value):
    """设置配置项"""
    config = load_config()
    
    # 尝试转换类型
    if value.lower() == 'true':
        value = True
    elif value.lower() == 'false':
        value = False
    elif value.isdigit():
        value = int(value)
    
    config[key] = value
    save_config(config)
    print(f"✅ 已设置 {key} = {value}")

def reset_config():
    """重置配置"""
    save_config(DEFAULT_CONFIG)
    print("✅ 配置已重置为默认值")

def main():
    if len(sys.argv) < 2:
        print("配置管理工具")
        print("\n用法：python config_manager.py <命令> [参数]")
        print("\n命令:")
        print("  view                    - 查看当前配置")
        print("  set <键> <值>          - 设置配置项")
        print("  reset                   - 重置为默认配置")
        print("  path                    - 显示配置文件路径")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'view':
        view_config()
    elif command == 'set':
        if len(sys.argv) < 4:
            print("用法：python config_manager.py set <键> <值>")
            sys.exit(1)
        set_config(sys.argv[2], sys.argv[3])
    elif command == 'reset':
        reset_config()
    elif command == 'path':
        print(f"配置文件：{CONFIG_FILE}")
    else:
        print(f"❌ 未知命令：{command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
