#!/usr/bin/env python3
"""微信公众号接口封装"""
import json
import mimetypes
import os
import urllib.parse
import urllib.request
import uuid
from base64 import b64encode
from pathlib import Path


class WeChatSkillError(Exception):
    pass


def load_dotenv() -> None:
    for env_path in [Path("/root/.openclaw/.env"), Path(__file__).resolve().parents[1] / ".env"]:
        if not env_path.exists():
            continue
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise WeChatSkillError(f"Missing env: {name}")
    return value


def build_api_url(path: str, **query) -> str:
    return f"https://api.weixin.qq.com{path}?{urllib.parse.urlencode(query)}"


def http_json(url: str, method: str = "GET", payload: dict | None = None) -> dict:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")
    try:
        return json.loads(body)
    except json.JSONDecodeError as e:
        raise WeChatSkillError(f"Non-JSON response: {body[:300]}") from e


def http_multipart(url: str, file_field: str, file_path: str, extra_fields: dict[str, str] | None = None) -> dict:
    path = Path(file_path).expanduser().resolve()
    if not path.is_file():
        raise WeChatSkillError(f"File not found: {file_path}")
    boundary = f"----OpenClawBoundary{uuid.uuid4().hex}"
    mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    body = bytearray()
    for name, value in (extra_fields or {}).items():
        body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n".encode())
    body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{file_field}\"; filename=\"{path.name}\"\r\nContent-Type: {mime_type}\r\n\r\n".encode())
    body.extend(path.read_bytes())
    body.extend(f"\r\n--{boundary}--\r\n".encode())
    req = urllib.request.Request(url, data=bytes(body), method="POST", headers={"Accept": "application/json", "Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read().decode("utf-8")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise WeChatSkillError(f"Non-JSON response: {raw[:300]}") from e


def get_access_token() -> str:
    load_dotenv()
    url = build_api_url("/cgi-bin/token", grant_type="client_credential", appid=require_env("WECHAT_APP_ID"), secret=require_env("WECHAT_APP_SECRET"))
    result = http_json(url)
    token = result.get("access_token")
    if not token:
        raise WeChatSkillError(f"Failed to get token: {json.dumps(result, ensure_ascii=False)}")
    return token


def check_wechat_error(result: dict, step: str) -> dict:
    if result.get("errcode", 0) not in (0, None):
        raise WeChatSkillError(f"{step} failed: {json.dumps(result, ensure_ascii=False)}")
    return result


def post_with_token(path: str, payload: dict, step: str) -> dict:
    token = get_access_token()
    return check_wechat_error(http_json(build_api_url(path, access_token=token), method="POST", payload=payload), step)


def get_with_token(path: str, step: str) -> dict:
    token = get_access_token()
    return check_wechat_error(http_json(build_api_url(path, access_token=token)), step)


def add_draft(article: dict) -> dict:
    return post_with_token("/cgi-bin/draft/add", {"articles": [article]}, "add_draft")

def update_draft(media_id: str, article: dict, index: int = 0) -> dict:
    return post_with_token("/cgi-bin/draft/update", {"media_id": media_id, "index": index, "articles": article}, "update_draft")

def get_draft(media_id: str) -> dict:
    return post_with_token("/cgi-bin/draft/get", {"media_id": media_id}, "get_draft")

def list_drafts(offset: int = 0, count: int = 20, no_content: bool = False) -> dict:
    return post_with_token("/cgi-bin/draft/batchget", {"offset": offset, "count": count, "no_content": int(no_content)}, "list_drafts")

def count_drafts() -> dict:
    return get_with_token("/cgi-bin/draft/count", "count_drafts")

def delete_draft(media_id: str) -> dict:
    return post_with_token("/cgi-bin/draft/delete", {"media_id": media_id}, "delete_draft")

def submit_publish(media_id: str) -> dict:
    return post_with_token("/cgi-bin/freepublish/submit", {"media_id": media_id}, "submit_publish")

def query_publish_status(publish_id: str) -> dict:
    return post_with_token("/cgi-bin/freepublish/get", {"publish_id": publish_id}, "query_publish_status")

def list_published(offset: int = 0, count: int = 20, no_content: bool = False) -> dict:
    return post_with_token("/cgi-bin/freepublish/batchget", {"offset": offset, "count": count, "no_content": int(no_content)}, "list_published")

def get_published_article(article_id: str) -> dict:
    return post_with_token("/cgi-bin/freepublish/getarticle", {"article_id": article_id}, "get_published_article")

def delete_published_article(article_id: str, index: int | None = None) -> dict:
    payload: dict = {"article_id": article_id}
    if index is not None:
        payload["index"] = index
    return post_with_token("/cgi-bin/freepublish/delete", payload, "delete_published_article")

def upload_permanent_material(file_path: str, material_type: str = "thumb") -> dict:
    token = get_access_token()
    url = build_api_url("/cgi-bin/material/add_material", access_token=token, type=material_type)
    return check_wechat_error(http_multipart(url, file_field="media", file_path=file_path), "upload_permanent_material")

def upload_article_image(file_path: str) -> dict:
    token = get_access_token()
    url = build_api_url("/cgi-bin/media/uploadimg", access_token=token)
    return check_wechat_error(http_multipart(url, file_field="media", file_path=file_path), "upload_article_image")

def get_material(media_id: str) -> dict:
    return post_with_token("/cgi-bin/material/get_material", {"media_id": media_id}, "get_material")

def delete_material(media_id: str) -> dict:
    return post_with_token("/cgi-bin/material/del_material", {"media_id": media_id}, "delete_material")

def list_materials(material_type: str, offset: int = 0, count: int = 20) -> dict:
    return post_with_token("/cgi-bin/material/batchget_material", {"type": material_type, "offset": offset, "count": count}, "list_materials")

def get_material_count() -> dict:
    return get_with_token("/cgi-bin/material/get_materialcount", "get_material_count")
