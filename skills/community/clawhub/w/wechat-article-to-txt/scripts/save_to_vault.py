#!/usr/bin/env python3
"""
save_to_vault.py - 将生成的笔记存入 Obsidian Vault

用法:
    python3 save_to_vault.py --note /path/to/note.md [--vault /path/to/vault] [--dir "Inbox/微信公众号"]
"""

import argparse
import json
import os
import shutil
import sys


def get_obsidian_config():
    """从 Obsidian 配置文件获取 vault 路径"""
    obsidian_json_path = os.path.expanduser(
        '~/Library/Application Support/obsidian/obsidian.json'
    )
    if os.path.exists(obsidian_json_path):
        try:
            with open(obsidian_json_path, 'r') as f:
                config = json.load(f)
            vaults = config.get('vaults', {})
            # 找到第一个打开的 vault
            for vault_id, vault_info in vaults.items():
                if vault_info.get('open'):
                    return vault_info.get('path', '')
            # 如果没有打开的 vault，返回第一个
            for vault_info in vaults.values():
                return vault_info.get('path', '')
        except (json.JSONDecodeError, KeyError):
            pass
    return ''


def main():
    parser = argparse.ArgumentParser(description='保存笔记到 Obsidian Vault')
    parser.add_argument('--note', '-n', required=True, help='笔记文件路径')
    parser.add_argument('--vault', '-v', default='', help='Vault 根目录路径')
    parser.add_argument('--dir', '-d', default='Inbox/微信公众号', help='Vault 内子目录')

    args = parser.parse_args()

    if not os.path.exists(args.note):
        print(f'❌ 笔记文件不存在: {args.note}')
        sys.exit(1)

    # 确定 vault 路径
    vault_path = args.vault
    if not vault_path:
        vault_path = get_obsidian_config()

    if not vault_path:
        print('❌ 未找到 Obsidian vault 路径')
        print('💡 请通过 --vault 参数指定，或确保 Obsidian 已配置')
        sys.exit(1)

    if not os.path.exists(vault_path):
        print(f'❌ Vault 目录不存在: {vault_path}')
        sys.exit(1)

    # 构建目标路径
    target_dir = os.path.join(vault_path, args.dir)
    os.makedirs(target_dir, exist_ok=True)

    # 获取文件名
    filename = os.path.basename(args.note)
    target_path = os.path.join(target_dir, filename)

    # 复制文件
    shutil.copy2(args.note, target_path)

    print(f'✅ 笔记已存入 Obsidian vault')
    print(f'   📂 {target_path}')

    # 显示 vault 相对路径
    rel_path = os.path.relpath(target_path, vault_path)
    print(f'   📎 Vault: {rel_path}')


if __name__ == '__main__':
    main()
