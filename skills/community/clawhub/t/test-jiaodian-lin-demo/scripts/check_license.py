#!/usr/bin/env python3
"""
授权码验证脚本 - 收费技能演示
验证方式：简单哈希验证，生产环境建议使用更安全的签名验证
"""

import argparse
import hashlib
import os
import sys
from typing import Tuple

# 公钥/盐值，实际部署请修改为你自己的值
SALT = "PaidSkillDemoClawHub2024"


def hash_license(license_key: str, salt: str = SALT) -> str:
    """计算授权码哈希"""
    return hashlib.sha256((license_key + salt).encode()).hexdigest()


def check_license() -> Tuple[bool, str]:
    """
    检查授权码
    返回: (是否有效, 消息)
    """
    license_key = os.environ.get("SKILL_LICENSE_KEY", "").strip()
    
    if not license_key:
        return False, "未配置授权码，请设置环境变量 SKILL_LICENSE_KEY"
    
    # 这里存储已授权的哈希，实际可以从你的服务器动态验证
    # 示例：license "demo-license-123" 哈希后是:
    expected_hash = hash_license("demo-license-123")
    
    # 检查用户提供的授权码
    user_hash = hash_license(license_key)
    
    if user_hash == expected_hash:
        return True, "授权验证通过"
    
    # 生产环境可以在这里增加联网验证
    # import requests
    # response = requests.post("https://your-server.com/verify", json={"key": license_key})
    # return response.json().get("valid", False)
    
    return False, "授权码无效，请检查 SKILL_LICENSE_KEY 配置"


def main():
    parser = argparse.ArgumentParser(description="检查收费技能授权")
    args = parser.parse_args()
    
    valid, msg = check_license()
    
    if valid:
        print(f'{"valid": true, "message": "{msg}"}')
        sys.exit(0)
    else:
        print(f'{"valid": false, "message": "{msg}"}', file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
