#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
友盟配置管理模块
支持从 umeng-config.json 配置文件或环境变量读取认证信息
"""

import os
import json
from pathlib import Path


def find_config_file():
    """
    查找 umeng-config.json 配置文件
    
    搜索顺序：
    1. 当前工作目录
    2. 用户主目录
    3. 技能目录
    
    Returns:
        str: 配置文件路径，如果不存在则返回 None
    """
    # 可能的配置文件路径
    config_paths = [
        Path.cwd() / 'umeng-config.json',
        Path.home() / 'umeng-config.json',
        Path(__file__).parent.parent / 'umeng-config.json',
    ]
    
    for config_path in config_paths:
        if config_path.exists():
            return str(config_path)
    
    return None


def load_config(config_path=None):
    """
    加载友盟配置文件
    
    Args:
        config_path (str, optional): 配置文件路径，如果为 None 则自动查找
        
    Returns:
        dict: 配置信息，包含 apiKey 和 apiSecurity
        None: 如果配置文件不存在
        
    Raises:
        json.JSONDecodeError: JSON 格式错误
        PermissionError: 文件无权限读取
    """
    if config_path is None:
        config_path = find_config_file()
    
    if config_path is None:
        return None
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 支持多种字段名
        api_key = config.get('apiKey') or config.get('api_key') or config.get('UMENG_API_KEY')
        api_security = config.get('apiSecurity') or config.get('api_security') or config.get('UMENG_API_SECURITY')
        
        return {
            'apiKey': api_key,
            'apiSecurity': api_security,
            'configPath': config_path
        }
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in config file {config_path}: {e.msg}", e.doc, e.pos)
    except Exception as e:
        raise Exception(f"Failed to load config from {config_path}: {str(e)}")


def get_umeng_credentials(api_key=None, api_security=None):
    """
    获取友盟认证信息
    
    优先级顺序：
    1. 直接传入的参数（最高优先级）
    2. umeng-config.json 配置文件
    3. 环境变量（UMENG_API_KEY, UMENG_API_SECURITY）
    
    Args:
        api_key (str, optional): 直接传入的 API Key
        api_security (str, optional): 直接传入的 API Security
        
    Returns:
        dict: 包含 apiKey 和 apiSecurity 的字典
        
    Raises:
        ValueError: 如果所有来源都未找到认证信息
    """
    # 1. 优先使用直接传入的参数
    if api_key and api_security:
        return {
            'apiKey': api_key,
            'apiSecurity': api_security,
            'source': 'parameters'
        }
    
    # 2. 尝试从配置文件读取
    try:
        config = load_config()
        if config and config.get('apiKey') and config.get('apiSecurity'):
            return {
                'apiKey': config['apiKey'],
                'apiSecurity': config['apiSecurity'],
                'source': 'config',
                'configPath': config.get('configPath')
            }
    except Exception:
        # 配置文件读取失败，继续尝试环境变量
        pass
    
    # 3. 尝试从环境变量读取
    env_api_key = os.getenv("UMENG_API_KEY")
    env_api_security = os.getenv("UMENG_API_SECURITY")
    
    if env_api_key and env_api_security:
        return {
            'apiKey': env_api_key,
            'apiSecurity': env_api_security,
            'source': 'environment'
        }
    
    # 所有来源都未找到
    raise ValueError(
        "友盟认证信息未找到。请通过以下方式之一配置：\n"
        "1. 创建 umeng-config.json 文件，包含 apiKey 和 apiSecurity 字段\n"
        "2. 设置环境变量 UMENG_API_KEY 和 UMENG_API_SECURITY\n"
        "3. 在调用时直接传入 apiKey 和 apiSecurity 参数"
    )


def save_config(api_key, api_security, config_path=None):
    """
    保存友盟配置到文件
    
    Args:
        api_key (str): API Key
        api_security (str): API Security
        config_path (str, optional): 配置文件路径，默认为用户主目录
        
    Returns:
        str: 保存的配置文件路径
    """
    if config_path is None:
        config_path = Path.home() / 'umeng-config.json'
    else:
        config_path = Path(config_path)
    
    config = {
        'apiKey': api_key,
        'apiSecurity': api_security,
        'note': '友盟 API 配置文件 - 请妥善保管，不要提交到版本控制系统'
    }
    
    # 确保目录存在
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    # 设置文件权限（仅所有者可读写）
    try:
        os.chmod(config_path, 0o600)
    except Exception:
        pass  # 在某些系统上可能不支持 chmod
    
    return str(config_path)


# 使用示例
if __name__ == "__main__":
    # 示例：获取认证信息
    try:
        creds = get_umeng_credentials()
        print(f"认证信息来源：{creds['source']}")
        print(f"API Key: {creds['apiKey'][:10]}...")
        print(f"API Security: {creds['apiSecurity'][:10]}...")
    except ValueError as e:
        print(f"Error: {e}")
    
    # 示例：保存配置
    # config_path = save_config("your_api_key", "your_api_security")
    # print(f"配置已保存到：{config_path}")
