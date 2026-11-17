import json
import os
import re
from pathlib import Path
from typing import Dict, Any, Optional

DEFAULT_CONFIG = {
    "default_account": "default",
    "current_account": "default",
    "accounts": {
        "default": {
            "name": "默认公众号",
            "voice_name": ["默认", "主号", "第一个"],
            "APP_ID": "",
            "APP_SECRET": "",
            "author": ""
        }
    },
    "PUSH_MODE": "direct",
    "WECHAT_OA_SERVER": "http://120.79.2.44",
    "WECHAT_OA_SERVER_KEY": "",
    "ENV": "prod"
}

_CONFIG_CACHE: Optional[Dict[str, Any]] = None


def _remove_json_comments(json_str: str) -> str:
    lines = json_str.split('\n')
    cleaned_lines = []
    for line in lines:
        in_string = False
        escape = False
        comment_start = -1
        for i, char in enumerate(line):
            if escape:
                escape = False
                continue
            if char == '\\' and in_string:
                escape = True
                continue
            if char == '"':
                in_string = not in_string
                continue
            if not in_string and char == '/' and i + 1 < len(line) and line[i+1] == '/':
                comment_start = i
                break
        if comment_start != -1:
            line = line[:comment_start]
        if line.strip():
            cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)


def _is_new_format(config: Dict[str, Any]) -> bool:
    return "accounts" in config and isinstance(config.get("accounts"), dict)


def _migrate_old_format(old_config: Dict[str, Any]) -> Dict[str, Any]:
    new_config = DEFAULT_CONFIG.copy()
    new_config["accounts"] = {
        "default": {
            "name": old_config.get("author", "默认公众号"),
            "voice_name": ["默认", "主号", "第一个"],
            "APP_ID": old_config.get("APP_ID", ""),
            "APP_SECRET": old_config.get("APP_SECRET", ""),
            "author": old_config.get("author", "")
        }
    }
    new_config["PUSH_MODE"] = old_config.get("PUSH_MODE", "direct")
    new_config["WECHAT_OA_SERVER"] = old_config.get("WECHAT_OA_SERVER", "http://120.79.2.44")
    new_config["WECHAT_OA_SERVER_KEY"] = old_config.get("WECHAT_OA_SERVER_KEY", "")
    new_config["ENV"] = old_config.get("ENV", "prod")
    return new_config


def load_config(config_path: str = "") -> Dict[str, Any]:
    global _CONFIG_CACHE
    
    if _CONFIG_CACHE is not None:
        return _CONFIG_CACHE
    
    if config_path:
        config_file = Path(config_path)
    else:
        config_file = Path(__file__).parent.parent.parent / "config.json"
    
    config = DEFAULT_CONFIG.copy()
    
    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                raw_content = f.read()
            content_without_comments = _remove_json_comments(raw_content)
            user_config = json.loads(content_without_comments)
            
            if _is_new_format(user_config):
                config.update(user_config)
                if "accounts" in user_config:
                    config["accounts"] = user_config["accounts"]
            else:
                config = _migrate_old_format(user_config)
        except Exception as e:
            raise ConfigError(f"加载配置文件失败: {e}")
    
    env_config = {k: v for k, v in os.environ.items() if k.startswith("WECHAT_OA_")}
    for key, value in env_config.items():
        config_key = key.replace("WECHAT_OA_", "")
        if config_key in config:
            config[config_key] = value
    
    _CONFIG_CACHE = config
    return config


def _parse_comments(json_str: str) -> Dict[str, str]:
    lines = json_str.split('\n')
    comments = {}
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('//'):
            continue
        
        in_string = False
        escape = False
        colon_pos = -1
        comment_pos = -1
        
        for i, char in enumerate(line):
            if escape:
                escape = False
                continue
            if char == '\\' and in_string:
                escape = True
                continue
            if char == '"':
                in_string = not in_string
                continue
            if not in_string and char == ':' and colon_pos == -1:
                colon_pos = i
            if not in_string and char == '/' and i + 1 < len(line) and line[i+1] == '/':
                comment_pos = i
                break
        
        if colon_pos != -1 and comment_pos != -1:
            key_part = line[:colon_pos].strip()
            if key_part.startswith('"') and key_part.endswith('"'):
                key = key_part[1:-1]
                comments[key] = line[comment_pos:]
    return comments


def save_config(config: Dict[str, Any]) -> None:
    config_file = Path(__file__).parent.parent.parent / "config.json"
    try:
        key_comments = {}
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                original_content = f.read()
            key_comments = _parse_comments(original_content)
        
        new_json_str = json.dumps(config, ensure_ascii=False, indent=4)
        
        if key_comments:
            lines = new_json_str.split('\n')
            result_lines = []
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    result_lines.append(line)
                    continue
                
                in_string = False
                escape = False
                colon_pos = -1
                
                for i, char in enumerate(line):
                    if escape:
                        escape = False
                        continue
                    if char == '\\' and in_string:
                        escape = True
                        continue
                    if char == '"':
                        in_string = not in_string
                        continue
                    if not in_string and char == ':' and colon_pos == -1:
                        colon_pos = i
                
                if colon_pos != -1:
                    key_part = line[:colon_pos].strip()
                    if key_part.startswith('"') and key_part.endswith('"'):
                        key = key_part[1:-1]
                        if key in key_comments:
                            result_lines.append(line.rstrip() + ' ' + key_comments[key])
                            continue
                
                result_lines.append(line)
            
            new_json_str = '\n'.join(result_lines)
        
        with open(config_file, "w", encoding="utf-8") as f:
            f.write(new_json_str + '\n')
        
        global _CONFIG_CACHE
        _CONFIG_CACHE = config
    except Exception as e:
        raise ConfigError(f"保存配置文件失败: {e}")


def get_account(account_name: Optional[str] = None) -> Dict[str, Any]:
    config = load_config()
    
    if account_name is None:
        account_name = config.get("current_account", config.get("default_account", "default"))
    
    accounts = config.get("accounts", {})
    
    if account_name in accounts:
        account = accounts[account_name].copy()
        account["account_key"] = account_name
        account["PUSH_MODE"] = config.get("PUSH_MODE", "direct")
        account["WECHAT_OA_SERVER"] = config.get("WECHAT_OA_SERVER", "http://120.79.2.44")
        account["WECHAT_OA_SERVER_KEY"] = config.get("WECHAT_OA_SERVER_KEY", "")
        account["ENV"] = config.get("ENV", "prod")
        if not account.get("author"):
            account["author"] = ""
        return account
    
    raise ConfigError(f"公众号不存在: {account_name}")


def validate_config(config: Dict[str, Any]) -> None:
    if not config.get("APP_ID"):
        raise ConfigError("APP_ID 不能为空")
    if not config.get("APP_SECRET"):
        raise ConfigError("APP_SECRET 不能为空")
    if config.get("PUSH_MODE") not in ("direct", "relay", "hybrid"):
        raise ConfigError(f"无效的 PUSH_MODE: {config.get('PUSH_MODE')}")


class ConfigError(Exception):
    pass
