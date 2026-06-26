#!/usr/bin/env python3
"""
龙虾记忆系统 - 迁移脚本
为已安装用户自动配置 IMA 凭证
"""

import argparse
import json
import os
from pathlib import Path


def check_existing_ima_config() -> dict:
    """检查现有 IMA 配置"""
    config = {
        "has_env": False,
        "has_file": False,
        "client_id": None,
        "api_key": None,
    }
    
    # 检查环境变量
    if os.environ.get("IMA_OPENAPI_CLIENTID") and os.environ.get("IMA_OPENAPI_APIKEY"):
        config["has_env"] = True
        config["client_id"] = os.environ.get("IMA_OPENAPI_CLIENTID")
        config["api_key"] = os.environ.get("IMA_OPENAPI_APIKEY")
    
    # 检查配置文件
    config_dir = Path.home() / ".config" / "ima"
    if config_dir.exists():
        client_id_file = config_dir / "client_id"
        api_key_file = config_dir / "api_key"
        
        if client_id_file.exists() and api_key_file.exists():
            config["has_file"] = True
            if not config["client_id"]:
                config["client_id"] = client_id_file.read_text().strip()
            if not config["api_key"]:
                config["api_key"] = api_key_file.read_text().strip()
    
    return config


def migrate_ima_config(client_id: str, api_key: str) -> bool:
    """迁移 IMA 配置到文件"""
    config_dir = Path.home() / ".config" / "ima"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    (config_dir / "client_id").write_text(client_id)
    (config_dir / "api_key").write_text(api_key)
    
    return True


def check_today_task_config() -> dict:
    """检查 today-task 配置"""
    config = {
        "has_auth_code": False,
        "auth_code": None,
    }
    
    return config


def main():
    parser = argparse.ArgumentParser(description="迁移 yaoyao-memory 配置")
    parser.add_argument("--ima-client-id", help="IMA Client ID")
    parser.add_argument("--ima-api-key", help="IMA API Key")
    parser.add_argument("--check", action="store_true", help="仅检查配置状态")
    args = parser.parse_args()
    
    print("🦞 龙虾记忆系统 - 配置迁移")
    print("=" * 40)
    
    # 检查 IMA 配置
    print("\n📋 检查 IMA 配置...")
    ima_config = check_existing_ima_config()
    
    if ima_config["has_env"] or ima_config["has_file"]:
        print("   ✅ IMA 凭证已配置")
        if ima_config["client_id"]:
            print(f"   Client ID: {ima_config['client_id'][:10]}***")
    else:
        print("   ⚠️  IMA 凭证未配置")
        print("   获取凭证: https://ima.qq.com/agent-interface")
    
    # 检查 today-task 配置
    print("\n📋 检查 today-task 配置...")
    today_task_config = check_today_task_config()
    
    if today_task_config["has_auth_code"]:
        print("   ✅ today-task 授权码已配置")
    else:
        print("   ⚠️  today-task 授权码未配置")
        print("   配置命令: openclaw config set skills.entries.today-task.config.authCode YOUR_CODE")
    
    # 如果只是检查，到此结束
    if args.check:
        print("\n" + "=" * 40)
        print("检查完成")
        return
    
    # 迁移 IMA 配置
    if args.ima_client_id and args.ima_api_key:
        print("\n🚀 迁移 IMA 配置...")
        if migrate_ima_config(args.ima_client_id, args.ima_api_key):
            print("   ✅ IMA 配置已迁移到 ~/.config/ima/")
    elif not (ima_config["has_env"] or ima_config["has_file"]):
        print("\n💡 提示：请提供 IMA 凭证进行迁移")
        print("   python3 migrate.py --ima-client-id YOUR_ID --ima-api-key YOUR_KEY")
    
    print("\n" + "=" * 40)
    print("✅ 迁移完成")


if __name__ == "__main__":
    main()
