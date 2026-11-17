from typing import Dict, List, Optional
from wechat_oa.core.config import load_config, save_config, get_account, ConfigError


def get_accounts() -> Dict[str, any]:
    """获取所有公众号列表"""
    try:
        config = load_config()
        accounts = []
        for key, account in config.get("accounts", {}).items():
            accounts.append({
                "key": key,
                "name": account.get("name", key),
                "voice_name": account.get("voice_name", []),
                "is_default": key == config.get("default_account"),
                "is_current": key == config.get("current_account")
            })
        return {"success": True, "accounts": accounts}
    except Exception as e:
        return {"success": False, "error": str(e)}


def select_account(account_name: str) -> Dict[str, any]:
    """选择当前公众号（会话级别）"""
    try:
        config = load_config()
        
        if account_name not in config.get("accounts", {}):
            return {"success": False, "error": f"公众号不存在: {account_name}"}
        
        config["current_account"] = account_name
        save_config(config)
        
        account = config["accounts"][account_name]
        return {
            "success": True,
            "message": f"已切换到公众号: {account.get('name', account_name)}",
            "account": {
                "key": account_name,
                "name": account.get("name", account_name)
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def select_account_by_voice(voice_text: str) -> Dict[str, any]:
    """根据语音指令匹配公众号"""
    try:
        config = load_config()
        voice_text_lower = voice_text.lower()
        
        for key, account in config.get("accounts", {}).items():
            for name in account.get("voice_name", []):
                if name.lower() in voice_text_lower:
                    return select_account(key)
            
            if account.get("name", "").lower() in voice_text_lower:
                return select_account(key)
        
        return {"success": False, "error": f"未找到匹配的公众号: {voice_text}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_current_account() -> Dict[str, any]:
    """获取当前选中的公众号配置"""
    try:
        account = get_account()
        config = load_config()
        current_key = config.get("current_account", config.get("default_account", "default"))
        return {
            "success": True,
            "account_key": current_key,
            "name": account.get("name", current_key),
            "author": account.get("author", ""),
            "APP_ID": account.get("APP_ID", "")[:10] + "..." if account.get("APP_ID") else ""
        }
    except ConfigError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def set_default_account(account_name: str) -> Dict[str, any]:
    """设置默认公众号"""
    try:
        config = load_config()
        
        if account_name not in config.get("accounts", {}):
            return {"success": False, "error": f"公众号不存在: {account_name}"}
        
        config["default_account"] = account_name
        if "current_account" not in config:
            config["current_account"] = account_name
        save_config(config)
        
        account = config["accounts"][account_name]
        return {
            "success": True,
            "message": f"已设置默认公众号: {account.get('name', account_name)}",
            "account": {
                "key": account_name,
                "name": account.get("name", account_name)
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
