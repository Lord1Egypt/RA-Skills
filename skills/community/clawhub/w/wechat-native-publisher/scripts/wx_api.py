# -*- coding: utf-8 -*-
"""
wechat-native-publisher 微信 API 封装
提供: 获取 access_token / 上传封面(thumb) / 上传正文插图(uploadimg) / 新增草稿 / 查询草稿

安全约定：
- 本文件【绝不】内置凭据。config.json 通过环境变量 WECHAT_PUSH_CONFIG 或当前工作目录读取。
- skill 目录本身不放任何 config.json / 凭据，防止 skill 被分享/同步时泄漏账号。
"""
import requests, json, os

API_BASE = "https://api.weixin.qq.com/cgi-bin"


def _config_path():
    """优先环境变量 -> 当前工作目录 config.json -> 本文件同目录 config.json（仅兼容）"""
    env = os.environ.get("WECHAT_PUSH_CONFIG")
    if env and os.path.exists(env):
        return env
    local = os.path.join(os.getcwd(), "config.json")
    if os.path.exists(local):
        return local
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")


def load_config(config_path=None):
    path = config_path or _config_path()
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _gen_headers():
    return {"Content-Type": "application/json; charset=utf-8"}


def get_access_token(config_path=None):
    cfg = load_config(config_path)
    url = API_BASE + "/token"
    params = {
        "grant_type": "client_credential",
        "appid": cfg["appid"],
        "secret": cfg["appsecret"],
    }
    r = requests.get(url, params=params, timeout=15)
    data = r.json()
    if "access_token" not in data:
        raise RuntimeError("获取 access_token 失败: %s" % json.dumps(data, ensure_ascii=False))
    return data["access_token"]


def upload_thumb(token, image_path_or_url, media_type="thumb"):
    """上传封面图到永久素材库, 返回 media_id。media_type: image/thumb(图文封面)"""
    url = API_BASE + "/material/add_material"
    params = {"access_token": token, "type": media_type}
    with open(image_path_or_url, "rb") as f:
        files = {"media": (os.path.basename(image_path_or_url), f, "image/jpeg")}
        r = requests.post(url, params=params, files=files, timeout=60)
    res = r.json()
    if "media_id" not in res:
        raise RuntimeError("上传封面失败: %s" % json.dumps(res, ensure_ascii=False))
    return res["media_id"]


def upload_img(token, image_path):
    """上传正文插图（media/uploadimg）, 返回可直接塞进正文 <img src> 的 URL"""
    url = API_BASE + "/media/uploadimg"
    params = {"access_token": token}
    with open(image_path, "rb") as f:
        files = {"media": (os.path.basename(image_path), f, "image/jpeg")}
        r = requests.post(url, params=params, files=files, timeout=60)
    res = r.json()
    if "url" not in res:
        raise RuntimeError("上传正文插图失败: %s" % json.dumps(res, ensure_ascii=False))
    return res["url"]


def add_draft(token, article):
    """新增草稿。article: dict, 含 title/author/digest/content/thumb_media_id/content_source_url 等"""
    url = API_BASE + "/draft/add"
    params = {"access_token": token}
    payload = {"articles": [article]}
    r = requests.post(url, params=params,
                      data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                      headers=_gen_headers(), timeout=30)
    res = r.json()
    if res.get("errcode", 0) != 0:
        raise RuntimeError("新增草稿失败: %s" % json.dumps(res, ensure_ascii=False))
    return res["media_id"]


def get_draft_count(token):
    url = API_BASE + "/draft/count"
    params = {"access_token": token}
    r = requests.get(url, params=params, timeout=15)
    return r.json()


if __name__ == "__main__":
    try:
        token = get_access_token()
        print("[OK] access_token:", token[:24] + "...")
        cnt = get_draft_count(token)
        print("[INFO] 草稿箱数量:", json.dumps(cnt, ensure_ascii=False))
    except Exception as e:
        print("[FAIL]", e)
