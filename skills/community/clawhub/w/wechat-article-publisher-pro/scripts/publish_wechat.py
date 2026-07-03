#!/usr/bin/env python3
"""
微信公众号文章发布工具 — v1.0.7

纯 Python stdlib，零外部依赖。
覆盖微信官方文档全部发布相关 API。

接口文档: https://developers.weixin.qq.com/doc/subscription/api/

用法:
  python3 publish_wechat.py --help
"""

import os
import sys
import json
import time
import re
import urllib.request
import urllib.parse
import urllib.error


# ── Constants ─────────────────────────────────────────────
WECHAT_API_BASE = "https://api.weixin.qq.com/cgi-bin"
DATACUBE_BASE = "https://api.weixin.qq.com/datacube"
RATE_LIMIT_DAY = 2000
RATE_LIMIT_WINDOW = 86400
MAX_CONTENT_CHARS = 20000
MAX_TITLE_CHARS = 32
MAX_AUTHOR_CHARS = 16
MAX_DIGEST_CHARS = 128
MAX_CONTENT_BYTES = 1 * 1024 * 1024
MAX_SOURCE_URL_BYTES = 1024


# ── Error ─────────────────────────────────────────────────
class WechatError(Exception):
    def __init__(self, errcode, errmsg, detail=None):
        self.errcode = errcode
        self.errmsg = errmsg
        self.detail = detail
        parts = [f"[{errcode}] {errmsg}"]
        if detail:
            parts.append(f"({detail})")
        super().__init__(" ".join(parts))


# ── Rate Limiter ──────────────────────────────────────────
class RateLimiter:
    def __init__(self, max_calls=RATE_LIMIT_DAY, window=RATE_LIMIT_WINDOW):
        self.max_calls = max_calls
        self.window = window
        self.calls = []

    def acquire(self):
        now = time.time()
        self.calls = [t for t in self.calls if now - t < self.window]
        if len(self.calls) >= self.max_calls:
            oldest = self.calls[0]
            wait = self.window - (now - oldest) + 1
            if wait > 0:
                print(f"[rate] 接近每日限流 ({self.max_calls}/天)，等待 {wait:.0f}s", file=sys.stderr)
                time.sleep(wait)
        self.calls.append(now)


# ── Validation ────────────────────────────────────────────
def validate_article(title, content, digest="", author="", source_url=""):
    errors = []
    if len(title) > MAX_TITLE_CHARS:
        errors.append(f"标题长度 {len(title)} 超过限制 {MAX_TITLE_CHARS}")
    if author and len(author) > MAX_AUTHOR_CHARS:
        errors.append(f"作者长度 {len(author)} 超过限制 {MAX_AUTHOR_CHARS}")
    if digest and len(digest) > MAX_DIGEST_CHARS:
        errors.append(f"摘要长度 {len(digest)} 超过限制 {MAX_DIGEST_CHARS}")
    if len(content) > MAX_CONTENT_CHARS:
        errors.append(f"正文 {len(content)} 字符超过限制 {MAX_CONTENT_CHARS}")
    content_bytes = len(content.encode("utf-8"))
    if content_bytes > MAX_CONTENT_BYTES:
        errors.append(f"正文 {content_bytes} 字节超过限制 {MAX_CONTENT_BYTES}")
    if re.search(r"<script\b", content, re.IGNORECASE):
        errors.append("正文包含 <script> 标签，微信会过滤")
    if source_url and len(source_url.encode("utf-8")) > MAX_SOURCE_URL_BYTES:
        errors.append(f"原文链接超过限制 {MAX_SOURCE_URL_BYTES}")
    if errors:
        raise WechatError(-1, "参数校验失败", "; ".join(errors))


def _build_multipart(field_name, filename, filedata, content_type, extra_fields=None):
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    parts = []
    if extra_fields:
        for k, v in extra_fields.items():
            parts.append(
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="{k}"\r\n'
                f"\r\n"
                f"{v}\r\n"
            )
    parts.append(
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    )
    body = "".join(parts).encode("utf-8") + filedata + f"\r\n--{boundary}--\r\n".encode("utf-8")
    return body, boundary


# ── Client ────────────────────────────────────────────────
class WechatClient:
    def __init__(self, app_id=None, app_secret=None):
        self.app_id = app_id or os.environ.get("WECHAT_APP_ID", "")
        self.app_secret = app_secret or os.environ.get("WECHAT_APP_SECRET", "")
        if not self.app_id or not self.app_secret:
            raise WechatError(-1, "配置缺失", "请设置 WECHAT_APP_ID 和 WECHAT_APP_SECRET")
        self._token = None
        self._token_expires = 0
        self._limiter = RateLimiter()
        self._retry = 3

    # ── Token ──
    def get_token(self, stable=False):
        now = time.time()
        if self._token and now < self._token_expires:
            return self._token
        if stable:
            return self._fetch_stable_token()
        return self._fetch_token()

    def _fetch_token(self):
        params = urllib.parse.urlencode({
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret,
        })
        data = self._raw_get(f"{WECHAT_API_BASE}/token?{params}")
        self._token = data["access_token"]
        self._token_expires = time.time() + data["expires_in"] - 300
        return self._token

    def _fetch_stable_token(self):
        body = json.dumps({
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret,
            "force_refresh": False,
        }).encode()
        data = self._raw_post(f"{WECHAT_API_BASE}/stable_token", body, add_token=False)
        self._token = data["access_token"]
        self._token_expires = time.time() + data["expires_in"] - 300
        return self._token

    # ── HTTP helpers ──
    def _api_url(self, path):
        return f"{WECHAT_API_BASE}{path}?access_token={self.get_token()}"

    def _dc_url(self, path):
        return f"{DATACUBE_BASE}{path}?access_token={self.get_token()}"

    def _request(self, url, method="GET", body=None, headers=None):
        hdrs = {"User-Agent": "WechatPublisher/1.0"}
        if headers:
            hdrs.update(headers)
        req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read()
        except urllib.error.HTTPError as e:
            raw = e.read()
            raise WechatError(-1, f"HTTP {e.code}", raw.decode("utf-8", errors="replace")[:500])
        except urllib.error.URLError as e:
            raise WechatError(-1, "网络错误", str(e.reason))

        ct = resp.headers.get("Content-Type", "")
        if "application/json" in ct or "text/plain" in ct:
            return json.loads(raw.decode("utf-8"))
        return raw

    def _raw_get(self, url):
        return self._request(url, "GET")

    def _raw_post(self, url, body, add_token=True, headers=None):
        return self._request(url, "POST", body, headers=headers)

    def _post(self, path, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        for attempt in range(self._retry):
            self._limiter.acquire()
            url = self._api_url(path)
            try:
                result = self._request(url, "POST", body)
            except WechatError as e:
                if e.errcode == 42001 and attempt < self._retry - 1:
                    self._token = None
                    self._token_expires = 0
                    continue
                raise
            errcode = result.get("errcode", 0)
            if errcode == 0:
                return result
            if errcode == 42001 and attempt < self._retry - 1:
                self._token = None
                self._token_expires = 0
                continue
            if errcode in (45009, 45047) and attempt < self._retry - 1:
                wait = 2 ** attempt
                print(f"[rate] 触发限流 ({errcode})，等待 {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            if errcode == 88000 and attempt < self._retry - 1:
                time.sleep(5)
                continue
            raise WechatError(errcode, result.get("errmsg", ""), json.dumps(payload, ensure_ascii=False)[:300])
        raise WechatError(-1, "请求失败", "重试次数耗尽")

    def _get(self, path, params=None):
        qs = urllib.parse.urlencode(params) if params else ""
        url = f"{WECHAT_API_BASE}{path}?access_token={self.get_token()}"
        if qs:
            url += f"&{qs}"
        for attempt in range(self._retry):
            self._limiter.acquire()
            try:
                result = self._request(url, "GET")
            except WechatError as e:
                if e.errcode == 42001 and attempt < self._retry - 1:
                    self._token = None
                    self._token_expires = 0
                    continue
                raise
            errcode = result.get("errcode", 0)
            if errcode == 0:
                return result
            if errcode == 42001 and attempt < self._retry - 1:
                self._token = None
                self._token_expires = 0
                continue
            raise WechatError(errcode, result.get("errmsg", ""))
        raise WechatError(-1, "请求失败", "重试次数耗尽")

    def _dc_post(self, path, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        url = f"{DATACUBE_BASE}{path}?access_token={self.get_token()}"
        return self._request(url, "POST", body)

    def _media_upload(self, url, filepath, field_name="media", extra_fields=None):
        if not os.path.exists(filepath):
            raise WechatError(-1, "文件不存在", filepath)
        ext = os.path.splitext(filepath)[1].lower()
        ct_map = {
            ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".png": "image/png", ".gif": "image/gif",
            ".bmp": "image/bmp", ".mp4": "video/mp4",
            ".mp3": "audio/mpeg", ".amr": "audio/amr",
            ".wma": "audio/x-ms-wma",
        }
        ctype = ct_map.get(ext, "application/octet-stream")
        filename = os.path.basename(filepath)
        with open(filepath, "rb") as f:
            filedata = f.read()
        body, boundary = _build_multipart(field_name, filename, filedata, ctype, extra_fields)
        headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}
        return self._request(url, "POST", body, headers)

    # ── Draft ──
    def draft_create(self, articles):
        for art in articles:
            validate_article(
                art.get("title", ""),
                art.get("content", ""),
                art.get("digest", ""),
                art.get("author", ""),
                art.get("content_source_url", ""),
            )
        return self._post("/draft/add", {"articles": articles}).get("media_id")

    def draft_get(self, media_id):
        return self._post("/draft/get", {"media_id": media_id})

    def draft_update(self, media_id, index, article):
        validate_article(
            article.get("title", ""),
            article.get("content", ""),
            article.get("digest", ""),
            article.get("author", ""),
            article.get("content_source_url", ""),
        )
        return self._post("/draft/update", {
            "media_id": media_id, "index": index, "articles": article,
        })

    def draft_count(self):
        return self._get("/draft/count")

    def draft_delete(self, media_id):
        return self._post("/draft/delete", {"media_id": media_id})

    def draft_list(self, offset=0, count=20, no_content=1):
        return self._post("/draft/batchget", {
            "offset": offset, "count": min(count, 20), "no_content": no_content,
        })

    # ── Publish ──
    def publish_submit(self, media_id):
        result = self._post("/freepublish/submit", {"media_id": media_id})
        return result.get("publish_id"), result.get("msg_data_id")

    def publish_status(self, publish_id):
        return self._post("/freepublish/get", {"publish_id": publish_id})

    def published_list(self, offset=0, count=20, no_content=0):
        return self._post("/freepublish/batchget", {
            "offset": offset, "count": min(count, 20), "no_content": no_content,
        })

    def published_delete(self, article_id):
        return self._post("/freepublish/delete", {"article_id": article_id})

    def published_getarticle(self, article_id):
        return self._post("/freepublish/getarticle", {"article_id": article_id})

    # ── Material ──
    def material_add_image(self, filepath):
        token = self.get_token()
        url = f"{WECHAT_API_BASE}/material/add_material?access_token={token}"
        data = self._media_upload(url, filepath)
        if isinstance(data, dict) and data.get("errcode", 0) != 0:
            raise WechatError(data.get("errcode"), data.get("errmsg", ""))
        return data

    def material_add_thumb(self, filepath):
        token = self.get_token()
        url = f"{WECHAT_API_BASE}/material/add_material?access_token={token}&type=thumb"
        return self._media_upload(url, filepath)

    def material_add_video(self, filepath, title, introduction=""):
        token = self.get_token()
        url = f"{WECHAT_API_BASE}/material/add_material?access_token={token}&type=video"
        desc = json.dumps({"title": title, "introduction": introduction}, ensure_ascii=False)
        return self._media_upload(url, filepath, extra_fields={"description": desc})

    def material_get(self, media_id):
        token = self.get_token()
        url = f"{WECHAT_API_BASE}/material/get_material?access_token={token}"
        body = json.dumps({"media_id": media_id}).encode("utf-8")
        return self._request(url, "POST", body)

    def material_delete(self, media_id):
        return self._post("/material/del_material", {"media_id": media_id})

    def material_list(self, material_type="image", offset=0, count=20):
        return self._post("/material/batchget_material", {
            "type": material_type, "offset": offset, "count": min(count, 20),
        })

    def material_update_news(self, media_id, index, article):
        return self._post("/material/update_news", {
            "media_id": media_id, "index": index, "articles": article,
        })

    # ── Image upload for content ──
    def upload_image(self, filepath):
        token = self.get_token()
        url = f"{WECHAT_API_BASE}/media/uploadimg?access_token={token}"
        data = self._media_upload(url, filepath)
        return data.get("url", "")

    # ── Stats ──
    def stats_summary(self, begin_date, end_date):
        return self._dc_post("/getarticlesummary", {
            "begin_date": begin_date, "end_date": end_date,
        })

    def stats_total(self, begin_date, end_date):
        return self._dc_post("/getarticletotal", {
            "begin_date": begin_date, "end_date": end_date,
        })

    def stats_read(self, begin_date, end_date):
        return self._dc_post("/getarticleread", {
            "begin_date": begin_date, "end_date": end_date,
        })

    def stats_read_hour(self, begin_date, end_date):
        return self._dc_post("/getarticlereadhour", {
            "begin_date": begin_date, "end_date": end_date,
        })

    def stats_share(self, begin_date, end_date):
        return self._dc_post("/getarticleshare", {
            "begin_date": begin_date, "end_date": end_date,
        })

    def stats_share_hour(self, begin_date, end_date):
        return self._dc_post("/getarticlesharehour", {
            "begin_date": begin_date, "end_date": end_date,
        })

    def stats_user_read(self, begin_date, end_date):
        return self._dc_post("/getuserread", {
            "begin_date": begin_date, "end_date": end_date,
        })

    def stats_user_read_hour(self, begin_date, end_date):
        return self._dc_post("/getuserreadhour", {
            "begin_date": begin_date, "end_date": end_date,
        })

    # ── Comment ──
    def comment_list(self, msg_data_id, index=0, begin=0, count=50, comment_type=0):
        return self._post("/comment/list", {
            "msg_data_id": msg_data_id, "index": index,
            "begin": begin, "count": min(count, 50), "type": comment_type,
        })

    def comment_mark(self, msg_data_id, comment_id, index=0):
        return self._post("/comment/markelect", {
            "msg_data_id": msg_data_id, "comment_id": comment_id, "index": index,
        })

    def comment_unmark(self, msg_data_id, comment_id, index=0):
        return self._post("/comment/unmarkelect", {
            "msg_data_id": msg_data_id, "comment_id": comment_id, "index": index,
        })

    def comment_delete(self, msg_data_id, comment_id, index=0):
        return self._post("/comment/delete", {
            "msg_data_id": msg_data_id, "comment_id": comment_id, "index": index,
        })

    def comment_reply(self, msg_data_id, comment_id, content, index=0):
        return self._post("/comment/addreply", {
            "msg_data_id": msg_data_id, "comment_id": comment_id,
            "content": content, "index": index,
        })

    def comment_delete_reply(self, msg_data_id, comment_id, index=0):
        return self._post("/comment/delreply", {
            "msg_data_id": msg_data_id, "comment_id": comment_id, "index": index,
        })


# ── Template rendering ────────────────────────────────────
def extract_title(content):
    for line in content.split("\n"):
        m = re.match(r"^#\s+(.+)$", line.strip())
        if m:
            return m.group(1)
    for line in content.split("\n"):
        m = re.match(r"<h[12][^>]*>(.+?)</h[12]>", line.strip(), re.IGNORECASE)
        if m:
            return m.group(1)
    return "Untitled"


def render_html(title, content, style="standard", author="", date=""):
    date_str = date or time.strftime("%Y-%m-%d")
    author_str = author or os.environ.get("WECHAT_AUTHOR", "")

    TM = {
        "standard": (
            '<div style="font-family: -apple-system,BlinkMacSystemFont,\'Microsoft YaHei\',sans-serif;'
            'max-width:677px;margin:0 auto;padding:20px;">'
            '<h1 style="font-size:22px;font-weight:bold;color:#1a1a1a;margin-bottom:8px;">{t}</h1>'
            '<p style="color:#999;font-size:13px;margin-bottom:24px;">{m}</p>'
            '<div style="font-size:15px;line-height:1.8;color:#333;">{c}</div></div>'
        ),
        "business": (
            '<div style="font-family:-apple-system,BlinkMacSystemFont,\'Microsoft YaHei\',sans-serif;'
            'max-width:677px;margin:0 auto;">'
            '<div style="background:linear-gradient(135deg,#1a365d,#2b6cb0);padding:36px 24px;text-align:center;">'
            '<h1 style="color:#fff;font-size:24px;margin:0 0 8px;">{t}</h1>'
            '<p style="color:rgba(255,255,255,.75);font-size:13px;margin:0;">{m}</p></div>'
            '<div style="padding:24px;font-size:15px;line-height:1.8;color:#333;">{c}</div>'
            '<div style="background:linear-gradient(135deg,#2b6cb0,#1a365d);padding:16px;text-align:center;">'
            '<p style="color:rgba(255,255,255,.6);font-size:12px;margin:0;">{a}</p></div></div>'
        ),
        "minimal": (
            '<div style="font-family:Georgia,\'Songti SC\',serif;max-width:677px;margin:0 auto;padding:32px 20px;">'
            '<h1 style="font-size:26px;font-weight:400;color:#1a1a1a;text-align:center;margin-bottom:6px;">{t}</h1>'
            '<p style="text-align:center;color:#aaa;font-size:13px;margin-bottom:28px;">{m}</p>'
            '<hr style="border:none;border-top:1px solid #eee;margin:0 0 28px;">'
            '<div style="font-size:16px;line-height:1.9;color:#333;">{c}</div>'
            '<hr style="border:none;border-top:1px solid #eee;margin:28px 0 0;">'
            '<p style="text-align:center;color:#aaa;font-size:12px;margin-top:12px;">{a}</p></div>'
        ),
        "tech": (
            '<div style="font-family:\'SF Mono\',Monaco,\'Microsoft YaHei\',monospace;'
            'max-width:677px;margin:0 auto;">'
            '<div style="background:linear-gradient(135deg,#0d4a2e,#1a9c5e);padding:32px 24px;text-align:center;">'
            '<h1 style="color:#fff;font-size:22px;margin:0 0 6px;">{t}</h1>'
            '<p style="color:rgba(255,255,255,.7);font-size:13px;margin:0;">{m}</p></div>'
            '<div style="padding:24px;font-size:14px;line-height:1.8;color:#2d3748;">{c}</div>'
            '<div style="background:#f0faf4;padding:16px 24px;text-align:center;">'
            '<p style="color:#666;font-size:12px;margin:0;">{a}</p></div></div>'
        ),
        "academic": (
            '<div style="font-family:\'Palatino\',\'STSong\',\'Songti SC\',serif;'
            'max-width:677px;margin:0 auto;">'
            '<div style="background:linear-gradient(135deg,#3b0764,#7c3aed);padding:32px 24px;text-align:center;">'
            '<h1 style="color:#fff;font-size:22px;margin:0 0 6px;">{t}</h1>'
            '<p style="color:rgba(255,255,255,.7);font-size:13px;margin:0;">{m}</p></div>'
            '<div style="padding:24px;font-size:15px;line-height:1.9;color:#333;">{c}</div>'
            '<div style="background:#f5f3ff;padding:12px 24px;text-align:center;">'
            '<p style="color:#666;font-size:12px;margin:0;">{a}</p></div></div>'
        ),
        "warm": (
            '<div style="font-family:-apple-system,\'Microsoft YaHei\',sans-serif;'
            'max-width:677px;margin:0 auto;">'
            '<div style="background:linear-gradient(135deg,#c05621,#ed8936);padding:36px 24px;text-align:center;">'
            '<h1 style="color:#fff;font-size:24px;margin:0 0 8px;">{t}</h1>'
            '<p style="color:rgba(255,255,255,.75);font-size:13px;margin:0;">{m}</p></div>'
            '<div style="padding:24px;font-size:15px;line-height:1.8;color:#4a3728;">{c}</div>'
            '<div style="background:linear-gradient(135deg,#ed8936,#c05621);padding:16px;text-align:center;">'
            '<p style="color:rgba(255,255,255,.6);font-size:12px;margin:0;">{a}</p></div></div>'
        ),
    }
    tpl = TM.get(style, TM["standard"])
    meta = f"{author_str} | {date_str}" if author_str else date_str
    return tpl.format(t=title, m=meta, c=content, a=author_str or "")


# ── CLI helpers ────────────────────────────────────────────
def _consume_flags(args):
    flags = {}
    positionals = []
    i = 0
    while i < len(args):
        if args[i].startswith("--"):
            key = args[i][2:]
            if i + 1 < len(args) and not args[i + 1].startswith("--"):
                flags[key] = args[i + 1]
                i += 2
            else:
                flags[key] = True
                i += 1
        elif args[i].startswith("-") and not args[i].startswith("--"):
            key = args[i][1:]
            if i + 1 < len(args) and not args[i + 1].startswith("-"):
                flags[key] = args[i + 1]
                i += 2
            else:
                flags[key] = True
                i += 1
        else:
            positionals.append(args[i])
            i += 1
    return flags, positionals


def _read(path):
    if path == "-":
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _exit(msg):
    print(f"错误: {msg}", file=sys.stderr)
    sys.exit(1)


# ── Command handlers ──────────────────────────────────────
def cmd_draft_create(client, args):
    flags, pos = _consume_flags(args)
    if len(pos) < 1:
        _exit("用法: draft create <json_file>")
    payload = json.loads(_read(pos[0]))
    articles = payload if isinstance(payload, list) else payload.get("articles", [payload])
    for art in articles:
        art.setdefault("author", flags.get("author", os.environ.get("WECHAT_AUTHOR", "")))
    mid = client.draft_create(articles)
    print(mid)


def cmd_draft_get(client, args):
    if not args:
        _exit("用法: draft get <media_id>")
    result = client.draft_get(args[0])
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_draft_update(client, args):
    flags, pos = _consume_flags(args)
    if len(pos) < 2:
        _exit("用法: draft update <media_id> <json_file> [--index 0]")
    result = client.draft_update(pos[0], int(flags.get("index", "0")), json.loads(_read(pos[1])))
    print(json.dumps(result, ensure_ascii=False))


def cmd_draft_count(client, args):
    result = client.draft_count()
    print(result.get("total_count", 0))


def cmd_draft_list(client, args):
    flags, _ = _consume_flags(args)
    result = client.draft_list(int(flags.get("offset", "0")), int(flags.get("count", "20")))
    for item in result.get("item", []):
        art = item.get("content", {}).get("news_item", [{}])[0]
        print(f"{item['media_id']}  {art.get('title','?')}  [{art.get('update_time','')}]")
    print(f"\n总计: {len(result.get('item', []))}")


def cmd_draft_delete(client, args):
    if not args:
        _exit("用法: draft delete <media_id>")
    client.draft_delete(args[0])
    print("OK")


# ── Publish ──
def cmd_publish_submit(client, args):
    if not args:
        _exit("用法: publish <media_id>")
    pid, msg_data_id = client.publish_submit(args[0])
    out = f"publish_id: {pid}"
    if msg_data_id:
        out += f"\nmsg_data_id: {msg_data_id}"
    print(out)


def cmd_publish_status(client, args):
    if not args:
        _exit("用法: publish status <publish_id>")
    result = client.publish_status(args[0])
    s = result.get("publish_status", "?")
    sm = {0: "发布成功", 1: "发布中", 2: "原创失败", 3: "常规失败", 4: "审核不通过",
          5: "用户删除所有文章", 6: "系统封禁所有文章"}
    print(f"状态: {sm.get(s, s)}")
    for k in ("article_id", "publish_id"):
        if result.get(k):
            print(f"{k}: {result[k]}")
    if result.get("fail_idx"):
        print(f"失败索引: {result['fail_idx']}")


def cmd_published_list(client, args):
    flags, _ = _consume_flags(args)
    no_content = 1 if flags.get("no-content", "0") == "1" else 0
    result = client.published_list(int(flags.get("offset", "0")), int(flags.get("count", "20")), no_content)
    for item in result.get("item", []):
        art = item.get("content", {}).get("news_item", [{}])[0]
        print(f"{item['article_id']}  {art.get('title','?')}  {art.get('update_time','')}")
    print(f"\n总计: {result.get('total_count', 0)}")


def cmd_published_delete(client, args):
    if not args:
        _exit("用法: published delete <article_id>")
    client.published_delete(args[0])
    print("OK")


def cmd_published_getarticle(client, args):
    if not args:
        _exit("用法: published getarticle <article_id>")
    result = client.published_getarticle(args[0])
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ── Material ──
def cmd_material_add(client, args):
    flags, pos = _consume_flags(args)
    if not pos:
        _exit("用法: material add <filepath> [--type image|thumb|video] [--title <title>] [--intro <intro>]")
    fpath = pos[0]
    mtype = flags.get("type", "image")
    if mtype == "video":
        result = client.material_add_video(fpath, flags.get("title", ""), flags.get("intro", ""))
    elif mtype == "thumb":
        result = client.material_add_thumb(fpath)
    else:
        result = client.material_add_image(fpath)
    print(json.dumps(result, ensure_ascii=False))


def cmd_material_get(client, args):
    if not args:
        _exit("用法: material get <media_id> [--out <file>]")
    flags, pos = _consume_flags(args)
    result = client.material_get(pos[0])
    if isinstance(result, bytes):
        out = flags.get("out", "")
        if out:
            with open(out, "wb") as f:
                f.write(result)
            print(f"已保存到 {out}")
        else:
            sys.stdout.buffer.write(result)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_material_delete(client, args):
    if not args:
        _exit("用法: material delete <media_id>")
    client.material_delete(args[0])
    print("OK")


def cmd_material_list(client, args):
    flags, _ = _consume_flags(args)
    result = client.material_list(
        flags.get("type", "image"),
        int(flags.get("offset", "0")),
        int(flags.get("count", "20")),
    )
    for item in result.get("item", []):
        info = f"{item.get('media_id','?')}  {item.get('name','?')}"
        if "update_time" in item:
            info += f"  [{item['update_time']}]"
        print(info)
    total = result.get("total_count", result.get("item_count", 0))
    print(f"\n总计: {total}")


def cmd_material_update_news(client, args):
    flags, pos = _consume_flags(args)
    if len(pos) < 2:
        _exit("用法: material update_news <media_id> <json_file> [--index 0]")
    result = client.material_update_news(pos[0], int(flags.get("index", "0")), json.loads(_read(pos[1])))
    print(json.dumps(result, ensure_ascii=False))


# ── Upload ──
def cmd_upload(client, args):
    if not args:
        _exit("用法: upload <image_path>")
    print(client.upload_image(args[0]))


# ── Stats ──
def _fmt_date_range(args):
    flags, pos = _consume_flags(args)
    if len(pos) < 2:
        _exit("用法: ... <begin_date> <end_date>")
    return flags, pos[0], pos[1]


def cmd_stats_summary(client, args):
    _, b, e = _fmt_date_range(args)
    result = client.stats_summary(b, e)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_stats_total(client, args):
    _, b, e = _fmt_date_range(args)
    result = client.stats_total(b, e)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_stats_read(client, args):
    _, b, e = _fmt_date_range(args)
    result = client.stats_read(b, e)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_stats_read_hour(client, args):
    _, b, e = _fmt_date_range(args)
    result = client.stats_read_hour(b, e)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_stats_share(client, args):
    _, b, e = _fmt_date_range(args)
    result = client.stats_share(b, e)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_stats_share_hour(client, args):
    _, b, e = _fmt_date_range(args)
    result = client.stats_share_hour(b, e)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_stats_user_read(client, args):
    _, b, e = _fmt_date_range(args)
    result = client.stats_user_read(b, e)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_stats_user_read_hour(client, args):
    _, b, e = _fmt_date_range(args)
    result = client.stats_user_read_hour(b, e)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ── Comment ──
def _parse_comment_args(args):
    flags, pos = _consume_flags(args)
    if len(pos) < 1:
        _exit("需要 msg_data_id")
    return flags, pos[0]


def cmd_comment_list(client, args):
    flags, mid = _parse_comment_args(args)
    result = client.comment_list(mid, int(flags.get("index", "0")),
                                 int(flags.get("begin", "0")),
                                 int(flags.get("count", "50")),
                                 int(flags.get("type", "0")))
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_comment_mark(client, args):
    flags, mid = _parse_comment_args(args)
    if len(flags.get("comment_id", "")) == 0:
        _exit("需要 --comment_id <id>")
    client.comment_mark(mid, flags["comment_id"], int(flags.get("index", "0")))
    print("OK")


def cmd_comment_unmark(client, args):
    flags, mid = _parse_comment_args(args)
    if not flags.get("comment_id"):
        _exit("需要 --comment_id <id>")
    client.comment_unmark(mid, flags["comment_id"], int(flags.get("index", "0")))
    print("OK")


def cmd_comment_delete(client, args):
    flags, mid = _parse_comment_args(args)
    if not flags.get("comment_id"):
        _exit("需要 --comment_id <id>")
    client.comment_delete(mid, flags["comment_id"], int(flags.get("index", "0")))
    print("OK")


def cmd_comment_reply(client, args):
    flags, mid = _parse_comment_args(args)
    if not flags.get("comment_id"):
        _exit("需要 --comment_id <id>")
    content = flags.get("content", "")
    if not content and len(args) > 1:
        content = args[-1]
    if not content:
        _exit("需要 --content <回复内容>")
    client.comment_reply(mid, flags["comment_id"], content, int(flags.get("index", "0")))
    print("OK")


def cmd_comment_delete_reply(client, args):
    flags, mid = _parse_comment_args(args)
    if not flags.get("comment_id"):
        _exit("需要 --comment_id <id>")
    client.comment_delete_reply(mid, flags["comment_id"], int(flags.get("index", "0")))
    print("OK")


# ── Render ──
def cmd_render(client, args):
    flags, pos = _consume_flags(args)
    content = _read(pos[0]) if pos else sys.stdin.read()
    title = extract_title(content)
    print(render_html(title, content, style=flags.get("style", "standard")))


# ── Test ──
def cmd_test(client, args):
    token = client.get_token()
    masked = token[:10] + "..." if len(token) > 10 else "?"
    print(f"Token: {masked}")
    cnt = client.draft_count()
    print(f"草稿数: {cnt.get('total_count', 0)}")
    print("连接正常 ✓")


# ── Help ──
def cmd_help(client, args):
    print("""微信公众号发布工具 v1.0.7

草稿管理:
  draft create <json>                   创建草稿（JSON 支持多图文）
  draft get <media_id>                  获取草稿详情
  draft update <media_id> <json> [--index N]
  draft count                           草稿数量
  draft list [--offset 0] [--count 20]
  draft delete <media_id>

发布管理:
  publish <media_id>                    提交发布
  publish status <publish_id>           查询发布状态

已发布管理:
  published list [--offset 0] [--count 20] [--no-content 1]
  published delete <article_id>
  published getarticle <article_id>     获取已发布图文详情

素材管理:
  material add <file> [--type image|thumb|video] [--title T] [--intro I]
  material get <media_id> [--out <file>]
  material delete <media_id>
  material list [--type image|video|voice|news] [--offset 0] [--count 20]
  material update_news <media_id> <json> [--index 0]

图片上传（用于正文）:
  upload <image_path>

数据统计:
  stats summary <begin> <end>
  stats total <begin> <end>
  stats read <begin> <end>
  stats readhour <begin> <end>
  stats share <begin> <end>
  stats sharehour <begin> <end>
  stats userread <begin> <end>
  stats userreadhour <begin> <end>

评论管理:
  comment list <msg_data_id> [--index 0] [--begin 0] [--count 50] [--type 0]
  comment mark <msg_data_id> --comment_id <id>
  comment unmark <msg_data_id> --comment_id <id>
  comment delete <msg_data_id> --comment_id <id>
  comment reply <msg_data_id> --comment_id <id> --content <text>
  comment delreply <msg_data_id> --comment_id <id>

其他:
  render <file> [--style standard|business|minimal|tech|academic|warm]
  test                                测试连接
""")


# ── Command routing ───────────────────────────────────────
CMDS = {
    "draft": {
        None: cmd_draft_create,
        "create": cmd_draft_create,
        "get": cmd_draft_get,
        "update": cmd_draft_update,
        "count": cmd_draft_count,
        "list": cmd_draft_list,
        "delete": cmd_draft_delete,
    },
    "publish": {
        None: cmd_publish_submit,
        "status": cmd_publish_status,
    },
    "published": {
        "list": cmd_published_list,
        "delete": cmd_published_delete,
        "getarticle": cmd_published_getarticle,
    },
    "material": {
        None: cmd_material_add,
        "add": cmd_material_add,
        "get": cmd_material_get,
        "delete": cmd_material_delete,
        "list": cmd_material_list,
        "update_news": cmd_material_update_news,
    },
    "upload": {None: cmd_upload},
    "stats": {
        "summary": cmd_stats_summary,
        "total": cmd_stats_total,
        "read": cmd_stats_read,
        "readhour": cmd_stats_read_hour,
        "share": cmd_stats_share,
        "sharehour": cmd_stats_share_hour,
        "userread": cmd_stats_user_read,
        "userreadhour": cmd_stats_user_read_hour,
    },
    "comment": {
        None: cmd_comment_list,
        "list": cmd_comment_list,
        "mark": cmd_comment_mark,
        "unmark": cmd_comment_unmark,
        "delete": cmd_comment_delete,
        "reply": cmd_comment_reply,
        "delreply": cmd_comment_delete_reply,
    },
    "render": {None: cmd_render},
    "test": {None: cmd_test},
    "help": {None: cmd_help},
}


def main():
    flags, positionals = _consume_flags(sys.argv[1:])
    if flags.get("help") or not positionals:
        cmd_help(None, [])
        sys.exit(0 if flags.get("help") else 1)

    app_id = os.environ.get("WECHAT_APP_ID")
    app_secret = os.environ.get("WECHAT_APP_SECRET")
    client = None
    try:
        if positionals[0] not in ("render", "help"):
            client = WechatClient(app_id, app_secret)
    except WechatError as e:
        _exit(str(e))

    cmd = positionals[0]
    sub = CMDS.get(cmd)
    if not sub:
        _exit(f"未知命令: {cmd}\n请用 --help 查看用法")

    sub_args = positionals[1:]
    if isinstance(sub, dict):
        if not sub_args:
            handler = sub.get(None) or cmd_help
            handler(client, [])
        else:
            handler = sub.get(sub_args[0]) or sub.get(None)
            if handler:
                handler(client, sub_args[1:] if sub.get(sub_args[0]) else sub_args)
            else:
                _exit(f"未知子命令: {sub_args[0]}")
    else:
        sub(client, sub_args)


if __name__ == "__main__":
    try:
        main()
    except WechatError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(130)
