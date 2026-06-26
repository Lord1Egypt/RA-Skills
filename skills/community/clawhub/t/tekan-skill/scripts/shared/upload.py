"""Upload local files to Tekan S3 and return fileId.

Used internally by avatar4, video_gen, ecommerce_image, etc.

Two upload modes:
  1. Legacy (upload_file): via /v1/upload/credential — for avatar4, video_gen, etc.
  2. S3 SDK (ecommerce_upload): via S3 temporary credentials — for ecommerce_image.
     This mode uploads to the correct S3 path prefix so that the LLM backend
     can access images through CloudFront.
"""

import os
import sys
import uuid
from typing import Optional

import requests as _requests

from .client import TopviewClient, TEKAN_API_URL

TEKAN_S3_API_URL = "https://api.tekan.cn:8095"

SUPPORTED_FORMATS = {
    "png", "jpg", "jpeg", "bmp", "webp",
    "mp3", "wav", "m4a",
    "mp4", "avi", "mov",
}


def detect_format(file_path: str) -> str:
    """Return file extension if supported, else raise SystemExit."""
    ext = os.path.splitext(file_path)[1].lstrip(".").lower()
    if ext not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported format '{ext}'. "
            f"Supported: {', '.join(sorted(SUPPORTED_FORMATS))}"
        )
    return ext


def upload_file(file_path: str, fmt: str, *, quiet: bool = False,
                client: Optional[TopviewClient] = None) -> dict:
    """Three-step upload: get credential -> PUT to S3 -> verify.

    Returns dict with keys: fileId, fileName, format.
    """
    if client is None:
        client = TopviewClient()

    if not quiet:
        print(f"[1/3] Requesting upload credential (format={fmt})...", file=sys.stderr)

    cred = client.get("/v1/upload/credential", params={
        "format": fmt,
        "needAccelerateUrl": "",
    })

    file_id = cred["fileId"]
    upload_url = cred["uploadUrl"]
    file_name = cred.get("fileName", "")

    if not quiet:
        print(f"[2/3] Uploading {os.path.basename(file_path)} to S3...", file=sys.stderr)

    client.put_file(upload_url, file_path)

    if not quiet:
        print("[3/3] Verifying upload...", file=sys.stderr)

    check = client.get("/v1/upload/check", params={"fileId": file_id})

    if check is not True and str(check) != "true":
        raise RuntimeError("Upload verification failed")

    if not quiet:
        print("Upload complete.", file=sys.stderr)

    return {"fileId": file_id, "fileName": file_name, "format": fmt}


_CDN_PROXY_PREFIX = "/cdn-proxy/"
_CLOUDFRONT_BASE = "https://dr1coeak04nbk.cloudfront.net/"

_EXT_TO_MIME = {
    "png": "image/png",
    "webp": "image/webp",
    "gif": "image/gif",
}


def get_file_url(file_path: str, *, uid: Optional[str] = None,
                 client: Optional[TopviewClient] = None) -> str:
    """Convert an S3 path to an accessible URL via the /s3/file/url endpoint."""
    url = f"{TEKAN_S3_API_URL}/s3/file/url"
    if uid:
        headers = {"uid": uid, "Content-Type": "application/json"}
    else:
        if client is None:
            client = TopviewClient()
        headers = {"uid": client._uid, "Content-Type": "application/json"}
    resp = _requests.get(url, headers=headers, params={"filePath": file_path})
    resp.raise_for_status()
    data = resp.json()
    code = str(data.get("code", ""))
    if code != "200":
        raise RuntimeError(f"get_file_url failed: {data}")
    result = data.get("result", {})
    file_url = result.get("fileUrl", "") if isinstance(result, dict) else str(result)
    if file_url.startswith(_CDN_PROXY_PREFIX):
        file_url = file_url.replace(_CDN_PROXY_PREFIX, _CLOUDFRONT_BASE, 1)
    return file_url


def upload_and_get_url(file_path: str, *, quiet: bool = False,
                       client: Optional[TopviewClient] = None) -> dict:
    """Upload a local file to S3 and return fileId + accessible URL + mimeType.

    Returns dict with keys: fileId, fileUrl, mimeType.
    """
    fmt = detect_format(file_path)
    result = upload_file(file_path, fmt, quiet=quiet, client=client)
    file_id = result["fileId"]

    if not quiet:
        print(f"Resolving accessible URL for {file_id}...", file=sys.stderr)

    file_url = get_file_url(file_id, client=client)
    mime_type = _EXT_TO_MIME.get(fmt, "image/jpeg")

    if not quiet:
        print(f"Accessible URL: {file_url}", file=sys.stderr)

    return {"fileId": file_id, "fileUrl": file_url, "mimeType": mime_type}


def resolve_local_file(file_ref: str, *, quiet: bool = False,
                       client: Optional[TopviewClient] = None) -> str:
    """If file_ref is a local path, upload it and return fileId. Otherwise pass through."""
    if os.path.isfile(file_ref):
        if not quiet:
            print(f"Detected local file, uploading: {file_ref}", file=sys.stderr)
        fmt = detect_format(file_ref)
        result = upload_file(file_ref, fmt, quiet=quiet, client=client)
        file_id = result["fileId"]
        if not quiet:
            print(f"Uploaded. fileId: {file_id}", file=sys.stderr)
        return file_id
    return file_ref


# ---------------------------------------------------------------------------
# E-commerce image upload: S3 SDK mode (matches web frontend behaviour)
# ---------------------------------------------------------------------------

_ECOMMERCE_S3_PREFIX = "analyzed_video/task/product_detail_image"

# aigc-web ProductMainImageEcomm: useRemoveBackground + generateS3UploadPath
# pathPrefix = f"{PRODUCT_MAIN_IMAGE_S3_PREFIX}/{teamId}/product"
# -> analyzed_video/task/product_main_image/{teamId}/product/{teamId}/{nanoid}.ext
_PRODUCT_MAIN_IMAGE_PREFIX = "analyzed_video/task/product_main_image"


def _get_s3_credentials(uid: str) -> dict:
    """GET /s3/upload/credentials from TEKAN_S3_API_URL."""
    url = f"{TEKAN_S3_API_URL}/s3/upload/credentials"
    resp = _requests.get(url, headers={"uid": uid, "Content-Type": "application/json"})
    resp.raise_for_status()
    data = resp.json()
    if str(data.get("code", "")) != "200":
        raise RuntimeError(f"Failed to get S3 credentials: {data}")
    return data["result"]


def _ecommerce_s3_path(uid: str, ext: str) -> str:
    """Generate an S3 key matching the web frontend pattern."""
    nano = uuid.uuid4().hex[:21]
    return f"{_ECOMMERCE_S3_PREFIX}/{uid}/anonymous/{nano}.{ext}"


def _product_main_image_s3_path(uid: str, ext: str) -> str:
    """Same S3 layout as apps/base/.../ProductMainImageEcomm useRemoveBackground."""
    u = uid or "anonymous"
    nano = uuid.uuid4().hex[:21]
    return f"{_PRODUCT_MAIN_IMAGE_PREFIX}/{u}/product/{u}/{nano}.{ext}"


def product_main_image_upload(file_path: str, uid: str, *,
                              quiet: bool = False) -> dict:
    """Upload product image for remove_background — matches web product_main_image path + S3 SDK."""
    import boto3

    ext = detect_format(file_path)
    mime = _EXT_TO_MIME.get(ext, "image/jpeg")

    if not quiet:
        print("Getting S3 credentials (product main image path)...", file=sys.stderr)
    creds = _get_s3_credentials(uid or "anonymous")

    s3_key = _product_main_image_s3_path(uid, ext)
    if not quiet:
        print(f"Uploading to s3://{creds['bucket']}/{s3_key}...", file=sys.stderr)

    s3 = boto3.client(
        "s3",
        region_name=creds["region"],
        aws_access_key_id=creds["accessKeyId"],
        aws_secret_access_key=creds["secretAccessKey"],
        aws_session_token=creds["sessionToken"],
    )
    s3.upload_file(file_path, creds["bucket"], s3_key,
                   ExtraArgs={"ContentType": mime})

    if not quiet:
        print("Resolving CloudFront URL...", file=sys.stderr)
    file_url = get_file_url(s3_key, uid=uid or "anonymous")

    if not quiet:
        print(f"Accessible URL: {file_url[:100]}...", file=sys.stderr)

    return {"s3Path": s3_key, "fileUrl": file_url, "mimeType": mime}


def _product_main_image_ref_s3_path(uid: str, ext: str) -> str:
    """S3 key for reference image — matches useReferenceImageUpload.ts subPath='reference'."""
    u = uid or "anonymous"
    nano = uuid.uuid4().hex[:21]
    return f"{_PRODUCT_MAIN_IMAGE_PREFIX}/{u}/reference/{u}/{nano}.{ext}"


def product_main_image_reference_upload(file_path: str, uid: str, *,
                                         quiet: bool = False) -> dict:
    """Upload reference image for product_main_image — matches web reference/ path."""
    import boto3

    ext = detect_format(file_path)
    mime = _EXT_TO_MIME.get(ext, "image/jpeg")

    if not quiet:
        print("Getting S3 credentials (product main image reference)...", file=sys.stderr)
    creds = _get_s3_credentials(uid or "anonymous")

    s3_key = _product_main_image_ref_s3_path(uid, ext)
    if not quiet:
        print(f"Uploading to s3://{creds['bucket']}/{s3_key}...", file=sys.stderr)

    s3 = boto3.client(
        "s3",
        region_name=creds["region"],
        aws_access_key_id=creds["accessKeyId"],
        aws_secret_access_key=creds["secretAccessKey"],
        aws_session_token=creds["sessionToken"],
    )
    s3.upload_file(file_path, creds["bucket"], s3_key,
                   ExtraArgs={"ContentType": mime})

    if not quiet:
        print("Resolving CloudFront URL...", file=sys.stderr)
    file_url = get_file_url(s3_key, uid=uid or "anonymous")

    if not quiet:
        print(f"Accessible URL: {file_url[:100]}...", file=sys.stderr)

    return {"s3Path": s3_key, "fileUrl": file_url, "mimeType": mime}


def ecommerce_upload(file_path: str, uid: str, *,
                     quiet: bool = False) -> dict:
    """Upload a local image via S3 SDK + get CloudFront signed URL.

    This replicates the web frontend upload path so that the LLM backend
    (enhance-prompt) can access the image.

    Returns dict with keys: s3Path, fileUrl, mimeType.
    """
    import boto3

    ext = detect_format(file_path)
    mime = _EXT_TO_MIME.get(ext, "image/jpeg")

    if not quiet:
        print("Getting S3 credentials...", file=sys.stderr)
    creds = _get_s3_credentials(uid)

    s3_key = _ecommerce_s3_path(uid, ext)
    if not quiet:
        print(f"Uploading to s3://{creds['bucket']}/{s3_key}...", file=sys.stderr)

    s3 = boto3.client(
        "s3",
        region_name=creds["region"],
        aws_access_key_id=creds["accessKeyId"],
        aws_secret_access_key=creds["secretAccessKey"],
        aws_session_token=creds["sessionToken"],
    )
    s3.upload_file(file_path, creds["bucket"], s3_key,
                   ExtraArgs={"ContentType": mime})

    if not quiet:
        print("Resolving CloudFront URL...", file=sys.stderr)
    file_url = get_file_url(s3_key, uid=uid)

    if not quiet:
        print(f"Accessible URL: {file_url[:100]}...", file=sys.stderr)

    return {"s3Path": s3_key, "fileUrl": file_url, "mimeType": mime}
