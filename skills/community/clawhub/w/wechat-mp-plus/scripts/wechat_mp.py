#!/usr/bin/env python3
"""微信公众号核心API封装 - Token管理、素材上传、草稿管理、自动回复查询"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
import tempfile

# Token缓存文件
TOKEN_CACHE = os.path.join(tempfile.gettempdir(), "wechat_mp_token.json")

# 错误码中文映射
ERROR_MESSAGES = {
    40001: "AppSecret错误或不属于该公众号",
    40002: "无效的凭证类型",
    40013: "无效的AppID",
    40014: "无效的access_token",
    40125: "无效的AppSecret",
    41001: "缺少access_token参数",
    42001: "access_token已过期，请重新获取",
    43004: "需要关注公众号后才能操作",
    45009: "接口调用超出频率限制",
    45064: "创建菜单数量达到上限",
    48001: "该API功能未授权给此公众号",
    61451: "参数错误",
    -1: "微信系统繁忙，请稍后重试",
}


def _get_config():
    """从环境变量或配置文件获取AppID和AppSecret"""
    app_id = os.environ.get("WECHAT_MP_APP_ID", "")
    app_secret = os.environ.get("WECHAT_MP_APP_SECRET", "")
    if app_id and app_secret:
        return app_id, app_secret
    # 尝试从 .secrets/wechat_mp.env 读取
    for env_path in [
        os.path.join(os.path.expanduser("~"), "openclaw-workspace", ".secrets", "wechat_mp.env"),
        os.path.join(os.path.dirname(__file__), "..", "..", "..", ".secrets", "wechat_mp.env"),
    ]:
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k, v = k.strip(), v.strip()
                        if k == "WECHAT_MP_APP_ID":
                            app_id = v
                        elif k == "WECHAT_MP_APP_SECRET":
                            app_secret = v
            break
    if not app_id or not app_secret:
        print("❌ 错误：未配置 WECHAT_MP_APP_ID 或 WECHAT_MP_APP_SECRET", file=sys.stderr)
        print("请设置环境变量或在 .secrets/wechat_mp.env 中配置", file=sys.stderr)
        sys.exit(1)
    return app_id, app_secret


def _api_error(data):
    """检查API响应中的错误"""
    errcode = data.get("errcode", 0)
    if errcode != 0:
        msg = ERROR_MESSAGES.get(errcode, data.get("errmsg", "未知错误"))
        print(f"❌ 微信API错误 [{errcode}]: {msg}", file=sys.stderr)
        return True
    return False


def _http_get(url):
    """GET请求"""
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def _http_post_json(url, data):
    """POST JSON请求"""
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def _http_post_multipart(url, filepath, field="media"):
    """上传文件（multipart/form-data）"""
    import mimetypes
    boundary = "----WechatMPBoundary" + str(int(time.time()))
    filename = os.path.basename(filepath)
    mime = mimetypes.guess_type(filepath)[0] or "application/octet-stream"
    with open(filepath, "rb") as f:
        file_data = f.read()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="{field}"; filename="{filename}"\r\n'
        f"Content-Type: {mime}\r\n\r\n"
    ).encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": str(len(body)),
    })
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())


def get_access_token(force=False):
    """获取access_token，带缓存（2小时有效期）"""
    if not force and os.path.exists(TOKEN_CACHE):
        try:
            with open(TOKEN_CACHE) as f:
                cache = json.load(f)
            if cache.get("expires_at", 0) > time.time() + 60:
                return cache["access_token"]
        except Exception:
            pass
    app_id, app_secret = _get_config()
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    data = _http_get(url)
    if _api_error(data):
        sys.exit(1)
    token = data["access_token"]
    with open(TOKEN_CACHE, "w") as f:
        json.dump({"access_token": token, "expires_at": time.time() + data.get("expires_in", 7200)}, f)
    return token


# ============ 素材管理 ============

def upload_image(filepath):
    """上传图片素材（永久），返回 {media_id, url}"""
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
    data = _http_post_multipart(url, filepath)
    if _api_error(data):
        return None
    print(f"✅ 图片上传成功: media_id={data.get('media_id')}")
    return {"media_id": data.get("media_id"), "url": data.get("url", "")}


def upload_article_image(filepath):
    """上传文内图片（返回url，用于文章内容中引用）"""
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={token}"
    data = _http_post_multipart(url, filepath)
    if _api_error(data):
        return None
    print(f"✅ 文内图片上传成功: url={data.get('url')}")
    return data.get("url")


# ============ 草稿箱管理 ============

def create_draft(articles):
    """创建草稿。articles: list of dict，每个包含 title, author, content, thumb_media_id, digest 等"""
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    payload = {"articles": []}
    for a in articles:
        payload["articles"].append({
            "title": a.get("title", ""),
            "author": a.get("author", ""),
            "content": a.get("content", ""),
            "thumb_media_id": a.get("thumb_media_id", ""),
            "digest": a.get("digest", ""),
            "content_source_url": a.get("content_source_url", ""),
            "need_open_comment": a.get("need_open_comment", 0),
        })
    data = _http_post_json(url, payload)
    if _api_error(data):
        return None
    media_id = data.get("media_id")
    print(f"✅ 草稿创建成功: media_id={media_id}")
    return media_id


def list_drafts(offset=0, count=20):
    """列出草稿"""
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={token}"
    data = _http_post_json(url, {"offset": offset, "count": count, "no_content": 0})
    if _api_error(data):
        return None
    items = data.get("item", [])
    print(f"📋 共 {data.get('total_count', 0)} 篇草稿，当前返回 {len(items)} 篇")
    for i, item in enumerate(items):
        articles = item.get("content", {}).get("news_item", [])
        title = articles[0].get("title", "无标题") if articles else "空草稿"
        print(f"  {offset + i + 1}. {title} (media_id: {item.get('media_id', 'N/A')})")
    return data


def delete_draft(media_id):
    """删除草稿"""
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/draft/delete?access_token={token}"
    data = _http_post_json(url, {"media_id": media_id})
    if _api_error(data):
        return False
    print(f"✅ 草稿已删除: {media_id}")
    return True


# ============ 自动回复 ============

def get_autoreply_rules():
    """查询自动回复规则"""
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/get_current_autoreply_info?access_token={token}"
    data = _http_get(url)
    if "errcode" in data and data["errcode"] != 0:
        _api_error(data)
        return None
    # 关注回复
    if data.get("is_add_friend_reply_open"):
        info = data.get("add_friend_autoreply_info", {})
        print(f"👋 关注自动回复: {info.get('content', '未设置')}")
    else:
        print("👋 关注自动回复: 未开启")
    # 关键词回复
    if data.get("is_autoreply_open"):
        kw_info = data.get("keyword_autoreply_info", {})
        rules = kw_info.get("list", [])
        print(f"🔑 关键词回复规则: {len(rules)} 条")
        for r in rules[:10]:
            kws = ", ".join([k.get("content", "") for k in r.get("keyword_list_info", [])])
            print(f"  - 关键词: {kws}")
    else:
        print("🔑 关键词自动回复: 未开启")
    return data


# ============ CLI ============

def main():
    if len(sys.argv) < 2:
        print("用法: wechat_mp.py <命令> [参数]")
        print("命令: token, upload <文件>, upload-article-image <文件>,")
        print("      draft-create <json>, draft-list [offset] [count], draft-delete <media_id>,")
        print("      autoreply")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "token":
        t = get_access_token()
        print(f"access_token: {t[:20]}...{t[-10:]}")
    elif cmd == "upload":
        upload_image(sys.argv[2])
    elif cmd == "upload-article-image":
        upload_article_image(sys.argv[2])
    elif cmd == "draft-create":
        articles = json.loads(sys.argv[2])
        if isinstance(articles, dict):
            articles = [articles]
        create_draft(articles)
    elif cmd == "draft-list":
        offset = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 20
        list_drafts(offset, count)
    elif cmd == "draft-delete":
        delete_draft(sys.argv[2])
    elif cmd == "autoreply":
        get_autoreply_rules()
    else:
        print(f"未知命令: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
