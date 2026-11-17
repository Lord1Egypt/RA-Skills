import requests
import json
import re
from typing import Dict, Optional


def get_api_prefix(env: str = "") -> str:
    if env == "dev":
        return "/testapi"
    return "/api"


def _fix_garbled(obj):
    if isinstance(obj, str):
        result = obj
        try:
            result = result.encode('latin-1').decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
        result = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), result)
        return result
    elif isinstance(obj, dict):
        return {k: _fix_garbled(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_fix_garbled(item) for item in obj]
    else:
        return obj


def relay_post(path: str, json_data: Dict, config: Dict) -> Dict:
    server_url = config.get("WECHAT_OA_SERVER", "http://120.79.2.44")
    key = config.get("WECHAT_OA_SERVER_KEY", "")
    api_prefix = get_api_prefix(config.get("ENV", ""))
    
    url = f"{server_url.rstrip('/')}{api_prefix}/{path}"
    
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-API-Key": key,
    }
    
    data = json.dumps(json_data, ensure_ascii=False).encode("utf-8")
    resp = requests.post(url, data=data, headers=headers, timeout=30)
    
    try:
        return _fix_garbled(resp.json())
    except json.JSONDecodeError:
        return {"success": False, "error": f"服务器返回非 JSON 数据: {resp.text[:200]}"}


def relay_get(path: str, params: Dict, config: Dict) -> Dict:
    server_url = config.get("WECHAT_OA_SERVER", "http://120.79.2.44")
    key = config.get("WECHAT_OA_SERVER_KEY", "")
    api_prefix = get_api_prefix(config.get("ENV", ""))
    
    url = f"{server_url.rstrip('/')}{api_prefix}/{path}"
    
    headers = {"X-API-Key": key}
    
    resp = requests.get(url, params=params, headers=headers, timeout=30)
    
    try:
        return _fix_garbled(resp.json())
    except json.JSONDecodeError:
        return {"success": False, "error": f"服务器返回非 JSON 数据: {resp.text[:200]}"}


def relay_upload(path: str, file_path: str, config: Dict) -> Dict:
    server_url = config.get("WECHAT_OA_SERVER", "http://120.79.2.44")
    key = config.get("WECHAT_OA_SERVER_KEY", "")
    api_prefix = get_api_prefix(config.get("ENV", ""))
    
    url = f"{server_url.rstrip('/')}{api_prefix}/{path}"
    
    headers = {"X-API-Key": key}
    
    with open(file_path, "rb") as f:
        files = {"file": (file_path.split("/")[-1], f)}
        resp = requests.post(url, files=files, headers=headers, timeout=60)
    
    try:
        return _fix_garbled(resp.json())
    except json.JSONDecodeError:
        return {"success": False, "error": f"服务器返回非 JSON 数据: {resp.text[:200]}"}


def relay_put(path: str, json_data: Dict, config: Dict) -> Dict:
    server_url = config.get("WECHAT_OA_SERVER", "http://120.79.2.44")
    key = config.get("WECHAT_OA_SERVER_KEY", "")
    api_prefix = get_api_prefix(config.get("ENV", ""))
    
    url = f"{server_url.rstrip('/')}{api_prefix}/{path}"
    
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-API-Key": key,
    }
    
    data = json.dumps(json_data, ensure_ascii=False).encode("utf-8")
    resp = requests.put(url, data=data, headers=headers, timeout=30)
    
    try:
        return _fix_garbled(resp.json())
    except json.JSONDecodeError:
        return {"success": False, "error": f"服务器返回非 JSON 数据: {resp.text[:200]}"}


def relay_delete(path: str, params: Dict, config: Dict) -> Dict:
    server_url = config.get("WECHAT_OA_SERVER", "http://120.79.2.44")
    key = config.get("WECHAT_OA_SERVER_KEY", "")
    api_prefix = get_api_prefix(config.get("ENV", ""))
    
    url = f"{server_url.rstrip('/')}{api_prefix}/{path}"
    
    headers = {"X-API-Key": key}
    
    resp = requests.delete(url, params=params, headers=headers, timeout=15)
    
    try:
        return _fix_garbled(resp.json())
    except json.JSONDecodeError:
        return {"success": False, "error": f"服务器返回非 JSON 数据: {resp.text[:200]}"}
