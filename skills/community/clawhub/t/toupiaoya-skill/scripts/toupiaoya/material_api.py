from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from toupiaoya.constants import BROWSER_CHROME_UA, DEFAULT_TIMEOUT, MATERIAL_API_BASE
from toupiaoya.http import get, post_json

_MATERIAL_SAVE_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "user-agent": BROWSER_CHROME_UA,
}

_MATERIAL_LIST_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "origin": "https://www.toupiaoya.com",
    "user-agent": BROWSER_CHROME_UA,
}


def fetch_user_upload_list(
    access_token: str,
    *,
    file_type: int = 1,
    page_no: int = 1,
    page_size: int = 30,
    tag_id: int = -1,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """
    GET /m/material/user/upload/list2
    用户上传素材列表；fileType=1 表示图片。
    """
    url = f"{MATERIAL_API_BASE}/m/material/user/upload/list2"
    res = get(
        url,
        access_token=access_token,
        params={
            "fileType": file_type,
            "pageNo": page_no,
            "pageSize": page_size,
            "tagId": tag_id,
        },
        extra_headers=dict(_MATERIAL_LIST_HEADERS),
        timeout=timeout,
    )
    res.raise_for_status()
    body = res.json()
    if not isinstance(body, dict):
        raise RuntimeError("list2 返回非 JSON 对象")
    if not body.get("success") or body.get("code") != 200:
        raise RuntimeError(str(body.get("msg") or "素材列表 list2 失败"))
    return body


def save_material_file(
    access_token: str,
    payload: Mapping[str, Any],
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """
    POST /m/material/info/saveFile
    将已上传到 COS 的对象登记到投票鸭素材库。
    """
    url = f"{MATERIAL_API_BASE}/m/material/info/saveFile"
    res = post_json(
        url,
        dict(payload),
        access_token=access_token,
        extra_headers=dict(_MATERIAL_SAVE_HEADERS),
        timeout=timeout,
    )
    res.raise_for_status()
    body = res.json()
    if not isinstance(body, dict):
        raise RuntimeError("saveFile 返回非 JSON 对象")
    if not body.get("success") or body.get("code") != 200:
        raise RuntimeError(str(body.get("msg") or "素材库 saveFile 失败"))
    obj = body.get("obj")
    if not isinstance(obj, dict):
        raise RuntimeError("saveFile 返回缺少 obj")
    return dict(obj)


def build_save_file_payload(
    *,
    cos_key: str,
    local_path: Path,
    logical_bucket: str,
    source: str,
    tag_id: int,
    file_type: int,
    tmb_path: str | None,
) -> dict[str, Any]:
    """组装 saveFile 请求体（path/tmbPath 为 COS 上的 key，name 为展示用本地文件名）。"""
    key = cos_key.lstrip("/")
    tmb = (tmb_path or key).lstrip("/")
    ext = local_path.suffix or ""
    return {
        "path": key,
        "tmbPath": tmb,
        "name": local_path.name,
        "size": local_path.stat().st_size,
        "extName": ext,
        "tagId": tag_id,
        "fileType": file_type,
        "storageType": 0,
        "uploadType": 0,
        "providerType": 1,
        "source": source,
        "bucket": logical_bucket,
    }
