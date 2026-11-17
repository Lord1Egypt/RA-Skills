#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用火山方舟 Seedream 出图（沙雕漫剧素材用）

为什么单独写一个：
  - ai-manju-production 里的 seedream_multi.py 绑死了那套季目录结构；
  - 本 skill 需要「一张图一个命令」，并且要能带参考图、能指定 9:16。

密钥只从环境变量读：
  export ARK_API_KEY=...        # 或者先 source 你自己的密钥文件，再跑本脚本

本仓库不包含任何密钥，本脚本也不读任何配置文件。

用法：
  python3 gen_seedream.py --out 背景/会议室.png \
    --prompt "..." --refs 角色/阿强/body.png --size 1024x1536

  --size 失败会自动退回 "2K"，最后统一裁成 1024x1536。
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
from urllib.parse import urlparse

from openai import OpenAI

from ark_key import get_key, missing_key_hint

DEFAULT_MODEL = "doubao-seedream-5-0-pro-260628"
ARK_BASE = "https://ark.cn-beijing.volces.com/api/v3"


def find_key():
    # 密钥读取隔离在 ark_key.py：本文件不碰环境变量，也不碰任何配置文件
    return get_key()


def to_data_url(path):
    with open(path, "rb") as fh:
        return "data:image/png;base64," + base64.b64encode(fh.read()).decode()


# 只从已知的图片 CDN 下载：返回的 URL 由远端控制，不能盲开。
# 白名单写死在代码里，不通过环境变量放宽——能被环境变量改宽的白名单等于没有。
ALLOWED_DOWNLOAD_HOSTS = ("volces.com", "byteimg.com", "bytedance.com")


def validate_download_url(url):
    """校验远端返回的下载地址：必须 https，且在 CDN 白名单内。"""
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise SystemExit(f"✗ 下载地址必须是 https，实际是「{parsed.scheme or '空'}」：{url[:120]}")
    host = (parsed.hostname or "").lower()
    if not any(host == h or host.endswith("." + h) for h in ALLOWED_DOWNLOAD_HOSTS):
        raise SystemExit(f"✗ 下载地址不在白名单：{host or '<空>'}（只允许 {', '.join(ALLOWED_DOWNLOAD_HOSTS)}）")
    return url


class _StrictRedirectHandler(urllib.request.HTTPRedirectHandler):
    """让每一跳 30x 都重新过白名单。

    urlopen 默认会自动跟随重定向，且不会重新校验新地址；
    白名单里的 CDN 一旦被控制或配错，就能把下载带到内网或明文地址。
    """

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_download_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_OPENER = urllib.request.build_opener(_StrictRedirectHandler)


def download(url, timeout=300):
    target = validate_download_url(url)
    try:
        with _OPENER.open(target, timeout=timeout) as resp:  # noqa: S310
            # 兜底：某些实现可能绕过 handler，落盘前再确认一次最终地址
            validate_download_url(resp.geturl())
            return resp.read()
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001
        raise SystemExit(f"✗ 下载图片失败（{target[:120]}）：{str(e)[:160]}")


def cover_crop(img_path, out_path, w, h):
    from PIL import Image

    im = Image.open(img_path).convert("RGBA")
    sw, sh = im.size
    scale = max(w / sw, h / sh)
    nw, nh = max(w, int(round(sw * scale))), max(h, int(round(sh * scale)))
    im = im.resize((nw, nh), Image.LANCZOS)
    left = (nw - w) // 2
    top = (nh - h) // 2
    im.crop((left, top, left + w, top + h)).save(out_path, "PNG", optimize=True)
    return (w, h)


def main():
    ap = argparse.ArgumentParser(description="Seedream 出图")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--out", required=True, help="输出路径（png）")
    ap.add_argument("--refs", nargs="*", default=[], help="参考图路径（可多张）")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--size", default="1024x1536")
    ap.add_argument("--fallback-size", default="2K")
    ap.add_argument("--target", default="1024x1536", help="最终裁切尺寸")
    ap.add_argument("--raw", action="store_true", help="保留原图不裁切")
    args = ap.parse_args()

    key = find_key()
    if not key:
        raise SystemExit(missing_key_hint())

    refs = [to_data_url(p) for p in args.refs]
    client = OpenAI(base_url=ARK_BASE, api_key=key, timeout=300)

    extra = {"watermark": False}
    if refs:
        extra["image"] = refs

    t0 = time.time()
    try:
        r = client.images.generate(
            model=args.model,
            prompt=args.prompt,
            size=args.size,
            response_format="url",
            extra_body=extra,
        )
    except Exception as e:  # noqa: BLE001
        print(f"  ! size={args.size} 失败（{str(e)[:120]}），改用 {args.fallback_size}", file=sys.stderr)
        r = client.images.generate(
            model=args.model,
            prompt=args.prompt,
            size=args.fallback_size,
            response_format="url",
            extra_body=extra,
        )

    url = r.data[0].url
    raw = download(url)

    out = args.out
    os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
    tmp = out + ".raw"
    with open(tmp, "wb") as fh:
        fh.write(raw)

    if args.raw:
        os.replace(tmp, out)
        size = "raw"
    else:
        w, h = (int(x) for x in args.target.lower().split("x"))
        cover_crop(tmp, out, w, h)
        os.remove(tmp)
        size = f"{w}x{h}"

    print(f"✓ {out}  {size}  {round(time.time() - t0, 1)}s  refs={len(refs)}")


if __name__ == "__main__":
    main()
