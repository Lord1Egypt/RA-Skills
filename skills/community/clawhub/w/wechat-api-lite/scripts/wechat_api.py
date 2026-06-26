#!/usr/bin/env python3
"""
wechat-api-lite — 微信公众号 API 轻量化脚本
支持：获取 access_token、上传素材、创建草稿、发布等

环境变量（从 config.env 读取）：
  WECHAT_APP_ID
  WECHAT_APP_SECRET
"""

import os, sys, json, re, time
import urllib.request
import urllib.parse
import urllib.error

# ── Config ────────────────────────────────────────────────────────────────────

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE  = os.path.join(SKILL_DIR, "..", "config.env")

def load_env():
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

load_env()

APP_ID     = os.environ.get("WECHAT_APP_ID", "")
APP_SECRET = os.environ.get("WECHAT_APP_SECRET", "")

# ── HTTP helper ────────────────────────────────────────────────────────────────

def wechat_request(method, url, data=None, token=None):
    """Send HTTP request to WeChat API with JSON handling."""
    if data is not None:
        data = json.dumps(data, ensure_ascii=False).encode()

    params = {}
    if token:
        params["access_token"] = token

    if params:
        url += ("?" if "?" not in url else "&") + urllib.parse.urlencode(params)

    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json; charset=utf-8")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            result = json.loads(body)
        except Exception:
            result = {"errcode": -1, "errmsg": body}
    except urllib.error.URLError as e:
        result = {"errcode": -1, "errmsg": str(e)}

    return result


def get_access_token():
    """获取 access_token（有效期 7200 秒）"""
    if not APP_ID or not APP_SECRET:
        print("错误：请先在 config.env 中填入 WECHAT_APP_ID 和 WECHAT_APP_SECRET")
        sys.exit(1)

    url = f"https://api.weixin.qq.com/cgi-bin/token"
    result = wechat_request("GET", url, token=False)

    # Build URL manually
    full_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    req = urllib.request.Request(full_url, method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode())

    if "access_token" in result:
        return result["access_token"], result.get("expires_in", 7200)
    else:
        errcode = result.get("errcode", -1)
        errmsg  = result.get("errmsg", "unknown error")
        print(f"获取 access_token 失败: [{errcode}] {errmsg}")
        sys.exit(1)


# ── Token cache (simple file-based) ───────────────────────────────────────────

TOKEN_CACHE = os.path.join(SKILL_DIR, ".token_cache")

def read_cached_token():
    """读取缓存的 token"""
    if not os.path.exists(TOKEN_CACHE):
        return None
    try:
        with open(TOKEN_CACHE) as f:
            cache = json.loads(f.read())
        # 检查是否过期（提前5分钟）
        if time.time() < cache["expires_at"] - 300:
            return cache["token"]
    except Exception:
        pass
    return None

def write_cached_token(token, expires_in):
    with open(TOKEN_CACHE, "w") as f:
        json.dump({
            "token": token,
            "expires_at": time.time() + expires_in
        }, f)

def get_token():
    """获取 token（优先使用缓存）"""
    token = read_cached_token()
    if token:
        return token
    token, expires_in = get_access_token()
    write_cached_token(token, expires_in)
    return token


# ── API: 上传永久素材（图片） ────────────────────────────────────────────────

def upload_image(file_path):
    """
    上传图片永久素材。
    返回 {"media_id": "...", "url": "..."}
    """
    if not os.path.isfile(file_path):
        print(f"错误：文件不存在 {file_path}")
        sys.exit(1)

    token = get_token()
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"

    boundary = "----WechatBoundary" + str(int(time.time() * 1000))
    body_bytes = []

    filename = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        file_data = f.read()

    # Form field
    body_bytes.append(f"--{boundary}\r\n".encode())
    body_bytes.append(f'Content-Disposition: form-data; name="media"; filename="{filename}"\r\n'.encode())
    body_bytes.append("Content-Type: application/octet-stream\r\n\r\n".encode())
    body_bytes.append(file_data)
    body_bytes.append(f"\r\n--{boundary}--\r\n".encode())

    req = urllib.request.Request(url, data=b"".join(body_bytes), method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")

    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode())

    if result.get("errcode") == 0 or "media_id" in result:
        print(f"✅ 图片上传成功: media_id={result.get('media_id', 'N/A')}")
        return result
    else:
        print(f"❌ 上传失败: {result}")
        sys.exit(1)


# ── API: 上传 thumb（封面） ───────────────────────────────────────────────────

def upload_thumb(file_path):
    """
    上传封面缩略图（永久）。
    返回 media_id。
    """
    if not os.path.isfile(file_path):
        print(f"错误：文件不存在 {file_path}")
        sys.exit(1)

    token = get_token()
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=thumb"

    boundary = "----WechatBoundary" + str(int(time.time() * 1000))
    body_bytes = []

    filename = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        file_data = f.read()

    body_bytes.append(f"--{boundary}\r\n".encode())
    body_bytes.append(f'Content-Disposition: form-data; name="media"; filename="{filename}"\r\n'.encode())
    body_bytes.append("Content-Type: application/octet-stream\r\n\r\n".encode())
    body_bytes.append(file_data)
    body_bytes.append(f"\r\n--{boundary}--\r\n".encode())

    req = urllib.request.Request(url, data=b"".join(body_bytes), method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")

    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode())

    if result.get("errcode") == 0 or "media_id" in result:
        print(f"✅ 封面上传成功: media_id={result.get('media_id', 'N/A')}")
        return result
    else:
        print(f"❌ 封面上传失败: {result}")
        sys.exit(1)


# ── API: 创建草稿 ─────────────────────────────────────────────────────────────

def create_draft(articles):
    """
    创建草稿箱图文消息。
    articles: list of dict, each dict has keys:
      title, author (opt), digest (opt), content,
      content_source_url (opt), thumb_media_id,
      show_cover_pic (0/1), need_open_comment (0/1), only_fans_can_comment (0/1)
    """
    token = get_token()
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"

    payload = {"articles": articles}
    result = wechat_request("POST", url, data=payload)

    # 微信新增草稿接口成功时不返回 errcode，仅检查 media_id
    if "media_id" in result:
        media_id = result.get("media_id", "N/A")
        print(f"✅ 草稿创建成功: media_id={media_id}")
        return {"media_id": media_id}
    else:
        errcode = result.get("errcode", -1)
        errmsg  = result.get("errmsg", "unknown error")
        print(f"❌ 创建草稿失败: [{errcode}] {errmsg}")
        print(f"   完整响应: {result}")
        sys.exit(1)


# ── API: 获取草稿列表 ─────────────────────────────────────────────────────────

def get_draft_list():
    """获取草稿列表"""
    token = get_token()
    url = f"https://api.weixin.qq.com/cgi-bin/draft/count?access_token={token}"
    result = wechat_request("GET", url)

    # 微信草稿计数接口成功时直接返回 total_count，无 errcode
    if "total_count" in result:
        count = result.get("total_count", 0)
        print(f"草稿箱共有 {count} 篇草稿")
        return result
    else:
        errcode = result.get("errcode", -1)
        errmsg  = result.get("errmsg", "unknown error")
        print(f"❌ 获取草稿列表失败: [{errcode}] {errmsg}")
        sys.exit(1)


# ── CLI ───────────────────────────────────────────────────────────────────────

def usage():
    print("""
wechat-api — 微信公众号 API 工具

用法:
  python3 wechat_api.py token                        # 获取 access_token
  python3 wechat_api.py upload-image <file>          # 上传图片素材
  python3 wechat_api.py upload-thumb <file>          # 上传封面缩略图
  python3 wechat_api.py create-draft <json_file>     # 创建草稿（从 JSON 文件）
  python3 wechat_api.py draft-list                   # 查看草稿数量

示例:
  # 1. 上传封面图获取 thumb_media_id
  python3 wechat_api.py upload-thumb ~/hermes/research/Cover.png

  # 2. 创建草稿（准备好 JSON 文件）
  python3 wechat_api.py create-draft ~/hermes/research/draft.json

JSON 草稿文件格式:
  [
    {
      "title": "文章标题",
      "author": "作者名",
      "digest": "摘要（可选）",
      "content": "<p>HTML 正文内容</p>",
      "thumb_media_id": "缩略图 media_id",
      "show_cover_pic": 1,
      "need_open_comment": 1,
      "only_fans_can_comment": 0
    }
  ]
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "token":
        token, exp = get_access_token()
        print(f"access_token: {token}")
        print(f"expires_in:   {exp}s")

    elif cmd == "upload-image":
        if len(sys.argv) < 3:
            print("错误：缺少文件路径"); sys.exit(1)
        result = upload_image(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False))

    elif cmd == "upload-thumb":
        if len(sys.argv) < 3:
            print("错误：缺少文件路径"); sys.exit(1)
        result = upload_thumb(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False))

    elif cmd == "create-draft":
        if len(sys.argv) < 3:
            print("错误：缺少 JSON 文件路径"); sys.exit(1)
        with open(sys.argv[2], encoding="utf-8") as f:
            articles = json.load(f)
        result = create_draft(articles)
        print(json.dumps(result, ensure_ascii=False))

    elif cmd == "draft-list":
        result = get_draft_list()
        print(json.dumps(result, ensure_ascii=False))

    else:
        print(f"未知命令: {cmd}")
        usage()
        sys.exit(1)
