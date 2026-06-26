#!/usr/bin/env python3
"""星桥 Skill 安装脚本

安装时自动生成 64 位唯一 Token 并写入 config.json
"""
import os
import sys
import json
import uuid
import requests
from pathlib import Path

# 配置
API_BASE = "http://121.40.126.7"
CONFIG_PATH = Path(__file__).parent.parent / "config.json"


def generate_skill_token():
    """生成唯一的 Skill Token
    
    固定长度: 64 位
    """
    # 生成 64 位唯一 ID
    return uuid.uuid4().hex + uuid.uuid4().hex[:32]  # 32 + 32 = 64 位


def register_skill_account(skill_token: str):
    """向星桥平台登录（自动创建账户）
    
    Args:
        skill_token: 生成的 64 位 skill token
        
    Returns:
        JWT token 用于后续 API 调用
    """
    url = f"{API_BASE}/api/auth/login?token_id={skill_token}&auto_create=true"
    
    try:
        response = requests.post(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token"), data.get("encrypted_token_id"), data.get("user", {}).get("username")
        else:
            print(f"登录失败: {response.status_code} - {response.text}")
            return None, None, None
    except Exception as e:
        print(f"请求失败: {e}")
        return None, None, None


def create_config(jwt_token: str, encrypted_token_id: str, username: str, token_id: str):
    """创建或更新 config.json"""
    config = {
        "token": jwt_token,
        "token_id": token_id,
        "encrypted_token_id": encrypted_token_id,
        "skill_username": username,
        "api_base": API_BASE
    }
    
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] 配置已写入: {CONFIG_PATH}")
    return config


def main():
    print("=" * 60)
    print("星桥 Skill 安装")
    print("=" * 60)
    
    # 1. 生成唯一 token
    skill_token = generate_skill_token()
    print(f"\n[1/3] 生成 Skill Token: {skill_token[:20]}...{skill_token[-8:]}")
    print(f"      长度: {len(skill_token)} 字符")
    
    # 2. 注册账号获取 JWT
    print(f"\n[2/3] 注册 Skill 账号...")
    jwt_token, encrypted_token_id, username = register_skill_account(skill_token)
    
    if not jwt_token:
        print("\n[错误] 注册失败，请检查网络连接或 API 服务")
        print("       你可以手动运行以下命令重试：")
        print("       python scripts/install.py")
        sys.exit(1)
    
    print(f"      账号: {username}")
    print(f"      JWT: {jwt_token[:30]}...")
    
    # 3. 写入配置
    print(f"\n[3/3] 写入配置文件...")
    config = create_config(jwt_token, encrypted_token_id, username, skill_token)
    
    print("\n" + "=" * 60)
    print("[完成] 星桥 Skill 安装成功！")
    print("=" * 60)
    print(f"\nToken ID: {skill_token}")
    print(f"加密Token ID: {encrypted_token_id}")
    print("\n现在可以使用以下命令：")
    print('  星桥 发送 你好')
    print('  星桥 最新消息')
    print('  星桥 问 <问题>')
    print("\n" + "-" * 60)
    print("【重要】请保存您的 Token ID，可用于登录前端查看：")
    print(f"  前端地址: http://121.40.126.7")
    print(f"  Token ID: {skill_token}")
    print("-" * 60)


if __name__ == "__main__":
    main()
