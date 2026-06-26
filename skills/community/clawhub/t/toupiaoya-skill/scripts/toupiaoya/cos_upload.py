from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from toupiaoya.constants import ASSET_PUBLIC_BASE, BROWSER_CHROME_UA, COS_TOKEN_API_BASE, DEFAULT_TIMEOUT
from toupiaoya.http import get

_COS_TOKEN_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "origin": "https://www.toupiaoya.com",
    "user-agent": BROWSER_CHROME_UA,
}


def _cos_bucket_for_sdk(inner: Mapping[str, Any]) -> str:
    """COS PutObject 使用的桶名一般为 bucket-appId。"""
    name = str(inner.get("bucket") or "")
    aid = str(inner.get("appId") or "").strip()
    if aid and not name.endswith("-" + aid):
        return f"{name}-{aid}"
    return name


def build_object_key(prefix: str, object_name: str) -> str:
    """prefix 如 /material/；COS Key 一般不带前导斜杠。"""
    p = prefix.strip().replace("\\", "/")
    if not p.endswith("/"):
        p += "/"
    dir_part = p.lstrip("/")
    name = object_name.lstrip("/")
    if not dir_part:
        return name
    return f"{dir_part}{name}"


def fetch_cos_token(
    access_token: str,
    *,
    bucket: str = "eqxiu",
    prefix: str = "/material/",
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """
    调用投票鸭接口换取 COS 临时凭证。
    GET .../cos/user/token-upload?bucket=eqxiu&prefix=%2Fmaterial%2F
    """
    url = f"{COS_TOKEN_API_BASE}/cos/user/token-upload"
    res = get(
        url,
        access_token=access_token,
        params={"bucket": bucket, "prefix": prefix},
        extra_headers=dict(_COS_TOKEN_HEADERS),
        timeout=timeout,
    )
    res.raise_for_status()
    body = res.json()
    if not isinstance(body, dict):
        raise ValueError("token-upload 返回非 JSON 对象")
    if not body.get("success") or body.get("code") != 200:
        raise RuntimeError(str(body.get("msg") or "获取 COS 凭证失败"))
    inner = body.get("obj")
    if not isinstance(inner, dict):
        raise RuntimeError("token-upload 返回缺少 obj")
    if inner.get("success") is False and inner.get("msg"):
        raise RuntimeError(str(inner.get("msg")))
    for k in ("tmpSecretId", "tmpSecretKey", "sessionToken", "region", "bucket"):
        if not inner.get(k):
            raise RuntimeError(f"COS 凭证字段缺失: {k}")
    return dict(inner)


def put_local_file(inner: dict[str, Any], local_path: Path, object_key: str) -> dict[str, Any]:
    """使用临时密钥通过 COS SDK 上传本地文件。"""
    try:
        from qcloud_cos import CosConfig, CosS3Client
    except ImportError as e:
        raise ImportError(
            "请先安装腾讯云 COS SDK：pip install cos-python-sdk-v5"
        ) from e

    region = str(inner["region"])
    secret_id = str(inner["tmpSecretId"])
    secret_key = str(inner["tmpSecretKey"])
    session_token = str(inner["sessionToken"])
    bucket = _cos_bucket_for_sdk(inner)

    config = CosConfig(
        Region=region,
        SecretId=secret_id,
        SecretKey=secret_key,
        Token=session_token,
        Scheme="https",
    )
    client = CosS3Client(config)

    key = object_key.lstrip("/")
    with local_path.open("rb") as fp:
        resp = client.put_object(Bucket=bucket, Body=fp, Key=key, EnableMD5=False)

    etag = (resp.get("ETag") or resp.get("Etag") or "").strip('"')
    out: dict[str, Any] = {
        "success": True,
        "code": 200,
        "msg": "ok",
        "bucket": bucket,
        "region": region,
        "key": key,
        "etag": etag,
    }
    # 与站内素材 CDN 习惯拼接（不保证所有桶路径均如此暴露）
    out["assetUrl"] = f"{ASSET_PUBLIC_BASE.rstrip('/')}/{key}"
    return out
