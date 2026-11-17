from typing import Dict
from .router import hybrid_route
from .direct import _get, API_URL_BASE, WeChatAPIError
from .relay import relay_post


def _get_token_manager():
    from wechat_oa.core.config import load_config
    from wechat_oa.core.token import TokenManager
    cfg = load_config()
    return TokenManager(cfg["APP_ID"], cfg["APP_SECRET"])


def _user_info_direct(openid: str) -> Dict:
    token_manager = _get_token_manager()
    get = _get(token_manager)
    
    params = {"openid": openid, "lang": "zh_CN"}
    
    url = f"{API_URL_BASE}/user/info"
    result = get(url, params)
    
    return {"success": True, "data": result}


def _user_info_relay(openid: str) -> Dict:
    from wechat_oa.core.config import load_config
    cfg = load_config()
    
    json_data = {
        "appid": cfg["APP_ID"],
        "secret": cfg["APP_SECRET"],
        "action": "user_info",
        "data": {"openid": openid}
    }
    
    result = relay_post("wechat/user", json_data, cfg)
    
    if result.get("success") or result.get("errcode") == 0:
        return {"success": True, "data": result}
    return {"success": False, "error": result.get("errmsg", str(result))}


@hybrid_route(_user_info_direct, _user_info_relay)
def user_info(openid: str) -> Dict:
    pass
