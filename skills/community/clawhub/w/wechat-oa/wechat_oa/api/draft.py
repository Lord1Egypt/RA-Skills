from typing import Dict, Optional
from .router import hybrid_route
from .direct import _get, _post, API_URL_BASE, WeChatAPIError


def _get_token_manager(account_name: Optional[str] = None):
    from wechat_oa.core.config import get_account
    cfg = get_account(account_name)
    from wechat_oa.core.token import TokenManager
    return TokenManager(cfg["APP_ID"], cfg["APP_SECRET"])


def _draft_create_direct(title: str, content: str, author: str = "", digest: str = "", thumb_media_id: str = "", account_name: Optional[str] = None) -> Dict:
    token_manager = _get_token_manager(account_name)
    post = _post(token_manager)
    
    json_data = {
        "articles": [{
            "title": title,
            "author": author,
            "digest": digest,
            "content": content,
            "thumb_media_id": thumb_media_id,
            "show_cover_pic": 1 if thumb_media_id else 0,
            "content_source_url": ""
        }]
    }
    
    url = f"{API_URL_BASE}/draft/add"
    result = post(url, json_data)
    
    return {"success": True, "media_id": result.get("media_id"), "message": "草稿创建成功"}


def _draft_create_relay(title: str, content: str, author: str = "", digest: str = "", thumb_media_id: str = "", account_name: Optional[str] = None) -> Dict:
    import base64
    import os
    from wechat_oa.core.config import get_account
    from wechat_oa.features.cover_generator import generate_cover
    cfg = get_account(account_name)
    
    json_data = {
        "appid": cfg["APP_ID"],
        "appsecret": cfg["APP_SECRET"],
        "title": title,
        "content": content,
        "author": author or cfg.get("author", ""),
        "digest": digest,
    }
    
    if thumb_media_id:
        json_data["thumb_media_id"] = thumb_media_id
    else:
        cover_path = generate_cover(title)
        if os.path.exists(cover_path):
            with open(cover_path, 'rb') as f:
                img_data = f.read()
            json_data["thumb_image"] = base64.b64encode(img_data).decode('utf-8')
            json_data["thumb_filename"] = os.path.basename(cover_path)
    
    from .relay import relay_post
    result = relay_post("push/article", json_data, cfg)
    
    if result.get("errcode") == 0 or result.get("success") is True or result.get("media_id"):
        return {"success": True, "media_id": result.get("media_id"), "message": "草稿创建成功"}
    if result.get("success") is False:
        return {"success": False, "error": result.get("error", str(result))}
    return {"success": False, "error": result.get("errmsg", str(result))}


@hybrid_route(_draft_create_direct, _draft_create_relay)
def draft_create(title: str, content: str, author: str = "", digest: str = "", thumb_media_id: str = "", account_name: Optional[str] = None) -> Dict:
    pass


def _draft_update_direct(media_id: str, title: str, content: str, author: str = "", digest: str = "", thumb_media_id: str = "", account_name: Optional[str] = None) -> Dict:
    token_manager = _get_token_manager(account_name)
    post = _post(token_manager)
    
    json_data = {
        "media_id": media_id,
        "index": 0,
        "articles": [{
            "title": title,
            "author": author,
            "digest": digest,
            "content": content,
            "thumb_media_id": thumb_media_id,
            "show_cover_pic": 1 if thumb_media_id else 0,
            "content_source_url": ""
        }]
    }
    
    url = f"{API_URL_BASE}/draft/update"
    post(url, json_data)
    
    return {"success": True, "message": "草稿更新成功"}


def _draft_update_relay(media_id: str, title: str, content: str, author: str = "", digest: str = "", thumb_media_id: str = "", account_name: Optional[str] = None) -> Dict:
    import base64
    import os
    from wechat_oa.core.config import get_account
    from wechat_oa.features.cover_generator import generate_cover
    from .relay import relay_put
    cfg = get_account(account_name)
    
    json_data = {
        "appid": cfg["APP_ID"],
        "appsecret": cfg["APP_SECRET"],
        "title": title,
        "author": author,
        "digest": digest,
        "content": content,
    }
    
    if thumb_media_id:
        json_data["thumb_media_id"] = thumb_media_id
    else:
        cover_path = generate_cover(title)
        if os.path.exists(cover_path):
            with open(cover_path, 'rb') as f:
                img_data = f.read()
            json_data["thumb_image"] = base64.b64encode(img_data).decode('utf-8')
    
    result = relay_put(f"push/article/{media_id}", json_data, cfg)
    
    if result.get("errcode") == 0 or result.get("success") is True:
        return {"success": True, "message": "草稿更新成功"}
    if result.get("success") is False:
        return {"success": False, "error": result.get("error", str(result))}
    return {"success": False, "error": result.get("errmsg", str(result))}


@hybrid_route(_draft_update_direct, _draft_update_relay)
def draft_update(media_id: str, title: str, content: str, author: str = "", digest: str = "", thumb_media_id: str = "", account_name: Optional[str] = None) -> Dict:
    pass


def _draft_list_direct(offset: int = 0, count: int = 20, account_name: Optional[str] = None) -> Dict:
    token_manager = _get_token_manager(account_name)
    post = _post(token_manager)
    
    json_data = {"offset": offset, "count": count, "no_content": 0}
    
    url = f"{API_URL_BASE}/draft/batchget"
    result = post(url, json_data)
    
    return {"success": True, "data": result}


def _draft_list_relay(offset: int = 0, count: int = 20, account_name: Optional[str] = None) -> Dict:
    from wechat_oa.core.config import get_account
    from .relay import relay_get
    cfg = get_account(account_name)
    
    params = {
        "appid": cfg["APP_ID"],
        "appsecret": cfg["APP_SECRET"],
        "count": min(count, 20),
        "offset": offset,
    }
    
    result = relay_get("push/drafts", params, cfg)
    
    if result.get("success") or result.get("errcode") == 0:
        return {"success": True, "data": result}
    return {"success": False, "error": result.get("errmsg", str(result))}


@hybrid_route(_draft_list_direct, _draft_list_relay)
def draft_list(offset: int = 0, count: int = 20, account_name: Optional[str] = None) -> Dict:
    pass


def _draft_get_direct(media_id: str, account_name: Optional[str] = None) -> Dict:
    token_manager = _get_token_manager(account_name)
    post = _post(token_manager)
    
    json_data = {"media_id": media_id}
    
    url = f"{API_URL_BASE}/draft/get"
    result = post(url, json_data)
    
    return {"success": True, "data": result}


def _draft_get_relay(media_id: str, account_name: Optional[str] = None) -> Dict:
    from wechat_oa.core.config import get_account
    cfg = get_account(account_name)
    
    json_data = {
        "appid": cfg["APP_ID"],
        "appsecret": cfg["APP_SECRET"],
        "media_id": media_id
    }
    
    from .relay import relay_post
    result = relay_post("push/article/get", json_data, cfg)
    
    if result.get("success") or result.get("errcode") == 0 or result.get("news_item"):
        return {"success": True, "data": result}
    return {"success": False, "error": result.get("errmsg", str(result))}


@hybrid_route(_draft_get_direct, _draft_get_relay)
def draft_get(media_id: str, account_name: Optional[str] = None) -> Dict:
    pass


def _draft_delete_direct(media_id: str, account_name: Optional[str] = None) -> Dict:
    token_manager = _get_token_manager(account_name)
    post = _post(token_manager)
    
    json_data = {"media_id": media_id}
    
    url = f"{API_URL_BASE}/draft/delete"
    post(url, json_data)
    
    return {"success": True, "message": "草稿删除成功"}


def _draft_delete_relay(media_id: str, account_name: Optional[str] = None) -> Dict:
    from wechat_oa.core.config import get_account
    from .relay import relay_delete
    cfg = get_account(account_name)
    
    params = {
        "appid": cfg["APP_ID"],
        "appsecret": cfg["APP_SECRET"],
    }
    
    result = relay_delete(f"push/article/{media_id}", params, cfg)
    
    if result.get("errcode") == 0 or result.get("success") is True:
        return {"success": True, "message": "草稿删除成功"}
    if result.get("success") is False:
        return {"success": False, "error": result.get("error", str(result))}
    return {"success": False, "error": result.get("errmsg", str(result))}


@hybrid_route(_draft_delete_direct, _draft_delete_relay)
def draft_delete(media_id: str, account_name: Optional[str] = None) -> Dict:
    pass
