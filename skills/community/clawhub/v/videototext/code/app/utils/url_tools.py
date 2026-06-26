from urllib.parse import parse_qs, urlparse

import httpx

from app.core.errors import AppError, ErrorCodes


def expand_short_url(url: str, timeout_seconds: int = 20) -> str:
    parsed = urlparse(url)
    if "b23.tv" not in parsed.netloc.lower():
        return url
    try:
        with httpx.Client(timeout=timeout_seconds, follow_redirects=True) as client:
            response = client.get(url)
            return str(response.url)
    except Exception as exc:
        raise AppError(ErrorCodes.INVALID_URL, f"短链展开失败: {exc}", 400) from exc


def detect_platform(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if "bilibili.com" in host or "b23.tv" in host:
        return "bilibili"
    raise AppError(ErrorCodes.UNSUPPORTED_PLATFORM, "当前仅支持 B 站链接", 400)


def parse_bilibili_identity(url: str) -> dict:
    parsed = urlparse(url)
    parts = [part for part in parsed.path.split("/") if part]
    bvid = None
    for idx, part in enumerate(parts):
        if part == "video" and idx + 1 < len(parts):
            bvid = parts[idx + 1]
            break
        if part.startswith("BV"):
            bvid = part
            break
    if not bvid:
        raise AppError(ErrorCodes.INVALID_URL, "未识别到有效的 B 站 BV 号", 400)
    query = parse_qs(parsed.query)
    page = int(query.get("p", ["1"])[0] or "1")
    if page < 1:
        page = 1
    return {"bvid": bvid, "page": page}
