"""
QR Code Decoder - 本地 zxing 解码。

用法:
  python scripts/decode.py <图片路径或URL>
  python scripts/decode.py --file <本地文件路径>
  python scripts/decode.py --url <图片URL>

输出 JSON:
  {"source": "zxing", "contents": ["..."]}
  错误时: {"error": "..."}
"""

import sys
import json
import os
import tempfile
from pathlib import Path


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


def output(source: str, contents: list[str]):
    print(json.dumps({"source": source, "contents": contents}, ensure_ascii=False))
    sys.exit(0)


def error(msg: str):
    print(json.dumps({"error": msg}, ensure_ascii=False))
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        error("用法: python decode.py <图片路径或URL>")

    args = sys.argv[1:]

    if not args:
        error("用法: python decode.py <图片路径或URL>")

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

        results = decode_with_zxing(target)
        if results:
            output("zxing", results)

        error("无法解码: 本地 zxing 未识别到二维码")

    else:  # --url
        tmp_path = None
        try:
            tmp_path = download_image(target)
            results = decode_with_zxing(tmp_path)
            if results:
                output("zxing", results)
        except RuntimeError as e:
            error(str(e))
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)

        error("无法解码: 本地 zxing 未识别到二维码")


if __name__ == "__main__":
    main()
