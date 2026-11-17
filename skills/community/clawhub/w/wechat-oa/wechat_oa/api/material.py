from typing import Dict
from .router import hybrid_route
from .direct import _get, _post, _post_file, API_URL_BASE, WeChatAPIError
from .relay import relay_upload, relay_post


def _get_token_manager():
    from wechat_oa.core.config import load_config
    from wechat_oa.core.token import TokenManager
    cfg = load_config()
    return TokenManager(cfg["APP_ID"], cfg["APP_SECRET"])


def _material_upload_direct(file_path: str, media_type: str = "image") -> Dict:
    token_manager = _get_token_manager()
    post_file = _post_file(token_manager)
    
    url = f"{API_URL_BASE}/material/add_material?type={media_type}"
    
    result = post_file(url, file_path)
    
    return {"success": True, "media_id": result.get("media_id"), "message": "素材上传成功"}


def _material_upload_relay(file_path: str, media_type: str = "image") -> Dict:
    from wechat_oa.core.config import load_config
    cfg = load_config()
    
    result = relay_upload(f"wechat/upload?appid={cfg['APP_ID']}&secret={cfg['APP_SECRET']}&type={media_type}", file_path, cfg)
    
    if result.get("success") or result.get("errcode") == 0:
        return {"success": True, "media_id": result.get("media_id", result.get("url")), "message": "素材上传成功"}
    return {"success": False, "error": result.get("errmsg", str(result))}


@hybrid_route(_material_upload_direct, _material_upload_relay)
def material_upload(file_path: str, media_type: str = "image") -> Dict:
    pass


def _material_count_direct() -> Dict:
    token_manager = _get_token_manager()
    get = _get(token_manager)
    
    url = f"{API_URL_BASE}/material/get_materialcount"
    result = get(url)
    
    return {"success": True, "data": result}


def _material_count_relay() -> Dict:
    from wechat_oa.core.config import load_config
    from .relay import relay_get
    cfg = load_config()
    
    params = {
        "appid": cfg["APP_ID"],
        "appsecret": cfg["APP_SECRET"],
    }
    
    result = relay_get("material/count", params, cfg)
    
    if result.get("success") or result.get("errcode") == 0:
        return {"success": True, "data": result}
    return {"success": False, "error": result.get("errmsg", str(result))}


@hybrid_route(_material_count_direct, _material_count_relay)
def material_count() -> Dict:
    pass


def _material_list_direct(media_type: str = "news", offset: int = 0, count: int = 20) -> Dict:
    token_manager = _get_token_manager()
    post = _post(token_manager)
    
    json_data = {"type": media_type, "offset": offset, "count": count}
    
    url = f"{API_URL_BASE}/material/batchget_material"
    result = post(url, json_data)
    
    return {"success": True, "data": result}


def _material_list_relay(media_type: str = "news", offset: int = 0, count: int = 20) -> Dict:
    from wechat_oa.core.config import load_config
    cfg = load_config()
    
    json_data = {
        "appid": cfg["APP_ID"],
        "secret": cfg["APP_SECRET"],
        "action": "material_list",
        "data": {"type": media_type, "offset": offset, "count": count}
    }
    
    result = relay_post("wechat/material", json_data, cfg)
    
    if result.get("success") or result.get("errcode") == 0:
        return {"success": True, "data": result}
    return {"success": False, "error": result.get("errmsg", str(result))}


@hybrid_route(_material_list_direct, _material_list_relay)
def material_list(media_type: str = "news", offset: int = 0, count: int = 20) -> Dict:
    pass


def _material_delete_direct(media_id: str) -> Dict:
    token_manager = _get_token_manager()
    get = _get(token_manager)
    
    params = {"media_id": media_id}
    
    url = f"{API_URL_BASE}/material/del_material"
    get(url, params)
    
    return {"success": True, "message": "素材删除成功"}


def _material_delete_relay(media_id: str) -> Dict:
    from wechat_oa.core.config import load_config
    cfg = load_config()
    
    json_data = {
        "appid": cfg["APP_ID"],
        "secret": cfg["APP_SECRET"],
        "action": "material_delete",
        "data": {"media_id": media_id}
    }
    
    result = relay_post("wechat/material", json_data, cfg)
    
    if result.get("success") or result.get("errcode") == 0:
        return {"success": True, "message": "素材删除成功"}
    return {"success": False, "error": result.get("errmsg", str(result))}


@hybrid_route(_material_delete_direct, _material_delete_relay)
def material_delete(media_id: str) -> Dict:
    pass
