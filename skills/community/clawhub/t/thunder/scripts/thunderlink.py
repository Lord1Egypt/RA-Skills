#!/usr/bin/env python3
"""迅雷/QQ旋风/快车 专用下载链接编解码（纯本地，零依赖）。

用法:
    python3 thunderlink.py decode <thunder://... | qqdl://... | flashget://...>
    python3 thunderlink.py encode <普通URL>
"""
import base64
import sys


def _b64decode(data: str) -> str:
    pad = -len(data) % 4
    return base64.b64decode(data + "=" * pad).decode("utf-8", "replace")


def decode(link: str) -> str:
    low = link.lower()
    if low.startswith("thunder://"):
        raw = _b64decode(link[10:])
        if raw.startswith("AA") and raw.endswith("ZZ"):
            return raw[2:-2]
        return raw
    if low.startswith("qqdl://"):
        return _b64decode(link[7:])
    if low.startswith("flashget://"):
        body = link[11:].split("&", 1)[0]
        raw = _b64decode(body)
        return raw.replace("[FLASHGET]", "")
    raise ValueError("不是可识别的专用链接 (thunder:// qqdl:// flashget://)")


def encode(url: str) -> str:
    payload = ("AA" + url + "ZZ").encode("utf-8")
    return "thunder://" + base64.b64encode(payload).decode("ascii")


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] not in ("decode", "encode"):
        print(__doc__)
        sys.exit(1)
    action, value = sys.argv[1], sys.argv[2]
    try:
        print(decode(value) if action == "decode" else encode(value))
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
