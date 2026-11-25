#!/usr/bin/env python3
"""上传图片/视频/音频文件到 VoooAI：通过 COS 三步上传流程

流程：
1. POST /api/cos/request-upload — 获取预签名URL和file_id
2. PUT <presigned_url> — 直传文件到COS
3. POST /api/cos/confirm-upload — 确认上传并获取文件URL
"""

import argparse
import hashlib
import mimetypes
import os
import sys
import urllib.request
import urllib.error

sys.path.insert(0, os.path.dirname(__file__))
from _common import BASE_URL, json_output, error_exit, api_post, api_get

# 允许的 MIME 类型前缀
ALLOWED_PREFIXES = ("image/", "video/", "audio/")

# 文件大小限制（与 cos_config.py 保持一致）
MAX_SIZE_MB = {
    "image": 10,
    "video": 200,
    "audio": 15,
}


def _detect_file_category(mime_type: str) -> str:
    """根据 MIME 类型判断文件类别"""
    if mime_type.startswith("image/"):
        return "image"
    elif mime_type.startswith("video/"):
        return "video"
    elif mime_type.startswith("audio/"):
        return "audio"
    return "unknown"


def _compute_md5(file_path: str) -> str:
    """计算文件的 MD5 哈希值"""
    md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            md5.update(chunk)
    return md5.hexdigest()


def upload_file(file_path: str) -> dict:
    """
    上传本地文件到 VoooAI 平台（COS 三步上传）。
    
    Args:
        file_path: 本地文件路径
    
    Returns:
        上传结果字典，包含 url 和 file_type
    """
    if not os.path.isfile(file_path):
        error_exit(f"文件不存在: {file_path}")
    
    # 检查 MIME 类型
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type and not any(mime_type.startswith(p) for p in ALLOWED_PREFIXES):
        error_exit(f"不支持的文件类型: {mime_type}，仅支持图片、视频和音频")
    
    content_type = mime_type or "application/octet-stream"
    category = _detect_file_category(content_type)
    
    # 检查文件大小
    file_size = os.path.getsize(file_path)
    max_mb = MAX_SIZE_MB.get(category, 15)
    if file_size > max_mb * 1024 * 1024:
        error_exit(f"文件过大: {file_size / 1024 / 1024:.1f}MB（{category} 最大 {max_mb}MB）")
    
    filename = os.path.basename(file_path)
    file_md5 = _compute_md5(file_path)
    
    # ── Step 1: 请求上传凭证 ──────────────────────────────────────
    print(f"正在请求上传凭证...", file=sys.stderr)
    request_data = {
        "filename": filename,
        "file_size": file_size,
        "file_md5": file_md5,
    }
    resp = api_post("/api/cos/request-upload", request_data)
    
    if not resp.get("success"):
        error_exit(f"请求上传凭证失败: {resp.get('error', resp.get('message', '未知错误'))}")
    
    upload_data = resp.get("data", {})
    file_id = upload_data.get("file_id", "")
    upload_url = upload_data.get("upload_url", "")
    status = upload_data.get("status", "")
    
    # 如果文件已存在（MD5 去重），直接返回
    if status == "exists":
        print(f"文件已存在（MD5去重命中），跳过上传", file=sys.stderr)
        # 获取已有文件的下载URL
        download_resp = api_get(f"/api/cos/download-url/{file_id}")
        file_url = ""
        if download_resp.get("success"):
            file_url = download_resp.get("data", {}).get("download_url", "")
        return {
            "url": file_url,
            "file_type": content_type,
            "file_name": filename,
            "file_size_bytes": file_size,
            "file_id": file_id,
            "status": "exists",
        }
    
    if not upload_url:
        error_exit("上传凭证中缺少 upload_url")
    
    # ── Step 2: 直传文件到 COS ──────────────────────────────────────
    print(f"正在上传文件到 COS...", file=sys.stderr)
    
    with open(file_path, "rb") as f:
        file_content = f.read()
    
    req = urllib.request.Request(
        upload_url,
        data=file_content,
        method="PUT",
        headers={
            "Content-Type": content_type,
            "Content-Length": str(file_size),
        },
    )
    try:
        timeout = 300 if file_size > 50 * 1024 * 1024 else 120
        with urllib.request.urlopen(req, timeout=timeout) as cos_resp:
            if cos_resp.status not in (200, 201, 204):
                error_exit(f"COS 上传失败: HTTP {cos_resp.status}")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8") if e.fp else ""
        error_exit(f"COS 上传失败: HTTP {e.code} - {err_body}")
    except urllib.error.URLError as e:
        error_exit(f"COS 网络错误: {e.reason}")
    
    # ── Step 3: 确认上传 ──────────────────────────────────────
    print(f"正在确认上传...", file=sys.stderr)
    confirm_data = {
        "file_id": file_id,
    }
    confirm_resp = api_post("/api/cos/confirm-upload", confirm_data)
    
    if not confirm_resp.get("success"):
        # 确认失败但文件可能已上传成功，输出警告而非终止
        print(f"警告：确认上传失败: {confirm_resp.get('error', confirm_resp.get('message', '未知错误'))}", file=sys.stderr)
    
    # 获取下载 URL
    download_resp = api_get(f"/api/cos/download-url/{file_id}")
    file_url = ""
    if download_resp.get("success"):
        file_url = download_resp.get("data", {}).get("download_url", "")
    
    if not file_url:
        # 回退：使用 COS 路径构造 URL
        cos_key = upload_data.get("cos_key", "")
        if cos_key:
            file_url = f"{BASE_URL.rstrip('/')}/api/cos/download-url/{file_id}"
    
    return {
        "url": file_url,
        "file_type": content_type,
        "file_name": filename,
        "file_size_bytes": file_size,
        "file_id": file_id,
        "status": "uploaded",
    }


def main():
    parser = argparse.ArgumentParser(
        description="上传图片、视频或音频文件到 VoooAI 平台（COS 三步上传）",
        epilog="""
环境变量:
  VOOOAI_ACCESS_KEY  必填，Bearer 鉴权
  VOOOAI_BASE_URL    可选，默认 https://voooai.com

上传流程（COS 三步上传）:
  1. POST /api/cos/request-upload — 获取预签名URL和file_id
  2. PUT <presigned_url> — 直传文件到COS
  3. POST /api/cos/confirm-upload — 确认上传并获取文件URL

支持的文件类型:
  - 图片: jpg, jpeg, png, webp, gif, svg, bmp (最大 10MB)
  - 视频: mp4, mov, avi, mkv, webm (最大 200MB)
  - 音频: mp3, wav, flac, m4a, ogg (最大 15MB)

特性:
  - MD5 去重：相同文件不会重复上传
  - 大文件支持：视频最大 200MB
  - 自动分类：根据文件类型应用对应大小限制

示例:
  # 上传参考图片
  python3 upload_file.py /path/to/image.png

  # 上传参考视频
  python3 upload_file.py /path/to/video.mp4

  # 上传参考音频
  python3 upload_file.py /path/to/audio.mp3
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "file",
        help="要上传的图片、视频或音频文件路径",
    )
    args = parser.parse_args()

    result = upload_file(args.file)
    
    if not result.get("url"):
        error_exit("上传成功但未返回文件 URL")
    
    out = {
        "file_url": result["url"],
        "file_type": result["file_type"],
        "file_name": result["file_name"],
        "file_size_bytes": result["file_size_bytes"],
        "file_id": result.get("file_id", ""),
        "status": result.get("status", ""),
    }
    json_output(out)


if __name__ == "__main__":
    main()
