#!/usr/bin/env python3
"""
OpenClaw 配置更新脚本 - 添加 Hooks 配置

用法:
    python3 update_openclaw_config.py [--dry-run]
"""

import json
import sys
from pathlib import Path
import shutil
from datetime import datetime

# OpenClaw 配置文件路径
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"
HOOK_TOKEN = "6fb57eb806f64da4e70b1b7a8c41f6b97a4788dc9f6b15430cdfedc0b61c75b1"
HOOK_ENDPOINT = "http://127.0.0.1:8765/hook"

def update_config(dry_run=False):
    """更新 OpenClaw 配置文件"""
    
    if not OPENCLAW_CONFIG.exists():
        print(f"错误：配置文件不存在 {OPENCLAW_CONFIG}")
        return False
    
    # 读取现有配置
    with open(OPENCLAW_CONFIG, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 检查是否已配置 hooks
    existing_hooks = config.get('hooks', {})
    if existing_hooks.get('enabled') == True:
        print("⚠️  警告：hooks 已经配置")
        print(f"   当前配置：{json.dumps(existing_hooks, indent=2)}")
        
        response = input("是否覆盖现有配置？(y/N): ")
        if response.lower() != 'y':
            print("已取消")
            return False
    
    # 创建备份
    backup_path = OPENCLAW_CONFIG.with_suffix('.json.hook_backup')
    if not dry_run:
        shutil.copy2(OPENCLAW_CONFIG, backup_path)
        print(f"✅ 已创建备份：{backup_path}")
    
    # 更新配置
    config['hooks'] = {
        'enabled': True,
        'token': HOOK_TOKEN,
        'internal': {
            'enabled': True,
            'endpoint': HOOK_ENDPOINT
        }
    }
    
    if dry_run:
        print("\n📋 预览将要添加的配置:")
        print(json.dumps(config['hooks'], indent=2))
        return True
    
    # 保存新配置
    with open(OPENCLAW_CONFIG, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 配置已更新")
    print(f"\n📋 添加的 hooks 配置:")
    print(json.dumps(config['hooks'], indent=2))
    print(f"\n⚠️  下一步操作:")
    print(f"   1. 重启 OpenClaw Gateway: openclaw gateway restart")
    print(f"   2. 确保 Hook 服务运行：python3 openclaw_hook.py --port 8765 --token {HOOK_TOKEN}")
    print(f"   3. 测试：发送微信消息 '帮我开机' 或 '添加网络唤醒'")
    
    return True


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Update OpenClaw config with hooks')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("OpenClaw Hooks 配置更新工具")
    print("=" * 60)
    print(f"配置文件：{OPENCLAW_CONFIG}")
    print(f"Hook 端点：{HOOK_ENDPOINT}")
    print()
    
    success = update_config(dry_run=args.dry_run)
    
    if success and not args.dry_run:
        print("\n✅ 配置更新完成！请重启 OpenClaw Gateway 使配置生效。")
    elif args.dry_run:
        print("\n💡 这是预览模式，未实际修改配置文件。")
        print("   运行 `python3 update_openclaw_config.py` 应用更改。")
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
