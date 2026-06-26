#!/usr/bin/env python3.9
"""
配置 API Key 工具
"""

import os
import sys

def configure_api_key(api_key, domain="agent-sandbox.baidu-int.com"):
    """
    配置沙箱 API Key

    Args:
        api_key: API Key
        domain: 沙箱域名
    """
    env_path = os.path.expanduser('~/.env')

    # 读取现有配置
    existing = {}
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    existing[key.strip()] = value.strip()

    # 更新配置
    existing['E2B_API_KEY'] = api_key
    existing['E2B_DOMAIN'] = domain

    # 写入文件
    with open(env_path, 'w') as f:
        f.write(f"E2B_API_KEY={api_key}\n")
        f.write(f"E2B_DOMAIN={domain}\n")

        # 写入其他配置
        for key, value in existing.items():
            if key not in ['E2B_API_KEY', 'E2B_DOMAIN']:
                f.write(f"{key}={value}\n")

    print(f"✅ API Key 已保存到: {env_path}")
    print(f"   API Key: {api_key[:10]}...")
    print(f"   Domain: {domain}")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='配置沙箱 API Key')
    parser.add_argument('api_key', help='API Key')
    parser.add_argument('--domain', '-d', default='agent-sandbox.baidu-int.com', help='沙箱域名')

    args = parser.parse_args()

    configure_api_key(args.api_key, args.domain)