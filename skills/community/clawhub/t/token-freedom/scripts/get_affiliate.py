#!/usr/bin/env python3
"""
联盟配置解析器
用法: python get_affiliate.py <平台key>
      python get_affiliate.py --all
数据来源优先级: ~/.qclaw/affiliate-config.json > references/default_config.json
"""
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
DEFAULT_CONFIG = SKILL_DIR / "references" / "default_config.json"
USER_CONFIG = Path.home() / ".qclaw" / "affiliate-config.json"


def load_config():
    """加载配置，用户配置覆盖默认配置"""
    config = {}

    # 1. 先加载默认配置（Skill 自带的）
    if DEFAULT_CONFIG.exists():
        with open(DEFAULT_CONFIG, "r", encoding="utf-8") as f:
            config.update(json.load(f))

    # 2. 用户配置覆盖（如果有的话）
    if USER_CONFIG.exists():
        with open(USER_CONFIG, "r", encoding="utf-8") as f:
            user = json.load(f)
            config.update(user)

    return config


def main():
    config = load_config()

    if len(sys.argv) < 2:
        print("用法: python get_affiliate.py <key>")
        print("      python get_affiliate.py --all")
        print(f"\n可用 Key: {', '.join(config.keys())}")
        return

    arg = sys.argv[1]

    if arg == "--all":
        print(json.dumps(config, ensure_ascii=False, indent=2))
        return

    value = config.get(arg)
    if value:
        print(value)
    else:
        print(f"ERROR: key '{arg}' not found", file=sys.stderr)
        print(f"可用: {', '.join(config.keys())}", file=sys.stderr)


if __name__ == "__main__":
    main()
