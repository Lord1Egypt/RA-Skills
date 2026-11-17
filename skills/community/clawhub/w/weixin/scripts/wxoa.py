#!/usr/bin/env python3
"""微信公众号 API 命令行工具（零依赖，仅标准库）。

环境变量:
    WX_APPID   公众号/小程序 AppID
    WX_SECRET  AppSecret

子命令:
    token                                   获取 access_token（本地缓存，7000秒过期）
    call <path> [json_body]                 通用调用：无 body 为 GET，有 body 为 POST
    upload-image <file>                     上传图文内图片（uploadimg，不占素材库）
    upload-thumb <file>                     上传永久图片素材（返回 media_id 可作封面）
    draft-add <title> <content_file> <thumb_media_id> [author] [digest]
    drafts [offset] [count]                 列出草稿箱
    publish <media_id>                      发布草稿
    published [offset] [count]              列出已发表记录

示例:
    export WX_APPID=wx123... WX_SECRET=abc...
    python3 wxoa.py token
    python3 wxoa.py call /cgi-bin/get_api_domain_ip
    python3 wxoa.py upload-thumb cover.jpg
    python3 wxoa.py draft-add "标题" article.html MEDIA_ID
"""
import json
import mimetypes
import os
import sys
import tempfile
import time
import urllib.parse
import urllib.request

API = "https://api.weixin.qq.com"
CACHE = os.path.join(tempfile.gettempdir(), "wxoa_token_%s.json")


def die(msg: str, code: int = 1) -> None:
    print(f"错误: {msg}", file=sys.stderr)
    sys.exit(code)


def http(url: str, data: bytes = None, headers: dict = None) -> dict:
    req = urllib.request.Request(url, data=data, headers=headers or {})
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read()
    try:
        return json.loads(body)
    except ValueError:
        return {"raw": body.decode("utf-8", "replace")}


def get_token() -> str:
    appid = os.environ.get("WX_APPID") or die("未设置 WX_APPID")
    secret = os.environ.get("WX_SECRET") or die("未设置 WX_SECRET")
    cache_file = CACHE % appid
    try:
        c = json.load(open(cache_file))
        if c["expire_at"] > time.time():
            return c["token"]
    except Exception:
        pass
    q = urllib.parse.urlencode(
        {"grant_type": "client_credential", "appid": appid, "secret": secret})
    r = http(f"{API}/cgi-bin/token?{q}")
    if "access_token" not in r:
        die(f"取 token 失败: {r} (40164=IP不在白名单, 40125=secret错误)")
    json.dump({"token": r["access_token"],
               "expire_at": time.time() + 7000}, open(cache_file, "w"))
    return r["access_token"]


def api(path: str, body: dict = None) -> dict:
    sep = "&" if "?" in path else "?"
    url = f"{API}{path}{sep}access_token={get_token()}"
    if body is None:
        return http(url)
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    return http(url, data, {"Content-Type": "application/json"})


def upload(path: str, filepath: str, field: str = "media") -> dict:
    if not os.path.isfile(filepath):
        die(f"文件不存在: {filepath}")
    boundary = "----wxoaboundary%d" % int(time.time())
    fname = os.path.basename(filepath)
    ctype = mimetypes.guess_type(fname)[0] or "application/octet-stream"
    raw = open(filepath, "rb").read()
    parts = (
        f"--{boundary}\r\nContent-Disposition: form-data; "
        f'name="{field}"; filename="{fname}"\r\n'
        f"Content-Type: {ctype}\r\n\r\n"
    ).encode() + raw + f"\r\n--{boundary}--\r\n".encode()
    sep = "&" if "?" in path else "?"
    url = f"{API}{path}{sep}access_token={get_token()}"
    return http(url, parts,
                {"Content-Type": f"multipart/form-data; boundary={boundary}"})


def out(r: dict) -> None:
    print(json.dumps(r, ensure_ascii=False, indent=1))
    if isinstance(r, dict) and r.get("errcode") not in (None, 0):
        sys.exit(2)


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    cmd, rest = args[0], args[1:]

    if cmd == "token":
        print(get_token())
    elif cmd == "call":
        if not rest:
            die("用法: call <path> [json_body]")
        body = json.loads(rest[1]) if len(rest) > 1 else None
        out(api(rest[0], body))
    elif cmd == "upload-image":
        out(upload("/cgi-bin/media/uploadimg", rest[0]))
    elif cmd == "upload-thumb":
        out(upload("/cgi-bin/material/add_material?type=image", rest[0]))
    elif cmd == "draft-add":
        if len(rest) < 3:
            die("用法: draft-add <title> <content_file> <thumb_media_id> [author] [digest]")
        title, content_file, thumb = rest[0], rest[1], rest[2]
        article = {
            "title": title,
            "content": open(content_file, encoding="utf-8").read(),
            "thumb_media_id": thumb,
            "need_open_comment": 1,
        }
        if len(rest) > 3:
            article["author"] = rest[3]
        if len(rest) > 4:
            article["digest"] = rest[4]
        out(api("/cgi-bin/draft/add", {"articles": [article]}))
    elif cmd == "drafts":
        offset = int(rest[0]) if rest else 0
        count = int(rest[1]) if len(rest) > 1 else 20
        out(api("/cgi-bin/draft/batchget",
                {"offset": offset, "count": count, "no_content": 1}))
    elif cmd == "publish":
        if not rest:
            die("用法: publish <media_id>")
        out(api("/cgi-bin/freepublish/submit", {"media_id": rest[0]}))
    elif cmd == "published":
        offset = int(rest[0]) if rest else 0
        count = int(rest[1]) if len(rest) > 1 else 20
        out(api("/cgi-bin/freepublish/batchget",
                {"offset": offset, "count": count, "no_content": 1}))
    else:
        die(f"未知子命令: {cmd}（运行不带参数查看帮助）")


if __name__ == "__main__":
    main()
