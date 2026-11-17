import requests
import json
from typing import Dict, Optional

API_URL_BASE = "https://api.weixin.qq.com/cgi-bin"


def _get(token_manager):
    def _get_internal(url: str, params: Optional[Dict] = None) -> Dict:
        token = token_manager.get_token()
        req_params = {"access_token": token}
        if params:
            req_params.update(params)
        
        resp = requests.get(url, params=req_params, timeout=30)
        resp.encoding = "utf-8"
        data = resp.json()
        
        if "errcode" in data and data["errcode"] != 0:
            raise WeChatAPIError(f"API错误 {data.get('errcode')}: {data.get('errmsg')}")
        
        return data
    return _get_internal


def _post(token_manager):
    def _post_internal(url: str, json_data: Optional[Dict] = None) -> Dict:
        token = token_manager.get_token()
        url_with_token = f"{url}?access_token={token}"
        
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = json.dumps(json_data, ensure_ascii=False).encode("utf-8")
        resp = requests.post(url_with_token, data=data, headers=headers, timeout=30)
        resp.encoding = "utf-8"
        data = resp.json()
        
        if "errcode" in data and data["errcode"] != 0:
            raise WeChatAPIError(f"API错误 {data.get('errcode')}: {data.get('errmsg')}")
        
        return data
    return _post_internal


def _post_file(token_manager):
    def _post_file_internal(url: str, file_path: str, form_field: str = "media") -> Dict:
        token = token_manager.get_token()
        separator = "&" if "?" in url else "?"
        url_with_token = f"{url}{separator}access_token={token}"
        
        with open(file_path, "rb") as f:
            files = {form_field: (file_path.split("/")[-1], f)}
            resp = requests.post(url_with_token, files=files, timeout=60)
        
        data = resp.json()
        
        if "errcode" in data and data["errcode"] != 0:
            raise WeChatAPIError(f"API错误 {data.get('errcode')}: {data.get('errmsg')}")
        
        return data
    return _post_file_internal


class WeChatAPIError(Exception):
    pass
