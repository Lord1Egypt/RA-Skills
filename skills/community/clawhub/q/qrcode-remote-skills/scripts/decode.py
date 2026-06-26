"""
QR Code Decoder - 本地 zxing 优先，失败时回退到草料 API。

用法:
  python scripts/decode.py <图片路径或URL>
  python scripts/decode.py --file <本地文件路径>
  python scripts/decode.py --url <图片URL>

输出 JSON:
  {"source": "zxing"|"api", "contents": ["..."]}
  错误时: {"error": "..."}
"""

import sys
import json
import os
import tempfile
from pathlib import Path
from urllib.parse import quote

API_ENDPOINT = "https://api.2dcode.biz/v1/read-qr-code"


def is_url(s: str) -> bool:
    return s.startswith("http://") or s.startswith("https://")


def download_image(url: str) -> str:
    """下载图片到临时文件，返回临时文件路径。"""
    import urllib.request

    suffix = Path(url.split("?")[0]).suffix or ".png"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    try:
        urllib.request.urlretrieve(url, tmp.name)
    except Exception as e:
        tmp.close()
        os.unlink(tmp.name)
        raise RuntimeError(f"下载图片失败: {e}")
    tmp.close()
    return tmp.name


def decode_with_zxing(image_path: str) -> list[str] | None:
    """使用 zxingcpp 本地解码，成功返回内容列表，失败返回 None。"""
    try:
        import zxingcpp
        from PIL import Image

        img = Image.open(image_path)
        results = zxingcpp.read_barcodes(img)
        if results:
            return [r.text for r in results]
        return None
    except ImportError:
        return None
    except Exception:
        return None


def decode_with_api_url(image_url: str) -> list[str] | None:
    """通过 GET 方式调用草料 API 解码图片 URL。"""
    import urllib.request

    api_url = f"{API_ENDPOINT}?file_url={quote(image_url, safe='')}"
    try:
        with urllib.request.urlopen(api_url) as resp:
            data = json.loads(resp.read().decode())
        if data.get("code") == 0 and data.get("data", {}).get("contents"):
            return data["data"]["contents"]
        return None
    except Exception:
        return None


def decode_with_api_file(file_path: str) -> list[str] | None:
    """通过 POST multipart 方式调用草料 API 解码本地文件。"""
    import urllib.request
    import mimetypes
    import uuid

    boundary = uuid.uuid4().hex
    filename = os.path.basename(file_path)
    mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"

    with open(file_path, "rb") as f:
        file_data = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: {mime_type}\r\n\r\n"
    ).encode() + file_data + f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        API_ENDPOINT,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        if data.get("code") == 0 and data.get("data", {}).get("contents"):
            return data["data"]["contents"]
        return None
    except Exception:
        return None


def output(source: str, contents: list[str]):
    print(json.dumps({"source": source, "contents": contents}, ensure_ascii=False))
    sys.exit(0)


def error(msg: str):
    print(json.dumps({"error": msg}, ensure_ascii=False))
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        error("用法: python decode.py [--force-api] <图片路径或URL>")

    args = sys.argv[1:]
    force_api = False
    if "--force-api" in args:
        force_api = True
        args.remove("--force-api")

    if not args:
        error("用法: python decode.py [--force-api] <图片路径或URL>")

    arg1 = args[0]
    if arg1 in ("--file", "--url") and len(args) >= 2:
        mode = arg1
        target = args[1]
    else:
        target = arg1
        mode = "--url" if is_url(target) else "--file"

    if mode == "--file":
        if not os.path.isfile(target):
            error(f"文件不存在: {target}")

        if not force_api:
            results = decode_with_zxing(target)
            if results:
                output("zxing", results)

        results = decode_with_api_file(target)
        if results:
            output("api", results)

        error("无法解码: 本地 zxing 和远程 API 均未识别到二维码")

    else:  # --url
        if not force_api:
            tmp_path = None
            try:
                tmp_path = download_image(target)
                results = decode_with_zxing(tmp_path)
                if results:
                    output("zxing", results)
            except RuntimeError:
                pass
            finally:
                if tmp_path and os.path.exists(tmp_path):
                    os.unlink(tmp_path)

        results = decode_with_api_url(target)
        if results:
            output("api", results)

        error("无法解码: 远程 API 未识别到二维码")


if __name__ == "__main__":
    main()
