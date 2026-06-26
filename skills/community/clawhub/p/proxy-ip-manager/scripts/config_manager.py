#!/usr/bin/env python3
"""
配置管理模块
- 配置存储和读取
- 密钥验证
- 自动获取 secret_token
- 脱敏输出
"""

import os
import json
import re
import requests
from datetime import datetime
from pathlib import Path

# 配置文件路径
CONFIG_DIR = Path.home() / ".openclaw" / "skills" / "proxy-ip-manager"
CONFIG_FILE = CONFIG_DIR / "config.json"
STATS_DIR = CONFIG_DIR / "stats"

# 默认配置
DEFAULT_CONFIG = {
    "secret_id": "",
    "secret_key": "",
    "secret_token": "",
    "token_expire_time": None,
    "test_url": "https://httpbin.org/ip",
    "timeout": 5,
    "configured_at": None
}

# Token 获取接口
TOKEN_API_URL = "https://auth.kdlapi.com/api/get_secret_token"


def ensure_dirs():
    """确保目录存在"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    STATS_DIR.mkdir(parents=True, exist_ok=True)


def load_config():
    """加载配置"""
    ensure_dirs()
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()


def save_config(config):
    """保存配置"""
    ensure_dirs()
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def validate_credentials(secret_id, secret_key):
    """验证密钥格式"""
    if not secret_id:
        return False, "secret_id 不能为空"
    if not secret_key:
        return False, "secret_key 不能为空"
    
    # 基本格式检查
    if len(secret_id) < 10:
        return False, "secret_id 格式无效"
    if len(secret_key) < 10:
        return False, "secret_key 格式无效"
    
    return True, "密钥格式验证通过"


def get_secret_token(secret_id, secret_key, timeout=10):
    """
    获取 secret_token
    
    接口: POST https://auth.kdlapi.com/api/get_secret_token
    参数: secret_id, secret_key
    
    Returns:
        dict: {"success": bool, "secret_token": str, "expire_time": str}
    """
    try:
        data = {
            "secret_id": secret_id,
            "secret_key": secret_key
        }
        
        response = requests.post(
            TOKEN_API_URL,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=timeout
        )
        
        result = response.json()
        
        if result.get("code") != 0:
            return {
                "success": False,
                "error": f"API错误: {result.get('msg', '未知错误')}"
            }
        
        token_data = result.get("data", {})
        
        return {
            "success": True,
            "secret_token": token_data.get("secret_token", ""),
            "expire_time": token_data.get("expire_time", "")
        }
        
    except requests.exceptions.Timeout:
        return {"success": False, "error": "请求超时，请检查网络"}
    
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"网络错误: {str(e)}"}
    
    except json.JSONDecodeError:
        return {"success": False, "error": "API返回数据格式异常"}


def mask_secret(secret):
    """脱敏密钥"""
    if not secret or len(secret) < 8:
        return "***"
    return secret[:4] + "***" + secret[-4:]


def set_config(secret_id, secret_key, test_url=None, timeout=None):
    """
    设置配置
    
    Args:
        secret_id: 快代理 SecretId
        secret_key: 快代理 SecretKey
        test_url: 测试URL（可选）
        timeout: 超时时间（可选）
    
    Returns:
        dict: {"success": bool, "message": str}
    """
    # 验证密钥格式
    valid, msg = validate_credentials(secret_id, secret_key)
    if not valid:
        return {"success": False, "error": msg}
    
    # 获取 secret_token
    print(f"[认证] 正在获取 secret_token...")
    token_result = get_secret_token(secret_id, secret_key)
    
    if not token_result["success"]:
        return {"success": False, "error": f"认证失败: {token_result['error']}"}
    
    secret_token = token_result["secret_token"]
    expire_time = token_result.get("expire_time", "")
    
    print(f"[认证] 成功获取 secret_token")
    
    # 保存配置
    config = load_config()
    config["secret_id"] = secret_id
    config["secret_key"] = secret_key
    config["secret_token"] = secret_token
    config["token_expire_time"] = expire_time
    config["configured_at"] = datetime.now().isoformat()
    
    if test_url:
        config["test_url"] = test_url
    if timeout:
        config["timeout"] = timeout
    
    save_config(config)
    
    return {
        "success": True,
        "message": "配置已保存",
        "masked_secret_id": mask_secret(secret_id),
        "masked_secret_key": mask_secret(secret_key)
    }


def refresh_token():
    """
    刷新 secret_token
    
    Returns:
        dict: {"success": bool, "secret_token": str}
    """
    config = load_config()
    
    if not config.get("secret_id") or not config.get("secret_key"):
        return {"success": False, "error": "未配置密钥，请先使用 set_config"}
    
    token_result = get_secret_token(config["secret_id"], config["secret_key"])
    
    if not token_result["success"]:
        return token_result
    
    config["secret_token"] = token_result["secret_token"]
    config["token_expire_time"] = token_result.get("expire_time", "")
    save_config(config)
    
    return {
        "success": True,
        "secret_token": token_result["secret_token"]
    }


def show_config():
    """显示配置（脱敏）"""
    config = load_config()
    
    if not config.get("secret_id"):
        return {
            "configured": False,
            "message": "请先配置API密钥（使用 set_config）"
        }
    
    return {
        "configured": True,
        "secret_id": mask_secret(config["secret_id"]),
        "secret_key": mask_secret(config["secret_key"]),
        "secret_token": mask_secret(config.get("secret_token", "")),
        "test_url": config["test_url"],
        "timeout": config["timeout"],
        "configured_at": config["configured_at"]
    }


def is_configured():
    """检查是否已配置"""
    config = load_config()
    return bool(config.get("secret_id") and config.get("secret_key"))


def get_credentials():
    """
    获取认证信息
    
    Returns:
        dict: {"secret_id": str, "signature": str} 或 {"error": str}
    """
    config = load_config()
    
    if not config.get("secret_id"):
        return {"error": "未配置密钥"}
    
    # 检查 token 是否存在
    if not config.get("secret_token"):
        # 尝试刷新 token
        refresh_result = refresh_token()
        if not refresh_result["success"]:
            return {"error": refresh_result["error"]}
        config = load_config()
    
    return {
        "secret_id": config["secret_id"],
        "signature": config["secret_token"]
    }


# 命令行入口
if __name__ == '__main__':
    import sys
    
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    if len(sys.argv) < 2:
        print("用法: config_manager.py <command> [args]")
        print("命令: set <secret_id> <secret_key> | show | check | refresh")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "set":
        if len(sys.argv) < 4:
            print("错误: 请提供 secret_id 和 secret_key")
            print("示例: config_manager.py set example_id123 example_key456")
            sys.exit(1)
        result = set_config(sys.argv[2], sys.argv[3])
        if result["success"]:
            print(f"[OK] 配置已保存")
            print(f"     SecretId: {result['masked_secret_id']}")
            print(f"     SecretKey: {result['masked_secret_key']}")
            print(f"\n[安全提示] 密钥已保存在本地，请勿在群聊中分享")
        else:
            print(f"[错误] {result['error']}")
    
    elif cmd == "show":
        result = show_config()
        if result["configured"]:
            print("[配置信息]")
            print(f"  SecretId: {result['secret_id']}")
            print(f"  SecretKey: {result['secret_key']}")
            print(f"  Token: {result['secret_token']}")
            print(f"  测试URL: {result['test_url']}")
            print(f"  超时: {result['timeout']}秒")
            print(f"  配置时间: {result['configured_at']}")
        else:
            print(f"[提示] {result['message']}")
    
    elif cmd == "check":
        if is_configured():
            print("[OK] 已配置")
        else:
            print("[提示] 未配置，请使用 set_config")
    
    elif cmd == "refresh":
        result = refresh_token()
        if result["success"]:
            print(f"[OK] Token 已刷新")
        else:
            print(f"[错误] {result['error']}")